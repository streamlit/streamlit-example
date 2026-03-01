# 分布式审稿协调系统 - 使用指南

## 这是什么？

这是一个基于 Streamlit 的**网页应用**，模拟学术期刊的多轮审稿流程。包含三个智能代理：
- **EIC (主编)** - 统筹协调审稿，综合评分，做出最终决定
- **Reviewer (审稿人)** - 按维度评估稿件，提供修改意见
- **Author (作者)** - 接收反馈，逐条回复，修改稿件

---

## 从零开始运行（Mac 版）

### 第一步：打开终端

按 `Command + 空格`，输入 `Terminal`，按回车。

### 第二步：下载代码

在终端中逐行输入以下命令：

```bash
git clone https://github.com/chenhaozhou1996/streamlit-example.git
```

```bash
cd streamlit-example
```

```bash
git checkout claude/manuscript-review-coordinator-wz0mC
```

### 第三步：安装依赖

```bash
pip3 install streamlit pandas altair
```

> 如果提示 `pip3: command not found`，试试：
> ```bash
> python3 -m pip install streamlit pandas altair
> ```

### 第四步：运行应用

```bash
streamlit run manuscript_review_app.py
```

运行后终端会显示类似：
```
  Local URL: http://localhost:8501
```

浏览器会**自动打开**这个地址。如果没有自动打开，手动在浏览器中输入 `http://localhost:8501`。

### 第五步：停止运行

回到终端，按 `Ctrl + C` 即可停止。

---

## 使用说明

### 基本流程

1. **配置参数** - 左侧边栏可修改论文标题、摘要、最大审稿轮数
2. **提交稿件** - 点击「提交稿件并开始审稿流程」
3. **执行审稿** - 点击「执行第 N 轮审稿」，3位审稿人将各自评审
4. **查看结果** - 查看审稿报告、EIC综合意见、评分趋势、分歧分析
5. **作者修改** - 如果需要修改，点击「作者开始修改」
6. **循环** - 系统自动进入下一轮审稿，直到接受或拒稿
7. **下载报告** - 完成后可下载 TXT/JSON/CSV 格式的完整报告

### 自动模式

点击「自动运行完整流程」可以一键跑完所有轮次，自动完成审稿-修改-再审循环。

### 可查看的面板

| 标签页 | 内容 |
|--------|------|
| 审稿报告 | 各审稿人的详细评分和意见 |
| EIC综合意见 | 主编综合评定、共识度分析 |
| 意见追踪 | 每条意见的解决状态（已解决/部分/未解决） |
| 评分趋势 | 各维度评分的跨轮次变化曲线 |
| 分歧分析 | 审稿人评分热力图，可视化分歧 |
| 版本对比 | 稿件不同版本间的章节级差异 |
| 收敛趋势 | 综合评分是否在向接受阈值收敛 |

### 下载文档

审稿完成后，页面底部会出现三个下载按钮：
- **TXT** - 完整审稿报告（人工阅读）
- **JSON** - 结构化数据（程序分析）
- **CSV** - 评分汇总表（Excel打开）

---

## 常见问题

### Q: `git clone` 失败？
确保已安装 Git。Mac 上在终端输入 `git --version`，如果没有会提示安装。

### Q: `pip3 install` 失败？
试试：
```bash
python3 -m pip install --user streamlit pandas altair
```

### Q: 端口被占用？
```bash
streamlit run manuscript_review_app.py --server.port 8502
```

### Q: 浏览器没有自动打开？
手动访问终端显示的 `Local URL` 地址（通常是 `http://localhost:8501`）。
