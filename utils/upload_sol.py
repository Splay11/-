"""上传题解到 /api/problem/upload_sol；账号密码从环境变量读取。"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("通信安全：BASE_URL 须为 https:// 开头")


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problem/upload_sol 上传题解")
    parser.add_argument(
        "--base-url",
        default="https://codefun2000.com",
        help="站点根地址，无末尾斜杠",
    )
    parser.add_argument("--domain-id", default="system", help="domainId，例如 system")
    parser.add_argument("--pid", required=True, help="题目 pid，例如 P4029")
    parser.add_argument(
        "--solution-file",
        default=None,
        help="题解 Markdown/HTML 等文本文件路径（与 --solution 二选一）",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="题解文件路径（与 --solution-file 等价）",
    )
    parser.add_argument(
        "--solution",
        default=None,
        help="题解正文字符串（小内容可用；大内容建议用文件）",
    )
    parser.add_argument("--user", default=None, help="覆盖环境变量 HYDRO_API_UNAME")
    parser.add_argument("--password", default=None, help="覆盖环境变量 HYDRO_API_PASSWORD")
    parser.add_argument("--ca-cert", default=None, help="可选：自签证书 CA 路径")
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)

    uname = args.user or os.environ.get("HYDRO_API_UNAME")
    password = args.password or os.environ.get("HYDRO_API_PASSWORD")
    if not uname or not password:
        print(
            "请设置环境变量 HYDRO_API_UNAME 与 HYDRO_API_PASSWORD，"
            "或传入 --user / --password。",
            file=sys.stderr,
        )
        sys.exit(1)

    solution_path = args.solution_file or args.file
    if solution_path:
        try:
            solution = Path(solution_path).read_text(encoding="utf-8")
        except OSError as e:
            print(f"读取文件失败: {solution_path}: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.solution is not None:
        solution = args.solution
    else:
        print("请指定 --solution-file、位置参数文件路径或 --solution。", file=sys.stderr)
        sys.exit(1)

    if not solution.strip():
        print("题解内容为空，接口会拒绝。", file=sys.stderr)
        sys.exit(1)

    url = f"{args.base_url.rstrip('/')}/api/problem/upload_sol"
    payload = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid.upper(),
        "solution": solution,
    }

    verify = args.ca_cert if args.ca_cert else True
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False

    try:
        resp = session.post(
            url,
            json=payload,
            timeout=(10, 120),
            verify=verify,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    print("HTTP", resp.status_code)
    try:
        body = resp.json()
        print(json.dumps(body, ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
