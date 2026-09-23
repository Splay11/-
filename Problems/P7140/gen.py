# -*- coding: utf-8 -*-
"""P7140 造数：判断字符串是否为有效数字。

stdin：一行字符串 s。输出 true / false。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

N_MAX = 20
PAT = re.compile(r"[+-]?((\d+\.?\d*)|(\.\d+))([eE][+-]?\d+)?")


def naive(s):
    return "true" if PAT.fullmatch(s) else "false"


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, s, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    # 题面列出的合法 / 非法串先自检一遍
    goods = [
        "2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10",
        "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789",
    ]
    bads = ["abc", "1a", "1e", "e3", "99e2.5", "--6", "-+3", "95a54e53"]
    for x in goods:
        assert naive(x) == "true" == solve(x), x
    for x in bads:
        assert naive(x) == "false" == solve(x), x

    plan = [
        ("0",
         "样例 1", "整数 $0$ 合法",
         "把前导零当非法"),
        ("e",
         "样例 2", "单独 $e$ 非法",
         "指数没有底数仍输出 true"),
        (".",
         "样例 3", "单独小数点非法",
         "把 $.$ 当成小数"),
        ("4.",
         "数字加小数点", "合法小数",
         "要求小数点后必须有数字"),
        ("-.9",
         "符号加 $.9$", "合法小数",
         "要求小数点前必须有数字"),
        ("2e10",
         "整数带指数", "合法",
         "没处理指数"),
        ("99e2.5",
         "指数部分是小数", "非法",
         "指数里允许小数点"),
        ("--6",
         "两个符号", "非法",
         "只看了有没有数字"),
        ("-123.456e789",
         "较长合法串，小数加指数", "合法",
         "E 和 e 只认一种"),
        ("95a54e53",
         "数字中间夹字母", "非法",
         "扫到 $e$ 就忽略前面的 $a$"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (s, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, s))

    for i, (s, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        assert ib.decode("utf-8") == s
        got = ob.decode("utf-8").strip()
        assert got == answers[i - 1] == naive(s)

    assert answers[0] == "true"
    assert answers[1] == "false"
    assert answers[2] == "false"
    assert answers[3] == "true"
    assert answers[4] == "true"
    assert answers[5] == "true"
    assert answers[6] == "false"
    assert answers[7] == "false"
    assert answers[8] == "true"
    assert answers[9] == "false"

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7140 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行字符串 $s$。",
        "输出：$true$ 或 $false$（小写）。",
        "",
        r"约束：$1\le |s|\le 20$，$s$ 只含字母、数字、正负号和小数点。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：规则解析必须等于正则 `fullmatch`。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans)


if __name__ == "__main__":
    main()
