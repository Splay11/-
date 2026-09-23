# -*- coding: utf-8 -*-
"""P7172 造数：二进制补码转十进制，n<=31。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def brute(bits):
    n = len(bits)
    s = "".join(str(b) for b in bits)
    if bits[0] == 0:
        return int(s, 2)
    # 补码负数：减去 2^n
    return int(s, 2) - (1 << n)


def write_case(idx, bits):
    n = len(bits)
    assert 1 <= n <= 31
    for b in bits:
        assert b in (0, 1)
    ans = solve(bits)
    assert ans == brute(bits)
    inp = f"{n}\n" + " ".join(str(b) for b in bits)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        ([0, 1, 0, 1], "样例 1 正数", "5", "把最高位当正权得到 5 碰巧对"),
        ([1, 1, 0, 1], "样例 2 负数", "-3", "当无符号 13"),
        ([1, 0, 0, 0, 0, 0, 0, 0], "样例 3，-128", "-128", "输出 128"),
        ([0], "n=1 的 0", "0", "输出 -1"),
        ([1], "n=1 的 -1", "-1", "输出 1"),
        ([0, 0, 0, 1], "正数 1", "1", "权值写反"),
        ([1, 1, 1, 1], "4 位全 1 是 -1", "-1", "输出 15"),
        ([0] + [1] * 30, "31 位最大正数 2^30-1", "1073741823", "符号位搞反"),
        ([1] + [0] * 30, "31 位最小负数 -2^30", "-1073741824", "当无符号"),
        ([1] * 31, "31 位全 1 是 -1", "-1", "输出 2^31-1"),
    ]
    answers, metas = [], []
    for i, (bits, _, _, _) in enumerate(plan, 1):
        metas.append(bits)
        answers.append(write_case(i, bits))
    assert answers[0] == 5 and answers[1] == -3 and answers[2] == -128
    assert answers[3] == 0 and answers[4] == -1 and answers[6] == -1
    assert answers[8] == -(1 << 30) and answers[9] == -1

    for i, bits in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(bits)}\n" + " ".join(str(b) for b in bits)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7172 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。约束 $1\le n\le 31$，$bits_i\in\{0,1\}$。",
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
        print(i, a, "n", len(metas[i - 1]))


if __name__ == "__main__":
    main()
