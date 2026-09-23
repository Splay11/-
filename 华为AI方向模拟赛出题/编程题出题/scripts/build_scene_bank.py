#!/usr/bin/env python3
"""从 华为机考题汇总 的 AI 岗编程题抽取业务背景，写入 scenes.json。"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DOMAIN_RULES = [
    ("混合专家 / 路由", ("专家", "moe", "token", "路由", "top-k", "topk")),
    ("注意力 / Transformer", ("attention", "注意力", "transformer", "query", "softmax", "rope")),
    ("推理服务 / KV Cache", ("kv", "cache", "paged", "推理", "decode", "prefill", "显存页")),
    ("训练资源 / 并行", ("npu", "gpu", "swap", "重计算", "流水线", "集群", "显存", "张量")),
    ("推荐 / 检索", ("推荐", "商品", "用户", "召回", "相似度", "特征向量")),
    ("数据采集 / 时序", ("采集", "时间戳", "传感器", "异常值", "插值", "质量标记")),
    ("基站 / 空间", ("基站", "曼哈顿", "核心点", "邻域", "坐标")),
    ("微调 / 对齐", ("lora", "微调", "rlhf", "奖励", "sft", "对齐")),
    ("视觉 / 卷积", ("卷积", "cnn", "图像", "patch", "特征图")),
    ("聚类 / 统计", ("聚类", "k-means", "kmeans", "高斯", "gmm", "方差")),
]


def classify_domain(text: str) -> str:
    low = text.lower()
    for name, keys in DOMAIN_RULES:
        if any(k.lower() in low for k in keys):
            return name
    return "其他工程场景"


def strip_heading(text: str) -> str:
    text = text.replace("\r\n", "\n")
    m = re.search(r"^#+\s*题目(?:内容|描述)\s*$", text, re.M)
    if m:
        text = text[m.end() :]
    cut = re.search(r"^#+\s*输入描述", text, re.M)
    if cut:
        text = text[: cut.start()]
    return text.strip()


def first_hook(body: str, limit: int = 420) -> str:
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    kept: list[str] = []
    n = 0
    for p in paras:
        if p.startswith("#") or p.startswith("$$"):
            continue
        if p.startswith("```"):
            continue
        compact = re.sub(r"\s+", "", p)
        if len(compact) < 8:
            continue
        kept.append(re.sub(r"\s+", " ", p))
        n += len(kept[-1])
        if n >= limit or len(kept) >= 3:
            break
    hook = " ".join(kept).strip()
    if len(hook) > 480:
        hook = hook[:477].rstrip() + "…"
    return hook


def is_mcq(text: str) -> bool:
    return "{{ select" in text or "{{ multiselect" in text


def iter_ai_prog(root: Path) -> list[dict]:
    rows: list[dict] = []
    for exam in sorted(root.iterdir()):
        if not exam.is_dir():
            continue
        name = exam.name
        if "AI方向" not in name or "非AI" in name:
            continue
        session = name.split("-", 1)[-1] if re.match(r"^\d+-", name) else name
        for prob in sorted(exam.iterdir()):
            if not (prob.is_dir() and re.fullmatch(r"P\d+", prob.name, re.I)):
                continue
            path = prob / "题面.md"
            if not path.exists() or path.stat().st_size == 0:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if is_mcq(text):
                continue
            body = strip_heading(text)
            hook = first_hook(body)
            if len(hook) < 12:
                continue
            rows.append(
                {
                    "pid": prob.name.upper(),
                    "session": session,
                    "domain": classify_domain(hook + "\n" + body[:800]),
                    "hook": hook,
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src",
        default=None,
        help="华为机考题汇总目录",
    )
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    here = Path(__file__).resolve()
    repo = next(
        (p for p in [here, *here.parents] if (p / "华为机考题汇总").is_dir()),
        here.parents[3],
    )
    src = Path(args.src).resolve() if args.src else (repo / "华为机考题汇总")
    out = Path(args.out).resolve() if args.out else (here.parent.parent / "scenes.json")
    rows = iter_ai_prog(src)
    payload = {"count": len(rows), "scenes": rows}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from collections import Counter

    print(f"写入 {out} ，共 {len(rows)} 条")
    print("domain：", dict(Counter(x["domain"] for x in rows)))


if __name__ == "__main__":
    main()
