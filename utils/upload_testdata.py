import argparse
import json
import os
from pathlib import Path

import requests


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("通信安全：BASE_URL 须为 https:// 开头")


def collect_files(data_dir: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for p in data_dir.iterdir():
        if p.is_file() and (p.name.endswith(".in") or p.name.endswith(".out")):
            files[p.name] = p.read_text(encoding="utf-8")
    return files


def validate_pairs(files: dict[str, str]) -> None:
    stems: dict[str, set[str]] = {}
    for name in files:
        stem, ext = name.rsplit(".", 1)
        stems.setdefault(stem, set()).add(ext)
    for stem, exts in stems.items():
        if not {"in", "out"}.issubset(exts):
            raise ValueError(f"数据不成对：需要 {stem}.in 与 {stem}.out")


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/upload_testdata")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--domain-id", required=True)
    parser.add_argument("--pid", required=True)
    parser.add_argument("--data-dir", required=True, help="含 1.in 1.out ... 的目录")
    parser.add_argument("--ca-cert", default=None)
    ow = parser.add_mutually_exclusive_group()
    ow.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=True,
        help="覆盖已有测试数据并上传（默认，与接口默认一致）",
    )
    ow.add_argument(
        "--no-overwrite",
        dest="overwrite",
        action="store_false",
        help="若题目已有 .in/.out 测试数据则跳过上传",
    )
    args = parser.parse_args()

    require_https(args.base_url)

    uname = os.environ.get("HYDRO_API_UNAME")
    password = os.environ.get("HYDRO_API_PASSWORD")
    if not uname or not password:
        raise SystemExit("请设置环境变量 HYDRO_API_UNAME 与 HYDRO_API_PASSWORD")

    data_dir = Path(args.data_dir)
    if not data_dir.is_dir():
        raise SystemExit("data-dir 不存在或不是目录")

    files = collect_files(data_dir)
    if not files:
        raise SystemExit("目录中未找到 .in/.out 文件")
    validate_pairs(files)

    payload = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid,
        "files": files,
        "overwrite": bool(args.overwrite),
    }

    url = f"{args.base_url.rstrip('/')}/api/problem/upload_testdata"
    verify = args.ca_cert if args.ca_cert else True
    resp = requests.post(
        url,
        json=payload,
        timeout=(10, 300),
        verify=verify,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    print("HTTP", resp.status_code)
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)


if __name__ == "__main__":
    main()