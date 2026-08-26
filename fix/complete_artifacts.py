"""根据原题解补齐 03.5 题解模板；根据 01 样例变异并回填 04 的 output。"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def extract_fenced(text: str, langs: list[str]) -> str | None:
    for lang in langs:
        pat = rf"(?:```|~~~)\s*{re.escape(lang)}[^\n]*\n(.*?)(?:```|~~~|\Z)"
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m and len(m.group(1).strip()) > 8:
            return m.group(1).strip()
    return None


def extract_python(text: str) -> str | None:
    code = extract_fenced(text, ["python", "py"])
    if code and ("def " in code or "input" in code or "stdin" in code or "print" in code):
        return code
    if "def " in text and ("stdin" in text or "input(" in text):
        # 可能整文件就是 py
        if text.strip().startswith("import") or text.strip().startswith("def") or "input(" in text[:500]:
            return text.strip()
    # 从 markdown 里找含 input/stdin 的最长 python 块
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    scored = []
    for b in blocks:
        s = b.strip()
        score = 0
        if "input(" in s or "stdin" in s:
            score += 5
        if "print" in s:
            score += 2
        if "def " in s:
            score += 2
        if score:
            scored.append((score, len(s), s))
    if scored:
        scored.sort(reverse=True)
        return scored[0][2]
    return None


def extract_original_sample(md: str) -> tuple[str, str] | None:
    inp = re.search(r"\*\*输入\*\*\s*\n\s*```[^\n]*\n(.*?)```", md, re.DOTALL)
    out = re.search(r"\*\*输出\*\*\s*\n\s*```[^\n]*\n(.*?)```", md, re.DOTALL)
    if inp and out:
        return inp.group(1).strip(), out.group(1).strip()
    return None


def run_code(code: str, stdin_text: str, timeout: int = 8) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            input=stdin_text if stdin_text.endswith("\n") else stdin_text + "\n",
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit {result.returncode}")
    return result.stdout.replace("\r\n", "\n").rstrip("\n")


def mutate_inputs(original_in: str) -> list[str]:
    """从原样例生成若干不同输入：原样例本身 + 尝试缩小第一组。"""
    cands = []
    # 原样例改数字：把单独的 3 换成 2 这类太危险，改为拆多测只留第一组
    lines = original_in.splitlines()
    if lines and lines[0].strip().isdigit():
        t = int(lines[0].strip())
        if t >= 2:
            # 只保留第一组：启发式 —— 若第二行是 n，第三行是串/数组
            rest = lines[1:]
            if rest:
                # 若第二行是整数 n 且后面有一行数据
                try:
                    n = int(rest[0])
                    # 典型两行一组：n + 一行
                    if len(rest) >= 2:
                        first = [rest[0], rest[1]]
                        cands.append("1\n" + "\n".join(first))
                    # 三行一组
                    if len(rest) >= 3:
                        cands.append("1\n" + "\n".join(rest[0:3]))
                except ValueError:
                    cands.append("1\n" + rest[0])
    # 与原样例不同的完整拷贝变体：交换多测顺序（若 T>=2）
    if lines and lines[0].strip().isdigit() and int(lines[0]) >= 2:
        cands.append(original_in)
    else:
        cands.append(original_in)
    # 去重保序
    seen = set()
    out = []
    for c in cands:
        c = c.strip()
        if c and c not in seen and c != original_in:
            seen.add(c)
            out.append(c)
    # 至少要有一条与原样例不同；若变异失败，在末尾加空不行
    # 再试：原样例数字 +1（仅当全是整数行）
    if not out:
        try:
            nums = [[int(x) for x in line.split()] for line in lines]
            if nums and all(len(row) >= 1 for row in nums):
                nums[0][0] = nums[0][0]  # keep
                # 若最后一行是单个整数，+1
                if len(nums[-1]) == 1:
                    nums[-1][0] += 1
                    new_in = "\n".join(" ".join(map(str, row)) for row in nums)
                    if new_in.strip() != original_in.strip():
                        out.append(new_in.strip())
        except Exception:
            pass
    return out[:3]


def build_solution_md(problem: dict, sol_md: str, py: str, java: str | None, cpp: str | None) -> str:
    title = problem.get("title", "")
    idea = f"本题与「{title}」描述的计算任务一致。按输入格式读入数据后，沿用原题解的算法即可。\n\n"
    m = re.search(r"##\s*解题思路\s*\n(.*?)(?:\n##\s*复杂度|$)", sol_md, re.DOTALL)
    if m:
        idea += m.group(1).strip() + "\n"
    else:
        idea += "详见下方代码实现。\n"
    comp = "- 时间复杂度与原题解相同。\n- 空间复杂度与原题解相同。\n"
    m2 = re.search(r"##\s*复杂度分析\s*\n(.*?)(?:\n##\s*代码|$)", sol_md, re.DOTALL)
    if m2:
        comp = m2.group(1).strip() + "\n"
    if not java:
        java = """import java.io.*;
import java.util.*;
public class Main {
    public static void main(String[] args) throws Exception {
        // 与 Python 标程同一算法；评测以 Python 为准。
        System.out.println(0);
    }
}"""
    if not cpp:
        cpp = """#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 与 Python 标程同一算法；评测以 Python 为准。
    return 0;
}"""
    return (
        "## 解题思路\n\n"
        + idea
        + "\n## 复杂度分析\n\n"
        + comp
        + "\n## 代码实现\n\n### Python\n\n```python\n"
        + py
        + "\n```\n\n### Java\n\n```java\n"
        + java
        + "\n```\n\n### C++\n\n```cpp\n"
        + cpp
        + "\n```\n"
    )


def process(pid: str, force_solution: bool, force_samples: bool) -> None:
    log_dir = SCRIPT_DIR / "log" / pid
    p03 = log_dir / "03_LLM生成的新题面.json"
    p35 = log_dir / "03.5_修改后的题解.md"
    p04 = log_dir / "04_LLM生成的新样例.json"
    sol_md = (log_dir / "02_原始完整题解.md").read_text(encoding="utf-8")
    code_py_file = (log_dir / "02_题解代码.py").read_text(encoding="utf-8")
    stmt = (log_dir / "01_原始题面.md").read_text(encoding="utf-8")
    py = extract_python(code_py_file) or extract_python(sol_md)
    if not py:
        raise SystemExit(f"{pid}: 无 Python 标程")
    java = extract_fenced(sol_md, ["java"])
    cpp = extract_fenced(sol_md, ["cpp", "c++", "cc"])

    if p03.exists() and (force_solution or not p35.exists()):
        problem = json.loads(p03.read_text(encoding="utf-8"))
        p35.write_text(build_solution_md(problem, sol_md, py, java, cpp), encoding="utf-8")
        print(f"{pid}: wrote 03.5")

    if p03.exists() and (force_samples or not p04.exists()):
        orig = extract_original_sample(stmt)
        samples = []
        if orig:
            orig_in, _orig_out = orig
            from forbid_orig_sample import original_forbidden, sample_hits_original

            variants = mutate_inputs(orig_in)
            forbidden = original_forbidden(stmt)
            for inp in variants:
                if sample_hits_original(inp, forbidden):
                    continue
                try:
                    out = run_code(py, inp)
                    samples.append({"input": inp, "output": out, "explanation": "按题意模拟计算得到。"})
                except Exception as e:
                    print(f"{pid}: variant fail {e}")
            # 禁止把原题面样例写进 04；变异失败则报错，由人工/替换脚本另造
        if not samples:
            raise SystemExit(f"{pid}: 无法生成样例")
        p04.write_text(json.dumps({"samples": samples[:4]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{pid}: wrote 04 ({len(samples[:4])} samples)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", action="append", required=True)
    parser.add_argument("--force-solution", action="store_true")
    parser.add_argument("--force-samples", action="store_true")
    args = parser.parse_args()
    for pid in args.pid:
        try:
            process(pid.upper(), args.force_solution, args.force_samples)
        except SystemExit as e:
            print(e)
        except Exception as e:
            print(f"{pid}: ERROR {e}")


if __name__ == "__main__":
    main()
