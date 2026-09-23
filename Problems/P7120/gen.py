# -*- coding: utf-8 -*-
"""P7120 造数：找出 3 位偶数（ACM 模式，stdin 两行：n，然后 n 个数字）。

10 组数据：前 8 组小数据（样例 / 边界 / 多重集 / hack），后 2 组大数据压满 n=100。
写文件规则：`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
输出格式：第一行 k；若 k>0 再输出一行递增排列的 k 个数；若 k=0 只输出一行 0。
"""
from __future__ import annotations

import random
import sys
from itertools import permutations
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712020260914)

N_MIN, N_MAX = 3, 100


def three_digit_evens(digits):
    """基准解：统计每个数字的出现次数，按百位->十位->个位从小到大枚举并扣次数。"""
    cnt = [0] * 10
    for d in digits:
        cnt[d] += 1
    res = []
    for a in range(1, 10):
        if cnt[a] == 0:
            continue
        cnt[a] -= 1
        for b in range(10):
            if cnt[b] == 0:
                continue
            cnt[b] -= 1
            for c in (0, 2, 4, 6, 8):
                if cnt[c] == 0:
                    continue
                res.append(a * 100 + b * 10 + c)
            cnt[b] += 1
        cnt[a] += 1
    return res


def brute_three_digit_evens(digits):
    """独立暴力：枚举三个不同下标的全排列，用集合去重后排序。"""
    n = len(digits)
    seen = set()
    for i, j, k in permutations(range(n), 3):
        a, b, c = digits[i], digits[j], digits[k]
        if a == 0:          # 不能有前导零
            continue
        if c % 2 != 0:      # 必须是偶数
            continue
        seen.add(a * 100 + b * 10 + c)
    return sorted(seen)


def case_in_text(digits):
    return str(len(digits)) + "\n" + " ".join(str(x) for x in digits)


def case_out_text(res):
    if not res:
        return "0\n"
    return str(len(res)) + "\n" + " ".join(str(x) for x in res) + "\n"


def write_case(idx, digits):
    assert N_MIN <= len(digits) <= N_MAX, (idx, len(digits))
    assert all(0 <= d <= 9 for d in digits), idx
    # .in：最后一行数据后不留换行符
    (DATA / f"{idx}.in").write_bytes(case_in_text(digits).encode("utf-8"))
    # .out：末尾恰好一个换行符
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(case_out_text(three_digit_evens(digits)))


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    # (digits, 规模/分布, 目标, 卡掉的错误解)
    plan = [
        ([2, 1, 3, 0], "样例 1，$n=4$",
         "输出 $k=10$ 与 $102$ 起的 10 个数", "漏掉含 $0$ 的组合或忘记去重"),
        ([2, 2, 8, 8, 2], "样例 2，$n=5$，含重复数字",
         "输出 $k=7$，同一个数字可按出现次数重复使用", "把重复数字当成只能用一次"),
        ([3, 7, 5], "样例 3，$n=3$，全为奇数",
         "无解，只输出一行 $0$", "无解时多输出一个空行或输出 $k=0$ 后还打第二行"),
        ([0, 0, 0], "边界，$n=3$，全为 $0$",
         "无解，只输出一行 $0$", "没排除前导零，误判出 $000$"),
        ([0, 2, 4], "边界，$n=3$，含一个 $0$",
         "恰有 $204,240,402,420$ 四个", "把 $024$、$042$ 这类前导零数字也算进去"),
        ([2, 2, 2], "多重集，三个相同的数字",
         "只有 $222$ 一个", "同一个下标被重复使用，或误判成多个"),
        ([2, 2, 3], "部分重复，$n=3$",
         "恰有 $232,322$ 两个", "只用一次 $2$，漏掉 $322$ 这类需要两个 $2$ 的数"),
        ([0, 0, 2, 4, 6], "hack 组，$n=5$，两个 $0$",
         "统计出全部合法三位偶数",
         "重复的 $0$ 只算一次会少算（$200$/$400$/$600$ 这类需要两个 $0$）"),
        ([0] * 30 + [2] * 12 + [4] * 6 + [8] * 2, "较大且数字稀缺，$n=50$：只有 $0,2,4,8$，且 $8$ 仅 $2$ 个",
         "与暴力枚举对拍；用掉三位数时受每个数字出现次数限制",
         "把「每个数字最多用一次」当成约束会大幅少算；漏判需要三个 $8$ 的组合"),
        ([d for d in range(10) for _ in range(10)], "压满，$n=100$，每个数字各 $10$ 个",
         "结果数量最大的情形，压测枚举与输出", "输出格式错误或结果未递增"),
    ]
    assert len(plan) == 10

    for idx, (digits, _, _, _) in enumerate(plan, 1):
        write_case(idx, digits)

    # ---- 生成后自校验 ----
    for i in range(1, 11):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob, f"{i}.out 换行规则不符"

        lines = ib.decode("utf-8").split("\n")
        n = int(lines[0])
        digits = list(map(int, lines[1].split()))
        assert len(digits) == n, f"{i}.in 第二行元素个数与 n 不符"
        assert N_MIN <= n <= N_MAX and all(0 <= d <= 9 for d in digits), f"{i}.in 超出题面约束"

        res = three_digit_evens(digits)
        # 基准解复算必须与写出的 .out 一致
        assert case_out_text(res).encode("utf-8") == ob, f"{i}.out 与基准解不一致"
        # 递增且无重复
        assert res == sorted(set(res)), f"{i} 结果未递增或存在重复"
        # 与独立暴力交叉校验
        assert brute_three_digit_evens(digits) == res, f"{i} 基准解与暴力不一致"

    # 题面三组样例的输出锁定
    assert case_out_text(three_digit_evens([2, 1, 3, 0])) == \
        "10\n102 120 130 132 210 230 302 310 312 320\n"
    assert case_out_text(three_digit_evens([2, 2, 8, 8, 2])) == \
        "7\n222 228 282 288 822 828 882\n"
    assert case_out_text(three_digit_evens([3, 7, 5])) == "0\n"

    readme = [
        "# P7120 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 两行：第一行 `n`，第二行 `n` 个数字（`0`~`9`，空格分隔）。",
        "输出：第一行 `k`；若 `k>0` 再输出一行递增排列的 `k` 个数；若 `k=0` 只输出一行 `0`。",
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
        "生成后已用基准解（`gen.py` 内 `three_digit_evens`）对 10 组全部复算比对，",
        "并与独立暴力实现 `brute_three_digit_evens`（枚举三个不同下标的全排列后集合去重）",
        "交叉校验一致；同时校验了每组结果严格递增且无重复。",
        "",
    ]
    (DATA / "README.md").write_text("\n".join(readme), encoding="utf-8")

    print("P7120 data ok:", [len(three_digit_evens(c[0])) for c in plan])


if __name__ == "__main__":
    main()
