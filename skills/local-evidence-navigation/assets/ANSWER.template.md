# 回答与最终复核模板

普通对话优先给用户简洁回答、精确来源和范围；需要结构化提交/存档时用下列 JSON。控制器有不同 schema 时按其入口映射，不附加不接受的字段。

```json
{
  "schema_version": "local.evidence-answer.v1",
  "task_id": "REPLACE_TASK_ID",
  "answer": "REPLACE_SUPPORTED_ANSWER_WITH_CITATIONS_AND_LIMITS",
  "review": [],
  "aspects": [],
  "reading_scope": [],
  "unverified_entries": [],
  "remaining_gaps": [],
  "stop_reason": "REPLACE_ACTUAL_STOP_REASON",
  "navigation_calls_used": 0,
  "followup_rounds_used": 0
}
```

## 最终 review

每个已保存 evidence_id 恰好一次，结构为：

```text
{evidence_id, disposition, reason, per_aspect: [{aspect_id, disposition, reason}]}
```

disposition 为 used / limited / not_used。至少一项直接支持时顶层为 used；单个问题项仍只按自己的关系引用。复核依据原文，不照抄旧 Agent 分类。

## 问题项结果

每个原问题项一次，结构为：

```text
{aspect_id, status, conclusion, direct_evidence_ids, context_evidence_ids, remaining_gap}
```

status 为 supported / partly_supported / unresolved / contradicted。direct_evidence_ids 仅含对该问题项 used 的已保存 ID。背景可以解释但不能证明具体动作；source 自述不变成独立认证。

reading_scope 给来源版本与实际已读位置；unverified_entries 给已发现未读入口及原因。不需要枚举未知全库。stop_reason 使用实际停止原因；未核验不等于否定，额度耗尽不等于证据充分。

## 面向用户的文字形式

```text
{直接回答，关键判断附来源位置。}

{已证实的机制/阶段与边界；用途、范围或自述属性需要时明确。}

{尚缺什么，已读范围和停止原因。若有矛盾，保留双方来源。}
```

证据链展示为简短的来源位置与阅读关系，不逐句输出内部思考，也不重复整份账本。
