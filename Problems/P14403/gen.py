# -*- coding: utf-8 -*-
"""P14403 测试数据生成。stdin 一行：[logs],[keywords]"""
import ast
import os
import random
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14403001)


def split_top_level_commas(s: str):
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(s):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts


def format_string_array(arr):
    return "[" + ",".join('"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' for s in arr) + "]"


def format_in(logs, keywords):
    return format_string_array(logs) + "," + format_string_array(keywords)


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    logs = ast.literal_eval(parts[0])
    keywords = ast.literal_eval(parts[1])
    ans = Solution().analyzeLogKeywords(logs, keywords)
    return format_out(ans)


def write_in(path: str, text: str):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n"))


def write_out(path: str, text: str):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_config_yaml(data_dir: str):
    lines = [
        "type: default\n",
        "user_extra_files:\n",
        "  - template.py\n",
        "  - template.java\n",
        "  - template.cc\n",
        "  - compile.sh\n",
        "  - config.yaml\n",
        "  - user.cc\n",
        "  - user.java\n",
        "  - user.py\n",
        "subtasks:\n",
        "  - score: 100\n",
        "    if: []\n",
        "    id: 1\n",
        "    type: sum\n",
        "    cases:\n",
    ]
    for i in range(1, 11):
        lines.append(f"      - input: {i}.in\n")
        lines.append(f"        output: {i}.out\n")
    lines += ["langs:\n", "  - py.py3\n", "  - java\n", "  - cc.cc14o2\n", "  - py\n", "  - cc\n"]
    with open(os.path.join(data_dir, "config.yaml"), "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)


def gen_random_log(keywords, max_words=20):
    words = []
    n = RNG.randint(3, max_words)
    for _ in range(n):
        if RNG.random() < 0.35 and keywords:
            kw = RNG.choice(keywords)
            if RNG.random() < 0.5:
                words.append(kw.upper() if RNG.random() < 0.5 else kw.capitalize())
            else:
                words.append(kw)
        else:
            words.append("".join(RNG.choice(string.ascii_lowercase) for _ in range(RNG.randint(2, 8))))
    sep = RNG.choice([" ", ": ", ", ", ". ", "! ", "? "])
    return sep.join(words)


def gen_max_stress():
    keywords = [f"kw{i}" for i in range(100)]
    logs = []
    for t in range(1000):
        parts = []
        for ki in range(5):
            parts.append(keywords[(t + ki) % 100])
        filler = " ".join("x" * 10 for _ in range(80))
        logs.append(" ".join(parts) + " " + filler[: min(900, 1000 - 40)])
        if len(logs[-1]) > 1000:
            logs[-1] = logs[-1][:1000]
    return logs, keywords


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in(
            ["Error in system", "warning: error detected", "No errors found"],
            ["error", "warning"],
        )),
        ("样例2", lambda: format_in(
            [
                "Error: system failure",
                "Warning: error in network",
                "System error detected again",
                "Network warning error found",
            ],
            ["error", "system", "warning", "network"],
        )),
        ("样例3", lambda: format_in(
            [
                "Error in module A",
                "Module error B error",
                "Error module C error",
                "Module error D",
            ],
            ["error", "module"],
        )),
        ("样例4", lambda: format_in(
            ["Test log one", "Test log two", "Test log three"],
            ["test", "log", "one", "two", "three"],
        )),
        ("hack：子串不匹配 errors", lambda: format_in(
            ["errors everywhere", "error once", "more errors"],
            ["error"],
        )),
        ("hack：共现仅1条日志", lambda: format_in(
            ["alpha beta", "alpha only", "beta only"],
            ["alpha", "beta"],
        )),
        ("hack：标点切分", lambda: format_in(
            ["fail,error;done!", "warning? error: ok"],
            ["error", "warning"],
        )),
        ("hack：同日志多次计数", lambda: format_in(
            ["error error error", "no match"],
            ["error"],
        )),
        ("随机中等规模", lambda: format_in(
            [gen_random_log(["alpha", "beta", "gamma"], 15) for _ in range(50)],
            ["alpha", "beta", "gamma", "delta"],
        )),
        ("极限1000日志100关键词", lambda: format_in(*gen_max_stress())),
    ]
    for i, (_, gen) in enumerate(generators, start=1):
        inp = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_line(inp))
    write_config_yaml(data_dir)
    for i in range(1, 11):
        with open(os.path.join(data_dir, f"{i}.in"), "rb") as f:
            if f.read().endswith(b"\n"):
                raise SystemExit(f"{i}.in must not end with newline")
        with open(os.path.join(data_dir, f"{i}.out"), "rb") as f:
            raw = f.read()
            if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
                raise SystemExit(f"{i}.out newline rule")
        with open(os.path.join(data_dir, f"{i}.in"), encoding="utf-8") as f:
            if solve_line(f.read()) != open(os.path.join(data_dir, f"{i}.out"), encoding="utf-8").read():
                raise SystemExit(f"group {i} mismatch")
    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14403 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14403 data ok")


if __name__ == "__main__":
    main()
