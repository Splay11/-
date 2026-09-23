"""调用 POST /api/problem/list，批量获取题目与管理员题解。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/list 批量获取题面与题解")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pids", nargs="+", default=None, help="题目编号列表，如 P1001 P1002")
    parser.add_argument("--query", default=None, help='查询条件 JSON，如 {"tag":"all"}')
    parser.add_argument("--latest", type=int, default=None, help="配合 --query，按题号倒序截取最新 N 道")
    parser.add_argument("--output-dir", default=None, help="每道题写入 <pid>_题面.md 与 <pid>_题解.md")
    parser.add_argument("--output-json", default=None, help="完整 JSON 输出路径")
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    if not args.pids and not args.query:
        print("请至少提供 --pids 或 --query。", file=sys.stderr)
        sys.exit(1)

    payload: dict = {"domainId": args.domain_id}
    if args.pids:
        payload["pids"] = [p.strip().upper() for p in args.pids if p.strip()]
    if args.query:
        try:
            payload["query"] = json.loads(args.query)
        except json.JSONDecodeError as e:
            print(f"--query 不是合法 JSON：{e}", file=sys.stderr)
            sys.exit(1)
    if args.latest is not None:
        payload["latest"] = args.latest

    url = f"{args.base_url.rstrip('/')}/api/problem/list"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json=payload,
        timeout=(15, 180),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(),
    )
    try:
        body = resp.json()
    except ValueError:
        print(resp.text[:500], file=sys.stderr)
        sys.exit(1)

    items = body.get("data") if isinstance(body, dict) else None
    if not isinstance(items, list):
        print("HTTP", resp.status_code)
        print(json.dumps(body, ensure_ascii=False, indent=2))
        sys.exit(0 if resp.ok else 1)

    if args.output_json:
        Path(args.output_json).write_text(
            json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"JSON 已写入 {args.output_json}")

    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for item in items:
            pid = str(item.get("pid") or "").strip().upper()
            if not pid:
                continue
            (out / f"{pid}_题面.md").write_text(item.get("content") or "", encoding="utf-8")
            sols = item.get("psdocs") or []
            sol_text = ""
            if isinstance(sols, list) and sols:
                sol_text = sols[0].get("content") or ""
            (out / f"{pid}_题解.md").write_text(sol_text, encoding="utf-8")
        print(f"已写入 {len(items)} 道题到 {out}")
    elif not args.output_json:
        print("HTTP", resp.status_code)
        for item in items:
            pid = item.get("pid")
            title = item.get("title")
            n_sol = len(item.get("psdocs") or [])
            tags = item.get("alg_tag") or []
            print(f"{pid}\t{title}\t题解{n_sol}篇\t{tags}")

    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
