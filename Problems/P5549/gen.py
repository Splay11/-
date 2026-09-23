# -*- coding: utf-8 -*-
# 题面 L,d<=8；后两组取满上限。样例 1 的 Wv 按题面原文写入（与打印输出可能因誊写不一致）。
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5549)

SAMPLE1 = """2 4 4 2
1.0 0.0 1.0 0.0
0.0 1.0 0.0 1.0
1.0 0.0 0.0 0.0
0.0 1.0 0.0 0.0
0.0 0.0 1.0 0.0
0.0 0.0 0.0 1.0
1.0 0.0
0.0 1.0
0.0 0.0
0.0 0.0
0.0 1.0
0.0 0.0
0.0 0.0
0.0 0.0
1.0 0.0 0.0 0.0
0.0 1.0 0.0 0.0
0.0 0.0 1.0 0.0
0.0 0.0 0.0 1.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{v:.4f}" for v in row) for row in M)


def rand_mat(r, c):
    return [[rng.uniform(-1, 1) for _ in range(c)] for _ in range(r)]


def make_case(L, d, hq, hkv):
    assert hq % hkv == 0 and d % hq == 0 and hkv <= hq <= d
    dkv = d * hkv // hq
    X = rand_mat(L, d)
    Wq = rand_mat(d, d)
    Wk = rand_mat(d, dkv)
    Wv = rand_mat(d, dkv)
    Wo = rand_mat(d, d)
    return "\n".join([f"{L} {d} {hq} {hkv}", fmt_mat(X), fmt_mat(Wq), fmt_mat(Wk), fmt_mat(Wv), fmt_mat(Wo)])


def gen_inputs():
    cases = [SAMPLE1.strip()]
    cases.append(make_case(1, 2, 2, 1))
    cases.append(make_case(2, 2, 2, 2))  # 退化为 MHA
    cases.append(make_case(2, 4, 4, 1))  # MQA
    cases.append(make_case(3, 4, 4, 2))
    cases.append(make_case(4, 6, 6, 3))
    cases.append(make_case(5, 6, 3, 1))
    cases.append(make_case(6, 8, 8, 2))
    cases.append(make_case(8, 8, 8, 4))  # 接近上限
    cases.append(make_case(8, 8, 8, 1))
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
    print("P5549 gen ok: 10/10")


if __name__ == "__main__":
    main()
