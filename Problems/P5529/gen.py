# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"

SAMPLES = [
    "4\n1 0.9\n0 0.4\n1 0.6\n0 0.3",
    "6\n1 0.8\n0 0.7\n1 0.5\n0 0.6\n1 0.3\n0 0.2",
]


def write_in(idx, text):
    (DATA / f"{idx}.in").write_text(text.rstrip("\n"), encoding="utf-8")


def gen_case(rng, n, tie_prob=0.0):
    n_pos = rng.randint(1, n - 1)
    labels = [1] * n_pos + [0] * (n - n_pos)
    rng.shuffle(labels)
    preds = [round(rng.random(), 4) for _ in labels]
    if tie_prob > 0 and n >= 2:
        for i in range(n):
            if rng.random() < tie_prob:
                preds[i] = preds[rng.randint(0, n - 1)]
    lines = [str(n)]
    for y, p in zip(labels, preds):
        lines.append(f"{y} {p:.4f}")
    return "\n".join(lines)


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


def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(5529)
    cases = [
        SAMPLES[0],
        SAMPLES[1],
        gen_case(rng, 2),
        gen_case(rng, 5, 0.3),
        gen_case(rng, 20),
        gen_case(rng, 50, 0.2),
        gen_case(rng, 100),
        gen_case(rng, 200),
        gen_case(rng, 5000),
        gen_case(rng, 10000),
    ]
    for i, c in enumerate(cases, 1):
        write_in(i, c)
        out = run_std(c)
        (DATA / f"{i}.out").write_text(out, encoding="utf-8")
        got = run_std((DATA / f"{i}.in").read_text(encoding="utf-8"))
        if got != out:
            raise SystemExit(f"mismatch {i}")
    # 样例输出校准
    assert run_std(SAMPLES[0]).strip() == "1.0000"
    assert run_std(SAMPLES[1]).strip() == "0.5556"
    print("P5529 gen ok")


if __name__ == "__main__":
    main()
