# -*- coding: utf-8 -*-
"""P7006 造数：ClusterPool best-fit 调度（10 组）。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import List, Set, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7006)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")


def run_ops(ops: List[str]) -> List[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.run_ops(ops)


def write_case(idx: int, ops: List[str]) -> None:
    assert ops[0] == "ClusterPool()"
    assert len(ops) <= 4000
    text_in = "\n".join(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    outs = run_ops(ops)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def write_config() -> None:
    lines = [
        "type: default",
        "user_extra_files:",
        "  - template.py",
        "  - template.java",
        "  - template.cc",
        "  - template.c",
        "  - compile.sh",
        "  - config.yaml",
        "  - user.cc",
        "  - user.java",
        "  - user.py",
        "  - user.c",
        "subtasks:",
        "  - score: 100",
        "    if: []",
        "    id: 1",
        "    type: sum",
        "    cases:",
    ]
    for i in range(1, 11):
        lines.append(f"      - input: {i}.in")
        lines.append(f"        output: {i}.out")
    lines.extend(
        [
            "langs:",
            "  - py.py3",
            "  - java",
            "  - cc.cc14o2",
            "  - py",
            "  - cc",
            "  - c",
            "",
        ]
    )
    (DATA / "config.yaml").write_text("\n".join(lines), encoding="utf-8")


def build_random(n_ops: int, n_nodes: int, cap_hi: int) -> List[str]:
    """随机混合合法/非法操作，保持规模在题面约束内。"""
    ops = ["ClusterPool()"]
    nodes: Set[int] = set()
    live_jobs: Set[int] = set()
    next_job = 1
    node_pool = list(range(1, n_nodes + 1))

    while len(ops) < n_ops:
        op = RNG.choice(
            [
                "add",
                "add",
                "submit",
                "submit",
                "submit",
                "kill",
                "remove",
                "used",
                "free",
                "job",
                "bad_size",
                "dup_add",
            ]
        )
        if op == "add" or (op == "dup_add" and not nodes):
            nid = RNG.choice(node_pool)
            cap = RNG.randint(1, cap_hi)
            ops.append(f"addNode({nid}, {cap})")
            # 真实是否成功由 std 决定；此处只粗跟踪
            if nid not in nodes:
                nodes.add(nid)
        elif op == "dup_add":
            nid = RNG.choice(list(nodes))
            ops.append(f"addNode({nid}, {RNG.randint(1, cap_hi)})")
        elif op == "remove":
            if nodes and RNG.random() < 0.7:
                nid = RNG.choice(list(nodes))
            else:
                nid = RNG.randint(1, n_nodes + 5)
            ops.append(f"removeNode({nid})")
            # 粗估：不保证同步，仅用于造随机序列
        elif op == "submit":
            jid = next_job
            next_job += 1
            size = RNG.randint(1, max(1, cap_hi // 2))
            ops.append(f"submit({jid}, {size})")
            live_jobs.add(jid)
        elif op == "bad_size":
            jid = next_job
            next_job += 1
            ops.append(f"submit({jid}, {RNG.choice([0, -1, -5])})")
        elif op == "kill":
            if live_jobs and RNG.random() < 0.7:
                jid = RNG.choice(list(live_jobs))
            else:
                jid = RNG.randint(1, max(2, next_job + 3))
            ops.append(f"kill({jid})")
            live_jobs.discard(jid)
        elif op == "used":
            nid = RNG.choice(node_pool) if node_pool else 1
            ops.append(f"usedOf({nid})")
        elif op == "free":
            nid = RNG.choice(node_pool) if node_pool else 1
            ops.append(f"freeOf({nid})")
        else:
            jid = RNG.randint(1, max(2, next_job + 2))
            ops.append(f"jobNode({jid})")
    return ops[:n_ops]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    if COMPILE_SH.is_file():
        shutil.copyfile(COMPILE_SH, DATA / "compile.sh")

    cases: List[Tuple[str, List[str]]] = []

    # 1-2: 题面样例（样例1 输出已按 best-fit 规则校正）
    cases.append(
        (
            "样例1",
            [
                "ClusterPool()",
                "addNode(2, 10)",
                "addNode(1, 10)",
                "submit(100, 6)",
                "submit(101, 6)",
                "submit(102, 5)",
                "usedOf(1)",
                "usedOf(2)",
                "freeOf(1)",
                "kill(100)",
                "submit(102, 5)",
                "removeNode(2)",
                "kill(101)",
                "removeNode(2)",
                "jobNode(102)",
            ],
        )
    )
    cases.append(
        (
            "样例2",
            [
                "ClusterPool()",
                "addNode(5, 3)",
                "addNode(5, 9)",
                "submit(1, 0)",
                "submit(1, 3)",
                "submit(1, 1)",
                "kill(2)",
                "jobNode(1)",
                "freeOf(5)",
                "removeNode(5)",
                "kill(1)",
                "removeNode(5)",
            ],
        )
    )

    # 3: best-fit 并列 — 剩余相同必须选更小 nodeId
    cases.append(
        (
            "hack-bestfit并列取小id",
            [
                "ClusterPool()",
                "addNode(30, 20)",
                "addNode(10, 20)",
                "addNode(20, 20)",
                "submit(1, 5)",
                "usedOf(10)",
                "usedOf(20)",
                "usedOf(30)",
                "submit(2, 5)",
                "submit(3, 5)",
                "freeOf(10)",
                "freeOf(20)",
                "freeOf(30)",
                "jobNode(1)",
                "jobNode(2)",
                "jobNode(3)",
            ],
        )
    )

    # 4: 有任务时 remove 失败；杀光后可删；再 add 同 id 不同容量
    cases.append(
        (
            "hack-有任务不可删再上线",
            [
                "ClusterPool()",
                "addNode(7, 100)",
                "submit(1, 40)",
                "submit(2, 30)",
                "removeNode(7)",
                "kill(1)",
                "removeNode(7)",
                "kill(2)",
                "removeNode(7)",
                "addNode(7, 8)",
                "submit(3, 8)",
                "freeOf(7)",
                "usedOf(7)",
                "jobNode(3)",
                "removeNode(7)",
                "kill(3)",
                "removeNode(7)",
                "usedOf(7)",
            ],
        )
    )

    # 5: 非法 size / 重复 job / 重复 add / 查不存在
    cases.append(
        (
            "hack-非法size与重复",
            [
                "ClusterPool()",
                "addNode(1, 50)",
                "addNode(1, 1)",
                "addNode(0, 10)",
                "addNode(2, 0)",
                "addNode(2, -3)",
                "submit(9, 0)",
                "submit(9, -1)",
                "submit(9, 10)",
                "submit(9, 1)",
                "kill(8)",
                "usedOf(99)",
                "freeOf(1)",
                "jobNode(9)",
                "kill(9)",
                "jobNode(9)",
                "removeNode(99)",
                "removeNode(1)",
            ],
        )
    )

    # 6: best-fit 选更紧剩余（非 first-fit / 非最大剩余）
    cases.append(
        (
            "hack-选最紧剩余非最大",
            [
                "ClusterPool()",
                "addNode(1, 100)",
                "addNode(2, 30)",
                "addNode(3, 50)",
                "submit(1, 20)",
                "submit(2, 25)",
                "freeOf(1)",
                "freeOf(2)",
                "freeOf(3)",
                "submit(3, 20)",
                "jobNode(3)",
                "usedOf(1)",
                "usedOf(2)",
                "usedOf(3)",
            ],
        )
    )

    # 7: 边界 — 大容量与大任务、装不下返回 -1
    cases.append(
        (
            "边界-大值与装不下",
            [
                "ClusterPool()",
                "addNode(1000000, 1000000000)",
                "addNode(1, 1)",
                "submit(1, 1000000000)",
                "submit(2, 2)",
                "submit(3, 1)",
                "freeOf(1000000)",
                "freeOf(1)",
                "kill(1)",
                "submit(4, 1000000000)",
                "jobNode(4)",
                "removeNode(1000000)",
                "kill(4)",
                "removeNode(1000000)",
            ],
        )
    )

    # 8: 中等随机
    cases.append(("中等随机", build_random(200, 12, 100)))

    # 9-10: 偏大（压满调用次数上限附近）
    cases.append(("偏大随机-A", build_random(2000, 80, 1000)))
    cases.append(("偏大随机-B", build_random(4000, 200, 10000)))

    assert len(cases) == 10
    for i, (name, ops) in enumerate(cases, 1):
        print(f"case {i}: {name}, ops={len(ops)}")
        write_case(i, ops)

    write_config()
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 每行一次调用；"
        "ClusterPool() 输出 null；addNode/removeNode/kill 输出 true/false；"
        "submit/usedOf/freeOf/jobNode 输出整数。\n",
        encoding="utf-8",
    )

    for i in range(1, 11):
        ops = (DATA / f"{i}.in").read_text(encoding="utf-8").split("\n")
        got = "\n".join(run_ops(ops)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        if got != exp:
            raise SystemExit(f"self-check failed on case {i}")
    print("self-check OK")


if __name__ == "__main__":
    main()
