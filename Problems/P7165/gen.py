# -*- coding: utf-8 -*-
"""P7165 造数：24 点。四个 1..9，输出小写 true/false。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716520260915)


def write_case(idx, cards):
    assert len(cards) == 4
    for x in cards:
        assert 1 <= x <= 9
    ans = solve(cards)
    text = "true" if ans else "false"
    inp = " ".join(str(x) for x in cards)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    return text


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        ([4, 1, 8, 7], "样例 1，(8-4)*(7-1)", "true", "整数除法或漏括号"),
        ([1, 2, 1, 2], "样例 2 凑不出", "false", "输出 true"),
        ([1, 1, 1, 1], "全 1", "false", "输出 true"),
        ([3, 3, 8, 8], "经典 8/(3-8/3)", "true", "整数除法得到 false"),
        ([1, 1, 1, 8], "8*(1+1+1)", "true", "只用加法"),
        ([5, 5, 5, 5], "5 5 5 5", "对拍回溯", "只做加减"),
        ([9, 9, 9, 9], "全 9", "对拍", "爆搜漏排列"),
        ([2, 5, 5, 1], "中等组合", "对拍", "除以 0 没跳过"),
        ([9, 8, 7, 6], "接近上限的牌面", "对拍", "没枚举减法和除法方向"),
        ([1, 3, 4, 6], "另一组常用牌", "对拍", "只检查一种括号"),
    ]
    answers, metas = [], []
    for i, (cards, _, _, _) in enumerate(plan, 1):
        metas.append(cards)
        answers.append(write_case(i, cards))
    assert answers[0] == "true" and answers[1] == "false" and answers[2] == "false"
    assert answers[3] == "true" and answers[4] == "true"

    for i, cards in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == " ".join(str(x) for x in cards)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7165 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。四个 $1..9$，实数四则运算凑 $24$。",
            "约束始终是 $4$ 张牌，后两组用较大数字覆盖搜索分支。",
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
        print(i, a, metas[i - 1])


if __name__ == "__main__":
    main()
