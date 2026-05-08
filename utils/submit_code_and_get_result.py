import os
import sys
import argparse
from pathlib import Path
import requests
import json
def require_https(url: str):
    if not url.startswith("https://"):
        raise ValueError("出于通信安全考虑，BASE_URL 必须是 https:// 开头")

def fail(message: str, code: int = 1):
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(code)

def main():
    parser = argparse.ArgumentParser(description="调用提交代理API并获取详细中文结果")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--domain-id", required=True)
    parser.add_argument("--pid", required=True)
    parser.add_argument("--lang", required=True, help="如 py.py3 / cc.cc14o2")
    parser.add_argument("--code-file", required=True, help="本地代码文件路径")
    parser.add_argument("--pretest", action="store_true")
    parser.add_argument("--input-file", default=None, help="pretest 时可选输入文件")
    parser.add_argument("--timeout-ms", type=int, default=60000)
    parser.add_argument("--poll-interval-ms", type=int, default=1000)
    parser.add_argument("--ca-cert", default=None)
    args = parser.parse_args()
    try:
        require_https(args.base_url)
    except ValueError as e:
        fail(str(e))

    if args.timeout_ms <= 0:
        fail("--timeout-ms 必须为正整数")
    if args.poll_interval_ms <= 0:
        fail("--poll-interval-ms 必须为正整数")

    uname = os.getenv("HYDRO_API_UNAME")
    password = os.getenv("HYDRO_API_PASSWORD")
    if not uname or not password:
        fail("请先设置环境变量 HYDRO_API_UNAME / HYDRO_API_PASSWORD")

    code_path = Path(args.code_file)
    if not code_path.is_file():
        fail(f"代码文件不存在：{code_path}")
    try:
        code = code_path.read_text(encoding="utf-8")
    except OSError as e:
        fail(f"读取代码文件失败：{code_path}，{e}")

    input_text = ""
    if args.pretest and args.input_file:
        input_path = Path(args.input_file)
        if not input_path.is_file():
            fail(f"输入文件不存在：{input_path}")
        try:
            input_text = input_path.read_text(encoding="utf-8")
        except OSError as e:
            fail(f"读取输入文件失败：{input_path}，{e}")
    payload = {
        "domainId": args.domain_id,
        "uname": uname,
        "password": password,
        "pid": args.pid,
        "lang": args.lang,
        "code": code,
        "pretest": args.pretest,
        "input": input_text,
        "baseUrl": args.base_url.rstrip("/"),
        "timeoutMs": args.timeout_ms,
        "pollIntervalMs": args.poll_interval_ms,
    }
    verify = args.ca_cert if args.ca_cert else True
    timeout = (8, 180)
    url = f"{args.base_url.rstrip('/')}/api/problem/submit_proxy"
<<<<<<< HEAD
    session = requests.Session()
    session.trust_env = False
    resp = session.post(url, json=payload, timeout=timeout, verify=verify)
    resp.raise_for_status()
    body = resp.json()
=======
    try:
        resp = requests.post(url, json=payload, timeout=timeout, verify=verify)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        fail(f"提交接口请求失败：{e}")

    try:
        body = resp.json()
    except ValueError:
        fail(f"接口返回非 JSON，HTTP {resp.status_code}，响应片段：{resp.text[:200]!r}")

    if not isinstance(body, dict):
        fail(f"接口返回格式错误，期望对象，实际：{type(body).__name__}")

>>>>>>> a638131c8242a5683837a95699a8094384c40123
    # 输出关键信息
    print("RID:", body.get("rid"))
    result = body.get("result", {})
    if not isinstance(result, dict):
        fail(f"接口返回的 result 字段格式错误，实际：{type(result).__name__}")
    print("是否完全通过:", result.get("isAccepted"))
    print("错误种类:", result.get("errorType"))
    print("状态:", (result.get("status") or {}).get("textZh"))
    print("编译信息:", result.get("compilerMessage"))
    print("运行信息:", result.get("runtimeMessage"))
    print("失败点:", json.dumps(result.get("firstFailedCase"), ensure_ascii=False))
    print("完整返回:")
    print(json.dumps(body, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
