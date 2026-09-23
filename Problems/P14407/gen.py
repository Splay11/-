# -*- coding: utf-8 -*-
"""P14407 测试数据生成。stdin 一行：Python 字符串列表字面量。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14407001)


def format_commands(commands):
    inner = ", ".join('"' + c.replace("\\", "\\\\").replace('"', '\\"') + '"' for c in commands)
    return "[" + inner + "]"


def format_out(val: int) -> str:
    return str(val) + "\n"


def solve_line(line: str) -> str:
    commands = ast.literal_eval(line.strip())
    ans = Solution().queryNetEnergy(commands)
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


def gen_random_case(n_records: int):
    base = 1700000000
    cmds = []
    for i in range(n_records):
        s = base + RNG.randint(0, 100000)
        e = s + RNG.randint(100, 5000)
        if RNG.random() < 0.5:
            typ = RNG.choice(["wind", "solar", "grid"])
            amt = RNG.randint(1, 10000)
            cmds.append(f"AddProductionRecord,{typ},{amt},{s},{e}")
        else:
            amt = RNG.randint(1, 10000)
            cmds.append(f"AddConsumptionRecord,{amt},{s},{e}")
    ver = RNG.choice(["A", str(RNG.randint(1, n_records))])
    qs = base + RNG.randint(0, 50000)
    qe = qs + RNG.randint(1000, 80000)
    cmds.append(f"QueryNetEnergy,{ver},{qs},{qe}")
    return format_commands(cmds)


def gen_max_stress():
    base = 1600000000
    cmds = []
    for i in range(999):
        s = base + i * 10
        e = s + 1000
        if i % 2 == 0:
            cmds.append(f"AddProductionRecord,wind,{100 + i % 500},{s},{e}")
        else:
            cmds.append(f"AddConsumptionRecord,{50 + i % 300},{s},{e}")
    cmds.append(f"QueryNetEnergy,A,{base},{base + 9990}")
    return format_commands(cmds)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：部分重叠加权", lambda: format_commands([
            "AddProductionRecord,wind,500,1640000000,1640001000",
            "AddConsumptionRecord,100,1640000000,1640000600",
            "AddConsumptionRecord,200,1640000251,1640001251",
            "QueryNetEnergy,3,1640000000,1640001000",
        ])),
        ("样例2：无时间交集", lambda: format_commands([
            "AddProductionRecord,wind,1000,1640000000,1640000500",
            "QueryNetEnergy,1,1640001000,1640002000",
        ])),
        ("样例3：全量查询A", lambda: format_commands([
            "AddProductionRecord,solar,300,1640000000,1640002000",
            "AddConsumptionRecord,150,1640001000,1640003000",
            "QueryNetEnergy,A,1640000000,1640002000",
        ])),
        ("边界：版本过滤仅v1", lambda: format_commands([
            "AddProductionRecord,grid,400,1640000000,1640001000",
            "AddConsumptionRecord,999,1640000000,1640001000",
            "AddProductionRecord,solar,800,1640000000,1640001000",
            "QueryNetEnergy,1,1640000000,1640001000",
        ])),
        ("边界：四舍五入0.5", lambda: format_commands([
            "AddProductionRecord,wind,1,1640000000,1640001000",
            "QueryNetEnergy,1,1640000000,1640000500",
        ])),
        ("hack：部分重叠非全额", lambda: format_commands([
            "AddProductionRecord,wind,0,1640000000,1640001000",
            "AddConsumptionRecord,1000,1640000000,1640002000",
            "QueryNetEnergy,2,1640001000,1640002000",
        ])),
        ("hack：版本截断漏计", lambda: format_commands([
            "AddProductionRecord,wind,100,1640000000,1640001000",
            "AddProductionRecord,solar,900,1640000000,1640001000",
            "QueryNetEnergy,1,1640000000,1640001000",
        ])),
        ("负数净能量", lambda: format_commands([
            "AddProductionRecord,wind,50,1640000000,1640001000",
            "AddConsumptionRecord,200,1640000000,1640001000",
            "QueryNetEnergy,2,1640000000,1640001000",
        ])),
        ("随机中等规模", lambda: gen_random_case(120)),
        ("极限999条记录", lambda: gen_max_stress()),
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
        f.write("# P14407 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14407 data ok")


if __name__ == "__main__":
    main()
