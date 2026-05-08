import os
import sys
import argparse
import requests

def require_https(url: str):
    if not url.startswith("https://"):
        raise ValueError("出于通信安全考虑，BASE_URL 必须是 https:// 开头")

def fail(message: str, code: int = 1):
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(code)

def main():
    parser = argparse.ArgumentParser(description="调用题面API，获取 Markdown 题面并写入文件")
    parser.add_argument("--base-url", required=True, help="例如 https://codefun2000.com")
    parser.add_argument("--domain-id", required=True, help="例如 system")
    parser.add_argument("--pid", required=True, help="例如 P1001")
    parser.add_argument("--output", required=True, help="输出 Markdown 文件路径，例如 ./P1001/题面.md")
    parser.add_argument("--ca-cert", default=None, help="可选：自签证书 CA 文件路径")
    args = parser.parse_args()

    try:
        require_https(args.base_url)
    except ValueError as e:
        fail(str(e))

    uname = os.getenv("HYDRO_API_UNAME")
    password = os.getenv("HYDRO_API_PASSWORD")
    if not uname or not password:
        fail("请先设置环境变量 HYDRO_API_UNAME / HYDRO_API_PASSWORD")

    verify = args.ca_cert if args.ca_cert else True
    timeout = (5, 20)

    params = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid,
    }

    url = f"{args.base_url.rstrip('/')}/api/problem/detail"
    try:
        resp = requests.get(url, params=params, timeout=timeout, verify=verify)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        fail(f"请求题面接口失败：{e}")

    try:
        data = resp.json()
    except ValueError:
        fail(f"接口返回非 JSON，HTTP {resp.status_code}，响应片段：{resp.text[:200]!r}")

    if not isinstance(data, dict):
        fail(f"接口返回格式错误，期望对象，实际：{type(data).__name__}")

    if "data" not in data:
        fail(f"接口返回缺少 data 字段：{data!r}")

    markdown_text = data["data"] or ""
    if not isinstance(markdown_text, str):
        fail(f"接口返回的 data 不是字符串，实际：{type(markdown_text).__name__}")

    output_path = os.path.abspath(args.output)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            fail(f"创建输出目录失败：{output_dir}，{e}")

    try:
        with open(output_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(markdown_text)
    except OSError as e:
        fail(f"写入文件失败：{output_path}，{e}")

    print(f"获取题面成功，已写入：{output_path}（长度：{len(markdown_text)} 字符）")

if __name__ == "__main__":
    main()