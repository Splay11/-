# -*- coding: utf-8 -*-
"""P5334 造数：三角层台图上的无向欧拉回路。"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from std import solve

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def max_id(h):
    return h * (h + 1) // 2


def build_edges(h):
    edges = set()
    for r in range(2, h + 1):
        base = r * (r - 1) // 2
        prev = (r - 1) * (r - 2) // 2
        for c in range(1, r):
            u = base + c
            v = base + c + 1
            w = prev + c
            for a, b in ((u, v), (u, w), (v, w)):
                edges.add((min(a, b), max(a, b)))
    return edges


def check_path(h, start, path):
    need = 3 * h * (h - 1) // 2 + 1
    if len(path) != need:
        return "len %d != %d" % (len(path), need)
    if path[0] != start or path[-1] != start:
        return "start/end"
    edges = build_edges(h)
    used = set()
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        e = (min(a, b), max(a, b))
        if e not in edges:
            return "not-edge %s-%s" % (a, b)
        if e in used:
            return "reuse"
        used.add(e)
    if used != edges:
        return "missing"
    return None


def write_file(idx, queries):
    assert 1 <= len(queries) <= 50
    sm = 0
    for h, s in queries:
        assert 2 <= h <= 1000
        assert 1 <= s <= max_id(h)
        sm += h
    assert sm <= 1000

    in_lines = [str(len(queries))]
    out_lines = []
    for h, s in queries:
        in_lines.append("%d %d" % (h, s))
        path = solve(h, s)
        err = check_path(h, s, path)
        if err:
            raise RuntimeError("case %d h=%d s=%d: %s" % (idx, h, s, err))
        out_lines.append(" ".join(str(x) for x in path))

    in_path = os.path.join(DIR, "%d.in" % idx)
    out_path = os.path.join(DIR, "%d.out" % idx)
    with open(in_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(in_lines))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out_lines) + "\n")


def rand_start(rng, h):
    return rng.randint(1, max_id(h))


def main():
    rng = random.Random(5334)

    # 1-3 改写题面样例
    write_file(1, [(2, 3)])
    write_file(2, [(3, 4)])
    write_file(3, [(2, 2), (4, 7)])

    # 4 基础：最小层数，三个角都当起点
    write_file(4, [(2, 1), (2, 2), (2, 3)])

    # 5 边界：顶角、底左、底右、内部点
    write_file(5, [(5, 1), (5, 11), (5, 15), (5, 8)])

    # 6 构造：层数递增，覆盖建图递推
    write_file(6, [(3, 6), (4, 1), (6, 13), (7, 28)])

    # 7 随机小数据，便于暴力对拍
    qs = []
    remain = 40
    while remain >= 2 and len(qs) < 12:
        h = rng.randint(2, min(8, remain))
        qs.append((h, rand_start(rng, h)))
        remain -= h
    write_file(7, qs)

    # 8 hack：只建「竖向柱」或漏掉第三条边的假图；以及忽略多询问
    # 50 组 n=2 会卡只处理第一组的程序；n=6 内部点卡错误三角剖分
    qs = [(2, rng.choice([1, 2, 3])) for _ in range(44)]
    qs.append((6, 10))
    qs.append((8, 1))
    qs.append((8, 36))
    qs.append((9, 20))
    write_file(8, qs)

    # 9 大数据：若干中等层数，总和接近 1000
    qs = [(200, 1), (200, max_id(200)), (250, 12345), (350, 100)]
    write_file(9, qs)

    # 10 上限：单组 h=1000，从最后一个台位出发
    write_file(10, [(1000, max_id(1000))])

    # 生成后自校验：重读 in，再算一遍，与 out 文本一致
    for idx in range(1, 11):
        with open(os.path.join(DIR, "%d.in" % idx), "r", encoding="utf-8") as f:
            raw = f.read()
        if raw.endswith("\n\n"):
            raise RuntimeError("%d.in 末尾有多余空行" % idx)
        lines = raw.split("\n")
        k = int(lines[0])
        rebuilt = []
        for i in range(k):
            h, s = map(int, lines[1 + i].split())
            rebuilt.append(" ".join(str(x) for x in solve(h, s)))
        with open(os.path.join(DIR, "%d.out" % idx), "r", encoding="utf-8") as f:
            got = f.read()
        if not got.endswith("\n") or got.endswith("\n\n"):
            raise RuntimeError("%d.out 换行不符合规范" % idx)
        expect = "\n".join(rebuilt) + "\n"
        if got != expect:
            raise RuntimeError("%d.out 与标程不一致" % idx)
        print("ok", idx, "queries", k)


if __name__ == "__main__":
    main()
