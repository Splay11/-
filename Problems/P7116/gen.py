# -*- coding: utf-8 -*-
"""P7116 造数：长度至少为 k 的无重复子串计数。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7116)


def load_std():
    spec = importlib.util.spec_from_file_location("p7116_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.count_unique


count_unique = load_std()


def brute(s, k):
    n = len(s)
    ans = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            if j - i + 1 >= k:
                ans += 1
    return ans


def wrong_strict_gt(s, k):
    return count_unique(s, k + 1)


def wrong_longest_only(s, k):
    """假解：只求最长无重复长度，再看是否 >= k。"""
    last = [-1] * 26
    left = 0
    best = 0
    for right, ch in enumerate(s):
        idx = ord(ch) - 97
        if last[idx] >= left:
            left = last[idx] + 1
        last[idx] = right
        best = max(best, right - left + 1)
    return 1 if best >= k else 0


def write_case(idx, s, k):
    assert s.isalpha() and s.islower()
    assert 1 <= len(s) <= 10**5
    assert 1 <= k <= 10**5
    text_in = s + "\n" + str(k)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    ans = count_unique(s, k)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_s(n, alphabet):
    return "".join(RNG.choice(alphabet) for _ in range(n))


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例
    cases.append(("abcabcbb", 3))
    # 2. 样例：全相同且 k=2
    cases.append(("aaaa", 2))
    # 3. 最短
    cases.append(("a", 1))
    # 4. k > n，答案 0
    cases.append(("abc", 5))
    # 5. 全互异，k=1，答案为全部子串
    cases.append(("abcdef", 1))
    # 6. 随机小串，与暴力对拍
    cases.append((rand_s(20, "abcde"), 3))
    # 7. hack：k 恰好等于某段无重复长度，卡 >k
    cases.append(("abcabc", 3))
    # 8. 单字符重复，k=1
    cases.append(("zzzzz", 1))
    # 9. 大数据随机
    cases.append((rand_s(10**5, "abcdefghijklmnopqrstuvwxyz"), 10))
    # 10. 大数据全互异循环字母，卡 O(n^2) 与 int 溢出
    letters = "abcdefghijklmnopqrstuvwxyz"
    s10 = (letters * ((10**5) // 26 + 1))[:10**5]
    cases.append((s10, 1))

    notes = [
        "样例 abcabcbb k=3，答案 4",
        "全 a，k=2，答案 0",
        "n=k=1",
        "k>n，答案 0",
        "全互异 k=1，答案 n(n+1)/2",
        "随机小串对拍",
        "hack 长度恰好为 k，卡写成 >k",
        "全相同 k=1，答案 n",
        "n=1e5 随机压测",
        "n=1e5 k=1，卡暴力与 32 位溢出",
    ]

    for i, (s, k) in enumerate(cases, 1):
        ans = write_case(i, s, k)
        extra = ""
        if len(s) <= 40:
            b = brute(s, k)
            if b != ans:
                raise SystemExit(f"与暴力不一致：第 {i} 组 {ans} vs {b}")
            extra = f" brute={b}"
        print(
            f"case {i}: n={len(s)} k={k} ans={ans} "
            f"gt={wrong_strict_gt(s, k)} longest={wrong_longest_only(s, k)}"
            f"{extra} note={notes[i - 1]}"
        )

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        s, ks = raw.split("\n")
        k = int(ks)
        got = count_unique(s, k)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out")
        if (DATA / f"{i}.in").read_bytes().endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        outb = (DATA / f"{i}.out").read_bytes()
        if not outb.endswith(b"\n") or outb.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    # 第 1、7 组应卡 >k；第 1 组应卡只输出最长
    s1, k1 = "abcabcbb", 3
    if wrong_strict_gt(s1, k1) == count_unique(s1, k1):
        raise SystemExit("第 1 组未能卡掉 >k")
    if wrong_longest_only(s1, k1) == count_unique(s1, k1):
        raise SystemExit("第 1 组未能卡掉只求最长")
    s7, k7 = "abcabc", 3
    if wrong_strict_gt(s7, k7) == count_unique(s7, k7):
        raise SystemExit("第 7 组未能卡掉 >k")

    print("gen ok")


if __name__ == "__main__":
    main()
