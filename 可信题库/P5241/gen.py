# -*- coding: utf-8 -*-
"""P5241 造数：可抢占单核优先级调度。"""
from __future__ import annotations

import heapq
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5241)

Case = Tuple[List[int], List[int], List[int]]


def finish_times(arrival: List[int], duration: List[int], priority: List[int]) -> List[int]:
    n = len(arrival)
    rem = duration[:]
    ans = [-1] * n
    order = sorted(range(n), key=lambda i: (arrival[i], i))
    ready: List[tuple] = []
    time = 0
    i = 0
    cur = None
    while i < n or ready or cur is not None:
        if cur is None and not ready:
            if i >= n:
                break
            time = max(time, arrival[order[i]])
        while i < n and arrival[order[i]] <= time:
            idx = order[i]
            heapq.heappush(ready, (-priority[idx], idx))
            i += 1
        if cur is not None:
            if ready and (ready[0][0], ready[0][1]) < (-priority[cur], cur):
                heapq.heappush(ready, (-priority[cur], cur))
                cur = heapq.heappop(ready)[1]
        else:
            if not ready:
                continue
            cur = heapq.heappop(ready)[1]
        next_arr = arrival[order[i]] if i < n else None
        finish = time + rem[cur]
        if next_arr is not None and next_arr < finish:
            rem[cur] -= next_arr - time
            time = next_arr
        else:
            time = finish
            ans[cur] = time
            rem[cur] = 0
            cur = None
    return ans


def fmt_arr(a: List[int]) -> str:
    if not a:
        return "[]"
    return "[" + ", ".join(str(x) for x in a) + "]"


def write_case(idx: int, arrival: List[int], duration: List[int], priority: List[int]) -> None:
    n = len(arrival)
    assert 1 <= n <= 10**4
    assert len(duration) == n and len(priority) == n
    for i in range(n):
        assert 0 <= arrival[i] <= 10**9
        assert 1 <= duration[i] <= 10**4
        assert 1 <= priority[i] <= 10**9
    text_in = fmt_arr(arrival) + "\n" + fmt_arr(duration) + "\n" + fmt_arr(priority)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    out = fmt_arr(finish_times(arrival, duration, priority))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def gen_random(n: int, t_span: int, d_max: int, p_max: int) -> Case:
    arrival = [RNG.randint(0, t_span) for _ in range(n)]
    duration = [RNG.randint(1, d_max) for _ in range(n)]
    priority = [RNG.randint(1, p_max) for _ in range(n)]
    return arrival, duration, priority


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Case] = []

    # 1-2: 题面样例
    cases.append(([0, 1, 2], [3, 1, 2], [1, 2, 1]))
    cases.append(([0], [5], [1]))

    # 3: 无抢占，按到达顺序
    cases.append(([0, 10, 20], [2, 2, 2], [1, 1, 1]))

    # 4: 高优先级后到立刻抢占
    cases.append(([0, 1], [10, 1], [1, 100]))

    # 5: 同优先级选更小下标
    cases.append(([0, 0, 0], [1, 1, 1], [5, 5, 5]))

    # 6: 空闲空隙
    cases.append(([0, 100], [5, 3], [1, 2]))

    # 7: 多次抢占
    cases.append(([0, 1, 2, 3], [10, 2, 2, 2], [1, 2, 3, 4]))

    # 8: 中等
    cases.append(gen_random(200, 10**6, 50, 100))

    # 9: 近上限 n，中等 duration
    cases.append(gen_random(10000, 10**9, 20, 10**9))

    # 10: 近上限，较大 duration 总和压力
    cases.append(gen_random(10000, 10**5, 100, 1000))

    assert len(cases) == 10
    assert finish_times(*cases[0]) == [4, 2, 6]
    assert finish_times(*cases[1]) == [5]

    for i, c in enumerate(cases, 1):
        write_case(i, *c)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        assert len(lines) == 3
        a, d, p = eval(lines[0]), eval(lines[1]), eval(lines[2])
        got = fmt_arr(finish_times(a, d, p)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().count(b"\n") == 1

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 三行：arrival / duration / priority。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    print("P5241 data ok:", [finish_times(*c) for c in cases[:3]])


if __name__ == "__main__":
    main()
