"""按 leetcode_core_bundle_paths.json 上传核心代码模式附加文件（compile.sh / config.yaml / template.* / user.*）。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

from leetcode_core_bundle_common import (
    MANIFEST_NAME,
    read_manifest,
    collect_file_contents_from_manifest,
    write_manifest,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="读取清单并上传 LeetCode 核心代码模式附加文件包"
    )
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument("--domain-id", required=True, help="domainId，例如 system")
    parser.add_argument("--pid", required=True, help="题目 pid，例如 P14207")
    parser.add_argument(
        "--problem-dir",
        required=True,
        help="题目根目录（用于默认 manifest 路径及刷新扫描）",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="清单 JSON 路径（默认 <problem-dir>/leetcode_core_bundle_paths.json）",
    )
    parser.add_argument(
        "--api-segment",
        default="upload_leetcode_core_bundle",
        help="接口路径段，默认 upload_leetcode_core_bundle",
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="可选：将请求体先写入该文件（大 payload 时使用）",
    )
    parser.add_argument("--user", default=None, help="覆盖环境变量 HYDRO_API_UNAME")
    parser.add_argument(
        "--password", default=None, help="覆盖环境变量 HYDRO_API_PASSWORD"
    )

    rg = parser.add_mutually_exclusive_group()
    rg.add_argument(
        "--refresh-manifest",
        dest="refresh",
        action="store_true",
        default=True,
        help="上传前重新扫描并写回 manifest（默认）",
    )
    rg.add_argument(
        "--no-refresh-manifest",
        dest="refresh",
        action="store_false",
        help="仅使用已有 manifest，不重新扫描",
    )

    args = parser.parse_args()

    uname = args.user or os.environ.get("HYDRO_API_UNAME")
    password = args.password or os.environ.get("HYDRO_API_PASSWORD")
    if not uname or not password:
        print(
            "请设置环境变量 HYDRO_API_UNAME 与 HYDRO_API_PASSWORD，"
            "或传入 --user / --password。",
            file=sys.stderr,
        )
        sys.exit(1)

    root = Path(args.problem_dir).resolve()
    manifest_path = (
        Path(args.manifest) if args.manifest else (root / MANIFEST_NAME)
    )

    if args.refresh:
        write_manifest(root, manifest_path)
        print(f"已刷新路径清单: {manifest_path}")

    if not manifest_path.is_file():
        print(f"路径清单文件不存在: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    doc = read_manifest(manifest_path)
    files_content, skipped = collect_file_contents_from_manifest(doc)

    if skipped:
        print(f"以下文件路径失效，已跳过: {', '.join(skipped)}", file=sys.stderr)

    if not files_content:
        print("无可上传的文件（全部缺失或路径失效），已退出。", file=sys.stderr)
        sys.exit(0)

    url = f"{args.base_url.rstrip('/')}/api/problem/{args.api_segment}"
    payload = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid,
        "files": files_content,
    }

    # 可选：先落盘请求体（便于调试或大文件）
    if args.body_file:
        body_path = Path(args.body_file)
        body_path.parent.mkdir(parents=True, exist_ok=True)
        body_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"请求体已写入: {body_path}")

    try:
        r = requests.post(url, json=payload, timeout=120)
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    print("HTTP", r.status_code)
    print(r.text)
    if not r.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
