"""
分布式存储协调代理审稿修改模型
Distributed Storage Coordination Agent - Manuscript Review System

Architecture:
- EIC (Editor-in-Chief) Agent: 统筹指导，协调审稿流程
- Reviewer Agent(s): 审稿评分，提供修改意见
- Author Agent: 根据反馈修改稿件

Workflow:
  Author submits → EIC assigns reviewers → Reviewers provide feedback
  → Author revises → EIC re-coordinates review → Loop until satisfied
"""

import streamlit as st
import json
import uuid
import time
import random
import hashlib
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Literal
from enum import Enum
import pandas as pd


# ============================================================
# 1. 数据模型 (Data Models)
# ============================================================

class ReviewDecision(str, Enum):
    ACCEPT = "accept"
    MINOR_REVISION = "minor_revision"
    MAJOR_REVISION = "major_revision"
    REJECT = "reject"
    PENDING = "pending"


class AgentRole(str, Enum):
    EIC = "eic"
    REVIEWER = "reviewer"
    AUTHOR = "author"


class MessageType(str, Enum):
    SUBMIT = "submit"
    ASSIGN = "assign"
    REVIEW = "review"
    FEEDBACK_SUMMARY = "feedback_summary"
    REVISION = "revision"
    DECISION = "decision"
    RE_REVIEW = "re_review"
    FINAL_DECISION = "final_decision"


@dataclass
class AgentMessage:
    """代理间通信消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    sender: str = ""
    sender_role: str = ""
    receiver: str = ""
    receiver_role: str = ""
    msg_type: str = ""
    content: str = ""
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    round_number: int = 1


@dataclass
class ReviewComment:
    """单条审稿意见"""
    reviewer_id: str = ""
    category: str = ""  # methodology, writing, novelty, data, structure
    severity: str = ""  # critical, major, minor, suggestion
    comment: str = ""
    addressed: bool = False
    response: str = ""


@dataclass
class ReviewReport:
    """审稿报告"""
    reviewer_id: str = ""
    reviewer_name: str = ""
    round_number: int = 1
    decision: str = ReviewDecision.PENDING.value
    overall_score: float = 0.0
    scores: dict = field(default_factory=dict)
    comments: list = field(default_factory=list)
    summary: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class ManuscriptVersion:
    """稿件版本"""
    version: int = 1
    title: str = ""
    abstract: str = ""
    content_sections: dict = field(default_factory=dict)
    revision_notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    content_hash: str = ""


@dataclass
class ManuscriptState:
    """稿件全局状态"""
    manuscript_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    current_round: int = 1
    max_rounds: int = 5
    status: str = "submitted"  # submitted, under_review, revision_requested, revised, accepted, rejected
    current_version: int = 1
    versions: list = field(default_factory=list)
    review_reports: list = field(default_factory=list)
    eic_decisions: list = field(default_factory=list)
    message_log: list = field(default_factory=list)
    assigned_reviewers: list = field(default_factory=list)


# ============================================================
# 2. 分布式存储协调引擎 (Distributed Storage Coordinator)
# ============================================================

class DistributedStore:
    """
    分布式存储协调器
    模拟多代理间的状态同步与消息传递

    Storage Partitions:
    - manuscripts: 稿件版本存储
    - reviews: 审稿报告存储
    - messages: 代理间消息队列
    - agent_states: 各代理状态
    - coordination: 协调元数据
    """

    def __init__(self):
        if 'store_manuscripts' not in st.session_state:
            st.session_state.store_manuscripts = {}
        if 'store_reviews' not in st.session_state:
            st.session_state.store_reviews = {}
        if 'store_messages' not in st.session_state:
            st.session_state.store_messages = []
        if 'store_agent_states' not in st.session_state:
            st.session_state.store_agent_states = {}
        if 'store_coordination' not in st.session_state:
            st.session_state.store_coordination = {
                'lock_owner': None,
                'round_status': {},
                'pending_actions': [],
                'event_log': []
            }

    def acquire_lock(self, agent_id: str) -> bool:
        """获取分布式锁"""
        coord = st.session_state.store_coordination
        if coord['lock_owner'] is None or coord['lock_owner'] == agent_id:
            coord['lock_owner'] = agent_id
            return True
        return False

    def release_lock(self, agent_id: str):
        """释放分布式锁"""
        coord = st.session_state.store_coordination
        if coord['lock_owner'] == agent_id:
            coord['lock_owner'] = None

    def store_manuscript(self, ms_id: str, version: dict):
        """存储稿件版本"""
        if ms_id not in st.session_state.store_manuscripts:
            st.session_state.store_manuscripts[ms_id] = []
        st.session_state.store_manuscripts[ms_id].append(version)
        self._log_event(f"Manuscript {ms_id} v{version.get('version', '?')} stored")

    def get_manuscript_versions(self, ms_id: str) -> list:
        """获取稿件所有版本"""
        return st.session_state.store_manuscripts.get(ms_id, [])

    def get_latest_version(self, ms_id: str) -> Optional[dict]:
        """获取稿件最新版本"""
        versions = self.get_manuscript_versions(ms_id)
        return versions[-1] if versions else None

    def store_review(self, ms_id: str, review: dict):
        """存储审稿报告"""
        key = f"{ms_id}_r{review.get('round_number', 1)}"
        if key not in st.session_state.store_reviews:
            st.session_state.store_reviews[key] = []
        st.session_state.store_reviews[key].append(review)
        self._log_event(f"Review stored: {review.get('reviewer_name', '?')} for {ms_id} round {review.get('round_number', 1)}")

    def get_reviews(self, ms_id: str, round_number: int) -> list:
        """获取指定轮次审稿报告"""
        key = f"{ms_id}_r{round_number}"
        return st.session_state.store_reviews.get(key, [])

    def send_message(self, msg: AgentMessage):
        """发送代理间消息"""
        st.session_state.store_messages.append(asdict(msg))
        self._log_event(f"Message [{msg.msg_type}]: {msg.sender}({msg.sender_role}) → {msg.receiver}({msg.receiver_role})")

    def get_messages(self, receiver: str = None, msg_type: str = None) -> list:
        """获取消息"""
        msgs = st.session_state.store_messages
        if receiver:
            msgs = [m for m in msgs if m['receiver'] == receiver]
        if msg_type:
            msgs = [m for m in msgs if m['msg_type'] == msg_type]
        return msgs

    def update_agent_state(self, agent_id: str, state: dict):
        """更新代理状态"""
        st.session_state.store_agent_states[agent_id] = {
            **state,
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_agent_state(self, agent_id: str) -> dict:
        """获取代理状态"""
        return st.session_state.store_agent_states.get(agent_id, {})

    def _log_event(self, event: str):
        """记录协调事件"""
        st.session_state.store_coordination['event_log'].append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'event': event
        })

    def get_event_log(self) -> list:
        """获取事件日志"""
        return st.session_state.store_coordination['event_log']

    def reset(self):
        """重置所有存储"""
        st.session_state.store_manuscripts = {}
        st.session_state.store_reviews = {}
        st.session_state.store_messages = []
        st.session_state.store_agent_states = {}
        st.session_state.store_coordination = {
            'lock_owner': None,
            'round_status': {},
            'pending_actions': [],
            'event_log': []
        }


# ============================================================
# 3. 代理实现 (Agent Implementations)
# ============================================================

# --- 审稿知识库 (Review Knowledge Base) ---

REVIEW_DIMENSIONS = {
    "novelty": {"name": "创新性 (Novelty)", "weight": 0.25,
                "criteria": "研究的原创性和创新程度"},
    "methodology": {"name": "方法论 (Methodology)", "weight": 0.25,
                     "criteria": "研究方法的严谨性和适当性"},
    "writing": {"name": "写作质量 (Writing Quality)", "weight": 0.15,
                "criteria": "论文结构、语言表达和逻辑性"},
    "significance": {"name": "重要性 (Significance)", "weight": 0.20,
                      "criteria": "研究对领域的贡献和影响"},
    "data_analysis": {"name": "数据分析 (Data Analysis)", "weight": 0.15,
                       "criteria": "数据处理和分析的正确性"}
}

REVIEWER_PROFILES = [
    {
        "id": "reviewer_1", "name": "Reviewer A (方法论专家)",
        "expertise": ["methodology", "data_analysis"],
        "strictness": 0.7, "personality": "严谨型",
        "focus_areas": ["实验设计", "统计分析", "可重复性"]
    },
    {
        "id": "reviewer_2", "name": "Reviewer B (领域专家)",
        "expertise": ["novelty", "significance"],
        "strictness": 0.5, "personality": "建设型",
        "focus_areas": ["文献综述", "创新点", "理论贡献"]
    },
    {
        "id": "reviewer_3", "name": "Reviewer C (写作专家)",
        "expertise": ["writing", "methodology"],
        "strictness": 0.6, "personality": "细致型",
        "focus_areas": ["论文结构", "图表质量", "语言表达"]
    }
]

# --- 常见审稿意见模板 ---
REVIEW_TEMPLATES = {
    "methodology": {
        "critical": [
            "实验设计存在重大缺陷，缺乏对照组，无法验证因果关系。",
            "样本量不足以支持统计结论，需要进行功效分析。",
            "研究方法的选择缺乏合理性论证，建议补充方法论依据。"
        ],
        "major": [
            "建议增加更多的消融实验以验证各组件的贡献。",
            "数据预处理步骤描述不够详细，影响可重复性。",
            "缺少与最新基线方法的比较，建议补充对比实验。"
        ],
        "minor": [
            "建议补充超参数敏感性分析。",
            "实验结果的可视化可以进一步优化。",
            "建议增加计算复杂度分析。"
        ]
    },
    "novelty": {
        "critical": [
            "论文的核心贡献与已有工作高度相似，创新性不足。",
            "技术方案缺乏新颖性，仅是已有方法的简单组合。"
        ],
        "major": [
            "建议更清晰地阐述与相关工作的区别和改进。",
            "创新点的理论分析不够深入，建议补充理论证明。"
        ],
        "minor": [
            "建议在引言中更突出研究的创新贡献。",
            "与现有方法的对比讨论可以更加深入。"
        ]
    },
    "writing": {
        "critical": [
            "论文结构混乱，逻辑不清，需要大幅重写。"
        ],
        "major": [
            "摘要未能准确概括研究贡献，需要重写。",
            "相关工作部分组织不当，建议按主题分类讨论。",
            "结论过于笼统，缺乏具体的发现总结。"
        ],
        "minor": [
            "部分图表的标注不够清晰，建议优化。",
            "参考文献格式不统一，请检查。",
            "建议精简冗余表述，提升可读性。"
        ]
    },
    "significance": {
        "major": [
            "研究的实际应用价值需要进一步论证。",
            "对领域的潜在影响讨论不足。"
        ],
        "minor": [
            "建议讨论研究的局限性和未来工作方向。",
            "可以增加更多实际应用场景的讨论。"
        ]
    },
    "data_analysis": {
        "critical": [
            "统计检验方法选择不当，结论可能不可靠。"
        ],
        "major": [
            "缺少误差分析和置信区间报告。",
            "数据集的代表性需要进一步验证。"
        ],
        "minor": [
            "建议报告更多的评估指标。",
            "结果表格可以增加标准差信息。"
        ]
    }
}

# --- 作者回复模板 ---
AUTHOR_RESPONSE_TEMPLATES = {
    "critical": [
        "感谢审稿人指出这一关键问题。我们已{action}，具体修改如下：\n{detail}",
        "非常感谢这一重要意见。经过深入分析，我们{action}。修改后的结果显示{result}。"
    ],
    "major": [
        "感谢审稿人的宝贵建议。我们已按要求{action}，详见修改稿第{section}节。",
        "感谢这一建设性意见。我们{action}，新增内容已在修改稿中标注。"
    ],
    "minor": [
        "感谢审稿人的细致审阅。已按建议{action}。",
        "已采纳此建议，{action}。"
    ]
}

REVISION_ACTIONS = {
    "methodology": [
        "补充了详细的实验设计说明和对照组设置",
        "增加了消融实验和敏感性分析",
        "补充了方法论的理论依据和引用",
        "增加了与最新方法的对比实验"
    ],
    "novelty": [
        "重新撰写了创新性论述，明确区分与现有工作的差异",
        "补充了理论分析以支撑创新点",
        "增加了创新性对比表格"
    ],
    "writing": [
        "重新组织了论文结构，改善了逻辑流",
        "重写了摘要和结论部分",
        "优化了图表质量和标注",
        "统一了参考文献格式"
    ],
    "significance": [
        "增加了应用场景讨论和案例分析",
        "扩展了对领域影响的讨论"
    ],
    "data_analysis": [
        "补充了统计检验和置信区间",
        "增加了多项评估指标和误差分析",
        "验证了数据集的代表性"
    ]
}


class EICAgent:
    """
    主编代理 (Editor-in-Chief Agent)

    职责:
    1. 接收稿件提交
    2. 选择和分配审稿人
    3. 综合审稿意见，形成指导性反馈
    4. 协调修改-再审循环
    5. 做出最终决定
    """

    def __init__(self, store: DistributedStore):
        self.id = "eic_001"
        self.name = "Editor-in-Chief"
        self.role = AgentRole.EIC
        self.store = store
        self.store.update_agent_state(self.id, {
            'role': 'eic', 'name': self.name, 'status': 'active'
        })

    def receive_submission(self, manuscript: ManuscriptState, version: ManuscriptVersion) -> ManuscriptState:
        """接收并登记稿件"""
        manuscript.status = "submitted"
        self.store.store_manuscript(manuscript.manuscript_id, asdict(version))

        msg = AgentMessage(
            sender=self.id, sender_role="eic",
            receiver="system", receiver_role="system",
            msg_type=MessageType.SUBMIT.value,
            content=f"稿件 [{version.title}] 已接收登记，编号: {manuscript.manuscript_id}",
            round_number=1
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))
        return manuscript

    def assign_reviewers(self, manuscript: ManuscriptState, reviewer_ids: list) -> ManuscriptState:
        """分配审稿人"""
        manuscript.assigned_reviewers = reviewer_ids
        manuscript.status = "under_review"

        for rid in reviewer_ids:
            profile = next((r for r in REVIEWER_PROFILES if r['id'] == rid), None)
            reviewer_name = profile['name'] if profile else rid

            msg = AgentMessage(
                sender=self.id, sender_role="eic",
                receiver=rid, receiver_role="reviewer",
                msg_type=MessageType.ASSIGN.value,
                content=f"请您审阅稿件 {manuscript.manuscript_id}，请重点关注研究的创新性、方法论严谨性及写作质量。",
                metadata={'manuscript_id': manuscript.manuscript_id, 'reviewer_name': reviewer_name},
                round_number=manuscript.current_round
            )
            self.store.send_message(msg)
            manuscript.message_log.append(asdict(msg))

        return manuscript

    def synthesize_feedback(self, manuscript: ManuscriptState) -> dict:
        """
        综合所有审稿意见，生成指导性反馈摘要

        EIC的核心协调功能：
        - 识别审稿人共识意见
        - 标注分歧点
        - 形成优先级排序的修改指导
        """
        reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round)
        if not reviews:
            return {"error": "No reviews found"}

        # 收集所有评论
        all_comments = []
        score_summary = {}
        decisions = []

        for review in reviews:
            decisions.append(review.get('decision', 'pending'))
            for dim, score in review.get('scores', {}).items():
                if dim not in score_summary:
                    score_summary[dim] = []
                score_summary[dim].append(score)
            for comment in review.get('comments', []):
                all_comments.append(comment)

        # 分类统计
        critical_issues = [c for c in all_comments if c.get('severity') == 'critical']
        major_issues = [c for c in all_comments if c.get('severity') == 'major']
        minor_issues = [c for c in all_comments if c.get('severity') == 'minor']

        # 计算维度平均分
        avg_scores = {dim: sum(s) / len(s) for dim, s in score_summary.items() if s}

        # EIC决策逻辑
        overall_avg = sum(avg_scores.values()) / len(avg_scores) if avg_scores else 0
        has_critical = len(critical_issues) > 0

        if overall_avg >= 8.0 and not has_critical:
            eic_recommendation = ReviewDecision.ACCEPT.value
        elif overall_avg >= 6.0 and not has_critical:
            eic_recommendation = ReviewDecision.MINOR_REVISION.value
        elif overall_avg >= 4.0 or has_critical:
            eic_recommendation = ReviewDecision.MAJOR_REVISION.value
        else:
            eic_recommendation = ReviewDecision.REJECT.value

        synthesis = {
            "round": manuscript.current_round,
            "reviewer_count": len(reviews),
            "avg_scores": avg_scores,
            "overall_avg": round(overall_avg, 2),
            "critical_count": len(critical_issues),
            "major_count": len(major_issues),
            "minor_count": len(minor_issues),
            "critical_issues": critical_issues,
            "major_issues": major_issues,
            "minor_issues": minor_issues,
            "reviewer_decisions": decisions,
            "eic_recommendation": eic_recommendation,
            "guidance": self._generate_guidance(eic_recommendation, critical_issues, major_issues, avg_scores)
        }

        # 发送综合反馈
        msg = AgentMessage(
            sender=self.id, sender_role="eic",
            receiver="author", receiver_role="author",
            msg_type=MessageType.FEEDBACK_SUMMARY.value,
            content=synthesis['guidance'],
            metadata=synthesis,
            round_number=manuscript.current_round
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))
        manuscript.eic_decisions.append(synthesis)

        return synthesis

    def _generate_guidance(self, recommendation: str, critical: list, major: list, scores: dict) -> str:
        """生成EIC指导意见"""
        lines = []
        lines.append(f"【EIC综合评审意见 - 第{st.session_state.get('ms_state', {}).get('current_round', 1) if isinstance(st.session_state.get('ms_state'), dict) else 1}轮】\n")

        if recommendation == ReviewDecision.ACCEPT.value:
            lines.append("综合评定：接受 (Accept)")
            lines.append("恭喜！您的稿件经审稿人评审后达到发表标准。\n")
        elif recommendation == ReviewDecision.MINOR_REVISION.value:
            lines.append("综合评定：小修 (Minor Revision)")
            lines.append("您的稿件质量较好，但仍需进行部分修改。请重点关注以下问题：\n")
        elif recommendation == ReviewDecision.MAJOR_REVISION.value:
            lines.append("综合评定：大修 (Major Revision)")
            lines.append("您的稿件需要实质性修改。请务必逐条回复审稿人意见：\n")
        else:
            lines.append("综合评定：拒稿 (Reject)")
            lines.append("很遗憾，您的稿件目前不符合发表要求。主要问题如下：\n")

        if critical:
            lines.append("⚠ 关键问题 (必须解决):")
            for i, c in enumerate(critical, 1):
                lines.append(f"  {i}. [{c.get('category', '')}] {c.get('comment', '')}")
            lines.append("")

        if major:
            lines.append("● 重要问题 (需要认真处理):")
            for i, c in enumerate(major, 1):
                lines.append(f"  {i}. [{c.get('category', '')}] {c.get('comment', '')}")
            lines.append("")

        weak_dims = [d for d, s in scores.items() if s < 6.0]
        if weak_dims:
            lines.append("△ 薄弱环节 (建议加强):")
            for d in weak_dims:
                dim_info = REVIEW_DIMENSIONS.get(d, {})
                lines.append(f"  - {dim_info.get('name', d)}: 当前均分 {scores[d]:.1f}/10")

        return "\n".join(lines)

    def request_re_review(self, manuscript: ManuscriptState) -> ManuscriptState:
        """请求审稿人重新审阅修改稿"""
        for rid in manuscript.assigned_reviewers:
            msg = AgentMessage(
                sender=self.id, sender_role="eic",
                receiver=rid, receiver_role="reviewer",
                msg_type=MessageType.RE_REVIEW.value,
                content=f"作者已提交修改稿（第{manuscript.current_version}版），请您重新审阅并评估修改是否充分。",
                metadata={'manuscript_id': manuscript.manuscript_id, 'version': manuscript.current_version},
                round_number=manuscript.current_round
            )
            self.store.send_message(msg)
            manuscript.message_log.append(asdict(msg))

        manuscript.status = "under_review"
        return manuscript

    def make_final_decision(self, manuscript: ManuscriptState) -> dict:
        """做出最终决定"""
        reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round)
        if not reviews:
            return {"decision": "pending", "reason": "无审稿意见"}

        avg_score = sum(r.get('overall_score', 0) for r in reviews) / len(reviews)
        has_critical = any(
            c.get('severity') == 'critical' and not c.get('addressed', False)
            for r in reviews for c in r.get('comments', [])
        )

        if avg_score >= 7.5 and not has_critical:
            decision = ReviewDecision.ACCEPT.value
            reason = f"稿件经过{manuscript.current_round}轮审稿后达到发表标准，平均分 {avg_score:.1f}/10。"
        elif avg_score >= 6.0:
            decision = ReviewDecision.MINOR_REVISION.value
            reason = f"稿件仍需小幅修改，平均分 {avg_score:.1f}/10。"
        elif manuscript.current_round >= manuscript.max_rounds:
            decision = ReviewDecision.REJECT.value
            reason = f"经过{manuscript.current_round}轮审稿，稿件未能达到发表标准。"
        else:
            decision = ReviewDecision.MAJOR_REVISION.value
            reason = f"稿件需继续修改，当前平均分 {avg_score:.1f}/10。"

        result = {
            "decision": decision,
            "reason": reason,
            "round": manuscript.current_round,
            "avg_score": round(avg_score, 2)
        }

        msg = AgentMessage(
            sender=self.id, sender_role="eic",
            receiver="author", receiver_role="author",
            msg_type=MessageType.FINAL_DECISION.value,
            content=reason,
            metadata=result,
            round_number=manuscript.current_round
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))

        return result


class ReviewerAgent:
    """
    审稿人代理 (Reviewer Agent)

    职责:
    1. 按维度评估稿件
    2. 给出评分和意见
    3. 重新审阅修改稿并更新评价
    """

    def __init__(self, profile: dict, store: DistributedStore):
        self.id = profile['id']
        self.name = profile['name']
        self.expertise = profile.get('expertise', [])
        self.strictness = profile.get('strictness', 0.5)
        self.personality = profile.get('personality', '')
        self.focus_areas = profile.get('focus_areas', [])
        self.role = AgentRole.REVIEWER
        self.store = store
        self.store.update_agent_state(self.id, {
            'role': 'reviewer', 'name': self.name,
            'status': 'active', 'expertise': self.expertise
        })

    def review_manuscript(self, manuscript: ManuscriptState, is_re_review: bool = False) -> ReviewReport:
        """
        审阅稿件

        审稿逻辑：
        - 对专长领域更严格/更有见地
        - 考虑审稿人性格特征
        - 再审时考虑作者回复质量
        """
        version = self.store.get_latest_version(manuscript.manuscript_id)

        # 生成维度评分
        scores = {}
        base_quality = random.uniform(4.5, 8.5)

        # 再审时，基于前一轮提升
        if is_re_review and manuscript.current_round > 1:
            prev_reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round - 1)
            my_prev = next((r for r in prev_reviews if r.get('reviewer_id') == self.id), None)
            if my_prev:
                prev_avg = my_prev.get('overall_score', base_quality)
                # 作者修改后通常会有提升
                improvement = random.uniform(0.5, 2.0)
                base_quality = min(prev_avg + improvement, 9.5)

        for dim, info in REVIEW_DIMENSIONS.items():
            # 专长领域评分更精准
            if dim in self.expertise:
                score = base_quality + random.uniform(-1.0, 0.5) - (self.strictness * 0.5)
            else:
                score = base_quality + random.uniform(-1.5, 1.0)
            scores[dim] = round(max(1.0, min(10.0, score)), 1)

        overall_score = sum(scores[d] * REVIEW_DIMENSIONS[d]['weight'] for d in scores)

        # 生成审稿意见
        comments = self._generate_comments(scores, is_re_review, manuscript)

        # 确定审稿决定
        if overall_score >= 8.0:
            decision = ReviewDecision.ACCEPT.value
        elif overall_score >= 6.5:
            decision = ReviewDecision.MINOR_REVISION.value
        elif overall_score >= 4.5:
            decision = ReviewDecision.MAJOR_REVISION.value
        else:
            decision = ReviewDecision.REJECT.value

        report = ReviewReport(
            reviewer_id=self.id,
            reviewer_name=self.name,
            round_number=manuscript.current_round,
            decision=decision,
            overall_score=round(overall_score, 2),
            scores=scores,
            comments=[asdict(c) if isinstance(c, ReviewComment) else c for c in comments],
            summary=self._generate_summary(scores, decision),
            confidence=round(random.uniform(0.7, 0.95), 2)
        )

        report_dict = asdict(report)
        self.store.store_review(manuscript.manuscript_id, report_dict)
        manuscript.review_reports.append(report_dict)

        # 发送审稿消息
        msg = AgentMessage(
            sender=self.id, sender_role="reviewer",
            receiver="eic_001", receiver_role="eic",
            msg_type=MessageType.REVIEW.value,
            content=f"审稿完成: {self.name} - 总评分 {overall_score:.1f}/10 - 建议: {decision}",
            metadata={'report': report_dict},
            round_number=manuscript.current_round
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))

        return report

    def _generate_comments(self, scores: dict, is_re_review: bool, manuscript: ManuscriptState) -> list:
        """生成审稿意见"""
        comments = []
        for dim, score in scores.items():
            templates = REVIEW_TEMPLATES.get(dim, {})

            if score < 4.5 and templates.get('critical'):
                severity = 'critical'
                pool = templates['critical']
            elif score < 6.5 and templates.get('major'):
                severity = 'major'
                pool = templates['major']
            elif score < 8.0 and templates.get('minor'):
                severity = 'minor'
                pool = templates['minor']
            else:
                continue

            # 专长领域给出更多意见
            n_comments = 2 if dim in self.expertise else 1
            selected = random.sample(pool, min(n_comments, len(pool)))

            for text in selected:
                # 再审时标注是否已解决
                addressed = is_re_review and random.random() > self.strictness
                comment = ReviewComment(
                    reviewer_id=self.id,
                    category=dim,
                    severity=severity,
                    comment=text,
                    addressed=addressed
                )
                comments.append(comment)

        return comments

    def _generate_summary(self, scores: dict, decision: str) -> str:
        """生成审稿总结"""
        strong = [REVIEW_DIMENSIONS[d]['name'] for d, s in scores.items() if s >= 7.0]
        weak = [REVIEW_DIMENSIONS[d]['name'] for d, s in scores.items() if s < 6.0]

        lines = [f"【{self.name} 审稿总结】"]
        if strong:
            lines.append(f"优势方面: {', '.join(strong)}")
        if weak:
            lines.append(f"待改进方面: {', '.join(weak)}")

        decision_text = {
            'accept': '建议接受',
            'minor_revision': '建议小修后接受',
            'major_revision': '建议大修后重审',
            'reject': '建议拒稿'
        }
        lines.append(f"审稿建议: {decision_text.get(decision, decision)}")
        return "\n".join(lines)


class AuthorAgent:
    """
    作者代理 (Author Agent)

    职责:
    1. 接收审稿意见
    2. 逐条回复审稿意见
    3. 修改稿件
    4. 生成修改说明
    """

    def __init__(self, store: DistributedStore):
        self.id = "author_001"
        self.name = "Author"
        self.role = AgentRole.AUTHOR
        self.store = store
        self.store.update_agent_state(self.id, {
            'role': 'author', 'name': self.name, 'status': 'active'
        })

    def process_feedback(self, manuscript: ManuscriptState, synthesis: dict) -> dict:
        """
        处理EIC综合反馈，生成逐条回复

        回复策略:
        - 关键问题: 详细说明修改方案
        - 重要问题: 说明修改内容或合理解释
        - 小问题: 简短确认
        """
        responses = []

        all_issues = (
            [(c, 'critical') for c in synthesis.get('critical_issues', [])] +
            [(c, 'major') for c in synthesis.get('major_issues', [])] +
            [(c, 'minor') for c in synthesis.get('minor_issues', [])]
        )

        for comment, severity in all_issues:
            category = comment.get('category', 'general')
            actions = REVISION_ACTIONS.get(category, ["进行了相应修改"])
            action = random.choice(actions)
            templates = AUTHOR_RESPONSE_TEMPLATES.get(severity, AUTHOR_RESPONSE_TEMPLATES['minor'])
            template = random.choice(templates)

            response = template.format(
                action=action,
                detail=f"已在修改稿中进行标注（见{category}相关章节）",
                result="改进效果显著",
                section=random.choice(["2", "3", "4", "5"])
            )

            responses.append({
                'original_comment': comment.get('comment', ''),
                'category': category,
                'severity': severity,
                'response': response,
                'addressed': True
            })

        return {
            'round': manuscript.current_round,
            'total_issues': len(all_issues),
            'responses': responses
        }

    def revise_manuscript(self, manuscript: ManuscriptState, feedback_response: dict) -> ManuscriptVersion:
        """
        修改稿件，生成新版本
        """
        prev_version = self.store.get_latest_version(manuscript.manuscript_id)
        new_version_num = manuscript.current_version + 1

        # 生成修改说明
        revision_notes = self._generate_revision_notes(feedback_response)

        # 模拟内容修改
        new_sections = {}
        if prev_version and prev_version.get('content_sections'):
            for sec, content in prev_version['content_sections'].items():
                new_sections[sec] = content + f"\n[第{new_version_num}版修改]"
        else:
            new_sections = {
                "introduction": f"引言部分 [第{new_version_num}版]",
                "methodology": f"方法论部分 [第{new_version_num}版]",
                "results": f"结果部分 [第{new_version_num}版]",
                "discussion": f"讨论部分 [第{new_version_num}版]",
                "conclusion": f"结论部分 [第{new_version_num}版]"
            }

        new_version = ManuscriptVersion(
            version=new_version_num,
            title=prev_version.get('title', '未命名稿件') if prev_version else '未命名稿件',
            abstract=prev_version.get('abstract', '') if prev_version else '',
            content_sections=new_sections,
            revision_notes=revision_notes,
            content_hash=hashlib.md5(json.dumps(new_sections).encode()).hexdigest()[:12]
        )

        manuscript.current_version = new_version_num
        self.store.store_manuscript(manuscript.manuscript_id, asdict(new_version))
        manuscript.versions.append(asdict(new_version))

        # 发送修改消息
        msg = AgentMessage(
            sender=self.id, sender_role="author",
            receiver="eic_001", receiver_role="eic",
            msg_type=MessageType.REVISION.value,
            content=f"已提交第{new_version_num}版修改稿，共处理{feedback_response.get('total_issues', 0)}条审稿意见。",
            metadata={'version': new_version_num, 'response': feedback_response},
            round_number=manuscript.current_round
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))

        return new_version

    def _generate_revision_notes(self, feedback_response: dict) -> str:
        """生成修改说明文档"""
        lines = [f"=== 修改说明 (Revision Notes) ===\n"]
        lines.append(f"本次修改共回复 {feedback_response.get('total_issues', 0)} 条审稿意见。\n")

        for i, resp in enumerate(feedback_response.get('responses', []), 1):
            lines.append(f"--- 问题 {i} [{resp['severity'].upper()}] [{resp['category']}] ---")
            lines.append(f"审稿意见: {resp['original_comment']}")
            lines.append(f"作者回复: {resp['response']}")
            lines.append("")

        return "\n".join(lines)


# ============================================================
# 4. 审稿协调器 (Review Coordinator)
# ============================================================

class ReviewCoordinator:
    """
    审稿流程协调器 - 管理完整的多轮审稿循环

    流程:
    Author提交 → EIC分配 → Reviewer审稿 → EIC综合 → Author修改
    → EIC再分配 → Reviewer再审 → ... → EIC最终决定
    """

    def __init__(self):
        self.store = DistributedStore()
        self.eic = EICAgent(self.store)
        self.reviewers = [ReviewerAgent(p, self.store) for p in REVIEWER_PROFILES]
        self.author = AuthorAgent(self.store)

    def init_manuscript(self, title: str, abstract: str) -> ManuscriptState:
        """初始化稿件"""
        ms = ManuscriptState()
        version = ManuscriptVersion(
            version=1,
            title=title,
            abstract=abstract,
            content_sections={
                "introduction": "引言内容...",
                "methodology": "方法论内容...",
                "results": "结果内容...",
                "discussion": "讨论内容...",
                "conclusion": "结论内容..."
            },
            content_hash=hashlib.md5(title.encode()).hexdigest()[:12]
        )
        ms.versions.append(asdict(version))
        ms = self.eic.receive_submission(ms, version)
        return ms

    def run_review_round(self, manuscript: ManuscriptState) -> dict:
        """执行一轮完整审稿"""

        # Step 1: EIC分配审稿人
        reviewer_ids = [r.id for r in self.reviewers]
        manuscript = self.eic.assign_reviewers(manuscript, reviewer_ids)

        # Step 2: 各审稿人审稿
        is_re_review = manuscript.current_round > 1
        reports = []
        for reviewer in self.reviewers:
            report = reviewer.review_manuscript(manuscript, is_re_review=is_re_review)
            reports.append(asdict(report))

        # Step 3: EIC综合反馈
        synthesis = self.eic.synthesize_feedback(manuscript)

        return {
            'round': manuscript.current_round,
            'reports': reports,
            'synthesis': synthesis,
            'recommendation': synthesis.get('eic_recommendation', 'pending')
        }

    def author_revise(self, manuscript: ManuscriptState, synthesis: dict) -> dict:
        """作者修改流程"""
        # Author处理反馈
        response = self.author.process_feedback(manuscript, synthesis)
        # Author修改稿件
        new_version = self.author.revise_manuscript(manuscript, response)

        return {
            'response': response,
            'new_version': asdict(new_version),
            'version_number': new_version.version
        }

    def advance_round(self, manuscript: ManuscriptState):
        """推进到下一轮"""
        manuscript.current_round += 1
        manuscript.status = "under_review"

    def is_process_complete(self, synthesis: dict) -> bool:
        """判断审稿流程是否结束"""
        rec = synthesis.get('eic_recommendation', '')
        return rec in [ReviewDecision.ACCEPT.value, ReviewDecision.REJECT.value]


# ============================================================
# 5. Streamlit UI
# ============================================================

def setup_page():
    """页面配置"""
    st.set_page_config(
        page_title="分布式审稿协调系统",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3a5f;
        padding-bottom: 1rem;
        border-bottom: 3px solid #00d4ff;
        margin-bottom: 1.5rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0d6efd;
    }
    .agent-card-eic { border-left-color: #dc3545; }
    .agent-card-reviewer { border-left-color: #198754; }
    .agent-card-author { border-left-color: #0d6efd; }

    .score-high { color: #198754; font-weight: bold; }
    .score-mid { color: #fd7e14; font-weight: bold; }
    .score-low { color: #dc3545; font-weight: bold; }

    .message-bubble {
        background: #f0f7ff;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    .message-bubble-eic { background: #fff0f0; }
    .message-bubble-reviewer { background: #f0fff0; }
    .message-bubble-author { background: #f0f0ff; }

    .round-badge {
        display: inline-block;
        background: #0d6efd;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .decision-accept { background: #198754; color: white; padding: 0.3rem 1rem; border-radius: 8px; }
    .decision-revision { background: #fd7e14; color: white; padding: 0.3rem 1rem; border-radius: 8px; }
    .decision-reject { background: #dc3545; color: white; padding: 0.3rem 1rem; border-radius: 8px; }

    .metric-box {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e3a5f;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
    }
    .event-log {
        background: #1e1e1e;
        color: #00ff00;
        font-family: monospace;
        font-size: 0.8rem;
        padding: 1rem;
        border-radius: 8px;
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'coordinator' not in st.session_state:
        st.session_state.coordinator = None
    if 'ms_state' not in st.session_state:
        st.session_state.ms_state = None
    if 'review_history' not in st.session_state:
        st.session_state.review_history = []
    if 'revision_history' not in st.session_state:
        st.session_state.revision_history = []
    if 'process_complete' not in st.session_state:
        st.session_state.process_complete = False
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = "init"  # init, reviewing, feedback, revising, complete
    if 'auto_running' not in st.session_state:
        st.session_state.auto_running = False


def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("### ⚙ 系统配置")

        st.markdown("**稿件信息**")
        title = st.text_input("论文标题", value="基于多代理协调的分布式审稿系统研究")
        abstract = st.text_area("摘要", value="本文提出了一种基于多代理协调的分布式审稿系统，"
                                             "通过EIC、Reviewer和Author三类代理的协同工作，"
                                             "实现了审稿流程的自动化管理...",
                                height=100)

        st.divider()
        st.markdown("**审稿参数**")
        max_rounds = st.slider("最大审稿轮数", 1, 10, 5)

        st.divider()
        st.markdown("**审稿人配置**")
        for p in REVIEWER_PROFILES:
            with st.expander(p['name']):
                st.write(f"性格: {p['personality']}")
                st.write(f"专长: {', '.join(p['expertise'])}")
                st.write(f"严格度: {p['strictness']}")

        st.divider()
        if st.button("🔄 重置系统", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith('store_') or key in [
                    'coordinator', 'ms_state', 'review_history',
                    'revision_history', 'process_complete', 'current_phase', 'auto_running'
                ]:
                    del st.session_state[key]
            st.rerun()

        return title, abstract, max_rounds


def render_agent_status():
    """渲染代理状态面板"""
    st.markdown("### 🤖 代理状态")
    cols = st.columns(3)

    with cols[0]:
        st.markdown('<div class="agent-card agent-card-eic">', unsafe_allow_html=True)
        st.markdown("**🔴 EIC (主编)**")
        st.caption("统筹协调审稿流程")
        phase = st.session_state.get('current_phase', 'init')
        status_map = {
            'init': '等待稿件', 'reviewing': '协调审稿中',
            'feedback': '综合反馈', 'revising': '等待修改稿',
            'complete': '流程完成'
        }
        st.write(f"状态: {status_map.get(phase, phase)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[1]:
        st.markdown('<div class="agent-card agent-card-reviewer">', unsafe_allow_html=True)
        st.markdown("**🟢 Reviewers (审稿人)**")
        st.caption(f"共 {len(REVIEWER_PROFILES)} 位审稿人")
        if phase == 'reviewing':
            st.write("状态: 审稿中...")
        elif phase == 'feedback':
            st.write("状态: 审稿完成")
        else:
            st.write("状态: 待命")
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[2]:
        st.markdown('<div class="agent-card agent-card-author">', unsafe_allow_html=True)
        st.markdown("**🔵 Author (作者)**")
        st.caption("接收反馈并修改")
        if phase == 'revising':
            st.write("状态: 修改中...")
        elif phase == 'feedback':
            st.write("状态: 查看反馈")
        else:
            st.write("状态: 待命")
        st.markdown('</div>', unsafe_allow_html=True)


def render_review_report(report: dict, round_num: int):
    """渲染单个审稿报告"""
    reviewer_name = report.get('reviewer_name', 'Unknown')
    decision = report.get('decision', 'pending')
    score = report.get('overall_score', 0)

    decision_labels = {
        'accept': ('接受', 'decision-accept'),
        'minor_revision': ('小修', 'decision-revision'),
        'major_revision': ('大修', 'decision-revision'),
        'reject': ('拒稿', 'decision-reject'),
        'pending': ('待定', 'decision-revision')
    }
    label, css_class = decision_labels.get(decision, ('未知', 'decision-revision'))

    with st.expander(f"📋 {reviewer_name} | 评分: {score:.1f}/10 | {label}", expanded=False):
        # 评分详情
        scores = report.get('scores', {})
        if scores:
            score_df = pd.DataFrame([
                {
                    '维度': REVIEW_DIMENSIONS.get(d, {}).get('name', d),
                    '评分': s,
                    '权重': REVIEW_DIMENSIONS.get(d, {}).get('weight', 0)
                }
                for d, s in scores.items()
            ])
            st.dataframe(score_df, use_container_width=True, hide_index=True)

        # 审稿意见
        comments = report.get('comments', [])
        if comments:
            st.markdown("**审稿意见:**")
            for c in comments:
                severity = c.get('severity', 'minor')
                icon = {'critical': '🔴', 'major': '🟠', 'minor': '🟡'}.get(severity, '⚪')
                category = REVIEW_DIMENSIONS.get(c.get('category', ''), {}).get('name', c.get('category', ''))
                addressed = " ✅" if c.get('addressed') else ""
                st.markdown(f"{icon} **[{category}]** {c.get('comment', '')}{addressed}")

        st.markdown(f"**总结:** {report.get('summary', '')}")
        st.caption(f"审稿信心: {report.get('confidence', 0):.0%}")


def render_revision_response(revision: dict):
    """渲染作者修改回复"""
    response = revision.get('response', {})
    responses = response.get('responses', [])

    if not responses:
        return

    st.markdown(f"**共回复 {len(responses)} 条意见:**")

    for i, resp in enumerate(responses, 1):
        severity = resp.get('severity', 'minor')
        icon = {'critical': '🔴', 'major': '🟠', 'minor': '🟡'}.get(severity, '⚪')
        category = REVIEW_DIMENSIONS.get(resp.get('category', ''), {}).get('name', resp.get('category', ''))

        with st.expander(f"{icon} 问题 {i}: [{category}] {resp.get('original_comment', '')[:50]}..."):
            st.markdown(f"**审稿意见:** {resp.get('original_comment', '')}")
            st.markdown(f"**作者回复:** {resp.get('response', '')}")


def render_metrics(ms_state):
    """渲染关键指标"""
    if not ms_state:
        return

    cols = st.columns(4)

    with cols[0]:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{ms_state.current_round}</div>
            <div class="metric-label">当前轮次</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{ms_state.current_version}</div>
            <div class="metric-label">稿件版本</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        reviews = st.session_state.get('review_history', [])
        latest_avg = 0
        if reviews:
            latest = reviews[-1]
            scores = [r.get('overall_score', 0) for r in latest.get('reports', [])]
            latest_avg = sum(scores) / len(scores) if scores else 0
        color_class = "score-high" if latest_avg >= 7 else ("score-mid" if latest_avg >= 5 else "score-low")
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value {color_class}">{latest_avg:.1f}</div>
            <div class="metric-label">平均评分</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        total_comments = sum(
            len(r.get('comments', []))
            for rh in reviews
            for r in rh.get('reports', [])
        )
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{total_comments}</div>
            <div class="metric-label">累计意见数</div>
        </div>
        """, unsafe_allow_html=True)


def render_score_trend():
    """渲染评分趋势图"""
    reviews = st.session_state.get('review_history', [])
    if len(reviews) < 1:
        return

    trend_data = []
    for rh in reviews:
        round_num = rh.get('round', 1)
        for report in rh.get('reports', []):
            for dim, score in report.get('scores', {}).items():
                trend_data.append({
                    'Round': f"第{round_num}轮",
                    'Dimension': REVIEW_DIMENSIONS.get(dim, {}).get('name', dim),
                    'Score': score,
                    'Reviewer': report.get('reviewer_name', '?')
                })

    if trend_data:
        df = pd.DataFrame(trend_data)
        import altair as alt

        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Round:N', title='审稿轮次'),
            y=alt.Y('Score:Q', title='评分', scale=alt.Scale(domain=[0, 10])),
            color='Dimension:N',
            strokeDash='Reviewer:N',
            tooltip=['Round', 'Dimension', 'Score', 'Reviewer']
        ).properties(
            title='各维度评分趋势',
            height=300
        ).interactive()

        st.altair_chart(chart, use_container_width=True)


def render_message_flow():
    """渲染消息流"""
    store = st.session_state.get('store_messages', [])
    if not store:
        st.info("暂无消息记录")
        return

    for msg in store[-20:]:  # 最近20条
        role = msg.get('sender_role', '')
        css_class = {
            'eic': 'message-bubble-eic',
            'reviewer': 'message-bubble-reviewer',
            'author': 'message-bubble-author'
        }.get(role, '')
        role_icon = {'eic': '🔴', 'reviewer': '🟢', 'author': '🔵'}.get(role, '⚪')
        msg_type_label = {
            'submit': '提交', 'assign': '分配', 'review': '审稿',
            'feedback_summary': '综合反馈', 'revision': '修改',
            'decision': '决定', 're_review': '重审', 'final_decision': '最终决定'
        }.get(msg.get('msg_type', ''), msg.get('msg_type', ''))

        st.markdown(f"""
        <div class="message-bubble {css_class}">
            {role_icon} <strong>[{msg_type_label}]</strong>
            {msg.get('sender', '')} → {msg.get('receiver', '')}
            <br><small>{msg.get('content', '')[:200]}</small>
            <br><small style="color:#999">{msg.get('timestamp', '')}</small>
        </div>
        """, unsafe_allow_html=True)


def render_event_log():
    """渲染事件日志"""
    coord = st.session_state.get('store_coordination', {})
    events = coord.get('event_log', [])

    if events:
        log_text = "\n".join([f"[{e['time']}] {e['event']}" for e in events[-30:]])
        st.markdown(f'<div class="event-log">{log_text}</div>', unsafe_allow_html=True)
    else:
        st.info("暂无事件日志")


def render_workflow_diagram(current_phase: str):
    """渲染工作流状态图"""
    phases = [
        ("提交", "init"),
        ("分配审稿", "reviewing"),
        ("审稿评估", "reviewing"),
        ("EIC综合", "feedback"),
        ("作者修改", "revising"),
        ("最终决定", "complete")
    ]

    cols = st.columns(len(phases))
    for i, (label, phase) in enumerate(phases):
        with cols[i]:
            if phase == current_phase:
                st.markdown(f"**▶ {label}**")
            elif phases.index((label, phase)) < [p[1] for p in phases].index(current_phase) if current_phase in [p[1] for p in phases] else 0:
                st.markdown(f"~~{label}~~ ✅")
            else:
                st.markdown(f"○ {label}")


def main():
    setup_page()
    init_session_state()

    st.markdown('<div class="main-header">📝 分布式存储协调代理审稿修改模型</div>', unsafe_allow_html=True)
    st.caption("Distributed Storage Coordination Agent - Manuscript Review System | EIC ↔ Reviewer ↔ Author")

    # 侧边栏
    title, abstract, max_rounds = render_sidebar()

    # 工作流状态
    current_phase = st.session_state.get('current_phase', 'init')
    render_workflow_diagram(current_phase)
    st.divider()

    # 代理状态
    render_agent_status()
    st.divider()

    ms_state = st.session_state.get('ms_state', None)

    # ---- 稿件提交阶段 ----
    if current_phase == "init":
        st.markdown("### 📤 步骤 1: 提交稿件")
        st.info(f"**标题:** {title}\n\n**摘要:** {abstract[:100]}...")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📨 提交稿件并开始审稿流程", type="primary", use_container_width=True):
                coordinator = ReviewCoordinator()
                ms = coordinator.init_manuscript(title, abstract)
                ms.max_rounds = max_rounds

                st.session_state.coordinator = coordinator
                st.session_state.ms_state = ms
                st.session_state.current_phase = "reviewing"
                st.rerun()
        with col2:
            if st.button("🚀 自动运行完整流程", use_container_width=True):
                coordinator = ReviewCoordinator()
                ms = coordinator.init_manuscript(title, abstract)
                ms.max_rounds = max_rounds

                st.session_state.coordinator = coordinator
                st.session_state.ms_state = ms
                st.session_state.auto_running = True
                st.session_state.current_phase = "reviewing"
                st.rerun()

    # ---- 审稿阶段 ----
    elif current_phase == "reviewing":
        ms_state = st.session_state.ms_state
        coordinator = st.session_state.coordinator
        render_metrics(ms_state)

        st.markdown(f"### 🔍 第 {ms_state.current_round} 轮审稿")

        auto = st.session_state.get('auto_running', False)
        if auto or st.button(f"▶ 执行第 {ms_state.current_round} 轮审稿", type="primary"):
            with st.spinner("审稿人正在审阅稿件..."):
                result = coordinator.run_review_round(ms_state)
                st.session_state.review_history.append(result)
                st.session_state.current_phase = "feedback"
                st.rerun()

    # ---- 反馈阶段 ----
    elif current_phase == "feedback":
        ms_state = st.session_state.ms_state
        coordinator = st.session_state.coordinator
        render_metrics(ms_state)

        reviews = st.session_state.review_history
        if reviews:
            latest = reviews[-1]
            synthesis = latest.get('synthesis', {})

            st.markdown(f"### 📊 第 {ms_state.current_round} 轮审稿结果")

            # 审稿报告
            tab_reports, tab_synthesis, tab_trend = st.tabs(["📋 审稿报告", "📝 EIC综合意见", "📈 评分趋势"])

            with tab_reports:
                for report in latest.get('reports', []):
                    render_review_report(report, ms_state.current_round)

            with tab_synthesis:
                rec = synthesis.get('eic_recommendation', 'pending')
                rec_labels = {
                    'accept': ('✅ 接受', 'decision-accept'),
                    'minor_revision': ('📝 小修', 'decision-revision'),
                    'major_revision': ('📝 大修', 'decision-revision'),
                    'reject': ('❌ 拒稿', 'decision-reject')
                }
                rec_label, rec_css = rec_labels.get(rec, ('?', ''))
                st.markdown(f'<span class="{rec_css}">{rec_label}</span>', unsafe_allow_html=True)
                st.markdown(f"**综合评分:** {synthesis.get('overall_avg', 0):.1f}/10")
                st.markdown(f"**关键问题:** {synthesis.get('critical_count', 0)} | "
                            f"**重要问题:** {synthesis.get('major_count', 0)} | "
                            f"**小问题:** {synthesis.get('minor_count', 0)}")

                guidance = synthesis.get('guidance', '')
                if guidance:
                    st.text_area("EIC指导意见", guidance, height=300, disabled=True)

            with tab_trend:
                render_score_trend()

            # 判断流程是否结束
            if coordinator.is_process_complete(synthesis):
                st.session_state.current_phase = "complete"
                st.session_state.process_complete = True
                st.rerun()
            else:
                auto = st.session_state.get('auto_running', False)
                if auto or st.button("📝 作者开始修改", type="primary"):
                    st.session_state.current_phase = "revising"
                    st.rerun()

    # ---- 修改阶段 ----
    elif current_phase == "revising":
        ms_state = st.session_state.ms_state
        coordinator = st.session_state.coordinator
        render_metrics(ms_state)

        reviews = st.session_state.review_history
        latest = reviews[-1] if reviews else {}
        synthesis = latest.get('synthesis', {})

        st.markdown(f"### ✏ 作者修改 (第 {ms_state.current_round} 轮)")

        auto = st.session_state.get('auto_running', False)
        if auto or st.button("▶ 执行修改并提交", type="primary"):
            with st.spinner("作者正在修改稿件..."):
                revision = coordinator.author_revise(ms_state, synthesis)
                st.session_state.revision_history.append(revision)

                # 推进到下一轮
                coordinator.advance_round(ms_state)
                st.session_state.current_phase = "reviewing"
                st.rerun()

        # 显示待处理的问题
        if synthesis:
            st.markdown("**待回复的审稿意见:**")
            all_issues = (
                synthesis.get('critical_issues', []) +
                synthesis.get('major_issues', []) +
                synthesis.get('minor_issues', [])
            )
            for i, issue in enumerate(all_issues, 1):
                severity = issue.get('severity', 'minor')
                icon = {'critical': '🔴', 'major': '🟠', 'minor': '🟡'}.get(severity, '⚪')
                st.markdown(f"{icon} {i}. [{issue.get('category', '')}] {issue.get('comment', '')}")

    # ---- 完成阶段 ----
    elif current_phase == "complete":
        ms_state = st.session_state.ms_state
        render_metrics(ms_state)

        reviews = st.session_state.review_history
        latest = reviews[-1] if reviews else {}
        synthesis = latest.get('synthesis', {})
        rec = synthesis.get('eic_recommendation', 'pending')

        st.markdown("### 🏁 审稿流程完成")

        if rec == ReviewDecision.ACCEPT.value:
            st.success(f"🎉 恭喜！稿件经过 {ms_state.current_round} 轮审稿后被接受！")
            st.balloons()
        else:
            st.error(f"稿件在第 {ms_state.current_round} 轮后被拒稿。")

        # 完整历史
        st.markdown("### 📜 审稿历史回顾")
        for i, rh in enumerate(reviews, 1):
            with st.expander(f"第 {i} 轮审稿", expanded=(i == len(reviews))):
                for report in rh.get('reports', []):
                    render_review_report(report, i)

                syn = rh.get('synthesis', {})
                if syn:
                    st.markdown(f"**EIC建议:** {syn.get('eic_recommendation', '')} | "
                                f"**综合评分:** {syn.get('overall_avg', 0):.1f}")

        if st.session_state.revision_history:
            st.markdown("### 📝 修改历史")
            for i, rev in enumerate(st.session_state.revision_history, 1):
                with st.expander(f"第 {i} 次修改 (版本 {rev.get('version_number', '?')})"):
                    render_revision_response(rev)

        render_score_trend()

    # ---- 底部面板 ----
    st.divider()
    tab_msg, tab_log, tab_store = st.tabs(["💬 消息流", "📋 事件日志", "🗄 存储状态"])

    with tab_msg:
        render_message_flow()

    with tab_log:
        render_event_log()

    with tab_store:
        st.markdown("**分布式存储分区状态:**")
        col1, col2 = st.columns(2)
        with col1:
            ms_count = len(st.session_state.get('store_manuscripts', {}))
            review_count = len(st.session_state.get('store_reviews', {}))
            msg_count = len(st.session_state.get('store_messages', []))
            st.metric("稿件存储分区", f"{ms_count} 份")
            st.metric("审稿报告分区", f"{review_count} 组")
        with col2:
            agent_count = len(st.session_state.get('store_agent_states', {}))
            st.metric("消息队列", f"{msg_count} 条")
            st.metric("代理状态分区", f"{agent_count} 个")


if __name__ == "__main__":
    main()
