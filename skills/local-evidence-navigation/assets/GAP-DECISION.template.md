# 缺口与下一步决策模板

选择下一次阅读前填写；并非要求公开模型内部推理。简短表达证据缺口与导航依据即可。`REPLACE_*` 需替换为真实值。

```json
{
  "decision_id": "REPLACE_DECISION_ID",
  "task_id": "REPLACE_TASK_ID",
  "action": "next_read",
  "round_number": 1,
  "aspect_ids": [],
  "evidence_ids": [],
  "missing": "REPLACE_ANSWER_RELEVANT_GAP",
  "target": {
    "source_id": "REPLACE_SOURCE_ID",
    "uri_or_path": "REPLACE_REAL_ENTRY",
    "locator": "REPLACE_REAL_SECTION_OR_RANGE"
  },
  "entry_origin": {
    "call_id": "REPLACE_CONFIRMED_CALL_ID",
    "locator": "REPLACE_WHERE_ENTRY_WAS_FOUND"
  },
  "why_this_entry": "REPLACE_BRIEF_NAVIGATION_REASON",
  "expected_answer_change": "REPLACE_SPECIFICITY_SCOPE_OR_CONCLUSION_CHANGE",
  "already_read": false,
  "budget_check": {
    "navigation_calls_remaining": null,
    "round_calls_remaining": null,
    "reading_capacity_ok": null,
    "recording_and_synthesis_reserved": null
  },
  "stop_reason": null
}
```

action 为 next_read / synthesize / stop。next_read 必须有真实 target、来源入口和重要缺口；预算无法确认安全时不继续。正文已读但上下文未读的目标，明确记录新范围，不假装整个章节都未读。

synthesize/stop 时 target 与 entry_origin 可为 null，填写真实停止原因和仍有的缺口。synthesize 表示进行综合，不等于所有信息齐全。账本已经保存的证据即使下一步被拒绝，也不能被误删。
