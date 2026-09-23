#!/usr/bin/env python3
"""从 object.json 按 tag1/tag2 频次比例随机抽 15 单选 + 5 多选，写出一场模拟卷。"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SINGLE_N = 15
MULTI_N = 5
SINGLE_SCORE = 6
MULTI_SCORE = 12
BANDS = ("简单", "中等", "困难")
BAND_FILL_ORDER = ("中等", "困难", "简单")


def local_now() -> datetime:
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("Asia/Shanghai"))
    except Exception:
        return datetime.now()


def date_folder_name(dt: datetime) -> str:
    return f"{dt.month}.{dt.day}"


def unique_dir(root: Path, base: str) -> Path:
    candidate = root / base
    if not (candidate / "选择题").exists():
        return candidate
    n = 2
    while True:
        candidate = root / f"{base}-{n}"
        if not (candidate / "选择题").exists():
            return candidate
        n += 1


def load_bank(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(
            f"无法继续：题库为空或不存在：{path}\n请先保存 object.json 后再出题。"
        )
    raw = path.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    if not isinstance(data, list) or not data:
        raise SystemExit(f"无法继续：{path} 不是非空 JSON 数组。")
    return data


def norm_type(item: dict) -> str:
    t = str(item.get("type") or "").strip().lower()
    if t in {"single", "单选"}:
        return "single"
    if t in {"multi", "multiple", "多选"}:
        return "multi"
    answers = item.get("answer") or []
    return "multi" if len(answers) > 1 else "single"


def tag1_of(item: dict) -> str:
    return str(item.get("tag1") or "").strip() or "未标注"


def tag2_of(item: dict) -> str:
    return str(item.get("tag2") or "").strip() or "其他"


def difficulty_band(raw) -> str:
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = 4
    if n <= 3:
        return "简单"
    if n <= 5:
        return "中等"
    return "困难"


def even_band_quotas(k: int, available: dict[str, int]) -> dict[str, int]:
    """简单/中等/困难尽量均分；余数优先给中等、困难，避免全堆简单题。"""
    keys = [b for b in BAND_FILL_ORDER if available.get(b, 0) > 0]
    if not keys or k <= 0:
        return {}
    q = {b: 0 for b in BANDS}
    assigned = 0
    i = 0
    while assigned < k:
        progressed = False
        for _ in range(len(keys)):
            b = keys[i % len(keys)]
            i += 1
            if q[b] < available.get(b, 0) and assigned < k:
                q[b] += 1
                assigned += 1
                progressed = True
                if assigned >= k:
                    break
        if not progressed:
            break
    return {b: n for b, n in q.items() if n > 0}


def annotate(bank: list[dict]) -> list[dict]:
    out = []
    for i, item in enumerate(bank):
        if not isinstance(item, dict):
            continue
        options = item.get("options") or []
        answers = [str(a).strip().upper() for a in (item.get("answer") or []) if str(a).strip()]
        if not options or not answers:
            continue
        row = dict(item)
        row["_i"] = i
        row["_type"] = norm_type(item)
        row["_tag1"] = tag1_of(item)
        row["_tag2"] = tag2_of(item)
        row["_band"] = difficulty_band(item.get("difficulty"))
        row["_diff"] = item.get("difficulty")
        row["_answers"] = answers
        row["_options"] = [str(x) for x in options]
        out.append(row)
    return out


def largest_remainder_quotas(weights: dict[str, int], k: int) -> dict[str, int]:
    tags = [t for t, w in weights.items() if w > 0]
    if not tags or k <= 0:
        return {}
    n = len(tags)
    min_each = 1 if k >= n else 0
    base = {t: min(min_each, weights[t]) for t in tags}
    rem = k - sum(base.values())
    if rem < 0:
        rem = 0
    cap = {t: weights[t] - base[t] for t in tags}
    total_w = sum(weights[t] for t in tags) or 1
    exact = {t: rem * weights[t] / total_w for t in tags}
    extra = {t: min(cap[t], int(exact[t])) for t in tags}
    leftover = rem - sum(extra.values())
    by_frac = sorted(tags, key=lambda t: (exact[t] - int(exact[t]), weights[t]), reverse=True)
    for t in by_frac:
        if leftover <= 0:
            break
        if extra[t] < cap[t]:
            extra[t] += 1
            leftover -= 1
    if leftover:
        for t in sorted(tags, key=lambda x: -weights[x]):
            while leftover > 0 and extra[t] < cap[t]:
                extra[t] += 1
                leftover -= 1
    return {t: base[t] + extra[t] for t in tags if base[t] + extra[t] > 0}


def sample_by_tags(pool: list[dict], k: int, rng: random.Random) -> list[dict]:
    if k <= 0:
        return []
    if len(pool) < k:
        raise SystemExit(f"无法继续：该题型题库只有 {len(pool)} 道，需要 {k} 道。")
    w1 = Counter(x["_tag1"] for x in pool)
    q1 = largest_remainder_quotas(dict(w1), k)
    chosen: list[dict] = []
    used: set[int] = set()
    grouped1: dict[str, list[dict]] = defaultdict(list)
    for x in pool:
        grouped1[x["_tag1"]].append(x)

    for t1, n1 in q1.items():
        sub = grouped1[t1]
        w2 = Counter(x["_tag2"] for x in sub)
        q2 = largest_remainder_quotas(dict(w2), n1)
        grouped2: dict[str, list[dict]] = defaultdict(list)
        for x in sub:
            grouped2[x["_tag2"]].append(x)
        for t2, n2 in q2.items():
            cand = [x for x in grouped2[t2] if x["_i"] not in used]
            if len(cand) < n2:
                extra = [
                    x
                    for x in sub
                    if x["_i"] not in used and x not in cand
                ]
                rng.shuffle(extra)
                cand.extend(extra)
            if len(cand) < n2:
                raise SystemExit(f"无法继续：tag1={t1} tag2={t2} 可抽题不足 {n2}。")
            pick = rng.sample(cand, n2)
            for x in pick:
                used.add(x["_i"])
            chosen.extend(pick)

    if len(chosen) < k:
        rest = [x for x in pool if x["_i"] not in used]
        need = k - len(chosen)
        if len(rest) < need:
            raise SystemExit("无法继续：去重后可抽题不足。")
        chosen.extend(rng.sample(rest, need))
    elif len(chosen) > k:
        chosen = rng.sample(chosen, k)

    rng.shuffle(chosen)
    return chosen[:k]


def sample_by_tags_and_difficulty(pool: list[dict], k: int, rng: random.Random) -> list[dict]:
    """tag1/tag2 比例抽题后，再交换补齐简单/中等/困难，尽量保住考点分布。"""
    chosen = sample_by_tags(pool, k, rng)
    avail = Counter(x["_band"] for x in pool)
    target = even_band_quotas(k, dict(avail))
    used = {x["_i"] for x in chosen}
    chosen = list(chosen)

    def counts() -> Counter:
        return Counter(x["_band"] for x in chosen)

    for _ in range(120):
        cur = counts()
        surplus = [b for b in BANDS if cur[b] > target.get(b, 0)]
        deficit = [b for b in BANDS if cur[b] < target.get(b, 0)]
        if not surplus or not deficit:
            break
        rng.shuffle(surplus)
        rng.shuffle(deficit)
        swapped = False
        for sb in surplus:
            out_idxs = [i for i, x in enumerate(chosen) if x["_band"] == sb]
            rng.shuffle(out_idxs)
            for db in deficit:
                cand_all = [x for x in pool if x["_i"] not in used and x["_band"] == db]
                rng.shuffle(cand_all)
                for oi in out_idxs:
                    old = chosen[oi]
                    same_t1 = [x for x in cand_all if x["_tag1"] == old["_tag1"]]
                    same_t2 = [x for x in same_t1 if x["_tag2"] == old["_tag2"]]
                    cand = same_t2 or same_t1 or cand_all
                    if not cand:
                        continue
                    new = cand[0]
                    used.discard(old["_i"])
                    used.add(new["_i"])
                    chosen[oi] = new
                    swapped = True
                    break
                if swapped:
                    break
            if swapped:
                break
        if not swapped:
            break

    rng.shuffle(chosen)
    return chosen[:k]


def clean_stem(text: str) -> str:
    s = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if s.startswith("**") and s.endswith("**"):
        inner = s[2:-2].strip()
        s = inner
    return s.strip()


def extract_analysis(solution: str) -> str:
    text = (solution or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\n---+\s*$", "", text).strip()
    for marker in ("**解析：**", "**解析:**", "解析：", "解析:"):
        if marker in text:
            return text.split(marker, 1)[1].strip()
    lines = [ln for ln in text.split("\n") if not re.match(r"^(\*\*)?答案", ln.strip())]
    return "\n".join(lines).strip() or text


def option_text(item: dict, letter: str) -> str:
    idx = LETTERS.index(letter)
    opts = item["_options"]
    if idx >= len(opts):
        return ""
    return str(opts[idx]).strip()


def render_one_question(n: int, item: dict) -> str:
    kind = "select" if item["_type"] == "single" else "multiselect"
    stem = clean_stem(item.get("content") or "")
    lines = [f"**{n}、{stem}**", f"{{{{ {kind}({n}) }}}}"]
    for opt in item["_options"]:
        lines.append(f"- {opt}")
    return "\n".join(lines)


def render_statement(items: list[dict]) -> str:
    singles = [x for x in items if x["_type"] == "single"]
    multis = [x for x in items if x["_type"] == "multi"]
    parts = ["## 一、单选题"]
    for n, item in enumerate(singles, 1):
        parts.append(render_one_question(n, item))
        parts.append("")
    parts.append("## 二、多选题")
    for i, item in enumerate(multis):
        n = len(singles) + i + 1
        parts.append(render_one_question(n, item))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_solution(items: list[dict]) -> str:
    blocks = []
    for n, item in enumerate(items, 1):
        letters = item["_answers"]
        analysis = extract_analysis(str(item.get("solution") or ""))
        if item["_type"] == "single":
            letter = letters[0]
            ans_line = f"答案：{letter}.{option_text(item, letter)}"
        else:
            rows = [f"{L}.{option_text(item, L)}" for L in letters]
            ans_line = "答案：\n" + "\n".join(rows)
        blocks.append(f"## T{n}\n{ans_line}\n解析：{analysis}")
    return "\n\n".join(blocks).rstrip() + "\n"


def yaml_quote_key(n: int) -> str:
    return f"'{n}'"


def render_config(items: list[dict]) -> str:
    lines = ["type: objective", "answers:"]
    for n, item in enumerate(items, 1):
        letters = item["_answers"]
        key = yaml_quote_key(n)
        lines.append(f"  {key}:")
        if item["_type"] == "single":
            lines.append(f"    - {letters[0]}")
            lines.append(f"    - {SINGLE_SCORE}")
        else:
            lines.append(f"    - - {letters[0]}")
            for L in letters[1:]:
                lines.append(f"      - {L}")
            lines.append(f"    - {MULTI_SCORE}")
    return "\n".join(lines) + "\n"


def print_stats(bank: list[dict]) -> None:
    rows = annotate(bank)
    print(f"题库有效题数：{len(rows)}")
    print("type：", dict(Counter(x["_type"] for x in rows)))
    print("难度档：", dict(Counter(x["_band"] for x in rows)))
    print("difficulty 原始：", dict(sorted(Counter(x["_diff"] for x in rows).items(), key=lambda kv: (kv[0] is None, kv[0]))))
    print("tag1：")
    for k, v in Counter(x["_tag1"] for x in rows).most_common():
        print(f"  {k}: {v}")
    print("tag2：")
    for k, v in Counter(x["_tag2"] for x in rows).most_common():
        print(f"  {k}: {v}")


def print_paper_mix(items: list[dict]) -> None:
    print("本场 tag1：", dict(Counter(x["_tag1"] for x in items)))
    print("本场 tag2：", dict(Counter(x["_tag2"] for x in items)))
    print("本场 type：", dict(Counter(x["_type"] for x in items)))
    print("本场难度档：", dict(Counter(x["_band"] for x in items)))
    print("本场 difficulty：", dict(sorted(Counter(x["_diff"] for x in items).items(), key=lambda kv: (kv[0] is None, kv[0]))))


def main() -> None:
    parser = argparse.ArgumentParser(description="华为 AI 岗选择题模拟卷抽题")
    parser.add_argument(
        "--root",
        default=None,
        help="选择题出题根目录（含 object.json）",
    )
    parser.add_argument("--json", default=None, help="题库 JSON 路径")
    parser.add_argument("--date", default=None, help="日期目录名，默认当天 M.D，如 9.8")
    parser.add_argument("--seed", default=None, help="随机种子；默认每次随机")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有同名日期目录")
    parser.add_argument("--stats", action="store_true", help="只打印题库 tag 统计")
    args = parser.parse_args()

    here = Path(__file__).resolve()
    default_root = here.parent.parent
    root = Path(args.root).expanduser().resolve() if args.root else default_root
    json_path = Path(args.json).expanduser().resolve() if args.json else (root / "object.json")

    bank = load_bank(json_path)
    if args.stats:
        print_stats(bank)
        return

    rows = annotate(bank)
    singles = [x for x in rows if x["_type"] == "single"]
    multis = [x for x in rows if x["_type"] == "multi"]

    if args.seed is None:
        seed = random.SystemRandom().randrange(1, 2**31)
    else:
        seed = int(args.seed) if str(args.seed).isdigit() else abs(hash(args.seed)) % (2**31)
    rng = random.Random(seed)

    picked_s = sample_by_tags_and_difficulty(singles, SINGLE_N, rng)
    picked_m = sample_by_tags_and_difficulty(multis, MULTI_N, rng)
    paper = picked_s + picked_m

    dt = local_now()
    base = args.date.strip() if args.date else date_folder_name(dt)
    if args.overwrite:
        out_root = root / base
    else:
        out_root = unique_dir(root, base)
    out_dir = out_root / "选择题"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "选择题题面.md").write_text(render_statement(paper), encoding="utf-8")
    (out_dir / "题解.md").write_text(render_solution(paper), encoding="utf-8")
    (out_dir / "config.yaml").write_text(render_config(paper), encoding="utf-8")

    print(f"seed={seed}")
    print(f"日期目录：{out_root.name}")
    print(f"输出：{out_dir}")
    print(f"单选 {len(picked_s)}，多选 {len(picked_m)}")
    print_paper_mix(paper)
    print("题库 tag1 频次（供对照）：")
    for k, v in Counter(x["_tag1"] for x in rows).most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
