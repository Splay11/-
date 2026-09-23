# -*- coding: utf-8 -*-
"""P5245 造数：TTL 缓存模拟。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(524520260815)


class TTLCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: Dict[int, Tuple[int, int]] = {}

    def put(self, key: int, value: int, expireAt: int) -> None:
        self.data[key] = (value, expireAt)
        if len(self.data) > self.capacity:
            victim = min(self.data.items(), key=lambda kv: (kv[1][1], kv[0]))[0]
            del self.data[victim]

    def get(self, key: int, now: int) -> int:
        if key not in self.data:
            return -1
        value, expireAt = self.data[key]
        if now >= expireAt:
            return -1
        return value

    def purge(self, now: int) -> int:
        dead = [k for k, (_, exp) in self.data.items() if now >= exp]
        for k in dead:
            del self.data[k]
        return len(dead)

    def size(self) -> int:
        return len(self.data)


def run_ops(ops: List[str]) -> List[str]:
    outs: List[str] = []
    obj: TTLCache | None = None
    for line in ops:
        if line.startswith("TTLCache("):
            cap = int(line[line.find("(") + 1 : line.find(")")])
            obj = TTLCache(cap)
            outs.append("null")
        elif line.startswith("put("):
            a, b, c = [int(x.strip()) for x in line[4:-1].split(",")]
            obj.put(a, b, c)
            outs.append("null")
        elif line.startswith("get("):
            a, b = [int(x.strip()) for x in line[4:-1].split(",")]
            outs.append(str(obj.get(a, b)))
        elif line.startswith("purge("):
            a = int(line[6:-1])
            outs.append(str(obj.purge(a)))
        elif line.startswith("size("):
            outs.append(str(obj.size()))
        else:
            raise ValueError(line)
    return outs


def write_cases(cases: List[Tuple[str, List[str]]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    readme = [
        "# P5245 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 每行一次调用，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, ops) in enumerate(cases, 1):
        assert ops[0].startswith("TTLCache(")
        assert len(ops) <= 4000
        outs = run_ops(ops)
        text_in = "\n".join(ops)
        (DATA / f"{i}.in").write_bytes(text_in.encode("utf-8"))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(outs) + "\n")
        readme.append(f"| {i} | {desc} |")

    # 自校验：std.TTLCache + template 解析逻辑
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)

    def run_with_std(ops: List[str]) -> List[str]:
        outs = []
        obj = None
        for line in ops:
            if line.startswith("TTLCache("):
                cap = int(line[line.find("(") + 1 : line.find(")")])
                obj = std_mod.TTLCache(cap)
                outs.append("null")
            elif line.startswith("put("):
                a, b, c = [int(x.strip()) for x in line[4:-1].split(",")]
                obj.put(a, b, c)
                outs.append("null")
            elif line.startswith("get("):
                a, b = [int(x.strip()) for x in line[4:-1].split(",")]
                outs.append(str(obj.get(a, b)))
            elif line.startswith("purge("):
                a = int(line[6:-1])
                outs.append(str(obj.purge(a)))
            elif line.startswith("size("):
                outs.append(str(obj.size()))
        return outs

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        ops = raw.decode("utf-8").split("\n")
        got = run_with_std(ops)
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8").splitlines()
        assert got == exp, (i, got, exp)
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n")

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
        f.write("\n".join(readme) + "\n")
    print("P5245 generated 10 cases OK")


def rand_ops(cap: int, n_ops: int, key_lo: int = 1, key_hi: int = 20) -> List[str]:
    ops = [f"TTLCache({cap})"]
    keys_used: List[int] = []
    t = 0
    for _ in range(n_ops):
        choice = RNG.random()
        if choice < 0.45 or not keys_used:
            k = RNG.randint(key_lo, key_hi)
            v = RNG.randint(-100, 100)
            exp = t + RNG.randint(1, 30)
            ops.append(f"put({k}, {v}, {exp})")
            if k not in keys_used:
                keys_used.append(k)
        elif choice < 0.7:
            k = RNG.choice(keys_used)
            now = RNG.randint(0, t + 20)
            ops.append(f"get({k}, {now})")
        elif choice < 0.85:
            now = RNG.randint(0, t + 25)
            ops.append(f"purge({now})")
        else:
            ops.append("size()")
        t += RNG.randint(0, 3)
    return ops


def main() -> None:
    cases: List[Tuple[str, List[str]]] = []

    # 1 样例1（与题面完全一致）
    sample1 = [
        "TTLCache(2)",
        "put(1, 10, 5)",
        "put(2, 20, 3)",
        "get(2, 2)",
        "get(2, 3)",
        "put(3, 30, 4)",
        "get(1, 0)",
        "size()",
        "purge(4)",
        "size()",
        "get(3, 4)",
    ]
    cases.append(("样例1", sample1))

    # 2 容量 1，覆盖与淘汰
    cases.append(
        (
            "边界：capacity=1",
            [
                "TTLCache(1)",
                "put(1, 1, 10)",
                "put(2, 2, 5)",
                "get(1, 0)",
                "get(2, 0)",
                "size()",
            ],
        )
    )

    # 3 hack：get 不删过期；同 expireAt 淘汰更小 key
    cases.append(
        (
            "hack：同 expireAt 淘汰更小 key；过期仍占位",
            [
                "TTLCache(2)",
                "put(5, 1, 10)",
                "put(3, 2, 10)",
                "put(7, 3, 20)",
                "get(5, 0)",
                "get(3, 0)",
                "size()",
                "get(5, 10)",
                "size()",
                "purge(10)",
                "size()",
            ],
        )
    )

    # 4 覆盖写不增容量
    cases.append(
        (
            "覆盖 put 不触发淘汰",
            [
                "TTLCache(2)",
                "put(1, 1, 100)",
                "put(2, 2, 100)",
                "put(1, 9, 50)",
                "size()",
                "put(3, 3, 1)",
                "get(1, 0)",
                "get(2, 0)",
                "get(3, 0)",
            ],
        )
    )

    # 5 purge 边界 now==expireAt
    cases.append(
        (
            "hack：now==expireAt 视为过期",
            [
                "TTLCache(3)",
                "put(1, 1, 5)",
                "put(2, 2, 5)",
                "put(3, 3, 6)",
                "get(1, 5)",
                "purge(5)",
                "size()",
                "get(3, 5)",
            ],
        )
    )

    # 6 负 key/value
    cases.append(
        (
            "负键值",
            [
                "TTLCache(2)",
                "put(-1, -10, 3)",
                "put(-2, 0, 4)",
                "get(-1, 2)",
                "put(0, 1, 1)",
                "get(-2, 0)",
                "purge(4)",
                "size()",
            ],
        )
    )

    cases.append(("随机小", rand_ops(3, 40, 1, 8)))
    cases.append(("随机中", rand_ops(10, 200, 1, 30)))
    cases.append(("压力：cap=500 中等调用", rand_ops(500, 800, -1000, 1000)))
    cases.append(("压力：近 4000 次调用", rand_ops(200, 3500, -10000, 10000)))

    assert len(cases) == 10
    write_cases(cases)


if __name__ == "__main__":
    main()
