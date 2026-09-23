# -*- coding: utf-8 -*-
"""P2977 测试数据生成。stdin 一行：n,cap,workers,[submit...],[exec...]。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(2977001)


def format_in(n, cap, workers, submit, exec_times):
    return (
        f"{n},{cap},{workers},"
        f"[{','.join(str(x) for x in submit)}],"
        f"[{','.join(str(x) for x in exec_times)}]"
    )


def format_out(ans):
    return "[" + ",".join(str(x) for x in ans) + "]\n"


def solve_raw(submit, exec_times, cap, workers):
    return Solution().simulateTaskQueue(submit, exec_times, cap, workers)


def solve_line(line):
    line = line.strip("\r\n")
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(line):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(line[start:i])
            start = i + 1
    parts.append(line[start:])
    cap = int(parts[1].strip())
    workers = int(parts[2].strip())
    submit = eval(parts[3].strip())
    exec_times = eval(parts[4].strip())
    return format_out(solve_raw(submit, exec_times, cap, workers))


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n"))


def write_out(path, text):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_config_yaml(data_dir):
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


def gen_random_case(n, t_max=500):
    times = sorted(RNG.sample(range(1, t_max + 1), n))
    exec_times = [RNG.randint(1, min(1000, t_max)) for _ in range(n)]
    return times, exec_times


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    st9, ex9 = gen_random_case(15, 800)
    st10, ex10 = gen_random_case(20, 1000)

    generators = [
        ("样例1", lambda: format_in(3, 3, 2, [1, 2, 3], [3, 2, 3])),
        ("样例2", lambda: format_in(4, 1, 2, [1, 2, 4, 6], [6, 4, 3, 3])),
        ("样例3", lambda: format_in(5, 1, 2, [1, 2, 3, 4, 6], [6, 4, 3, 3, 3])),
        ("基础：单任务", lambda: format_in(1, 1, 1, [5], [7])),
        ("边界：队列容量等于任务数", lambda: format_in(3, 3, 1, [1, 2, 3], [2, 2, 2])),
        ("单执行者", lambda: format_in(4, 2, 1, [1, 3, 5, 7], [2, 2, 2, 2])),
        ("hack：同刻提交与释放且队列满", lambda: format_in(3, 1, 2, [1, 2, 2], [5, 3, 4])),
        ("hack：连续满队丢弃", lambda: format_in(5, 1, 1, [1, 2, 3, 4, 5], [1, 1, 1, 1, 1])),
        ("随机 n=15", lambda: format_in(15, 3, 4, st9, ex9)),
        ("极限 n=20", lambda: format_in(20, 1, 80, st10, ex10)),
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
            if solve_line(f.read()) != open(
                os.path.join(data_dir, f"{i}.out"), encoding="utf-8"
            ).read():
                raise SystemExit(f"group {i} mismatch")

    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P2977 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P2977 data ok")


if __name__ == "__main__":
    main()
