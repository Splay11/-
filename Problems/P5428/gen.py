# -*- coding: utf-8 -*-
"""P5428 作业限放最小耗时：10 组测例（二级 I/O：数组 / t / lim）。"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import is_empty, min_cost  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(542820260911)


def brute(arr: list[int], t: int, lim: int) -> int:
    n = len(arr)
    if n == 0:
        return 0
    if t == 0:
        return 0 if n <= lim else -1
    if t > n:
        return -1
    inf = 10**18
    best = inf
    for comb in itertools.combinations(range(n), t):
        if comb[0] > lim:
            continue
        if n - 1 - comb[-1] > lim:
            continue
        ok = True
        for i in range(1, t):
            if comb[i] - comb[i - 1] - 1 > lim:
                ok = False
                break
        if ok:
            s = sum(arr[i] for i in comb)
            if s < best:
                best = s
    return -1 if best >= inf else best


def write_in(path: Path, text: str) -> None:
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def fmt_case(arr: list[int], t: int, lim: int | None = None, *, empty: bool = False) -> str:
    if empty:
        return f"0\n{t}"
    line1 = " ".join(str(x) for x in arr)
    return f"{line1}\n{t}\n{lim}"


def parse_in(text: str) -> tuple[list[int], int, int]:
    lines = text.split("\n")
    arr = list(map(int, lines[0].split()))
    if is_empty(arr):
        return [], 0, 0
    t = int(lines[1])
    lim = int(lines[2])
    return arr, t, lim


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
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5428 测例说明

输入与二级题面一致：非空为三行（空格分隔数组、`t`、`lim`）；空队列为两行（`0` 与 `t`）。
`.in` 末行后无换行；`.out` 一个整数加一个换行。

分层（每组 10 分）：

- 1：二级样例 1。`n=7,t=2,lim=1` → `-1`。卡「接满 t 项就停、不管队尾」。
- 2：二级样例 2。`11 4 15 6 8`，`t=4,lim=3` → `29`。最优唯一，必须放掉 `15`。
- 3：二级样例 3。交替小数与大数，必须隔项接 → `16`。
- 4：二级样例 4。空队列哨兵 `0`，即使后面写了 `t` 也输出 `0`。
- 5：基础。`n=1,t=1`，接仅有的一项。
- 6：边界。`t=0` 且 `n<=lim`，全部放掉合法，答案 `0`。
- 7：边界。`t=n` 且 `lim=0`，必须全接。
- 8：hack 贪心。小值扎在左侧，受空隙限制不能只接最小的三项，卡「全局取 t 个最小」。
- 9：大数据。`n=1000` 随机，压测 `O(nt)` DP。
- 10：hack + 上限。`t=0` 且 `n=1000>lim`，卡「`t=0` 一律输出 0」。

hack 点：忽略队首/队尾放掉、贪心取最小、`t=0` 漏判、空队列、间隔 off-by-one。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def make_cases() -> list[tuple[str, int, str]]:
    # (raw_in, expected_or_None, note) expected computed later
    cases: list[tuple[list[int], int, int, bool]] = []
    # 1-4 样例
    cases.append(([9, 8, 7, 6, 11, 12, 10], 2, 1, False))
    cases.append(([11, 4, 15, 6, 8], 4, 3, False))
    cases.append(([4, 80, 4, 80, 4, 80, 4], 4, 2, False))
    cases.append(([], 4, 0, True))
    # 5 n=1
    cases.append(([7], 1, 0, False))
    # 6 t=0 且能全部放掉
    cases.append(([9, 8, 7], 0, 3, False))
    # 7 t=n lim=0 必须全接
    cases.append(([3, 9, 4, 8, 2], 5, 0, False))
    # 8 贪心失败：四个 1 扎堆，必须留下空隙，最优 1+1+50
    cases.append(([1, 1, 1, 1, 50, 50, 50], 3, 1, False))
    # 9 满规模随机
    n9 = 1000
    arr9 = [RNG.randint(1, 10000) for _ in range(n9)]
    t9 = 400
    lim9 = 2
    cases.append((arr9, t9, lim9, False))
    # 10 t=0 但 n>lim
    arr10 = [RNG.randint(1, 10000) for _ in range(1000)]
    cases.append((arr10, 0, 999, False))
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10

    # 小数据对拍
    for _ in range(80):
        n = RNG.randint(1, 10)
        arr = [RNG.randint(1, 20) for _ in range(n)]
        t = RNG.randint(0, n)
        lim = RNG.randint(0, n)
        a = min_cost(arr, t, lim)
        b = brute(arr, t, lim)
        if a != b:
            raise SystemExit(f"对拍失败 arr={arr} t={t} lim={lim} dp={a} brute={b}")

    for i, (arr, t, lim, empty) in enumerate(cases, 1):
        raw = fmt_case(arr, t, lim, empty=empty)
        parsed_arr, parsed_t, parsed_lim = parse_in(raw)
        if empty:
            ans = 0
        else:
            ans = min_cost(arr, t, lim)
            if len(arr) <= 12 and t <= 12:
                br = brute(arr, t, lim)
                if br != ans:
                    raise SystemExit(f"自校验失败：{i} dp={ans} brute={br}")
        if min_cost(parsed_arr, parsed_t, parsed_lim) != ans and not empty:
            raise SystemExit(f"parse 不一致：{i}")
        write_in(DATA / f"{i}.in", raw)
        write_out(DATA / f"{i}.out", ans)
        got = min_cost(parsed_arr, parsed_t, parsed_lim)
        if empty:
            got = 0
        if got != ans:
            raise SystemExit(f"自校验失败：{i}")
        assert 0 <= (0 if empty else len(arr)) <= 1000

    write_config()
    write_readme()
    print("generated 10 cases")
    for i, (arr, t, lim, empty) in enumerate(cases, 1):
        if empty:
            print(i, "empty", "->", 0)
        else:
            print(i, "n=", len(arr), "t=", t, "lim=", lim, "->", min_cost(arr, t, lim))


if __name__ == "__main__":
    main()
