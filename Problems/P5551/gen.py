# -*- coding: utf-8 -*-
# 题面 L,d<=8,dff<=16。题面样例缺 Wo 前三行，1.in 按单位阵补全 Wo 后再接 FFN（不改题面.md）。
# 后两组取 L=8,d=8,dff=16，Python 秒内可算完。
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5551)

# 补全 Wo 为单位阵后的样例输入
SAMPLE1 = """2 4 2 8
1.0 0.0 1.0 0.0
0.0 1.0 0.0 1.0
0.5 0.0 0.0 0.5
0.0 0.5 0.5 0.0
0.0 0.0 0.5 0.5
0.5 0.5 0.0 0.0
0.0 0.5 0.0 0.5
0.5 0.0 0.0 0.5
0.0 0.0 0.5 0.5
0.0 0.0 0.0 1.0
0.0 0.5 0.5 0.0
0.0 0.0 0.5 0.5
0.0 1.0 0.0 0.0
0.0 0.0 1.0 0.0
1.0 0.0 0.0 0.0
0.0 1.0 0.0 0.0
0.0 0.0 1.0 0.0
0.0 0.0 0.0 1.0
0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.1 0.1 0.1 0.1
0.0 0.0 0.0 0.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{v:.4f}" for v in row) for row in M)


def rand_mat(r, c, lo=-0.5, hi=0.5):
    return [[rng.uniform(lo, hi) for _ in range(c)] for _ in range(r)]


def make_case(L, d, h, dff):
    assert d % h == 0
    X = rand_mat(L, d, -1, 1)
    Wq, Wk, Wv, Wo = [rand_mat(d, d) for _ in range(4)]
    W1 = rand_mat(d, dff)
    b1 = [rng.uniform(-0.1, 0.1) for _ in range(dff)]
    W2 = rand_mat(dff, d)
    b2 = [rng.uniform(-0.1, 0.1) for _ in range(d)]
    parts = [
        f"{L} {d} {h} {dff}",
        fmt_mat(X),
        fmt_mat(Wq),
        fmt_mat(Wk),
        fmt_mat(Wv),
        fmt_mat(Wo),
        fmt_mat(W1),
        " ".join(f"{v:.4f}" for v in b1),
        fmt_mat(W2),
        " ".join(f"{v:.4f}" for v in b2),
    ]
    return "\n".join(parts)


def gen_inputs():
    cases = [SAMPLE1.strip()]
    cases.append(make_case(1, 2, 1, 2))
    cases.append(make_case(2, 2, 2, 4))
    cases.append(make_case(2, 4, 2, 8))
    cases.append(make_case(3, 4, 2, 8))
    cases.append(make_case(4, 4, 4, 8))
    cases.append(make_case(5, 6, 3, 12))
    cases.append(make_case(6, 6, 2, 12))
    cases.append(make_case(8, 8, 4, 16))  # 上限附近
    cases.append(make_case(8, 8, 8, 16))
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
    print("P5551 gen ok: 10/10")


if __name__ == "__main__":
    main()
