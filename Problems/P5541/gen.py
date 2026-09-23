# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5541)


def fmt_mat(a, prec=6):
    lines = []
    for row in a:
        lines.append(" ".join(f"{float(v):.{prec}f}" for v in row))
    return "\n".join(lines)


def make_case(N, din, dout):
    X = [[rng.uniform(-5, 5) for _ in range(din)] for _ in range(N)]
    W = [[rng.uniform(-1, 1) for _ in range(dout)] for _ in range(din)]
    b = [rng.uniform(-1, 1) for _ in range(dout)]
    parts = [f"{N} {din} {dout}", fmt_mat(X), fmt_mat(W), " ".join(f"{float(v):.6f}" for v in b)]
    return "\n".join(parts)


SAMPLES = [
"""2 3 2
1.0 2.0 3.0
4.0 5.0 6.0
0.1 0.2
0.3 0.4
0.5 0.6
0.1 0.2""",
"""1 2 3
1.0 -1.0
1.0 0.0 -1.0
0.0 1.0 0.0
0.5 0.5 0.5""",
]


def gen_inputs():
    cases = []
    cases.append(SAMPLES[0].strip())
    cases.append(SAMPLES[1].strip())
    # 边界：最小规模
    cases.append(make_case(1, 1, 1))
    # 中小随机
    for _ in range(4):
        N = rng.randint(1, 10)
        din = rng.randint(1, 16)
        dout = rng.randint(1, 8)
        cases.append(make_case(N, din, dout))
    # 第 8 组：中等
    cases.append(make_case(20, 32, 16))
    # 接近上限
    cases.append(make_case(100, 128, 64))
    cases.append(make_case(80, 100, 64))
    assert len(cases) == 10
    return cases


def write_no_trailing_nl(path, text):
    text = text.replace("\r\n", "\n").rstrip("\n")
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def write_out(path, text):
    text = text.replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"
    # 保证末尾仅一个换行
    text = text.rstrip("\n") + "\n"
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def main():
    os.makedirs(DATA, exist_ok=True)
    cases = gen_inputs()
    for i, inp in enumerate(cases, 1):
        in_path = os.path.join(DATA, f"{i}.in")
        out_path = os.path.join(DATA, f"{i}.out")
        write_no_trailing_nl(in_path, inp)
        p = subprocess.run(
            [sys.executable, STD],
            input=inp.encode("utf-8") + b"\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )
        if p.returncode != 0:
            raise SystemExit(f"std failed on {i}: {p.stderr.decode()}")
        write_out(out_path, p.stdout.decode("utf-8"))
        # 再校验
        p2 = subprocess.run(
            [sys.executable, STD],
            input=open(in_path, "rb").read() + b"\n",
            stdout=subprocess.PIPE,
            cwd=ROOT,
        )
        got = p2.stdout.decode("utf-8").replace("\r\n", "\n")
        exp = open(out_path, "r", encoding="utf-8").read().replace("\r\n", "\n")
        if got != exp:
            raise SystemExit(f"mismatch case {i}")
    print("P5541 gen ok: 10/10")


if __name__ == "__main__":
    main()
