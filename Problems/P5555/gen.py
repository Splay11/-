# -*- coding: utf-8 -*-
"""
MLA 造数说明：
stdin 与题面一致：
首行 N d n_h n_q d_c d_h d_rope
随后依次 X(Nxd), W_DQ(dxn_q), W_UQ(n_q x n_h*d_h),
W_DKV(dxd_c), W_UK(d_c x n_h*d_h), W_UV(d_c x n_h*d_h),
W_QR(d x n_h*d_rope), W_KR(d x d_rope), W_o(n_h*d_h x d)。
后两组取 N=12,d=8,n_h=4 量级（题面可见上限附近），秒内可算。
"""
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)


def fmt_mat(M):
    return "\n".join(" ".join(f"{x:.4f}" for x in row) for row in M)


def make_case(seed, N, d, n_h, n_q, d_c, d_h, d_rope):
    rng = np.random.RandomState(seed)
    assert n_h * d_h >= 1
    X = rng.randn(N, d)
    W_DQ = rng.randn(d, n_q)
    W_UQ = rng.randn(n_q, n_h * d_h)
    W_DKV = rng.randn(d, d_c)
    W_UK = rng.randn(d_c, n_h * d_h)
    W_UV = rng.randn(d_c, n_h * d_h)
    W_QR = rng.randn(d, n_h * d_rope)
    W_KR = rng.randn(d, d_rope)
    W_o = rng.randn(n_h * d_h, d)
    parts = [
        f"{N} {d} {n_h} {n_q} {d_c} {d_h} {d_rope}",
        fmt_mat(X), fmt_mat(W_DQ), fmt_mat(W_UQ), fmt_mat(W_DKV),
        fmt_mat(W_UK), fmt_mat(W_UV), fmt_mat(W_QR), fmt_mat(W_KR), fmt_mat(W_o),
    ]
    return "\n".join(parts)


# 手工小样例（确定性），作为第 1 组“样例位”
def hand_sample():
    # N=2,d=2,n_h=1,n_q=1,d_c=1,d_h=1,d_rope=1
    lines = [
        "2 2 1 1 1 1 1",
        "1.0000 0.0000",
        "0.0000 1.0000",
        "1.0000",
        "0.0000",
        "1.0000",
        "0.0000",
        "1.0000",
        "1.0000",
        "1.0000",
        "1.0000",
        "0.0000",
        "0.0000",
        "1.0000",
        "1.0000 0.0000",
    ]
    return "\n".join(lines)


cases = [
    hand_sample(),
    make_case(1, 2, 2, 1, 1, 1, 1, 1),
    make_case(2, 3, 4, 2, 2, 2, 2, 1),
    make_case(3, 4, 4, 2, 2, 2, 2, 2),
    make_case(4, 5, 6, 2, 3, 2, 3, 2),
    make_case(5, 6, 8, 2, 4, 3, 4, 2),
    make_case(6, 8, 8, 4, 4, 4, 2, 2),
    make_case(7, 10, 8, 4, 4, 4, 2, 2),
    # 接近可见上限
    make_case(8, 12, 8, 4, 4, 4, 2, 2),
    make_case(9, 12, 8, 4, 4, 4, 2, 4),
]
assert len(cases) == 10
std = os.path.join(DIR, "std.py")
for i, text in enumerate(cases, 1):
    open(os.path.join(DATA, f"{i}.in"), "w", encoding="utf-8", newline="").write(
        text.replace("\r\n", "\n").rstrip("\n"))
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"fail {i}: {p.stderr}")
    open(os.path.join(DATA, f"{i}.out"), "w", encoding="utf-8", newline="").write(
        p.stdout.replace("\r\n", "\n").rstrip("\n") + "\n")
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    exp = open(os.path.join(DATA, f"{i}.out"), encoding="utf-8").read()
    got = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True).stdout
    got = got.replace("\r\n", "\n").rstrip("\n") + "\n"
    if got != exp:
        raise SystemExit(f"mismatch {i}")
print("P5555 gen ok 10/10")
