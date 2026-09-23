# -*- coding: utf-8 -*-
"""P5535 gen: 数值稳定 Sigmoid"""
import os, subprocess, sys, random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLES = [
    "5\n0.0 1.0 -1.0 10.0 -10.0",
    "3\n-1000.0 0.0 1000.0",
]


def make_case(seed, n, lo, hi):
    rng = random.Random(seed)
    xs = [rng.uniform(lo, hi) for _ in range(n)]
    return f"{n}\n" + " ".join(f"{v:.4f}" for v in xs)


cases = list(SAMPLES)
cases.append(make_case(1, 1, -1, 1))
cases.append(make_case(2, 8, -5, 5))
cases.append(make_case(3, 20, -20, 20))
cases.append(make_case(4, 50, -100, 100))
cases.append(make_case(5, 100, -500, 500))
cases.append(make_case(6, 200, -10, 10))
# 接近上限
cases.append(make_case(7, 1000, -1000, 1000))
cases.append(make_case(8, 1000, -1000, 1000))

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
        raise SystemExit(p.stderr)
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
# 核对题面样例输出
exp1 = "0.50 0.73 0.27 1.00 0.00\n0.25 0.20 0.20 0.00 0.00\n"
exp2 = "0.00 0.50 1.00\n0.00 0.25 0.00\n"
assert open(os.path.join(DATA, "1.out"), encoding="utf-8").read() == exp1
assert open(os.path.join(DATA, "2.out"), encoding="utf-8").read() == exp2
print("P5535 gen ok 10/10 sample match")
