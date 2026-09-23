# -*- coding: utf-8 -*-
"""P5540 gen: 两层全连接前向反向
题面样例在 b2 与 y 之间多了一个 0.0；造数用去掉多余 0.0 后的合法输入（y=1.0）。
"""
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

# 去掉题面中 b2 后多余的那个 0.0
SAMPLE = """2 3 1
1.0 2.0
0.5 0.3 0.1
0.2 0.4 0.6
0.0 0.0 0.0
0.5
0.3
0.1
0.0
1.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{x:.4f}" for x in row) for row in M)


def make_case(seed, d_in, d_h, d_out):
    rng = np.random.RandomState(seed)
    x = rng.randn(d_in)
    W1 = rng.randn(d_in, d_h)
    b1 = rng.randn(d_h)
    W2 = rng.randn(d_h, d_out)
    b2 = rng.randn(d_out)
    y = rng.randn(d_out)
    parts = [
        f"{d_in} {d_h} {d_out}",
        " ".join(f"{v:.4f}" for v in x),
        fmt_mat(W1),
        " ".join(f"{v:.4f}" for v in b1),
        fmt_mat(W2),
        " ".join(f"{v:.4f}" for v in b2),
        " ".join(f"{v:.4f}" for v in y),
    ]
    return "\n".join(parts)


cases = [SAMPLE]
cases.append(make_case(1, 1, 1, 1))
cases.append(make_case(2, 2, 2, 1))
cases.append(make_case(3, 2, 3, 2))
cases.append(make_case(4, 3, 3, 3))
cases.append(make_case(5, 4, 4, 2))
cases.append(make_case(6, 5, 5, 4))
cases.append(make_case(7, 6, 6, 6))
# 接近上限
cases.append(make_case(8, 8, 8, 8))
cases.append(make_case(9, 8, 8, 8))

assert len(cases) == 10
std = os.path.join(DIR, "std.py")
for i, text in enumerate(cases, 1):
    open(os.path.join(DATA, f"{i}.in"), "w", encoding="utf-8", newline="").write(
        text.replace("\r\n", "\n").rstrip("\n")
    )
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"case {i}: {p.stderr}")
    open(os.path.join(DATA, f"{i}.out"), "w", encoding="utf-8", newline="").write(
        p.stdout.replace("\r\n", "\n").rstrip("\n") + "\n"
    )
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    exp = open(os.path.join(DATA, f"{i}.out"), encoding="utf-8").read()
    got = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True).stdout
    got = got.replace("\r\n", "\n").rstrip("\n") + "\n"
    if got != exp:
        raise SystemExit(f"mismatch {i}")
expected = (
    "0.2800\n0.5184\n"
    "0.0720 0.0432 0.0144\n"
    "0.1440 0.0864 0.0288\n"
    "0.0720 0.0432 0.0144\n"
    "0.6480 0.2160 0.0720\n"
    "-0.7200 -0.2400 -0.0880\n"
    "-1.4400\n"
)
got1 = open(os.path.join(DATA, "1.out"), encoding="utf-8").read()
print("P5540 gen ok 10/10")
print("sample_match", got1 == expected)
print("got_sample:\n" + got1)
