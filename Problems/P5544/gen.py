# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5544)


def make_case(L, K, S, P):
    assert 0 <= P <= K // 2
    L2 = L + 2 * P
    assert (L2 - K) // S + 1 >= 1
    x = [rng.uniform(-5, 5) for _ in range(L)]
    w = [rng.uniform(-2, 2) for _ in range(K)]
    lines = [
        f"{L} {K} {S} {P}",
        " ".join(f"{v:.4f}" for v in x),
        " ".join(f"{v:.4f}" for v in w),
    ]
    return "\n".join(lines)


SAMPLES = [
"""5 3 1 0
1.0000 2.0000 3.0000 4.0000 5.0000
0.5000 -0.5000 1.0000""",
"""6 3 2 1
1.0000 3.0000 -1.0000 2.0000 4.0000 -2.0000
-1.0000 0.5000 1.0000""",
]


def gen_inputs():
    cases = [SAMPLES[0].strip(), SAMPLES[1].strip()]
    cases.append(make_case(4, 2, 1, 0))  # 边界最小 L
    cases.append(make_case(8, 3, 1, 1))
    cases.append(make_case(10, 5, 2, 2))
    cases.append(make_case(16, 4, 3, 1))
    cases.append(make_case(20, 7, 1, 3))
    cases.append(make_case(32, 5, 2, 2))
    cases.append(make_case(64, 9, 1, 4))  # 上限附近
    cases.append(make_case(64, 9, 3, 4))
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
    print("P5544 gen ok: 10/10")


if __name__ == "__main__":
    main()
