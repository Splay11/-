# -*- coding: utf-8 -*-
"""
批量修复题面中的字面量换行符 bug。

背景：LLM 在生成题面 JSON 时，把换行写成了字面量 "\\n"（反斜杠+n 两个字符），
而不是真正的换行符，导致 Markdown 渲染时不会换行。

本脚本：
1. 扫描所有 log/{pid}/05_拼接后的完整题面.md，找出含字面量 \\n 的题目
2. 对每个受影响题目，读取 03_LLM生成的新题面.json + 04_LLM生成的新样例.json，
   用修复后的 step5 逻辑重新拼接（把字面量 \\n 转换为真正换行符）
3. 调用 /api/problem/update 重新上传修复后的题面到平台

用法：
  python fix_newline_statements.py            # 扫描并修复所有受影响题目
  python fix_newline_statements.py --pids P4785 P1147   # 只修复指定题目
  python fix_newline_statements.py --dry-run  # 只扫描并重新拼接，不上传
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import requests

# 复用 rewrite_and_upload 的 step5 / step7 逻辑
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rewrite_and_upload as rau

BASE_URL = rau.BASE_URL
DOMAIN_ID = rau.DOMAIN_ID


def scan_affected() -> list[str]:
    """扫描所有 05_拼接后的完整题面.md，返回含字面量 \\n 的 PID 列表"""
    affected = []
    for f in sorted(glob.glob(str(rau.get_script_dir() / "log" / "*" / "05_拼接后的完整题面.md"))):
        pid = Path(f).parent.name
        with open(f, encoding="utf-8") as fh:
            content = fh.read()
        if "\\n" in content:
            affected.append(pid)
    return affected


def rebuild_statement(pid: str, log_dir: Path) -> tuple[str | None, str | None]:
    """
    读取 03 + 04 JSON，用修复后的 step5 重新拼接。
    返回 (title, content)；任一文件缺失返回 (None, None)
    """
    f03 = log_dir / "03_LLM生成的新题面.json"
    f04 = log_dir / "04_LLM生成的新样例.json"
    if not f03.exists() or not f04.exists():
        return None, None

    with open(f03, encoding="utf-8") as fh:
        problem_data = json.load(fh)
    with open(f04, encoding="utf-8") as fh:
        samples = json.load(fh).get("samples", [])

    def log(msg):
        pass

    content = rau.step5_assemble_final_statement(problem_data, samples, log, log_dir)
    title = problem_data.get("title", "")
    return title, content


def upload_statement(pid: str, title: str, content: str, log_dir: Path) -> bool:
    """调用 /api/problem/update 上传修复后的题面"""
    uname = os.environ.get("HYDRO_API_UNAME")
    password = os.environ.get("HYDRO_API_PASSWORD")
    if not uname or not password:
        print(f"[{pid}] 错误：缺少环境变量 HYDRO_API_UNAME / HYDRO_API_PASSWORD")
        return False

    payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
        "title": title,
        "content": content,
    }
    url = f"{BASE_URL}/api/problem/update"
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=(10, 60),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        print(f"[{pid}] 上传请求失败：{e}")
        return False

    try:
        body = resp.json()
    except Exception:
        body = resp.text

    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / "07_上传新题面结果.json", "w", encoding="utf-8") as fh:
        json.dump(body, fh, ensure_ascii=False, indent=2)

    if resp.ok:
        print(f"[{pid}] 上传成功")
        return True
    else:
        print(f"[{pid}] 上传失败 HTTP {resp.status_code}: {json.dumps(body, ensure_ascii=False)[:300]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="批量修复题面字面量换行符 bug")
    parser.add_argument("--pids", nargs="*", default=None, help="只修复指定 PID")
    parser.add_argument("--dry-run", action="store_true", help="只重新拼接，不上传")
    args = parser.parse_args()

    if args.pids:
        pids = args.pids
    else:
        pids = scan_affected()

    print(f"待处理题目数：{len(pids)}")
    results = {"success": [], "fail": [], "skipped": []}

    for pid in pids:
        log_dir = rau.get_log_dir(pid)
        title, content = rebuild_statement(pid, log_dir)
        if title is None or content is None:
            print(f"[{pid}] 跳过：缺少 03/04 JSON 文件")
            results["skipped"].append(pid)
            continue

        # 检查修复后是否还有字面量 \n
        if "\\n" in content:
            print(f"[{pid}] 警告：修复后仍含字面量 \\\\n")
            results["fail"].append(pid)
            continue

        if args.dry_run:
            print(f"[{pid}] (dry-run) 重新拼接完成，未上传")
            results["success"].append(pid)
            continue

        if upload_statement(pid, title, content, log_dir):
            results["success"].append(pid)
        else:
            results["fail"].append(pid)

    print("\n===== 汇总 =====")
    print(f"成功：{len(results['success'])}")
    print(f"失败：{len(results['fail'])}")
    print(f"跳过：{len(results['skipped'])}")
    if results["fail"]:
        print("失败列表：", results["fail"])
    if results["skipped"]:
        print("跳过列表：", results["skipped"])


if __name__ == "__main__":
    main()
