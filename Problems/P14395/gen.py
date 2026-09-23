# -*- coding: utf-8 -*-
"""P14395 测试数据生成。stdin 一行 JSON 风格字符串数组。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14395001)


def format_in(ips):
    return "[" + ",".join(f'"{ip}"' for ip in ips) + "]"


def format_out(values):
    return "[" + ",".join(f'"{x}"' for x in values) + "]\n"


def solve_line(line: str) -> str:
    ips = ast.literal_eval(line.strip())
    ans = Solution().filterValidAClassIPs(ips)
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


def gen_random_valid(count):
    out = []
    for _ in range(count):
        a = RNG.randint(0, 255)
        b = RNG.randint(0, 255)
        c = RNG.randint(0, 255)
        out.append(f"10.{a}.{b}.{c}")
    return out


def gen_random_invalid(count):
    out = []
    for _ in range(count):
        kind = RNG.randint(0, 6)
        if kind == 0:
            out.append(f"{RNG.randint(1, 250)}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}")
        elif kind == 1:
            out.append(f"10.{RNG.randint(0, 99):02d}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}")
        elif kind == 2:
            out.append(f"10.{RNG.randint(0, 255)}.{RNG.randint(256, 999)}.{RNG.randint(0, 255)}")
        elif kind == 3:
            out.append(f"10.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.{RNG.randint(256, 999)}")
        elif kind == 4:
            out.append(
                ".".join(str(RNG.randint(0, 255)) for _ in range(RNG.choice([3, 5, 6])))
            )
        elif kind == 5:
            out.append("")
        else:
            out.append(f"10.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.extra")
    return out


def gen_mixed_list(valid_n, invalid_n):
    ips = gen_random_valid(valid_n) + gen_random_invalid(invalid_n)
    RNG.shuffle(ips)
    return ips[:15]


def gen_max_valid():
    ips = []
    for a in range(0, 256, 17):
        for b in range(0, 256, 43):
            if len(ips) >= 15:
                return ips[:15]
            ips.append(f"10.{a}.{b}.{RNG.randint(0, 255)}")
    while len(ips) < 15:
        ips.append(f"10.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}")
    return ips[:15]


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        (
            "样例1",
            lambda: format_in(
                ast.literal_eval(
                    '["10.2.3.4","192.168.1.1","10.0.1.1","10.01.2.3","10.1.0.256","10.10.5.6","10.1.8.9"]'
                )
            ),
        ),
        (
            "样例2",
            lambda: format_in(
                ast.literal_eval(
                    '["10.216.20.96","10.257.25.193","10.218.150.20","10.159.163.72","10.233.43.60","10.263.201.27","10.94.142.203","10.251.113.174","44.74.87.156","10.145.173.233","10.102.21.96","10.20.23.65","10.43.130.246.12","250.166.162.178","10.138.80.223"]'
                )
            ),
        ),
        (
            "样例3",
            lambda: format_in(
                ast.literal_eval(
                    '["10.45.50.76","10.72.48.0","137.8.136.55","10.72.99.206","10.46.51.77","10.0.166.206","10.46.51.79","10.2.111.132.253","10.45.50.77","10.46.50.77"]'
                )
            ),
        ),
        ("空列表", lambda: format_in([])),
        ("全部非法", lambda: format_in(["192.168.1.1", "10.01.1.1", "10.1.1.256", "1.2.3.4", "10.1.2"])),
        (
            "hack：前导零",
            lambda: format_in(["10.00.1.1", "10.0.1.1", "10.010.2.3", "10.10.2.3"]),
        ),
        (
            "hack：字符串排序",
            lambda: format_in(["10.2.3.4", "10.10.1.1", "10.9.1.1"]),
        ),
        (
            "hack：漏判首段",
            lambda: format_in(["9.0.0.1", "10.0.0.1", "11.0.0.1", "10.255.255.255"]),
        ),
        ("随机混合 12 条", lambda: format_in(gen_mixed_list(6, 6))),
        ("极限 15 条合法", lambda: format_in(gen_max_valid())),
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
        f.write("# P14395 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14395 data ok")


if __name__ == "__main__":
    main()
