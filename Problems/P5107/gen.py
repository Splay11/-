# -*- coding: utf-8 -*-
"""P5107 测试数据生成。stdin 单行："sn",m"""
import os
import random
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(5107001)


def format_in(sn: str, m: int) -> str:
    return f'"{sn}",{m}'


def format_out(value: str) -> str:
    return f'"{value}"\n'


def solve_line(line: str) -> str:
    line = line.strip()
    if not line or line[0] != '"':
        raise ValueError("bad input")
    i = 1
    sn_chars = []
    while i < len(line) and line[i] != '"':
        sn_chars.append(line[i])
        i += 1
    if i >= len(line) or line[i] != '"':
        raise ValueError("bad string end")
    i += 1
    if i >= len(line) or line[i] != ",":
        raise ValueError("bad comma")
    sn = "".join(sn_chars)
    m = int(line[i + 1 :])
    ans = Solution().rearrangeSN(sn, m)
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


def gen_random_sn(alnum_len: int, dash_prob: float = 0.25) -> str:
    pool = string.ascii_letters + string.digits
    chars = [RNG.choice(pool) for _ in range(alnum_len)]
    if alnum_len == 0:
        return ""
    out = [chars[0]]
    for c in chars[1:]:
        if RNG.random() < dash_prob:
            out.append("-")
        out.append(c)
    return "".join(out)


def gen_large_sn(alnum_len: int) -> str:
    pool = string.ascii_lowercase + string.digits
    body = "".join(RNG.choice(pool) for _ in range(alnum_len))
    # 每隔 m 个字符插入破折号，保证总长 < 10000
    parts = []
    step = 7
    for i in range(0, len(body), step):
        parts.append(body[i : i + step])
    return "-".join(parts)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in("8F-3T-1G-2n", 4)),
        ("样例2", lambda: format_in("2-2g-5-g", 2)),
        ("样例3", lambda: format_in("g", 10)),
        ("样例4", lambda: format_in("2-2g-5-g", 1)),
        ("样例5", lambda: format_in("", 10)),
        ("样例6", lambda: format_in("---------", 1)),
        (
            "hack：余数首段",
            lambda: format_in("abc-def-gh", 3),
        ),
        (
            "hack：非法字符",
            lambda: format_in("ab@c-de", 2),
        ),
        (
            "hack：未转大写",
            lambda: format_in("a-b-c-d-e", 2),
        ),
        ("极限：约 9990 有效字符 m=10", lambda: format_in(gen_large_sn(9990), 10)),
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
        f.write("# P5107 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P5107 data ok")


if __name__ == "__main__":
    main()
