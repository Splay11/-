"""核心代码模式（LeetCode 式）题目附加文件：清单文件名列表与读写逻辑。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 与 leetcode-core-code-mode Skill 及题目目录约定一致（平台侧文件名即 key）
CORE_BUNDLE_FILENAMES: Tuple[str, ...] = (
    "compile.sh",
    "config.yaml",
    "template.py",
    "template.cc",
    "template.java",
    "user.cc",
    "user.java",
    "user.py",
)

MANIFEST_NAME = "leetcode_core_bundle_paths.json"


def problem_root_resolve(problem_dir: Path) -> Path:
    p = problem_dir.resolve()
    if not p.is_dir():
        raise ValueError(f"题目根目录不存在或不是目录: {p}")
    return p


def scan_bundle_paths(problem_root: Path) -> Tuple[Dict[str, str], List[str]]:
    """返回 (已找到的逻辑名 -> 绝对路径字符串, 缺失的逻辑名列表)。"""
    found: Dict[str, str] = {}
    missing: List[str] = []
    for name in CORE_BUNDLE_FILENAMES:
        fp = problem_root / name
        if fp.is_file():
            found[name] = str(fp.resolve())
        else:
            missing.append(name)
    return found, missing


def write_manifest(problem_root: Path, out_path: Path | None = None) -> Tuple[Path, Dict[str, str], List[str]]:
    root = problem_root_resolve(problem_root)
    found, missing = scan_bundle_paths(root)
    target = out_path or (root / MANIFEST_NAME)
    doc: Dict[str, Any] = {
        "kind": "leetcode_core_bundle_paths",
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "problem_root": str(root),
        "files": found,
        "missing": missing,
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target, found, missing


def read_manifest(manifest_path: Path) -> Dict[str, Any]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("kind") != "leetcode_core_bundle_paths":
        raise ValueError("manifest kind 不是 leetcode_core_bundle_paths")
    if int(data.get("version", 0)) != 1:
        raise ValueError("不支持的 manifest version")
    return data


def collect_file_contents_from_manifest(doc: Dict[str, Any]) -> Tuple[Dict[str, str], List[str]]:
    """根据 manifest 的 files 映射读取文本内容；路径不存在则从上传集合中剔除并记录。"""
    skipped: List[str] = []
    raw_files = doc.get("files") or {}
    if not isinstance(raw_files, dict):
        raise ValueError("manifest.files 须为对象")

    out: Dict[str, str] = {}
    for logical_name, path_str in raw_files.items():
        if not isinstance(path_str, str) or not path_str.strip():
            skipped.append(str(logical_name))
            continue
        p = Path(path_str)
        if not p.is_file():
            skipped.append(str(logical_name))
            continue
        out[str(logical_name)] = p.read_text(encoding="utf-8")
    return out, skipped
