# -*- coding: utf-8 -*-
"""造数：练歌房麦序。"""
from __future__ import annotations

import heapq
import random
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(540320260909)


class MicQueue:
    def __init__(self):
        self.heat: Dict[int, int] = {}
        self.heap: List[Tuple[int, int]] = []

    def enroll(self, songId: int, heat: int) -> bool:
        if songId in self.heat:
            return False
        self.heat[songId] = heat
        heapq.heappush(self.heap, (-heat, songId))
        return True

    def nextPlay(self) -> int:
        while self.heap:
            h, sid = heapq.heappop(self.heap)
            h = -h
            if self.heat.get(sid) == h:
                del self.heat[sid]
                return sid
        return -1

    def boost(self, songId: int, addHeat: int) -> bool:
        if songId not in self.heat:
            return False
        self.heat[songId] += addHeat
        heapq.heappush(self.heap, (-self.heat[songId], songId))
        return True

    def cancel(self, songId: int) -> bool:
        if songId not in self.heat:
            return False
        del self.heat[songId]
        return True

    def waiting(self) -> int:
        return len(self.heat)


def run_ops(ops: List[str]) -> List[str]:
    outs: List[str] = []
    obj: MicQueue | None = None
    for line in ops:
        if line.startswith("MicQueue("):
            obj = MicQueue()
            outs.append("null")
        elif line.startswith("enroll("):
            a, b = [int(x.strip()) for x in line[7:-1].split(",")]
            outs.append("true" if obj.enroll(a, b) else "false")
        elif line.startswith("nextPlay("):
            outs.append(str(obj.nextPlay()))
        elif line.startswith("boost("):
            a, b = [int(x.strip()) for x in line[6:-1].split(",")]
            outs.append("true" if obj.boost(a, b) else "false")
        elif line.startswith("cancel("):
            a = int(line[7:-1])
            outs.append("true" if obj.cancel(a) else "false")
        elif line.startswith("waiting("):
            outs.append(str(obj.waiting()))
        else:
            raise ValueError(line)
    return outs


def rand_ops(n: int, nsong: int) -> List[str]:
    ops = ["MicQueue()"]
    songs = list(range(1, nsong + 1))
    for _ in range(n):
        kind = RNG.choice(
            ["enroll", "enroll", "nextPlay", "boost", "cancel", "waiting"]
        )
        if kind == "enroll":
            ops.append(f"enroll({RNG.choice(songs)}, {RNG.randint(1, 10**9)})")
        elif kind == "nextPlay":
            ops.append("nextPlay()")
        elif kind == "boost":
            ops.append(f"boost({RNG.choice(songs)}, {RNG.randint(1, 10**6)})")
        elif kind == "cancel":
            ops.append(f"cancel({RNG.choice(songs)})")
        else:
            ops.append("waiting()")
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
        assert ops[0] == "MicQueue()"
        assert len(ops) <= 8000
        for line in ops:
            if line.startswith("enroll(") or line.startswith("boost("):
                a, b = [int(x.strip()) for x in line[line.index("(") + 1 : -1].split(",")]
                assert 1 <= a <= 10**9 and 1 <= b <= 10**9
            elif line.startswith("cancel("):
                a = int(line[7:-1])
                assert 1 <= a <= 10**9
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
            if line.startswith("MicQueue("):
                obj = std_mod.MicQueue()
                outs.append("null")
            elif line.startswith("enroll("):
                a, b = [int(x.strip()) for x in line[7:-1].split(",")]
                outs.append("true" if obj.enroll(a, b) else "false")
            elif line.startswith("nextPlay("):
                outs.append(str(obj.nextPlay()))
            elif line.startswith("boost("):
                a, b = [int(x.strip()) for x in line[6:-1].split(",")]
                outs.append("true" if obj.boost(a, b) else "false")
            elif line.startswith("cancel("):
                a = int(line[7:-1])
                outs.append("true" if obj.cancel(a) else "false")
            elif line.startswith("waiting("):
                outs.append(str(obj.waiting()))
        return outs

    for i, (_, ops) in enumerate(cases, 1):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        got = run_with_std(ops)
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8").splitlines()
        assert got == exp, (i, got[:12], exp[:8])
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
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")


def main() -> None:
    s1 = [
        "MicQueue()",
        "enroll(3, 10)",
        "enroll(5, 10)",
        "enroll(3, 20)",
        "waiting()",
        "nextPlay()",
        "boost(5, 5)",
        "enroll(8, 20)",
        "nextPlay()",
        "nextPlay()",
        "cancel(9)",
        "waiting()",
    ]
    s2 = [
        "MicQueue()",
        "nextPlay()",
        "boost(1, 1)",
        "cancel(1)",
        "enroll(2, 1)",
        "cancel(2)",
        "waiting()",
        "enroll(2, 3)",
        "nextPlay()",
    ]
    s3 = [
        "MicQueue()",
        "enroll(9, 1)",
        "enroll(4, 100)",
        "boost(9, 50)",
        "nextPlay()",
        "waiting()",
    ]
    same_heat = (
        ["MicQueue()"]
        + [f"enroll({i}, 7)" for i in (9, 1, 5, 2)]
        + ["nextPlay()", "nextPlay()", "nextPlay()", "nextPlay()", "nextPlay()"]
    )
    hack_boost = [
        "MicQueue()",
        "enroll(1, 10)",
        "enroll(2, 20)",
        "boost(1, 100)",
        "nextPlay()",
        "nextPlay()",
        "waiting()",
    ]
    hack_cancel = [
        "MicQueue()",
        "enroll(6, 50)",
        "enroll(7, 1)",
        "cancel(6)",
        "nextPlay()",
        "enroll(6, 3)",
        "nextPlay()",
        "waiting()",
    ]
    many_boost = ["MicQueue()", "enroll(1, 1)", "enroll(2, 2)"]
    for _ in range(40):
        many_boost.append("boost(1, 1000000000)")
    many_boost += ["nextPlay()", "nextPlay()"]

    cases: List[Tuple[str, List[str]]] = [
        ("样例1：同热度编号小先唱 + 重复 enroll 失败", s1),
        ("样例2：空队列失败路径与撤后再点", s2),
        ("样例3：加热仍不超高热度对手", s3),
        ("同热度按编号升序出队", same_heat),
        ("hack：boost 后必须按新热度出队", hack_boost),
        ("hack：cancel 后不得弹出；可再 enroll", hack_cancel),
        ("中等随机", rand_ops(80, 12)),
        ("多次加热溢出 32 位", many_boost),
        ("较大随机", rand_ops(2000, 80)),
        ("接近上限随机", rand_ops(7999, 200)),
    ]
    assert len(cases) == 10
    assert run_ops(s1)[-1] == "0"
    assert run_ops(s1)[5] == "3"
    write_cases(cases)
    print("P5403 data ok")


if __name__ == "__main__":
    main()
