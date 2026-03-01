#!/usr/bin/env python3
"""
分布式审稿协调系统 - MCP Server Plugin
Manuscript Review Coordination MCP Server

作为 MCP 插件运行，提供以下工具:
- init_review: 初始化审稿流程
- run_review: 执行一轮审稿
- author_revise: 作者修改稿件
- get_status: 查看当前状态
- get_report: 获取审稿报告
- next_round: 推进到下一轮
- export_report: 导出完整报告

安装: pip install mcp
运行: python mcp_review_server.py
"""

import json
import uuid
import random
import hashlib
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Any
from enum import Enum

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("请先安装 mcp: pip install mcp")
    raise


# ============================================================
# 数据模型
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


REVIEW_DIMENSIONS = {
    "novelty": {"name": "创新性", "weight": 0.25},
    "methodology": {"name": "方法论", "weight": 0.25},
    "writing": {"name": "写作质量", "weight": 0.15},
    "significance": {"name": "研究意义", "weight": 0.20},
    "data_analysis": {"name": "数据分析", "weight": 0.15},
}

REVIEWER_PROFILES = [
    {
        "id": "rev_001", "name": "审稿人A (方法论专家)",
        "expertise": ["methodology", "data_analysis"],
        "strictness": 0.7, "personality": "严谨型"
    },
    {
        "id": "rev_002", "name": "审稿人B (领域专家)",
        "expertise": ["novelty", "significance"],
        "strictness": 0.4, "personality": "开放型"
    },
    {
        "id": "rev_003", "name": "审稿人C (写作审查)",
        "expertise": ["writing", "methodology"],
        "strictness": 0.6, "personality": "细致型"
    },
]

REVIEW_COMMENT_POOL = {
    "novelty": {
        "critical": ["研究缺乏新意，与已有工作重复度高", "创新点不明确，需重新定位"],
        "major": ["创新性论证不足，需加强与现有方法的对比", "需更清晰地阐述核心贡献"],
        "minor": ["建议补充相关领域最新进展的讨论"],
    },
    "methodology": {
        "critical": ["研究方法存在根本性缺陷", "实验设计不合理，无法支撑结论"],
        "major": ["需补充更多实验验证", "方法描述不够详细，难以复现"],
        "minor": ["建议增加方法论的理论推导"],
    },
    "writing": {
        "critical": ["文章结构混乱，逻辑不通", "大量语法错误影响理解"],
        "major": ["部分段落表述不清", "图表质量需要提升"],
        "minor": ["个别用词不够准确", "参考文献格式需统一"],
    },
    "significance": {
        "critical": ["研究意义不明确", "应用价值有限"],
        "major": ["需加强研究影响力的论证", "应用场景描述不足"],
        "minor": ["建议讨论未来研究方向"],
    },
    "data_analysis": {
        "critical": ["数据分析方法不当", "统计检验缺失"],
        "major": ["需补充更多统计分析", "数据可视化需改进"],
        "minor": ["建议增加敏感性分析"],
    },
}

AUTHOR_RESPONSE_TEMPLATES = {
    "critical": [
        "感谢审稿人指出此关键问题。我们已{action}。{detail}",
        "非常重要的意见。我们已彻底重新设计了{action}，{detail}",
    ],
    "major": [
        "感谢建议。我们已{action}，具体修改见第{section}节。",
        "已按建议{action}，{result}",
    ],
    "minor": [
        "已修改。{action}",
        "感谢提醒，已{action}",
    ],
}

REVISION_ACTIONS = {
    "novelty": ["重新梳理了创新点", "补充了与现有方法的详细对比", "明确了核心贡献"],
    "methodology": ["完善了研究方法", "补充了实验验证", "增加了方法论的理论推导"],
    "writing": ["全文润色修改", "重新组织了文章结构", "改进了图表质量"],
    "significance": ["加强了研究意义论证", "补充了应用场景", "增加了影响力分析"],
    "data_analysis": ["补充了统计分析", "改进了数据可视化", "增加了敏感性分析"],
}


# ============================================================
# 核心引擎 (无 Streamlit 依赖)
# ============================================================

class ReviewStore:
    """审稿数据存储"""

    def __init__(self):
        self.manuscripts = {}  # {ms_id: [versions]}
        self.reviews = {}      # {ms_id: {round: [reports]}}
        self.messages = []
        self.agent_states = {}

    def store_version(self, ms_id: str, version: dict):
        if ms_id not in self.manuscripts:
            self.manuscripts[ms_id] = []
        self.manuscripts[ms_id].append(version)

    def get_latest_version(self, ms_id: str) -> dict:
        versions = self.manuscripts.get(ms_id, [])
        return versions[-1] if versions else None

    def get_all_versions(self, ms_id: str) -> list:
        return self.manuscripts.get(ms_id, [])

    def store_review(self, ms_id: str, round_num: int, report: dict):
        if ms_id not in self.reviews:
            self.reviews[ms_id] = {}
        if round_num not in self.reviews[ms_id]:
            self.reviews[ms_id][round_num] = []
        self.reviews[ms_id][round_num].append(report)

    def get_reviews(self, ms_id: str, round_num: int) -> list:
        return self.reviews.get(ms_id, {}).get(round_num, [])

    def add_message(self, msg: dict):
        self.messages.append(msg)


class EICEngine:
    """EIC 决策引擎"""

    def synthesize(self, reviews: list) -> dict:
        """综合审稿意见 (含专家加权 + 共识分析)"""
        all_comments = []
        score_data = {}
        decisions = []

        for review in reviews:
            decisions.append(review.get("decision", "pending"))
            rid = review.get("reviewer_id", "")
            profile = next((p for p in REVIEWER_PROFILES if p["id"] == rid), None)
            expertise = profile.get("expertise", []) if profile else []

            for dim, score in review.get("scores", {}).items():
                if dim not in score_data:
                    score_data[dim] = []
                score_data[dim].append({
                    "score": score, "reviewer_id": rid,
                    "is_expert": dim in expertise
                })
            for c in review.get("comments", []):
                all_comments.append(c)

        # 专家加权评分
        weighted_avg = {}
        simple_avg = {}
        variance = {}
        disagreement_dims = []

        for dim, entries in score_data.items():
            scores = [e["score"] for e in entries]
            s_avg = sum(scores) / len(scores)
            weights = [1.5 if e["is_expert"] else 1.0 for e in entries]
            w_avg = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            var = sum((s - s_avg) ** 2 for s in scores) / len(scores) if len(scores) > 1 else 0

            weighted_avg[dim] = round(w_avg, 2)
            simple_avg[dim] = round(s_avg, 2)
            variance[dim] = round(var, 2)

            if len(scores) >= 2 and max(scores) - min(scores) > 2.0:
                disagreement_dims.append({
                    "dimension": dim,
                    "name": REVIEW_DIMENSIONS.get(dim, {}).get("name", dim),
                    "max_diff": round(max(scores) - min(scores), 2),
                    "scores": {e["reviewer_id"]: e["score"] for e in entries},
                })

        # 共识度
        all_var = list(variance.values())
        consensus_level = round(max(0, 1 - sum(all_var) / len(all_var) / 10), 2) if all_var else 1.0

        # 综合评分
        overall = sum(
            weighted_avg.get(d, 0) * REVIEW_DIMENSIONS[d]["weight"]
            for d in weighted_avg
        ) if weighted_avg else 0

        critical = [c for c in all_comments if c.get("severity") == "critical"]
        major = [c for c in all_comments if c.get("severity") == "major"]
        minor = [c for c in all_comments if c.get("severity") == "minor"]
        has_critical = len(critical) > 0

        # 决策
        if overall >= 8.0 and not has_critical:
            rec = ReviewDecision.ACCEPT.value
        elif overall >= 6.0 and not has_critical:
            rec = ReviewDecision.MINOR_REVISION.value
        elif overall >= 4.0 or has_critical:
            rec = ReviewDecision.MAJOR_REVISION.value
        else:
            rec = ReviewDecision.REJECT.value

        return {
            "overall_avg": round(overall, 2),
            "weighted_avg": weighted_avg,
            "simple_avg": simple_avg,
            "consensus_level": consensus_level,
            "disagreement_dims": disagreement_dims,
            "eic_recommendation": rec,
            "reviewer_decisions": decisions,
            "critical_count": len(critical),
            "major_count": len(major),
            "minor_count": len(minor),
            "critical_issues": critical,
            "major_issues": major,
            "minor_issues": minor,
        }


class ReviewerEngine:
    """审稿人引擎"""

    def review(self, profile: dict, round_num: int,
               prev_review: dict = None, addressed_ratio: float = 0.0) -> dict:
        """生成审稿报告"""
        expertise = profile.get("expertise", [])
        strictness = profile.get("strictness", 0.5)

        base = random.uniform(4.5, 8.5)
        if prev_review:
            prev_avg = prev_review.get("overall_score", base)
            improvement = addressed_ratio * random.uniform(1.0, 2.5) + random.uniform(0.0, 0.5)
            base = min(prev_avg + improvement, 9.5)

        scores = {}
        for dim in REVIEW_DIMENSIONS:
            if dim in expertise:
                s = base + random.uniform(-1.0, 0.5) - (strictness * 0.5)
            else:
                s = base + random.uniform(-1.5, 1.0)
            scores[dim] = round(max(1.0, min(10.0, s)), 1)

        overall = sum(scores[d] * REVIEW_DIMENSIONS[d]["weight"] for d in scores)

        # 生成意见
        comments = []
        for dim, score in scores.items():
            pool_map = REVIEW_COMMENT_POOL.get(dim, {})
            if score < 4.5 and pool_map.get("critical"):
                sev, pool = "critical", pool_map["critical"]
            elif score < 6.5 and pool_map.get("major"):
                sev, pool = "major", pool_map["major"]
            elif score < 8.0 and pool_map.get("minor"):
                sev, pool = "minor", pool_map["minor"]
            else:
                continue
            n = 2 if dim in expertise else 1
            for text in random.sample(pool, min(n, len(pool))):
                comments.append({
                    "id": str(uuid.uuid4())[:8],
                    "reviewer_id": profile["id"],
                    "category": dim,
                    "severity": sev,
                    "comment": text,
                    "resolution": CommentResolution.PENDING.value,
                    "round_created": round_num,
                })

        # 一致性: 低分维度必须有对应意见
        comment_dims = {(c["category"], c["severity"]) for c in comments}
        for dim, score in scores.items():
            if score < 5.0:
                if not any(cat == dim and sev in ("critical", "major") for cat, sev in comment_dims):
                    pool = REVIEW_COMMENT_POOL.get(dim, {}).get("major", [])
                    if pool:
                        comments.append({
                            "id": str(uuid.uuid4())[:8],
                            "reviewer_id": profile["id"],
                            "category": dim, "severity": "major",
                            "comment": random.choice(pool),
                            "resolution": CommentResolution.PENDING.value,
                            "round_created": round_num,
                        })

        if overall >= 8.0:
            dec = ReviewDecision.ACCEPT.value
        elif overall >= 6.5:
            dec = ReviewDecision.MINOR_REVISION.value
        elif overall >= 4.5:
            dec = ReviewDecision.MAJOR_REVISION.value
        else:
            dec = ReviewDecision.REJECT.value

        n_expert = sum(1 for d in scores if d in expertise)
        confidence = round(min(0.95, 0.6 + 0.1 * n_expert + random.uniform(-0.05, 0.05)), 2)

        strong = [REVIEW_DIMENSIONS[d]["name"] for d, s in scores.items() if s >= 7.0]
        weak = [REVIEW_DIMENSIONS[d]["name"] for d, s in scores.items() if s < 6.0]

        return {
            "reviewer_id": profile["id"],
            "reviewer_name": profile["name"],
            "round": round_num,
            "decision": dec,
            "overall_score": round(overall, 2),
            "scores": scores,
            "comments": comments,
            "confidence": confidence,
            "summary": f"优势: {', '.join(strong) if strong else '无'} | 待改进: {', '.join(weak) if weak else '无'} | 建议: {dec}",
        }


class AuthorEngine:
    """作者引擎"""

    def respond_and_revise(self, synthesis: dict, prev_sections: dict,
                           version_num: int) -> dict:
        """处理反馈并生成修改版本"""
        responses = []
        modified_categories = set()

        priority_groups = [
            ("critical", synthesis.get("critical_issues", [])),
            ("major", synthesis.get("major_issues", [])),
            ("minor", synthesis.get("minor_issues", [])),
        ]

        for severity, issues in priority_groups:
            for comment in issues:
                cat = comment.get("category", "general")
                actions = REVISION_ACTIONS.get(cat, ["进行了相应修改"])
                action = random.choice(actions)
                templates = AUTHOR_RESPONSE_TEMPLATES.get(severity, AUTHOR_RESPONSE_TEMPLATES["minor"])
                template = random.choice(templates)
                resp_text = template.format(
                    action=action,
                    detail=f"见{cat}相关章节",
                    result="改进效果显著",
                    section=random.choice(["2", "3", "4", "5"]),
                )
                responses.append({
                    "original_comment": comment.get("comment", ""),
                    "category": cat,
                    "severity": severity,
                    "response": resp_text,
                    "addressed": True,
                    "resolution": CommentResolution.ADDRESSED.value,
                })
                modified_categories.add(cat)

        # 生成新章节内容
        cat_to_sec = {
            "novelty": "introduction", "methodology": "methodology",
            "data_analysis": "results", "significance": "discussion",
            "writing": "conclusion",
        }
        new_sections = {}
        for sec, content in prev_sections.items():
            modified_by = [c for c, s in cat_to_sec.items() if s == sec and c in modified_categories]
            if modified_by:
                new_sections[sec] = content + f"\n[v{version_num} 修改: 回应{','.join(modified_by)}意见]"
            else:
                new_sections[sec] = content

        return {
            "responses": responses,
            "total_issues": sum(len(issues) for _, issues in priority_groups),
            "addressed_count": len(responses),
            "new_sections": new_sections,
            "revision_notes": "\n".join(
                f"[{r['severity'].upper()}][{r['category']}] {r['original_comment']}\n  -> {r['response']}"
                for r in responses
            ),
        }


# ============================================================
# 会话管理器
# ============================================================

class ReviewSession:
    """单个审稿会话"""

    def __init__(self, title: str, abstract: str, max_rounds: int = 5):
        self.ms_id = str(uuid.uuid4())[:8]
        self.title = title
        self.abstract = abstract
        self.max_rounds = max_rounds
        self.current_round = 0
        self.current_version = 1
        self.status = "initialized"
        self.store = ReviewStore()
        self.eic = EICEngine()
        self.reviewer_engine = ReviewerEngine()
        self.author_engine = AuthorEngine()
        self.score_history = []
        self.review_history = []
        self.revision_history = []

        # 存储初始版本
        initial = {
            "version": 1, "title": title, "abstract": abstract,
            "content_sections": {
                "introduction": "引言内容...", "methodology": "方法论内容...",
                "results": "结果内容...", "discussion": "讨论内容...",
                "conclusion": "结论内容...",
            },
            "content_hash": hashlib.md5(title.encode()).hexdigest()[:12],
            "timestamp": datetime.now().isoformat(),
        }
        self.store.store_version(self.ms_id, initial)

    def to_status(self) -> dict:
        return {
            "manuscript_id": self.ms_id,
            "title": self.title,
            "current_round": self.current_round,
            "current_version": self.current_version,
            "max_rounds": self.max_rounds,
            "status": self.status,
            "score_history": self.score_history,
            "total_reviews": len(self.review_history),
            "total_revisions": len(self.revision_history),
        }


# 全局会话存储
_sessions: dict[str, ReviewSession] = {}


# ============================================================
# MCP Server
# ============================================================

mcp = FastMCP(
    "manuscript-review",
    instructions=(
        "分布式审稿协调系统 MCP 插件。"
        "提供学术稿件多轮审稿流程模拟，包含 EIC(主编)、Reviewer(审稿人)、Author(作者) 三个代理角色。"
        "使用流程: init_review → run_review → (查看结果) → author_revise → next_round → run_review → ... → export_report"
    ),
)


@mcp.tool()
def init_review(title: str, abstract: str, max_rounds: int = 5) -> str:
    """
    初始化审稿流程。创建新的审稿会话。

    Args:
        title: 论文标题
        abstract: 论文摘要
        max_rounds: 最大审稿轮数 (默认5)

    Returns:
        会话ID和初始状态
    """
    session = ReviewSession(title, abstract, max_rounds)
    _sessions[session.ms_id] = session

    return json.dumps({
        "message": f"审稿会话已创建",
        "session_id": session.ms_id,
        "title": title,
        "max_rounds": max_rounds,
        "reviewers": [p["name"] for p in REVIEWER_PROFILES],
        "next_step": "调用 run_review 开始第一轮审稿",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def run_review(session_id: str) -> str:
    """
    执行一轮审稿。所有审稿人对当前版本进行评审，EIC综合反馈。

    Args:
        session_id: 会话ID (从 init_review 获取)

    Returns:
        审稿结果：各审稿人评分、意见、EIC综合建议
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    session.current_round += 1
    is_re_review = session.current_round > 1

    # 各审稿人审稿
    reports = []
    for profile in REVIEWER_PROFILES:
        prev_review = None
        addressed_ratio = 0.5
        if is_re_review:
            prev_reviews = session.store.get_reviews(session.ms_id, session.current_round - 1)
            prev_review = next((r for r in prev_reviews if r.get("reviewer_id") == profile["id"]), None)
            if session.revision_history:
                total = session.revision_history[-1].get("total_issues", 1)
                addressed = session.revision_history[-1].get("addressed_count", 0)
                addressed_ratio = addressed / max(total, 1)

        report = session.reviewer_engine.review(
            profile, session.current_round, prev_review, addressed_ratio
        )
        session.store.store_review(session.ms_id, session.current_round, report)
        reports.append(report)

    # EIC综合
    synthesis = session.eic.synthesize(reports)
    session.score_history.append(synthesis["overall_avg"])
    session.review_history.append({
        "round": session.current_round,
        "reports": reports,
        "synthesis": synthesis,
    })
    session.status = "reviewed"

    # 判断是否结束
    is_complete, reason = _check_complete(session, synthesis)

    result = {
        "round": session.current_round,
        "eic_recommendation": synthesis["eic_recommendation"],
        "overall_score": synthesis["overall_avg"],
        "consensus_level": f"{synthesis['consensus_level']:.0%}",
        "issues": {
            "critical": synthesis["critical_count"],
            "major": synthesis["major_count"],
            "minor": synthesis["minor_count"],
        },
        "reviewer_reports": [
            {
                "name": r["reviewer_name"],
                "score": r["overall_score"],
                "decision": r["decision"],
                "confidence": f"{r['confidence']:.0%}",
                "summary": r["summary"],
                "comments": [
                    f"[{c['severity'].upper()}][{REVIEW_DIMENSIONS.get(c['category'], {}).get('name', c['category'])}] {c['comment']}"
                    for c in r["comments"]
                ],
            }
            for r in reports
        ],
    }

    if synthesis["disagreement_dims"]:
        result["disagreements"] = [
            f"{d['name']}: 分差 {d['max_diff']:.1f}"
            for d in synthesis["disagreement_dims"]
        ]

    if is_complete:
        session.status = "accepted" if synthesis["eic_recommendation"] in ["accept", "minor_revision"] else "rejected"
        result["process_complete"] = True
        result["termination_reason"] = reason
        result["next_step"] = "审稿完成！调用 export_report 导出报告"
    else:
        result["process_complete"] = False
        result["next_step"] = "调用 author_revise 进行修改，然后 next_round + run_review"

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def author_revise(session_id: str) -> str:
    """
    作者根据审稿意见修改稿件。自动生成逐条回复和修改版本。

    Args:
        session_id: 会话ID

    Returns:
        修改结果：逐条回复和新版本信息
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    if not session.review_history:
        return json.dumps({"error": "尚无审稿结果，请先调用 run_review"}, ensure_ascii=False)

    synthesis = session.review_history[-1]["synthesis"]
    prev_version = session.store.get_latest_version(session.ms_id)
    prev_sections = prev_version.get("content_sections", {}) if prev_version else {}

    session.current_version += 1
    result = session.author_engine.respond_and_revise(
        synthesis, prev_sections, session.current_version
    )

    # 存储新版本
    new_version = {
        "version": session.current_version,
        "title": session.title,
        "abstract": session.abstract,
        "content_sections": result["new_sections"],
        "revision_notes": result["revision_notes"],
        "content_hash": hashlib.md5(
            json.dumps(result["new_sections"], sort_keys=True).encode()
        ).hexdigest()[:12],
        "timestamp": datetime.now().isoformat(),
    }
    session.store.store_version(session.ms_id, new_version)
    session.revision_history.append(result)
    session.status = "revised"

    output = {
        "version": session.current_version,
        "total_issues": result["total_issues"],
        "addressed": result["addressed_count"],
        "responses": [
            {
                "severity": r["severity"],
                "category": REVIEW_DIMENSIONS.get(r["category"], {}).get("name", r["category"]),
                "original": r["original_comment"],
                "reply": r["response"],
            }
            for r in result["responses"]
        ],
        "next_step": "调用 next_round 推进到下一轮审稿",
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


@mcp.tool()
def next_round(session_id: str) -> str:
    """
    推进到下一轮审稿。在 author_revise 之后调用。

    Args:
        session_id: 会话ID

    Returns:
        下一轮状态
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    if session.status not in ("revised", "reviewed"):
        return json.dumps({"error": f"当前状态 '{session.status}'，不能推进"}, ensure_ascii=False)

    session.status = "ready_for_review"

    return json.dumps({
        "message": f"已准备第 {session.current_round + 1} 轮审稿",
        "current_round": session.current_round,
        "current_version": session.current_version,
        "score_history": session.score_history,
        "next_step": "调用 run_review 执行审稿",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_status(session_id: str) -> str:
    """
    查看审稿会话当前状态。

    Args:
        session_id: 会话ID

    Returns:
        当前状态摘要
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    return json.dumps(session.to_status(), ensure_ascii=False, indent=2)


@mcp.tool()
def list_sessions() -> str:
    """
    列出所有活跃的审稿会话。

    Returns:
        会话列表
    """
    if not _sessions:
        return json.dumps({"message": "暂无会话，调用 init_review 创建"}, ensure_ascii=False)

    return json.dumps({
        "sessions": [
            {"id": sid, "title": s.title, "status": s.status, "round": s.current_round}
            for sid, s in _sessions.items()
        ]
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def export_report(session_id: str, format: str = "text") -> str:
    """
    导出完整审稿报告。

    Args:
        session_id: 会话ID
        format: 输出格式 - "text" (可读文本) 或 "json" (结构化数据)

    Returns:
        完整审稿报告
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    if format == "json":
        export = {
            "manuscript": session.to_status(),
            "review_history": session.review_history,
            "revision_history": [
                {k: v for k, v in r.items() if k != "new_sections"}
                for r in session.revision_history
            ],
            "versions": session.store.get_all_versions(session.ms_id),
            "export_time": datetime.now().isoformat(),
        }
        return json.dumps(export, ensure_ascii=False, indent=2, default=str)

    # 文本格式
    lines = []
    lines.append("=" * 50)
    lines.append("    分布式审稿协调系统 - 完整审稿报告")
    lines.append("=" * 50)
    lines.append(f"稿件ID: {session.ms_id}")
    lines.append(f"标题: {session.title}")
    lines.append(f"摘要: {session.abstract}")
    lines.append(f"审稿轮数: {session.current_round}")
    lines.append(f"最终状态: {session.status}")
    lines.append(f"评分历史: {' → '.join(f'{s:.1f}' for s in session.score_history)}")
    lines.append("")

    for rh in session.review_history:
        r = rh["round"]
        syn = rh["synthesis"]
        lines.append(f"{'─' * 40}")
        lines.append(f"第 {r} 轮 | 建议: {syn['eic_recommendation']} | 综合分: {syn['overall_avg']:.1f} | 共识度: {syn['consensus_level']:.0%}")
        lines.append(f"问题: 关键{syn['critical_count']} 重要{syn['major_count']} 小{syn['minor_count']}")

        for report in rh["reports"]:
            lines.append(f"  [{report['reviewer_name']}] {report['overall_score']:.1f}分 → {report['decision']} (信心{report['confidence']:.0%})")
            for c in report["comments"]:
                dim_name = REVIEW_DIMENSIONS.get(c["category"], {}).get("name", c["category"])
                lines.append(f"    [{c['severity'].upper()}][{dim_name}] {c['comment']}")
        lines.append("")

    if session.revision_history:
        lines.append(f"{'─' * 40}")
        lines.append("修改历史")
        for i, rev in enumerate(session.revision_history, 1):
            lines.append(f"  第{i}次修改: 处理 {rev['total_issues']} 条意见, 解决 {rev['addressed_count']} 条")
        lines.append("")

    lines.append("=" * 50)
    lines.append(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)


@mcp.tool()
def auto_run(session_id: str) -> str:
    """
    自动运行完整审稿流程直到结束。

    Args:
        session_id: 会话ID

    Returns:
        完整流程结果摘要
    """
    session = _sessions.get(session_id)
    if not session:
        return json.dumps({"error": f"会话 {session_id} 不存在"}, ensure_ascii=False)

    results = []
    while True:
        # 审稿
        session.current_round += 1
        is_re = session.current_round > 1

        reports = []
        for profile in REVIEWER_PROFILES:
            prev = None
            ratio = 0.5
            if is_re:
                prev_revs = session.store.get_reviews(session.ms_id, session.current_round - 1)
                prev = next((r for r in prev_revs if r.get("reviewer_id") == profile["id"]), None)
                if session.revision_history:
                    t = session.revision_history[-1].get("total_issues", 1)
                    a = session.revision_history[-1].get("addressed_count", 0)
                    ratio = a / max(t, 1)
            report = session.reviewer_engine.review(profile, session.current_round, prev, ratio)
            session.store.store_review(session.ms_id, session.current_round, report)
            reports.append(report)

        synthesis = session.eic.synthesize(reports)
        session.score_history.append(synthesis["overall_avg"])
        session.review_history.append({"round": session.current_round, "reports": reports, "synthesis": synthesis})

        results.append(
            f"第{session.current_round}轮: {synthesis['overall_avg']:.1f}分 → {synthesis['eic_recommendation']} (共识{synthesis['consensus_level']:.0%})"
        )

        is_complete, reason = _check_complete(session, synthesis)
        if is_complete:
            session.status = "accepted" if synthesis["eic_recommendation"] in ["accept", "minor_revision"] else "rejected"
            break

        # 作者修改
        prev_ver = session.store.get_latest_version(session.ms_id)
        session.current_version += 1
        rev = session.author_engine.respond_and_revise(
            synthesis, prev_ver.get("content_sections", {}), session.current_version
        )
        new_ver = {
            "version": session.current_version, "title": session.title,
            "content_sections": rev["new_sections"],
            "content_hash": hashlib.md5(json.dumps(rev["new_sections"]).encode()).hexdigest()[:12],
            "timestamp": datetime.now().isoformat(),
        }
        session.store.store_version(session.ms_id, new_ver)
        session.revision_history.append(rev)

    return json.dumps({
        "summary": results,
        "final_status": session.status,
        "total_rounds": session.current_round,
        "final_score": session.score_history[-1],
        "score_trend": [round(s, 2) for s in session.score_history],
        "next_step": "调用 export_report 导出完整报告",
    }, ensure_ascii=False, indent=2)


def _check_complete(session: ReviewSession, synthesis: dict) -> tuple:
    """检查审稿是否结束"""
    rec = synthesis.get("eic_recommendation", "")

    if rec == ReviewDecision.ACCEPT.value:
        return True, "accepted"
    if rec == ReviewDecision.REJECT.value:
        return True, "rejected"
    if session.current_round >= session.max_rounds:
        return True, "max_rounds_reached"
    if (rec == ReviewDecision.MINOR_REVISION.value and
            session.current_round > 1 and synthesis.get("critical_count", 0) == 0):
        return True, "minor_revision_accepted"
    if len(session.score_history) >= 3:
        d1 = session.score_history[-1] - session.score_history[-2]
        d2 = session.score_history[-2] - session.score_history[-3]
        if d1 < 0.5 and d2 < 0.5:
            return True, "diminishing_returns"

    return False, ""


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    mcp.run()
