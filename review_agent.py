#!/usr/bin/env python3
"""
分布式审稿协调代理 - Claude Agent SDK 版本
Manuscript Review Multi-Agent System

真正的多代理审稿系统:
- EIC Agent: 调用 Claude 做综合决策
- Reviewer Agents: 调用 Claude 做智能审稿
- Author Agent: 调用 Claude 做针对性回复和修改
- Coordinator: 编排多轮审稿循环

安装:
    pip install anthropic

使用:
    export ANTHROPIC_API_KEY=sk-ant-...
    python review_agent.py --title "论文标题" --abstract "论文摘要"

或作为模块导入:
    from review_agent import ReviewOrchestrator
    orch = ReviewOrchestrator()
    result = await orch.run("论文标题", "论文摘要")
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from dataclasses import dataclass, field

try:
    import anthropic
except ImportError:
    print("请安装 anthropic SDK: pip install anthropic")
    sys.exit(1)


# ============================================================
# 代理定义
# ============================================================

EIC_SYSTEM_PROMPT = """你是一位学术期刊主编(Editor-in-Chief)。你的职责是:

1. 综合多位审稿人的意见，做出公正的评审决策
2. 识别审稿人之间的分歧，进行协调
3. 给作者提供清晰、有建设性的修改指导
4. 决定稿件是接受(accept)、小修(minor_revision)、大修(major_revision)还是拒稿(reject)

你应该:
- 关注审稿人的共识和分歧
- 对关键性问题(critical)给予最高优先级
- 如果审稿人意见冲突，给出你的专业判断
- 输出结构化的JSON格式决策

请用中文回复。"""

REVIEWER_SYSTEM_PROMPT = """你是一位学术论文审稿人。你的专长领域是: {expertise}。
你的审稿风格: {personality}，严格度: {strictness}/10。

审稿要求:
1. 从以下5个维度评分(1-10分):
   - novelty (创新性, 权重25%)
   - methodology (方法论, 权重25%)
   - writing (写作质量, 权重15%)
   - significance (研究意义, 权重20%)
   - data_analysis (数据分析, 权重15%)

2. 对每个低于7分的维度，给出具体的审稿意见，标注严重程度:
   - critical: 必须解决的根本性问题
   - major: 需要认真处理的重要问题
   - minor: 建议改进的小问题

3. 给出总体建议: accept / minor_revision / major_revision / reject

4. 如果是再审(re-review)，需要评估作者是否充分回应了之前的意见

输出格式为JSON。请用中文给出评审意见。"""

AUTHOR_SYSTEM_PROMPT = """你是一位学术论文作者。你需要:

1. 逐条回复审稿人的意见
2. 对合理的批评，说明你的修改方案
3. 对不合理的批评，礼貌地给出反驳和解释
4. 如果不同审稿人意见冲突，说明你的处理策略
5. 生成修改说明

回复策略:
- critical 问题: 必须详细回应，说明具体修改内容
- major 问题: 认真处理，给出修改或解释
- minor 问题: 简短确认
- 冲突意见: 客观分析，说明取舍理由

输出格式为JSON。请用中文回复。"""


@dataclass
class AgentConfig:
    """代理配置"""
    model: str = "claude-haiku-4-5-20251001"  # 默认用 Haiku 节省成本
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class ReviewerProfile:
    id: str
    name: str
    expertise: list
    strictness: float
    personality: str


REVIEWERS = [
    ReviewerProfile("rev_A", "审稿人A", ["methodology", "data_analysis"], 0.7, "严谨、注重方法论"),
    ReviewerProfile("rev_B", "审稿人B", ["novelty", "significance"], 0.4, "开放、鼓励创新"),
    ReviewerProfile("rev_C", "审稿人C", ["writing", "methodology"], 0.6, "细致、关注表达"),
]


# ============================================================
# Agent 基类
# ============================================================

class BaseAgent:
    """代理基类"""

    def __init__(self, name: str, system_prompt: str, config: AgentConfig = None):
        self.name = name
        self.system_prompt = system_prompt
        self.config = config or AgentConfig()
        self.client = anthropic.Anthropic()
        self.history = []

    def call(self, user_message: str) -> str:
        """调用 Claude API"""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        text = response.content[0].text
        self.history.append({"input": user_message[:200], "output": text[:200]})
        return text

    def parse_json(self, text: str) -> dict:
        """从回复中提取JSON"""
        # 尝试找到 JSON 块
        if "```json" in text:
            start = text.index("```json") + 7
            end = text.index("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.index("```") + 3
            end = text.index("```", start)
            text = text[start:end].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 尝试找到第一个 { 和最后一个 }
            first = text.find("{")
            last = text.rfind("}")
            if first >= 0 and last > first:
                try:
                    return json.loads(text[first:last + 1])
                except json.JSONDecodeError:
                    pass
            return {"raw_response": text, "parse_error": True}


# ============================================================
# 具体代理
# ============================================================

class EICAgent(BaseAgent):
    """主编代理"""

    def __init__(self, config: AgentConfig = None):
        super().__init__("EIC", EIC_SYSTEM_PROMPT, config)

    def synthesize(self, manuscript_info: str, reviews: list, round_num: int,
                   prev_decisions: list = None) -> dict:
        prompt = f"""请综合以下审稿意见，做出编辑决策。

## 稿件信息
{manuscript_info}

## 当前轮次: 第{round_num}轮

## 审稿报告
{json.dumps(reviews, ensure_ascii=False, indent=2)}

{"## 前轮决策历史" + chr(10) + json.dumps(prev_decisions, ensure_ascii=False, indent=2) if prev_decisions else ""}

请输出JSON格式:
{{
    "recommendation": "accept/minor_revision/major_revision/reject",
    "overall_score": 0-10的综合评分,
    "consensus_level": "high/medium/low",
    "key_issues": ["关键问题列表"],
    "guidance_to_author": "给作者的修改指导",
    "disagreement_analysis": "审稿人分歧分析(如有)",
    "reasoning": "决策理由"
}}"""
        response = self.call(prompt)
        return self.parse_json(response)


class ReviewerAgent(BaseAgent):
    """审稿人代理"""

    def __init__(self, profile: ReviewerProfile, config: AgentConfig = None):
        system = REVIEWER_SYSTEM_PROMPT.format(
            expertise=", ".join(profile.expertise),
            personality=profile.personality,
            strictness=int(profile.strictness * 10),
        )
        super().__init__(profile.name, system, config)
        self.profile = profile

    def review(self, manuscript_info: str, round_num: int,
               prev_comments: list = None, author_response: str = None) -> dict:
        prompt = f"""请审阅以下稿件。

## 稿件信息
{manuscript_info}

## 审稿轮次: 第{round_num}轮
"""
        if prev_comments and author_response:
            prompt += f"""
## 你上一轮的审稿意见
{json.dumps(prev_comments, ensure_ascii=False, indent=2)}

## 作者对你意见的回复
{author_response}

请评估作者是否充分回应了你的意见，并给出新一轮评审。
"""

        prompt += """
请输出JSON格式:
{
    "scores": {"novelty": 0-10, "methodology": 0-10, "writing": 0-10, "significance": 0-10, "data_analysis": 0-10},
    "overall_score": 加权总分,
    "decision": "accept/minor_revision/major_revision/reject",
    "comments": [
        {"category": "维度名", "severity": "critical/major/minor", "comment": "具体意见"}
    ],
    "summary": "审稿总结",
    "confidence": 0-1的审稿信心
}"""
        response = self.call(prompt)
        result = self.parse_json(response)
        result["reviewer_id"] = self.profile.id
        result["reviewer_name"] = self.profile.name
        result["round"] = round_num
        return result


class AuthorAgent(BaseAgent):
    """作者代理"""

    def __init__(self, config: AgentConfig = None):
        super().__init__("Author", AUTHOR_SYSTEM_PROMPT, config)

    def respond(self, manuscript_info: str, eic_guidance: str,
                reviews: list, round_num: int) -> dict:
        prompt = f"""请根据审稿意见修改稿件。

## 你的稿件
{manuscript_info}

## EIC指导意见
{eic_guidance}

## 审稿人意见 (第{round_num}轮)
{json.dumps(reviews, ensure_ascii=False, indent=2)}

请输出JSON格式:
{{
    "responses": [
        {{
            "reviewer": "审稿人名",
            "original_comment": "原始意见",
            "severity": "critical/major/minor",
            "response": "你的回复",
            "action_taken": "具体修改内容",
            "addressed": true/false
        }}
    ],
    "revision_summary": "修改概述",
    "rebuttal_points": ["如有反驳，列出理由"],
    "sections_modified": ["修改的章节列表"]
}}"""
        response = self.call(prompt)
        return self.parse_json(response)


# ============================================================
# 编排器
# ============================================================

class ReviewOrchestrator:
    """
    审稿流程编排器 - 协调 EIC、Reviewer、Author 三类代理

    流程:
    提交 → [Reviewer审稿 × N] → EIC综合 → Author修改
    → [Reviewer再审 × N] → EIC再综合 → ... → 最终决定
    """

    def __init__(self, config: AgentConfig = None, max_rounds: int = 3):
        self.config = config or AgentConfig()
        self.max_rounds = max_rounds
        self.eic = EICAgent(self.config)
        self.reviewers = [ReviewerAgent(p, self.config) for p in REVIEWERS]
        self.author = AuthorAgent(self.config)
        self.history = []
        self.score_history = []

    async def run(self, title: str, abstract: str,
                  content: str = None, verbose: bool = True) -> dict:
        """运行完整审稿流程"""
        manuscript_info = f"标题: {title}\n摘要: {abstract}"
        if content:
            manuscript_info += f"\n内容: {content}"

        if verbose:
            print(f"\n{'=' * 50}")
            print(f"  分布式审稿协调代理系统")
            print(f"  稿件: {title}")
            print(f"{'=' * 50}\n")

        prev_reviews_by_reviewer = {}
        prev_author_response = None
        eic_decisions = []

        for round_num in range(1, self.max_rounds + 1):
            if verbose:
                print(f"\n{'─' * 40}")
                print(f"  第 {round_num} 轮审稿")
                print(f"{'─' * 40}")

            # Step 1: 各审稿人审稿
            reviews = []
            for reviewer in self.reviewers:
                if verbose:
                    print(f"  {reviewer.profile.name} 审稿中...")

                prev = prev_reviews_by_reviewer.get(reviewer.profile.id)
                result = reviewer.review(
                    manuscript_info, round_num,
                    prev_comments=prev,
                    author_response=prev_author_response,
                )
                reviews.append(result)

                if verbose:
                    score = result.get("overall_score", "?")
                    dec = result.get("decision", "?")
                    n_comments = len(result.get("comments", []))
                    print(f"    → 评分: {score} | 建议: {dec} | 意见: {n_comments}条")

            # Step 2: EIC 综合
            if verbose:
                print(f"\n  EIC 综合分析中...")

            eic_result = self.eic.synthesize(
                manuscript_info, reviews, round_num, eic_decisions
            )
            eic_decisions.append(eic_result)

            rec = eic_result.get("recommendation", "pending")
            overall = eic_result.get("overall_score", 0)
            self.score_history.append(overall)

            if verbose:
                print(f"    → 建议: {rec} | 综合分: {overall}")
                print(f"    → 共识度: {eic_result.get('consensus_level', '?')}")
                if eic_result.get("key_issues"):
                    print(f"    → 关键问题: {', '.join(eic_result['key_issues'][:3])}")

            self.history.append({
                "round": round_num,
                "reviews": reviews,
                "eic_decision": eic_result,
            })

            # 检查是否结束
            if rec in ("accept", "reject"):
                if verbose:
                    emoji = "🎉" if rec == "accept" else "❌"
                    print(f"\n  {emoji} 最终决定: {rec}")
                break

            if round_num >= self.max_rounds:
                if verbose:
                    print(f"\n  达到最大轮数 ({self.max_rounds})，流程结束")
                break

            # 收敛检测
            if len(self.score_history) >= 3:
                d1 = self.score_history[-1] - self.score_history[-2]
                d2 = self.score_history[-2] - self.score_history[-3]
                if d1 < 0.5 and d2 < 0.5:
                    if verbose:
                        print(f"\n  评分收敛 (改善不足0.5分)，流程结束")
                    break

            # Step 3: 作者修改
            if verbose:
                print(f"\n  作者修改中...")

            guidance = eic_result.get("guidance_to_author", "请根据审稿意见修改")
            author_result = self.author.respond(
                manuscript_info, guidance, reviews, round_num
            )
            prev_author_response = json.dumps(author_result, ensure_ascii=False)

            # 保存各审稿人的意见供下轮参考
            for review in reviews:
                rid = review.get("reviewer_id", "")
                prev_reviews_by_reviewer[rid] = review.get("comments", [])

            if verbose:
                n_resp = len(author_result.get("responses", []))
                n_addr = sum(1 for r in author_result.get("responses", []) if r.get("addressed"))
                print(f"    → 回复 {n_resp} 条意见, 解决 {n_addr} 条")
                if author_result.get("rebuttal_points"):
                    print(f"    → 反驳 {len(author_result['rebuttal_points'])} 点")

            self.history[-1]["author_response"] = author_result

        # 最终报告
        final = {
            "title": title,
            "total_rounds": len(self.history),
            "final_decision": eic_decisions[-1].get("recommendation", "pending") if eic_decisions else "pending",
            "score_history": self.score_history,
            "history": self.history,
            "eic_reasoning": eic_decisions[-1].get("reasoning", "") if eic_decisions else "",
        }

        if verbose:
            print(f"\n{'=' * 50}")
            print(f"  审稿完成")
            print(f"  最终决定: {final['final_decision']}")
            print(f"  评分趋势: {' → '.join(str(s) for s in self.score_history)}")
            print(f"  总轮数: {final['total_rounds']}")
            print(f"{'=' * 50}")

        return final

    def export_report(self) -> str:
        """导出文本报告"""
        lines = ["=" * 50, "  分布式审稿协调代理 - 审稿报告", "=" * 50, ""]

        for entry in self.history:
            r = entry["round"]
            lines.append(f"── 第 {r} 轮 ──")
            eic = entry.get("eic_decision", {})
            lines.append(f"EIC建议: {eic.get('recommendation', '?')} | 综合分: {eic.get('overall_score', '?')}")
            lines.append(f"决策理由: {eic.get('reasoning', '无')}")
            lines.append("")

            for review in entry.get("reviews", []):
                name = review.get("reviewer_name", "?")
                score = review.get("overall_score", "?")
                dec = review.get("decision", "?")
                lines.append(f"  [{name}] {score}分 → {dec}")
                for c in review.get("comments", []):
                    lines.append(f"    [{c.get('severity', '?').upper()}] {c.get('comment', '')}")
                lines.append("")

            author = entry.get("author_response", {})
            if author:
                lines.append(f"  作者回复 {len(author.get('responses', []))} 条")
                lines.append(f"  修改概述: {author.get('revision_summary', '无')}")
                lines.append("")

        lines.append(f"评分趋势: {' → '.join(str(s) for s in self.score_history)}")
        lines.append(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="分布式审稿协调代理系统")
    parser.add_argument("--title", required=True, help="论文标题")
    parser.add_argument("--abstract", required=True, help="论文摘要")
    parser.add_argument("--content", default=None, help="论文内容(可选)")
    parser.add_argument("--max-rounds", type=int, default=3, help="最大审稿轮数")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001", help="Claude模型")
    parser.add_argument("--export", default=None, help="导出报告到文件")
    parser.add_argument("--quiet", action="store_true", help="静默模式")

    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("错误: 请设置 ANTHROPIC_API_KEY 环境变量")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    config = AgentConfig(model=args.model)
    orchestrator = ReviewOrchestrator(config=config, max_rounds=args.max_rounds)

    result = asyncio.run(
        orchestrator.run(args.title, args.abstract, args.content, verbose=not args.quiet)
    )

    if args.export:
        report = orchestrator.export_report()
        with open(args.export, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已导出到: {args.export}")

    # 输出JSON结果
    if args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
