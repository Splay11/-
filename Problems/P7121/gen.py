# -*- coding: utf-8 -*-
"""P7121 造数：找出数组中的第 k 大整数（ACM 模式，stdin 两行）。

10 组数据：前 8 组小数据（样例 / 边界 / 整数溢出 / 重复名次 hack），后 2 组大数据。
写文件规则：`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712120260914)

N_MAX = 10 ** 4
LEN_MAX = 100


def kth_largest(nums, k):
    """基准解：按 (长度, 字符串) 倒序排序，取第 k-1 个（不转整数，避免超出 64 位）。"""
    ordered = sorted(nums, key=lambda s: (len(s), s), reverse=True)
    return ordered[k - 1]


def brute_kth_largest(nums, k):
    """独立暴力：用 Python 大整数比较（int 无 64 位限制），与字符串比较法互为独立实现。"""
    return sorted(nums, key=lambda s: int(s), reverse=True)[k - 1]


def rand_num(max_len):
    """生成一个不含前导零的非负整数字符串，长度在 1..max_len 之间。"""
    length = RNG.randint(1, max_len)
    if length == 1:
        return str(RNG.randint(0, 9))          # 允许单个 "0"
    first = str(RNG.randint(1, 9))             # 首位非 0，保证无前导零
    rest = "".join(str(RNG.randint(0, 9)) for _ in range(length - 1))
    return first + rest


def case_in_text(nums, k):
    return f"{len(nums)} {k}\n" + " ".join(nums)


def write_case(idx, nums, k):
    assert 1 <= len(nums) <= N_MAX, (idx, len(nums))
    assert 1 <= k <= len(nums), (idx, k)
    for s in nums:
        assert 1 <= len(s) <= LEN_MAX, (idx, s)
        assert s.isdigit(), (idx, s)
        assert s == "0" or not s.startswith("0"), (idx, s)   # 不含前导零
    # .in：最后一行数据后不留换行符
    (DATA / f"{idx}.in").write_bytes(case_in_text(nums, k).encode("utf-8"))
    # .out：末尾恰好一个换行符
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(kth_largest(nums, k) + "\n")


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    # (nums, k, 规模/分布, 目标, 卡掉的错误解)
    plan = [
        (["3", "6", "7", "10"], 4, "样例 1，$n=4,\\ k=4$",
         "降序为 $10,7,6,3$，答案 $3$", "漏掉长度优先，把 $3$ 当成最大"),
        (["2", "21", "12", "1"], 3, "样例 2，$n=4,\\ k=3$",
         "降序为 $21,12,2,1$，答案 $2$", "按字典序排会得到 $2,21,12,1$ 的错误顺序"),
        (["0", "0"], 2, "样例 3，$n=2,\\ k=2$，全为 $0$",
         "重复元素各自占名次，答案 $0$", "先去重再排名，$k$ 越界"),
        (["0"], 1, "最小规模 $n=1$，值为 $0$",
         "答案 $0$", "把 $0$ 当成非法输入"),
        (["9" * 100], 1, "最大长度：单个 $100$ 位数",
         "答案就是它本身", "$100$ 位无法转成 $64$ 位整数"),
        (["9", "10"], 1, "hack 组：长度优先，$n=2,\\ k=1$",
         "答案 $10$（数值上 $10>9$）",
         "按字典序排会认为 $\\texttt{\"9\"} > \\texttt{\"10\"}$，错答 $9$"),
        (["10000000000000000000", "10000000000000000001"], 1,
         "hack 组：$20$ 位数，超出 $64$ 位整数范围",
         "答案 $10000000000000000001$",
         "转成 $\\texttt{long long}$/$\\texttt{long}$ 会溢出或报错，比较结果错乱"),
        (["123", "124", "125", "125"], 2, "hack 组：长度相同 + 重复元素，$k=2$",
         "降序为 $125,125,124,123$，答案 $125$",
         "同长度下不按字典序比会乱序；先去重会让名次错位"),
        ([rand_num(10) for _ in range(1000)], 500, "随机，$n=1000$，长度 $1\\sim10$",
         "与暴力大整数比较对拍", "排序方向写反或下标差 $1$"),
        ([rand_num(LEN_MAX) for _ in range(N_MAX)], 2500,
         "压满，$n=10000$，长度 $1\\sim100$",
         "压测排序与字符串比较", "转整数溢出；比较器不满足严格弱序导致排序结果错误"),
    ]
    assert len(plan) == 10

    for idx, (nums, k, _, _, _) in enumerate(plan, 1):
        write_case(idx, nums, k)

    # ---- 生成后自校验 ----
    for i in range(1, 11):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob, f"{i}.out 换行规则不符"
        assert ob.count(b"\n") == 1, f"{i}.out 应只有一行"

        lines = ib.decode("utf-8").split("\n")
        n, k = map(int, lines[0].split())
        nums = lines[1].split()
        assert len(nums) == n, f"{i}.in 第二行元素个数与 n 不符"
        assert 1 <= k <= n <= N_MAX, f"{i}.in k/n 越界"
        for s in nums:
            assert 1 <= len(s) <= LEN_MAX and s.isdigit(), f"{i}.in 元素非法"
            assert s == "0" or not s.startswith("0"), f"{i}.in 含前导零"

        # 基准解复算 == 写出的 .out
        assert (kth_largest(nums, k) + "\n").encode("utf-8") == ob, f"{i}.out 与基准解不一致"
        # 与独立大整数比较对拍
        assert brute_kth_largest(nums, k) == kth_largest(nums, k), f"{i} 与暴力大整数比较不一致"

    # 题面三组样例输出锁定
    assert kth_largest(["3", "6", "7", "10"], 4) == "3"
    assert kth_largest(["2", "21", "12", "1"], 3) == "2"
    assert kth_largest(["0", "0"], 2) == "0"

    readme = [
        "# P7121 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 两行：第一行 `n k`，第二行 `n` 个不含前导零的非负整数字符串（空格分隔）。",
        "输出：一行，第 `k` 大整数对应的字符串。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        readme.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme += [
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后已用基准解（`gen.py` 内 `kth_largest`，按「长度 + 字典序」倒序）对 10 组全部复算比对，",
        "并与独立暴力实现 `brute_kth_largest`（用 Python 大整数 `int` 比较，无 64 位限制）",
        "交叉校验一致。",
        "",
    ]
    (DATA / "README.md").write_text("\n".join(readme), encoding="utf-8")

    print("P7121 data ok:", [kth_largest(c[0], c[1]) for c in plan])


if __name__ == "__main__":
    main()
