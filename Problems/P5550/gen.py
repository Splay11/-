# -*- coding: utf-8 -*-
# 题面 Lq,Lkv<=10,d<=8；后两组取满，秒内可算完。
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STD = os.path.join(ROOT, "std.py")
rng = random.Random(5550)

SAMPLE1 = """2 3 2
1.0 0.0
1.0 1.0
1.0 0.0
0.0 0.0
-1.0 1.0
1.0 0.0
0.0 1.0
1.0 0.0
0.0 1.0
1.0 0.0
0.0 1.0"""

SAMPLE2 = """1 4 3
1.0 2.0 3.0
0.5 0.5 0.5
1.0 1.0 1.0
-1.0 0.0 1.0
0.0 -1.0 0.0
0.0 1.0 0.0
0.0 0.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0
0.0 1.0 0.0
0.0 0.0 0.0
0.0 1.0 0.0
1.0 0.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0"""


def fmt_mat(M):
    return "\n".join(" ".join(f"{v:.4f}" for v in row) for row in M)


def rand_mat(r, c):
    return [[rng.uniform(-1, 1) for _ in range(c)] for _ in range(r)]


def make_case(Lq, Lkv, d):
    Xq = rand_mat(Lq, d)
    Xkv = rand_mat(Lkv, d)
    Wq, Wk, Wv = [rand_mat(d, d) for _ in range(3)]
    return "\n".join([f"{Lq} {Lkv} {d}", fmt_mat(Xq), fmt_mat(Xkv), fmt_mat(Wq), fmt_mat(Wk), fmt_mat(Wv)])


def gen_inputs():
    # SAMPLE2 题面多 1 行（15 行数据 vs 需要 14）；按 d=3 截断到 1+4+9 行矩阵浮点
    s2_nums = SAMPLE2.strip().split()
    # 保留头与恰好 1*3+4*3+3*3*3=42 个后续？头已含在 split 里：3 ints + 42 floats = 45 tokens
    # 题面共 3+45? 实际 SAMPLE2 行数导致 3+45=48 tokens，多 3 个 float（一行）
    toks = SAMPLE2.strip().split()
    need = 3 + 1 * 3 + 4 * 3 + 3 * 3 * 3
    SAMPLE2_FIXED = " ".join(toks[:3]) + "\n" + "\n".join(
        " ".join(toks[i:i + 3]) for i in range(3, need, 3)
    )
    cases = [SAMPLE1.strip(), SAMPLE2_FIXED.strip()]
    cases.append(make_case(1, 1, 1))
    cases.append(make_case(2, 2, 2))
    cases.append(make_case(3, 4, 3))
    cases.append(make_case(4, 5, 4))
    cases.append(make_case(5, 6, 5))
    cases.append(make_case(6, 8, 6))
    cases.append(make_case(10, 10, 8))  # 上限
    cases.append(make_case(10, 10, 8))
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
    print("P5550 gen ok: 10/10")


if __name__ == "__main__":
    main()
