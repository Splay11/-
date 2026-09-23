# -*- coding: utf-8 -*-
"""P5240 造数：按类型滑动窗口限流。"""
from __future__ import annotations

import random
import shutil
from collections import defaultdict, deque
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5240)

Case = Tuple[List[List[int]], int, int]


def count_kept(events: List[List[int]], window: int, limit: int) -> int:
    dq = defaultdict(deque)
    kept = 0
    for t, typ in events:
        q = dq[typ]
        while q and q[0] <= t - window and q[0] < t:
            q.popleft()
        if len(q) < limit:
            q.append(t)
            kept += 1
    return kept


def fmt_events(events: List[List[int]]) -> str:
    # 紧凑 JSON，避免大测例 literal_eval/空白膨胀导致 Python MLE
    import json

    return json.dumps(events, separators=(",", ":"))


def write_case(idx: int, events: List[List[int]], window: int, limit: int) -> None:
    assert 0 <= len(events) <= 10**5
    assert 0 <= window <= 10**9
    assert 1 <= limit <= 10**5
    prev_t = None
    for e in events:
        assert len(e) == 2
        t, typ = e
        assert 0 <= t <= 10**9
        assert 1 <= typ <= 10**5
        if prev_t is not None:
            assert t >= prev_t
        prev_t = t
    text_in = fmt_events(events) + "\n" + str(window) + "\n" + str(limit)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(count_kept(events, window, limit)) + "\n")


def gen_sorted(n: int, n_types: int, t_span: int) -> List[List[int]]:
    ts = sorted(RNG.randint(0, t_span) for _ in range(n))
    return [[ts[i], RNG.randint(1, n_types)] for i in range(n)]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Case] = []

    # 1-3: 题面样例
    cases.append(([[1, 1], [2, 1], [3, 1], [10, 1]], 5, 2))
    cases.append(([[0, 2], [0, 2], [0, 3]], 0, 1))
    cases.append(([], 10, 3))

    # 4: 单事件
    cases.append(([[0, 1]], 0, 1))

    # 5: window=0 同刻 limit=2
    cases.append(([[5, 1], [5, 1], [5, 1], [6, 1]], 0, 2))

    # 6: 按类型隔离（异类型互不影响）
    cases.append(([[1, 1], [2, 2], [3, 1]], 10, 1))

    # 7: 恰在窗口边界：ts == t-window 应弹出
    cases.append(([[0, 1], [5, 1], [5, 1]], 5, 1))

    # 8: 中等随机
    cases.append((gen_sorted(500, 30, 10**6), 1000, 3))

    # 9/10: 大测例用 3e4，避免单行 JSON 解析在 OJ 内存限额下 MLE
    cases.append((gen_sorted(30000, 5, 10**9), 10**8, 2))
    cases.append((gen_sorted(30000, 30000, 10**9), 0, 5))

    assert len(cases) == 10
    assert count_kept(*cases[0]) == 3
    assert count_kept(*cases[1]) == 2
    assert count_kept(*cases[2]) == 0
    assert count_kept(*cases[5]) == 2  # 类型1保留1；类型2保留1；第三条类型1被抑
    assert count_kept(*cases[6]) == 2  # 0保留；5时0弹出可再保留一条；同刻第二条抑

    for i, (events, window, limit) in enumerate(cases, 1):
        write_case(i, events, window, limit)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        assert len(lines) == 3
        events = eval(lines[0])
        window = int(lines[1])
        limit = int(lines[2])
        got = str(count_kept(events, window, limit)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 三行：events / window / limit。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    print("P5240 data ok:", [count_kept(*c) for c in cases])


if __name__ == "__main__":
    main()
