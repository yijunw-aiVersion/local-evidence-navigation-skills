# Local Evidence Navigation

独立的标准 Agent Skill package，提供 **Local Evidence Navigation Baseline 0.1.0**。围绕用户问题，在文件章节与明确关联来源中逐步展开证据，保留原文、定位、阅读路径和答案缺口，形成可追溯的回答。

结构与 `cad-document-ingest`、`assembly-package-design` 一致：Skill 入口、按需参考、模板和仓库级验证/CI。安装内容仅含 Markdown。读取工具、知识库、持久控制器和硬预算由目标环境提供。

## 工作方式

```text
原问题 → 真实入口 → 小批原文 → 保存证据
       → 重要缺口 → 同文件/明确引用补读 → 复核全部证据 → 回答
```

用户给定文件时直接读相关结构和正文；需要找入口时做一次针对原问题的受限定位。后续阅读优先同文件上下文、定义、子章节、限制和脚注，必要时沿已发现引用跨来源。每次补读说明缺口和可能的答案变化，形成“为什么读这里、读到什么、还缺什么”的路径记录。

标题/摘要帮助选址，原文支持结论。行为自述、具体机制和完整流程按用户实际问题区分。早期证据持续保留；后续背景不能替代它。未读章节保持未核验，负面结论限定实际阅读范围。

## 安装与使用

将 `skills/local-evidence-navigation/` 整个目录复制到 Agent 的标准 skills 目录，或使用标准 [skills CLI](https://github.com/vercel-labs/skills) 从 [GitHub 仓库](https://github.com/yijunw-aiVersion/local-evidence-navigation-skills) 安装：

```bash
npx skills add yijunw-aiVersion/local-evidence-navigation-skills
npx skills add yijunw-aiVersion/local-evidence-navigation-skills --agent pi --skill local-evidence-navigation --copy --yes
```

在本地仓库根目录检查可安装内容或安装本地版本：

```bash
npx skills add . --list
npx skills add . --agent pi --skill local-evidence-navigation --copy --yes
```

默认安装到当前项目，用户级安装按需要加 `--global`。私有仓库需要访问权限和可用的 Git 凭据。无需 npm 发布。

Pi 调用：

```text
/skill:local-evidence-navigation 在这些文件中核查这个机制如何工作。从相关章节逐步展开，保留原文证据与缺口，并明确哪些阶段尚未说明。
```

Codex 显式调用：

```text
$local-evidence-navigation 根据这份资料回答我的问题；沿目录和明确引用局部补读，给出来源位置、结论范围和未解项。
```

可用于 Markdown/文本、PDF/Word、网页、项目说明或已有层级知识库。具体支持范围由真实读取工具确定。Local 指当前来源及其关联阅读邻域，不限定本机路径；OpenViking 是可选适配。

## 默认产出与预算

| 产出 | 内容 |
|---|---|
| 任务 profile | 用户问题、来源范围、工具能力与预算 |
| 证据账本 | 同版原文、定位、来源组、读取回执 |
| 缺口决策 | 关联证据、真实目标、预期变化与停止原因 |
| 回答/复核 | 问题项结论、直接/背景支持、范围和缺口 |

模板用于本次任务记录，不强制每次向用户输出完整 JSON。默认最多两轮补读、每轮五次导航调用、任务总导航十次（含初读/定位/恢复）；用户或运行环境预算优先。额度耗尽与证据充分分别报告。

## 内容

| 内容 | 文件 |
|---|---|
| Skill 入口与执行流程 | [SKILL.md](skills/local-evidence-navigation/SKILL.md) |
| 核心规则、阅读邻域与预算 | [navigation-policy.md](skills/local-evidence-navigation/references/navigation-policy.md) |
| 来源身份、精确引文、账本和复核 | [evidence-contract.md](skills/local-evidence-navigation/references/evidence-contract.md) |
| 动作/对象匹配、支持强度与冲突 | [evidence-reading.md](skills/local-evidence-navigation/references/evidence-reading.md) |
| 文件、文档与知识库适配 | [source-adapters.md](skills/local-evidence-navigation/references/source-adapters.md) |
| 可选记录/阶段控制器接入 | [harness-workflow.md](skills/local-evidence-navigation/references/harness-workflow.md) |
| 行为验收用例 | [conformance.md](skills/local-evidence-navigation/references/conformance.md) |
| 当前 Local Navigation 的来源与迁移 | [implementation-map.md](skills/local-evidence-navigation/references/implementation-map.md) |
| 任务 profile 模板 | [NAVIGATION-PROFILE.template.md](skills/local-evidence-navigation/assets/NAVIGATION-PROFILE.template.md) |
| 证据账本模板 | [EVIDENCE-LEDGER.template.md](skills/local-evidence-navigation/assets/EVIDENCE-LEDGER.template.md) |
| 缺口决策模板 | [GAP-DECISION.template.md](skills/local-evidence-navigation/assets/GAP-DECISION.template.md) |
| 回答与最终复核模板 | [ANSWER.template.md](skills/local-evidence-navigation/assets/ANSWER.template.md) |
| 单文件逐步导航示例 | [NAVIGATION-EXAMPLE.md](skills/local-evidence-navigation/assets/NAVIGATION-EXAMPLE.md) |

## 仓库结构

```text
skills/local-evidence-navigation/
  SKILL.md
  references/
  assets/
scripts/validate_skill.py       # 仓库维护，不随 Skill 安装
.github/workflows/validate.yml  # CI，不随 Skill 安装
```

## 验证与边界

```bash
python3 scripts/validate_skill.py
```

维护检查验证安装内容、frontmatter、内部引用、JSON 模板与示例引文定位。CI 使用固定版本 skills CLI，在临时 Pi 项目中检查发现与复制安装。模板和安装通过不证明导航选择总是正确；实际任务按验收用例核查原文语义、支持分类和阅读成本。

本次封装已通过上述内容检查、Skill Creator 格式验证与 skills CLI 1.7.0 的隔离项目发现/复制安装检查。该 CLI 版本实际安装到 `.pi/skills/local-evidence-navigation/`，其他版本以其真实结果为准。示例精确引文和行号已核对；跨格式、跨后端行为效果需实际任务验证。

本包不提供全库无遗漏、最优导航或独立事实认证。真实任务的证据充分性以所问问题、已读范围和原文为准。来源为当前 `openviking-local-navigation` 0.4.1 的通用机制；保留其证据规则并将工具与本机运行约束移到可选适配，未修改原 skill。
