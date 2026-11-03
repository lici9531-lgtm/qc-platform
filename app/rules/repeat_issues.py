"""Day07：重复 / excessive_repeat 独立小练（不动 qc_okbad / E0）。

规则（与任务书一致）：
- 同一 sample_id 第 2 次及以后：每行 1 条 type="duplicate_sample_id"
- 同一 sample_id 第 3 次及以后：每行再 1 条 type="excessive_repeat"
- 两条可以出现在同一行（issues 里两条）

请你实现 collect_repeat_issues，不要打开别的文件抄完整答案。
跑：python3 repeat_issues.py
"""

from __future__ import annotations


def collect_repeat_issues(sample_ids: list[str]) -> list[dict]:
    """按行扫描 sample_ids，返回 issues 列表。

    每条 issue 形如：
      {"row_index": int, "column": "sample_id", "type": "...", "value": sid}

    type 只能是 "duplicate_sample_id" 或 "excessive_repeat"。
    同一行若两类都触发，先 append duplicate，再 append excessive（方便对答案）。
    """
    # TODO: 你来写。提示：用 dict 记每个 id 已经出现几次。
    issues = []
    seen = {}
    for i, sid in enumerate(sample_ids):
        count = seen.get(sid,0) + 1
        seen[sid] = count
        if count >=2:
            issues.append({"sample_id": sid,"verdict": "confirmed","row_index": i, "column": "sample_id", "type": "duplicate_sample_id", "value": sid})
        if count >=3:
            issues.append({"sample_id": sid,"verdict": "confirmed","row_index": i, "column": "sample_id", "type": "excessive_repeat", "value": sid})
    return issues


def main() -> None:
    cases = [
        (["a", "a", "a", "a"], {"duplicate_sample_id": 3, "excessive_repeat": 2}),
        (["a", "b", "a", "a"], {"duplicate_sample_id": 2, "excessive_repeat": 1}),
        (["x", "y", "z"], {"duplicate_sample_id": 0, "excessive_repeat": 0}),
        (["s", "s"], {"duplicate_sample_id": 1, "excessive_repeat": 0}),
    ]
    for ids, expect in cases:
        issues = collect_repeat_issues(ids)
        counts = {"duplicate_sample_id": 0, "excessive_repeat": 0}
        for it in issues:
            counts[it["type"]] = counts.get(it["type"], 0) + 1
        ok = counts == expect
        print(ids, "=>", counts, "OK" if ok else f"FAIL expect {expect}")
        if not ok:
            print("  issues:", issues)


if __name__ == "__main__":
    main()
