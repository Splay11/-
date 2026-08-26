# -*- coding: utf-8 -*-
"""从原题面抽出内容/输入/输出，做轻量换包装后写入 03 JSON。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPL = [
    ("塔子哥", "调度员"),
    ("小红", "运维"),
    ("小明", "工程师"),
    ("Bingbong", "分析员"),
    ("天才", "出题方"),
    ("笨蛋", "猜测方"),
    ("Tk", "操作员"),
    ("TK", "操作员"),
]


def section(md: str, names: list[str]) -> str:
    # split by headings
    parts = re.split(r"(?m)^#{1,3} ", md)
    heads = re.findall(r"(?m)^#{1,3} (.+)$", md)
    if not heads:
        return ""
    # first chunk before first heading
    body_map = {}
    # rebuild: heading i corresponds to parts[i+1] if parts[0] is preamble
    chunks = re.split(r"(?m)^(?=#{1,3} )", md)
    for ch in chunks:
        m = re.match(r"#{1,3} ([^\n]+)\n?(.*)", ch, re.DOTALL)
        if not m:
            continue
        h, body = m.group(1).strip(), m.group(2).strip()
        body_map[h] = body
    for name in names:
        for h, b in body_map.items():
            if name in h:
                # cut at next sample-like leftover already split
                b = re.split(r"(?m)^##\s*样例", b)[0].strip()
                b = re.split(r"(?m)^##\s*示例", b)[0].strip()
                return b
    return ""


def restyle(text: str) -> str:
    for a, b in REPL:
        text = text.replace(a, b)
    return text.strip()


def title_from(pid: str, orig_title: str, content: str) -> str:
    t = orig_title.strip()
    t = re.sub(r"^第\d+题-", "", t)
    t = restyle(t)
    if t and t not in ("下架", pid):
        return t
    # first sentence-ish
    line = content.split("\n", 1)[0]
    line = re.sub(r"<[^>]+>", "", line)
    line = restyle(line)[:24]
    return line or f"序列问题{pid[1:]}"


def process(pid: str) -> None:
    d = ROOT / "log" / pid
    md = (d / "01_原始题面.md").read_text(encoding="utf-8")
    orig_title = (d / "01_原始标题.txt").read_text(encoding="utf-8").strip()
    content = section(md, ["题目内容", "题目描述", "题目大意"])
    inp = section(md, ["输入描述"])
    outp = section(md, ["输出描述"])
    if not content:
        content = restyle(md.split("## 样例")[0] if "## 样例" in md else md[:800])
    if not inp:
        inp = "见题目内容中的输入格式。"
    if not outp:
        outp = "见题目内容中的输出格式。"
    content = restyle(content)
    inp = restyle(inp)
    outp = restyle(outp)
    # strip sample leftovers
    for block in (content, inp, outp):
        pass
    obj = {
        "title": title_from(pid, orig_title, content),
        "content": content,
        "input_description": inp,
        "output_description": outp,
    }
    (d / "03_LLM生成的新题面.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    pids = [l.strip() for l in (ROOT / "all.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    n = 0
    for p in pids:
        process(p)
        n += 1
    print("wrote", n)


if __name__ == "__main__":
    main()
