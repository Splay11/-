# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5546)


def make_case(N, d, eps=1e-5):
    X = [[rng.uniform(-5, 5) for _ in range(d)] for _ in range(N)]
    gamma = [rng.uniform(0.5, 2.0) for _ in range(d)]
    beta = [rng.uniform(-1, 1) for _ in range(d)]
    lines = [f"{N} {d}"]
    for row in X:
        lines.append(" ".join(f"{v:.6f}" for v in row))
    lines.append(" ".join(f"{v:.6f}" for v in gamma))
    lines.append(" ".join(f"{v:.6f}" for v in beta))
    lines.append(f"{eps}")
    return "\n".join(lines)


SAMPLES = [
"""4 2
1.0 2.0
2.0 4.0
3.0 6.0
4.0 8.0
1.0 1.0
0.0 0.0
1e-5""",
"""2 3
0.0 0.0 0.0
2.0 4.0 6.0
2.0 2.0 2.0
1.0 1.0 1.0
1e-5""",
]


def gen_inputs():
    cases = [SAMPLES[0].strip(), SAMPLES[1].strip()]
    cases.append(make_case(2, 1))  # 最小 N,d
    cases.append(make_case(3, 2, 1e-3))
    cases.append(make_case(8, 4))
    cases.append(make_case(16, 8))
    cases.append(make_case(32, 16))
    cases.append(make_case(64, 32))
    cases.append(make_case(128, 64))  # 上限
    cases.append(make_case(100, 64, 1e-6))
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
    print("P5546 gen ok: 10/10")


if __name__ == "__main__":
    main()
