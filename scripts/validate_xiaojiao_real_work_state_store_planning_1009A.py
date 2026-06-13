import argparse, json, re, zipfile
from pathlib import Path

SLUG="xiaojiao_real_work_state_store_planning_1009A"
FINAL_STATUS="XIAOJIAO_REAL_WORK_STATE_STORE_PLANNING_PASS"
MARKER="ALL_1009A_REAL_WORK_STATE_STORE_PLANNING_CHECKS_OK"
SECRET_PATTERNS=[re.compile(r"sk-[A-Za-z0-9_\-]{12,}"), re.compile(r"gho_[A-Za-z0-9_]{12,}"), re.compile(r"(?i)(authorization|bearer)\s*[:=]\s*['\"]?[^'\"]{12,}")]
FORBIDDEN=[".env","token","secret","api_key","node_modules","__pycache__",".db",".sqlite","dist","build","coverage",".DS_Store"]
REQUIRED=[
  "docs/foundation/xiaojiao_real_work_state_store_planning_1009A.md",
  "docs/foundation/xiaojiao_real_work_state_store_planning_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/work_state_schema_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/work_object_schema_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/event_log_schema_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/work_object_patch_schema_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/teacher_review_gate_schema_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/store_boundary_policy_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/cost_gate_policy_1009A.json",
  "samples/xiaojiao_real_work_state_store_planning_1009A/preview_route_future_binding_plan_1009A.json",
  "docs/audit/xiaojiao_real_work_state_store_planning_1009A_result.json",
  "docs/audit/xiaojiao_real_work_state_store_planning_1009A_report.md",
  "docs/audit_packages/xiaojiao_real_work_state_store_planning_1009A_manifest.json",
  "docs/audit_packages/xiaojiao_real_work_state_store_planning_1009A.zip",
]

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def no_secret(p):
    text=Path(p).read_text(encoding="utf-8", errors="ignore")
    return not any(rx.search(text) for rx in SECRET_PATTERNS)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", default="."); args=ap.parse_args(); root=Path(args.root)
    for rel in REQUIRED:
        p=root/rel
        if not p.exists(): raise SystemExit(f"VALIDATION_FAILED missing {rel}")
        if p.suffix.lower() != ".zip" and not no_secret(p):
            raise SystemExit(f"VALIDATION_FAILED possible secret leakage {rel}")
    result=load(root/"docs/audit"/f"{SLUG}_result.json")
    manifest=load(root/"docs/audit_packages"/f"{SLUG}_manifest.json")
    foundation=load(root/"docs/foundation"/f"{SLUG}.json")
    required_flags={
      "real_persistence_enabled":False,
      "database_written":False,
      "memory_written":False,
      "Feishu_written":False,
      "formal_apply_performed":False,
      "default_route_changed":False,
      "provider_called":False,
      "model_called":False,
      "cost_gate_incomplete":True,
      "batch_generation_allowed":False,
      "background_generation_allowed":False,
      "teacher_review_required":True,
    }
    if result.get("final_status") != FINAL_STATUS or result.get("pass") is not True:
        raise SystemExit("VALIDATION_FAILED status")
    if result.get("marker") != MARKER:
        raise SystemExit("VALIDATION_FAILED marker")
    for key, expected in required_flags.items():
        if result.get(key) is not expected:
            raise SystemExit(f"VALIDATION_FAILED result {key}")
        if foundation.get(key) is not expected:
            raise SystemExit(f"VALIDATION_FAILED foundation {key}")
    for schema_name in ["work_state_schema_1009A","work_object_schema_1009A","event_log_schema_1009A","work_object_patch_schema_1009A","teacher_review_gate_schema_1009A"]:
        path=root/"samples"/SLUG/f"{schema_name}.json"
        if not load(path).get("schema_id"):
            raise SystemExit(f"VALIDATION_FAILED schema id {schema_name}")
    boundary=load(root/"samples"/SLUG/"store_boundary_policy_1009A.json")
    cost=load(root/"samples"/SLUG/"cost_gate_policy_1009A.json")
    if boundary.get("real_persistence_enabled") is not False:
        raise SystemExit("VALIDATION_FAILED boundary real persistence")
    if cost.get("cost_gate_incomplete") is not True or cost.get("batch_generation_allowed") is not False:
        raise SystemExit("VALIDATION_FAILED cost gate")
    with zipfile.ZipFile(root/"docs/audit_packages"/f"{SLUG}.zip") as zf:
        names=sorted(zf.namelist())
    if names != sorted(manifest.get("entries") or []):
        raise SystemExit("VALIDATION_FAILED manifest zip mismatch")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        raise SystemExit("VALIDATION_FAILED manifest diffs")
    for name in names:
        if "\\" in name or name.startswith("/") or ":" in name:
            raise SystemExit(f"VALIDATION_FAILED bad zip path {name}")
        lower=name.lower()
        if any(f in lower for f in FORBIDDEN):
            raise SystemExit(f"VALIDATION_FAILED forbidden zip path {name}")
    print(MARKER)

if __name__=="__main__":
    main()
