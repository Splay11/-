# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5542)


def fmt_mat(a, prec=2):
    lines = []
    for row in a:
        lines.append(" ".join(f"{float(v):.{prec}f}" for v in row))
    return "\n".join(lines)


def make_case(N, dm, dff):
    X = [[rng.uniform(-3, 3) for _ in range(dm)] for _ in range(N)]
    W1 = [[rng.uniform(-1, 1) for _ in range(dff)] for _ in range(dm)]
    b1 = [rng.uniform(-0.5, 0.5) for _ in range(dff)]
    W2 = [[rng.uniform(-1, 1) for _ in range(dm)] for _ in range(dff)]
    b2 = [rng.uniform(-0.5, 0.5) for _ in range(dm)]
    parts = [
        f"{N} {dm} {dff}",
        fmt_mat(X, 6),
        fmt_mat(W1, 6),
        " ".join(f"{v:.6f}" for v in b1),
        fmt_mat(W2, 6),
        " ".join(f"{v:.6f}" for v in b2),
    ]
    return "\n".join(parts)


SAMPLE = """1 2 3
1.0 2.0
0.5 -0.5 1.0
-1.0 0.5 0.5
0.1 0.0 -0.1
0.5 0.5
1.0 -1.0
-0.5 1.0
0.0 0.0"""


def gen_inputs():
    cases = [SAMPLE.strip()]
    cases.append(make_case(1, 1, 1))  # 边界最小
    # 含负激活被 ReLU 清零
    cases.append(make_case(2, 3, 4))
    for _ in range(4):
        cases.append(make_case(rng.randint(1, 8), rng.randint(1, 8), rng.randint(1, 16)))
    cases.append(make_case(10, 16, 32))
    cases.append(make_case(50, 32, 64))
    cases.append(make_case(40, 32, 64))
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
        p = subprocess.run([sys.executable, STD], input=(inp + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT)
        if p.returncode != 0:
            raise SystemExit(f"std fail {i}: {p.stderr.decode()}")
        write_out(out_path, p.stdout.decode())
        p2 = subprocess.run([sys.executable, STD], input=open(in_path, "rb").read() + b"\n", stdout=subprocess.PIPE, cwd=ROOT)
        if p2.stdout.decode().replace("\r\n", "\n") != open(out_path, encoding="utf-8").read().replace("\r\n", "\n"):
            raise SystemExit(f"mismatch {i}")
    print("P5542 gen ok: 10/10")


if __name__ == "__main__":
    main()
