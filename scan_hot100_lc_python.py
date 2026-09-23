# -*- coding: utf-8 -*-
"""
扫描 HOT100/*.md：按小节提取 LeetCode 题号，将本地 Python class Solution 中
与官网 Python3 模板「同名入口方法」的方法名、参数名（不含类型注解）比对。
类名须为 Solution；方法名、参数标识符须与官网一致。
"""
from __future__ import annotations

import ast
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

GRAPHQL_URL = "https://leetcode.com/graphql"
UA = "Mozilla/5.0 (compatible; LC-sig-scan/1.0)"


def load_id_slug() -> dict[str, str]:
    req = urllib.request.Request(
        "https://leetcode.com/api/problems/all/",
        headers={"User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    m: dict[str, str] = {}
    for p in data["stat_status_pairs"]:
        if p.get("paid_only"):
            continue
        st = p["stat"]
        m[str(st["frontend_question_id"])] = st["question__title_slug"]
    return m


QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    codeSnippets {
      lang
      code
    }
  }
}
"""


def fetch_official_python(slug: str) -> str | None:
    body = json.dumps(
        {"query": QUERY, "variables": {"titleSlug": slug}}
    ).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers={"User-Agent": UA, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.load(r)
    except Exception:
        return None
    if "errors" in resp:
        return None
    q = (resp.get("data") or {}).get("question") or {}
    for snip in q.get("codeSnippets") or []:
        if snip.get("lang") == "Python3":
            return snip.get("code") or ""
    for snip in q.get("codeSnippets") or []:
        if snip.get("lang") == "Python":
            return snip.get("code") or ""
    return None


def official_entry_sig(code: str) -> tuple[str | None, tuple[str, ...] | None, str | None]:
    """
    官网模板中 class Solution 内第一个非 dunder 的 def，作为入口方法。
    返回 (method_name, (param names without self), class_line) 或 (None, None, None)
    """
    if not code or "class Solution" not in code:
        return None, None, None
    # 官网片段常为「只有方法签名、无函数体」，补 pass 才能 ast.parse
    patched = _patch_empty_method_bodies(code)
    try:
        tree = ast.parse(patched)
    except SyntaxError:
        return None, None, None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Solution":
            class_line = f"class {node.name}:"
            for item in node.body:
                if not isinstance(item, ast.FunctionDef):
                    continue
                if item.name.startswith("__") or item.name.startswith("_"):
                    continue
                args = item.args.args
                if not args or args[0].arg != "self":
                    continue
                names = tuple(a.arg for a in args[1:])
                return item.name, names, class_line
    return None, None, None


def _patch_empty_method_bodies(code: str) -> str:
    """在 `def foo(...):` 后若下一行缩进不足（或空），插入 `pass` 以满足语法。"""
    lines = code.splitlines()
    inserts_after: dict[int, str] = {}
    for i, line in enumerate(lines):
        if not re.match(r"^\s*def\s+\w+\s*\(", line) or not line.rstrip().endswith(":"):
            continue
        cur_indent = len(line) - len(line.lstrip(" "))
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        need_pass = False
        if j >= len(lines):
            need_pass = True
        else:
            nxt = lines[j]
            ni = len(nxt) - len(nxt.lstrip(" "))
            if not nxt.strip() or ni <= cur_indent:
                need_pass = True
        if need_pass:
            inserts_after[i] = " " * (cur_indent + 4) + "pass"
    out: list[str] = []
    for i, line in enumerate(lines):
        out.append(line)
        if i in inserts_after:
            out.append(inserts_after[i])
    return "\n".join(out)


def local_method_sig(
    code: str, want_name: str
) -> tuple[str | None, tuple[str, ...] | None, str | None]:
    """在本地代码块中找 class Solution 里名为 want_name 的方法，返回其参数名元组。"""
    if not code or "class Solution" not in code:
        return None, None, None
    try:
        tree = ast.parse(_patch_empty_method_bodies(code))
    except SyntaxError:
        return None, None, None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Solution":
            class_line = f"class {node.name}:"
            for item in node.body:
                if not isinstance(item, ast.FunctionDef) or item.name != want_name:
                    continue
                args = item.args.args
                if not args or args[0].arg != "self":
                    continue
                names = tuple(a.arg for a in args[1:])
                return item.name, names, class_line
            return None, None, class_line
    return None, None, None


def first_python_solution_block(chunk: str) -> str | None:
    for fm in re.finditer(
        r"```\s*(?:python|py)\s*\n(.*?)```", chunk, re.DOTALL | re.IGNORECASE
    ):
        block = fm.group(1)
        if "class Solution" in block:
            return block
    return None


def extract_sections(text: str) -> list[tuple[str, int, int]]:
    """
    仅匹配 markdown 标题行（行首 # 开头）中的 Leetcode 题号，避免目录式「LeetCode 78.」行重复切分。
    返回 [(题号, 标题行结束位置, 下一标题行起点或文末), ...]
    """
    pat = re.compile(r"(?im)^#{1,6}\s.*Leetcode\s*(?P<num>\d+)\s*\.")
    matches = list(pat.finditer(text))
    fixed: list[tuple[str, int, int]] = []
    for i, m in enumerate(matches):
        num = m.group("num")
        sec_start = m.end()
        sec_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        fixed.append((num, sec_start, sec_end))
    return fixed


def scan_file(path: Path, id_slug: dict[str, str], cache: dict[str, str | None]):
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[dict[str, Any]] = []
    sections = extract_sections(text)
    if not sections:
        return rows
    for lc_id, sec_start, sec_end in sections:
        chunk = text[sec_start:sec_end]
        block = first_python_solution_block(chunk)
        slug = id_slug.get(lc_id)
        if slug not in cache:
            cache[slug] = fetch_official_python(slug) if slug else None
        official = cache.get(slug) if slug else None
        off_name, off_params, off_class = (
            official_entry_sig(official) if official else (None, None, None)
        )
        row: dict[str, Any] = {
            "file": path.name,
            "lc_id": lc_id,
            "slug": slug,
            "has_block": block is not None,
            "official_ok": bool(official and off_name),
            "off_name": off_name,
            "off_params": off_params,
        }
        if not slug:
            row["issue"] = "no_slug"
            rows.append(row)
            continue
        if not official:
            row["issue"] = "no_official_fetch"
            rows.append(row)
            continue
        if not off_name:
            row["issue"] = "no_official_method"
            rows.append(row)
            continue
        if not block:
            row["issue"] = "no_python_solution_block"
            rows.append(row)
            continue
        loc_name, loc_params, loc_class = local_method_sig(block, off_name)
        if loc_name is None:
            row["issue"] = "method_name_mismatch"
            row["detail"] = f"官网入口 {off_name}{off_params}，本地未找到同名方法"
            # 列出本地 Solution 里有哪些 def
            try:
                tree = ast.parse(block)
                alts = []
                for n in tree.body:
                    if isinstance(n, ast.ClassDef) and n.name == "Solution":
                        for it in n.body:
                            if isinstance(it, ast.FunctionDef) and not it.name.startswith(
                                "__"
                            ):
                                alts.append(it.name)
                row["local_methods"] = alts
            except SyntaxError:
                row["local_methods"] = ["<parse error>"]
            rows.append(row)
            continue
        if loc_params != off_params:
            row["issue"] = "param_names_mismatch"
            row["detail"] = f"方法 {off_name}: 本地参数 {loc_params} vs 官网 {off_params}"
            rows.append(row)
            continue
        row["issue"] = "ok"
        rows.append(row)
    return rows


def main():
    root = Path(__file__).resolve().parent
    hot_dir = root / "HOT100"
    id_slug = load_id_slug()
    cache: dict[str, str | None] = {}

    all_rows: list[dict[str, Any]] = []
    for md in sorted(hot_dir.glob("P*.md")):
        all_rows.extend(scan_file(md, id_slug, cache))

    bad = [r for r in all_rows if r.get("issue") != "ok"]
    out_path = root / "hot100_lc_api_mismatch.txt"
    lines = [
        "与 LeetCode 官网 Python3 模板不一致：方法名或参数名不同，或缺少 class Solution 代码块",
        f"共 {len(bad)} 条（总扫描小节 {len(all_rows)}）",
        "",
    ]
    for r in bad:
        lines.append(
            f"- {r['file']} | LC{r['lc_id']} | slug={r.get('slug')} | {r.get('issue')}"
        )
        if r.get("detail"):
            lines.append(f"  {r['detail']}")
        if r.get("local_methods"):
            lines.append(f"  本地 Solution 方法列表: {r['local_methods']}")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print("written", out_path)
    print("bad count", len(bad), "total", len(all_rows))


if __name__ == "__main__":
    main()
