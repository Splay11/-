#!/usr/bin/env python3
"""从 scenes.json 随机抽 3 条互异业务背景（尽量不同 domain）。"""
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
    if not isinstance(scenes, list) or len(scenes) < 3:
        raise SystemExit("无法继续：scenes.json 有效条目不足 3 条。")
    return scenes


def pick_three(scenes: list[dict], rng: random.Random) -> list[dict]:
    by_dom: dict[str, list[dict]] = defaultdict(list)
    for s in scenes:
        by_dom[str(s.get("domain") or "其他工程场景")].append(s)
    domains = list(by_dom)
    rng.shuffle(domains)
    picked: list[dict] = []
    used_pids: set[str] = set()
    for d in domains:
        if len(picked) >= 3:
            break
        cands = [x for x in by_dom[d] if str(x.get("pid")) not in used_pids]
        if not cands:
            continue
        x = rng.choice(cands)
        picked.append(x)
        used_pids.add(str(x.get("pid")))
    if len(picked) < 3:
        rest = [x for x in scenes if str(x.get("pid")) not in used_pids]
        rng.shuffle(rest)
        for x in rest:
            picked.append(x)
            used_pids.add(str(x.get("pid")))
            if len(picked) >= 3:
                break
    if len(picked) < 3:
        raise SystemExit("无法继续：抽不满 3 条互异 pid 的业务背景。")
    return picked[:3]


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
    picked = pick_three(scenes, rng)
    print(f"seed={seed}")
    print(json.dumps({"seed": seed, "picked": picked}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
