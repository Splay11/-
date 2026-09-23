"""调用 POST /api/problems/update，修改已有题库（只更新传入字段）。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

from codefun_auth import dump_response, api_headers, require_https


def _load_json_arg(raw: str | None, path: str | None, label: str):
    if path:
        text = Path(path).read_text(encoding="utf-8")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"{label} 不是合法 JSON：{e}", file=sys.stderr)
            raise SystemExit(1)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"{label} 不是合法 JSON：{e}", file=sys.stderr)
        raise SystemExit(1)


def _load_json_or_text(raw: str | None, path: str | None, label: str):
    if path:
        return _load_json_arg(None, path, label)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def _put_bool(payload: dict, key: str, value) -> None:
    if value is not None:
        payload[key] = bool(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 /api/problems/update")
    parser.add_argument("--base-url", default="https://codefun2000.com")
    parser.add_argument(
        "--domain-id",
        default="system",
        help="改 DAG 时必填；默认 system，始终随请求发送",
    )
    parser.add_argument("--psid", required=True, help="题库 ObjectId 或简称")
    parser.add_argument("--name", default=None)
    parser.add_argument("--abbreviation", default=None)
    parser.add_argument("--company-tag", default=None)
    parser.add_argument("--introduction", default=None)
    parser.add_argument("--profile", default=None)
    parser.add_argument("--profile-file", default=None, help="题库介绍 Markdown/文本文件")
    parser.add_argument("--usage", default=None)
    parser.add_argument("--picture-url", default=None)
    parser.add_argument("--buying-guide", default=None)
    parser.add_argument("--after-sales-guide", default=None)
    parser.add_argument("--purchase-url", default=None)
    parser.add_argument("--price", type=float, default=None)
    parser.add_argument("--origin-price", type=float, default=None, help="原价（origin_price）")
    parser.add_argument(
        "--type",
        default=None,
        choices=["problem_set", "course", "codenote", "training_camp"],
    )
    parser.add_argument("--dag", default=None, help="章节 JSON 字符串")
    parser.add_argument("--dag-file", default=None, help="章节 JSON 文件")
    parser.add_argument("--page-config", default=None)
    parser.add_argument("--page-config-file", default=None)
    parser.add_argument("--codenote-setting", default=None)
    parser.add_argument("--codenote-setting-file", default=None)
    parser.add_argument("--valid-days", type=int, default=None)
    parser.add_argument(
        "--end-time",
        default=None,
        help="结束时间；传空字符串可清除",
    )
    parser.add_argument("--top", type=int, default=None)
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--choice-practice-id", default=None)
    parser.add_argument(
        "--payload-file",
        default=None,
        help="额外 JSON 对象，与命令行字段合并（命令行优先）",
    )

    parser.add_argument("--hidden", dest="hidden", action="store_true", default=None)
    parser.add_argument("--visible", dest="hidden", action="store_false")
    parser.add_argument("--owner-only", dest="owner_only", action="store_true", default=None)
    parser.add_argument("--not-owner-only", dest="owner_only", action="store_false")
    parser.add_argument("--manual", dest="manual", action="store_true", default=None)
    parser.add_argument("--not-manual", dest="manual", action="store_false")
    parser.add_argument("--extra-pay", dest="extra_pay", action="store_true", default=None)
    parser.add_argument("--no-extra-pay", dest="extra_pay", action="store_false")
    parser.add_argument("--hidden-content", dest="hidden_content", action="store_true", default=None)
    parser.add_argument("--show-content", dest="hidden_content", action="store_false")
    parser.add_argument("--show-video", dest="show_video", action="store_true", default=None)
    parser.add_argument("--hide-video", dest="show_video", action="store_false")
    parser.add_argument("--enable-comment", dest="enable_comment", action="store_true", default=None)
    parser.add_argument("--disable-comment", dest="enable_comment", action="store_false")
    parser.add_argument(
        "--codenote-text-sol-render",
        dest="codenote_render",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--no-codenote-text-sol-render",
        dest="codenote_render",
        action="store_false",
    )
    parser.add_argument(
        "--enable-choice-practice",
        dest="enable_choice_practice",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--disable-choice-practice",
        dest="enable_choice_practice",
        action="store_false",
    )

    parser.add_argument("--ca-cert", default=None)
    parser.add_argument("--no-proxy", action="store_true")
    args = parser.parse_args()

    require_https(args.base_url)
    payload: dict = {"psid": args.psid, "domainId": args.domain_id}

    extra = _load_json_arg(None, args.payload_file, "--payload-file")
    if extra is not None:
        if not isinstance(extra, dict):
            print("--payload-file 须是 JSON 对象。", file=sys.stderr)
            sys.exit(1)
        payload.update(extra)
        payload["psid"] = args.psid
        payload["domainId"] = args.domain_id

    if args.name is not None:
        payload["name"] = args.name
    if args.abbreviation is not None:
        payload["abbreviation"] = args.abbreviation
    if args.company_tag is not None:
        payload["company_tag"] = args.company_tag
    if args.introduction is not None:
        payload["introduction"] = args.introduction
    if args.profile_file:
        payload["profile"] = Path(args.profile_file).read_text(encoding="utf-8")
    elif args.profile is not None:
        payload["profile"] = args.profile
    if args.usage is not None:
        payload["usage"] = args.usage
    if args.picture_url is not None:
        payload["picture_url"] = args.picture_url
    if args.buying_guide is not None:
        payload["buying_guide"] = args.buying_guide
    if args.after_sales_guide is not None:
        payload["after_sales_guide"] = args.after_sales_guide
    if args.purchase_url is not None:
        payload["purchase_url"] = args.purchase_url
    if args.price is not None:
        payload["price"] = args.price
    if args.origin_price is not None:
        payload["origin_price"] = args.origin_price
    if args.type is not None:
        payload["type"] = args.type

    dag = _load_json_arg(args.dag, args.dag_file, "dag")
    if dag is not None:
        payload["dag"] = dag

    page_config = _load_json_or_text(args.page_config, args.page_config_file, "pageConfig")
    if page_config is not None:
        payload["pageConfig"] = page_config

    note_setting = _load_json_or_text(
        args.codenote_setting, args.codenote_setting_file, "CodeNoteSetting"
    )
    if note_setting is not None:
        payload["CodeNoteSetting"] = note_setting

    if args.valid_days is not None:
        payload["validDays"] = args.valid_days
    if args.end_time is not None:
        payload["endTime"] = args.end_time
    if args.top is not None:
        payload["top"] = args.top
    if args.group_id is not None:
        payload["groupId"] = args.group_id
    if args.choice_practice_id is not None:
        payload["choicePracticeId"] = args.choice_practice_id

    _put_bool(payload, "hidden", args.hidden)
    _put_bool(payload, "ownerOnly", args.owner_only)
    _put_bool(payload, "manual", args.manual)
    _put_bool(payload, "extra_pay", args.extra_pay)
    _put_bool(payload, "hidden_content", args.hidden_content)
    _put_bool(payload, "show_video", args.show_video)
    _put_bool(payload, "enableComment", args.enable_comment)
    _put_bool(payload, "useCodenoteTextSolRender", args.codenote_render)
    _put_bool(payload, "enableChoicePractice", args.enable_choice_practice)

    if set(payload) <= {"psid", "domainId"}:
        print("除 psid 外至少再提供一个要修改的字段。", file=sys.stderr)
        sys.exit(1)

    url = f"{args.base_url.rstrip('/')}/api/problems/update"
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json=payload,
        timeout=(10, 180),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(),
    )
    dump_response(resp)
    if not resp.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
