# -*- coding: utf-8 -*-
"""P5539 gen: 两层 MLP
题面样例输入少一行（W1 第二行与 W2 共需 4 行、样例只给 3 行）。
此处按「W1 第二行为 1.0 -1.0，W2 为 1.0 / -1.0」补全后造数。
"""
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

# 补全后的样例输入（相对题面多了 W1 第二行的 -1.0 写在同一行）
SAMPLE = """3 2 2 0.1
1.0 2.0 3.0
1.0 0.5
0.5 1.0
0.0 0.5
0.5 0.5
1.0 -1.0
1.0
-1.0"""


def fmt_mat(M, prec=4):
    return "\n".join(" ".join(f"{x:.{prec}f}" for x in row) for row in M)


def make_case(seed, n, d_in, d_h, eta):
    rng = np.random.RandomState(seed)
    y = rng.randn(n)
    X = rng.randn(n, d_in)
    W1 = rng.randn(d_in, d_h)
    W2 = rng.randn(d_h, 1)
    return "\n".join([
        f"{n} {d_in} {d_h} {eta:.4f}",
        " ".join(f"{v:.4f}" for v in y),
        fmt_mat(X),
        fmt_mat(W1),
        fmt_mat(W2),
    ])


cases = [SAMPLE]
cases.append(make_case(1, 2, 2, 2, 0.01))
cases.append(make_case(2, 3, 2, 3, 0.1))
cases.append(make_case(3, 4, 3, 2, 0.05))
cases.append(make_case(4, 5, 3, 3, 0.2))
cases.append(make_case(5, 6, 4, 4, 0.01))
cases.append(make_case(6, 8, 4, 5, 0.5))
cases.append(make_case(7, 8, 5, 4, 0.1))
# 接近上限
cases.append(make_case(8, 10, 5, 5, 1.0))
cases.append(make_case(9, 10, 5, 5, 0.001))

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
expected = "0.2500 0.2500 -0.5000\n1.7500\n0.4950 0.5050\n0.9700 -0.4700\n0.9667\n-0.9667\n"
got1 = open(os.path.join(DATA, "1.out"), encoding="utf-8").read()
print("P5539 gen ok 10/10")
print("sample_match", got1 == expected)
print("got_sample:\n" + got1)
