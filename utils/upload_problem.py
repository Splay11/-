"""一键上传题目题面 + 题解到 CodeFun2000。

鉴权：项目根 `.env` 的 `CF_API_KEY`（X-Api-Key）。
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Dict

import requests

from codefun_auth import api_headers


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("安全要求：BASE_URL 须以 https:// 开头")


def auto_find(pid: str, suffixes: list) -> Dict[str, Optional[Path]]:
    """在当前目录或子目录中自动查找 pid 对应的题面 / 题解。"""
    cwd = Path.cwd()
    results: Dict[str, Optional[Path]] = {}
    for suffix in suffixes:
        name = f"{suffix}.md"
        # 1) {pid}/xxx.md
        candidate = cwd / pid / name
        if candidate.is_file():
            results[suffix] = candidate
            continue
        # 2) 递归搜索
        found = list(cwd.rglob(f"**/{pid}/{name}"))
        if found:
            results[suffix] = found[0]
        else:
            results[suffix] = None
    return results


def do_post(url: str, payload: dict, verify):
    session = requests.Session()
    session.trust_env = False
    resp = session.post(
        url,
        json=payload,
        timeout=(10, 120),
        verify=verify,
        headers=api_headers(),
    )
    try:
        body = resp.json()
    except Exception:
        body = resp.text[:500]
    # resp.json() 可能直接返回字符串（如 "success"）
    if not isinstance(body, dict):
        body = {"message": str(body)}
    return {"http": resp.status_code, "body": body, "ok": resp.ok}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="一键上传题目题面 + 题解到 CodeFun2000"
    )
    ap.add_argument("--base-url", default="https://codefun2000.com")
    ap.add_argument("--domain-id", default="system")
    ap.add_argument("--pid", required=True)
    ap.add_argument(
        "--statement",
        default=None,
        help="题面 Markdown 文件路径（默认自动查找 题面_改写_保IO.md）",
    )
    ap.add_argument(
        "--solution",
        default=None,
        help="题解 Markdown 文件路径（默认自动查找 题解.md）",
    )
    ap.add_argument("--skip-statement", action="store_true", help="跳过题面上传")
    ap.add_argument("--skip-solution", action="store_true", help="跳过题解上传")
    ap.add_argument("--ca-cert", default=None)
    ap.add_argument("--no-proxy", action="store_true")
    args = ap.parse_args()

    require_https(args.base_url)
    base = args.base_url.rstrip("/")

    pid = args.pid.upper()
    verify = args.ca_cert if args.ca_cert else True

    # ---------- 题面 ----------
    if not args.skip_statement:
        stmt_path: str | None = args.statement
        if stmt_path is None:
            found = auto_find(pid, ["题面_改写_保IO", "题面"])
            stmt_file = found.get("题面_改写_保IO") or found.get("题面")
            if stmt_file is None:
                print(f"[题面] 未找到 {pid}/题面_改写_保IO.md 或 {pid}/题面.md，"
                      f"请用 --statement 指定路径。", file=sys.stderr)
                sys.exit(1)
            stmt_path = str(stmt_file)

        md = Path(stmt_path).read_text(encoding="utf-8").strip()
        if not md:
            print("[题面] 文件为空，跳过。", file=sys.stderr)
        else:
            payload = {
                "domainId": args.domain_id,
                "pid": pid,
                "content": md,
            }
            result = do_post(f"{base}/api/problem/upload_zh_content", payload, verify)
            msg = result["body"].get("message", result["body"])
            icon = "OK" if result["ok"] else "FAIL"
            print(f"[题面] HTTP {result['http']}  {icon}  {msg}")

    # ---------- 题解 ----------
    if not args.skip_solution:
        sol_path: str | None = args.solution
        if sol_path is None:
            found = auto_find(pid, ["题解"])
            sol_file = found.get("题解")
            if sol_file is None:
                print(f"[题解] 未找到 {pid}/题解.md，请用 --solution 指定路径。",
                      file=sys.stderr)
                sys.exit(1)
            sol_path = str(sol_file)

        sol = Path(sol_path).read_text(encoding="utf-8").strip()
        if not sol:
            print("[题解] 文件为空，跳过。", file=sys.stderr)
        else:
            payload = {
                "domainId": args.domain_id,
                "pid": pid,
                "solution": sol,
            }
            result = do_post(f"{base}/api/problem/upload_sol", payload, verify)
            msg = result["body"].get("message", result["body"])
            icon = "OK" if result["ok"] else "FAIL"
            print(f"[题解] HTTP {result['http']}  {icon}  {msg}")


if __name__ == "__main__":
    main()
