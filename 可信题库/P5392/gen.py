# -*- coding: utf-8 -*-
"""造数：配置文件编辑锁。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(539220260907)


class FileLockBoard:
    def __init__(self):
        self.own: Dict[int, int] = {}

    def lock(self, fileId: int, ownerId: int) -> bool:
        if fileId in self.own:
            return False
        self.own[fileId] = ownerId
        return True

    def unlock(self, fileId: int, ownerId: int) -> bool:
        if self.own.get(fileId) != ownerId:
            return False
        del self.own[fileId]
        return True

    def holder(self, fileId: int) -> int:
        return self.own.get(fileId, -1)

    def lockedCount(self) -> int:
        return len(self.own)


def run_ops(ops: List[str]) -> List[str]:
    outs: List[str] = []
    obj: FileLockBoard | None = None
    for line in ops:
        if line.startswith("FileLockBoard("):
            obj = FileLockBoard()
            outs.append("null")
        elif line.startswith("lock("):
            a, b = [int(x.strip()) for x in line[5:-1].split(",")]
            outs.append("true" if obj.lock(a, b) else "false")
        elif line.startswith("unlock("):
            a, b = [int(x.strip()) for x in line[7:-1].split(",")]
            outs.append("true" if obj.unlock(a, b) else "false")
        elif line.startswith("holder("):
            a = int(line[7:-1])
            outs.append(str(obj.holder(a)))
        elif line.startswith("lockedCount("):
            outs.append(str(obj.lockedCount()))
        else:
            raise ValueError(line)
    return outs


def rand_ops(n: int, nfile: int, nowner: int) -> List[str]:
    ops = ["FileLockBoard()"]
    files = list(range(1, nfile + 1))
    owners = list(range(1, nowner + 1))
    for _ in range(n):
        kind = RNG.choice(["lock", "lock", "unlock", "holder", "lockedCount"])
        if kind == "lock":
            ops.append(f"lock({RNG.choice(files)}, {RNG.choice(owners)})")
        elif kind == "unlock":
            ops.append(f"unlock({RNG.choice(files)}, {RNG.choice(owners)})")
        elif kind == "holder":
            ops.append(f"holder({RNG.choice(files)})")
        else:
            ops.append("lockedCount()")
    return ops


def write_cases(cases: List[Tuple[str, List[str]]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    readme = [
        "# 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 每行一次调用，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, ops) in enumerate(cases, 1):
        assert ops[0] == "FileLockBoard()"
        assert len(ops) <= 10000
        outs = run_ops(ops)
        text_in = "\n".join(ops)
        (DATA / f"{i}.in").write_bytes(text_in.encode("utf-8"))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(outs) + "\n")
        readme.append(f"| {i} | {desc} |")

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)

    def run_with_std(ops: List[str]) -> List[str]:
        outs = []
        obj = None
        for line in ops:
            if line.startswith("FileLockBoard("):
                obj = std_mod.FileLockBoard()
                outs.append("null")
            elif line.startswith("lock("):
                a, b = [int(x.strip()) for x in line[5:-1].split(",")]
                outs.append("true" if obj.lock(a, b) else "false")
            elif line.startswith("unlock("):
                a, b = [int(x.strip()) for x in line[7:-1].split(",")]
                outs.append("true" if obj.unlock(a, b) else "false")
            elif line.startswith("holder("):
                a = int(line[7:-1])
                outs.append(str(obj.holder(a)))
            elif line.startswith("lockedCount("):
                outs.append(str(obj.lockedCount()))
        return outs

    for i, (_, ops) in enumerate(cases, 1):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        got = run_with_std(ops)
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8").splitlines()
        assert got == exp, (i, got[:8], exp[:8])
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
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")


def main() -> None:
    s1 = [
        "FileLockBoard()",
        "lock(1, 10)",
        "lock(1, 20)",
        "holder(1)",
        "unlock(1, 20)",
        "unlock(1, 10)",
        "holder(1)",
        "lockedCount()",
    ]
    s2 = [
        "FileLockBoard()",
        "lock(3, 1)",
        "lock(3, 1)",
        "lock(4, 1)",
        "lockedCount()",
        "holder(4)",
        "unlock(4, 1)",
        "lockedCount()",
    ]
    s3 = [
        "FileLockBoard()",
        "unlock(9, 1)",
        "holder(9)",
        "lock(9, 2)",
        "lock(8, 2)",
        "lockedCount()",
    ]
    cases: List[Tuple[str, List[str]]] = [
        ("样例1：抢锁失败与错误持有者解锁", s1),
        ("样例2：不可重入 + 同一人锁多文件", s2),
        ("样例3：对空文件 unlock/holder", s3),
        ("单文件反复锁解", ["FileLockBoard()", "lock(1, 1)", "lock(1, 1)", "unlock(1, 2)", "unlock(1, 1)", "lock(1, 2)", "holder(1)", "lockedCount()"]),
        ("多文件互不干扰", ["FileLockBoard()", "lock(1, 7)", "lock(2, 8)", "lock(3, 7)", "holder(2)", "unlock(1, 8)", "unlock(1, 7)", "lockedCount()"]),
        ("hack：覆盖式 lock / 不校验 unlock", ["FileLockBoard()", "lock(5, 1)", "lock(5, 2)", "holder(5)", "unlock(5, 2)", "holder(5)", "unlock(5, 1)", "holder(5)"]),
        ("中等随机", rand_ops(80, 12, 5)),
        ("构造：锁满再逐个解", ["FileLockBoard()"] + [f"lock({i}, {i})" for i in range(1, 41)] + ["lockedCount()"] + [f"unlock({i}, {i})" for i in range(1, 41)] + ["lockedCount()"]),
        ("较大随机", rand_ops(2000, 80, 20)),
        ("接近上限随机", rand_ops(9999, 200, 50)),
    ]
    assert len(cases) == 10
    write_cases(cases)
    print("P5392 data ok")


if __name__ == "__main__":
    main()
