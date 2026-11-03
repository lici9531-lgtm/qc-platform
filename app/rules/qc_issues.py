"""Day07 加码：issues 小闭环（并行于 qc_okbad，不改 E0）。

流程：
1. 读 CSV；缺必需列 → error，issues 空
2. 逐行：空 label → missing_label；非空且不在 allowed → illegal_label
3. 全部 sample_id 交给 collect_repeat_issues，extend 进 issues
4. 按 type 计数填 summary；写出 JSON

验收 CSV：labels_okbad_dup.csv
  期望 summary 大致：
    total_rows=6, missing_label=1, illegal_label=1,
    duplicate_sample_id=2, excessive_repeat=1

运行：
  python3 qc_issues.py --csv labels_okbad_dup.csv --out report_issues_dup.json
"""

from __future__ import annotations

import argparse
import csv
import json
import hashlib
from pathlib import Path

from .repeat_issues import collect_repeat_issues
from .rules_okbad import check_illegal, check_missing

REQUIRED_COLS = ("sample_id", "label", "confidence")
DEFAULT_ALLOWED = {"ok", "bad"}
HERE = Path(__file__).resolve().parent
RULES_VERSION = "okbad-issues-v1"


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def empty_summary() -> dict:
    return {
        "total_rows": 0,
        "missing_label": 0,
        "illegal_label": 0,
        "duplicate_sample_id": 0,
        "excessive_repeat": 0,
    }


def summarize(issues: list[dict], total_rows: int) -> dict:
    """根据 issues 的 type 计数；total_rows 直接写入。"""
    s = empty_summary()
    s["total_rows"] = total_rows
    for issue in issues:
        kind = issue["type"]
        if kind in s:
            s[kind] += 1
    return s
    



def load_and_check_issues(path: str, allowed: set[str] | None = None) -> dict:
    """返回 {summary, issues, error}。"""
    if allowed is None:
        allowed = DEFAULT_ALLOWED

    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            if not header:
                return {"summary": empty_summary(), "issues": [], "error": "空文件或没有表头"}

            for col in REQUIRED_COLS:
                if col not in header:
                    return {
                        "summary": empty_summary(),
                        "issues": [],
                        "error": f"Missing required columns: {col}",
                    }

            issues: list[dict] = []
            sample_ids: list[str] = []
            rows = 0

            for row in reader:
                rows += 1
                sid = (row.get("sample_id") or "").strip() or f"row{rows}"
                label = row.get("label") or ""
                sample_ids.append(sid)
                if check_missing(label):
                    issues.append(
                        {
                            "sample_id": sid,
                            "verdict": "confirmed",
                            "row_index": rows - 1,
                            "column": "label",
                            "type": "missing_label",
                            "value": label,
                        }
                    )
                    continue
                if check_illegal(label, allowed):
                    issues.append(
                        {
                            "sample_id": sid,
                            "verdict": "confirmed",
                            "row_index": rows - 1,
                            "column": "label",
                            "type": "illegal_label",
                            "value": label,
                        }
                    )

        issues.extend(collect_repeat_issues(sample_ids))
        return {
            "rules_version": RULES_VERSION,
            "input_sha256": file_sha256(path),
            "summary": summarize(issues, rows),
            "issues": issues,
            "error": None,
        }
    except FileNotFoundError:
        return {
            
            "rules_version": RULES_VERSION,
            "input_sha256": None,
            "summary": empty_summary(),
            "issues": [],
            "error": f"Error loading {path}",
        }


def write_report(result: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="CSV QC with issues list")
    p.add_argument("--csv", required=True)
    p.add_argument("--out", default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = HERE / csv_path
    result = load_and_check_issues(str(csv_path), DEFAULT_ALLOWED)
    print(result)
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = HERE / out_path
        write_report(result, str(out_path))


if __name__ == "__main__":
    main()
