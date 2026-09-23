# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5545)


def make_case(C, H, W, k, s):
    assert k <= H and k <= W
    assert (H - k) // s + 1 >= 1
    lines = [f"{C} {H} {W} {k} {s}"]
    for _c in range(C):
        for _h in range(H):
            lines.append(" ".join(f"{rng.uniform(-10, 20):.1f}" for _ in range(W)))
    return "\n".join(lines)


SAMPLES = [
"""1 4 4 2 2
1.0 2.0 3.0 4.0
5.0 6.0 7.0 8.0
9.0 10.0 11.0 12.0
13.0 14.0 15.0 16.0""",
"""2 3 3 2 1
1.0 2.0 3.0
4.0 5.0 6.0
7.0 8.0 9.0
-1.0 -2.0 -3.0
-4.0 -5.0 -6.0
-7.0 -8.0 -9.0""",
]


def gen_inputs():
    cases = [SAMPLES[0].strip(), SAMPLES[1].strip()]
    cases.append(make_case(1, 2, 2, 1, 1))  # k=1
    cases.append(make_case(1, 2, 2, 2, 1))
    cases.append(make_case(3, 5, 5, 2, 2))
    cases.append(make_case(2, 8, 8, 3, 1))
    cases.append(make_case(4, 10, 10, 2, 3))
    cases.append(make_case(2, 16, 16, 4, 2))
    cases.append(make_case(8, 32, 32, 4, 4))  # 上限附近
    cases.append(make_case(8, 32, 32, 5, 3))
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
    print("P5545 gen ok: 10/10")


if __name__ == "__main__":
    main()
