import os
import argparse
from pathlib import Path
import requests
import json
def require_https(url: str):
    if not url.startswith("https://"):
        raise ValueError("出于通信安全考虑，BASE_URL 必须是 https:// 开头")
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
    require_https(args.base_url)
    uname = os.getenv("HYDRO_API_UNAME")
    password = os.getenv("HYDRO_API_PASSWORD")
    if not uname or not password:
        raise RuntimeError("请先设置环境变量 HYDRO_API_UNAME / HYDRO_API_PASSWORD")
    code = Path(args.code_file).read_text(encoding="utf-8")
    input_text = ""
    if args.pretest and args.input_file:
        input_text = Path(args.input_file).read_text(encoding="utf-8")
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
    resp = requests.post(url, json=payload, timeout=timeout, verify=verify)
    resp.raise_for_status()
    body = resp.json()
    # 输出关键信息
    print("RID:", body.get("rid"))
    result = body.get("result", {})
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
