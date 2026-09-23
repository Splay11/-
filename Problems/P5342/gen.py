# -*- coding: utf-8 -*-
"""P5342 造数：统计 0/1 个数相等的串。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5342)


def load_std():
    spec = importlib.util.spec_from_file_location("p5342_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.count_clearable


count_clearable = load_std()


def wrong_paren(s):
    """错误：把 0 当左括号、1 当右括号做匹配。"""
    bal = 0
    for ch in s:
        if ch == "0":
            bal += 1
        else:
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


def wrong_even_only(s):
    """错误：只判断长度是偶数。"""
    return len(s) % 2 == 0


def write_case(idx, strs):
    m = len(strs)
    total = sum(len(s) for s in strs)
    assert 1 <= m <= 200000
    assert 1 <= total <= 500000
    for s in strs:
        assert 1 <= len(s) <= 100000
        assert all(ch in "01" for ch in s)
    ans = count_clearable(strs)
    lines = [str(m)] + strs
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_bitstr(n):
    return "".join(RNG.choice("01") for _ in range(n))


def equal_str(k):
    """长度为 2k、0 和 1 各 k 个的随机串。"""
    chars = ["0"] * k + ["1"] * k
    RNG.shuffle(chars)
    return "".join(chars)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1-3 样例
    cases.append(["00", "11", "10", "000"])
    cases.append(["1010", "1100", "1001"])
    cases.append(["111000"])
    # 4. 单条奇数，不可核销
    cases.append(["111"])
    # 5. 全是可核销的短串
    cases.append(["10", "01", "1100", "0011"])
    # 6. 括号匹配假解：1100 计数相等但 0=( 1=) 会失败
    cases.append(["1100", "0011", "1010", "000111"])
    # 7. 偶数长度但 0/1 个数不等
    cases.append(["0000", "1111", "001000"])
    # 8. 小随机
    small = [rand_bitstr(RNG.randint(1, 20)) for _ in range(30)]
    small.append(equal_str(8))
    cases.append(small)
    # 9. 中等：若干等长混合
    mid = []
    for _ in range(200):
        if RNG.random() < 0.4:
            mid.append(equal_str(RNG.randint(1, 40)))
        else:
            mid.append(rand_bitstr(RNG.randint(1, 80)))
    cases.append(mid)
    # 10. 满约束附近：大量短串
    big = []
    for i in range(100000):
        big.append("10" if i % 2 == 0 else "00")
    cases.append(big)

    notes = [
        "样例1",
        "样例2 三条都可核销",
        "样例3 111000",
        "奇数长度",
        "短串均可核销",
        "卡括号匹配：含 1100",
        "偶数但 0/1 个数不等",
        "小随机",
        "中等随机",
        "n=100000 短串压测",
    ]

    for i, strs in enumerate(cases, 1):
        ans = write_case(i, strs)
        p_wrong = sum(1 for s in strs if wrong_paren(s))
        e_wrong = sum(1 for s in strs if wrong_even_only(s))
        print(
            f"case {i}: m={len(strs)} L={sum(len(s) for s in strs)} "
            f"ans={ans} paren={p_wrong} even={e_wrong} note={notes[i - 1]}"
        )

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        m = int(lines[0])
        strs = lines[1 : m + 1]
        got = count_clearable(strs)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    # 第 6 组必须卡住括号匹配
    s6 = cases[5]
    if sum(wrong_paren(s) for s in s6) == count_clearable(s6):
        raise SystemExit("第 6 组未能卡掉括号匹配")
    # 第 7 组必须卡住「只看偶数长度」
    s7 = cases[6]
    if sum(wrong_even_only(s) for s in s7) == count_clearable(s7):
        raise SystemExit("第 7 组未能卡掉偶数长度假解")

    print("gen ok")


if __name__ == "__main__":
    main()
