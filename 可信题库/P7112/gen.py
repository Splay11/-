# -*- coding: utf-8 -*-
"""P7112 造数：分片租约管理器调用流。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7112)
PM = ROOT.parent.parent
COMPILE_SH = PM / "compile.sh"
EXECUTE_SH = PM / "核心代码模式模板" / "execute.sh"


def run_lines(lines: List[str]) -> List[str]:
    import importlib.util
    import re

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    obj = None
    outs: List[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("ShardLeaseManager("):
            m = re.fullmatch(r"ShardLeaseManager\((\d+),\s*(\d+)\)", line)
            assert m
            obj = mod.ShardLeaseManager(int(m.group(1)), int(m.group(2)))
            outs.append("null")
        elif line.startswith("acquire("):
            m = re.fullmatch(r"acquire\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            assert m and obj is not None
            a, b, c, d = map(int, m.groups())
            outs.append("true" if obj.acquire(a, b, c, d) else "false")
        elif line.startswith("renew("):
            m = re.fullmatch(r"renew\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            assert m and obj is not None
            a, b, c, d = map(int, m.groups())
            outs.append("true" if obj.renew(a, b, c, d) else "false")
        elif line.startswith("release("):
            m = re.fullmatch(r"release\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            assert m and obj is not None
            a, b, c = map(int, m.groups())
            outs.append("true" if obj.release(a, b, c) else "false")
        elif line.startswith("owner("):
            m = re.fullmatch(r"owner\((-?\d+),\s*(-?\d+)\)", line)
            assert m and obj is not None
            a, b = map(int, m.groups())
            outs.append(str(obj.owner(a, b)))
        elif line.startswith("heldCount("):
            m = re.fullmatch(r"heldCount\((-?\d+),\s*(-?\d+)\)", line)
            assert m and obj is not None
            a, b = map(int, m.groups())
            outs.append(str(obj.heldCount(a, b)))
        else:
            raise SystemExit("bad op " + line)
    return outs


def write_case(idx: int, lines: List[str]) -> None:
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    outs = run_lines(lines)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def random_script(sc: int, mh: int, nops: int) -> List[str]:
    lines = [f"ShardLeaseManager({sc}, {mh})"]
    now = 0
    clients = [1, 2, 3, 4, 5]
    for _ in range(nops):
        now += RNG.randint(0, 3)
        op = RNG.choice(["acquire", "acquire", "renew", "release", "owner", "heldCount"])
        cid = RNG.choice(clients)
        sid = RNG.randint(0, sc - 1)
        ttl = RNG.randint(1, 20)
        if op == "acquire":
            if RNG.random() < 0.05:
                cid = 0
            lines.append(f"acquire({cid}, {sid}, {now}, {ttl})")
        elif op == "renew":
            lines.append(f"renew({cid}, {sid}, {now}, {ttl})")
        elif op == "release":
            lines.append(f"release({cid}, {sid}, {now})")
        elif op == "owner":
            lines.append(f"owner({sid}, {now})")
        else:
            lines.append(f"heldCount({cid}, {now})")
    return lines


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[str]] = []

    cases.append(
        [
            "ShardLeaseManager(3, 2)",
            "acquire(1, 0, 0, 10)",
            "acquire(1, 1, 1, 10)",
            "acquire(1, 2, 2, 10)",
            "owner(0, 5)",
            "heldCount(1, 5)",
            "acquire(2, 0, 5, 5)",
            "release(1, 0, 5)",
            "acquire(2, 0, 5, 5)",
            "renew(1, 1, 8, 10)",
            "owner(1, 8)",
            "owner(1, 20)",
        ]
    )
    cases.append(
        [
            "ShardLeaseManager(2, 1)",
            "acquire(0, 0, 0, 1)",
            "acquire(1, 0, 0, 5)",
            "acquire(1, 0, 0, 5)",
            "renew(1, 0, 3, 2)",
            "release(1, 0, 4)",
            "release(1, 0, 4)",
            "owner(0, 4)",
            "heldCount(1, 4)",
        ]
    )
    cases.append(
        [
            "ShardLeaseManager(1, 1)",
            "acquire(1, 0, 0, 1)",
            "owner(0, 0)",
            "owner(0, 1)",
            "acquire(2, 0, 1, 3)",
            "heldCount(2, 1)",
        ]
    )
    # 越界 shard
    cases.append(
        [
            "ShardLeaseManager(2, 2)",
            "acquire(1, 2, 0, 5)",
            "acquire(1, -1, 0, 5)",
            "owner(2, 0)",
            "heldCount(0, 0)",
        ]
    )
    # 过期后同客户端可再 acquire
    cases.append(
        [
            "ShardLeaseManager(2, 1)",
            "acquire(1, 0, 0, 5)",
            "acquire(1, 0, 5, 5)",
            "owner(0, 5)",
            "heldCount(1, 5)",
        ]
    )
    cases.append(random_script(5, 2, 40))
    cases.append(random_script(8, 3, 80))
    # hack：不懒过期会占满 maxHold
    cases.append(
        [
            "ShardLeaseManager(3, 1)",
            "acquire(1, 0, 0, 2)",
            "acquire(1, 1, 2, 2)",
            "heldCount(1, 2)",
            "owner(0, 2)",
            "owner(1, 2)",
        ]
    )
    cases.append(random_script(20, 5, 200))
    cases.append(random_script(50, 10, 500))

    assert len(cases) == 10
    exp1 = run_lines(cases[0])
    assert exp1[1:4] == ["true", "true", "false"]

    for i, c in enumerate(cases, 1):
        write_case(i, c)

    for i in range(1, 11):
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
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
  - template.c
  - compile.sh
  - execute.sh
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
        "主造数脚本：题目根目录 `gen.py`。stdin 为 ShardLeaseManager 调用流。\n"
        "8 卡「不懒过期导致 maxHold 误判」。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    shutil.copyfile(EXECUTE_SH, DATA / "execute.sh")
    print("P7112 data ok")


if __name__ == "__main__":
    main()
