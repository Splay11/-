# -*- coding: utf-8 -*-
"""缺 04 时不要再把原题面样例抄进去；请改跑 _replace_copied_samples.py。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "log"


def main():
    pids = [
        l.strip()
        for l in Path(__file__).resolve().parent.joinpath("all.txt").read_text(encoding="utf-8-sig").splitlines()
        if l.strip()
    ]
    missing = []
    for p in pids:
        d = ROOT / p
        p04 = d / "04_LLM生成的新样例.json"
        p03 = d / "03_LLM生成的新题面.json"
        if p03.exists() and not p04.exists():
            missing.append(p)
    if missing:
        print("missing 04 (do not copy original samples):", missing)
        print("run: python _replace_copied_samples.py")
    else:
        print("all 04 present")


if __name__ == "__main__":
    main()
