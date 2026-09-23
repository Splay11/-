# -*- coding: utf-8 -*-
"""P7002 造数：打印任务优先队列。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7002)


def run_ops(ops: List[str]) -> List[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.run_ops(ops)


def write_case(idx: int, ops: List[str]) -> None:
    assert ops[0] == "JobQueueSys()"
    assert len(ops) <= 1000
    text_in = "\n".join(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    outs = run_ops(ops)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    cases: List[Tuple[str, List[str]]] = []

    # 1-2: 样例
    cases.append((
        "样例1",
        [
            "JobQueueSys()",
            "submit(2, 5)",
            "submit(1, 5)",
            "submit(3, 8)",
            "peekJob()",
            "popJob()",
            "peekJob()",
            "cancel(1)",
            "popJob()",
            "popJob()",
        ],
    ))
    cases.append((
        "样例2",
        [
            "JobQueueSys()",
            "submit(7, 1)",
            "submit(7, 9)",
            "cancel(8)",
            "popJob()",
            "cancel(7)",
            "peekJob()",
        ],
    ))

    # 3: 空队列 peek/pop
    cases.append((
        "空队列",
        ["JobQueueSys()", "peekJob()", "popJob()", "cancel(1)"],
    ))

    # 4: 同优先级按编号
    cases.append((
        "同优先级编号",
        [
            "JobQueueSys()",
            "submit(9, 1)",
            "submit(3, 1)",
            "submit(5, 1)",
            "popJob()",
            "popJob()",
            "popJob()",
        ],
    ))

    # 5: 取消堆顶后再 peek
    cases.append((
        "取消堆顶",
        [
            "JobQueueSys()",
            "submit(1, 10)",
            "submit(2, 5)",
            "cancel(1)",
            "peekJob()",
            "popJob()",
        ],
    ))

    # 6: 取消后再同号 submit
    cases.append((
        "取消后重提",
        [
            "JobQueueSys()",
            "submit(1, 3)",
            "cancel(1)",
            "submit(1, 9)",
            "peekJob()",
            "popJob()",
        ],
    ))

    # 7: 中等随机
    ops7 = ["JobQueueSys()"]
    alive = set()
    for _ in range(80):
        op = RNG.choice(["submit", "submit", "cancel", "peek", "pop"])
        if op == "submit":
            jid = RNG.randint(0, 50)
            pri = RNG.randint(0, 100)
            ops7.append(f"submit({jid}, {pri})")
            # 不维护真实集合，仅造调用
        elif op == "cancel":
            jid = RNG.randint(0, 50)
            ops7.append(f"cancel({jid})")
        elif op == "peek":
            ops7.append("peekJob()")
        else:
            ops7.append("popJob()")
    cases.append(("中等随机", ops7))

    # 8: 全部同优先级递增编号
    ops8 = ["JobQueueSys()"] + [f"submit({i}, 0)" for i in range(20)]
    ops8 += ["popJob()"] * 20
    cases.append(("顺序弹出", ops8))

    # 9: 较大调用量
    ops9 = ["JobQueueSys()"]
    for i in range(400):
        ops9.append(f"submit({i}, {RNG.randint(0, 10000)})")
    for i in range(0, 400, 3):
        ops9.append(f"cancel({i})")
    for _ in range(200):
        ops9.append(RNG.choice(["peekJob()", "popJob()"]))
    cases.append(("较大调用", ops9))

    # 10: 接近上限
    ops10 = ["JobQueueSys()"]
    for i in range(600):
        ops10.append(f"submit({i}, {i % 17})")
    for i in range(600):
        if i % 2 == 0:
            ops10.append(f"cancel({i})")
        else:
            ops10.append("popJob()")
    while len(ops10) < 900:
        ops10.append("peekJob()")
    cases.append(("接近上限", ops10[:1000]))

    assert len(cases) == 10

    exp1 = run_ops(cases[0][1])
    assert exp1 == [
        "null", "true", "true", "true", "3", "3", "1", "true", "2", "-1"
    ]
    exp2 = run_ops(cases[1][1])
    assert exp2 == ["null", "true", "false", "false", "7", "false", "-1"]

    for i, (_, ops) in enumerate(cases, 1):
        write_case(i, ops)
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
  - template.c
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
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
  - c
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 每行一次调用。\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    print("P7002 data ok")


if __name__ == "__main__":
    main()
