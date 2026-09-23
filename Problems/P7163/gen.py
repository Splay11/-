# -*- coding: utf-8 -*-
"""P7163 造数：按字符频率降序重排。标程输出确定；OJ 用 checker.cc。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716320260915)
L_MAX = 5 * 10**5
ALPH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def valid(s, t):
    if len(s) != len(t):
        return False
    from collections import Counter
    if Counter(s) != Counter(t):
        return False
    prev, seen = len(t) + 1, set()
    i, n = 0, len(t)
    while i < n:
        ch = t[i]
        if ch in seen:
            return False
        seen.add(ch)
        j = i
        while j < n and t[j] == ch:
            j += 1
        f = j - i
        if f > prev:
            return False
        prev = f
        i = j
    return True


def write_case(idx, s):
    assert 1 <= len(s) <= L_MAX
    for ch in s:
        assert ch.isalnum()
    ans = solve(s)
    assert valid(s, ans)
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    long_tie = ("a" * 2000 + "b" * 2000 + "C" * 100)
    huge = []
    # 62 种字符，次数互不相同，答案唯一
    for i, ch in enumerate(ALPH):
        huge.append(ch * (i + 1))
    rest = L_MAX - sum(range(1, 63))
    huge.append("z" * rest)
    huge_s = "".join(huge)
    assert len(huge_s) == L_MAX
    rnd = "".join(RNG.choice(ALPH) for _ in range(80))

    plan = [
        ("tree", "样例 1，$e$ 两次", "eert（也允许 eetr）", "交错输出 eret"),
        ("cccaaa", "样例 2，次数相同", "aaaccc 或 cccaaa", "cacaca 交错"),
        ("Aabb", "样例 3，大小写不同", "bbAa", "把 A、a 合并"),
        ("a", "长度 1", "a", "输出空"),
        ("zzzzz", "单字符重复", "zzzzz", "输出 z"),
        ("abcABC123", "字母数字各一次", "按 ASCII 的一种合法序", "打乱相同频率的块内部"),
        ("mississippi", "多字母不同次数", "频率降序连续块", "没把相同字母连在一起"),
        (rnd, "中等随机", "自校验计数与连续性", "按字典序而不是频率"),
        (long_tie, "较长串，a、b 次数相同", "SPJ 允许两种块顺序", "交叉摆放 a、b"),
        (huge_s, "压满 |s|=5e5，62 种字符", "O(|s|)", "O(|s|^2) 排序 TLE"),
    ]

    answers, metas = [], []
    for i, (s, _, _, _) in enumerate(plan, 1):
        metas.append(s)
        answers.append(write_case(i, s))
    assert answers[0] == "eert"
    assert answers[1] == "aaaccc"
    assert answers[2] == "bbAa"
    assert answers[3] == "a"

    for i, s in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == s
        assert ob.decode("utf-8")[:-1] == answers[i - 1]

    assert (DATA / "checker.cc").is_file()
    assert (DATA / "config.yaml").is_file()

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7163 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。多解，评测使用 `checker.cc`（testlib）。",
            r"约束：$1\le |s|\le 5\times 10^5$，大小写字母与数字。",
            "",
            "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
            "|---|---|---|---|",
            *rows,
            "",
            "`.in` 为整串且末尾无换行；`.out` 末尾恰好一个换行符。",
            "",
        ]),
        encoding="utf-8",
    )
    print("generated 10 cases")
    for i, a in enumerate(answers, 1):
        print(i, len(a))


if __name__ == "__main__":
    main()
