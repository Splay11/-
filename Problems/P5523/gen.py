# -*- coding: utf-8 -*-
"""P5523 小于 s 的最大整数. s 最长可达 10000 位."""
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


def dump(nums, s):
    return "%d\n%s\n%s" % (len(nums), " ".join(map(str, nums)), s)


def run_std(inp):
    # 经临时文件喂入，避免超长串在 Windows 管道上的编码问题
    tmp = os.path.join(DATA, "_tmp.in")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(inp)
    with open(tmp, "r", encoding="utf-8") as fin:
        p = subprocess.run(
            [sys.executable, os.path.join(DIR, "std.py")],
            stdin=fin, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    if os.path.exists(tmp):
        os.remove(tmp)
    if p.returncode != 0:
        raise RuntimeError(p.stderr or p.stdout or "std failed")
    return p.stdout


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5523)
    # 超长 s
    long_s = "9" + "".join(str(rng.randint(0, 9)) for _ in range(9999))
    long_s2 = "1" + "0" * 9999

    cases = [
        dump([5, 4, 8, 2], "5416"),           # 样例1
        dump([1, 2, 3], "111"),               # 样例2
        dump([0], "1"),                       # 只有 0
        dump([1], "1"),                       # 无解 -> -1
        dump([9, 8, 7], "10"),                # 更短位数更大
        dump([0, 1, 2], "100"),               # 前导零相关
        dump([5], "5"),                       # 等长失败
        dump([2, 0], "20"),                   # 卡前导零
        dump([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], long_s),   # 接近上限位数
        dump([1, 2, 3, 4, 5], long_s2),       # 10000 位边界
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok", "out=", out.strip()[:40])


if __name__ == "__main__":
    main()
