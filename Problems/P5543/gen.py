# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5543)


def make_case(C, Hin, Win, Kh, Kw, stride, padding):
    # 保证输出至少 1x1
    Hp = Hin + 2 * padding
    Wp = Win + 2 * padding
    assert (Hp - Kh) // stride + 1 >= 1
    assert (Wp - Kw) // stride + 1 >= 1
    lines = [f"{C} {Hin} {Win}"]
    for _c in range(C):
        for _h in range(Hin):
            lines.append(" ".join(str(rng.randint(-5, 9)) for _ in range(Win)))
    lines.append(f"{C} {Kh} {Kw}")
    for _c in range(C):
        for _h in range(Kh):
            lines.append(" ".join(str(rng.randint(-2, 2)) for _ in range(Kw)))
    lines.append(f"{stride} {padding}")
    return "\n".join(lines)


SAMPLE = """2 3 3
1 2 3
4 5 6
7 8 9
1 2 3
4 5 6
7 8 9
2 2 2
1 0
0 1
1 0
0 1
1 0"""


def gen_inputs():
    cases = [SAMPLE.strip()]
    cases.append(make_case(1, 2, 2, 2, 2, 1, 0))  # 最小
    cases.append(make_case(1, 3, 3, 2, 2, 1, 1))  # padding
    cases.append(make_case(2, 4, 4, 3, 3, 2, 0))  # stride>1
    cases.append(make_case(3, 5, 5, 2, 2, 1, 0))
    cases.append(make_case(2, 6, 6, 3, 3, 1, 2))
    cases.append(make_case(4, 5, 5, 2, 3, 1, 0))
    cases.append(make_case(3, 7, 7, 4, 4, 2, 1))
    cases.append(make_case(4, 8, 8, 5, 5, 1, 2))  # 接近上限
    cases.append(make_case(4, 8, 8, 5, 5, 3, 2))
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
    print("P5543 gen ok: 10/10")


if __name__ == "__main__":
    main()
