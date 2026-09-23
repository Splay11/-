# -*- coding: utf-8 -*-
import os, subprocess, sys
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
os.makedirs(DATA, exist_ok=True)

SAMPLE = """4 3
0 1 2 -1
0.5 0.3 0.2
0.1 0.8 0.1
0.2 0.3 0.5
0.4 0.4 0.2"""


def make_case(seed, L, V, pad_ratio=0.2):
    rng = np.random.RandomState(seed)
    tokens = rng.randint(0, V, size=L).tolist()
    # 末尾若干 padding
    n_pad = max(0, int(L * pad_ratio))
    for i in range(L - n_pad, L):
        tokens[i] = -1
    logits = rng.randn(L, V)
    lines = [f"{L} {V}", " ".join(str(t) for t in tokens)]
    for row in logits:
        lines.append(" ".join(f"{x:.4f}" for x in row))
    return "\n".join(lines)


cases = [SAMPLE]
cases.append(make_case(1, 2, 2, 0.0))
cases.append(make_case(2, 3, 4, 0.0))
cases.append("""3 2
-1 -1 -1
0.1 0.2
0.3 0.4
0.5 0.6""")  # 全 padding -> 0
cases.append(make_case(4, 8, 5, 0.25))
cases.append(make_case(5, 16, 8, 0.3))
cases.append(make_case(6, 32, 16, 0.2))
cases.append(make_case(7, 48, 24, 0.15))
cases.append(make_case(8, 64, 32, 0.1))  # 上限
cases.append(make_case(9, 64, 32, 0.5))

assert len(cases) == 10
std = os.path.join(DIR, "std.py")
for i, text in enumerate(cases, 1):
    with open(os.path.join(DATA, f"{i}.in"), "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\r\n", "\n").rstrip("\n"))
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    p = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    out = p.stdout.replace("\r\n", "\n").rstrip("\n") + "\n"
    open(os.path.join(DATA, f"{i}.out"), "w", encoding="utf-8", newline="").write(out)
for i in range(1, 11):
    inp = open(os.path.join(DATA, f"{i}.in"), encoding="utf-8").read()
    exp = open(os.path.join(DATA, f"{i}.out"), encoding="utf-8").read()
    got = subprocess.run([sys.executable, std], input=inp, text=True, capture_output=True).stdout
    got = got.replace("\r\n", "\n").rstrip("\n") + "\n"
    if got != exp:
        raise SystemExit(f"mismatch {i}")
print("P5553 gen ok 10/10")
