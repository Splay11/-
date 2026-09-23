"""调用 POST /api/problem/create，新建题目。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import dump_response, api_headers, require_https


def _split_tags(raw: str | None):
    if raw is None:
        return None
    text = raw.strip()
    if not text:
        return None
    if text.startswith("["):
        return json.loads(text)
    return [p.strip() for p in text.split(",") if p.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/create")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True)
    parser.add_argument("--content-file", default=None, help="中文题面 Markdown 文件")
    parser.add_argument("file", nargs="?", default=None, help="题面文件路径")
    parser.add_argument("--content", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--hidden", action="store_true")
    parser.add_argument("--difficulty", type=int, default=None)
    parser.add_argument("--tag", default=None, help="Hydro 标签，逗号分隔或 JSON 数组")
    parser.add_argument("--alg-tag", default=None, help="算法标签，逗号分隔或 JSON 数组")
    parser.add_argument("--ai-alg-tags", default=None)
    parser.add_argument("--videosol", default=None)
    parser.add_argument("--trial-videosol", default=None)
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
        print("请指定 --content-file、位置参数或 --content。", file=sys.stderr)
        sys.exit(1)
    if not content.strip():
        print("题面内容为空。", file=sys.stderr)
        sys.exit(1)

    payload: dict = {
        "domainId": args.domain_id,
        "pid": args.pid.upper(),
        "content": content,
    }
    if args.title is not None:
        payload["title"] = args.title
    if args.hidden:
        payload["hidden"] = True
    if args.difficulty is not None:
        payload["difficulty"] = args.difficulty
    tags = _split_tags(args.tag)
    if tags is not None:
        payload["tag"] = tags
    alg = _split_tags(args.alg_tag)
    if alg is not None:
        payload["alg_tag"] = alg
    ai = _split_tags(args.ai_alg_tags)
    if ai is not None:
        payload["ai_alg_tags"] = ai
    if args.videosol is not None:
        payload["videosol"] = args.videosol
    if args.trial_videosol is not None:
        payload["trial_videosol"] = args.trial_videosol

    url = f"{args.base_url.rstrip('/')}/api/problem/create"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json=payload,
        timeout=(10, 120),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(),
    )
    dump_response(resp)
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
