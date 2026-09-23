# -*- coding: utf-8 -*-
"""P5242 造数：区间预约停车场。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5242)


class ParkingLot:
    def __init__(self, n: int):
        self.n = n
        self.spots: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        self.car: Dict[int, Tuple[int, int, int]] = {}

    def _conflict(self, intervals: List[Tuple[int, int]], start: int, end: int) -> bool:
        for s, e in intervals:
            if start < e and s < end:
                return True
        return False

    def reserve(self, carId: int, start: int, end: int) -> int:
        if carId in self.car or start >= end:
            return -1
        for spot in range(self.n):
            if not self._conflict(self.spots[spot], start, end):
                self.spots[spot].append((start, end))
                self.car[carId] = (spot, start, end)
                return spot
        return -1

    def cancel(self, carId: int) -> bool:
        if carId not in self.car:
            return False
        spot, start, end = self.car.pop(carId)
        self.spots[spot].remove((start, end))
        return True

    def spotOf(self, carId: int) -> int:
        if carId not in self.car:
            return -1
        return self.car[carId][0]

    def busyCount(self, time: int) -> int:
        return sum(1 for _, s, e in self.car.values() if s <= time < e)


def simulate(ops: List[str]) -> List[str]:
    outs: List[str] = []
    obj = None
    for line in ops:
        if line.startswith("ParkingLot("):
            n = int(line[len("ParkingLot(") : -1])
            obj = ParkingLot(n)
            outs.append("null")
        elif line.startswith("reserve("):
            a, b, c = [int(x) for x in line[len("reserve(") : -1].split(",")]
            outs.append(str(obj.reserve(a, b, c)))
        elif line.startswith("cancel("):
            cid = int(line[len("cancel(") : -1])
            outs.append("true" if obj.cancel(cid) else "false")
        elif line.startswith("spotOf("):
            cid = int(line[len("spotOf(") : -1])
            outs.append(str(obj.spotOf(cid)))
        elif line.startswith("busyCount("):
            t = int(line[len("busyCount(") : -1])
            outs.append(str(obj.busyCount(t)))
        else:
            raise ValueError(line)
    return outs


def write_case(idx: int, ops: List[str]) -> None:
    assert 1 <= len(ops) <= 3000
    text_in = "\n".join(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    outs = simulate(ops)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def rand_scenario(n: int, steps: int, id_pool: int, t_span: int) -> List[str]:
    ops = [f"ParkingLot({n})"]
    active: Dict[int, Tuple[int, int, int]] = {}
    for _ in range(steps):
        choice = RNG.random()
        if choice < 0.45:
            cid = RNG.randint(1, id_pool)
            if cid in active and RNG.random() < 0.3:
                # 故意重复预约
                s = RNG.randint(0, t_span - 1)
                e = RNG.randint(s + 1, t_span)
                ops.append(f"reserve({cid}, {s}, {e})")
            else:
                # 新车或已取消后的车
                while cid in active:
                    cid = RNG.randint(1, id_pool)
                s = RNG.randint(0, t_span - 1)
                e = RNG.randint(s + 1, min(t_span, s + RNG.randint(1, max(2, t_span // 5))))
                ops.append(f"reserve({cid}, {s}, {e})")
                # 不本地模拟成功与否，交给 ParkingLot
                # 用影子对象同步
        elif choice < 0.6:
            if active and RNG.random() < 0.7:
                cid = RNG.choice(list(active.keys()))
            else:
                cid = RNG.randint(1, id_pool)
            ops.append(f"cancel({cid})")
        elif choice < 0.75:
            if active and RNG.random() < 0.7:
                cid = RNG.choice(list(active.keys()))
            else:
                cid = RNG.randint(1, id_pool)
            ops.append(f"spotOf({cid})")
        else:
            ops.append(f"busyCount({RNG.randint(0, t_span)})")

        # 用真实模拟刷新 active
        pl = ParkingLot(n)
        active.clear()
        for line in ops[1:]:
            if line.startswith("reserve("):
                a, b, c = [int(x) for x in line[len("reserve(") : -1].split(",")]
                sp = pl.reserve(a, b, c)
                if sp != -1:
                    active[a] = (sp, b, c)
            elif line.startswith("cancel("):
                cid = int(line[len("cancel(") : -1])
                if pl.cancel(cid):
                    active.pop(cid, None)
    assert len(ops) <= 3000
    return ops


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    sample1 = [
        "ParkingLot(2)",
        "reserve(1, 0, 10)",
        "reserve(2, 5, 15)",
        "reserve(3, 0, 6)",
        "busyCount(5)",
        "cancel(1)",
        "reserve(3, 0, 5)",
        "spotOf(3)",
        "busyCount(4)",
        "reserve(2, 0, 1)",
    ]
    assert simulate(sample1) == [
        "null", "0", "1", "-1", "2", "true", "0", "0", "1", "-1"
    ]

    cases: List[List[str]] = []
    cases.append(sample1)

    # 2: 单车位相邻半开可并排
    cases.append([
        "ParkingLot(1)",
        "reserve(1, 0, 5)",
        "reserve(2, 5, 10)",
        "busyCount(5)",
        "busyCount(4)",
        "cancel(1)",
        "spotOf(1)",
    ])

    # 3: 非法区间与重复预约
    cases.append([
        "ParkingLot(2)",
        "reserve(1, 5, 5)",
        "reserve(1, 0, 3)",
        "reserve(1, 10, 20)",
        "cancel(2)",
        "cancel(1)",
        "spotOf(1)",
    ])

    # 4: 最小编号偏好
    cases.append([
        "ParkingLot(3)",
        "reserve(1, 0, 10)",
        "reserve(2, 0, 10)",
        "reserve(3, 0, 10)",
        "reserve(4, 0, 10)",
        "cancel(2)",
        "reserve(5, 0, 10)",
        "spotOf(5)",
    ])

    # 5: busyCount 边界
    cases.append([
        "ParkingLot(1)",
        "reserve(1, 0, 1)",
        "busyCount(0)",
        "busyCount(1)",
        "cancel(1)",
        "busyCount(0)",
    ])

    # 6: 中等交错
    cases.append(rand_scenario(5, 40, 20, 100))

    # 7: 多车位碎片
    cases.append(rand_scenario(10, 80, 40, 200))

    # 8: 中等压力
    cases.append(rand_scenario(50, 200, 100, 1000))

    # 9: 近上限调用
    cases.append(rand_scenario(100, 800, 500, 10**6))

    # 10: 最大 n 与接近调用上限
    cases.append(rand_scenario(200, 2500, 1000, 10**9))

    assert len(cases) == 10
    for i, ops in enumerate(cases, 1):
        write_case(i, ops)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        ops = [ln for ln in raw.split("\n") if ln.strip() != ""]
        got = "\n".join(simulate(ops)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got[:200], exp[:200])
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

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
        "主造数脚本：题目根目录 `gen.py`。stdin 每行一次调用，首行 ParkingLot(n)。\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    print("P5242 data ok, sample outs:", simulate(sample1))


if __name__ == "__main__":
    main()
