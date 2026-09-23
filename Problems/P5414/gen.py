# -*- coding: utf-8 -*-
"""P5414 挑选四件礼物：10 组测例。

前 8 组小数据（含样例、不足 4 件、恰好 4 件、并列字典序）；
后 2 组 n=2000，卡四重循环暴力。
"""
from __future__ import annotations

import random
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(541420260909)
CAP = 10000
NEED = 4


def pick_four(b: list[int], w: list[int]):
    n = len(b)
    if n < NEED:
        return None
    order = sorted(range(n), key=lambda i: b[i])
    bb = [b[i] for i in order]
    ww = [w[i] for i in order]
    mask = (1 << (CAP + 1)) - 1
    cur = [0] * (NEED + 1)
    cur[0] = 1
    suffix = [None] * (n + 1)
    suffix[n] = cur[:]
    for i in range(n - 1, -1, -1):
        nxt = cur[:]
        ww_i = ww[i]
        for k in range(NEED - 1, -1, -1):
            nxt[k + 1] = (nxt[k + 1] | (cur[k] << ww_i)) & mask
        cur = nxt
        suffix[i] = cur[:]
    bits = suffix[0][NEED]
    if bits == 0:
        return None
    remain_s = bits.bit_length() - 1
    remain_k = NEED
    ans = []
    for i in range(n):
        if remain_k == 0:
            break
        ns = remain_s - ww[i]
        nk = remain_k - 1
        if ns >= 0 and ((suffix[i + 1][nk] >> ns) & 1):
            ans.append(bb[i])
            remain_s = ns
            remain_k = nk
    return ans


def brute_four(b: list[int], w: list[int]):
    n = len(b)
    if n < NEED:
        return None
    best = None
    for comb in combinations(range(n), 4):
        ids = tuple(sorted(b[i] for i in comb))
        sm = sum(w[i] for i in comb)
        if sm > CAP:
            continue
        if best is None or sm > best[0] or (sm == best[0] and ids < best[1]):
            best = (sm, ids)
    return None if best is None else list(best[1])


def write_in(path: Path, b: list[int], w: list[int]) -> None:
    lines = [str(len(b))]
    for i in range(len(b)):
        lines.append(f"{b[i]} {w[i]}")
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans) -> None:
    if ans is None:
        text = "0\n"
    else:
        text = " ".join(str(x) for x in ans) + "\n"
    path.write_bytes(text.encode("utf-8"))


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 1s
memory: 256m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
  - js
  - go
"""
    (DATA / "config.yaml").write_bytes(config.encode("utf-8"))


def write_readme(notes: list[dict]) -> None:
    rows = [
        "| 组别 | 规模/分布 | 生成逻辑 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, note in enumerate(notes, 1):
        rows.append(f"| {i} | {note['scale']} | {note['logic']} | {note['hack']} |")
    text = (
        "# P5414 测试数据说明\n\n"
        "恰好选 $4$ 件，总价不超过 $10000$，总价尽量大；并列时编号升序后字典序最小。"
        "没有方案输出 $0$。\n\n"
        + "\n".join(rows)
        + "\n"
    )
    (DATA / "README.md").write_bytes(text.encode("utf-8"))


def unique_ids(n: int, low: int = 1, high: int = 10000) -> list[int]:
    return RNG.sample(range(low, high + 1), n)


def build_cases():
    cases = []
    notes = []

    cases.append(([1, 2, 3, 4, 5, 6], [100, 100, 8000, 1800, 1800, 1800]))
    notes.append(
        {
            "scale": "m=6，样例1",
            "logic": "三组总价都是 10000，字典序最小为 1 2 3 4",
            "hack": "并列时没比编号；输出未排序",
        }
    )

    cases.append(([1, 2, 3, 4, 5], [3000, 3000, 3000, 3000, 2000]))
    notes.append(
        {
            "scale": "m=5，样例2",
            "logic": "任意四件都超过 10000",
            "hack": "硬选最便宜的四件却超限仍输出；输出空行",
        }
    )

    cases.append(([9, 2, 5], [10, 20, 30]))
    notes.append(
        {
            "scale": "m=3，不足 4 件",
            "logic": "件数不够",
            "hack": "输出仅有的三件；输出 -1",
        }
    )

    cases.append(([20, 1, 7, 3], [2500, 2500, 2500, 2500]))
    notes.append(
        {
            "scale": "m=4，恰好 10000",
            "logic": "四件刚好顶满，输入编号无序",
            "hack": "按输入顺序输出编号",
        }
    )

    cases.append(([4, 1, 2, 3], [2501, 2500, 2500, 2500]))
    notes.append(
        {
            "scale": "m=4，和为 10001",
            "logic": "只有四件且超限，应输出 0",
            "hack": "忽略上限直接输出四件",
        }
    )

    b = [9, 1, 8, 3, 5, 2, 7, 4]
    w = [1] * 8
    cases.append((b, w))
    notes.append(
        {
            "scale": "m=8，售价全是 1",
            "logic": "总价都很小，应选编号最小的四件 1 2 3 4",
            "hack": "选了输入里最靠前的四件",
        }
    )

    cases.append(
        (
            [10, 2, 8, 3, 15, 4, 6],
            [4000, 2000, 2500, 1500, 1000, 3000, 2000],
        )
    )
    notes.append(
        {
            "scale": "m=7，多组可达上限",
            "logic": "存在总价 10000 的组合 2 3 8 10",
            "hack": "选了总价更小但编号更小的组；漏掉恰好 10000",
        }
    )

    b = unique_ids(12, 1, 40)
    w = [RNG.randint(100, 4000) for _ in range(12)]
    cases.append((b, w))
    notes.append(
        {
            "scale": "m=12，随机小数据",
            "logic": "随机编号与售价，用暴力对照",
            "hack": "四元组枚举漏剪枝导致选超限",
        }
    )

    b = unique_ids(2000)
    w = [RNG.randint(1, 8000) for _ in range(2000)]
    cases.append((b, w))
    notes.append(
        {
            "scale": "m=2000，随机",
            "logic": "满规模随机，压测背包与读入",
            "hack": "四重循环超时",
        }
    )

    b = unique_ids(2000)
    w = [RNG.randint(1, 50) for _ in range(2000)]
    cases.append((b, w))
    notes.append(
        {
            "scale": "m=2000，售价很小",
            "logic": "大量合法四元组，暴力组合数爆炸",
            "hack": "四重循环超时；只取前四件",
        }
    )

    return cases, notes


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases, notes = build_cases()
    if len(cases) != 10:
        raise SystemExit(f"需要 10 组，实际 {len(cases)}")

    for i, (b, w) in enumerate(cases, 1):
        m = len(b)
        if m < 1 or m > 2000:
            raise SystemExit(f"第 {i} 组 m={m}")
        if len(set(b)) != m:
            raise SystemExit(f"第 {i} 组编号重复")
        for x, y in zip(b, w):
            if not (1 <= x <= 10000 and 1 <= y <= 10000):
                raise SystemExit(f"第 {i} 组值越界")
        ans = pick_four(b, w)
        if m <= 20:
            brute = brute_four(b, w)
            if ans != brute:
                raise SystemExit(f"第 {i} 组与暴力不一致: {ans} vs {brute}")
        write_in(DATA / f"{i}.in", b, w)
        write_out(DATA / f"{i}.out", ans)

    write_config()
    write_readme(notes)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
        if raw.endswith("\n"):
            raise SystemExit(f"{i}.in 末尾多了换行")
        lines = raw.split("\n")
        m = int(lines[0])
        b, w = [], []
        for line in lines[1:]:
            x, y = map(int, line.split())
            b.append(x)
            w.append(y)
        if len(b) != m:
            raise SystemExit(f"{i}.in 行数不对")
        got = pick_four(b, w)
        out_raw = (DATA / f"{i}.out").read_bytes()
        if not out_raw.endswith(b"\n") or out_raw.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不对")
        text = out_raw.decode("utf-8").strip()
        if got is None:
            if text != "0":
                raise SystemExit(f"{i}.out 应为 0")
        else:
            if text.split() != list(map(str, got)):
                raise SystemExit(f"{i}.out 不一致")

    print("已生成 10 组测例并完成自校验")


if __name__ == "__main__":
    main()
