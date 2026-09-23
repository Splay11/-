# -*- coding: utf-8 -*-
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """3 0.2
1.0000 -1.0000 -1.2000
-0.5000 -2.0000 -1.5000
2.0000 -0.8000 -0.8000"""


def make_case(seed, n, eps):
    rng = np.random.RandomState(seed)
    lines = [f"{n} {eps:.4f}"]
    for _ in range(n):
        A = rng.uniform(-10, 10)
        pi = rng.uniform(-20, 0)
        pi_old = rng.uniform(-20, 0)
        lines.append(f"{A:.4f} {pi:.4f} {pi_old:.4f}")
    return "\n".join(lines)


cases = [SAMPLE]
cases.append(make_case(1, 1, 0.01))
cases.append(make_case(2, 5, 0.1))
cases.append(make_case(3, 10, 0.2))
cases.append(make_case(4, 20, 0.3))
cases.append(make_case(5, 50, 0.05))
cases.append(make_case(6, 100, 0.2))
cases.append(make_case(7, 200, 0.15))
# 接近上限 n<=1000，向量运算秒级内
cases.append(make_case(8, 1000, 0.2))
cases.append(make_case(9, 800, 0.5))

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
print("P5554 gen ok 10/10")
