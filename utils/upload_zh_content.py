"""调用 POST /api/problem/upload_zh_content，上传或更新中文题面。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

from codefun_auth import dump_response, api_headers, require_https


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/upload_zh_content")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True)
    parser.add_argument(
        "--content-file",
        default=None,
        help="题面 Markdown 文件路径（与 --content、位置参数三选一）",
    )
    parser.add_argument("file", nargs="?", default=None, help="题面文件路径")
    parser.add_argument("--content", default=None, help="题面正文字符串")
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    path = args.content_file or args.file
    if path:
        content = Path(path).read_text(encoding="utf-8")
    elif args.content is not None:
        content = args.content
    else:
        print("请指定 --content-file、位置参数文件路径或 --content。", file=sys.stderr)
        sys.exit(1)
    if not content.strip():
        print("题面内容为空，接口会拒绝。", file=sys.stderr)
        sys.exit(1)

    url = f"{args.base_url.rstrip('/')}/api/problem/upload_zh_content"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json={"domainId": args.domain_id, "pid": args.pid.upper(), "content": content},
        timeout=(10, 120),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(),
    )
    dump_response(resp)
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
