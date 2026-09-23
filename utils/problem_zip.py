"""题目压缩包导入导出：/api/problem-zip/*。

指定域时走 /d/<domainId>/api/problem-zip/...（见 API.md）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import requests

from codefun_auth import (
    api_headers,
    dump_response,
    problem_zip_base,
    require_https,
)


def _session(no_proxy: bool) -> requests.Session:
    session = requests.Session()
    if no_proxy:
        session.trust_env = False
    return session


def _zip_root(args) -> str:
    return problem_zip_base(args.base_url, args.domain_id)


def _filename_from_cd(header: str, fallback: str) -> str:
    if not header:
        return fallback
    match = re.search(r"filename\*=(?:UTF-8''|)([^;]+)", header, re.I)
    if match:
        return Path(unquote(match.group(1).strip().strip('"'))).name
    match = re.search(r'filename="?([^";]+)"?', header, re.I)
    if match:
        return Path(match.group(1).strip()).name
    return fallback


def _save_download(resp: requests.Response, output: Path | None, fallback: str) -> Path:
    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "json" in ctype and "zip" not in ctype:
        dump_response(resp)
        raise SystemExit(1)
    dest = output or Path(_filename_from_cd(resp.headers.get("Content-Disposition") or "", fallback))
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if chunk:
                fh.write(chunk)
    print(f"HTTP {resp.status_code} 已保存 {dest}（{dest.stat().st_size} bytes）")
    return dest


def _json_get(session, url, verify, **kwargs):
    resp = session.get(url, timeout=(15, 300), verify=verify, headers=api_headers(json_body=False), **kwargs)
    dump_response(resp)
    if not resp.ok:
        raise SystemExit(1)
    return resp


def _json_post(session, url, verify, **kwargs):
    headers = kwargs.pop("headers", api_headers(json_body=False))
    resp = session.post(url, timeout=(15, 300), verify=verify, headers=headers, **kwargs)
    dump_response(resp)
    if not resp.ok:
        raise SystemExit(1)
    return resp


def cmd_export_problem(args) -> None:
    session = _session(args.no_proxy)
    url = f"{_zip_root(args)}/export/problem/{args.pid}"
    resp = session.get(
        url,
        timeout=(15, 300),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(json_body=False),
        stream=True,
    )
    if not resp.ok:
        dump_response(resp)
        raise SystemExit(1)
    _save_download(resp, Path(args.output) if args.output else None, f"{args.pid}.zip")


def cmd_export_pset(args) -> None:
    session = _session(args.no_proxy)
    url = f"{_zip_root(args)}/export/pset/{args.psid}"
    resp = session.get(
        url,
        timeout=(15, 1800),
        verify=args.ca_cert if args.ca_cert else True,
        headers=api_headers(json_body=False),
        stream=True,
    )
    if not resp.ok:
        dump_response(resp)
        raise SystemExit(1)
    _save_download(resp, Path(args.output) if args.output else None, f"pset-{args.psid}.zip")


def cmd_export_pset_local(args) -> None:
    session = _session(args.no_proxy)
    verify = args.ca_cert if args.ca_cert else True
    url = f"{_zip_root(args)}/export/pset/{args.psid}/local"
    resp = _json_post(session, url, verify)
    if not args.wait:
        return
    try:
        body = resp.json()
    except ValueError:
        return
    job = {}
    if isinstance(body, dict):
        job = body.get("job") or body.get("runningJob") or {}
    job_id = job.get("jobId") if isinstance(job, dict) else None
    if not job_id:
        print("未返回 jobId，无法轮询。", file=sys.stderr)
        raise SystemExit(1)
    args.job_id = job_id
    _poll_export_and_maybe_download(session, args, verify)


def _poll_export_and_maybe_download(session, args, verify) -> None:
    url = f"{_zip_root(args)}/export/job/{args.job_id}"
    deadline = time.time() + args.timeout
    while True:
        resp = session.get(
            url,
            timeout=(10, 60),
            verify=verify,
            headers=api_headers(json_body=False),
        )
        try:
            body = resp.json()
        except ValueError:
            dump_response(resp)
            raise SystemExit(1)
        job = body.get("job") if isinstance(body, dict) and "job" in body else body
        status = (job or {}).get("status") if isinstance(job, dict) else None
        print(json.dumps(body, ensure_ascii=False))
        if status == "done":
            if args.output or args.download:
                args.output = args.output
                cmd_export_file(args)
            return
        if status == "error":
            raise SystemExit(1)
        if time.time() > deadline:
            print("等待导出任务超时。", file=sys.stderr)
            raise SystemExit(1)
        time.sleep(args.poll_interval)


def cmd_export_jobs(args) -> None:
    _json_get(
        _session(args.no_proxy),
        f"{_zip_root(args)}/export/jobs",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_export_job(args) -> None:
    _json_get(
        _session(args.no_proxy),
        f"{_zip_root(args)}/export/job/{args.job_id}",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_export_file(args) -> None:
    session = _session(args.no_proxy)
    url = f"{_zip_root(args)}/export/job/{args.job_id}/file"
    headers = api_headers(json_body=False)
    dest = Path(args.output) if args.output else None
    if dest and dest.is_file() and args.resume:
        headers["Range"] = f"bytes={dest.stat().st_size}-"
    resp = session.get(
        url,
        timeout=(15, 1800),
        verify=args.ca_cert if args.ca_cert else True,
        headers=headers,
        stream=True,
    )
    if not resp.ok:
        dump_response(resp)
        raise SystemExit(1)
    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "json" in ctype and "zip" not in ctype:
        dump_response(resp)
        raise SystemExit(1)
    if dest is None:
        dest = Path(_filename_from_cd(resp.headers.get("Content-Disposition") or "", f"{args.job_id}.zip"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    mode = "ab" if resp.status_code == 206 and dest.is_file() else "wb"
    with dest.open(mode) as fh:
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if chunk:
                fh.write(chunk)
    print(f"HTTP {resp.status_code} 已保存 {dest}（{dest.stat().st_size} bytes）")


def cmd_export_retry(args) -> None:
    _json_post(
        _session(args.no_proxy),
        f"{_zip_root(args)}/export/job/{args.job_id}/retry",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_export_delete(args) -> None:
    _json_post(
        _session(args.no_proxy),
        f"{_zip_root(args)}/export/job/{args.job_id}",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_import_zip(args) -> None:
    path = Path(args.file)
    if not path.is_file():
        print(f"文件不存在: {path}", file=sys.stderr)
        raise SystemExit(1)
    data = {}
    if args.pid:
        data["pid"] = args.pid
    if args.psid:
        data["psid"] = args.psid
    if args.name:
        data["name"] = args.name
    if args.abbreviation:
        data["abbreviation"] = args.abbreviation
    if args.overwrite:
        data["overwrite"] = "1"
    session = _session(args.no_proxy)
    with path.open("rb") as fh:
        resp = session.post(
            f"{_zip_root(args)}/import",
            timeout=(30, 600),
            verify=args.ca_cert if args.ca_cert else True,
            headers=api_headers(json_body=False),
            files={"file": (path.name, fh, "application/zip")},
            data=data,
        )
    dump_response(resp)
    if not resp.ok:
        raise SystemExit(1)


def cmd_import_jobs(args) -> None:
    _json_get(
        _session(args.no_proxy),
        f"{_zip_root(args)}/import/jobs",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_import_job(args) -> None:
    _json_get(
        _session(args.no_proxy),
        f"{_zip_root(args)}/import/job/{args.job_id}",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_import_retry(args) -> None:
    _json_post(
        _session(args.no_proxy),
        f"{_zip_root(args)}/import/job/{args.job_id}/retry",
        args.ca_cert if args.ca_cert else True,
    )


def cmd_import_delete(args) -> None:
    _json_post(
        _session(args.no_proxy),
        f"{_zip_root(args)}/import/job/{args.job_id}",
        args.ca_cert if args.ca_cert else True,
    )


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--base-url", default="https://codefun2000.com")
    p.add_argument("--domain-id", default="system", help="压缩包接口域，默认 system")
    p.add_argument("--ca-cert", default=None)
    p.add_argument("--no-proxy", action="store_true")


def main() -> None:
    parser = argparse.ArgumentParser(description="CodeFun2000 题目压缩包导入导出")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("export-problem", help="GET /export/problem/:pid")
    _add_common(p)
    p.add_argument("--pid", required=True)
    p.add_argument("--output", default=None)
    p.set_defaults(func=cmd_export_problem)

    p = sub.add_parser("export-pset", help="GET /export/pset/:psid 流式下载")
    _add_common(p)
    p.add_argument("--psid", required=True)
    p.add_argument("--output", default=None)
    p.set_defaults(func=cmd_export_pset)

    p = sub.add_parser("export-pset-local", help="POST /export/pset/:psid/local")
    _add_common(p)
    p.add_argument("--psid", required=True)
    p.add_argument("--wait", action="store_true", help="轮询直到完成")
    p.add_argument("--download", action="store_true", help="完成后下载 zip（需 --wait）")
    p.add_argument("--output", default=None)
    p.add_argument("--timeout", type=int, default=3600)
    p.add_argument("--poll-interval", type=float, default=3.0)
    p.add_argument("--resume", action="store_true")
    p.set_defaults(func=cmd_export_pset_local)

    p = sub.add_parser("export-jobs", help="GET /export/jobs")
    _add_common(p)
    p.set_defaults(func=cmd_export_jobs)

    p = sub.add_parser("export-job", help="GET /export/job/:jobId")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_export_job)

    p = sub.add_parser("export-file", help="GET /export/job/:jobId/file")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.add_argument("--output", default=None)
    p.add_argument("--resume", action="store_true", help="已有本地文件时发 Range 断点续传")
    p.set_defaults(func=cmd_export_file)

    p = sub.add_parser("export-retry", help="POST /export/job/:jobId/retry")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_export_retry)

    p = sub.add_parser("export-delete", help="POST /export/job/:jobId")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_export_delete)

    p = sub.add_parser("import", help="POST /import 上传 zip")
    _add_common(p)
    p.add_argument("--file", required=True)
    p.add_argument("--pid", default=None)
    p.add_argument("--psid", default=None)
    p.add_argument("--name", default=None)
    p.add_argument("--abbreviation", default=None)
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_import_zip)

    p = sub.add_parser("import-jobs", help="GET /import/jobs")
    _add_common(p)
    p.set_defaults(func=cmd_import_jobs)

    p = sub.add_parser("import-job", help="GET /import/job/:jobId")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_import_job)

    p = sub.add_parser("import-retry", help="POST /import/job/:jobId/retry")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_import_retry)

    p = sub.add_parser("import-delete", help="POST /import/job/:jobId")
    _add_common(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=cmd_import_delete)

    args = parser.parse_args()
    require_https(args.base_url)
    args.func(args)


if __name__ == "__main__":
    main()
