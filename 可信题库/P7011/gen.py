# -*- coding: utf-8 -*-
"""P7011 造数：证书链签发与懒吊销。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7011)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")


def run_ops(ops: List[str]) -> List[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.run_ops(ops)


def write_case(idx: int, ops: List[str]) -> None:
    assert ops[0] == "CertAuthority()"
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


def sample1() -> List[str]:
    return [
        "CertAuthority()",
        "issue(1, 0, 100)",
        "issue(2, 1, 80)",
        "issue(3, 1, 120)",
        "isValid(2, 50)",
        "ttl(2, 50)",
        "issue(3, 1, 60)",
        "revoke(1)",
        "isValid(2, 50)",
        "isValid(1, 50)",
        "ttl(3, 10)",
        "issuerOf(2)",
        "rootOf(3)",
        "issue(4, 2, 50)",
    ]


def sample2() -> List[str]:
    return [
        "CertAuthority()",
        "issue(0, 0, 10)",
        "issue(1, 2, 10)",
        "issue(5, 0, 0)",
        "issue(5, 0, 10)",
        "issue(5, 0, 20)",
        "revoke(9)",
        "revoke(5)",
        "revoke(5)",
        "isValid(5, 0)",
        "ttl(5, 0)",
        "issuerOf(9)",
        "rootOf(5)",
    ]


def build_random(n_ops: int, id_hi: int) -> List[str]:
    ops = ["CertAuthority()"]
    parent: Dict[int, int] = {}
    expire: Dict[int, int] = {}
    revoked: Set[int] = set()
    nxt = 1

    def chain_clean(cid: int) -> bool:
        seen = set()
        cur = cid
        while cur != 0:
            if cur in seen or cur not in parent or cur in revoked:
                return False
            seen.add(cur)
            cur = parent[cur]
        return True

    for _ in range(n_ops):
        t = RNG.randint(0, 7)
        if t == 0:
            cid = nxt
            nxt += 1
            if RNG.random() < 0.25 or not parent:
                pid, exp = 0, RNG.randint(10, 1000)
            else:
                pids = list(parent.keys())
                pid = RNG.choice(pids)
                pe = expire[pid]
                exp = RNG.randint(1, pe) if pe >= 1 else 1
            if RNG.random() < 0.08:
                cid = RNG.choice(list(parent.keys()) + [0, cid])
            if RNG.random() < 0.05:
                exp = 0
            ops.append(f"issue({cid}, {pid}, {exp})")
            # mirror success conditions
            ok = cid > 0 and exp > 0 and cid not in parent
            if ok and pid == 0:
                parent[cid] = 0
                expire[cid] = exp
            elif ok and pid in parent and chain_clean(pid) and exp <= expire[pid]:
                parent[cid] = pid
                expire[cid] = exp
        elif t == 1:
            cid = RNG.choice(list(parent.keys())) if parent and RNG.random() < 0.7 else RNG.randint(1, id_hi)
            ops.append(f"revoke({cid})")
            if cid in parent and cid not in revoked:
                revoked.add(cid)
        elif t == 2:
            cid = RNG.choice(list(parent.keys())) if parent and RNG.random() < 0.8 else RNG.randint(1, id_hi)
            now = RNG.randint(0, 1200)
            ops.append(f"isValid({cid}, {now})")
        elif t == 3:
            cid = RNG.choice(list(parent.keys())) if parent and RNG.random() < 0.8 else RNG.randint(1, id_hi)
            now = RNG.randint(0, 1200)
            ops.append(f"ttl({cid}, {now})")
        elif t == 4:
            cid = RNG.choice(list(parent.keys())) if parent and RNG.random() < 0.8 else RNG.randint(1, id_hi)
            ops.append(f"issuerOf({cid})")
        else:
            cid = RNG.choice(list(parent.keys())) if parent and RNG.random() < 0.8 else RNG.randint(1, id_hi)
            ops.append(f"rootOf({cid})")
    return ops


def deep_chain(n: int) -> List[str]:
    ops = ["CertAuthority()"]
    ops.append("issue(1, 0, 100000)")
    for i in range(2, n + 1):
        ops.append(f"issue({i}, {i - 1}, {100000 - i})")
    ops.append(f"isValid({n}, 0)")
    ops.append(f"ttl({n}, 10)")
    ops.append(f"rootOf({n})")
    ops.append("revoke(2)")
    ops.append(f"isValid({n}, 0)")
    ops.append(f"issuerOf({n})")
    return ops


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        sample1(),
        sample2(),
        ["CertAuthority()", "isValid(1, 0)", "ttl(1, 0)", "issuerOf(1)", "rootOf(1)", "revoke(1)"],
        ["CertAuthority()", "issue(1, 0, 5)", "isValid(1, 4)", "isValid(1, 5)", "ttl(1, 4)", "ttl(1, 5)"],
        build_random(80, 50),
        deep_chain(30),
        build_random(200, 200),
        # hack: 子过期钳制 + 祖先吊销后仍能 rootOf
        [
            "CertAuthority()",
            "issue(10, 0, 50)",
            "issue(11, 10, 50)",
            "issue(12, 11, 51)",
            "issue(12, 11, 40)",
            "isValid(12, 39)",
            "revoke(11)",
            "isValid(12, 0)",
            "rootOf(12)",
            "issue(13, 12, 10)",
        ],
        build_random(800, 1000),
        deep_chain(400) + build_random(500, 2000)[1:],
    ]
    assert len(cases) == 10
    assert run_ops(cases[0])[-1] == "false"
    assert "30" in run_ops(cases[0])

    for i, ops in enumerate(cases, 1):
        write_case(i, ops)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

    write_config()
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 每行一次调用。\n"
        "1-2 样例；4 过期边界 now>=expireAt；6/10 深链+祖先吊销；8 子证书过期钳制。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    print("P7011 data ok")


if __name__ == "__main__":
    main()
