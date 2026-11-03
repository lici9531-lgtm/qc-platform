"""U02 独立变体 H0：规则层（ok / bad）。

策略（自己实现，不要打开 rules.py 抄）：
- normalize：strip + lower
- 空串（strip 后）→ missing，不是 illegal
- illegal：非空且不在 allowed
- 默认 allowed：{"ok", "bad"}

实现后运行：python3 rules_okbad.py
预期三行：True / False / False
"""

from __future__ import annotations


def normalize(label: str) -> str:
    label = label.strip().lower()
    return label


def is_allowed(label: str, allowed: set[str]) -> bool:
    label = normalize(label)
    if label in allowed:
        return True
    return False


def check_missing(label: str) -> bool:
    label = normalize(label)
    if label == "":
        return True
    return False


def check_illegal(label: str, allowed: set[str]) -> bool:
    label = normalize(label)
    if label != "" and label not in allowed:
        return True
    return False

if __name__ == "__main__":
    allowed = {"ok", "bad"}
    # 实现后应打印 True / False / False

    print(is_allowed(" Ok ", allowed))
    print(is_allowed("  ", allowed))
    print(is_allowed("cat", allowed))
