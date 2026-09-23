# -*- coding: utf-8 -*-
"""P7151 造数：前 k 个高频单词。

stdin：第一行 n k，第二行 n 个小写单词。
输出：k 个单词，空格分隔。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715120260915)

N_MAX = 500
LEN_MAX = 10


def naive(words, k):
    """先按字典序再稳定按次数降序，与复合关键字排序对拍。"""
    cnt = {}
    for w in words:
        cnt[w] = cnt.get(w, 0) + 1
    items = list(cnt.items())
    items.sort(key=lambda x: x[0])
    items.sort(key=lambda x: -x[1])
    return [w for w, _ in items[:k]]


def write_case(idx, words, k):
    n = len(words)
    assert 1 <= n <= N_MAX
    assert 1 <= k <= len(set(words))
    for w in words:
        assert 1 <= len(w) <= LEN_MAX
        assert w.isalpha() and w.islower()
    ans = solve(words, k)
    expect = naive(words, k)
    assert ans == expect, (idx, ans, expect)
    assert len(ans) == k
    inp = f"{n} {k}\n" + " ".join(words)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(" ".join(ans) + "\n")
    return ans


def rand_word(lo=1, hi=LEN_MAX):
    L = RNG.randint(lo, hi)
    return "".join(RNG.choice(string.ascii_lowercase) for _ in range(L))


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    vocab8 = [rand_word(1, 4) for _ in range(6)]
    p8 = [RNG.choice(vocab8) for _ in range(20)]
    k8 = min(3, len(set(p8)))

    vocab9 = [rand_word() for _ in range(20)]
    p9 = [RNG.choice(vocab9) for _ in range(N_MAX)]
    k9 = min(10, len(set(p9)))

    # 尽量多不同单词
    used = set()
    p10 = []
    while len(p10) < N_MAX:
        w = rand_word()
        if w not in used:
            used.add(w)
            p10.append(w)
        if len(used) >= N_MAX:
            break
    while len(p10) < N_MAX:
        p10.append(RNG.choice(p10))
    k10 = len(set(p10))

    plan = [
        (["i", "love", "leetcode", "i", "love", "coding"], 2,
         "样例 1，同频按字典序", "$i$ 在 $love$ 前",
         "按出现先后输出 $i$ $love$ 虽碰巧对，但 $love$ $i$ 会错"),
        (["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4,
         "样例 2，次数严格递减", "$the$ $is$ $sunny$ $day$",
         "漏掉次数为 $1$ 的 $day$"),
        (["a", "a", "a"], 1,
         "只有一种单词", "$a$",
         "输出多次 $a$"),
        (["z", "y", "x"], 3,
         "全部不同、次数都是 $1$", "字典序 $x$ $y$ $z$",
         "按输入顺序 $z$ $y$ $x$"),
        (["a", "b", "a"], 2,
         "一个高频一个低频", "$a$ $b$",
         "只输出 $a$"),
        (["c", "a", "b", "c", "a", "b"], 2,
         "三个单词同频", "字典序前两个 $a$ $b$",
         "按输入得到 $c$ $a$"),
        (["hello", "world", "hello"], 1,
         "只要最高频", "$hello$",
         "把 $world$ 也输出"),
        (p8, k8,
         "小随机短单词", "两种排序对拍",
         "同频没按字典序"),
        (p9, k9,
         "压满 $n=500$，约 $20$ 种单词", "计数后排序",
         "$O(n^2)$ 比较整表"),
        (p10, k10,
         "压满 $n=500$，不同单词尽量多，$k=m$", "输出全部不同单词",
         "k 取得不够"),
    ]
    assert len(plan) == 10

    answers = []
    metas = []
    for idx, (words, k, _, _, _) in enumerate(plan, 1):
        metas.append((words, k))
        answers.append(write_case(idx, words, k))

    for i, (words, k) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect_in = f"{len(words)} {k}\n" + " ".join(words)
        assert ib.decode("utf-8") == expect_in
        got = ob.decode("utf-8")[:-1]
        assert got == " ".join(answers[i - 1])
        assert answers[i - 1] == naive(words, k)

    assert answers[0] == ["i", "love"]
    assert answers[1] == ["the", "is", "sunny", "day"]
    assert answers[2] == ["a"]
    assert answers[3] == ["x", "y", "z"]
    assert answers[4] == ["a", "b"]
    assert answers[5] == ["a", "b"]
    assert answers[6] == ["hello"]
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7151 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$ $k$，第二行 $n$ 个小写单词。",
        "输出：$k$ 个单词，次数降序，同频字典序升序。",
        "",
        r"约束：$1\le n\le 500$，$1\le |words_i|\le 10$，$1\le k\le m$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：复合关键字排序必须等于先字典序再稳定按次数降序。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]), "k", metas[i - 1][1])


if __name__ == "__main__":
    main()
