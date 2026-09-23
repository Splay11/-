# -*- coding: utf-8 -*-
"""P7174 造数：银行卡最长前缀匹配。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(717420260915)
N_MAX = 10**5
M_MAX = 10**5
PRE_MAX = 20
CARD_MAX = 30


def bank_name(i: int) -> str:
    # 只用大小写字母，把编号编成 6 位 26 进制，保证 1e5 内互不撞车
    chars = []
    x = i + 1
    for k in range(6):
        base = ord("A") if k % 2 == 0 else ord("a")
        chars.append(chr(base + (x % 26)))
        x //= 26
    return "".join(chars)


def brute(prefixes, cards):
    mp = {p: b for p, b in prefixes}
    out = []
    for card in cards:
        ans = "UNKNOWN"
        best = 0
        lim = min(PRE_MAX, len(card))
        for L in range(1, lim + 1):
            pref = card[:L]
            if pref in mp and L > best:
                best = L
                ans = mp[pref]
        out.append(ans)
    return out


def rand_digits(length: int) -> str:
    return "".join(RNG.choice("0123456789") for _ in range(length))


def write_case(idx, prefixes, cards, note, hack):
    n = len(prefixes)
    m = len(cards)
    assert 1 <= n <= N_MAX
    assert 1 <= m <= M_MAX
    seen = set()
    for p, b in prefixes:
        assert 1 <= len(p) <= PRE_MAX
        assert p.isdigit()
        assert p not in seen
        seen.add(p)
        assert 1 <= len(b) <= 30
        assert b.isalpha()
    for c in cards:
        assert 1 <= len(c) <= CARD_MAX
        assert c.isdigit()
    ans = solve(prefixes, cards)
    if n * m <= 2 * 10**6:
        assert ans == brute(prefixes, cards)
    else:
        # 大数据用同一套从长到短的哈希核对一遍
        assert ans == brute(prefixes, cards)
    lines = [str(n)]
    for p, b in prefixes:
        lines.append(p + " " + b)
    lines.append(str(m))
    lines.extend(cards)
    (DATA / f"{idx}.in").write_bytes("\n".join(lines).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(ans) + "\n")
    return note, hack, n, m


def unique_random_prefixes(k, lo, hi, forbidden):
    s = set()
    while len(s) < k:
        L = RNG.randint(lo, hi)
        p = rand_digits(L)
        if p not in forbidden and p not in s:
            s.add(p)
    return list(s)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = []

    # 1 样例 1
    p1 = [("62", "BankA"), ("6222", "BankB"), ("622202", "BankC"), ("955", "BankD")]
    c1 = ["6222021234567890", "622233445566", "621234567890", "955880012345", "123456789"]
    plan.append((p1, c1, "样例 1 嵌套前缀", "按输入取第一条得到 BankA"))

    # 2 样例 2
    p2 = [("1", "Alpha"), ("12", "Beta"), ("123", "Gamma")]
    c2 = ["123456", "129999", "188888", "999999"]
    plan.append((p2, c2, "样例 2 数字链", "最短前缀优先"))

    # 3 最小规模，全部 UNKNOWN
    plan.append(
        ([("7", "Seven")], ["0", "8", "123"], "最小 n、全 UNKNOWN", "漏输出 UNKNOWN")
    )

    # 4 精确等于前缀，以及卡号比前缀短
    plan.append(
        (
            [("12345", "Short"), ("1234567890", "Long")],
            ["12345", "1234567890", "123456789012345", "1234", "12346"],
            "精确匹配与卡号更短",
            "用等于判断而不是前缀",
        )
    )

    # 5 短前缀写在前面：卡“按第一条匹配”的解
    plan.append(
        (
            [("1", "Alpha"), ("12", "Beta"), ("123", "Gamma"), ("9", "Omega")],
            ["123456", "129999", "188888", "9", "90", "0999"],
            "短规则在前",
            "startswith 后立刻 break",
        )
    )

    # 6 长前缀写在前面：卡“按最后一条匹配”的解
    plan.append(
        (
            [("622202", "BankC"), ("6222", "BankB"), ("62", "BankA"), ("955", "BankD")],
            ["6222021234567890", "622233445566", "621234567890", "955880012345", "62"],
            "长规则在前",
            "循环里不断覆盖成更短前缀",
        )
    )

    # 7 前导零、全零卡号
    plan.append(
        (
            [("0", "Zero"), ("00", "Double"), ("007", "Bond"), ("000", "Triple")],
            ["0", "00", "000", "007", "0071", "0007", "01", "1"],
            "前导零嵌套",
            "把前导零当空串丢掉",
        )
    )

    # 8 中等随机 + 边界长度
    forbidden = set()
    mid_p = unique_random_prefixes(80, 1, 20, forbidden)
    prefixes8 = [(p, bank_name(i)) for i, p in enumerate(mid_p)]
    mp8 = {p: b for p, b in prefixes8}
    cards8 = []
    # 命中最长
    for p, _ in prefixes8[:30]:
        extra = rand_digits(RNG.randint(0, CARD_MAX - len(p)))
        cards8.append(p + extra)
    # 卡号长度贴上限
    cards8.append(rand_digits(CARD_MAX))
    cards8.append("0" * CARD_MAX)
    # 故意 UNKNOWN：改最后一个数字
    for p, _ in prefixes8[30:50]:
        q = p[:-1] + ("0" if p[-1] != "0" else "1")
        if q not in mp8 and all(q[:L] not in mp8 for L in range(1, len(q) + 1)):
            cards8.append(q[: min(CARD_MAX, max(1, len(q)))])
        else:
            cards8.append("9" * min(CARD_MAX, 9))
    while len(cards8) < 120:
        cards8.append(rand_digits(RNG.randint(1, CARD_MAX)))
    plan.append((prefixes8, cards8, "中等随机约 80 条规则", "漏边界长度 20/30"))

    # 9 压满：8 位前缀 1e5 条，无更短前缀，卡 O(n) 扫会 TLE
    n9 = N_MAX
    prefs9 = [(f"{i:08d}", bank_name(i)) for i in range(n9)]
    cards9 = []
    for i in range(0, n9, 2):
        extra = rand_digits(RNG.randint(0, CARD_MAX - 8))
        cards9.append(prefs9[i][0] + extra)
        if len(cards9) >= M_MAX // 2:
            break
    k = 0
    while len(cards9) < M_MAX:
        # 00100000 起，碰不到 00000000-00099999，也没有更短前缀
        x = 100000 + k
        k += 1
        cards9.append(f"{x:08d}" + rand_digits(RNG.randint(0, CARD_MAX - 8)))
    cards9 = cards9[:M_MAX]
    plan.append((prefs9, cards9, "n=m=1e5，定长 8 位前缀", "对每个卡号扫全部规则 TLE"))

    # 10 压满：大量嵌套前缀，必须取最长
    chain_roots = []
    seen10 = set()
    prefixes10 = []
    # 2000 条链，每条 1..20 逐步加长，约 2000*20=40000
    for t in range(2000):
        root = rand_digits(1)
        cur = root
        if cur not in seen10:
            seen10.add(cur)
            prefixes10.append((cur, bank_name(len(prefixes10))))
        for L in range(2, 21):
            cur = cur + RNG.choice("0123456789")
            if cur not in seen10:
                seen10.add(cur)
                prefixes10.append((cur, bank_name(len(prefixes10))))
        chain_roots.append(cur)
    # 补到 1e5：长度 12 的互异前缀
    while len(prefixes10) < N_MAX:
        p = rand_digits(12)
        if p not in seen10:
            seen10.add(p)
            prefixes10.append((p, bank_name(len(prefixes10))))
    prefixes10 = prefixes10[:N_MAX]
    cards10 = []
    # 走完整条链再补后缀，必须命中长度 20；再截断一次测中等长度
    for cur in chain_roots:
        extra = rand_digits(CARD_MAX - len(cur)) if len(cur) < CARD_MAX else ""
        cards10.append(cur + extra)
        cards10.append(cur[: RNG.randint(1, len(cur))])
    while len(cards10) < M_MAX:
        cards10.append(rand_digits(RNG.randint(1, CARD_MAX)))
    cards10 = cards10[:M_MAX]
    plan.append((prefixes10, cards10, "n=m=1e5，最长 20 的嵌套链", "取最短或取输入最后一条"))

    rows = []
    for i, (prefs, cards, note, hack) in enumerate(plan, 1):
        note, hack, n, m = write_case(i, prefs, cards, note, hack)
        rows.append(f"| {i} | {note}（n={n}, m={m}） | 最长前缀银行名 | {hack} |")

    for i in range(1, 11):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert b"\r" not in ob

    # 核对样例输出
    s1 = (DATA / "1.out").read_text(encoding="utf-8")
    assert s1 == "BankC\nBankB\nBankA\nBankD\nUNKNOWN\n"
    s2 = (DATA / "2.out").read_text(encoding="utf-8")
    assert s2 == "Gamma\nBeta\nAlpha\nUNKNOWN\n"

    (DATA / "README.md").write_text(
        "\n".join(
            [
                "# P7174 测试数据说明",
                "",
                r"主造数脚本：题目根目录 `gen.py`。最长前缀匹配；无匹配输出 `UNKNOWN`。",
                r"约束：$1\le n,m\le 10^5$，$|prefix|\le 20$，$|card|\le 30$。",
                "",
                "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
                "|---|---|---|---|",
                *rows,
                "",
                "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print("generated 10 cases")


if __name__ == "__main__":
    main()
