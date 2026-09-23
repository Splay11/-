# -*- coding: utf-8 -*-
"""P7118 造数：有序无重复数组中和为 k 的数对个数。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7118)


def load_std():
    spec = importlib.util.spec_from_file_location("p7118_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution().twoSum2


two_sum2 = load_std()


def brute(nums, k):
    n = len(nums)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == k:
                ans += 1
    return ans


def unique_sorted(vals):
    return sorted(set(vals))


def rand_unique(n, lo, hi):
    s = set()
    while len(s) < n:
        s.add(RNG.randint(lo, hi))
    return sorted(s)


def write_case(idx, nums, k):
    n = len(nums)
    assert 1 <= n <= 10**5
    assert nums == sorted(set(nums))
    assert all(-(10**9) <= x <= 10**9 for x in nums)
    assert -(10**9) <= k <= 10**9
    lines = [f"{n} {k}", " ".join(str(x) for x in nums)]
    (DATA / f"{idx}.in").write_bytes("\n".join(lines).encode("utf-8"))
    ans = two_sum2(nums, k)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例
    cases.append(([-1, 1, 5, 7, 11], 6))
    # 2. n=1
    cases.append(([8], 0))
    # 3. 无解：全大于 k/2
    cases.append(([10, 20, 30], 5))
    # 4. 负数对
    cases.append(([-9, -4, -1, 2, 5], -5))
    # 5. k=0，若干相反数
    cases.append(([-7, -3, -1, 1, 3, 8], 0))
    # 6. 随机小数据对拍
    a = rand_unique(30, -50, 50)
    k = a[0] + a[-1] if len(a) >= 2 else 0
    cases.append((a, k))
    # 7. 相邻两项刚好为 k，卡只配两端
    cases.append(([1, 2, 4, 7, 11], 6))
    # 8. 两个元素
    cases.append(([-1000000000, 1000000000], 0))
    # 9. 大数据：很多互补对
    n9 = 10**5
    half = n9 // 2
    nums9 = list(range(-half, 0)) + list(range(1, half + 1))
    assert len(nums9) == n9
    cases.append((nums9, 0))
    # 10. 大数据随机
    cases.append((rand_unique(10**5, -(10**9), 10**9), 123456))

    notes = [
        "样例，答案 2",
        "n=1，答案 0",
        "全偏大，无解",
        "负数对 (-9,4 不存在) (-4,-1)",
        "k=0 的相反数",
        "随机小数据对拍",
        "hack：配对在中间而非两端",
        "值域两端，和为 0",
        "n=1e5，k=0，大量相反数",
        "n=1e5 随机压测",
    ]

    for i, (nums, k) in enumerate(cases, 1):
        ans = write_case(i, nums, k)
        extra = ""
        if len(nums) <= 40:
            b = brute(nums, k)
            if b != ans:
                raise SystemExit(f"与暴力不一致：第 {i} 组 {ans} vs {b}")
            extra = f" brute={b}"
        print(f"case {i}: n={len(nums)} k={k} ans={ans}{extra} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        n, k = map(int, lines[0].split())
        nums = list(map(int, lines[1].split()))
        assert n == len(nums)
        got = two_sum2(nums, k)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out")
        if (DATA / f"{i}.in").read_bytes().endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        outb = (DATA / f"{i}.out").read_bytes()
        if not outb.endswith(b"\n") or outb.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    print("gen ok")


if __name__ == "__main__":
    main()
