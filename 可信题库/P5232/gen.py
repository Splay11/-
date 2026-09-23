# -*- coding: utf-8 -*-
"""P5232 造数：页式内存紧凑整理。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5232)


class MemMgmtSys:
    def __init__(self, num: int):
        self.n = num
        self.page = [-1] * num
        self.info = {}

    def _find(self, size: int) -> int:
        i = 0
        while i < self.n:
            if self.page[i] != -1:
                i += 1
                continue
            j = i
            while j < self.n and self.page[j] == -1:
                j += 1
            if j - i >= size:
                return i
            i = j
        return -1

    def _defrag(self) -> None:
        items = [(sz, pid) for pid, (_st, sz) in self.info.items()]
        items.sort()
        self.page = [-1] * self.n
        self.info.clear()
        used = sum(sz for sz, _ in items)
        pos = self.n - used
        for sz, pid in items:
            for k in range(sz):
                self.page[pos + k] = pid
            self.info[pid] = (pos, sz)
            pos += sz

    def processMemAlloc(self, processId: int, size: int) -> int:
        st = self._find(size)
        if st < 0:
            self._defrag()
            st = self._find(size)
            if st < 0:
                return -1
        for k in range(size):
            self.page[st + k] = processId
        self.info[processId] = (st, size)
        return st

    def processMemFree(self, processId: int) -> None:
        st, sz = self.info.pop(processId)
        for k in range(sz):
            self.page[st + k] = -1

    def processMemQuery(self, processId: int) -> int:
        return self.info[processId][0]


def simulate(ops: List[str]) -> List[str]:
    outs: List[str] = []
    obj = None
    for line in ops:
        if line.startswith("MemMgmtSys("):
            num = int(line[line.find("(") + 1 : -1])
            obj = MemMgmtSys(num)
            outs.append("null")
        elif line.startswith("processMemAlloc("):
            a, b = line[len("processMemAlloc(") : -1].split(",")
            outs.append(str(obj.processMemAlloc(int(a), int(b))))
        elif line.startswith("processMemFree("):
            pid = int(line[len("processMemFree(") : -1])
            obj.processMemFree(pid)
            outs.append("null")
        elif line.startswith("processMemQuery("):
            pid = int(line[len("processMemQuery(") : -1])
            outs.append(str(obj.processMemQuery(pid)))
        else:
            raise ValueError(line)
    return outs


def write_case(idx: int, ops: List[str]) -> None:
    text_in = "\n".join(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    outs = simulate(ops)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def rand_scenario(n: int, steps: int) -> List[str]:
    ops = [f"MemMgmtSys({n})"]
    alive = {}
    next_pid = 1
    for _ in range(steps):
        choice = RNG.random()
        if not alive or choice < 0.55:
            # alloc new
            pid = next_pid
            next_pid += 1
            size = RNG.randint(1, max(1, n // 3))
            # only add if not already (always new pid)
            ops.append(f"processMemAlloc({pid}, {size})")
            # tentatively track by re-sim would be heavy; just append and let invalid free skip
            alive[pid] = size  # may fail alloc; cleaned by resim filter below
        elif choice < 0.8 and alive:
            pid = RNG.choice(list(alive.keys()))
            ops.append(f"processMemFree({pid})")
            alive.pop(pid, None)
        elif alive:
            pid = RNG.choice(list(alive.keys()))
            ops.append(f"processMemQuery({pid})")
    # rebuild ops with only valid sequence via dry-run filter
    obj = MemMgmtSys(n)
    valid = [f"MemMgmtSys({n})"]
    live = set()
    for line in ops[1:]:
        if line.startswith("processMemAlloc("):
            a, b = line[len("processMemAlloc(") : -1].split(",")
            pid, size = int(a), int(b)
            if pid in live:
                continue
            r = obj.processMemAlloc(pid, size)
            valid.append(line)
            if r >= 0:
                live.add(pid)
        elif line.startswith("processMemFree("):
            pid = int(line[len("processMemFree(") : -1])
            if pid not in live:
                continue
            obj.processMemFree(pid)
            live.remove(pid)
            valid.append(line)
        else:
            pid = int(line[len("processMemQuery(") : -1])
            if pid not in live:
                continue
            obj.processMemQuery(pid)
            valid.append(line)
    return valid


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[str]] = []

    # 1-2 样例
    cases.append(
        [
            "MemMgmtSys(10)",
            "processMemAlloc(0, 3)",
            "processMemAlloc(10, 1)",
            "processMemAlloc(40, 2)",
            "processMemAlloc(30, 1)",
            "processMemAlloc(20, 2)",
            "processMemFree(10)",
            "processMemFree(30)",
            "processMemAlloc(50, 2)",
            "processMemQuery(0)",
        ]
    )
    cases.append(
        [
            "MemMgmtSys(8)",
            "processMemAlloc(50, 1)",
            "processMemAlloc(30, 1)",
            "processMemFree(50)",
            "processMemAlloc(20, 2)",
            "processMemAlloc(10, 3)",
            "processMemFree(20)",
            "processMemAlloc(40, 5)",
            "processMemQuery(10)",
            "processMemFree(30)",
            "processMemAlloc(40, 5)",
        ]
    )

    # 3: 无需整理即可填满
    cases.append(
        [
            "MemMgmtSys(5)",
            "processMemAlloc(1, 2)",
            "processMemAlloc(2, 3)",
            "processMemQuery(2)",
            "processMemFree(1)",
            "processMemAlloc(3, 2)",
        ]
    )

    # 4: 整理靠右 + 同页数按 id
    cases.append(
        [
            "MemMgmtSys(9)",
            "processMemAlloc(0, 2)",
            "processMemAlloc(40, 2)",
            "processMemAlloc(20, 2)",
            "processMemFree(40)",
            "processMemAlloc(50, 3)",
            "processMemQuery(0)",
            "processMemQuery(20)",
        ]
    )

    # 5: hack — 总空闲够但连续不够，必须整理
    cases.append(
        [
            "MemMgmtSys(6)",
            "processMemAlloc(1, 1)",
            "processMemAlloc(2, 1)",
            "processMemAlloc(3, 1)",
            "processMemFree(2)",
            "processMemAlloc(4, 2)",
            "processMemQuery(1)",
            "processMemQuery(3)",
        ]
    )

    # 6: hack — 总空闲不足也要整理
    cases.append(
        [
            "MemMgmtSys(4)",
            "processMemAlloc(1, 2)",
            "processMemAlloc(2, 1)",
            "processMemFree(1)",
            "processMemAlloc(3, 3)",
            "processMemQuery(2)",
        ]
    )

    # 7: 单页反复
    cases.append(
        [
            "MemMgmtSys(3)",
            "processMemAlloc(9, 1)",
            "processMemFree(9)",
            "processMemAlloc(8, 1)",
            "processMemAlloc(7, 2)",
            "processMemQuery(8)",
        ]
    )

    # 8: 中等随机
    cases.append(rand_scenario(32, 40))

    # 9-10: 大数据接近上限
    cases.append(rand_scenario(256, 200))
    cases.append(rand_scenario(256, 300))

    assert len(cases) == 10
    for i, ops in enumerate(cases, 1):
        write_case(i, ops)
        # 校验
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        got = "\n".join(simulate(raw.split("\n"))) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)

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
    with open(DATA / "config.yaml", "w", encoding="utf-8", newline="\n") as f:
        f.write(config)
    with open(DATA / "README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "主造数脚本：题目根 `gen.py`。\n"
            "hack：`5.in` 连续不足但总空闲够；`6.in` 总空闲不足仍须整理。\n"
            "9/10：`num=256` 压力。\n"
        )
    print("generated 10 cases OK")


if __name__ == "__main__":
    main()
