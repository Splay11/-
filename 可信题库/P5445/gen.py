# -*- coding: utf-8 -*-
"""造数：食堂取餐叫号。"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import importlib.util
import random
import re
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(544520260914)

LIMIT = 10000
MAXID = 10 ** 9


def load_std():
    """加载题目根目录的 std.py，用它重放调用流做自校验。"""
    spec = importlib.util.spec_from_file_location("std_mod_p5445", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


STD = load_std()


def replay(lines: List[str]) -> List[str]:
    """按题面语义逐行重放一次调用流，返回每行输出。"""
    outs: List[str] = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == "PickupDesk()":
            obj = STD.PickupDesk()
            outs.append("null")
        elif line.startswith("order("):
            m = re.fullmatch(r"order\((-?\d+)\)", line)
            assert m is not None, line
            outs.append("true" if obj.order(int(m.group(1))) else "false")
        elif line == "serve()":
            outs.append(str(obj.serve()))
        elif line == "waiting()":
            outs.append(str(obj.waiting()))
        else:
            raise ValueError(line)
    return outs


def rand_ops(n: int, pool: List[int]) -> List[str]:
    """随机调用流：多取号，少量叫号与查询，制造重复取号和空队列叫号。"""
    ops = ["PickupDesk()"]
    for _ in range(n):
        r = RNG.random()
        if r < 0.55:
            ops.append(f"order({RNG.choice(pool)})")
        elif r < 0.85:
            ops.append("serve()")
        else:
            ops.append("waiting()")
    return ops


def build_cases() -> List[Tuple[str, List[str]]]:
    sample1 = [
        "PickupDesk()",
        "order(101)",
        "order(102)",
        "waiting()",
        "serve()",
        "serve()",
        "serve()",
        "waiting()",
    ]
    sample2 = [
        "PickupDesk()",
        "order(7)",
        "order(7)",
        "waiting()",
        "serve()",
        "order(7)",
        "waiting()",
    ]
    sample3 = [
        "PickupDesk()",
        "serve()",
        "waiting()",
        "order(5)",
        "serve()",
        "serve()",
    ]

    # 4 单号反复取/叫
    case4 = [
        "PickupDesk()",
        "order(1)",
        "order(1)",
        "serve()",
        "serve()",
        "order(1)",
        "waiting()",
        "serve()",
        "order(1)",
        "order(1)",
        "serve()",
        "waiting()",
    ]

    # 5 多人排队，按先来后到依次叫号
    case5 = (
        ["PickupDesk()"]
        + [f"order({x})" for x in (11, 22, 33, 44)]
        + ["waiting()", "serve()", "serve()", "waiting()", "serve()", "serve()", "serve()"]
    )

    # 6 hack：重复取号未判重会让人数虚高；也覆盖对空队列叫号
    case6 = [
        "PickupDesk()",
        "serve()",
        "order(1000000000)",
        "order(1000000000)",
        "order(1000000000)",
        "waiting()",
        "serve()",
        "serve()",
        "waiting()",
        "order(1000000000)",
        "waiting()",
    ]

    # 7 叫走之后再取同一个号
    case7 = [
        "PickupDesk()",
        "order(5)",
        "order(5)",
        "serve()",
        "order(5)",
        "order(5)",
        "waiting()",
        "serve()",
        "serve()",
        "order(5)",
        "waiting()",
    ]

    # 8 构造：连续取号后一次性全部叫走，再交叉取叫
    inter: List[str] = []
    for i in range(1, 21):
        inter.append(f"order({300 + i})")
        inter.append("serve()")
    inter += ["order(7)", "order(8)", "serve()", "order(9)", "serve()", "serve()", "waiting()"]
    case8 = (
        ["PickupDesk()"]
        + [f"order({i})" for i in range(1, 51)]
        + ["waiting()"]
        + ["serve()"] * 50
        + ["waiting()"]
        + inter
    )

    # 9 中等随机，约 2000 次调用
    case9 = rand_ops(1999, list(range(1, 301)))

    # 10 接近上限，约 10000 次调用，号覆盖 1 与 1e9
    big_pool = [1, MAXID] + [RNG.randint(1, 200) for _ in range(30)] + [
        RNG.randint(MAXID - 1000, MAXID) for _ in range(30)
    ]
    base = rand_ops(9993, big_pool)
    case10 = (
        base[:1]
        + [
            "order(1)",
            "order(1000000000)",
            "order(1000000000)",
            "waiting()",
            "serve()",
            "order(1)",
        ]
        + base[1:]
    )

    return [
        ("样例1：按取号先后叫号，空队列叫号返回 -1", sample1),
        ("样例2：重复取号失败，叫走之后可以再取", sample2),
        ("样例3：一开始没人等待，取号后立刻被叫走", sample3),
        ("单号反复取号/叫号", case4),
        ("多人排队按先来后到依次叫号，覆盖先来先叫顺序", case5),
        ("hack：重复取号不判重会让人数虚高，并覆盖对空队列叫号", case6),
        ("叫走之后再取同一个号", case7),
        ("构造：连续取号后一次性全部叫走，再交叉取叫", case8),
        ("中等随机约 2000 次调用", case9),
        ("接近上限约 10000 次调用，号覆盖 1 与 10^9", case10),
    ]


def write_cases(cases: List[Tuple[str, List[str]]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    for i, (_, ops) in enumerate(cases, 1):
        assert ops[0] == "PickupDesk()", i
        assert len(ops) <= LIMIT, (i, len(ops))
        for line in ops:
            m = re.fullmatch(r"order\((\d+)\)", line)
            if m is not None:
                assert 1 <= int(m.group(1)) <= MAXID, (i, line)
        outs = replay(ops)
        (DATA / f"{i}.in").write_bytes("\n".join(ops).encode("utf-8"))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(outs) + "\n")

    # 自校验：重新从磁盘读回 .in，用 std.py 的 PickupDesk 逐行重放并与 .out 比对
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert b"\r" not in raw, ("in 出现 CRLF", i)
        assert not raw.endswith(b"\n"), ("in 末尾多了换行", i)
        lines = raw.decode("utf-8").split("\n")
        assert lines[0] == "PickupDesk()", i
        got = replay(lines)

        outb = (DATA / f"{i}.out").read_bytes()
        assert b"\r" not in outb, ("out 出现 CRLF", i)
        assert outb.endswith(b"\n"), ("out 末尾缺换行", i)
        assert not outb.endswith(b"\n\n"), ("out 末尾换行多于一个", i)
        exp = outb.decode("utf-8").split("\n")[:-1]
        assert got == exp, (i, got[:8], exp[:8])
        assert len(got) == len(lines), i

    assert len((DATA / "10.in").read_text(encoding="utf-8").split("\n")) == LIMIT

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
    with open(DATA / "config.yaml", "w", encoding="utf-8", newline="\n") as f:
        f.write(config)

    readme = [
        "# 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 每行一次调用，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    with open(DATA / "README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(readme) + "\n")

    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(
        Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh"
    )


def main() -> None:
    cases = build_cases()
    assert len(cases) == 10
    write_cases(cases)
    print("OK")


if __name__ == "__main__":
    main()
