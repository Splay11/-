#!/usr/bin/env python3
"""从 scenes.json 随机抽 2 条互异业务背景（尽量不同 domain）。"""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def load_scenes(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f"无法继续：业务库不存在或为空：{path}\n请先运行 build_scene_bank.py")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    scenes = data.get("scenes") if isinstance(data, dict) else data
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise SystemExit("无法继续：scenes.json 有效条目不足 2 条。")
    return scenes


def pick_two(scenes: list[dict], rng: random.Random) -> list[dict]:
    by_dom: dict[str, list[dict]] = defaultdict(list)
    for s in scenes:
        by_dom[str(s.get("domain") or "其他工程场景")].append(s)
    domains = list(by_dom)
    rng.shuffle(domains)
    first_dom = domains[0]
    first = rng.choice(by_dom[first_dom])
    rest_doms = [d for d in domains if d != first_dom] or domains
    second_dom = rng.choice(rest_doms)
    cands = [x for x in by_dom[second_dom] if x.get("pid") != first.get("pid")]
    if not cands:
        cands = [x for x in scenes if x.get("pid") != first.get("pid")]
    second = rng.choice(cands)
    return [first, second]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", default=None)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    here = Path(__file__).resolve()
    bank = Path(args.bank).resolve() if args.bank else (here.parent.parent / "scenes.json")
    scenes = load_scenes(bank)
    if args.seed is None:
        seed = random.SystemRandom().randrange(1, 2**31)
    else:
        seed = int(args.seed) if str(args.seed).isdigit() else abs(hash(args.seed)) % (2**31)
    rng = random.Random(seed)
    picked = pick_two(scenes, rng)
    print(f"seed={seed}")
    print(json.dumps({"seed": seed, "picked": picked}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
