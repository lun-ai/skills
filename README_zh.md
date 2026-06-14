# Skills: Research Paper Writing

> 重要归属说明
> 本仓库中的大部分写作经验与方法论来自彭思达老师公开的学习笔记：
> https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e
> 彭老师原始仓库：
> https://github.com/pengsida/learning_research
> 衷心感谢彭思达老师把这些宝贵经验公开分享出来。
> 我主要做了资料整理、结构化适配，以及 Skills 封装。

## 仓库介绍

当前仓库提供 **22 个技能**，按以下分组组织。每个技能都是独立的包：其目录下包含一个
`SKILL.md`（核心流程与使用规则），以及可选的 `references/`。

<!-- SKILLS-CATALOG:START -->
### 写作与润色

| 技能 | 说明 |
|---|---|
| [ai-paper-writing](./ai-paper-writing/) | 按章节重写 ML/CV/NLP 论文，提升结构、行文流畅度与审稿人视角的呈现，并检查论证与证据的对应关系。 |
| [nature-polishing](./nature-polishing/) | 对学术文本进行润色、重组或翻译，使其更符合 Nature 风格的英文表达，并修复 LaTeX 排版问题。 |
| [nature-writing](./nature-writing/) | 根据作者提供的结论、数据、图表与笔记，撰写或重构 Nature 风格的论文各章节（摘要、引言、方法等）。 |

### 审稿与反馈

| 技能 | 说明 |
|---|---|
| [ai-paper-reviewer](./ai-paper-reviewer/) | 模拟特定会议/期刊标准的同行评审：给出新颖性/清晰度/严谨性/影响力评分、优缺点分析及修改建议路线图。 |
| [nature-response](./nature-response/) | 为 Nature 系列期刊的修回稿撰写、审核或修订逐点回复审稿人的回复信。 |
| [nature-reviewer](./nature-reviewer/) | 基于 Nature 官方审稿标准，模拟 3 份 Nature 风格审稿意见并生成交叉综合报告。 |

### 文献检索、阅读与引用

| 技能 | 说明 |
|---|---|
| [nature-academic-search](./nature-academic-search/) | 跨多个数据库（PubMed、CrossRef、arXiv、Scopus 等）进行文献检索、引文核对与文献管理（BibTeX/RIS 转换）。 |
| [nature-citation](./nature-citation/) | 为论文段落自动查找并添加 Nature/CNS 系列期刊的严格引用，拆分文本并导出文献管理格式。 |
| [nature-reader](./nature-reader/) | 根据论文的 PDF、DOI 或文本，生成中英对照、保留图表位置的全文 Markdown 精读版本。 |
| [paper-summarizer](./paper-summarizer/) | 为论文生成带精确位置引用的结构化摘要，帮助读者快速把握核心内容并定位关键部分。 |

### 论文流程与数据

| 技能 | 说明 |
|---|---|
| [document-changes](./document-changes/) | 根据代码库与 Git 状态生成带时间戳的 Markdown 文档，记录最近的实现变更、架构与设计决策。 |
| [nature-data](./nature-data/) | 为 Nature 系列投稿准备或审核数据可用性声明、数据仓库方案、数据集引用及 FAIR 元数据清单。 |
| [nature-figure](./nature-figure/) | 为 Nature 等高水平期刊创建、审核或优化投稿级多面板图表（基于 Python matplotlib/seaborn 或 R ggplot2）。 |
| [paper-manuscript](./paper-manuscript/) | 通用 LaTeX 论文流程：重新生成表格与图片、核对数值结论、检查排版并验证交叉引用。 |
| [programmatic-manuscript-pipeline](./programmatic-manuscript-pipeline/) | 搭建可复现的 LaTeX 论文流程，使每个图表与数字都可追溯到经过整理的原始数据。 |

### 规划与构思

| 技能 | 说明 |
|---|---|
| [explain-concept](./explain-concept/) | 用寓言或简单故事的形式，将复杂的技术概念讲解得通俗易懂。 |
| [framework-design-alternatives](./framework-design-alternatives/) | 为软件框架、库、SDK 或协议的架构设计头脑风暴多种替代方案，并分析各方案的权衡。 |
| [research-ideation](./research-ideation/) | 通过结构化提问，将一个研究想法发展为具体的研究计划、论文大纲或实验设计。 |

### 学术汇报

| 技能 | 说明 |
|---|---|
| [nature-paper2ppt](./nature-paper2ppt/) | 将论文、预印本或阅读笔记转化为适用于组会、文献汇报或学术报告的中文 PPTX 幻灯片。 |

### 技能与仓库工具

| 技能 | 说明 |
|---|---|
| [skill-improver](./skill-improver/) | 分析某个技能在会话中出现的问题并对其指令进行迭代改进。仅在用户明确要求时使用。 |
| [update-skills-readme](./update-skills-readme/) | 根据本仓库当前的技能目录，重新生成 README.md 与 README_zh.md 中的分类技能目录表。 |

### 高性能计算与基础设施

| 技能 | 说明 |
|---|---|
| [slurm](./slurm/) | 通过 Slurm 编排 HPC 任务的通用策略：作业提交、资源申请、服务管理与生命周期操作。 |
<!-- SKILLS-CATALOG:END -->

## 安装方式

将本仓库直接克隆到工具的技能目录中，即可一次性安装所有技能。如果只需要部分技能，
可以先克隆到任意位置，再复制出需要的目录（每个技能都是自包含的）。

### 1) Codex

```bash
git clone https://github.com/lun-ai/skills.git "$CODEX_HOME/skills"
```

> 如果 `$CODEX_HOME/skills` 已存在，请先克隆到临时目录再合并：
> `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$CODEX_HOME/skills/"`。

使用示例：

```text
Use $ai-paper-writing to improve my paper's Introduction.
```

### 2) CC（Claude Code）

可选择全局安装或项目级安装。

全局安装：

```bash
git clone https://github.com/lun-ai/skills.git "$HOME/.claude/skills"
```

项目级安装：

```bash
mkdir -p .claude
git clone https://github.com/lun-ai/skills.git .claude/skills
```

> 如果目标目录已存在，请先克隆到临时目录再合并：
> `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$HOME/.claude/skills/"`。

使用时建议在提示词中显式指定，例如：`Please use the ai-paper-writing skill`。

### 3) Gemini

```bash
git clone https://github.com/lun-ai/skills.git "$HOME/.gemini/skills"
```

> 如果 `$HOME/.gemini/skills` 已存在，请先克隆到临时目录再合并：
> `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$HOME/.gemini/skills/"`。

随后在 Gemini 中直接给出具体任务（例如：重写 Abstract 并做 claim-evidence 检查）。

## 致谢

再次说明：仓库核心知识来源于彭思达老师公开笔记；我主要负责整理与 Skills 化适配。
彭老师原始仓库：https://github.com/pengsida/learning_research

## 许可证

本项目采用 MIT License，详见 [LICENSE](./LICENSE)。
