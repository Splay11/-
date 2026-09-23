# -*- coding: utf-8 -*-
"""P5536 gen: KL 散度"""
import os, subprocess, sys, random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """2 3
0.5000 0.3000 0.2000
0.1000 0.2000 0.7000
0.4000 0.4000 0.2000
0.2000 0.3000 0.5000"""


def rand_dist(rng, n):
    xs = [rng.uniform(0.0001, 1.0) for _ in range(n)]
    s = sum(xs)
    xs = [max(0.0001, x / s) for x in xs]
    # 再归一并夹紧
    s = sum(xs)
    xs = [x / s for x in xs]
    return xs


def make_case(seed, m, n):
    rng = random.Random(seed)
    lines = [f"{m} {n}"]
    for _ in range(m):
        lines.append(" ".join(f"{v:.4f}" for v in rand_dist(rng, n)))
    for _ in range(m):
        lines.append(" ".join(f"{v:.4f}" for v in rand_dist(rng, n)))
    return "\n".join(lines)


cases = [SAMPLE]
cases.append(make_case(1, 1, 2))
cases.append(make_case(2, 3, 3))
cases.append(make_case(3, 5, 5))
cases.append(make_case(4, 10, 10))
cases.append(make_case(5, 20, 20))
cases.append(make_case(6, 50, 30))
cases.append(make_case(7, 100, 50))
# 接近上限
cases.append(make_case(8, 500, 100))
cases.append(make_case(9, 500, 100))

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
assert open(os.path.join(DATA, "1.out"), encoding="utf-8").read() == "0.055195\n"
print("P5536 gen ok 10/10 sample match")
