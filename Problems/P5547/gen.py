# -*- coding: utf-8 -*-
# 数据规模：题面 d<=8, T<=30；后两组取满上限，Python 毫秒级可算完。
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5547)

SAMPLE1 = """2 3
0.1000 0.9000 0.9990 0.00000001
1.0000 -1.0000
0.5000 -0.3000
0.5000 0.5000
0.4000 -0.2000"""

# 题面样例 2 多写了一行梯度；按 T=5 只取 5 步
SAMPLE2 = """3 5
0.0100 0.9000 0.9990 0.00000001
0.5000 0.5000 1.0000
0.8000 -0.6000 0.2000
0.3000 -0.4000 0.5000
0.6000 -0.1000 0.3000
0.5000 0.5000 0.4000
0.2000 0.5000 0.1000"""


def make_case(d, T, alpha=None):
    if alpha is None:
        alpha = rng.choice([0.001, 0.01, 0.05, 0.1])
    beta1 = 0.9
    beta2 = 0.999
    eps = 1e-8
    theta = [rng.uniform(-2, 2) for _ in range(d)]
    grads = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(T)]
    lines = [
        f"{d} {T}",
        f"{alpha:.4f} {beta1:.4f} {beta2:.4f} {eps:.8f}",
        " ".join(f"{v:.4f}" for v in theta),
    ]
    for g in grads:
        lines.append(" ".join(f"{v:.4f}" for v in g))
    return "\n".join(lines)


def gen_inputs():
    cases = [SAMPLE1.strip(), SAMPLE2.strip()]
    cases.append(make_case(1, 1, 0.1))
    cases.append(make_case(2, 2, 0.05))
    cases.append(make_case(3, 5, 0.01))
    cases.append(make_case(4, 10))
    cases.append(make_case(5, 15))
    cases.append(make_case(6, 20))
    cases.append(make_case(8, 30))  # 上限
    cases.append(make_case(8, 30, 0.001))
    assert len(cases) == 10
    return cases


def write_no_trailing_nl(path, text):
    text = text.replace("\r\n", "\n").rstrip("\n")
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def write_out(path, text):
    text = text.replace("\r\n", "\n").rstrip("\n") + "\n"
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def main():
    os.makedirs(DATA, exist_ok=True)
    for i, inp in enumerate(gen_inputs(), 1):
        in_path = os.path.join(DATA, f"{i}.in")
        out_path = os.path.join(DATA, f"{i}.out")
        write_no_trailing_nl(in_path, inp)
        p = subprocess.run(
            [sys.executable, STD],
            input=(inp + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )
        if p.returncode != 0:
            raise SystemExit(f"std fail {i}: {p.stderr.decode()}")
        write_out(out_path, p.stdout.decode())
        p2 = subprocess.run(
            [sys.executable, STD],
            input=open(in_path, "rb").read() + b"\n",
            stdout=subprocess.PIPE,
            cwd=ROOT,
        )
        if p2.stdout.decode().replace("\r\n", "\n") != open(out_path, encoding="utf-8").read().replace("\r\n", "\n"):
            raise SystemExit(f"mismatch {i}")
    print("P5547 gen ok: 10/10")


if __name__ == "__main__":
    main()
