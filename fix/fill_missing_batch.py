"""只给缺失产物的题目补 03/03.5/04，不覆盖已有 Agent 文件。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import complete_artifacts as ca
import light_restyle_03 as lr


def main() -> None:
    pids = [l.strip() for l in (ROOT / "all.txt").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    log = ROOT / "log"
    did = []
    fail = []
    for pid in pids:
        d = log / pid
        p03 = d / "03_LLM生成的新题面.json"
        p35 = d / "03.5_修改后的题解.md"
        p04 = d / "04_LLM生成的新样例.json"
        p02 = d / "02_原始完整题解.md"
        if p03.exists() and p35.exists() and p04.exists():
            continue
        if not (d / "01_原始题面.md").exists():
            fail.append((pid, "no 01"))
            continue
        try:
            if not p03.exists():
                lr.process(pid)
            if p02.exists() and (not p35.exists() or not p04.exists()):
                ca.process(pid, force_solution=not p35.exists(), force_samples=not p04.exists())
            did.append(pid)
        except SystemExit as e:
            fail.append((pid, str(e)[:200]))
        except Exception as e:
            fail.append((pid, str(e)[:200]))
    print("filled", len(did))
    print("fail", fail)


if __name__ == "__main__":
    main()
