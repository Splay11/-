# -*- coding: utf-8 -*-
"""P14382 测试数据生成。stdin 为单行 Python 双引号字符串字面量。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14382001)


def to_literal(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def solve_line(line: str) -> str:
    expr = ast.literal_eval(line.strip("\r\n"))
    ans = Solution().processExpression(expr)
    return ans + "\n"


def write_in(path: str, literal_line: str):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(literal_line.rstrip("\n"))


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


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1 混合进制", lambda: to_literal("023+0x21+0o13+1")),
        ("样例2 负结果取反", lambda: to_literal("0x0C-0o20+1")),
        ("样例3 负数字面 NA", lambda: to_literal("-1+5")),
        ("样例4 整数超999 NA", lambda: to_literal("2324+12-23")),
        ("样例5 空格非法", lambda: to_literal("123 + 12-13=")),
        ("样例6 非法进制串", lambda: to_literal("3A+0xEGW-0o89")),
        ("样例7 结果为-1", lambda: to_literal("45-46")),
        ("样例8 钳制255后取反", lambda: to_literal("30+0xEc+0O12+9")),
        ("单操作数 0xEF", lambda: to_literal("0xEF")),
        ("长表达式压力", lambda: to_literal("+".join([str(RNG.randint(0, 50)) for _ in range(200)]))),
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
        f.write("# P14382 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14382 data ok")


if __name__ == "__main__":
    main()
