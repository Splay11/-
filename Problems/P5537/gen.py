# -*- coding: utf-8 -*-
"""P5537 gen: 梯度下降求平方根"""
import os, subprocess, sys, random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = "4.0\n1.0\n0.01\n5"


def make_case(seed, a, x0, eta, T):
    return f"{a:.4f}\n{x0:.4f}\n{eta:.4f}\n{T}"


cases = [SAMPLE]
cases.append(make_case(1, 0.01, 0.1, 0.0001, 3))
cases.append(make_case(2, 1.0, 0.5, 0.01, 10))
cases.append(make_case(3, 9.0, 1.0, 0.005, 20))
cases.append(make_case(4, 16.0, 2.0, 0.001, 50))
cases.append(make_case(5, 25.0, 3.0, 0.002, 100))
cases.append(make_case(6, 49.0, 5.0, 0.0005, 200))
cases.append(make_case(7, 2.25, 1.0, 0.01, 30))
# 接近上限（学习率保持较小，避免发散）
cases.append(make_case(8, 100.0, 20.0, 0.0001, 1000))
cases.append(make_case(9, 100.0, 10.0, 0.0001, 1000))

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
sample_out = open(os.path.join(DATA, "1.out"), encoding="utf-8").read()
expected = "1.1200 3.9337\n1.2178 2.2386\n1.2956 1.1720\n1.3562 0.5655\n1.4021 0.2523\n"
print("P5537 gen ok 10/10")
print("sample_match", sample_out == expected)
print("got_sample:\n" + sample_out)
