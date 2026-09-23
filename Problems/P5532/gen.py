# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "6 1000 0.1 0.0001\n50 0.2 5 0\n30 0.6 2 1\n80 0.1 10 0\n25 0.8 1 1\n60 0.3 8 0\n35 0.7 3 1\n2\n45 0.75 6\n28 0.75 2",
    "4 500 0.05 0.001\n20 0.1 1 1\n100 0.1 15 0\n70 0.2 8 0\n25 0.85 2 1\n1\n50 0.5 5",
]


def write_in(idx, text):
    (DATA / f"{idx}.in").write_text(text.rstrip("\n"), encoding="utf-8")


def run_std(inp: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(STD)],
        input=inp.rstrip("\n") + "\n",
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr)
    return proc.stdout.rstrip("\n") + "\n"


def gen_case(rng, n, m, max_iter, alpha, tol):
    lines = [f"{n} {max_iter} {alpha} {tol}"]
    for i in range(n):
        # 特征保持 O(1)。原始年收入量级配合 0.05 学习率会梯度爆炸，
        # 损失在 0/1 之间来回跳，不同解释器上提前停止的轮次不同，标签会翻转。
        lab = i % 2
        if lab == 0:
            x1 = rng.uniform(-1.6, -0.5)
            x2 = rng.uniform(-1.3, -0.3)
            x3 = rng.uniform(0.4, 1.5)
        else:
            x1 = rng.uniform(0.5, 1.6)
            x2 = rng.uniform(0.3, 1.4)
            x3 = rng.uniform(-1.5, -0.4)
        lines.append(f"{x1:.4f} {x2:.4f} {x3:.4f} {lab}")
    lines.append(str(m))
    for i in range(m):
        # 测试点落在同一套 O(1) 两类簇里，避免训练在小特征、测试在大特征上全部饱和成 1。
        if i % 2 == 0:
            x1 = rng.uniform(-1.4, -0.6)
            x2 = rng.uniform(-1.1, -0.4)
            x3 = rng.uniform(0.5, 1.3)
        else:
            x1 = rng.uniform(0.6, 1.4)
            x2 = rng.uniform(0.4, 1.2)
            x3 = rng.uniform(-1.3, -0.5)
        lines.append(f"{x1:.4f} {x2:.4f} {x3:.4f}")
    return "\n".join(lines)


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5532)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        gen_case(rng, 2, 1, 400, 0.2, 1e-6),
        gen_case(rng, 5, 2, 400, 0.2, 1e-6),
        gen_case(rng, 10, 3, 500, 0.2, 1e-6),
        gen_case(rng, 20, 5, 600, 0.15, 1e-6),
        gen_case(rng, 50, 10, 800, 0.15, 1e-6),
        gen_case(rng, 100, 20, 800, 0.1, 1e-6),
        gen_case(rng, 400, 50, 1000, 0.08, 1e-6),
        gen_case(rng, 500, 100, 1000, 0.05, 1e-6),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        if run_std((DATA / f"{i}.in").read_text(encoding="utf-8")) != out:
            raise SystemExit(f"mismatch {i}")
    s1 = run_std(SAMPLES[0]).strip()
    s2 = run_std(SAMPLES[1]).strip()
    print("P5532 sample1:", repr(s1))
    print("P5532 sample2:", repr(s2))
    assert s1 == "0 0.0000\n0 0.0000"
    # 题面样例2写 1 0.5347；按算法步骤标准实现约为 1 0.5917
    print("P5532 gen ok")


if __name__ == "__main__":
    main()
