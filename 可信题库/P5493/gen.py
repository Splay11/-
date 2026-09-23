# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5493)


class LogChunk:
    def __init__(self, mid: int, idx: int) -> None:
        self.mid = mid
        self.idx = idx
        self.sz = 0


class FileLogger:
    def __init__(self, fileCap: int, totalCap: int) -> None:
        self.cap = fileCap
        self.quota = totalCap
        self.files: List[LogChunk] = []
        self.cur = {}
        self.seq = {}

    def totalSize(self) -> int:
        return sum(f.sz for f in self.files)

    def _drop_oldest(self) -> None:
        f = self.files.pop(0)
        if self.cur.get(f.mid) is f:
            del self.cur[f.mid]

    def putLog(self, mid: int, nbytes: int) -> int:
        while self.totalSize() + nbytes > self.quota:
            self._drop_oldest()
        cur = self.cur.get(mid)
        if cur is None or cur.sz + nbytes > self.cap:
            self.seq[mid] = self.seq.get(mid, 0) + 1
            cur = LogChunk(mid, self.seq[mid])
            self.files.append(cur)
            self.cur[mid] = cur
        cur.sz += nbytes
        return cur.sz

    def listFiles(self):
        return [[f.mid, f.idx, f.sz] for f in self.files]


def simulate(ops: List[str]) -> List[str]:
    obj = None
    outs: List[str] = []
    for line in ops:
        if line.startswith("FileLogger("):
            inner = line[len("FileLogger(") : -1]
            a, b = inner.split(",")
            obj = FileLogger(int(a), int(b))
            outs.append("null")
        elif line.startswith("putLog("):
            inner = line[7:-1]
            a, b = inner.split(",")
            outs.append(str(obj.putLog(int(a), int(b))))
        elif line == "listFiles()":
            outs.append(json.dumps(obj.listFiles()))
        elif line == "totalSize()":
            outs.append(str(obj.totalSize()))
        else:
            raise ValueError(line)
    return outs


def write_case(idx: int, ops: List[str]) -> None:
    text_in = "\n".join(ops)
    outs = simulate(ops)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def sample1() -> List[str]:
    return [
        "FileLogger(8, 50)",
        "putLog(3, 2)",
        "putLog(3, 3)",
        "putLog(4, 7)",
        "putLog(3, 4)",
        "totalSize()",
        "listFiles()",
    ]


def sample2() -> List[str]:
    return [
        "FileLogger(6, 16)",
        "putLog(1, 5)",
        "putLog(2, 4)",
        "putLog(1, 3)",
        "putLog(2, 5)",
        "totalSize()",
        "listFiles()",
    ]


def sample3() -> List[str]:
    return [
        "FileLogger(5, 20)",
        "putLog(9, 3)",
        "listFiles()",
        "totalSize()",
    ]


def random_ops() -> List[str]:
    cap = RNG.randint(4, 20)
    quota = RNG.randint(cap + 5, 80)
    ops = [f"FileLogger({cap}, {quota})"]
    for _ in range(RNG.randint(8, 40)):
        t = RNG.randint(0, 4)
        if t <= 2:
            mid = RNG.randint(1, 6)
            nbytes = RNG.randint(1, cap - 1)
            ops.append(f"putLog({mid}, {nbytes})")
        elif t == 3:
            ops.append("totalSize()")
        else:
            ops.append("listFiles()")
    return ops


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        sample1(),
        sample2(),
        sample3(),
        [
            "FileLogger(4, 10)",
            "putLog(1, 3)",
            "putLog(1, 2)",
            "putLog(1, 3)",
            "listFiles()",
            "totalSize()",
        ],
        [
            "FileLogger(7, 12)",
            "putLog(2, 6)",
            "putLog(3, 6)",
            "putLog(2, 5)",
            "totalSize()",
            "listFiles()",
        ],
        random_ops(),
        random_ops(),
        random_ops(),
        random_ops(),
        random_ops(),
    ]
    assert len(cases) == 10
    assert simulate(sample1())[-2] == "16"
    assert simulate(sample2())[-2] == "12"

    for i, ops in enumerate(cases, 1):
        write_case(i, ops)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        ops = [ln for ln in raw.split("\n") if ln.strip()]
        inner = ops[0][len("FileLogger(") : -1]
        a, b = inner.split(",")
        obj = std_mod.FileLogger(int(a), int(b))
        outs = ["null"]
        for line in ops[1:]:
            if line.startswith("putLog("):
                x, y = line[7:-1].split(",")
                outs.append(str(obj.putLog(int(x), int(y))))
            elif line == "listFiles()":
                outs.append(json.dumps(obj.listFiles()))
            elif line == "totalSize()":
                outs.append(str(obj.totalSize()))
        got = "\n".join(outs) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
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
    (DATA / "README.md").write_text("主造数脚本：题目根目录 gen.py。stdin 为 FileLogger 调用流。\n", encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")
    print("P5493 data ok")


if __name__ == "__main__":
    main()
