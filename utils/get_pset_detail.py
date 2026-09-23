"""调用 GET /api/problems/detail，获取题单简介、画像和题目难度/标签摘要。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problems/detail")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--psid", required=True, help="题单 ObjectId")
    parser.add_argument("--output", default=None, help="写入 JSON 文件；缺省打印到控制台")
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    url = f"{args.base_url.rstrip('/')}/api/problems/detail"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.get(
        url,
        params={"domainId": args.domain_id, "psid": args.psid},
        timeout=(10, 60),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(json_body=False),
    )
    if args.output:
        Path(args.output).write_text(
            json.dumps(resp.json(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"HTTP {resp.status_code} 已写入 {args.output}")
    else:
        print("HTTP", resp.status_code)
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
