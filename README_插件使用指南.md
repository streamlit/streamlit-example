# 审稿协调系统 - 插件使用指南

本项目提供 **3种使用方式**:

| 方式 | 文件 | 特点 |
|------|------|------|
| Streamlit 网页版 | `manuscript_review_app.py` | 可视化界面，鼠标操作 |
| MCP 插件 | `mcp_review_server.py` | 在 Claude Code 中直接调用 |
| Agent SDK 版 | `review_agent.py` | 真正的 AI 多代理审稿 |

---

## 方式一: MCP 插件 (在 Claude Code 中使用)

### 安装

```bash
pip install mcp
```

### 配置 Claude Code

在你的 Claude Code 设置中添加 MCP server。编辑 `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "manuscript-review": {
      "command": "python3",
      "args": ["/你的路径/streamlit-example/mcp_review_server.py"]
    }
  }
}
```

或者在项目的 `.mcp.json` 中配置:

```json
{
  "mcpServers": {
    "manuscript-review": {
      "command": "python3",
      "args": ["mcp_review_server.py"]
    }
  }
}
```

### 重启 Claude Code

配置完成后重启 Claude Code，你就可以直接说:

> "帮我审稿，标题是XXX，摘要是XXX"

Claude 会自动调用以下工具:

| 工具 | 说明 |
|------|------|
| `init_review` | 创建审稿会话 |
| `run_review` | 执行一轮审稿 |
| `author_revise` | 作者修改 |
| `next_round` | 推进下一轮 |
| `get_status` | 查看状态 |
| `export_report` | 导出报告 |
| `auto_run` | 自动跑完全流程 |
| `list_sessions` | 列出所有会话 |

### 使用示例

在 Claude Code 中输入:

```
初始化一个审稿，标题是"基于深度学习的图像分类研究"，摘要是"本文提出了一种新的CNN架构..."
```

然后:

```
执行审稿
```

```
让作者修改
```

```
导出审稿报告
```

---

## 方式二: Agent SDK 版 (真正的 AI 审稿)

这个版本使用 Claude API 真正生成智能审稿意见 (不是模板)。

### 安装

```bash
pip install anthropic
```

### 设置 API Key

```bash
export ANTHROPIC_API_KEY=sk-ant-你的key
```

### 命令行运行

```bash
# 基本用法
python3 review_agent.py \
  --title "基于多代理协调的分布式审稿系统研究" \
  --abstract "本文提出了一种基于多代理协调的分布式审稿系统..."

# 指定模型和轮数
python3 review_agent.py \
  --title "你的论文标题" \
  --abstract "你的摘要" \
  --max-rounds 3 \
  --model claude-haiku-4-5-20251001

# 导出报告
python3 review_agent.py \
  --title "论文标题" \
  --abstract "摘要" \
  --export report.txt

# 静默模式 (只输出JSON)
python3 review_agent.py \
  --title "论文标题" \
  --abstract "摘要" \
  --quiet
```

### 作为 Python 模块使用

```python
import asyncio
from review_agent import ReviewOrchestrator, AgentConfig

config = AgentConfig(model="claude-haiku-4-5-20251001")
orch = ReviewOrchestrator(config=config, max_rounds=3)

result = asyncio.run(orch.run(
    title="你的论文标题",
    abstract="你的摘要",
    verbose=True
))

# 导出报告
print(orch.export_report())
```

### 运行效果示例

```
==================================================
  分布式审稿协调代理系统
  稿件: 基于深度学习的图像分类研究
==================================================

────────────────────────────────
  第 1 轮审稿
────────────────────────────────
  审稿人A (方法论专家) 审稿中...
    → 评分: 6.2 | 建议: major_revision | 意见: 4条
  审稿人B (领域专家) 审稿中...
    → 评分: 7.5 | 建议: minor_revision | 意见: 2条
  审稿人C (写作审查) 审稿中...
    → 评分: 5.8 | 建议: major_revision | 意见: 5条

  EIC 综合分析中...
    → 建议: major_revision | 综合分: 6.5
    → 共识度: medium
    → 关键问题: 方法论需要更多验证, 写作需全面润色

  作者修改中...
    → 回复 11 条意见, 解决 9 条
    → 反驳 2 点

────────────────────────────────
  第 2 轮审稿
────────────────────────────────
  ...

==================================================
  审稿完成
  最终决定: accept
  评分趋势: 6.5 → 8.1
  总轮数: 2
==================================================
```

---

## 方式三: Streamlit 网页版

见 `README_审稿系统使用指南.md`。

---

## 费用说明

- **MCP 插件版**: 不消耗 API 额度 (使用模拟逻辑)
- **Agent SDK 版**: 每轮审稿约消耗 ~5000 tokens (使用 Haiku 模型，成本约 $0.005/轮)
- **Streamlit 版**: 不消耗 API 额度 (使用模拟逻辑)
