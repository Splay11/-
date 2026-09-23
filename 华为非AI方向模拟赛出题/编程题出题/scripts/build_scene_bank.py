#!/usr/bin/env python3
"""从 华为机考题汇总 的非 AI 岗编程题抽取业务背景，写入 scenes.json。"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DOMAIN_RULES = [
    ("依赖 / 版本", ("依赖", "版本号", "软件包", "安装顺序", "兼容")),
    ("物流 / 仓储", ("仓库", "货架", "货物", "物流", "包裹", "运单", "库存", "装卸", "货仓")),
    ("通信 / 协议", ("报文", "协议", "端口", "连接", "会话", "帧", "带宽", "信道", "频段")),
    ("加密 / 编码", ("加密", "密钥", "异或", "十六进制", "循环移位")),
    ("回文 / 数位", ("回文", "数位", "进制", "回文数")),
    ("图 / 网络", ("节点", "边", "连通", "路由", "交换机", "拓扑", "邻接", "最短路", "线路")),
    ("网格 / 地图", ("网格", "地图", "迷宫", "城墙", "格子", "上下左右", "行 w 列", "h 行")),
    ("几何 / 坐标", ("曼哈顿", "欧几里得", "坐标", "落点", "平面", "距离之和")),
    ("区间 / 时间", ("区间", "时间窗", "预约", "时段", "会议", "放映", "覆盖")),
    ("树 / 层级", ("父节点", "子节点", "层级", "组织", "目录", "二叉树", "多叉")),
    ("字符串 / 解析", ("字符串", "子串", "括号", "编码", "匹配", "重复串", "同步字符")),
    ("调度 / 资源", ("调度", "工单", "优先级", "配额", "产线", "机器", "预算", "任务")),
    ("模拟 / 过程", ("队列", "栈", "指令", "操作序列", "模拟", "取号", "浏览器", "visit")),
    ("游戏 / 对战", ("怪兽", "技能", "生命值", "砖块", "探索", "魔法")),
    ("统计 / 数组", ("数组", "前缀", "滑动", "子数组", "窗口", "高度")),
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


def iter_non_ai_prog(root: Path) -> list[dict]:
    rows: list[dict] = []
    for exam in sorted(root.iterdir()):
        if not exam.is_dir():
            continue
        name = exam.name
        if "非AI" not in name:
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
    parser.add_argument("--src", default=None, help="华为机考题汇总目录")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    here = Path(__file__).resolve()
    repo = next(
        (p for p in [here, *here.parents] if (p / "华为机考题汇总").is_dir()),
        here.parents[3],
    )
    src = Path(args.src).resolve() if args.src else (repo / "华为机考题汇总")
    out = Path(args.out).resolve() if args.out else (here.parent.parent / "scenes.json")
    rows = iter_non_ai_prog(src)
    payload = {"count": len(rows), "scenes": rows}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from collections import Counter

    print(f"写入 {out} ，共 {len(rows)} 条")
    print("domain：", dict(Counter(x["domain"] for x in rows)))


if __name__ == "__main__":
    main()
