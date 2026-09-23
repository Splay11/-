# -*- coding: utf-8 -*-
"""P14394 测试数据生成。stdin 一行 JSON 风格字符串数组。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14394001)


def format_in(commands):
    inner = ",".join(f'"{c}"' for c in commands)
    return f"[{inner}]"


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    commands = ast.literal_eval(line.strip("\r\n"))
    ans = Solution().processPacketCommands(commands)
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


def gen_random_commands(n, max_x=1000):
    ops = []
    in_buffer = set()
    buffer = []
    send_q = []
    for _ in range(n):
        r = RNG.random()
        if r < 0.45:
            x = RNG.randint(1, max_x)
            ops.append(f"RECEIVE {x}")
            if x not in in_buffer:
                buffer.append(x)
                in_buffer.add(x)
        elif r < 0.75:
            ops.append("SEND")
            if send_q:
                send_q.pop(0)
            elif buffer:
                while buffer:
                    x = buffer.pop(0)
                    in_buffer.discard(x)
                    send_q.append(x)
                send_q.pop(0)
        else:
            ops.append("QUERY")
            if not send_q and buffer:
                while buffer:
                    x = buffer.pop(0)
                    in_buffer.discard(x)
                    send_q.append(x)
    return ops


def gen_max_case():
    cmds = []
    for i in range(1, 51):
        cmds.append(f"RECEIVE {i}")
    for _ in range(25):
        cmds.append("QUERY")
    for _ in range(25):
        cmds.append("SEND")
    return cmds


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in(["RECEIVE 1", "RECEIVE 2", "QUERY", "SEND", "QUERY", "SEND"])),
        ("样例2", lambda: format_in(["RECEIVE 3", "RECEIVE 3", "SEND", "SEND", "SEND"])),
        ("样例3", lambda: format_in(["RECEIVE 1"])),
        ("仅 SEND 空操作", lambda: format_in(["SEND", "SEND", "SEND"])),
        ("hack：发送区有包时 RECEIVE 同号应成功", lambda: format_in(["RECEIVE 1", "QUERY", "RECEIVE 1", "QUERY"])),
        ("hack：连续 QUERY 不消耗", lambda: format_in(["RECEIVE 5", "QUERY", "QUERY", "SEND"])),
        ("多包接收后一次 QUERY", lambda: format_in(["RECEIVE 1", "RECEIVE 2", "RECEIVE 3", "QUERY", "SEND", "SEND"])),
        ("重复 RECEIVE 与 flush", lambda: format_in(["RECEIVE 7", "RECEIVE 7", "QUERY", "RECEIVE 7", "SEND"])),
        ("随机 90 条", lambda: format_in(gen_random_commands(90, 500))),
        ("极限 100 条混合", lambda: format_in(gen_max_case())),
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
        f.write("# P14394 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14394 data ok")


if __name__ == "__main__":
    main()
