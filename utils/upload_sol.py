import argparse
import json
import os
from pathlib import Path

import requests


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("通信安全：BASE_URL 须为 https:// 开头")


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/upload_sol")
    parser.add_argument("--base-url", required=True, help="例如 https://codefun2000.com")
    parser.add_argument("--domain-id", required=True, help="例如 system")
    parser.add_argument("--pid", required=True, help="题目 pid，如 P4719")
    parser.add_argument(
        "--solution-file",
        default=None,
        help="题解 Markdown/HTML 等文本文件路径（与 --solution 二选一）",
    )
    parser.add_argument(
        "--solution",
        default=None,
        help="题解正文字符串（小内容可用；大内容建议用文件）",
    )
    parser.add_argument("--ca-cert", default=None, help="可选：自签证书 CA 路径")
    args = parser.parse_args()

    require_https(args.base_url)

    uname = os.environ.get("HYDRO_API_UNAME")
    password = os.environ.get("HYDRO_API_PASSWORD")
    if not uname or not password:
        raise SystemExit("请设置环境变量 HYDRO_API_UNAME 与 HYDRO_API_PASSWORD")

    if args.solution_file:
        solution = Path(args.solution_file).read_text(encoding="utf-8")
    elif args.solution is not None:
        solution = args.solution
    else:
        raise SystemExit("请指定 --solution-file 或 --solution")

    url = f"{args.base_url.rstrip('/')}/api/problem/upload_sol"
    payload = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid,
        "solution": solution,
    }

    verify = args.ca_cert if args.ca_cert else True
    resp = requests.post(
        url,
        json=payload,
        timeout=(10, 120),
        verify=verify,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    print("HTTP", resp.status_code)
    try:
        body = resp.json()
        print(json.dumps(body, ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)


if __name__ == "__main__":
    main()