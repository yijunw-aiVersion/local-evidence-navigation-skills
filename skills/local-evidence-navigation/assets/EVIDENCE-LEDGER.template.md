# 证据账本模板

以下是普通环境可用的 JSON 结构，不是自带数据库或 controller API。`REPLACE_*` 由本次真实值替换；数组初始为空，读到后逐项记录。

```json
{
  "schema_version": "local.evidence-ledger.v1",
  "task_id": "REPLACE_TASK_ID",
  "question": "REPLACE_ORIGINAL_QUESTION",
  "aspects": [],
  "sources": [],
  "read_log": [],
  "evidence": [],
  "decisions": [],
  "budget": {
    "max_navigation_calls": 10,
    "max_followup_rounds": 2,
    "max_calls_per_round": 5,
    "used_navigation_calls": 0,
    "round_call_counts": {},
    "reading_measurement_unit": null,
    "reading_used": null,
    "synthesis_reserve": null,
    "limits_enforced_by": "REPLACE_RUNTIME_OR_SOFT_COUNTER"
  },
  "persistence": "REPLACE_FILE_OR_CONTROLLER_OR_SESSION_ONLY",
  "status": "exploring"
}
```

## 数组字段

- aspects：`{aspect_id, question_text, requirement}`，保留用户真实问题项，不新增搜索任务。
- sources：`{source_id, source_group, uri_or_path, format, version, sha256, retrieved_at, extraction_method, stability_note}`。未知 version/hash 为 null，写限制。
- read_log：`{call_id, phase, round_number, source_id, target, requested_locator, returned_locator, result_status, truncated, returned_size, measurement_unit, discovered_entries}`。初读 round_number=0；定位调用也记录，即使没有正文。
- evidence：按下方单条模板，使用真实读到的精确连续片段。
- decisions：使用 [缺口决策模板](GAP-DECISION.template.md)。

## 单条原文证据

```json
{
  "evidence_id": "REPLACE_EVIDENCE_ID",
  "source_id": "REPLACE_SOURCE_ID",
  "source_group": "REPLACE_SOURCE_GROUP",
  "source_version": null,
  "source_sha256": null,
  "locator": {
    "kind": "REPLACE_LINE_PAGE_SECTION_OR_OFFSET",
    "value": "REPLACE_ACTUAL_LOCATION",
    "convention": "REPLACE_LOCATION_CONVENTION"
  },
  "read_call_id": "REPLACE_CONFIRMED_READ_CALL_ID",
  "quote": "REPLACE_EXACT_CONTIGUOUS_READ_TEXT",
  "quote_origin": "original_text",
  "context_note": null,
  "aspect_ids": [],
  "subject": null,
  "action": null,
  "object": null,
  "conditions": [],
  "negation": null,
  "claim_type": "source_statement",
  "limitations": []
}
```

字段来源与定位规则见 [证据契约](../references/evidence-contract.md)。关键原文/定位先保存，再选择下一步。来源原文改变时新增版本记录；旧引文不能自动指向新版本。
