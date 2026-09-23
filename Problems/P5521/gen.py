# -*- coding: utf-8 -*-
"""P5521 三串字典序最小 LCS. 大数据不超过 |s|<=100."""
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def dump(a, b, c):
    return "%s\n%s\n%s" % (a, b, c)


def run_std(inp):
    p = subprocess.run(
        [sys.executable, os.path.join(DIR, "std.py")],
        input=inp, capture_output=True, text=True, encoding="utf-8"
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout


def rand_str(rng, L, alphabet="abcdefghijklmnopqrstuvwxyz"):
    return "".join(rng.choice(alphabet) for _ in range(L))


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5521)
    cases = [
        dump("bb", "bdb", "bcbb"),            # 样例1
        dump("bc", "cbacd", "bc"),            # 样例2
        dump("a", "b", "c"),                  # LCS=0
        dump("abc", "abc", "abc"),            # 完全相同
        dump("z", "z", "z"),                  # 单字符
        dump("aaaa", "aa", "aaa"),            # 重复字母
        dump("abcde", "edcba", "ace"),        # 交错
        dump("xyz", "xy", "x"),               # 短公共前缀
        dump(rand_str(rng, 100), rand_str(rng, 100), rand_str(rng, 100)),
        dump("a" * 100, "a" * 100, "a" * 100),  # 上限全 a
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok")


if __name__ == "__main__":
    main()
