# -*- coding: utf-8 -*-
"""P5264 测试数据生成。"""

from __future__ import annotations

import random
import subprocess
import sys
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from std import SegTree, merge

DATA = ROOT / "data"
SEED = 526420260819
RNG = random.Random(SEED)

B_MAX = 200_000
Q_MAX = 80_000
MX_LO, MX_HI = -50, 50
WD_LO, WD_HI = 0.1, 100.0
SV_LO, SV_HI = -10_000, 10_000


def brute_query(blocks, l, r):
    mx, wd, sv = blocks[l - 1]
    for i in range(l + 1, r + 1):
        mx, wd, sv = merge((mx, wd, sv), blocks[i - 1])
    return sv / wd


def run_std(text):
    proc = subprocess.run(
        [sys.executable, str(ROOT / "std.py")],
        input=text.encode("utf-8"),
        capture_output=True,
        check=True,
    )
    return proc.stdout.decode("utf-8")


def rand_state():
    mx = RNG.uniform(MX_LO, MX_HI)
    wd = RNG.uniform(WD_LO, WD_HI)
    sv = RNG.uniform(SV_LO, SV_HI)
    return (mx, wd, sv)


def fmt_state(mx, wd, sv, compact=False):
    if compact:
        return f"{mx:.4g} {wd:.4g} {sv:.4g}"
    return f"{mx:.6f} {wd:.6f} {sv:.6f}"


def build_case(B, Q, ops_builder, compact=False):
    blocks = [rand_state() for _ in range(B)]
    lines = [f"{B} {Q}"]
    for mx, wd, sv in blocks:
        lines.append(fmt_state(mx, wd, sv, compact))
    lines.extend(ops_builder(B, blocks, compact))
    return "\n".join(lines)


def fmt_in(text):
    return text


def fmt_out(text):
    if not text.endswith("\n"):
        text += "\n"
    return text


def write_pair(idx, tin, tout):
    DATA.mkdir(parents=True, exist_ok=True)
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in trailing newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out bad newline")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))


def sample1():
    return """4 6
0.0 2.0 4.0
2.0 1.5 9.0
1.0 3.0 6.0
4.0 2.0 8.0
2 1 4
2 2 2
1 3 0.0 1.0 20.0
2 1 3
2 3 4
2 4 4"""


def sample2():
    return """2 3
1.0 2.0 8.0
1.0 2.0 12.0
2 1 2
2 1 1
2 2 2"""


def ops_mixed(B, blocks, q, update_ratio=0.3, compact=False):
    ops = []
    for _ in range(q):
        if RNG.random() < update_ratio:
            i = RNG.randint(1, B)
            st = rand_state()
            blocks[i - 1] = st
            ops.append(f"1 {i} {fmt_state(st[0], st[1], st[2], compact)}")
        else:
            l = RNG.randint(1, B)
            r = RNG.randint(l, B)
            ops.append(f"2 {l} {r}")
    return ops


def build_stress_case(B, Q):
    lines = [f"{B} {Q}"]
    for _ in range(B):
        mx = RNG.randint(MX_LO, MX_HI)
        wd = RNG.randint(1, 100)
        sv = RNG.randint(SV_LO, SV_HI)
        lines.append(f"{mx} {wd} {sv}")
    for _ in range(Q):
        lines.append(f"2 1 {B}")
    return "\n".join(lines)


def main():
    cases = []
    cases.append(sample1())
    cases.append(sample2())
    cases.append(build_case(5, 8, lambda B, bl, c: ops_mixed(B, bl, 8, compact=c)))
    cases.append(build_case(1, 5, lambda B, bl, c: ["2 1 1"] * 5))
    cases.append(build_case(10, 20, lambda B, bl, c: ops_mixed(B, bl, 20, 0.5, compact=c)))
    # hack: 全 mx 相同，指数缩放为 1
    def same_mx_ops(B, bl, c):
        for i in range(B):
            bl[i] = (0.0, RNG.uniform(1, 10), RNG.uniform(-100, 100))
        return ops_mixed(B, bl, 15, 0.2, compact=c)

    cases.append(build_case(50, 15, same_mx_ops))
    cases.append(build_case(100, 80, lambda B, bl, c: ops_mixed(B, bl, 80, compact=c)))
    cases.append(build_case(200, 150, lambda B, bl, c: ops_mixed(B, bl, 150, compact=c)))
    cases.append(build_case(50_000, 50_000, lambda B, bl, c: ops_mixed(B, bl, 50_000, compact=c), compact=True))
    cases.append(build_stress_case(B_MAX, Q_MAX))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        tout = run_std(tin)
        if i <= 8:
            # 小数据与暴力对拍（仅查询输出）
            lines = tin.split("\n")
            B, Q = map(int, lines[0].split())
            blocks = []
            for j in range(1, B + 1):
                mx, wd, sv = map(float, lines[j].split())
                blocks.append((mx, wd, sv))
            out_lines = tout.strip().split("\n")
            qi = 0
            for line in lines[B + 1 :]:
                parts = line.split()
                if parts[0] == "2":
                    l, r = int(parts[1]), int(parts[2])
                    ans = brute_query(blocks, l, r)
                    exp = float(out_lines[qi])
                    if abs(ans - exp) > 1e-4:
                        raise RuntimeError(f"{i}: brute {ans} vs std {exp}")
                    qi += 1
                else:
                    idx = int(parts[1])
                    blocks[idx - 1] = float(parts[2]), float(parts[3]), float(parts[4])
        write_pair(i, fmt_in(tin), fmt_out(tout))
        print(f"{i}.in bytes={len(tin.encode())}")


if __name__ == "__main__":
    main()
