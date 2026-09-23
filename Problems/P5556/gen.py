# -*- coding: utf-8 -*-
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """2 3 2 1 0.5
1.0 0.0 1.0
0.0 1.0 0.0
1.0 0.0
0.0 1.0
1.0 0.0
1.0
0.0
1.0
1.0 1.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{x:.4f}" for x in row) for row in M)


def make_case(seed, n, d_in, d_out, r, alpha):
    rng = np.random.RandomState(seed)
    X = rng.randn(n, d_in)
    W = rng.randn(d_in, d_out)
    A = rng.randn(d_in, r)
    B = rng.randn(r, d_out)
    return "\n".join([
        f"{n} {d_in} {d_out} {r} {alpha:.4f}",
        fmt_mat(X), fmt_mat(W), fmt_mat(A), fmt_mat(B),
    ])


cases = [SAMPLE]
cases.append(make_case(1, 1, 1, 1, 1, 1.0))
cases.append(make_case(2, 2, 2, 2, 1, 0.5))
cases.append(make_case(3, 3, 4, 3, 2, 0.25))
cases.append(make_case(4, 4, 8, 8, 2, 1.0))
cases.append(make_case(5, 8, 8, 4, 3, 0.8))
cases.append(make_case(6, 8, 12, 12, 4, 0.5))
cases.append(make_case(7, 12, 12, 16, 4, 0.1))
# 上限 n,d<=16
cases.append(make_case(8, 16, 16, 16, 8, 0.5))
cases.append(make_case(9, 16, 16, 16, 16, 1.0))

assert len(cases) == 10
std = os.path.join(DIR, "std.py")
for i, text in enumerate(cases, 1):
    open(os.path.join(DATA, f"{i}.in"), "w", encoding="utf-8", newline="").write(
        text.replace("\r\n", "\n").rstrip("\n"))
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    open(os.path.join(DATA, f"{i}.out"), "w", encoding="utf-8", newline="").write(
        p.stdout.replace("\r\n", "\n").rstrip("\n") + "\n")
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    exp = open(os.path.join(DATA, f"{i}.out"), encoding="utf-8").read()
    got = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True).stdout
    got = got.replace("\r\n", "\n").rstrip("\n") + "\n"
    if got != exp:
        raise SystemExit(f"mismatch {i}")
print("P5556 gen ok 10/10")
