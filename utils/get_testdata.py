"""调用 GET /api/problem/get_testdata，下载题目测试数据。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/get_testdata")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True)
    parser.add_argument(
        "--output-dir",
        default=None,
        help="把 files 映射写入该目录；缺省打印 JSON",
    )
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    url = f"{args.base_url.rstrip('/')}/api/problem/get_testdata"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.get(
        url,
        params={"domainId": args.domain_id, "pid": args.pid},
        timeout=(15, 180),
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

    files = body.get("files") if isinstance(body, dict) else None
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        if not isinstance(files, dict) or not files:
            print("接口未返回 files，无法落盘。", file=sys.stderr)
            print(json.dumps(body, ensure_ascii=False, indent=2))
            sys.exit(1)
        for name, content in files.items():
            dest = out / Path(str(name)).name
            dest.write_text(content if isinstance(content, str) else str(content), encoding="utf-8")
        print(f"已写入 {len(files)} 个文件到 {out}")
    elif not args.output_json:
        print("HTTP", resp.status_code)
        print(json.dumps(body, ensure_ascii=False, indent=2))

    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
