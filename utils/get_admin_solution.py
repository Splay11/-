"""调用 GET /api/problem/admin_solution，获取单题管理员题解。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/admin_solution")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True)
    parser.add_argument(
        "--output",
        default=None,
        help="写入 Markdown 文件（取第一条题解）；缺省打印 JSON",
    )
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    url = f"{args.base_url.rstrip('/')}/api/problem/admin_solution"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.get(
        url,
        params={"domainId": args.domain_id, "pid": args.pid},
        timeout=(10, 60),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(json_body=False),
    )
    try:
        body = resp.json()
    except ValueError:
        print(resp.text[:500], file=sys.stderr)
        sys.exit(1)

    if args.output:
        items = body.get("data") if isinstance(body, dict) else []
        content = ""
        if isinstance(items, list) and items:
            content = items[0].get("content") or ""
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"HTTP {resp.status_code} 已写入 {args.output}（长度 {len(content)}）")
    else:
        print("HTTP", resp.status_code)
        print(json.dumps(body, ensure_ascii=False, indent=2))
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
