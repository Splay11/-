# -*- coding: utf-8 -*-
"""P7161 造数：所有串的公共字符（含次数），字典序输出。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716120260915)
N_MAX, L_MAX = 100, 100


def brute(words):
    from collections import Counter
    m = Counter(words[0])
    for w in words[1:]:
        m &= Counter(w)
    chars = []
    for ch in sorted(m):
        chars.extend([ch] * m[ch])
    return chars


def write_case(idx, words):
    n = len(words)
    assert 1 <= n <= N_MAX
    for w in words:
        assert 1 <= len(w) <= L_MAX
        assert w.isalpha() and w.islower()
    chars = solve(words)
    assert chars == brute(words)
    inp = f"{n}\n" + "\n".join(words)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    if chars:
        out = f"{len(chars)}\n" + " ".join(chars) + "\n"
    else:
        out = "0\n"
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    return chars


def rand_word(ln):
    return "".join(chr(97 + RNG.randint(0, 25)) for _ in range(ln))


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    big = [rand_word(L_MAX) for _ in range(N_MAX)]
    all_a = ["a" * L_MAX] * N_MAX

    plan = [
        (["bella", "label", "roller"], "样例 1，$e$ 一次 $l$ 两次", "3 / e l l", "忽略次数只输出 e l"),
        (["cool", "lock", "cook"], "样例 2", "2 / c o", "没按字典序"),
        (["abc"], "n=1，整串都是公共", "a b c", "输出 0"),
        (["abc", "def"], "完全没有公共字母", "只输出 0", "仍打印空第二行"),
        (["zzaa", "aa", "aaaa"], "次数取最小，$a$ 两次", "a a", "按最长串次数输出 4 个 a"),
        (["z", "z", "y"], "单字母对不上", "0", "输出 z"),
        (["ab", "ba", "aaab"], "公共 a 一次", "a", "输出 a b"),
        ([rand_word(8) for _ in range(12)], "中等随机", "与 Counter 交对拍", "只做集合交"),
        (big, "压满 n=100，每串长度 100", "O(nL) 计数", "指数枚举"),
        (all_a, "压满全是 a", "100 个 a", "输出 1 个 a"),
    ]

    answers, metas = [], []
    for i, (words, _, _, _) in enumerate(plan, 1):
        metas.append(words)
        answers.append(write_case(i, words))
    assert answers[0] == list("ell")
    assert answers[1] == list("co")
    assert answers[3] == []

    for i, words in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(words)}\n" + "\n".join(words)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7161 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。",
            "有公共字符时两行：个数、按字典序空格分隔的字符；否则只一行 $0$。",
            r"约束：$1\le n,|words_i|\le 100$，小写字母。",
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
    for i, ch in enumerate(answers, 1):
        print(i, len(ch), "n", len(metas[i - 1]))


if __name__ == "__main__":
    main()
