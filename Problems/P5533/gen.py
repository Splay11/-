# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "2 3\n1.0 2.0 3.0\n0.0 0.0 0.0\n2 1",
    "3 2\n10.0 0.0\n0.0 10.0\n5.0 5.0\n0 1 0",
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


def gen_case(rng, N, K):
    lines = [f"{N} {K}"]
    for _ in range(N):
        logits = [rng.uniform(-5, 5) for _ in range(K)]
        lines.append(" ".join(f"{v:.4f}" for v in logits))
    labels = [rng.randint(0, K - 1) for _ in range(N)]
    lines.append(" ".join(map(str, labels)))
    return "\n".join(lines)


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5533)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        gen_case(rng, 1, 2),
        gen_case(rng, 2, 2),
        gen_case(rng, 3, 4),
        gen_case(rng, 5, 5),
        gen_case(rng, 10, 6),
        gen_case(rng, 20, 8),
        gen_case(rng, 50, 10),
        gen_case(rng, 100, 10),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        if run_std((DATA / f"{i}.in").read_text(encoding="utf-8")) != out:
            raise SystemExit(f"mismatch {i}")
    s1 = run_std(SAMPLES[0]).strip()
    s2 = run_std(SAMPLES[1]).strip()
    print("P5533 sample1:", repr(s1))
    print("P5533 sample2:", repr(s2))
    assert s1 == "0.41 1.10\n0.75\n0.09 0.24 -0.33\n0.33 -0.67 0.33"
    print("P5533 gen ok")


if __name__ == "__main__":
    main()
