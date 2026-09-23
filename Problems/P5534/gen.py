# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "4\n1 0 1 0\n0.9 0.1 0.8 0.2",
    "2\n1 0\n0.0 1.0",
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


def gen_case(rng, N, extreme=False):
    y = [rng.randint(0, 1) for _ in range(N)]
    if extreme:
        p = [0.0 if yi == 1 else 1.0 for yi in y]
    else:
        p = [round(rng.random(), 6) for _ in range(N)]
    lines = [str(N), " ".join(map(str, y)), " ".join(f"{pi:.6f}" for pi in p)]
    return "\n".join(lines)


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5534)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        gen_case(rng, 1),
        gen_case(rng, 3),
        gen_case(rng, 10),
        gen_case(rng, 20, extreme=True),
        gen_case(rng, 100),
        gen_case(rng, 1000),
        gen_case(rng, 5000),
        gen_case(rng, 10000),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        if run_std((DATA / f"{i}.in").read_text(encoding="utf-8")) != out:
            raise SystemExit(f"mismatch {i}")
    assert run_std(SAMPLES[0]).strip() == "0.16"
    assert run_std(SAMPLES[1]).strip() == "16.12"
    print("P5534 gen ok")


if __name__ == "__main__":
    main()
