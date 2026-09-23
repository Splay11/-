# -*- coding: utf-8 -*-
"""P5518 分苹果方案：样例 + 边界 + 接近上限."""
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def write_in(path, text):
    # .in 不以换行结尾
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    # .out 末尾仅一个换行
    if not text.endswith("\n"):
        text = text + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run_std(inp):
    p = subprocess.run(
        [sys.executable, os.path.join(DIR, "std.py")],
        input=inp, capture_output=True, text=True, encoding="utf-8"
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout


def main():
    os.makedirs(DATA, exist_ok=True)
    cases = [
        "0 2",           # 样例1
        "2 1",           # 样例2
        "0 1",           # 边界：0 个苹果 1 人
        "1 2",           # 小数据
        "3 2",           # 中等
        "5 3",           # 中等
        "0 5",           # n 达上限，m=0
        "1 5",           # 卡「每人必须至少1」假解
        "15 4",          # 接近上限
        "15 5",          # 上限 m=15,n=5
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok")


if __name__ == "__main__":
    main()
