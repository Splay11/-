# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "6 2\n10.0 20.0 5.0\n12.0 22.0 6.0\n11.0 21.0 4.0\n80.0 5.0 50.0\n82.0 6.0 48.0\n78.0 4.0 52.0",
    "4 2\n0.0 0.0 0.0\n1.0 1.0 1.0\n100.0 100.0 100.0\n99.0 99.0 99.0",
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


def gen_case(rng, n, k):
    lines = [f"{n} {k}"]
    for i in range(n):
        # 围绕若干中心造团，保证可分
        base = rng.randint(0, k - 1)
        cx = 20 * base + rng.uniform(0, 5)
        cy = 20 * ((base * 2) % 3) + rng.uniform(0, 5)
        cz = 10 * base + rng.uniform(0, 5)
        lines.append(f"{cx:.4f} {cy:.4f} {cz:.4f}")
    return "\n".join(lines)


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5530)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        "1 1\n50.0 50.0 50.0",
        gen_case(rng, 5, 2),
        gen_case(rng, 10, 3),
        gen_case(rng, 20, 4),
        gen_case(rng, 50, 5),
        gen_case(rng, 100, 10),
        gen_case(rng, 400, 20),
        gen_case(rng, 500, 50),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        if run_std((DATA / f"{i}.in").read_text(encoding="utf-8")) != out:
            raise SystemExit(f"mismatch {i}")
    exp1 = "11.00 21.00 5.00\n80.00 5.00 50.00"
    exp2 = "0.50 0.50 0.50\n99.50 99.50 99.50"
    assert run_std(SAMPLES[0]).strip() == exp1
    assert run_std(SAMPLES[1]).strip() == exp2
    print("P5530 gen ok")


if __name__ == "__main__":
    main()
