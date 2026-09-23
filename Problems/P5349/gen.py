# -*- coding: utf-8 -*-
"""P5349 造数：软件包版本依赖 + 字典序最小拓扑序。"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def load_std():
    spec = importlib.util.spec_from_file_location("p5349_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.install_order, mod.parse_ver


install_order, parse_ver = load_std()


def solve_lines(lines):
    m = int(lines[0])
    pkgs = []
    for row in lines[1:]:
        p = row.split()
        pkgs.append((int(p[0]), parse_ver(p[1]), p[2:]))
    return install_order(m, pkgs)


def write_case(idx, lines):
    ans = solve_lines(lines)
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    cases.append(["2", "0 1.0.0 1>3.0.0", "1 3.0.0"])
    cases.append(["2", "0 1.0.0 1", "1 1.0.0 0"])
    cases.append(["3", "2 1.0.0 0 1", "0 1.0.0", "1 1.0.0"])
    # 自己依赖自己
    cases.append(["1", "0 1.0.0 0"])
    # 按字符串比版本会把 9.0.0 当成大于 10.0.0
    cases.append(["2", "0 1.0.0 1>=10.0.0", "1 9.0.0"])
    # >= 边界相等应通过；输入顺序打乱
    cases.append(["3", "2 1.0.0", "0 1.0.0 1>=3.0.0 2<=2.0.0", "1 3.0.0"])
    # 把 >= 当成 > 会错
    cases.append(["2", "1 2.0.0", "0 1.0.0 1>=2.0.0"])
    # 无依赖但输入倒序，卡按输入顺序输出
    cases.append(["4", "3 0.0.1", "2 0.0.2", "1 0.0.3", "0 0.0.4"])
    chain = ["100"]
    chain.append("0 1.0.0")
    for i in range(1, 100):
        chain.append(f"{i} 1.0.0 {i - 1}")
    cases.append(chain)
    indep = ["100"]
    for i in range(99, -1, -1):
        indep.append(f"{i} 1.0.0")
    cases.append(indep)

    notes = [
        "样例1 版本冲突",
        "样例2 环",
        "样例3 字典序",
        "自环",
        "卡字符串比版本",
        ">= 与 <= 同时成立",
        "卡把 >= 当成 >",
        "输入倒序无依赖",
        "m=100 链",
        "m=100 全无依赖倒序输入",
    ]
    for i, lines in enumerate(cases, 1):
        ans = write_case(i, lines)
        print(f"case {i}: m={lines[0]} ans={ans[:40]} note={notes[i - 1]}")

    assert solve_lines(["3", "0 1.0.0 1>=2.0.0", "1 4.0.0", "2 3.0.0 1<=3.0.0"]) == "-1"
    assert solve_lines(["3", "0 1.0.0 1", "1 2.0.0 2", "2 3.0.0 0"]) == "-2"
    assert solve_lines(["5", "0 1.0.0 1>=1.0.0 2<=2.0.0", "1 2.0.0", "2 2.0.0", "3 4.0.0 0", "4 5.0.0 3"]) == "1 2 0 3 4"

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        if raw.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        lines = raw.decode("utf-8").split("\n")
        got = solve_lines(lines)
        expect = (DATA / f"{i}.out").read_text(encoding="utf-8")
        if not expect.endswith("\n") or expect.endswith("\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")
        if got + "\n" != expect:
            raise SystemExit(f"校验失败 {i}")
    print("gen ok")


if __name__ == "__main__":
    main()
