# 证据记录契约

## 三类记录分别保存

| 记录 | 内容 | 不能当作什么 |
|---|---|---|
| 来源/导航记录 | 入口、目录、摘要、位置、已读范围、版本与调用回执 | 原文事实或支持结论 |
| 原文证据 | 精确引文、同版定位、问题关系与范围 | Agent 总结或未经读到的内容 |
| 缺口/复核记录 | 选择下一步的原因、支持分类、剩余未知、停止原因 | 新的外部事实 |

直接工具提供持久账本时用它；否则在本次已授权工作目录使用 [账本模板](../assets/EVIDENCE-LEDGER.template.md) 保存。没有持久存储能力时明确本次是会话内记录、无法保证恢复，不能声称已经持久保存。不要把任务账本写回原始来源文件。

## 来源身份与定位

每份来源保存 source_id、来源组、path/URI、版本或获取时间、实际可得的内容哈希、格式和读取能力。多个章节属于同一来源；转载/副本也不能自动算独立证据。哈希不可得时为 null 并标明稳定性限制，不伪造版本。

定位采用实际工具支持的章节锚点、行范围、页码/段落、单元格或字符偏移，声明是哪一种。行号属于读取工具/提取文本的版本，不一定是原始排版的行号；OCR/解析器版本与原文件页码另记。默认行范围 1-based 且包含首尾，字符偏移 0-based、右端不包含；目标工具不同则记录其实际约定。

## 每条原文证据

必需键：

```text
evidence_id
source_id / source_group / source_version / source_sha256
locator / read_call_id
quote / quote_origin / context_note
aspect_ids
subject / action / object / conditions / negation
claim_type / limitations
```

quote 必须是已读原文的连续精确片段；不能改标点、合并不同位置或添加省略号冒充原文。一项判断需要不相邻文字时分别记录多个 ID。context_note 可由 Agent 解释，但不能替代 quote。

quote_origin 标记 original_text / extracted_text / ocr_text；从提取/OCR 文本取得的引文保持该文本原样，引用时声明转写来源与潜在误差。原始排版存在歧义时查对应页/表头，不把 OCR 错位强作事实。

主体/动作/对象和条件是解释字段，允许重新判断。原文和定位是历史记录，不能因为重新分类而改写。claim_type 可为 self_report / source_statement / measured_result / mechanism_description；它描述证据类型，不是统一可信度评分。

## 阅读与缺口链

read_log 记实际请求与返回范围、是否截断、读到的入口、调用状态和预算计量。每次 gap decision 固定原问题项、关联已保存证据 ID、missing、真实 target、entry_origin、预期变化与轮次。这样可还原“为什么从 A 读到 B”，而不是只留下若干支持片段。

问题项映射到真实原问题；缺口允许一次服务多个问题项。账本可以有相关但未采用的证据，最终不必全部引用。

## 最终复核

每条已保存证据在最终 review 中恰好出现一次。review 使用 used / limited / not_used，同时保存各问题项的 disposition 和 reason，避免一个片段对 A 直接支持、对 B 仅作背景时误用。

顶层 disposition：对至少一项直接支持为 used；仅上下文为 limited；均不采用为 not_used。aspects 的 direct_evidence_ids 只列该问题项 disposition 为 used 的 ID；背景进入 context_evidence_ids 或解释。结构校验不能代替语义判断。

每个用户问题项给出 supported / partly_supported / unresolved / contradicted 之一、可追溯说明、direct_evidence_ids 与 remaining_gap。contradicted 必须有实际相反原文和范围，不能靠“未读到”得到。来源自述只能支持自述层面的结论。

最终记录用 [回答模板](../assets/ANSWER.template.md)。一般对话交付可用简洁文字加来源链接；用户未要求时不必展示完整 JSON 或长账本，但应保存本次关键证据和阅读路径。
