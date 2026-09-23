# -*- coding: utf-8 -*-
"""P7138 造数：用最短词根替换句子中的衍生词。

stdin：第一行 n；第二行 n 个词根；第三行句子（无首尾空格）。
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
RNG = random.Random(713820260914)

N_MAX = 1000
ROOT_LEN_MAX = 100
WORD_LEN_MAX = 1000
SENT_LEN_MAX = 10**6
WORD_CNT_MAX = 1000


def naive(dictionary, sentence):
    s = set(dictionary)
    max_r = max(len(x) for x in dictionary)
    out = []
    for w in sentence.split(" "):
        rep = w
        up = min(len(w), max_r)
        for L in range(1, up + 1):
            if w[:L] in s:
                rep = w[:L]
                break
        out.append(rep)
    return " ".join(out)


def rand_word(lo, hi):
    k = RNG.randint(lo, hi)
    return "".join(RNG.choice(string.ascii_lowercase) for _ in range(k))


def case_in_text(dictionary, sentence):
    n = len(dictionary)
    return f"{n}\n" + " ".join(dictionary) + "\n" + sentence


def write_case(idx, dictionary, sentence):
    n = len(dictionary)
    words = sentence.split(" ")
    assert 1 <= n <= N_MAX
    assert all(1 <= len(w) <= ROOT_LEN_MAX and w.isalpha() and w.islower() for w in dictionary)
    assert 1 <= len(words) <= WORD_CNT_MAX
    assert all(1 <= len(w) <= WORD_LEN_MAX for w in words)
    assert "  " not in sentence
    assert not sentence.startswith(" ") and not sentence.endswith(" ")
    assert 1 <= len(sentence) <= SENT_LEN_MAX
    (DATA / f"{idx}.in").write_bytes(case_in_text(dictionary, sentence).encode("utf-8"))
    ans = solve(dictionary, sentence)
    expect = naive(dictionary, sentence)
    assert ans == expect, (idx, ans[:80], expect[:80])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    s1_d = ["cat", "bat", "rat"]
    s1_s = "the cattle was rattled by the battery"
    s2_d = ["a", "b", "c"]
    s2_s = "aadsfasf absbs bbab cadsfafs"

    none_d = ["xyz", "uvw"]
    none_s = "hello world python"

    # cat 比 cattle 短，单词 cattlelike 应换成 cat 而不是更长前缀
    short_d = ["cat", "cattle"]
    short_s = "cattle cattlelike cat cats"

    # 词根本身出现在句子里
    same_d = ["go", "gone"]
    same_s = "go gone going"

    one_d = ["ab"]
    one_s = "abacus"

    rnd_d = [rand_word(1, 8) for _ in range(20)]
    rnd_w = [rand_word(1, 12) for _ in range(15)]
    # 掺几个确定能匹配的
    rnd_w[0] = rnd_d[0] + "zzz"
    rnd_s = " ".join(rnd_w)

    # 压长度：约 1e6 字符，1000 个单词、每词约 999
    big_d = ["q" + rand_word(4, 9) for _ in range(N_MAX)]
    # 多数单词以 z 开头，不匹配；少数用某个词根当前缀
    big_words = []
    remain = SENT_LEN_MAX
    wc = WORD_CNT_MAX
    # 预留 wc-1 个空格
    remain -= wc - 1
    base = remain // wc
    extra = remain % wc
    for i in range(wc):
        L = base + (1 if i < extra else 0)
        L = min(WORD_LEN_MAX, max(1, L))
        if i % 20 == 0:
            root = big_d[i % len(big_d)]
            tail = max(0, L - len(root))
            w = root + ("z" * tail)
        else:
            w = "z" + "".join(RNG.choice("xyz") for _ in range(L - 1))
        if len(w) > WORD_LEN_MAX:
            w = w[:WORD_LEN_MAX]
        big_words.append(w)
    big_s = " ".join(big_words)
    if len(big_s) > SENT_LEN_MAX:
        # 丢掉最后一个单词，保证不超过上限
        while len(big_s) > SENT_LEN_MAX and len(big_words) > 1:
            big_words.pop()
            big_s = " ".join(big_words)

    # 另一组大数据：短词根 a，几乎所有单词都会被换成 a
    d10 = ["a"] * 10 + [rand_word(2, 6) for _ in range(50)]
    w10 = ["a" + rand_word(50, 80) for _ in range(200)]
    s10 = " ".join(w10)

    plan = [
        (s1_d, s1_s,
         "样例 1", "cattle/rattled/battery 分别换成 cat/rat/bat",
         "用了包含关系而不是前缀，the 被 cat 影响"),
        (s2_d, s2_s,
         "样例 2，单字母词根", "四个单词都换成 $a\\ a\\ b\\ c$",
         "absbs 用更长的假词根"),
        (none_d, none_s,
         "没有任何前缀匹配", "原句不动",
         "整句清空或乱插空格"),
        (short_d, short_s,
         "同一单词有长短两个词根", "一律用更短的 $cat$",
         "用了最长词根 $cattle$"),
        (same_d, same_s,
         "词根本身出现在句子中", "$go$ 保持，$gone$ 用 $go$，$going$ 用 $go$",
         "gone 不被替换"),
        (one_d, one_s,
         "只有一个单词", "$abacus\\to ab$",
         "输出带多余空格"),
        (["x"], "x",
         "单词根单字母句子", "就是 $x$",
         "去读不存在的后续单词"),
        (rnd_d, rnd_s,
         "小随机词根和单词", "字典树与按前缀长度扫描对拍",
         "拆句时用了多个空格"),
        (big_d, big_s,
         "压满约 $10^6$ 字符、$1000$ 词根", "线性扫字典树",
         "每个前缀都去线性扫词典导致 TLE"),
        (d10, s10,
         "短词根 $a$ 覆盖 $200$ 个长单词", "全部变成 $a$",
         "只替换第一个单词"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (d, s, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, d, s))

    for i, (d, s, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        assert int(lines[0]) == len(d)
        assert lines[1].split() == d
        assert lines[2] == s
        got = ob.decode("utf-8")[:-1]
        assert got == answers[i - 1] == naive(d, s)

    assert answers[0] == "the cat was rat by the bat"
    assert answers[1] == "a a b c"
    assert answers[2] == none_s
    assert answers[4] == "go go go"
    assert answers[5] == "ab"
    assert answers[6] == "x"
    assert set(answers[9].split()) == {"a"}

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7138 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$；第二行 $n$ 个词根；第三行句子（无首尾空格，单词间一个空格）。",
        "输出：用最短词根替换衍生词后的句子。",
        "",
        r"约束：$1\le n\le 1000$，词根长 $\le 100$，句子长 $\le 10^6$，单词数 $\le 1000$，单词长 $\le 1000$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：字典树结果必须等于按前缀从短到长查哈希表。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "words", len(ans.split()), "len", len(ans), "head", ans[:40])


if __name__ == "__main__":
    main()
