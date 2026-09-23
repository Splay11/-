import argparse
import requests

from codefun_auth import api_headers, require_https

def main():
    parser = argparse.ArgumentParser(description="调用题面API，获取 Markdown 题面")
    parser.add_argument("--base-url", required=True, help="例如 https://codefun2000.com")
    parser.add_argument("--domain-id", required=True, help="例如 system")
    parser.add_argument("--pid", required=True, help="例如 P1001")
    parser.add_argument("--ca-cert", default=None, help="可选：自签证书 CA 文件路径")
    args = parser.parse_args()

    require_https(args.base_url)

    verify = args.ca_cert if args.ca_cert else True
    timeout = (5, 20)

    params = {
        "domainId": args.domain_id,
        "pid": args.pid,
    }

    url = f"{args.base_url.rstrip('/')}/api/problem/detail"
    session = requests.Session()
    session.trust_env = False
    resp = session.get(
        url,
        params=params,
        timeout=timeout,
        verify=verify,
        headers=api_headers(json_body=False),
    )
    resp.raise_for_status()
    data = resp.json()

    if "data" not in data:
        print("接口返回异常：", data)
        return

    markdown_text = data["data"] or ""
    print(markdown_text)

if __name__ == "__main__":
    main()