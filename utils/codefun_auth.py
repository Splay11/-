"""CodeFun2000 对外 API 鉴权：站点秘钥 CF_API_KEY（X-Api-Key）。

会自动读取仓库根目录 `.env`（不覆盖已有环境变量）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

DEFAULT_BASE_URL = "https://codefun2000.com"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_dotenv(path: Path | None = None) -> None:
    env_file = path or (repo_root() / ".env")
    if not env_file.is_file():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def get_api_key() -> str:
    load_dotenv()
    return (
        os.environ.get("CF_API_KEY")
        or os.environ.get("CODEFUN_API_KEY")
        or ""
    ).strip()


def require_api_key() -> str:
    key = get_api_key()
    if not key:
        print(
            "缺少站点秘钥：请在项目根目录 .env 设置 CF_API_KEY，"
            "或在控制面板 /manage/external-api 查看后写入。",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return key


def api_headers(*, json_body: bool = True) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "X-Api-Key": require_api_key(),
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    return headers


def hydro_submit_account() -> tuple[str, str]:
    """submit_proxy 交题身份；不能替代 CF_API_KEY。"""
    load_dotenv()
    uname = (os.environ.get("HYDRO_API_UNAME") or "").strip()
    password = (os.environ.get("HYDRO_API_PASSWORD") or "").strip()
    if not uname or not password:
        print(
            "submit_proxy 需要 HYDRO_API_UNAME / HYDRO_API_PASSWORD（写在 .env）。",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return uname, password


def hydro_web_account() -> tuple[str, str]:
    """网页登录（题集编辑页 dag 等）；不能替代 CF_API_KEY。"""
    load_dotenv()
    uname = (os.environ.get("HYDRO_API_UNAME") or "").strip()
    password = (os.environ.get("HYDRO_API_PASSWORD") or "").strip()
    if not uname or not password:
        print(
            "网页登录需要 HYDRO_API_UNAME / HYDRO_API_PASSWORD（写在 .env）。",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return uname, password


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("出于通信安全考虑，BASE_URL 必须是 https:// 开头")


def problem_zip_base(base_url: str, domain_id: str | None = None) -> str:
    """压缩包接口。指定域时走 /d/<domainId>/api/problem-zip。"""
    base = base_url.rstrip("/")
    if domain_id:
        return f"{base}/d/{domain_id}/api/problem-zip"
    return f"{base}/api/problem-zip"


def dump_response(resp) -> None:
    print("HTTP", resp.status_code)
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)
