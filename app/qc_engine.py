from __future__ import annotations

# 规则代码已搬进项目：app/rules/（原件在 练习/unit02/，以项目这份为准）
from app.rules.qc_issues import load_and_check_issues


def run_qc(file_path: str) -> dict:
    """输入 CSV 路径，返回质检报告 dict。"""
    return load_and_check_issues(file_path)
