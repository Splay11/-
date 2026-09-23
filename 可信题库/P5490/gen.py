# -*- coding: utf-8 -*-
"""P5490 造数：外卖格口墙。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5490)


class ParcelSlots:
    def __init__(self, n: int):
        self.n = n
        self.slot = [0] * n
        self.cnt = 0

    def put(self, i: int, w: int) -> bool:
        if i < 1 or i > self.n or w <= 0 or self.slot[i - 1] != 0:
            return False
        self.slot[i - 1] = w
        self.cnt += 1
        return True

    def take(self, i: int) -> int:
        if i < 1 or i > self.n or self.slot[i - 1] == 0:
            return 0
        w = self.slot[i - 1]
        self.slot[i - 1] = 0
        self.cnt -= 1
        return w

    def moveRight(self, i: int) -> bool:
        if i < 1 or i >= self.n or self.slot[i - 1] == 0 or self.slot[i] != 0:
            return False
        self.slot[i] = self.slot[i - 1]
        self.slot[i - 1] = 0
        return True

    def occupied(self) -> int:
        return self.cnt


def simulate(ops: List[str]) -> List[str]:
    obj = None
    outs: List[str] = []
    for line in ops:
        if line.startswith("ParcelSlots("):
            n = int(line[len("ParcelSlots(") : -1])
            obj = ParcelSlots(n)
            outs.append("null")
        elif line.startswith("put("):
            inner = line[4:-1]
            a, b = inner.split(",")
            outs.append("true" if obj.put(int(a), int(b)) else "false")
        elif line.startswith("take("):
            a = int(line[5:-1])
            outs.append(str(obj.take(a)))
        elif line.startswith("moveRight("):
            a = int(line[10:-1])
            outs.append("true" if obj.moveRight(a) else "false")
        elif line == "occupied()":
            outs.append(str(obj.occupied()))
        else:
            raise ValueError(line)
    return outs


def write_case(idx: int, ops: List[str]) -> None:
    assert 1 <= len(ops) <= 2000
    text_in = "\n".join(ops)
    outs = simulate(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def sample1() -> List[str]:
    return [
        "ParcelSlots(3)",
        "put(1, 5)",
        "put(1, 8)",
        "put(2, 0)",
        "put(3, 4)",
        "occupied()",
        "moveRight(1)",
        "take(2)",
        "take(2)",
        "moveRight(3)",
        "occupied()",
    ]


def sample2() -> List[str]:
    return [
        "ParcelSlots(1)",
        "put(2, 3)",
        "take(1)",
        "moveRight(1)",
        "put(1, 9)",
        "moveRight(1)",
        "occupied()",
    ]


def random_ops(n: int, q: int) -> List[str]:
    ops = [f"ParcelSlots({n})"]
    for _ in range(q):
        t = RNG.randint(0, 4)
        i = RNG.choice([RNG.randint(1, n), RNG.randint(-2, n + 3)])
        w = RNG.choice([RNG.randint(1, 100), 0, -1, RNG.randint(1, 10**4)])
        if t == 0:
            ops.append(f"put({i}, {w})")
        elif t == 1:
            ops.append(f"take({i})")
        elif t == 2:
            ops.append(f"moveRight({i})")
        else:
            ops.append("occupied()")
    return ops


def fill_then_shift(n: int) -> List[str]:
    """从左往右装满再试图右移，hack 覆盖占用格。"""
    ops = [f"ParcelSlots({n})"]
    for i in range(1, n + 1):
        ops.append(f"put({i}, {i})")
    ops.append("occupied()")
    for i in range(1, n + 1):
        ops.append(f"moveRight({i})")
    ops.append("occupied()")
    ops.append(f"take({n})")
    ops.append(f"moveRight({n - 1})")
    ops.append("occupied()")
    return ops


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[str]] = []

    cases.append(sample1())
    cases.append(sample2())

    # 3: 连续右移把餐送到最右
    cases.append(
        [
            "ParcelSlots(4)",
            "put(1, 7)",
            "moveRight(1)",
            "moveRight(2)",
            "moveRight(3)",
            "moveRight(4)",
            "occupied()",
            "take(4)",
            "occupied()",
        ]
    )

    # 4: 越界与负重量
    cases.append(
        [
            "ParcelSlots(2)",
            "put(0, 1)",
            "put(-1, 2)",
            "put(3, 2)",
            "put(1, -5)",
            "take(0)",
            "take(9)",
            "moveRight(0)",
            "occupied()",
        ]
    )

    # 5: 取出后再放入同一格
    cases.append(
        [
            "ParcelSlots(2)",
            "put(1, 10)",
            "take(1)",
            "put(1, 20)",
            "moveRight(1)",
            "take(2)",
            "occupied()",
        ]
    )

    # 6: 装满后右移全失败
    cases.append(fill_then_shift(5))

    # 7: 中等随机
    cases.append(random_ops(10, 80))

    # 8: 中等随机夹杂 occupied
    cases.append(random_ops(20, 120))

    # 9: 较大 n、较多调用
    cases.append(random_ops(200, 800))

    # 10: 压满调用上限附近，hack 计数维护错误
    cases.append(random_ops(200, 1800))

    assert len(cases) == 10
    assert simulate(cases[0])[-1] == "1"
    assert simulate(cases[1])[-1] == "1"

    for i, ops in enumerate(cases, 1):
        write_case(i, ops)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        ops = [ln for ln in raw.split("\n") if ln.strip() != ""]
        n = int(ops[0][len("ParcelSlots(") : -1])
        obj = std_mod.ParcelSlots(n)
        outs = ["null"]
        for line in ops[1:]:
            if line.startswith("put("):
                inner = line[4:-1]
                a, b = inner.split(",")
                outs.append("true" if obj.put(int(a), int(b)) else "false")
            elif line.startswith("take("):
                outs.append(str(obj.take(int(line[5:-1]))))
            elif line.startswith("moveRight("):
                outs.append("true" if obj.moveRight(int(line[10:-1])) else "false")
            elif line == "occupied()":
                outs.append(str(obj.occupied()))
        got = "\n".join(outs) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got[:80], exp[:80])
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
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
  - js
  - c
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 gen.py。stdin 为 ParcelSlots 调用流。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    exec_src = Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    shutil.copyfile(exec_src, DATA / "execute.sh")
    print("P5490 data ok")


if __name__ == "__main__":
    main()
