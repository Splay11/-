# -*- coding: utf-8 -*-
"""P5519 等和连续段最多划分."""
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
NMAX = 10 ** 5


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def dump(n, a):
    return "%d\n%s" % (n, " ".join(map(str, a)))


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
    rng = random.Random(5519)
    cases = [
        dump(5, [-3, -4, 5, -4, 3]),          # 样例1
        dump(4, [10, 10, 10, 10]),            # 样例2
        dump(1, [0]),                         # 单元素
        dump(3, [1, -1, 0]),                  # 全零和，多段
        dump(6, [1, 2, 3, 1, 2, 3]),          # 可分 2 段
        dump(5, [5, -5, 5, -5, 0]),           # 零和相关
        dump(7, [1, 1, 1, 1, 1, 1, 1]),       # 奇数个相同
        dump(8, [2, -1, -1, 2, -1, -1, 2, -1]),  # 负段
        dump(NMAX, [1] * NMAX),               # 上限：全 1
        dump(NMAX, [rng.randint(-1000, 1000) for _ in range(NMAX - 1)] + [0]),  # 上限随机
    ]
    # 修正最后一组使总和非零时也合法；上面已合法
    for i, inp in enumerate(cases, 1):
        # 修正 case 10：保证长度正确
        lines = inp.split("\n")
        n = int(lines[0])
        a = list(map(int, lines[1].split()))
        assert len(a) == n
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok", "n=", n)


if __name__ == "__main__":
    main()
