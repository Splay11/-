"""调用 POST /api/problem/update，修改已有题目（只更新传入字段）。"""
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
    parser = argparse.ArgumentParser(description="调用 /api/problem/update")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", default="system")
    parser.add_argument("--pid", required=True, help="当前题目编号")
    parser.add_argument("--new-pid", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--content-file", default=None)
    parser.add_argument("--content", default=None)
    parser.add_argument("--hidden", dest="hidden", action="store_true", default=None)
    parser.add_argument("--visible", dest="hidden", action="store_false")
    parser.add_argument("--difficulty", type=int, default=None)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--alg-tag", default=None)
    parser.add_argument("--ai-alg-tags", default=None)
    parser.add_argument("--videosol", default=None)
    parser.add_argument("--trial-videosol", default=None)
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    payload: dict = {"domainId": args.domain_id, "pid": args.pid.upper()}
    if args.new_pid:
        payload["newPid"] = args.new_pid.upper()
    if args.title is not None:
        payload["title"] = args.title
    if args.content_file:
        payload["content"] = Path(args.content_file).read_text(encoding="utf-8")
    elif args.content is not None:
        payload["content"] = args.content
    if args.hidden is not None:
        payload["hidden"] = bool(args.hidden)
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

    if len(payload) <= 2:
        print("除 domainId/pid 外至少再提供一个要修改的字段。", file=sys.stderr)
        sys.exit(1)

    url = f"{args.base_url.rstrip('/')}/api/problem/update"
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
