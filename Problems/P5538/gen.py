# -*- coding: utf-8 -*-
"""P5538 gen: SGD 线性回归"""
import os, subprocess, sys, random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """4 1 0.1000 1
1.0000 2.0000
2.0000 4.0000
3.0000 6.0000
4.0000 8.0000"""


def make_case(seed, n, d, eta, T):
    rng = random.Random(seed)
    lines = [f"{n} {d} {eta:.4f} {T}"]
    for _ in range(n):
        xs = [rng.uniform(-10, 10) for _ in range(d)]
        y = rng.uniform(-10, 10)
        lines.append(" ".join(f"{v:.4f}" for v in xs + [y]))
    return "\n".join(lines)


cases = [SAMPLE]
cases.append(make_case(1, 1, 1, 0.0001, 1))
cases.append(make_case(2, 5, 2, 0.01, 2))
cases.append(make_case(3, 10, 3, 0.05, 5))
cases.append(make_case(4, 20, 5, 0.001, 10))
cases.append(make_case(5, 50, 8, 0.0005, 20))
cases.append(make_case(6, 100, 10, 0.0002, 30))
cases.append(make_case(7, 200, 15, 0.0001, 50))
# 接近上限（学习率保持较小，避免 SGD 发散）
cases.append(make_case(8, 500, 20, 0.0001, 100))
cases.append(make_case(9, 500, 20, 0.0001, 100))

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
assert open(os.path.join(DATA, "1.out"), encoding="utf-8").read() == "1.5776\n0.9984\n"
print("P5538 gen ok 10/10 sample match")
