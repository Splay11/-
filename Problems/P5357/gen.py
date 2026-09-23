# -*- coding: utf-8 -*-
from pathlib import Path

from std import is_valid

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def fmt_out(ok):
    return ("true" if ok else "false") + "\n"


def dump(idx, t, note):
    ok = is_valid(t)
    inn = t.encode("utf-8")
    (DATA / f"{idx}.in").write_bytes(inn)
    (DATA / f"{idx}.out").write_bytes(fmt_out(ok).encode("utf-8"))
    print(f"case {idx}: n={len(t)} ans={ok} note={note}")


dump(1, "[()]{}", "样例1 合法嵌套并列")
dump(2, "([)]", "样例2 交叉")
dump(3, "", "样例3 空串")
dump(4, "()", "单对")
dump(5, "{{[]}}", "深层嵌套")
dump(6, "())", "多余闭封口")
dump(7, "(((", "只有开封口")
dump(8, "{[()()]}[]", "混合合法")
dump(9, "(" * 50000 + ")" * 50000, "n=1e5 合法深嵌套")
dump(10, "(" * 100000, "n=1e5 全开，卡计数相等")

for i in range(1, 11):
    t = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    got = fmt_out(is_valid(t))
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    if i != 3:
        assert not inn.endswith(b"\n"), i
    else:
        assert inn == b""
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
