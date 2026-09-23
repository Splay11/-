# -*- coding: utf-8 -*-
"""
P14379 测试数据生成器：作文批改后的最长无重复子串。
.in 为单行 Python 双引号字符串字面量；.in 末尾无换行，.out 末尾有且仅有一个换行。
"""
import ast
import os
import random
import string

from std import Solution, normalize

RNG = random.Random(14379001)
MAX_LEN = 1000


def solve_literal_line(line: str) -> str:
    story = ast.literal_eval(line.strip("\r\n"))
    ans = Solution().lengthOfLongestSubstring(story)
    return str(ans) + "\n"


def write_in(path: str, literal_line: str):
    text = literal_line.rstrip("\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path: str, text: str):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def to_literal(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def gen1_samples():
    return to_literal("Hello World!")


def gen2_sample2():
    return to_literal(" hi, jIn")


def gen3_empty():
    return '""'


def gen4_only_spaces():
    return to_literal("     ")


def gen5_collapse_spaces():
    # 中间多空格压缩后应连通
    return to_literal("a" + " " * 20 + "b" + " " * 15 + "c")


def gen6_case_insensitive_hack():
    # 忽略大小写：Aa 只能留 1 个
    return to_literal("AaBbCcDdEe")


def gen7_all_same_letter():
    return to_literal("aaaaaaa")


def gen8_punctuation_run():
    return to_literal("!@#$%^&*()_+-=[]{}|;:',.<>/?")


def gen9_random_medium():
    n = RNG.randint(200, 500)
    chars = string.ascii_letters + string.digits + " ,!?"
    s = "".join(RNG.choice(chars) for _ in range(n))
    return to_literal(s)


def gen10_max_stress():
    # 长度压满 1000，字符尽量多样以逼近 O(n) 滑动窗口
    pool = string.ascii_letters + string.digits + " ,!?;:"
    s = "".join(RNG.choice(pool) for _ in range(MAX_LEN))
    return to_literal(s)


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
    lines.append("langs:\n")
    lines.append("  - py.py3\n")
    lines.append("  - java\n")
    lines.append("  - cc.cc14o2\n")
    lines.append("  - py\n")
    lines.append("  - cc\n")
    with open(os.path.join(data_dir, "config.yaml"), "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)

    generators = [
        ("题面样例 1", gen1_samples),
        ("题面样例 2；首尾空格与词间空格", gen2_sample2),
        ("空串，答案 0", gen3_empty),
        ("仅空格，规范化后为空", gen4_only_spaces),
        ("多空格压缩；检验批改逻辑", gen5_collapse_spaces),
        ("hack：未忽略大小写会把 Aa 当 2", gen6_case_insensitive_hack),
        ("全相同字母，答案 1", gen7_all_same_letter),
        ("符号串，窗口边界", gen8_punctuation_run),
        ("随机中等长度", gen9_random_medium),
        ("长度 1000 压力", gen10_max_stress),
    ]

    for i, (_, gen) in enumerate(generators, start=1):
        inp_line = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp_line)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_literal_line(inp_line))

    write_config_yaml(data_dir)

    for i in range(1, 11):
        p_in = os.path.join(data_dir, f"{i}.in")
        p_out = os.path.join(data_dir, f"{i}.out")
        with open(p_in, "rb") as f:
            raw = f.read()
        if raw.endswith(b"\n"):
            raise SystemExit(f"fail: {i}.in should not end with newline")
        with open(p_out, "rb") as f:
            rawo = f.read()
        if not rawo.endswith(b"\n") or rawo.endswith(b"\n\n"):
            raise SystemExit(f"fail: {i}.out newline rule")
        with open(p_in, "r", encoding="utf-8") as f:
            line = f.read()
        if solve_literal_line(line) != open(p_out, "r", encoding="utf-8").read():
            raise SystemExit(f"fail: group {i} mismatch")

    readme = os.path.join(data_dir, "README.md")
    with open(readme, "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14379 测试数据说明\n\n")
        f.write("主造数脚本：题目根目录 `gen.py`。\n\n")
        f.write("| 编号 | 设计意图 |\n|---|---|\n")
        for i, (note, _) in enumerate(generators, start=1):
            f.write(f"| {i} | {note} |\n")

    print("generated 1..10.in/.out, config.yaml, README.md; self-check ok")


if __name__ == "__main__":
    main()
