"""生成一份带问题的 CSV，用于把报告撑到 MB 级。

目的：505 字节的报告测不出「查库」和「查缓存」的差别，需要一份够大的数据
让 SQL 往返 + 传输的时间显著大于测量误差。

用法（在项目根目录执行）：
    python3 scripts/gen_big_csv.py
输出：
    data/labels_big.csv
"""

import csv
import random

# ---------------------------------------------------------------
# 1. 可调参数
#
#    ? 20 万行会产生多大的文件？先猜，跑完用 ls -lh 核对。
#    ? 如果想让报告更大，改哪一个数？
# ---------------------------------------------------------------

ROWS = 200_000
OUT = "data/labels_big.csv"


# ---------------------------------------------------------------
# 2. 造数据
#
#    ? 为什么用同一个 r 判断两次，而不是调两次 random.random()？
#    ? elif 后面那个阈值如果是 0.02，会得到多少条非法标签？
# ---------------------------------------------------------------

def main() -> None:
    random.seed(42)          # 固定随机种子：同样的参数每次生成同样的文件，便于复现

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "label","confidence", "text"])

        for i in range(ROWS):
            r = random.random()
            #   3% 概率 label 留空       -> 触发 missing_label
            if r < 0.03:
                label = ""
            #   再 2% 概率 label = "cat" -> 触发 illegal_label
            elif r < 0.05:
                label = "cat"
            #   其余随机 ok / bad
            else:
                label = "ok" if random.random() < 0.5 else "bad"
            #   再 2% 概率 label = "cat" -> 触发 illegal_label
            #   其余随机 ok / bad
            w.writerow([f"s{i}", label,0.9, f"这是一段用于测试的样本文本，编号 {i}"])


if __name__ == "__main__":
    main()
