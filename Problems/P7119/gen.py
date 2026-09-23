# -*- coding: utf-8 -*-
"""P7119 造数：寻找数组的中心下标（ACM 模式，stdin 两行：n，然后 n 个整数）。

10 组数据：前 8 组小数据（样例 / 基础 / 边界 / 随机），后 2 组大数据压满 n=10^4。
写文件规则：`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(711920260914)

N_MAX = 10 ** 4
V_LO, V_HI = -1000, 1000


def pivot_index(nums):
    """基准解：前缀和一次扫描，返回最靠左的中心下标，找不到返回 -1。"""
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1


def brute_pivot(nums):
    """独立暴力：对每个下标分别求左右两侧的和，用于交叉校验基准解。"""
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):
            return i
    return -1


def case_text(nums):
    return str(len(nums)) + "\n" + " ".join(str(x) for x in nums)


def write_case(idx, nums):
    assert 1 <= len(nums) <= N_MAX, (idx, len(nums))
    assert all(V_LO <= x <= V_HI for x in nums), idx
    # .in：最后一行数据后不留换行符
    (DATA / f"{idx}.in").write_bytes(case_text(nums).encode("utf-8"))
    # .out：末尾恰好一个换行符
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(pivot_index(nums)) + "\n")


def build_big_with_pivot():
    """构造大数据且确定有解：A + [x] + A，左右两半完全相同，中心落在中间下标。"""
    half = 4999
    A = [RNG.randint(V_LO, V_HI) for _ in range(half)]
    nums = A + [RNG.randint(V_LO, V_HI)] + A
    assert len(nums) == 2 * half + 1
    return nums


def build_big_no_pivot():
    """构造大数据且确定无解：反复随机直到基准解判定不存在中心下标。"""
    for _ in range(500):
        nums = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]
        if pivot_index(nums) == -1:
            return nums
    raise SystemExit("未能构造出无解的大数据")


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    # (nums, 规模/分布, 目标, 卡掉的错误解)
    plan = [
        ([1, 7, 3, 6, 5, 6], "样例，$n=6$",
         "展示中心下标 $3$（左侧 $1+7+3=11$，右侧 $5+6=11$）", "漏算下标 $3$"),
        ([1, 2, 3], "样例，$n=3$",
         "无解，输出 $-1$", "强行输出某个下标"),
        ([2, 1, -1], "样例，$n=3$",
         "中心下标在最左端 $0$（右侧 $1+(-1)=0$）", "误以为下标 $0$ 不可能成立"),
        ([5], "最小规模 $n=1$",
         "左右两侧都视为 $0$，答案 $0$", "$n<2$ 就直接输出 $-1$"),
        ([1, 1], "$n=2$",
         "无解 $-1$：$i=0$ 右侧为 $1$，$i=1$ 左侧为 $1$，都不相等", "公式漏减当前元素"),
        ([0] * 6, "全 $0$，$n=6$",
         "每个下标都是中心下标，必须取最靠左的 $0$", "从右往左扫描会取到 $5$"),
        ([1, -1, 5], "中心下标在最右端，$n=3$",
         "答案 $2$（左侧 $1+(-1)=0$，右侧视为 $0$）", "漏判 $i=n-1$"),
        ([1, 1, 1, 1], "hack 组，$n=4$",
         "正确答案 $-1$（没有任何下标两侧相等）",
         "把前缀和算成「含当前元素」的错解会在下标 $1$ 处误判成立"),
        (build_big_with_pivot(), "$n=9999$，左右两半完全相同",
         "压测 $O(n)$，答案落在中间下标 $4999$", "$O(n^2)$ 逐下标重算两侧和会超时"),
        (build_big_no_pivot(), "$n=10000$，值域 $[-1000,1000]$ 随机",
         "压测读入与无解分支，答案 $-1$", "$O(n^2)$ 逐下标重算两侧和会超时"),
    ]
    assert len(plan) == 10

    for idx, (nums, _, _, _) in enumerate(plan, 1):
        write_case(idx, nums)

    # ---- 生成后自校验 ----
    for i in range(1, 11):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob, f"{i}.out 换行规则不符"

        lines = ib.decode("utf-8").split("\n")
        n = int(lines[0])
        nums = list(map(int, lines[1].split()))
        assert len(nums) == n, f"{i}.in 第二行元素个数与 n 不符"
        assert 1 <= n <= N_MAX and all(V_LO <= x <= V_HI for x in nums), f"{i}.in 超出题面约束"
        assert (str(pivot_index(nums)) + "\n").encode("utf-8") == ob, f"{i}.out 与基准解不一致"
        assert brute_pivot(nums) == pivot_index(nums), f"{i} 基准解与独立暴力不一致"

    # 关键样例期望值锁定
    assert pivot_index([1, 7, 3, 6, 5, 6]) == 3
    assert pivot_index([1, 2, 3]) == -1
    assert pivot_index([2, 1, -1]) == 0
    assert pivot_index([5]) == 0
    assert pivot_index([0] * 6) == 0
    assert pivot_index([1, -1, 5]) == 2
    assert pivot_index([1, 1, 1, 1]) == -1

    readme = [
        "# P7119 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 两行：第一行 `n`，第二行 `n` 个整数（空格分隔）。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        readme.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme += [
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后已用基准解（`gen.py` 内 `pivot_index`）对 10 组全部复算比对，",
        "并与独立暴力实现 `brute_pivot`（逐下标分别求左右两侧和）交叉校验一致。",
        "第 9、10 组的构造方式：第 9 组用「左半 + 中间 + 右半相同」保证必有解且中心在中间；",
        "第 10 组随机生成后用基准解确认无解再落盘。",
        "",
    ]
    (DATA / "README.md").write_text("\n".join(readme), encoding="utf-8")

    print("P7119 data ok:", [pivot_index(c[0]) for c in plan])


if __name__ == "__main__":
    main()
