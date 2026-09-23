# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """3 2 0.5
1.0 0.0
0.0 1.0
1.0 1.0
1.0 0.0
0.0 1.0
1.0 1.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{x:.4f}" for x in row) for row in M)


def make_case(seed, n, d, tau):
    rng = np.random.RandomState(seed)
    A = rng.randn(n, d)
    P = A + 0.1 * rng.randn(n, d)  # 正对略扰动
    return f"{n} {d} {tau:.4f}\n{fmt_mat(A)}\n{fmt_mat(P)}"


cases = [SAMPLE]
# 中小
cases.append(make_case(1, 2, 1, 0.1))
cases.append(make_case(2, 4, 3, 0.5))
cases.append(make_case(3, 5, 8, 1.0))
cases.append(make_case(4, 8, 4, 0.2))
cases.append(make_case(5, 10, 16, 0.07))
cases.append(make_case(6, 16, 8, 0.3))
cases.append(make_case(7, 32, 16, 0.5))
# 接近上限但可秒算：n<=64,d<=32
cases.append(make_case(8, 64, 32, 0.1))  # 上限
cases.append(make_case(9, 48, 24, 0.05))

assert len(cases) == 10

for i, text in enumerate(cases, 1):
    # .in 不以换行结尾
    path = os.path.join(DATA, f"{i}.in")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\r\n", "\n").rstrip("\n"))

# 用 std.py 生成 .out
std = os.path.join(DIR, "std.py")
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), "r", encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"std failed on {i}: {p.stderr}")
    out = p.stdout.replace("\r\n", "\n")
    if not out.endswith("\n"):
        out += "\n"
    # 仅一个末尾换行
    out = out.rstrip("\n") + "\n"
    with open(os.path.join(DATA, f"{i}.out"), "w", encoding="utf-8", newline="") as f:
        f.write(out)

# 再校验
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), "r", encoding="utf-8").read()
    exp = open(os.path.join(DATA, f"{i}.out"), "r", encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    got = p.stdout.replace("\r\n", "\n")
    if not got.endswith("\n"):
        got += "\n"
    got = got.rstrip("\n") + "\n"
    if got != exp:
        raise SystemExit(f"mismatch case {i}: {got!r} vs {exp!r}")
print("P5552 gen ok 10/10")
