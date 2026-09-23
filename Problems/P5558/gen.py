# -*- coding: utf-8 -*-
"""P5558 双色条码最长保留：按四级题面造 10 组数据。

输入两行：第一行 m，第二行只含 a/b 的字符串。
正解：枚举深色段右端点，用前缀维护左端点的最优差。
"""
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def solve(s):
    m = len(s)
    cnt_a = [0] * (m + 1)
    cnt_b = [0] * (m + 1)
    for i, ch in enumerate(s):
        cnt_a[i + 1] = cnt_a[i] + (ch == "a")
        cnt_b[i + 1] = cnt_b[i] + (ch == "b")
    total_a = cnt_a[m]
    best_diff = -10**18
    ans = 0
    for j in range(m + 1):
        best_diff = max(best_diff, cnt_a[j] - cnt_b[j])
        cur = best_diff + cnt_b[j] + (total_a - cnt_a[j])
        if cur > ans:
            ans = cur
    return ans


def solve_n2(s):
    """双重枚举左右切分点，用来对拍线性解。"""
    m = len(s)
    cnt_a = [0] * (m + 1)
    cnt_b = [0] * (m + 1)
    for i, ch in enumerate(s):
        cnt_a[i + 1] = cnt_a[i] + (ch == "a")
        cnt_b[i + 1] = cnt_b[i] + (ch == "b")
    total_a = cnt_a[m]
    ans = 0
    for j in range(m + 1):
        best_diff = -10**18
        for i in range(j + 1):
            best_diff = max(best_diff, cnt_a[i] - cnt_b[i])
        cur = best_diff + cnt_b[j] + (total_a - cnt_a[j])
        if cur > ans:
            ans = cur
    return ans


def brute(s):
    """n 很小的时候枚举保留子集，只接受 a*b*a*。"""
    n = len(s)
    best = 0
    for mask in range(1 << n):
        kept = [s[i] for i in range(n) if mask & (1 << i)]
        if not kept:
            continue
        bpos = [i for i, ch in enumerate(kept) if ch == "b"]
        if not bpos:
            best = max(best, len(kept))
            continue
        left, right = bpos[0], bpos[-1]
        if any(ch != "b" for ch in kept[left : right + 1]):
            continue
        best = max(best, len(kept))
    return best


def wrong_substring(s):
    """只在连续子串里找合格条码，删不掉中间墨点。"""
    n = len(s)
    best = 0
    for i in range(n):
        state = 0
        for j in range(i, n):
            ch = s[j]
            if state == 0:
                if ch == "b":
                    state = 1
            elif state == 1:
                if ch == "a":
                    state = 2
            elif ch == "b":
                break
            best = max(best, j - i + 1)
    return best


def wrong_ab(s):
    """只拼 a*b*，不要末尾再来一段 a。"""
    total_b = s.count("b")
    best = max(s.count("a"), total_b)
    ca = 0
    seen_b = 0
    for ch in s:
        if ch == "a":
            ca += 1
        else:
            seen_b += 1
        best = max(best, ca + (total_b - seen_b))
    return best


def wrong_ba(s):
    """只拼 b*a*，不要开头再来一段 a。"""
    total_a = s.count("a")
    best = max(total_a, s.count("b"))
    cb = 0
    seen_a = 0
    for ch in s:
        if ch == "b":
            cb += 1
        else:
            seen_a += 1
        best = max(best, cb + (total_a - seen_a))
    return best


def wrong_count(s):
    """只取浅色颗数和深色颗数的较大值。"""
    return max(s.count("a"), s.count("b"))


def write_in(path, text):
    # 最后一行后面不要换行
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    if text.endswith("\n"):
        body = text[:-1]
    else:
        body = text
    if "\n" in body:
        raise RuntimeError("答案不应含多行: %s" % path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body + "\n")


def pack(s):
    return "%d\n%s" % (len(s), s)


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5558)

    # 原题样例（不进新题面，只用来确认算法核没变）
    assert solve("abba") == 4
    assert solve("bab") == 2

    # 手算样例
    assert solve("bbaaba") == 5
    assert solve("ababa") == 4
    assert wrong_substring("bbaaba") == 4
    assert wrong_substring("ababa") == 3
    assert wrong_count("ababa") == 3

    # 单侧形态
    assert solve("baa") == 3 and wrong_ab("baa") == 2
    assert solve("aab") == 3 and wrong_ba("aab") == 2
    assert solve("a") == 1 and solve("b") == 1
    assert solve("a" * 20) == 20 and solve("b" * 20) == 20

    alt = "ab" * 2500
    block = "a" * 1000 + "b" * 3000 + "a" * 1000
    assert solve(alt) == 2501
    # 交替串里最长的连续合格段只有 aba，长度为 3
    assert wrong_substring(alt) == 3
    assert wrong_count(alt) == 2500
    assert solve(block) == 5000
    assert wrong_ab(block) == 4000
    assert wrong_ba(block) == 4000

    for n in (1, 8, 12):
        for _ in range(20):
            s = "".join(rng.choice("ab") for _ in range(n))
            got = solve(s)
            assert got == solve_n2(s)
            if n <= 12:
                assert got == brute(s)

    mid = "".join(rng.choice("ab") for _ in range(400))
    assert solve(mid) == solve_n2(mid)

    # 1 样例：删掉中间深色，子串假解偏短
    # 2 样例：交错串，连续子串和「只数个数」都偏短
    # 3-4 最小规模
    # 5 全深色，两侧浅色段为空
    # 6 卡只做 a*b*
    # 7 卡只做 b*a*
    # 8 中等随机
    # 9 满长度交替：连续子串最长只有 3，只数个数得到 2500
    # 10 满长度三段：只做 a*b* 或只做 b*a* 都只有 4000
    cases = [
        "bbaaba",
        "ababa",
        "a",
        "b",
        "b" * 20,
        "baa",
        "aab",
        mid,
        alt,
        block,
    ]
    assert len(cases) == 10

    for i, s in enumerate(cases, 1):
        inp = pack(s)
        ans = str(solve(s))
        assert solve_n2(s) == int(ans)
        in_path = os.path.join(DATA, "%d.in" % i)
        out_path = os.path.join(DATA, "%d.out" % i)
        write_in(in_path, inp)
        write_out(out_path, ans)
        raw_in = open(in_path, "rb").read()
        raw_out = open(out_path, "rb").read()
        if raw_in.endswith(b"\n"):
            raise RuntimeError("%d.in 末尾多了换行" % i)
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise RuntimeError("%d.out 换行不符合要求" % i)

    cfg = """type: default
time: 2s
memory: 256m
subtasks:
  - score: 100
    type: sum
    cases:
"""
    for i in range(1, 11):
        cfg += "      - input: %d.in\n        output: %d.out\n" % (i, i)
    cfg += "langs:\n  - py.py3\n  - java\n  - cc.cc14o2\n"
    with open(os.path.join(DATA, "config.yaml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(cfg)

    # 用 std.py 回读全部输入，核对写出的答案
    for i in range(1, 11):
        raw = open(os.path.join(DATA, "%d.in" % i), "rb").read()
        p = subprocess.run(
            [sys.executable, os.path.join(DIR, "std.py")],
            input=raw,
            capture_output=True,
        )
        if p.returncode != 0:
            raise RuntimeError(p.stderr.decode("utf-8", "replace"))
        got = p.stdout.replace(b"\r\n", b"\n")
        expect = open(os.path.join(DATA, "%d.out" % i), "rb").read()
        if got != expect:
            raise RuntimeError("std.py 与 %d.out 不一致: %r vs %r" % (i, got, expect))
        print("ok", i, "n", raw.split(b"\n", 1)[0].decode(), "ans", got.decode().strip())

    print("P5558 data ready")


if __name__ == "__main__":
    main()
