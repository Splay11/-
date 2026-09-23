# -*- coding: utf-8 -*-
"""P5437 连窗日均：10 组测例（四级 I/O：g 组，每组 m / w / 逗号分隔净值）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import max_floor_avg  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(543720260913)


def brute(vals: list[int], w: int) -> int:
    n = len(vals)
    best = -10**18
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += vals[r]
            leng = r - l + 1
            if leng >= w:
                best = max(best, s // leng)
    return best


def wrong_exact_len(vals: list[int], w: int) -> int:
    n = len(vals)
    s = sum(vals[:w])
    best = s // w
    for i in range(w, n):
        s += vals[i] - vals[i - w]
        best = max(best, s // w)
    return best


def wrong_max_sum(vals: list[int], w: int) -> int:
    n = len(vals)
    best_s = -10**18
    best_len = w
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += vals[r]
            leng = r - l + 1
            if leng >= w and s > best_s:
                best_s = s
                best_len = leng
    return best_s // best_len


def toward_zero_div(s: int, k: int) -> int:
    if s >= 0:
        return s // k
    return -((-s) // k)


def wrong_toward_zero(vals: list[int], w: int) -> int:
    n = len(vals)
    best = -10**18
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += vals[r]
            leng = r - l + 1
            if leng >= w:
                best = max(best, toward_zero_div(s, leng))
    return best


def write_in(path: Path, text: str) -> None:
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, answers: list[int]) -> None:
    path.write_bytes((" ".join(str(x) for x in answers) + "\n").encode("utf-8"))


def fmt_case(groups: list[tuple[int, list[int]]]) -> str:
    lines = [str(len(groups))]
    for w, vals in groups:
        lines.append(str(len(vals)))
        lines.append(str(w))
        lines.append(",".join(str(x) for x in vals))
    return "\n".join(lines)


def solve_groups(groups: list[tuple[int, list[int]]]) -> list[int]:
    return [max_floor_avg(vals, w) for w, vals in groups]


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
    text = """# P5437 测例说明

四级输入：首行 $g$，每组三行（$m$、$w$、逗号分隔净值）。输出一行 $g$ 个空格分隔整数。
`.in` 末行后无换行；`.out` 一行答案后恰有一个换行。

分层（每组 10 分）：

- 1：四级样例。三组，答案 `4 -5 4`。覆盖正数最优短窗、全负、强制整段。
- 2：最小规模。$m=1,w=1$，净值 $0$。
- 3：全正且 $w=1$，答案等于全局最大值。
- 4：全负，较短窗口更优。
- 5：边界 $w=m$，只能取整段。
- 6：小随机两组，含零与正负混合，与暴力对拍。
- 7：hack。`100,-50,-50,100` 且 $w=3$ 卡「只查恰好长度 $w$」；`-5,-4` 且 $w=2$ 卡向零取整。
- 8：hack。`1,1,1,1,100` 且 $w=2$ 卡「先最大化区间和再相除」。
- 9：大数据。$m=10^5$ 随机，$|v_p|\\le 10^9$，压测 $O(m\\log V)$ 与 64 位前缀。
- 10：大数据 hack。开头 `100,-50,-50,100`，其余 $-10^9$，$w=3$。只查长度恰好为 $3$ 得到 $0$，正解为 $25$。

hack 点：只取长度恰好为 $w$、最大化区间和、负数向零取整、`int` 溢出、$O(m^2)$ 枚举。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def rand_arr(n: int, lo: int, hi: int) -> list[int]:
    return [RNG.randint(lo, hi) for _ in range(n)]


def make_cases() -> list[list[tuple[int, list[int]]]]:
    cases: list[list[tuple[int, list[int]]]] = []
    # 1 样例
    cases.append(
        [
            (2, [4, -1, 8, -6, 3, 5]),
            (2, [-2, -9, -4]),
            (4, [10, -1, -1, 10]),
        ]
    )
    # 2 最小
    cases.append([(1, [0])])
    # 3 全正 w=1
    cases.append([(1, [2, 5, 9, 4])])
    # 4 全负，短窗更优
    cases.append([(2, [-1, -2, -100])])
    # 5 w=m
    cases.append([(5, [8, -3, -3, 8, 1])])
    # 6 小随机
    cases.append(
        [
            (3, rand_arr(12, -20, 20)),
            (1, [0, 0, 5, -2, 0]),
        ]
    )
    # 7 exact-L + toward-zero
    cases.append(
        [
            (3, [100, -50, -50, 100]),
            (2, [-5, -4]),
        ]
    )
    # 8 max-sum greedy
    cases.append([(2, [1, 1, 1, 1, 100])])
    # 9 满规模随机
    cases.append([(50000, rand_arr(100000, -10**9, 10**9))])
    # 10 大数据 hack：开头 100,-50,-50,100，其余 -1e9，w=3
    # 只查长度恰好为 3 得到 0，真正最优是这四个的均值 25
    n = 100000
    arr10 = [100, -50, -50, 100] + [-(10**9)] * (n - 4)
    cases.append([(3, arr10)])
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10

    for _ in range(80):
        n = RNG.randint(1, 12)
        w = RNG.randint(1, n)
        vals = rand_arr(n, -20, 20)
        a = max_floor_avg(vals, w)
        b = brute(vals, w)
        if a != b:
            raise SystemExit(f"对拍失败 vals={vals} w={w} bin={a} brute={b}")

    # 确认 hack 真能打偏
    h1, w1 = [100, -50, -50, 100], 3
    if wrong_exact_len(h1, w1) == max_floor_avg(h1, w1):
        raise SystemExit("exact-L hack 无效")
    h2, w2 = [-5, -4], 2
    if wrong_toward_zero(h2, w2) == max_floor_avg(h2, w2):
        raise SystemExit("toward-zero hack 无效")
    h3, w3 = [1, 1, 1, 1, 100], 2
    if wrong_max_sum(h3, w3) == max_floor_avg(h3, w3):
        raise SystemExit("max-sum hack 无效")

    for i, groups in enumerate(cases, 1):
        for w, vals in groups:
            if not (1 <= w <= len(vals) <= 10**5):
                raise SystemExit(f"非法规模 case {i}: n={len(vals)} w={w}")
            for x in vals:
                if abs(x) > 10**9:
                    raise SystemExit(f"净值越界 case {i}: {x}")
        answers = solve_groups(groups)
        total_n = sum(len(v) for _, v in groups)
        if total_n <= 30:
            for w, vals in groups:
                br = brute(vals, w)
                got = max_floor_avg(vals, w)
                if br != got:
                    raise SystemExit(f"自校验失败 {i}: {got} vs brute {br}")
        raw = fmt_case(groups)
        write_in(DATA / f"{i}.in", raw)
        write_out(DATA / f"{i}.out", answers)
        if i == 10 and answers != [25]:
            raise SystemExit(f"case 10 期望 25，实际 {answers}")
        if i == 7:
            if answers[0] != 25 or answers[1] != -5:
                raise SystemExit(f"case 7 期望 25 -5，实际 {answers}")
        if i == 8 and answers != [50]:
            raise SystemExit(f"case 8 期望 50，实际 {answers}")

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
