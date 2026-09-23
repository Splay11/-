# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def write_in(path, text):
    # .in 最后一行数据后不要换行
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    # .out 有且仅有一个末尾换行
    if not text.endswith("\n"):
        text = text + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run_std(inp):
    p = subprocess.run(
        [sys.executable, os.path.join(DIR, "std.py")],
        input=inp if inp.endswith("\n") else inp + "\n",
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout


def rand_part(rng, maxlen, leading_zeros=False):
    L = rng.randint(1, maxlen)
    if leading_zeros and L > 1:
        zeros = rng.randint(0, L - 1)
        rest = "".join(str(rng.randint(0, 9)) for _ in range(L - zeros))
        if rest == "" or all(c == "0" for c in rest):
            rest = str(rng.randint(1, 9)) + rest[1:] if len(rest) > 1 else str(rng.randint(0, 9))
        return "0" * zeros + rest
    if rng.random() < 0.1:
        return "0" * L
    s = str(rng.randint(1, 9))
    for _ in range(L - 1):
        s += str(rng.randint(0, 9))
    return s


def rand_ver(rng, parts, part_len, leading=False):
    return ".".join(rand_part(rng, part_len, leading) for _ in range(parts))


def long_digit(rng, length):
    return str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(length - 1))


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5499)
    cases = [
        "1.2\n1.10",
        "1.01\n1.001",
        "1.0\n1",
        "1.0.1\n1",
        "0.1\n1.1",
        "1.2.3\n1.2.3",
        # hack：超长修订号，不能用 64 位整数
        "1." + long_digit(rng, 80) + "\n1." + long_digit(rng, 79),
        "0001.000\n1",
        # 接近上限
        rand_ver(rng, 40, 12, True) + "\n" + rand_ver(rng, 40, 12, True),
        rand_ver(rng, 50, 9, True) + "\n" + rand_ver(rng, 45, 10, True),
    ]
    # 接近上限：总长约 500，含超长修订号（不能用 64 位整数）
    v9a = "1." + long_digit(rng, 498)
    v9b = "1." + long_digit(rng, 497)
    assert len(v9a) <= 500 and len(v9b) <= 500
    cases[8] = v9a + "\n" + v9b
    parts_a = [long_digit(rng, 8) for _ in range(55)]
    parts_b = ["0" + long_digit(rng, 7) for _ in range(55)]
    v10a = ".".join(parts_a)
    v10b = ".".join(parts_b)
    if len(v10a) > 500:
        v10a = v10a[:500].rstrip(".")
    if len(v10b) > 500:
        v10b = v10b[:500].rstrip(".")
    cases[9] = v10a + "\n" + v10b

    for i, inp in enumerate(cases, 1):
        in_path = os.path.join(DATA, "%d.in" % i)
        out_path = os.path.join(DATA, "%d.out" % i)
        write_in(in_path, inp)
        out = run_std(inp)
        write_out(out_path, out)
        # 重算比对
        again = run_std(inp)
        if again != out and again.rstrip("\n") + "\n" != out:
            # normalize to single trailing newline
            again_n = again if again.endswith("\n") else again + "\n"
            if again_n != out:
                raise AssertionError("mismatch case %d" % i)
        print("wrote", i)

    # 再用 std 对磁盘上的 .in 重算比对
    for i in range(1, 11):
        with open(os.path.join(DATA, "%d.in" % i), "r", encoding="utf-8") as f:
            raw = f.read()
        got = run_std(raw)
        got = got if got.endswith("\n") else got + "\n"
        with open(os.path.join(DATA, "%d.out" % i), "r", encoding="utf-8") as f:
            exp = f.read()
        if got != exp:
            raise AssertionError("recheck fail %d: %r vs %r" % (i, got, exp))
    print("all ok")


if __name__ == "__main__":
    main()
