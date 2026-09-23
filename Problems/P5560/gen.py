# -*- coding: utf-8 -*-
"""P5560 开合区间校验：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(556020260922)


def brute(w: str, ops: list[tuple[int, int, int]]) -> list[int]:
    s = list(w)
    out: list[int] = []
    for op, a, b in ops:
        if op == 1:
            for i in range(a - 1, b):
                s[i] = "]" if s[i] == "[" else "["
        else:
            bal = 0
            ok = True
            for i in range(a - 1, b):
                bal += 1 if s[i] == "[" else -1
                if bal < 0:
                    ok = False
                    break
            if bal != 0:
                ok = False
            out.append(1 if ok else 0)
    return out


def write_in(path: Path, w: str, ops: list[tuple[int, int, int]]) -> None:
    lines = [str(len(w)), str(len(ops)), w]
    for op, a, b in ops:
        lines.append(f"{op} {a} {b}")
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[int]) -> None:
    if ans:
        text = "\n".join(str(x) for x in ans) + "\n"
    else:
        text = "\n"
    path.write_bytes(text.encode("utf-8"))


def dump_case(
    idx: int,
    w: str,
    ops: list[tuple[int, int, int]],
    expect: list[int] | None = None,
    check_brute: bool = False,
) -> list[int]:
    ans = solve(w, ops)
    if expect is not None and ans != expect:
        raise SystemExit(f"case {idx} expect {expect} got {ans}")
    if check_brute and brute(w, ops) != ans:
        raise SystemExit(f"case {idx} brute mismatch")
    write_in(DATA / f"{idx}.in", w, ops)
    write_out(DATA / f"{idx}.out", ans)
    return ans


def rand_ops(n: int, q: int, rng: random.Random) -> list[tuple[int, int, int]]:
    ops = []
    for _ in range(q):
        a = rng.randint(1, n)
        b = rng.randint(1, n)
        if a > b:
            a, b = b, a
        ops.append((rng.randint(1, 2), a, b))
    return ops


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 20s
memory: 512m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5560 测例说明

输入：第一行长度 $m$，第二行动作数 $t$，第三行报文，随后 $t$ 行 `op a b`。`op=1` 对调，`op=2` 询问。每个询问一行 $1$ 或 $0$。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

- 1：四级样例 1。整段配平、对调前两格后不配平、中间 `[]` 仍配平。
- 2：四级样例 2。先问中间配平段，再两次单点对调把整段修好。
- 3：单字符，对调后仍不配平。
- 4：`][` 整段对调后变成 `[]`。和为 $0$ 但最小前缀为负，对调前必须输出 $0$。
- 5：`[[][]]` 只对调前三段，再问 $[2,6]$。结果是 $0$。把对调做成区间翻转的做法会得到 $1$。
- 6：$n=2$，两端各对调一次，覆盖下标 $1$ 和 $n$。
- 7：$n=300$ 随机，与直接模拟对拍。
- 8：$n=800$ 随机，再对拍一次。
- 9：$m=t=200000$ 随机。压测线段树。
- 10：先排成 `][` 重复。$[1,2]$ 和为 $0$ 但不配平，$[2,3]$ 是 `[]`。整段对调后全文配平，再对调回去。随后接满规模随机动作。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, "[[][]]", [(2, 1, 6), (1, 1, 2), (2, 1, 6), (2, 4, 5)], [1, 0, 1], True)
    dump_case(
        2,
        "][[]][][",
        [(2, 2, 7), (1, 1, 1), (2, 1, 8), (1, 8, 8), (2, 1, 8)],
        [1, 0, 1],
        True,
    )
    dump_case(3, "[", [(2, 1, 1), (1, 1, 1), (2, 1, 1)], [0, 0], True)
    dump_case(4, "][", [(2, 1, 2), (1, 1, 2), (2, 1, 2)], [0, 1], True)
    dump_case(5, "[[][]]", [(1, 1, 3), (2, 2, 6)], [0], True)
    dump_case(
        6,
        "[]",
        [(2, 1, 2), (1, 1, 1), (2, 1, 1), (1, 2, 2), (2, 1, 2)],
        [1, 0, 0],
        True,
    )
    n7 = 300
    w7 = "".join(RNG.choice("[]") for _ in range(n7))
    dump_case(7, w7, rand_ops(n7, 300, RNG), None, True)
    n8 = 800
    w8 = "".join(RNG.choice("[]") for _ in range(n8))
    dump_case(8, w8, rand_ops(n8, 800, RNG), None, True)

    n9 = 200000
    w9 = "".join(RNG.choice("[]") for _ in range(n9))
    dump_case(9, w9, rand_ops(n9, n9, RNG))

    n10 = 200000
    w10 = "][" * (n10 // 2)
    head = [
        (2, 1, 2),
        (2, 2, 3),
        (1, 1, n10),
        (2, 1, n10),
        (2, 1, 2),
        (1, 1, n10),
        (2, 1, 2),
    ]
    got = solve(w10, head)
    if got != [0, 1, 1, 1, 0]:
        raise SystemExit(f"case 10 head {got}")
    dump_case(10, w10, head + rand_ops(n10, n10 - len(head), RNG))

    for i in range(1, 11):
        raw_in = (DATA / f"{i}.in").read_bytes()
        raw_out = (DATA / f"{i}.out").read_bytes()
        if raw_in.endswith(b"\n"):
            raise SystemExit(f"{i}.in trailing newline")
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out newline")
        text = raw_in.decode("utf-8").split("\n")
        m = int(text[0])
        t = int(text[1])
        w = text[2]
        ops = []
        for line in text[3:]:
            op, a, b = map(int, line.split())
            ops.append((op, a, b))
        if len(w) != m or len(ops) != t:
            raise SystemExit(f"{i} shape")
        ans = solve(w, ops)
        body = raw_out.decode("utf-8")
        expect = ("\n".join(str(x) for x in ans) + "\n") if ans else "\n"
        if body != expect:
            raise SystemExit(f"{i}.out mismatch")
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
