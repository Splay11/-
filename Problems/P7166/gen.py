# -*- coding: utf-8 -*-
"""P7166 造数：判断回文整数。输出小写 true/false。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def brute(x):
    s = str(x)
    return s == s[::-1]


def write_case(idx, x):
    assert INT_MIN <= x <= INT_MAX
    ans = solve(x)
    assert ans == brute(x)
    text = "true" if ans else "false"
    (DATA / f"{idx}.in").write_bytes(str(x).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    return text


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        (121, "样例 1", "true", "输出 false"),
        (-121, "样例 2 负数", "false", "去掉负号后当回文"),
        (10, "样例 3 末尾 0", "false", "把 01 当成 10"),
        (0, "0 是回文", "true", "输出 false"),
        (11, "两位相同", "true", "只处理奇数位"),
        (1001, "中间两个 0", "true", "遇到 0 直接判否"),
        (12321, "奇数位回文", "true", "丢掉中间位时出错"),
        (100, "以 0 结尾", "false", "整段翻转溢出或判 true"),
        (INT_MIN, "32 位下界", "false", "取负溢出"),
        (INT_MAX, "32 位上界 2147483647", "false", "整段翻转溢出"),
    ]
    answers = []
    xs = []
    for i, (x, _, _, _) in enumerate(plan, 1):
        xs.append(x)
        answers.append(write_case(i, x))
    assert answers[0] == "true" and answers[1] == "false" and answers[2] == "false"
    assert answers[3] == "true" and answers[8] == "false"

    for i, x in enumerate(xs, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == str(x)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7166 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。约束 $-2^{31}\le x\le 2^{31}-1$。",
            "",
            "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
            "|---|---|---|---|",
            *rows,
            "",
            "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
            "",
        ]),
        encoding="utf-8",
    )
    print("generated 10 cases")
    for i, a in enumerate(answers, 1):
        print(i, a, xs[i - 1])


if __name__ == "__main__":
    main()
