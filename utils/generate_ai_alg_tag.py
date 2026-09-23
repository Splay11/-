"""调用 POST /api/problem/generate_ai_alg_tag，生成并写入 AI 算法标签。"""
from __future__ import annotations

import argparse
import sys

import requests

from codefun_auth import dump_response, api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/generate_ai_alg_tag")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True)
    parser.add_argument(
        "--cover",
        action="store_true",
        help="覆盖已有 AI 算法标签（默认不覆盖）",
    )
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    url = f"{args.base_url.rstrip('/')}/api/problem/generate_ai_alg_tag"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json={
            "domainId": args.domain_id,
            "pid": args.pid.upper(),
            "cover": bool(args.cover),
        },
        timeout=(10, 180),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(),
    )
    dump_response(resp)
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
