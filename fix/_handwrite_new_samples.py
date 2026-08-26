"""Hand-write legal new samples that do not reuse original signature lines."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from forbid_orig_sample import original_forbidden, sample_hits_original

LOG = Path(__file__).resolve().parent / "log"

HAND = {
    "P3359": [
        "2\npp\n1 2",
        "3\ndpd\n1 2\n2 3",
        "4\n????\n1 2\n2 3\n3 4",
    ],
    "P3747": [
        "1\nz",
        "2\naa",
        "4\nabba",
    ],
    "P3748": [
        "3\n1 0 1\n1 2\n1 3",
        "4\n1 1 0 1\n1 2\n2 3\n3 4",
        "2\n1 1\n1 2",
    ],
    "P3509": [
        "3\n7 7 7",
        "6\n1 1 1 2 2 2",
        "5\n9 8 7 8 9",
    ],
    "P1908": [
        "3\n1 1 1",
        "4\n2 2 1 1",
        "5\n1 2 1 2 3",
    ],
    "P2142": [
        "1\nxyz",
        "2\nab\ncd",
        "1\nhello",
    ],
    "P1451": [
        "2\n1 2\n2 1",
        "4\n2 1 4 3\n4 3 1 2",
        "3\n2 3 1\n1 3 2",
    ],
    "P1042": [
        "3\n0 1 0\n0 1 0",
        "2\n0 0\n1 1",
        "4\n1 0 1 0\n0 1 0 1",
    ],
}


def py_from_35(md: str) -> str | None:
    m = re.search(r"### Python\s+```(?:python)?\s*\n(.*?)```", md, re.S)
    if m and len(m.group(1).strip()) > 8:
        return m.group(1).strip()
    return None


def run_code(code: str, stdin_text: str, timeout: int = 8) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run(
            [sys.executable, path],
            input=stdin_text if stdin_text.endswith("\n") else stdin_text + "\n",
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "")[-400:] or f"exit {r.returncode}")
    return r.stdout.replace("\r\n", "\n").rstrip("\n")


def main() -> None:
    for pid, ins in HAND.items():
        d = LOG / pid
        fb = original_forbidden((d / "01_原始题面.md").read_text(encoding="utf-8"))
        py = py_from_35((d / "03.5_修改后的题解.md").read_text(encoding="utf-8"))
        if not py:
            print(pid, "NO PYTHON")
            continue
        samples = []
        for inp in ins:
            hit = sample_hits_original(inp, fb)
            if hit:
                print(pid, "HIT", hit, repr(inp))
                continue
            try:
                out = run_code(py, inp)
            except Exception as e:
                print(pid, "RUNFAIL", e, repr(inp))
                continue
            samples.append({"input": inp, "output": out, "explanation": "按题意模拟计算得到。"})
        if len(samples) < 2:
            print(pid, "FAIL only", len(samples))
            continue
        (d / "04_LLM生成的新样例.json").write_text(
            json.dumps({"samples": samples}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(pid, "wrote", len(samples), [s["output"][:40] for s in samples])


if __name__ == "__main__":
    main()
