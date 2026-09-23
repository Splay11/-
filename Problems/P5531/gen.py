# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "5\n1.0 2.1\n2.0 4.9\n3.0 7.2\n4.0 9.8\n5.0 12.1\n1",
    "4\n0.0 1.0\n1.0 2.0\n2.0 5.0\n3.0 10.0\n2",
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


def gen_case(rng, N, degree):
    # y ≈ poly(x) + noise
    coef = [rng.uniform(-2, 2) for _ in range(degree + 1)]
    lines = [str(N)]
    xs = []
    for i in range(N):
        x = rng.uniform(-5, 5)
        xs.append(x)
        y = 0.0
        for c in coef:
            y = y * x + c  # horner from high degree? actually coef[0] is a_n
        # recompute properly
        y = sum(coef[j] * (x ** (degree - j)) for j in range(degree + 1))
        y += rng.uniform(-0.05, 0.05)
        lines.append(f"{x:.6f} {y:.6f}")
    lines.append(str(degree))
    return "\n".join(lines)


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5531)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        gen_case(rng, 3, 1),
        gen_case(rng, 5, 2),
        gen_case(rng, 10, 3),
        gen_case(rng, 20, 4),
        gen_case(rng, 50, 5),
        gen_case(rng, 100, 8),
        gen_case(rng, 400, 10),
        # 20 阶范德蒙德在不同 BLAS 上第 4 位小数会分叉，收到 3 阶。
        gen_case(rng, 80, 3),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        if run_std((DATA / f"{i}.in").read_text(encoding="utf-8")) != out:
            raise SystemExit(f"mismatch {i}")
    s1 = run_std(SAMPLES[0]).strip()
    s2 = run_std(SAMPLES[1]).strip()
    assert s1 == "2.49 -0.25"
    assert s2 == "1.00 0.00 1.00"
    print("P5531 gen ok", s1, s2)


if __name__ == "__main__":
    main()
