# -*- coding: utf-8 -*-
"""P5453 造数：单车道停车调度。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(54533)


def run_ops(ops: List[str]) -> List[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    outs: List[str] = []
    obj = None
    for line in ops:
        if line.startswith("ParkingLane("):
            n = int(line[line.find("(") + 1 : line.find(")")])
            obj = std_mod.ParkingLane(n)
            outs.append("null")
        elif line.startswith("arrive("):
            a = int(line[7:-1])
            outs.append("true" if obj.arrive(a) else "false")
        elif line.startswith("admit("):
            outs.append("true" if obj.admit() else "false")
        elif line.startswith("depart("):
            a = int(line[7:-1])
            outs.append(str(obj.depart(a)))
        elif line.startswith("undo("):
            outs.append("true" if obj.undo() else "false")
        elif line.startswith("front("):
            outs.append(str(obj.front()))
        elif line.startswith("waiting("):
            outs.append(str(obj.waiting()))
        elif line.startswith("size("):
            outs.append(str(obj.size()))
        else:
            raise ValueError(line)
    return outs


def rand_ops(cap: int, steps: int) -> List[str]:
    ops = [f"ParkingLane({cap})"]
    live = set()
    nxt = 1
    for _ in range(steps):
        op = RNG.choice(
            ["arrive", "arrive", "admit", "depart", "undo", "front", "waiting", "size"]
        )
        if op == "arrive":
            if RNG.random() < 0.7 or not live:
                cid = nxt
                nxt += 1
            else:
                cid = RNG.choice(list(live))
            ops.append(f"arrive({cid})")
            # approximate tracking not needed; std decides
            live.add(cid)
        elif op == "depart":
            if live and RNG.random() < 0.8:
                ops.append(f"depart({RNG.choice(list(live))})")
            else:
                ops.append(f"depart({RNG.randint(1, nxt + 5)})")
        elif op == "admit":
            ops.append("admit()")
        elif op == "undo":
            ops.append("undo()")
        elif op == "front":
            ops.append("front()")
        elif op == "waiting":
            ops.append("waiting()")
        else:
            ops.append("size()")
    return ops


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[str, List[str]]] = []
    cases.append(
        (
            "样例1",
            """ParkingLane(2)
arrive(1)
arrive(2)
arrive(3)
waiting()
size()
front()
depart(1)
front()
waiting()
admit()
front()
size()""".splitlines(),
        )
    )
    cases.append(
        (
            "样例2",
            """ParkingLane(1)
arrive(10)
arrive(20)
depart(10)
undo()
front()
waiting()""".splitlines(),
        )
    )
    cases.append(
        (
            "样例3",
            """ParkingLane(3)
arrive(5)
depart(6)
arrive(5)
undo()
size()
waiting()""".splitlines(),
        )
    )
    cases.append(
        (
            "空车道",
            [
                "ParkingLane(2)",
                "depart(1)",
                "admit()",
                "undo()",
                "front()",
                "waiting()",
                "size()",
            ],
        )
    )
    cases.append(
        (
            "深层 depart",
            [
                "ParkingLane(5)",
                "arrive(1)",
                "arrive(2)",
                "arrive(3)",
                "arrive(4)",
                "depart(1)",
                "front()",
                "depart(2)",
                "size()",
            ],
        )
    )
    cases.append(("中等随机", rand_ops(3, 80)))
    cases.append(("交互随机", rand_ops(5, 200)))
    cases.append(("撤销压力", rand_ops(4, 500)))
    cases.append(("大调用", rand_ops(50, 2000)))
    cases.append(("极限", rand_ops(500, 4000)))

    assert len(cases) == 10
    assert run_ops([x.strip() for x in cases[0][1] if x.strip()])[7] == "1"

    for i, (desc, ops) in enumerate(cases, 1):
        ops = [x.strip() for x in ops if x.strip()]
        outs = run_ops(ops)
        (DATA / f"{i}.in").write_bytes("\n".join(ops).encode("utf-8"))
        (DATA / f"{i}.out").write_bytes(("\n".join(outs) + "\n").encode("utf-8"))
        assert run_ops(ops) == outs
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")

    (DATA / "config.yaml").write_text(
        """type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.js
  - template.c
  - execute.sh
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
  - user.js
  - user.c
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
      - input: 1.in
        output: 1.out
      - input: 2.in
        output: 2.out
      - input: 3.in
        output: 3.out
      - input: 4.in
        output: 4.out
      - input: 5.in
        output: 5.out
      - input: 6.in
        output: 6.out
      - input: 7.in
        output: 7.out
      - input: 8.in
        output: 8.out
      - input: 9.in
        output: 9.out
      - input: 10.in
        output: 10.out
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
  - js
  - c
""",
        encoding="utf-8",
    )
    (DATA / "README.md").write_text(
        "stdin 为 ParkingLane 调用流，与题面样例同构。\n", encoding="utf-8"
    )
    print("P5453 gen ok")


if __name__ == "__main__":
    main()
