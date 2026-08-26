"""用原题解 Python 代码回填 04 JSON 中的 output，避免手算样例答案出错。"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def extract_python(text: str) -> str | None:
    if "def " in text and ("input(" in text or "stdin" in text or "sys.stdin" in text):
        return text
    marker = "```python"
    if marker in text.lower():
        lower = text.lower()
        start = lower.find(marker)
        rest = text[start + len(marker):]
        end = rest.find("```")
        if end > 0:
            return rest[:end].strip()
    return None


def run_code(code: str, stdin_text: str, timeout: int = 8) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit {result.returncode}")
    return result.stdout.replace("\r\n", "\n")


def main():
    parser = argparse.ArgumentParser(description="用标程回填样例 output")
    parser.add_argument("--pid", required=True)
    args = parser.parse_args()
    pid = args.pid.upper()
    log_dir = SCRIPT_DIR / "log" / pid
    samples_path = log_dir / "04_LLM生成的新样例.json"
    code_path = log_dir / "02_题解代码.py"
    sol_path = log_dir / "02_原始完整题解.md"
    if not samples_path.exists():
        print(f"缺少 {samples_path}")
        sys.exit(1)
    raw = code_path.read_text(encoding="utf-8") if code_path.exists() else ""
    code = extract_python(raw)
    if code is None and sol_path.exists():
        code = extract_python(sol_path.read_text(encoding="utf-8"))
    if not code:
        print("无法提取可运行 Python 标程，跳过回填")
        sys.exit(2)
    data = json.loads(samples_path.read_text(encoding="utf-8"))
    samples = data.get("samples") or []
    for i, sample in enumerate(samples, 1):
        inp = sample.get("input", "")
        if not inp.endswith("\n"):
            inp = inp + "\n"
        out = run_code(code, inp)
        if out.endswith("\n"):
            out = out[:-1]
        sample["output"] = out
        print(f"{pid} 样例{i} 已回填 output")
    samples_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    main()
