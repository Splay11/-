"""调用 /api/problem/upload_testdata 上传测试数据；支持 LeetCode 核心代码模式配置文件一并上传。"""

import argparse
import json
from pathlib import Path

import requests

from codefun_auth import api_headers


# 核心代码模式约定文件名（可从题目根或 data/ 子目录自动定位）
CORE_BUNDLE_FILENAMES = (
    "compile.sh",
    "config.yaml",
    "template.py",
    "template.cc",
    "template.java",
    "user.cc",
    "user.java",
    "user.py",
)


def require_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("通信安全：BASE_URL 须为 https:// 开头")


def collect_files(data_dir: Path) -> dict[str, str]:
    """收集目录中所有文件的内容（文件名 -> 文件内容）。"""
    files: dict[str, str] = {}
    for p in data_dir.iterdir():
        if p.is_file():
            files[p.name] = p.read_text(encoding="utf-8")
    return files


def resolve_config_dir(target_dir: Path) -> Path:
    """
    智能解析配置文件所在目录：
    - 如果 target_dir 本身包含核心配置文件，则直接使用
    - 否则如果 target_dir/data/ 存在且包含核心文件，则使用 data/ 子目录
    - 否则返回 target_dir（后续会尝试上传所有文件）
    """
    target_dir = target_dir.resolve()
    if not target_dir.is_dir():
        raise ValueError(f"目录不存在或不是目录: {target_dir}")

    # 检查根目录是否有核心配置文件
    root_has_core = any((target_dir / name).is_file() for name in CORE_BUNDLE_FILENAMES)
    if root_has_core:
        return target_dir

    # 检查 data/ 子目录
    data_subdir = target_dir / "data"
    if data_subdir.is_dir():
        data_has_core = any((data_subdir / name).is_file() for name in CORE_BUNDLE_FILENAMES)
        if data_has_core:
            return data_subdir

    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="调用 /api/problem/upload_testdata（支持直接上传核心代码模式配置文件）"
    )
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--domain-id", required=True)
    parser.add_argument("--pid", required=True)
    parser.add_argument(
        "--data-dir",
        default=None,
        help="含文件的目录（原始用法，上传该目录下所有文件）",
    )
    parser.add_argument(
        "--problem-dir",
        default=None,
        help="题目文件夹路径（如 HOT100/两数之和），会自动查找配置文件（支持根目录或 data/ 子目录）",
    )
    parser.add_argument("--ca-cert", default=None)
    parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="禁用系统代理（Session.trust_env=False）",
    )
    ow = parser.add_mutually_exclusive_group()
    ow.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=True,
        help="覆盖已有文件并上传（默认）",
    )
    ow.add_argument(
        "--no-overwrite",
        dest="overwrite",
        action="store_false",
        help="若题目已有同名文件则跳过上传",
    )
    args = parser.parse_args()

    require_https(args.base_url)

    # 优先使用 --problem-dir（智能解析），否则使用 --data-dir
    if args.problem_dir:
        target = Path(args.problem_dir)
        data_dir = resolve_config_dir(target)
        print(f"使用配置目录: {data_dir}")
    elif args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        raise SystemExit("必须指定 --data-dir 或 --problem-dir")

    if not data_dir.is_dir():
        raise SystemExit(f"目录不存在或不是目录: {data_dir}")

    files = collect_files(data_dir)
    if not files:
        raise SystemExit("目录中未找到可上传文件")

    payload = {
        "domainId": args.domain_id,
        "pid": args.pid,
        "files": files,
        "overwrite": bool(args.overwrite),
    }

    url = f"{args.base_url.rstrip('/')}/api/problem/upload_testdata"
    verify = args.ca_cert if args.ca_cert else True
    session = requests.Session()
    if args.no_proxy:
        session.trust_env = False
    resp = session.post(
        url,
        json=payload,
        timeout=(60, 600),
        verify=verify,
        headers=api_headers(),
    )
    print("HTTP", resp.status_code)
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(resp.text)


if __name__ == "__main__":
    main()