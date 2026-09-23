# -*- coding: utf-8 -*-
"""P7170 造数：32 位整数反转，溢出输出 0。"""
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
    sign = -1 if x < 0 else 1
    s = str(abs(x))[::-1].lstrip("0") or "0"
    v = sign * int(s)
    if v < INT_MIN or v > INT_MAX:
        return 0
    return v


def write_case(idx, x):
    assert INT_MIN <= x <= INT_MAX
    ans = solve(x)
    assert ans == brute(x)
    (DATA / f"{idx}.in").write_bytes(str(x).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        (123, "样例 1", "321", "输出 3210"),
        (-123, "样例 2 负号保留", "-321", "输出 321"),
        (120, "样例 3 丢掉前导零", "21", "输出 021"),
        (0, "样例 4", "0", "输出空"),
        (INT_MIN, "下界，翻转必溢出", "0", "取相反数溢出"),
        (INT_MAX, "上界，翻转溢出", "0", "用 64 位硬存"),
        (1534236469, "正数翻转溢出", "0", "不检查溢出"),
        (-2147483412, "负数翻转仍在范围内", "对拍", "负号处理错"),
        (1000000003, "中间很多 0", "3000000001 溢出故 0", "丢掉 0 后位数判断错"),
        (1463847412, "翻转后贴上界", "2147483641", "误判溢出"),
    ]
    answers, xs = [], []
    for i, (x, _, _, _) in enumerate(plan, 1):
        xs.append(x)
        answers.append(write_case(i, x))
    assert answers[0] == 321 and answers[1] == -321 and answers[2] == 21
    assert answers[3] == 0 and answers[4] == 0 and answers[5] == 0
    assert answers[6] == 0

    for i, x in enumerate(xs, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == str(x)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7170 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。翻转后超出 $[-2^{31},2^{31}-1]$ 输出 $0$。",
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
