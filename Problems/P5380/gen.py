# -*- coding: utf-8 -*-
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import count_cabin

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5380)


def format_in(n, m, t):
    # 最后一行后不要换行符
    return str(n) + " " + str(m) + "\n" + t


def format_out(ans):
    # 末尾有且仅有一个换行符
    return str(ans) + "\n"


def dump(idx, n, m, t, note):
    ans = count_cabin(n, m, t)
    (DATA / f"{idx}.in").write_bytes(format_in(n, m, t).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: n={n} m={m} ans={ans} note={note}")


def adjacent(pairs):
    return "()" * pairs


def fully_nested(pairs):
    return "(" * pairs + ")" * pairs


def random_dyck(n, rnd):
    # n 为偶数；用随机 Dyck 路径生成合法括号串
    opens = n // 2
    closes = n // 2
    bal = 0
    chars = []
    for _ in range(n):
        can_open = opens > 0
        can_close = bal > 0 and closes > 0
        if can_open and can_close:
            if rnd.random() < 0.55:
                chars.append("(")
                opens -= 1
                bal += 1
            else:
                chars.append(")")
                closes -= 1
                bal -= 1
        elif can_open:
            chars.append("(")
            opens -= 1
            bal += 1
        else:
            chars.append(")")
            closes -= 1
            bal -= 1
    return "".join(chars)


def waves(blocks):
    # 若干段「全嵌套 + 若干相邻对」拼起来，打破单一结构
    parts = []
    for nest, adj in blocks:
        parts.append(fully_nested(nest))
        parts.append(adjacent(adj))
    return "".join(parts)


# 1-3：与改写题面三个样例一致
dump(1, 2, 1, "()", "样例1 单对 inner=0")
dump(2, 6, 3, "(()())", "样例2 近邻匹配 vs 最远匹配")
dump(3, 8, 5, "((()()))", "样例3 外层不能整除")

# 4：全是相邻 ()，卡 R-L / R-L+1 当内部长度
dump(4, 8, 3, adjacent(4), "全相邻 inner=0，m=3；错用跨度会漏计")

# 5：全嵌套，内部长度 0,2,4,...,8
dump(5, 10, 4, fully_nested(5), "全嵌套 m=4，只计 0/4/8")

# 6：m=1 时全部配对都算，答案必为 n/2
dump(6, 12, 1, waves([(2, 1), (1, 2)]), "m=1 全计；混合结构")

# 7：n=2、m 取到上界
dump(7, 2, 2, "()", "最小 n 且 m=n")

# 8：m=n 时只有 inner=0 能整除（inner 最大 n-2）
t8 = waves([(3, 2), (1, 1)])
n8 = len(t8)
dump(8, n8, n8, t8, "m=n 只计相邻对")

# 9：上限全嵌套，卡 O(n^2)/递归爆栈，以及 R-L 奇偶全错
n9 = 200000
dump(9, n9, 2, fully_nested(n9 // 2), "n=200000 全嵌套 m=2")

# 10：上限随机 Dyck，压测 I/O 与一般结构
n10 = 200000
t10 = random_dyck(n10, rng)
dump(10, n10, 7, t10, "n=200000 随机合法串 m=7")

# 自校验：用标程核心再算一遍
from std import count_cabin as chk

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    head, t = raw.split("\n", 1)
    n, m = map(int, head.split())
    got = chk(n, m, t)
    exp = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
    if got != exp:
        print(f"MISMATCH {i}: got={got} exp={exp}")
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
