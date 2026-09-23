"""爬取 sspoffer 题单题面（只保存题面，不含题解）。

题单目录接口公开；单题题面接口要求登录，请求头 `s` 为站点 Cookie `token`。

令牌来源（按顺序）：
1. 命令行 --token
2. 环境变量 SSPOFFER_TOKEN，或仓库根目录 .env 里的同名项
3. 本机 Edge 已登录 Cookie（Edge 完全退出后才能读到）

示例：
  python utils/crawl_sspoffer_oj.py --card-id 47
  python utils/crawl_sspoffer_oj.py --card-id 47 --token <token>
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

import requests

BASE = "https://www.sspoffer.com"
API = BASE + "/bapeApi"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_dotenv() -> None:
    env_file = repo_root() / ".env"
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


def fail(message: str, code: int = 1) -> None:
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(code)


def session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": BASE + "/",
        }
    )
    return s


def api_get(http: requests.Session, path: str, query: dict, token: str | None = None) -> dict:
    headers = {}
    if token:
        headers["s"] = token
        headers["Cookie"] = f"token={token}"
    last_err = None
    for attempt in range(3):
        try:
            resp = http.get(API + path, params=query, headers=headers, timeout=(8, 40))
            resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, dict):
                raise RuntimeError(f"返回不是对象：{type(data).__name__}")
            return data
        except (requests.RequestException, ValueError, RuntimeError) as e:
            last_err = e
            time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(str(last_err))


def walk_questions(nodes, path: list[str], out: list[dict]) -> None:
    for node in nodes or []:
        title = (node.get("title") or "").strip()
        here = path + [title] if title else path
        for q in node.get("questions") or []:
            out.append(
                {
                    "questionId": str(q.get("questionId")),
                    "title": q.get("questionTitle") or "",
                    "hardLevel": q.get("hardLevel") or "",
                    "vip": bool(q.get("vip")),
                    "detailUrl": q.get("detailUrl") or "",
                    "tags": q.get("questionAlias") or [],
                    "groupPath": here,
                }
            )
        walk_questions(node.get("groupInfos") or [], here, out)


def fetch_catalog(http: requests.Session, card_id: int) -> tuple[dict, list[dict]]:
    page = 1
    card_info = {}
    items = []
    while True:
        data = api_get(
            http,
            "/question/paper/question-list",
            {
                "paperCardId": card_id,
                "pageNumber": page,
                "pageSize": 500,
                "searchContent": "",
            },
        )
        if data.get("code") != 0:
            fail(f"题单接口失败：code={data.get('code')} msg={data.get('msg')}")
        body = data.get("data") or {}
        if not card_info:
            card_info = body.get("cardInfo") or {}
        info = body.get("questionInfo") or {}
        batch = info.get("items") or []
        items.extend(batch)
        if not info.get("hasMore"):
            break
        page += 1
        if page > 50:
            break
    questions = []
    walk_questions(items, [], questions)
    return card_info, questions


def safe_filename(text: str) -> str:
    text = re.sub(r'[\\/:*?"<>|]', "_", text)
    text = re.sub(r"\s+", " ", text).strip().rstrip(".")
    return text[:60] or "untitled"


def read_edge_token() -> str | None:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return None
    root = Path(local) / "Microsoft" / "Edge" / "User Data"
    cookies = root / "Default" / "Network" / "Cookies"
    local_state = root / "Local State"
    if not cookies.is_file() or not local_state.is_file():
        return None
    try:
        import win32crypt
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print("未安装 win32crypt/cryptography，跳过读取 Edge Cookie。")
        return None

    state = json.loads(local_state.read_text(encoding="utf-8"))
    enc_key = base64.b64decode(state["os_crypt"]["encrypted_key"])
    if enc_key.startswith(b"DPAPI"):
        enc_key = enc_key[5:]
    key = win32crypt.CryptUnprotectData(enc_key, None, None, None, 0)[1]

    tmp = Path(tempfile.gettempdir()) / "sspoffer_edge_cookies.db"
    try:
        tmp.write_bytes(cookies.read_bytes())
    except OSError as e:
        print(f"Edge 正在占用 Cookie 文件，无法自动读取登录态（{e.errno}）。")
        return None

    con = sqlite3.connect(tmp)
    try:
        rows = con.execute(
            "SELECT encrypted_value, value FROM cookies "
            "WHERE host_key LIKE '%sspoffer.com' AND name = 'token'"
        ).fetchall()
    finally:
        con.close()
        tmp.unlink(missing_ok=True)
    if not rows:
        print("Edge Cookie 里没有 sspoffer 的 token，请先在浏览器登录。")
        return None
    enc, plain = rows[0]
    if plain:
        return plain
    if not enc or enc[:3] not in (b"v10", b"v11"):
        print("token Cookie 的加密格式无法解密。")
        return None
    token = AESGCM(key).decrypt(enc[3:15], enc[15:], None).decode("utf-8", "replace")
    return token or None


def render_statement(q: dict, detail: dict) -> str:
    desc = detail.get("questionDesc") or ""
    if not isinstance(desc, str):
        desc = json.dumps(desc, ensure_ascii=False, indent=2)
    requires = detail.get("requires") or {}
    hard = ""
    stat = detail.get("statisticalInfo") or {}
    if isinstance(stat, dict):
        hard = stat.get("hardLevel") or q.get("hardLevel") or ""
    else:
        hard = q.get("hardLevel") or ""
    time_limit = requires.get("timeLimit") if isinstance(requires, dict) else None
    memory_limit = requires.get("memoryLimit") if isinstance(requires, dict) else None
    url = BASE + (q.get("detailUrl") or f"/oj/{q.get('cardId')}/{q['questionId']}")
    lines = [
        f"# {detail.get('questionTitle') or q.get('title') or q['questionId']}",
        "",
        f"- 题目编号：{q['questionId']}",
        f"- 难度：{hard}",
        f"- 分组：{' / '.join(q.get('groupPath') or [])}",
        f"- 原题：{url}",
    ]
    if time_limit is not None:
        lines.append(f"- 时间限制：{time_limit} ms")
    if memory_limit is not None:
        lines.append(f"- 空间限制：{memory_limit} M")
    tags = q.get("tags") or []
    if tags:
        lines.append(f"- 标签：{'、'.join(str(t) for t in tags)}")
    lines.append("")
    lines.append(desc.strip())
    lines.append("")
    return "\n".join(lines)


def write_catalog(out_dir: Path, card_info: dict, questions: list[dict]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {"cardInfo": card_info, "questions": questions}
    (out_dir / "catalog.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    title = card_info.get("cardTitle") or "题单"
    lines = [
        f"# {title}",
        "",
        card_info.get("cardDescription") or "",
        "",
        f"题目数量：{len(questions)}",
        "",
        "| 序号 | 编号 | 难度 | VIP | 分组 | 标题 |",
        "|---:|---:|---|---|---|---|",
    ]
    for i, q in enumerate(questions, 1):
        group = " / ".join(q.get("groupPath") or [])
        vip = "是" if q.get("vip") else ""
        lines.append(
            f"| {i} | {q['questionId']} | {q.get('hardLevel') or ''} | {vip} | {group} | {q.get('title') or ''} |"
        )
    lines.append("")
    (out_dir / "目录.md").write_text("\n".join(lines), encoding="utf-8")


def crawl_statements(
    http: requests.Session,
    card_id: int,
    questions: list[dict],
    token: str,
    out_dir: Path,
    force: bool,
    sleep_s: float,
) -> tuple[int, int, list[str]]:
    stem_dir = out_dir / "题面"
    stem_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    empty = 0
    errors: list[str] = []
    for i, q in enumerate(questions, 1):
        qid = q["questionId"]
        name = f"{i:04d}-{qid}-{safe_filename(q.get('title') or qid)}.md"
        path = stem_dir / name
        if path.is_file() and path.stat().st_size > 0 and not force:
            ok += 1
            continue
        data = None
        for attempt in range(6):
            try:
                data = api_get(
                    http,
                    "/question/detail-new",
                    {"questionId": qid, "papercardid": card_id},
                    token=token,
                )
            except RuntimeError as e:
                errors.append(f"{qid} {q.get('title')}: {e}")
                data = None
                break
            if data.get("code") == -101:
                wait = 12 + attempt * 8
                print(f"访问频繁，{wait} 秒后重试 {qid} {q.get('title')}")
                time.sleep(wait)
                continue
            break
        if data is None:
            continue
        if data.get("code") != 0:
            errors.append(f"{qid} {q.get('title')}: code={data.get('code')} msg={data.get('msg')}")
            if data.get("code") == 999 and i == 1:
                break
            continue
        detail = data.get("data") or {}
        text = render_statement({**q, "cardId": card_id}, detail)
        desc = (detail.get("questionDesc") or "").strip()
        if not desc:
            empty += 1
        path.write_text(text.replace("\r\n", "\n"), encoding="utf-8")
        ok += 1
        if i % 20 == 0 or i == len(questions):
            print(f"已保存 {i}/{len(questions)}")
        if sleep_s:
            time.sleep(sleep_s)
    return ok, empty, errors


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="爬取 sspoffer 题单题面到本地")
    parser.add_argument("--card-id", type=int, default=47, help="题单 id，默认 47")
    parser.add_argument("--output", default="", help="输出目录，默认 <仓库>/sspoffer/oj-<cardId>")
    parser.add_argument("--token", default="", help="登录 Cookie token，也可用环境变量 SSPOFFER_TOKEN")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的题面文件")
    parser.add_argument("--sleep", type=float, default=0.15, help="每题请求间隔秒数")
    parser.add_argument("--catalog-only", action="store_true", help="只保存目录，不请求题面")
    args = parser.parse_args()

    out_dir = Path(args.output) if args.output else repo_root() / "sspoffer" / f"oj-{args.card_id}"
    http = session()
    print(f"拉取题单 {args.card_id} …")
    card_info, questions = fetch_catalog(http, args.card_id)
    print(f"题单：{card_info.get('cardTitle') or args.card_id}，共 {len(questions)} 题")
    write_catalog(out_dir, card_info, questions)
    print(f"目录已写入：{out_dir}")

    if args.catalog_only:
        return
    token = (args.token or os.environ.get("SSPOFFER_TOKEN") or "").strip() or read_edge_token()
    if not token:
        fail(
            "题面接口需要登录。请任选一种方式后重跑：\n"
            "  1. 完全退出 Edge（所有窗口），再运行本脚本，它会读取本机 sspoffer 的 token Cookie\n"
            "  2. 在已登录页面的开发者工具里复制 Cookie 名 token，然后：\n"
            "     $env:SSPOFFER_TOKEN='粘贴的token'; python utils/crawl_sspoffer_oj.py --card-id "
            f"{args.card_id}",
            code=2,
        )
    print("开始拉取题面 …")
    ok, empty, errors = crawl_statements(
        http, args.card_id, questions, token, out_dir, args.force, args.sleep
    )
    print(f"题面文件：{ok}，其中题干为空：{empty}，失败：{len(errors)}")
    if errors:
        err_path = out_dir / "失败.txt"
        err_path.write_text("\n".join(errors) + "\n", encoding="utf-8")
        print(f"失败明细：{err_path}")
        if any("code=999" in e for e in errors):
            fail("登录态无效或已过期（接口返回未登录）。", code=2)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
