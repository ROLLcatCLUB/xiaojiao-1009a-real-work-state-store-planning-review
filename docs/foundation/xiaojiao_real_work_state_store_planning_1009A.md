# 1009A Real Work State Store Planning

```text
stage=1009A_REAL_WORK_STATE_STORE_PLANNING
final_status=XIAOJIAO_REAL_WORK_STATE_STORE_PLANNING_PASS
next_stage=1009B_WORK_STATE_STORE_SANDBOX_CONTRACT
real_persistence_enabled=false
database_written=false
provider_called=false
model_called=false
cost_gate_incomplete=true
```

1009A plans the future persistent Work State Store for Xiaojiao. It converts the already verified preview and provider candidate chain into a store contract, but it does not write a database, sqlite file, JSONL business log, memory, Feishu, or any formal work object.

## Core Meaning

Work State is Xiaojiao's durable understanding of what the teacher is currently handling. It is not chat history and not frontend UI state.

The planned chain is:

```text
Work State Store
→ Composer
→ render_directive
→ preview renderer
→ provider candidate
→ normalized_candidate
→ work_object_patch
→ teacher_review_gate
```

## Cost Gate Caveat

1008M proved hardened JSON output, but cost estimation is not sealed:

```text
cost_gate_incomplete=true
estimated_cost_cny=null
```

Until cost gate passes, background generation, batch generation, multi-class auto generation, and default-route provider auto calls remain forbidden.
