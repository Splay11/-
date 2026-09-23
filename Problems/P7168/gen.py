# -*- coding: utf-8 -*-
"""P7168 造数：两个轴对齐矩形的并面积。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LO, HI = -(10**4), 10**4


def write_case(idx, rec):
    ax1, ay1, ax2, ay2, bx1, by1, bx2, by2 = rec
    assert LO <= ax1 <= ax2 <= HI
    assert LO <= ay1 <= ay2 <= HI
    assert LO <= bx1 <= bx2 <= HI
    assert LO <= by1 <= by2 <= HI
    ans = solve(*rec)
    inp = " ".join(str(x) for x in rec)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        ((-3, 0, 3, 4, 0, -1, 9, 2), "样例 1 部分重叠", "45", "重叠算两次"),
        ((-2, -2, 2, 2, -2, -2, 2, 2), "样例 2 完全重合", "16", "输出 32"),
        ((0, 0, 1, 1, 2, 2, 3, 3), "完全分开", "2", "硬减出负数重叠"),
        ((0, 0, 2, 2, 2, 0, 4, 2), "只在边上相接", "8", "把边当成重叠宽度"),
        ((0, 0, 0, 5, 1, 1, 2, 2), "第一个退化成线段面积 0", "1", "宽为 0 仍算面积"),
        ((-10, -10, 10, 10, -1, -1, 1, 1), "第二个完全在第一个内部", "400", "再减一次内部"),
        ((0, 0, 4, 1, 0, 0, 1, 4), "十字交叉", "7", "重叠 1x1 漏减"),
        ((5, 5, 5, 5, 5, 5, 5, 5), "两个点矩形", "0", "输出 1"),
        ((LO, LO, HI, HI, LO, LO, HI, HI), "压满坐标完全重合", "4e8", "int 乘法溢出"),
        ((LO, LO, HI, HI, 0, 0, HI, HI), "压满部分重叠", "并面积", "重叠为负没取 0"),
    ]
    answers, metas = [], []
    for i, (rec, _, _, _) in enumerate(plan, 1):
        metas.append(rec)
        answers.append(write_case(i, rec))
    assert answers[0] == 45 and answers[1] == 16
    assert answers[2] == 2 and answers[3] == 8
    assert answers[4] == 1 and answers[5] == 400
    assert answers[6] == 7 and answers[7] == 0
    assert answers[8] == 20000 * 20000

    for i, rec in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == " ".join(str(x) for x in rec)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7168 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。坐标在 $[-10^4,10^4]$。",
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
        print(i, a)


if __name__ == "__main__":
    main()
