"""在题目根目录生成 leetcode_core_bundle_paths.json（核心代码模式附加文件路径清单）。"""

import argparse
import json
import sys
from pathlib import Path

_UTILS_DIR = Path(__file__).resolve().parent
if str(_UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(_UTILS_DIR))

from leetcode_core_bundle_common import MANIFEST_NAME, write_manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"扫描核心代码模式约定文件并写入 {MANIFEST_NAME}",
    )
    parser.add_argument("--problem-dir", required=True, help="题目根目录，如 Problems/P14207")
    parser.add_argument(
        "--out",
        default=None,
        help=f"清单输出路径（默认：<题目根>/{MANIFEST_NAME}）",
    )
    args = parser.parse_args()

    root = Path(args.problem_dir)
    out_path = Path(args.out) if args.out else None
    path, found, missing = write_manifest(root, out_path)

    summary = {
        "written": str(path),
        "found_count": len(found),
        "missing": missing,
        "found_keys": sorted(found.keys()),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if missing:
        print(
            "提示：以下约定文件未找到，已记入 manifest 的 missing 字段；"
            "上传脚本将只上传已存在的文件。",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
