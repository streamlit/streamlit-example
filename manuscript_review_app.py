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


class CommentResolution(str, Enum):
    PENDING = "pending"
    ADDRESSED = "addressed"
    PARTIALLY_ADDRESSED = "partially_addressed"
    NOT_ADDRESSED = "not_addressed"


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
    """单条审稿意见 (with resolution tracking)"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    reviewer_id: str = ""
    category: str = ""  # methodology, writing, novelty, data, structure
    severity: str = ""  # critical, major, minor, suggestion
    comment: str = ""
    addressed: bool = False
    resolution: str = CommentResolution.PENDING.value
    response: str = ""
    author_response: str = ""
    verification_note: str = ""
    round_created: int = 1
    round_resolved: int = 0


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
    comment_resolutions: dict = field(default_factory=dict)  # {comment_id: resolution_status}


# ============================================================
# 1.5 工具类 (Utility Classes)
# ============================================================

class CommentTracker:
    """跨轮次审稿意见生命周期追踪"""

    @staticmethod
    def get_all_comments(review_history: list) -> list:
        """收集所有轮次中的唯一审稿意见"""
        all_comments = []
        seen_texts = set()
        for rh in review_history:
            for report in rh.get('reports', []):
                for c in report.get('comments', []):
                    comment_key = (c.get('reviewer_id', ''), c.get('comment', ''))
                    if comment_key not in seen_texts:
                        seen_texts.add(comment_key)
                        all_comments.append(c)
        return all_comments

    @staticmethod
    def get_resolution_summary(review_history: list) -> dict:
        """获取意见解决状态摘要"""
        comments = CommentTracker.get_all_comments(review_history)
        summary = {
            'total': len(comments),
            'addressed': 0,
            'partially_addressed': 0,
            'not_addressed': 0,
            'pending': 0
        }
        for c in comments:
            status = c.get('resolution', CommentResolution.PENDING.value)
            if status == CommentResolution.ADDRESSED.value:
                summary['addressed'] += 1
            elif status == CommentResolution.PARTIALLY_ADDRESSED.value:
                summary['partially_addressed'] += 1
            elif status == CommentResolution.NOT_ADDRESSED.value:
                summary['not_addressed'] += 1
            else:
                summary['pending'] += 1
        return summary


class VersionDiffer:
    """稿件版本对比工具"""

    @staticmethod
    def diff_versions(v1: dict, v2: dict) -> dict:
        """对比两个版本的章节差异"""
        sections_v1 = v1.get('content_sections', {})
        sections_v2 = v2.get('content_sections', {})
        all_sections = set(list(sections_v1.keys()) + list(sections_v2.keys()))
        diffs = {}

        for sec in sorted(all_sections):
            old = sections_v1.get(sec, '')
            new = sections_v2.get(sec, '')
            if sec not in sections_v1:
                diffs[sec] = {'status': 'added', 'old': '', 'new': new}
            elif sec not in sections_v2:
                diffs[sec] = {'status': 'removed', 'old': old, 'new': ''}
            elif old != new:
                diffs[sec] = {'status': 'modified', 'old': old, 'new': new}
            else:
                diffs[sec] = {'status': 'unchanged', 'old': old, 'new': new}

        return {
            'v1_version': v1.get('version', '?'),
            'v2_version': v2.get('version', '?'),
            'v1_hash': v1.get('content_hash', ''),
            'v2_hash': v2.get('content_hash', ''),
            'section_diffs': diffs,
            'modified_sections': [s for s, d in diffs.items() if d['status'] != 'unchanged'],
            'total_sections': len(all_sections)
        }

    @staticmethod
    def get_version_timeline(manuscript_id: str, store) -> list:
        """获取版本时间线"""
        versions = store.get_manuscript_versions(manuscript_id)
        timeline = []
        for i, v in enumerate(versions):
            entry = {
                'version': v.get('version', i + 1),
                'timestamp': v.get('timestamp', ''),
                'hash': v.get('content_hash', ''),
                'revision_notes': v.get('revision_notes', ''),
                'sections_modified': []
            }
            if i > 0:
                diff = VersionDiffer.diff_versions(versions[i - 1], v)
                entry['sections_modified'] = diff['modified_sections']
            timeline.append(entry)
        return timeline


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
        - 专家加权评分
        - 形成优先级排序的修改指导
        """
        reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round)
        if not reviews:
            return {"error": "No reviews found"}

        # 收集所有评论
        all_comments = []
        decisions = []

        for review in reviews:
            decisions.append(review.get('decision', 'pending'))
            for comment in review.get('comments', []):
                all_comments.append(comment)

        # 分类统计
        critical_issues = [c for c in all_comments if c.get('severity') == 'critical']
        major_issues = [c for c in all_comments if c.get('severity') == 'major']
        minor_issues = [c for c in all_comments if c.get('severity') == 'minor']

        # 共识分析 (专家加权 + 方差检测)
        consensus = self._compute_consensus(reviews)

        avg_scores = consensus['weighted_avg']
        overall_avg = sum(
            avg_scores.get(d, 0) * REVIEW_DIMENSIONS[d]['weight']
            for d in avg_scores
        ) if avg_scores else 0

        # 轨迹分析
        trajectory = self._analyze_trajectory()

        # EIC决策逻辑 (考虑共识度和分歧)
        has_critical = len(critical_issues) > 0
        has_major_disagreement = len(consensus['disagreement_dims']) > 0

        if overall_avg >= 8.0 and not has_critical:
            eic_recommendation = ReviewDecision.ACCEPT.value
        elif overall_avg >= 6.0 and not has_critical:
            if has_major_disagreement and overall_avg < 7.0:
                eic_recommendation = ReviewDecision.MAJOR_REVISION.value
            else:
                eic_recommendation = ReviewDecision.MINOR_REVISION.value
        elif overall_avg >= 4.0 or has_critical:
            eic_recommendation = ReviewDecision.MAJOR_REVISION.value
        else:
            eic_recommendation = ReviewDecision.REJECT.value

        # 趋势修正：如果质量持续下降且偏低，倾向拒稿
        if (trajectory.get('trend') == 'declining' and
                eic_recommendation == ReviewDecision.MAJOR_REVISION.value and
                overall_avg < 5.0):
            eic_recommendation = ReviewDecision.REJECT.value

        synthesis = {
            "round": manuscript.current_round,
            "reviewer_count": len(reviews),
            "avg_scores": avg_scores,
            "simple_avg_scores": consensus['simple_avg'],
            "overall_avg": round(overall_avg, 2),
            "critical_count": len(critical_issues),
            "major_count": len(major_issues),
            "minor_count": len(minor_issues),
            "critical_issues": critical_issues,
            "major_issues": major_issues,
            "minor_issues": minor_issues,
            "reviewer_decisions": decisions,
            "eic_recommendation": eic_recommendation,
            "consensus_level": consensus['consensus_level'],
            "disagreement_dims": consensus['disagreement_dims'],
            "outlier_reviewers": consensus['outlier_reviewers'],
            "score_variance": consensus['variance'],
            "trajectory": trajectory,
            "guidance": self._generate_guidance(
                eic_recommendation, critical_issues, major_issues,
                avg_scores, manuscript.current_round, consensus, trajectory
            )
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

    def _compute_consensus(self, reviews: list) -> dict:
        """
        计算专家加权共识评分

        - 专长维度权重 1.5x
        - 检测维度分歧 (最大分差 > 2.0)
        - 检测离群审稿人 (偏离均值 > 2.0)
        """
        score_data = {}  # dim -> [(score, reviewer_id, is_expert)]
        for review in reviews:
            rid = review.get('reviewer_id', '')
            profile = next((p for p in REVIEWER_PROFILES if p['id'] == rid), None)
            expertise = profile.get('expertise', []) if profile else []
            for dim, score in review.get('scores', {}).items():
                if dim not in score_data:
                    score_data[dim] = []
                score_data[dim].append({
                    'score': score, 'reviewer_id': rid,
                    'is_expert': dim in expertise
                })

        result = {
            'weighted_avg': {}, 'simple_avg': {}, 'variance': {},
            'disagreement_dims': [], 'outlier_reviewers': [],
            'consensus_level': 1.0
        }

        all_variances = []
        for dim, entries in score_data.items():
            scores = [e['score'] for e in entries]
            simple_avg = sum(scores) / len(scores)
            weights = [1.5 if e['is_expert'] else 1.0 for e in entries]
            weighted_avg = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            variance = sum((s - simple_avg) ** 2 for s in scores) / len(scores) if len(scores) > 1 else 0

            result['weighted_avg'][dim] = round(weighted_avg, 2)
            result['simple_avg'][dim] = round(simple_avg, 2)
            result['variance'][dim] = round(variance, 2)
            all_variances.append(variance)

            # 分歧检测
            if len(scores) >= 2:
                max_diff = max(scores) - min(scores)
                if max_diff > 2.0:
                    result['disagreement_dims'].append({
                        'dimension': dim,
                        'max_diff': round(max_diff, 2),
                        'scores': {e['reviewer_id']: e['score'] for e in entries}
                    })

            # 离群审稿人
            for entry in entries:
                if abs(entry['score'] - simple_avg) > 2.0:
                    result['outlier_reviewers'].append({
                        'reviewer_id': entry['reviewer_id'],
                        'dimension': dim,
                        'score': entry['score'],
                        'mean': round(simple_avg, 2),
                        'deviation': round(entry['score'] - simple_avg, 2)
                    })

        # 共识度: 1 - 归一化方差 (0=完全分歧, 1=完全共识)
        if all_variances:
            avg_var = sum(all_variances) / len(all_variances)
            result['consensus_level'] = round(max(0, 1 - avg_var / 10), 2)

        return result

    def _analyze_trajectory(self) -> dict:
        """分析评分趋势 (轮次间改善方向和速度)"""
        history = st.session_state.get('review_history', [])
        if len(history) < 2:
            return {'trend': 'insufficient_data', 'improvement_rate': 0, 'round_averages': []}

        round_avgs = []
        for rh in history:
            scores = [r.get('overall_score', 0) for r in rh.get('reports', [])]
            avg = sum(scores) / len(scores) if scores else 0
            round_avgs.append(avg)

        improvements = [round_avgs[i + 1] - round_avgs[i] for i in range(len(round_avgs) - 1)]
        avg_improvement = sum(improvements) / len(improvements) if improvements else 0

        if avg_improvement > 1.0:
            trend = 'strong_improvement'
        elif avg_improvement > 0.3:
            trend = 'moderate_improvement'
        elif avg_improvement > 0:
            trend = 'slight_improvement'
        elif avg_improvement > -0.3:
            trend = 'stagnant'
        else:
            trend = 'declining'

        current_avg = round_avgs[-1]
        projected = max(0, (7.5 - current_avg) / avg_improvement) if avg_improvement > 0 else float('inf')

        return {
            'trend': trend,
            'improvement_rate': round(avg_improvement, 2),
            'round_averages': [round(a, 2) for a in round_avgs],
            'projected_rounds_to_accept': round(projected, 1),
            'current_avg': round(current_avg, 2)
        }

    def _generate_guidance(self, recommendation: str, critical: list, major: list,
                           scores: dict, current_round: int = 1,
                           consensus: dict = None, trajectory: dict = None) -> str:
        """生成EIC指导意见 (含共识分析和趋势)"""
        lines = []
        lines.append(f"【EIC综合评审意见 - 第{current_round}轮】\n")

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
            lines.append("")

        # 审稿人分歧提示
        if consensus and consensus.get('disagreement_dims'):
            lines.append("⚡ 审稿人分歧提示:")
            for flag in consensus['disagreement_dims']:
                dim_name = REVIEW_DIMENSIONS.get(flag['dimension'], {}).get('name', flag['dimension'])
                scores_str = ", ".join(f"{rid[-1]}: {s:.1f}" for rid, s in flag['scores'].items())
                lines.append(f"  - {dim_name}: 审稿人评分 [{scores_str}] (分差: {flag['max_diff']:.1f})")
            lines.append("  EIC已采用专家加权评分以协调分歧。")
            lines.append("")

        # 趋势分析
        if trajectory and trajectory.get('trend') != 'insufficient_data':
            trend_label = {
                'strong_improvement': '显著提升', 'moderate_improvement': '稳步提升',
                'slight_improvement': '略有提升', 'stagnant': '趋于停滞',
                'declining': '质量下降'
            }.get(trajectory['trend'], trajectory['trend'])
            lines.append(f"📊 质量趋势: {trend_label} (每轮变化: {trajectory['improvement_rate']:+.2f})")
            if trajectory['projected_rounds_to_accept'] < float('inf'):
                lines.append(f"   预计 ~{trajectory['projected_rounds_to_accept']:.0f} 轮后可达接受标准")

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
        - 再审时验证前轮意见是否被解决
        - 基于解决情况调整评分
        """
        version = self.store.get_latest_version(manuscript.manuscript_id)
        scores = {}
        base_quality = random.uniform(4.5, 8.5)

        # 再审时，基于前一轮评分 + 实际解决情况调整
        addressed_ratio = 0.0
        if is_re_review and manuscript.current_round > 1:
            prev_reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round - 1)
            my_prev = next((r for r in prev_reviews if r.get('reviewer_id') == self.id), None)
            if my_prev:
                prev_avg = my_prev.get('overall_score', base_quality)
                # 验证前轮意见解决情况
                prev_comments = my_prev.get('comments', [])
                addressed_ratio = self._check_addressed_ratio(prev_comments, manuscript)
                # 改善幅度与解决率成正比
                improvement = addressed_ratio * random.uniform(1.0, 2.5) + random.uniform(0.0, 0.5)
                base_quality = min(prev_avg + improvement, 9.5)

        for dim, info in REVIEW_DIMENSIONS.items():
            if dim in self.expertise:
                score = base_quality + random.uniform(-1.0, 0.5) - (self.strictness * 0.5)
            else:
                score = base_quality + random.uniform(-1.5, 1.0)
            scores[dim] = round(max(1.0, min(10.0, score)), 1)

        overall_score = sum(scores[d] * REVIEW_DIMENSIONS[d]['weight'] for d in scores)

        # 生成审稿意见 (含前轮验证)
        comments = self._generate_comments(scores, is_re_review, manuscript)
        # 评分-意见一致性检查
        comments = self._enforce_consistency(scores, comments, manuscript.current_round)

        if overall_score >= 8.0:
            decision = ReviewDecision.ACCEPT.value
        elif overall_score >= 6.5:
            decision = ReviewDecision.MINOR_REVISION.value
        elif overall_score >= 4.5:
            decision = ReviewDecision.MAJOR_REVISION.value
        else:
            decision = ReviewDecision.REJECT.value

        # 基于专长计算信心
        n_expert_dims = sum(1 for d in scores if d in self.expertise)
        confidence = 0.6 + 0.1 * n_expert_dims + 0.05 * (1 if is_re_review else 0)
        confidence = round(min(0.95, confidence + random.uniform(-0.05, 0.05)), 2)

        report = ReviewReport(
            reviewer_id=self.id,
            reviewer_name=self.name,
            round_number=manuscript.current_round,
            decision=decision,
            overall_score=round(overall_score, 2),
            scores=scores,
            comments=[asdict(c) if isinstance(c, ReviewComment) else c for c in comments],
            summary=self._generate_summary(scores, decision, addressed_ratio if is_re_review else None),
            confidence=confidence
        )

        report_dict = asdict(report)
        self.store.store_review(manuscript.manuscript_id, report_dict)
        manuscript.review_reports.append(report_dict)

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

    def _check_addressed_ratio(self, prev_comments: list, manuscript: ManuscriptState) -> float:
        """检查前轮意见中被作者回复的比例"""
        if not prev_comments:
            return 0.5
        revision_history = st.session_state.get('revision_history', [])
        if not revision_history:
            return 0.3
        latest_revision = revision_history[-1]
        author_responses = latest_revision.get('response', {}).get('responses', [])
        addressed = 0
        for pc in prev_comments:
            pc_text = pc.get('comment', '') if isinstance(pc, dict) else getattr(pc, 'comment', '')
            pc_cat = pc.get('category', '') if isinstance(pc, dict) else getattr(pc, 'category', '')
            for resp in author_responses:
                if resp.get('original_comment', '') == pc_text or resp.get('category', '') == pc_cat:
                    if resp.get('addressed', False):
                        addressed += 1
                    break
        return addressed / len(prev_comments)

    def _generate_comments(self, scores: dict, is_re_review: bool, manuscript: ManuscriptState) -> list:
        """生成审稿意见 (再审时验证前轮)"""
        comments = []

        # 再审时先验证前轮意见
        if is_re_review and manuscript.current_round > 1:
            verified = self._verify_previous_comments(manuscript)
            comments.extend(verified)

        # 基于当前评分生成新意见
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

            n_comments = 2 if dim in self.expertise else 1
            selected = random.sample(pool, min(n_comments, len(pool)))

            for text in selected:
                # 避免与验证携带的意见重复
                if any((getattr(c, 'comment', '') if isinstance(c, ReviewComment) else c.get('comment', '')) == text for c in comments):
                    continue
                comment = ReviewComment(
                    reviewer_id=self.id, category=dim, severity=severity,
                    comment=text, addressed=False,
                    resolution=CommentResolution.PENDING.value,
                    round_created=manuscript.current_round
                )
                comments.append(comment)
        return comments

    def _verify_previous_comments(self, manuscript: ManuscriptState) -> list:
        """验证前轮意见是否被作者解决"""
        prev_reviews = self.store.get_reviews(manuscript.manuscript_id, manuscript.current_round - 1)
        my_prev = next((r for r in prev_reviews if r.get('reviewer_id') == self.id), None)
        if not my_prev:
            return []

        prev_comments = my_prev.get('comments', [])
        revision_history = st.session_state.get('revision_history', [])
        author_responses = []
        if revision_history:
            author_responses = revision_history[-1].get('response', {}).get('responses', [])

        verified = []
        for pc in prev_comments:
            pc_text = pc.get('comment', '')
            pc_cat = pc.get('category', '')
            pc_sev = pc.get('severity', '')

            # 查找匹配的作者回复
            match = None
            for resp in author_responses:
                if resp.get('original_comment', '') == pc_text or (
                        resp.get('category') == pc_cat and resp.get('severity') == pc_sev):
                    match = resp
                    break

            # 基于审稿人严格度判定解决状态
            if match and match.get('addressed', False):
                resolve_prob = 1.0 - (self.strictness * 0.5)
                roll = random.random()
                if roll < resolve_prob * 0.7:
                    resolution = CommentResolution.ADDRESSED.value
                elif roll < resolve_prob:
                    resolution = CommentResolution.PARTIALLY_ADDRESSED.value
                else:
                    resolution = CommentResolution.NOT_ADDRESSED.value
            else:
                resolution = CommentResolution.NOT_ADDRESSED.value

            # 未完全解决的意见携带到新轮
            if resolution != CommentResolution.ADDRESSED.value:
                carried = ReviewComment(
                    reviewer_id=self.id, category=pc_cat, severity=pc_sev,
                    comment=pc_text, addressed=False,
                    resolution=resolution,
                    verification_note=f"来自第{manuscript.current_round - 1}轮",
                    round_created=pc.get('round_created', manuscript.current_round - 1)
                )
                verified.append(carried)
            else:
                # 已解决的也记录 (标记为addressed)
                resolved = ReviewComment(
                    reviewer_id=self.id, category=pc_cat, severity=pc_sev,
                    comment=pc_text, addressed=True,
                    resolution=CommentResolution.ADDRESSED.value,
                    round_resolved=manuscript.current_round,
                    round_created=pc.get('round_created', manuscript.current_round - 1)
                )
                verified.append(resolved)

        return verified

    def _enforce_consistency(self, scores: dict, comments: list, current_round: int) -> list:
        """确保评分与意见严重度一致"""
        comment_dims = set()
        for c in comments:
            cat = getattr(c, 'category', '') if isinstance(c, ReviewComment) else c.get('category', '')
            sev = getattr(c, 'severity', '') if isinstance(c, ReviewComment) else c.get('severity', '')
            comment_dims.add((cat, sev))

        for dim, score in scores.items():
            if score < 5.0:
                has_severe = any(cat == dim and sev in ('critical', 'major') for cat, sev in comment_dims)
                if not has_severe:
                    templates = REVIEW_TEMPLATES.get(dim, {})
                    pool = templates.get('major', templates.get('critical', []))
                    if pool:
                        text = random.choice(pool)
                        if not any((getattr(c, 'comment', '') if isinstance(c, ReviewComment) else c.get('comment', '')) == text for c in comments):
                            comments.append(ReviewComment(
                                reviewer_id=self.id, category=dim, severity='major',
                                comment=text, round_created=current_round
                            ))
        return comments

    def _generate_summary(self, scores: dict, decision: str, addressed_ratio: float = None) -> str:
        """生成审稿总结"""
        strong = [REVIEW_DIMENSIONS[d]['name'] for d, s in scores.items() if s >= 7.0]
        weak = [REVIEW_DIMENSIONS[d]['name'] for d, s in scores.items() if s < 6.0]

        lines = [f"【{self.name} 审稿总结】"]
        if strong:
            lines.append(f"优势方面: {', '.join(strong)}")
        if weak:
            lines.append(f"待改进方面: {', '.join(weak)}")
        if addressed_ratio is not None:
            lines.append(f"前轮意见解决率: {addressed_ratio:.0%}")

        decision_text = {
            'accept': '建议接受', 'minor_revision': '建议小修后接受',
            'major_revision': '建议大修后重审', 'reject': '建议拒稿'
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

        策略：
        1. 关键问题优先 (必须全部回复)
        2. 检测审稿人冲突意见 → 生成rebuttal
        3. 重要问题认真处理
        4. 小问题简短回复
        """
        responses = []
        conflicts = self._detect_conflicts(synthesis)

        # 按优先级排序
        priority_groups = [
            ('critical', synthesis.get('critical_issues', [])),
            ('major', synthesis.get('major_issues', [])),
            ('minor', synthesis.get('minor_issues', []))
        ]

        for severity, issues in priority_groups:
            for comment in issues:
                category = comment.get('category', 'general')

                # 检测是否属于冲突意见
                is_conflict = any(
                    c['comment_a'].get('comment') == comment.get('comment') or
                    c['comment_b'].get('comment') == comment.get('comment')
                    for c in conflicts
                )

                if is_conflict:
                    resp_text = self._generate_rebuttal(comment, conflicts)
                    addressed = False
                    resolution = CommentResolution.PARTIALLY_ADDRESSED.value
                elif severity == 'minor' and random.random() < 0.1:
                    resp_text = "感谢审稿人的建议，我们认同此观点并计划在后续工作中进一步完善。"
                    addressed = False
                    resolution = CommentResolution.PARTIALLY_ADDRESSED.value
                else:
                    actions = REVISION_ACTIONS.get(category, ["进行了相应修改"])
                    action = random.choice(actions)
                    templates = AUTHOR_RESPONSE_TEMPLATES.get(severity, AUTHOR_RESPONSE_TEMPLATES['minor'])
                    template = random.choice(templates)
                    resp_text = template.format(
                        action=action,
                        detail=f"已在修改稿中进行标注（见{category}相关章节）",
                        result="改进效果显著",
                        section=random.choice(["2", "3", "4", "5"])
                    )
                    addressed = True
                    resolution = CommentResolution.ADDRESSED.value

                responses.append({
                    'original_comment': comment.get('comment', ''),
                    'category': category,
                    'severity': severity,
                    'response': resp_text,
                    'addressed': addressed,
                    'resolution': resolution,
                    'is_conflict': is_conflict
                })

        addressed_count = sum(1 for r in responses if r['addressed'])
        total = sum(len(issues) for _, issues in priority_groups)
        return {
            'round': manuscript.current_round,
            'total_issues': total,
            'addressed_count': addressed_count,
            'conflict_count': len(conflicts),
            'responses': responses,
            'strategy_summary': f"回复 {total} 条意见: {addressed_count} 已解决, "
                                f"{len(conflicts)} 冲突处理"
        }

    def _detect_conflicts(self, synthesis: dict) -> list:
        """检测不同审稿人对同一维度的冲突意见"""
        conflicts = []
        all_issues = (
            synthesis.get('critical_issues', []) +
            synthesis.get('major_issues', []) +
            synthesis.get('minor_issues', [])
        )

        by_category = {}
        for issue in all_issues:
            cat = issue.get('category', '')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(issue)

        for cat, issues in by_category.items():
            if len(issues) < 2:
                continue
            severities = set(i.get('severity', '') for i in issues)
            if 'critical' in severities and 'minor' in severities:
                critical_items = [i for i in issues if i.get('severity') == 'critical']
                minor_items = [i for i in issues if i.get('severity') == 'minor']
                if critical_items and minor_items:
                    conflicts.append({
                        'category': cat,
                        'comment_a': critical_items[0],
                        'comment_b': minor_items[0],
                        'type': 'severity_mismatch'
                    })
        return conflicts

    def _generate_rebuttal(self, comment: dict, conflicts: list) -> str:
        """生成礼貌的反驳回复"""
        category = comment.get('category', '')
        dim_name = REVIEW_DIMENSIONS.get(category, {}).get('name', category)
        return (f"我们注意到审稿人对{dim_name}方面的评价存在分歧。"
                f"我们已仔细考虑各方意见，在保持原有方法优势的基础上进行了针对性改进，"
                f"并补充了额外的论证。恳请编辑综合裁量。")

    def revise_manuscript(self, manuscript: ManuscriptState, feedback_response: dict) -> ManuscriptVersion:
        """修改稿件，基于反馈类别针对性修改对应章节"""
        prev_version = self.store.get_latest_version(manuscript.manuscript_id)
        new_version_num = manuscript.current_version + 1
        revision_notes = self._generate_revision_notes(feedback_response)

        # 确定哪些章节需要修改
        modified_categories = set()
        for resp in feedback_response.get('responses', []):
            if resp.get('addressed', False):
                modified_categories.add(resp.get('category', ''))

        # 类别到章节的映射
        category_to_section = {
            'novelty': 'introduction',
            'methodology': 'methodology',
            'data_analysis': 'results',
            'significance': 'discussion',
            'writing': 'conclusion'
        }

        new_sections = {}
        if prev_version and prev_version.get('content_sections'):
            for sec, content in prev_version['content_sections'].items():
                # 只修改与反馈类别相关的章节
                modified_by = [cat for cat, s in category_to_section.items()
                               if s == sec and cat in modified_categories]
                if modified_by:
                    cats_label = ','.join(modified_by)
                    new_sections[sec] = content + f"\n[v{new_version_num} 修改: 回应{cats_label}意见]"
                else:
                    new_sections[sec] = content
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
            content_hash=hashlib.md5(json.dumps(new_sections, sort_keys=True).encode()).hexdigest()[:12]
        )

        manuscript.current_version = new_version_num
        self.store.store_manuscript(manuscript.manuscript_id, asdict(new_version))
        manuscript.versions.append(asdict(new_version))

        addressed = feedback_response.get('addressed_count', 0)
        total = feedback_response.get('total_issues', 0)
        msg = AgentMessage(
            sender=self.id, sender_role="author",
            receiver="eic_001", receiver_role="eic",
            msg_type=MessageType.REVISION.value,
            content=f"已提交第{new_version_num}版修改稿，解决{addressed}/{total}条审稿意见。",
            metadata={'version': new_version_num, 'response': feedback_response},
            round_number=manuscript.current_round
        )
        self.store.send_message(msg)
        manuscript.message_log.append(asdict(msg))
        return new_version

    def _generate_revision_notes(self, feedback_response: dict) -> str:
        """生成修改说明文档"""
        lines = [f"=== 修改说明 (Revision Notes) ===\n"]
        lines.append(f"本次修改共回复 {feedback_response.get('total_issues', 0)} 条审稿意见。")
        lines.append(f"策略: {feedback_response.get('strategy_summary', '')}\n")

        for i, resp in enumerate(feedback_response.get('responses', []), 1):
            conflict_tag = " [冲突]" if resp.get('is_conflict') else ""
            lines.append(f"--- 问题 {i} [{resp['severity'].upper()}] [{resp['category']}]{conflict_tag} ---")
            lines.append(f"审稿意见: {resp['original_comment']}")
            lines.append(f"作者回复: {resp['response']}")
            lines.append(f"解决状态: {resp.get('resolution', 'pending')}")
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
        self.score_history = []

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

        # 记录评分历史
        self.score_history.append(synthesis.get('overall_avg', 0))

        return {
            'round': manuscript.current_round,
            'reports': reports,
            'synthesis': synthesis,
            'recommendation': synthesis.get('eic_recommendation', 'pending')
        }

    def author_revise(self, manuscript: ManuscriptState, synthesis: dict) -> dict:
        """作者修改流程"""
        response = self.author.process_feedback(manuscript, synthesis)
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

    def is_process_complete(self, manuscript: ManuscriptState, synthesis: dict) -> tuple:
        """
        判断审稿流程是否结束

        终止条件:
        1. ACCEPT 或 REJECT
        2. 达到最大轮数
        3. 小修且无关键问题 (round > 1)
        4. 评分持续收敛 (连续两轮改善 < 0.5)

        Returns: (is_complete: bool, reason: str)
        """
        rec = synthesis.get('eic_recommendation', '')

        if rec == ReviewDecision.ACCEPT.value:
            return True, "accepted"
        if rec == ReviewDecision.REJECT.value:
            return True, "rejected"

        # 最大轮数
        if manuscript.current_round >= manuscript.max_rounds:
            return True, "max_rounds_reached"

        # 小修 + 无关键问题 + 已经过至少1轮修改
        if (rec == ReviewDecision.MINOR_REVISION.value and
                manuscript.current_round > 1 and
                synthesis.get('critical_count', 0) == 0):
            return True, "minor_revision_accepted"

        # 收敛检测
        if len(self.score_history) >= 3:
            d1 = self.score_history[-1] - self.score_history[-2]
            d2 = self.score_history[-2] - self.score_history[-3]
            if d1 < 0.5 and d2 < 0.5:
                return True, "diminishing_returns"

        return False, ""


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


def render_comment_tracker():
    """渲染意见追踪面板"""
    review_history = st.session_state.get('review_history', [])
    if not review_history:
        st.info("暂无审稿意见")
        return

    summary = CommentTracker.get_resolution_summary(review_history)
    total = summary['total']
    addressed = summary['addressed']
    partial = summary['partially_addressed']
    unresolved = summary['not_addressed'] + summary['pending']

    st.markdown("#### 意见解决状态追踪")

    cols = st.columns(4)
    with cols[0]:
        st.metric("总意见数", total)
    with cols[1]:
        st.metric("已解决", addressed)
    with cols[2]:
        st.metric("部分解决", partial)
    with cols[3]:
        st.metric("未解决", unresolved)

    if total > 0:
        st.progress(addressed / total, text=f"{addressed}/{total} 意见已解决 ({addressed / total:.0%})")

    # 详细列表
    all_comments = CommentTracker.get_all_comments(review_history)
    if all_comments:
        rows = []
        for c in all_comments:
            resolution = c.get('resolution', c.get('resolution_status', 'pending'))
            icon = {
                'addressed': '✅', 'partially_addressed': '🟡',
                'not_addressed': '❌', 'pending': '⏳'
            }.get(resolution, '⏳')
            rows.append({
                '状态': icon,
                '审稿人': c.get('reviewer_id', '')[-1:] if c.get('reviewer_id') else '?',
                '严重度': c.get('severity', ''),
                '维度': REVIEW_DIMENSIONS.get(c.get('category', ''), {}).get('name', c.get('category', '')),
                '意见': c.get('comment', '')[:60] + '...' if len(c.get('comment', '')) > 60 else c.get('comment', ''),
                '解决状态': resolution
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_version_diff():
    """渲染版本对比视图"""
    ms_state = st.session_state.get('ms_state')
    coordinator = st.session_state.get('coordinator')
    if not ms_state or not coordinator:
        return

    versions = coordinator.store.get_manuscript_versions(ms_state.manuscript_id)
    if len(versions) < 2:
        st.info("至少需要2个版本才能对比")
        return

    st.markdown("#### 版本对比")
    version_labels = [f"v{v.get('version', i + 1)}" for i, v in enumerate(versions)]

    col1, col2 = st.columns(2)
    with col1:
        v1_idx = st.selectbox("基准版本", range(len(versions)),
                              format_func=lambda i: version_labels[i], key="diff_v1")
    with col2:
        v2_idx = st.selectbox("对比版本", range(len(versions)),
                              index=min(v1_idx + 1, len(versions) - 1),
                              format_func=lambda i: version_labels[i], key="diff_v2")

    if v1_idx != v2_idx:
        diff = VersionDiffer.diff_versions(versions[v1_idx], versions[v2_idx])
        modified = diff['modified_sections']
        total = diff['total_sections']
        st.markdown(f"**{version_labels[v1_idx]} → {version_labels[v2_idx]}** | "
                    f"修改了 {len(modified)}/{total} 个章节")

        for sec, info in diff['section_diffs'].items():
            status = info['status']
            icon = {'added': '🟢', 'removed': '🔴', 'modified': '🟠', 'unchanged': '⚪'}.get(status, '?')
            if status != 'unchanged':
                with st.expander(f"{icon} {sec} ({status})"):
                    if status == 'modified':
                        st.text(f"旧版: {info['old']}")
                        st.text(f"新版: {info['new']}")
                    elif status == 'added':
                        st.text(f"新增: {info['new']}")
            else:
                st.markdown(f"{icon} {sec} (未修改)")


def render_convergence_chart():
    """渲染收敛趋势图"""
    reviews = st.session_state.get('review_history', [])
    if len(reviews) < 1:
        return

    import altair as alt
    round_data = []
    for rh in reviews:
        round_num = rh.get('round', 1)
        scores = [r.get('overall_score', 0) for r in rh.get('reports', [])]
        avg = sum(scores) / len(scores) if scores else 0
        round_data.append({'Round': f"第{round_num}轮", 'round_num': round_num, 'Score': avg})

    if not round_data:
        return

    df = pd.DataFrame(round_data)

    # 评分线
    line = alt.Chart(df).mark_line(point=True, color='#0d6efd', strokeWidth=3).encode(
        x=alt.X('round_num:Q', title='审稿轮次', axis=alt.Axis(tickMinStep=1)),
        y=alt.Y('Score:Q', title='综合评分', scale=alt.Scale(domain=[0, 10])),
        tooltip=['Round', 'Score']
    )

    # 接受阈值线
    threshold = alt.Chart(pd.DataFrame({'y': [7.5]})).mark_rule(
        color='#198754', strokeDash=[5, 5], strokeWidth=2
    ).encode(y='y:Q')

    # 拒稿阈值线
    reject_line = alt.Chart(pd.DataFrame({'y': [4.5]})).mark_rule(
        color='#dc3545', strokeDash=[5, 5], strokeWidth=2
    ).encode(y='y:Q')

    chart = (line + threshold + reject_line).properties(
        title='评分收敛趋势 (绿线=接受阈值, 红线=拒稿阈值)',
        height=250
    ).interactive()

    st.altair_chart(chart, use_container_width=True)


def render_disagreement_heatmap():
    """渲染审稿人分歧热力图"""
    reviews = st.session_state.get('review_history', [])
    if not reviews:
        return

    latest = reviews[-1]
    reports = latest.get('reports', [])
    if not reports:
        return

    import altair as alt
    heatmap_data = []
    for report in reports:
        reviewer = report.get('reviewer_name', '?')
        for dim, score in report.get('scores', {}).items():
            dim_name = REVIEW_DIMENSIONS.get(dim, {}).get('name', dim)
            heatmap_data.append({
                'Reviewer': reviewer,
                'Dimension': dim_name,
                'Score': score
            })

    if not heatmap_data:
        return

    df = pd.DataFrame(heatmap_data)

    chart = alt.Chart(df).mark_rect().encode(
        x=alt.X('Dimension:N', title='评审维度'),
        y=alt.Y('Reviewer:N', title='审稿人'),
        color=alt.Color('Score:Q', scale=alt.Scale(scheme='redyellowgreen', domain=[1, 10]),
                         title='评分'),
        tooltip=['Reviewer', 'Dimension', 'Score']
    ).properties(
        title='审稿人评分矩阵',
        height=200
    )

    st.altair_chart(chart, use_container_width=True)


def generate_review_report_text() -> str:
    """生成完整的审稿报告文本 (可下载)"""
    ms_state = st.session_state.get('ms_state')
    review_history = st.session_state.get('review_history', [])
    revision_history = st.session_state.get('revision_history', [])
    final_decision = st.session_state.get('final_decision', {})

    lines = []
    lines.append("=" * 60)
    lines.append("          分布式审稿协调系统 - 完整审稿报告")
    lines.append("   Distributed Storage Coordination Agent Review Report")
    lines.append("=" * 60)
    lines.append("")

    if ms_state:
        lines.append(f"稿件编号: {ms_state.manuscript_id}")
        lines.append(f"审稿轮数: {ms_state.current_round}")
        lines.append(f"稿件版本: v{ms_state.current_version}")
        lines.append(f"最终状态: {ms_state.status}")
        if ms_state.versions:
            v1 = ms_state.versions[0]
            lines.append(f"论文标题: {v1.get('title', '未知')}")
            lines.append(f"摘要: {v1.get('abstract', '')}")
        lines.append("")

    # 最终决定
    if final_decision:
        lines.append("-" * 40)
        lines.append("【最终决定】")
        lines.append(f"  决定: {final_decision.get('decision', '未知')}")
        lines.append(f"  原因: {final_decision.get('reason', '')}")
        lines.append(f"  平均分: {final_decision.get('avg_score', 0):.1f}/10")
        lines.append("")

    # 各轮审稿
    for i, rh in enumerate(review_history, 1):
        lines.append("=" * 40)
        lines.append(f"第 {i} 轮审稿")
        lines.append("=" * 40)

        synthesis = rh.get('synthesis', {})
        lines.append(f"EIC建议: {synthesis.get('eic_recommendation', '?')}")
        lines.append(f"综合评分: {synthesis.get('overall_avg', 0):.1f}/10")
        lines.append(f"共识度: {synthesis.get('consensus_level', 1.0):.0%}")
        lines.append(f"关键问题: {synthesis.get('critical_count', 0)} | "
                     f"重要问题: {synthesis.get('major_count', 0)} | "
                     f"小问题: {synthesis.get('minor_count', 0)}")
        lines.append("")

        for report in rh.get('reports', []):
            lines.append(f"  --- {report.get('reviewer_name', '?')} ---")
            lines.append(f"  总评分: {report.get('overall_score', 0):.1f}/10")
            lines.append(f"  建议: {report.get('decision', '?')}")
            lines.append(f"  信心: {report.get('confidence', 0):.0%}")

            scores = report.get('scores', {})
            if scores:
                lines.append("  维度评分:")
                for dim, score in scores.items():
                    dim_name = REVIEW_DIMENSIONS.get(dim, {}).get('name', dim)
                    lines.append(f"    {dim_name}: {score:.1f}/10")

            comments = report.get('comments', [])
            if comments:
                lines.append("  审稿意见:")
                for c in comments:
                    sev = c.get('severity', '')
                    cat = REVIEW_DIMENSIONS.get(c.get('category', ''), {}).get('name', c.get('category', ''))
                    resolution = c.get('resolution', '')
                    res_tag = f" [{resolution}]" if resolution and resolution != 'pending' else ""
                    lines.append(f"    [{sev.upper()}][{cat}] {c.get('comment', '')}{res_tag}")
            lines.append(f"  总结: {report.get('summary', '')}")
            lines.append("")

        # EIC指导意见
        guidance = synthesis.get('guidance', '')
        if guidance:
            lines.append("  EIC指导意见:")
            for gl in guidance.split('\n'):
                lines.append(f"    {gl}")
            lines.append("")

    # 修改历史
    if revision_history:
        lines.append("=" * 40)
        lines.append("修改历史")
        lines.append("=" * 40)

        for i, rev in enumerate(revision_history, 1):
            lines.append(f"\n第 {i} 次修改 (版本 v{rev.get('version_number', '?')})")
            response = rev.get('response', {})
            lines.append(f"策略: {response.get('strategy_summary', '')}")
            lines.append(f"总意见数: {response.get('total_issues', 0)} | "
                         f"已解决: {response.get('addressed_count', 0)}")

            for j, resp in enumerate(response.get('responses', []), 1):
                conflict_tag = " [冲突]" if resp.get('is_conflict') else ""
                lines.append(f"  问题{j} [{resp.get('severity', '').upper()}]"
                             f"[{resp.get('category', '')}]{conflict_tag}")
                lines.append(f"    审稿意见: {resp.get('original_comment', '')}")
                lines.append(f"    作者回复: {resp.get('response', '')}")
                lines.append(f"    解决状态: {resp.get('resolution', '')}")
            lines.append("")

    # 意见追踪摘要
    summary = CommentTracker.get_resolution_summary(review_history)
    if summary['total'] > 0:
        lines.append("=" * 40)
        lines.append("意见解决状态摘要")
        lines.append("=" * 40)
        lines.append(f"总意见数: {summary['total']}")
        lines.append(f"已解决: {summary['addressed']}")
        lines.append(f"部分解决: {summary['partially_addressed']}")
        lines.append(f"未解决: {summary['not_addressed']}")
        lines.append(f"待定: {summary['pending']}")
        lines.append(f"解决率: {summary['addressed'] / summary['total']:.0%}")

    lines.append("\n" + "=" * 60)
    lines.append("报告生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_export_json() -> str:
    """生成JSON格式的完整审稿数据 (可下载)"""
    ms_state = st.session_state.get('ms_state')
    export = {
        'manuscript': {
            'id': ms_state.manuscript_id if ms_state else '',
            'round': ms_state.current_round if ms_state else 0,
            'version': ms_state.current_version if ms_state else 0,
            'status': ms_state.status if ms_state else '',
            'versions': ms_state.versions if ms_state else [],
        },
        'review_history': st.session_state.get('review_history', []),
        'revision_history': st.session_state.get('revision_history', []),
        'final_decision': st.session_state.get('final_decision', {}),
        'messages': st.session_state.get('store_messages', []),
        'export_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return json.dumps(export, ensure_ascii=False, indent=2, default=str)


def render_download_panel():
    """渲染下载面板"""
    st.markdown("### 📥 文档下载")

    col1, col2, col3 = st.columns(3)

    with col1:
        report_text = generate_review_report_text()
        ms_state = st.session_state.get('ms_state')
        filename = f"review_report_{ms_state.manuscript_id if ms_state else 'draft'}.txt"
        st.download_button(
            label="📄 下载审稿报告 (TXT)",
            data=report_text,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        json_data = generate_export_json()
        json_filename = f"review_data_{ms_state.manuscript_id if ms_state else 'draft'}.json"
        st.download_button(
            label="📊 下载完整数据 (JSON)",
            data=json_data,
            file_name=json_filename,
            mime="application/json",
            use_container_width=True
        )

    with col3:
        # CSV格式的评分汇总
        review_history = st.session_state.get('review_history', [])
        csv_rows = []
        for rh in review_history:
            round_num = rh.get('round', 1)
            for report in rh.get('reports', []):
                row = {
                    '轮次': round_num,
                    '审稿人': report.get('reviewer_name', '?'),
                    '总评分': report.get('overall_score', 0),
                    '建议': report.get('decision', ''),
                    '信心': report.get('confidence', 0),
                }
                for dim, score in report.get('scores', {}).items():
                    dim_name = REVIEW_DIMENSIONS.get(dim, {}).get('name', dim)
                    row[dim_name] = score
                csv_rows.append(row)

        if csv_rows:
            csv_df = pd.DataFrame(csv_rows)
            csv_data = csv_df.to_csv(index=False, encoding='utf-8-sig')
            csv_filename = f"review_scores_{ms_state.manuscript_id if ms_state else 'draft'}.csv"
            st.download_button(
                label="📈 下载评分数据 (CSV)",
                data=csv_data,
                file_name=csv_filename,
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("📈 评分数据 (暂无)", disabled=True, use_container_width=True)


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

    PHASE_ORDER = {"init": 0, "reviewing": 1, "feedback": 3, "revising": 4, "complete": 5}
    current_idx = PHASE_ORDER.get(current_phase, 0)

    cols = st.columns(len(phases))
    for i, (label, phase) in enumerate(phases):
        with cols[i]:
            if i == current_idx or (i == current_idx + 1 and phase == current_phase):
                st.markdown(f"**▶ {label}**")
            elif i < current_idx:
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

            # 审稿报告 (含新增的意见追踪、分歧分析标签页)
            tab_reports, tab_synthesis, tab_tracker, tab_trend, tab_heatmap = st.tabs([
                "📋 审稿报告", "📝 EIC综合意见", "🔍 意见追踪", "📈 评分趋势", "🗺 分歧分析"
            ])

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
                st.markdown(f"**综合评分 (专家加权):** {synthesis.get('overall_avg', 0):.1f}/10")
                consensus_level = synthesis.get('consensus_level', 1.0)
                st.markdown(f"**共识度:** {consensus_level:.0%}")
                st.markdown(f"**关键问题:** {synthesis.get('critical_count', 0)} | "
                            f"**重要问题:** {synthesis.get('major_count', 0)} | "
                            f"**小问题:** {synthesis.get('minor_count', 0)}")

                # 分歧警告
                disagreements = synthesis.get('disagreement_dims', [])
                if disagreements:
                    st.warning(f"检测到 {len(disagreements)} 个维度存在审稿人分歧")

                guidance = synthesis.get('guidance', '')
                if guidance:
                    st.text_area("EIC指导意见", guidance, height=300, disabled=True)

            with tab_tracker:
                render_comment_tracker()

            with tab_trend:
                render_score_trend()
                render_convergence_chart()

            with tab_heatmap:
                render_disagreement_heatmap()

            # 判断流程是否结束 (新签名: 传入manuscript)
            is_complete, reason = coordinator.is_process_complete(ms_state, synthesis)
            if is_complete:
                # 调用正式最终决定
                final = coordinator.eic.make_final_decision(ms_state)
                st.session_state.final_decision = final
                st.session_state.termination_reason = reason
                if final['decision'] in [ReviewDecision.ACCEPT.value, ReviewDecision.MINOR_REVISION.value]:
                    ms_state.status = "accepted"
                else:
                    ms_state.status = "rejected"
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

        # 使用正式最终决定 (如果有)
        final_decision = st.session_state.get('final_decision', {})
        rec = final_decision.get('decision', synthesis.get('eic_recommendation', 'pending'))
        reason = st.session_state.get('termination_reason', '')

        st.markdown("### 🏁 审稿流程完成")

        reason_labels = {
            'accepted': '审稿人共识接受',
            'rejected': '审稿人建议拒稿',
            'max_rounds_reached': f'达到最大轮数 ({ms_state.max_rounds})',
            'minor_revision_accepted': '小修后无关键问题，予以接受',
            'diminishing_returns': '评分收敛，不再有显著提升'
        }
        reason_text = reason_labels.get(reason, '')

        if rec in [ReviewDecision.ACCEPT.value, ReviewDecision.MINOR_REVISION.value]:
            st.success(f"🎉 恭喜！稿件经过 {ms_state.current_round} 轮审稿后被接受！")
            if reason_text:
                st.info(f"终止原因: {reason_text}")
            st.balloons()
        else:
            st.error(f"稿件在第 {ms_state.current_round} 轮后被拒稿。")
            if reason_text:
                st.info(f"终止原因: {reason_text}")

        if final_decision.get('reason'):
            st.markdown(f"**EIC最终意见:** {final_decision['reason']}")

        # 完整历史 (多标签页)
        tab_history, tab_revisions, tab_tracker, tab_diff, tab_convergence = st.tabs([
            "📜 审稿历史", "📝 修改历史", "🔍 意见追踪", "📄 版本对比", "📈 收敛趋势"
        ])

        with tab_history:
            for i, rh in enumerate(reviews, 1):
                with st.expander(f"第 {i} 轮审稿", expanded=(i == len(reviews))):
                    for report in rh.get('reports', []):
                        render_review_report(report, i)
                    syn = rh.get('synthesis', {})
                    if syn:
                        st.markdown(f"**EIC建议:** {syn.get('eic_recommendation', '')} | "
                                    f"**综合评分:** {syn.get('overall_avg', 0):.1f} | "
                                    f"**共识度:** {syn.get('consensus_level', 1.0):.0%}")

        with tab_revisions:
            if st.session_state.revision_history:
                for i, rev in enumerate(st.session_state.revision_history, 1):
                    with st.expander(f"第 {i} 次修改 (版本 {rev.get('version_number', '?')})"):
                        render_revision_response(rev)
            else:
                st.info("无修改记录")

        with tab_tracker:
            render_comment_tracker()

        with tab_diff:
            render_version_diff()

        with tab_convergence:
            render_convergence_chart()
            render_score_trend()

        # 下载面板
        st.divider()
        render_download_panel()

    # ---- 底部面板 ----
    st.divider()
    tab_msg, tab_log, tab_store, tab_vdiff = st.tabs(["💬 消息流", "📋 事件日志", "🗄 存储状态", "📄 版本对比"])

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

    with tab_vdiff:
        render_version_diff()


if __name__ == "__main__":
    main()
