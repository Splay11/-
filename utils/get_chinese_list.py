"""调用 GET /api/problems/chinese_list，获取题单内全部中文题面。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problems/chinese_list")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--psid", required=True, help="题单 ObjectId")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="将每道题写入 <pid>.md；缺省打印 JSON",
    )
    parser.add_argument("--output-json", default=None, help="完整 JSON 输出路径")
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    url = f"{args.base_url.rstrip('/')}/api/problems/chinese_list"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.get(
        url,
        params={"domainId": args.domain_id, "psid": args.psid},
        timeout=(10, 120),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(json_body=False),
    )
    try:
        body = resp.json()
    except ValueError:
        print(resp.text[:500], file=sys.stderr)
        sys.exit(1)

    if args.output_json:
        Path(args.output_json).write_text(
            json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"JSON 已写入 {args.output_json}")

    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        items = body.get("data") if isinstance(body, dict) else []
        count = 0
        for item in items or []:
            pid = str(item.get("pid") or "").strip()
            if not pid:
                continue
            (out / f"{pid}.md").write_text(item.get("content") or "", encoding="utf-8")
            count += 1
        print(f"已写入 {count} 个题面到 {out}")
    elif not args.output_json:
        print("HTTP", resp.status_code)
        print(json.dumps(body, ensure_ascii=False, indent=2))

    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
