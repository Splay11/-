# -*- coding: utf-8 -*-
"""生成 data/*.in/*.out；自校验与 std.py 一致。固定种子，含近满约束极限组。"""

import ast
import importlib.util
import json
import random
from pathlib import Path

SEED = 472406897
RNG = random.Random(SEED)

# 题面：路径总长 <=128，深度 <=7（整条路径上目录层级不过深），n<=1e5，size<=1e9
PATH_MAX = 128
DEPTH_MAX = 7  # 题面：目录深度不高于 7 层（整条路径用 `/` 分段后不宜过多）
N_MAX = 100_000


def parse_leading_string(s: str):
    s = s.strip()
    i = 0
    while i < len(s) and s[i] in " \t":
        i += 1
    if i >= len(s) or s[i] != '"':
        raise ValueError("bad line")
    i += 1
    out = []
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 1
            if i < len(s):
                out.append(s[i])
                i += 1
            continue
        if c == '"':
            i += 1
            break
        out.append(c)
        i += 1
    rest = s[i:].lstrip()
    return "".join(out), rest


def split_two_top_arrays(s: str):
    s = s.strip()
    if not s.startswith("["):
        raise ValueError("need [")
    depth = 0
    in_str = False
    esc = False
    for i, c in enumerate(s):
        if esc:
            esc = False
            continue
        if c == "\\" and in_str:
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                first = s[: i + 1]
                j = i + 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                if j >= len(s) or s[j] != ",":
                    raise ValueError("comma between arrays")
                j += 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                second = s[j:]
                return first, second
    raise ValueError("unclosed array")


def parse_line(line: str):
    target, rest = parse_leading_string(line)
    if not rest.startswith(","):
        raise ValueError("comma")
    rest = rest[1:].strip()
    files_str, sizes_str = split_two_top_arrays(rest)
    files = ast.literal_eval(files_str)
    sizes = ast.literal_eval(sizes_str)
    return target, files, sizes


def expected(target: str, files: list, sizes: list) -> list:
    exists = any(p == target or (len(p) > len(target) and p.startswith(target + "/")) for p in files)
    if not exists:
        return []
    agg = {}
    for p, sz in zip(files, sizes):
        if p == target:
            continue
        if not (len(p) > len(target) and p.startswith(target + "/")):
            continue
        rel = p[len(target) + 1 :]
        slash = rel.find("/")
        if slash < 0:
            child = p
        else:
            child = target + "/" + rel[:slash]
        agg[child] = agg.get(child, 0) + int(sz)
    if not agg:
        return []
    mx = max(agg.values())
    out = [k for k, v in agg.items() if v == mx]
    out.sort()
    return out


def fmt_out(paths: list) -> str:
    return json.dumps(paths, ensure_ascii=False) + "\n"


def line_from_tfs(target: str, files: list, sizes: list) -> str:
    return (
        json.dumps(target, ensure_ascii=False)
        + ", "
        + json.dumps(files, ensure_ascii=False)
        + ", "
        + json.dumps(sizes)
    )


def path_join_under(target: str, parts: list) -> str:
    """parts 为不含斜杠的分段名。"""
    s = target + "/" + "/".join(parts)
    if len(s) > PATH_MAX:
        raise ValueError(f"path too long {len(s)}")
    return s


def depth_segments(path: str) -> int:
    """非空路径上 `/` 分隔得到的段数（含文件名片段）。"""
    parts = [x for x in path.split("/") if x != ""]
    return len(parts)


def assert_constraints(target: str, files: list, sizes: list) -> None:
    assert len(files) == len(sizes)
    assert 1 <= len(files) <= N_MAX
    for p in files + [target]:
        assert 1 <= len(p) <= PATH_MAX, (len(p), p[:80])
        assert depth_segments(p) <= DEPTH_MAX, (depth_segments(p), p[:80])
    for z in sizes:
        assert 0 <= int(z) <= 10**9


def build_cases():
    """返回 10 条 stdin 单行字符串（无末尾换行）。"""
    cases = []

    # 1–3 题面样例（格式金标准）
    cases.append(
        '"/dir1/dir2-1", ["/dir0/dir1-1/file1-1", "/dir1/dir1-1/file1-1", "/dir1/dir2-1/file3-1", "/dir1/dir2-1/file3-2", "/dir1/dir2-1/dir3-1/file4-1"], [8192, 81920, 2048, 8192, 1024]'
    )
    cases.append(
        '"/dir1", ["/dir0/dir2-1/file3-1", "/dir1/dir2-1/file3-1", "/dir1/dir2-1/file3-2", "/dir1/dir2-2/file3-3", "/dir1/file2-3"], [10240, 4096, 8192, 10240, 8192]'
    )
    cases.append(
        '"/dir1", ["/dir1/dir1/file1", "/dir1/dir1/file2", "/dir1/dir2/file3"], [1024, 2048, 3072]'
    )

    # 4–7 边界 / hack
    cases.append('"/missing", ["/a/b", "/b/c", "/c/d"], [1, 2, 3]')
    cases.append('"/solo", ["/solo"], [100]')
    cases.append('"/dir", ["/dir1/sub/f"], [999]')
    cases.append('"/x", ["/x/a/p", "/x/b/q"], [100, 100]')

    # 8 中层：深度贴满 7 段 + 多文件聚在同一一级子目录 c0
    target8 = "/t8"
    files8 = []
    sizes8 = []
    for i in range(800):
        parts = ["c0", "d1", "d2", "d3", f"leaf{i:04d}"]
        p = path_join_under(target8, parts)
        assert depth_segments(p) <= DEPTH_MAX
        sizes8.append(RNG.randint(0, 10**6))
        files8.append(p)
    cases.append(line_from_tfs(target8, files8, sizes8))

    # 9 极限：5e4 条、每条路径总长 128、深度 <=7、size 大量顶 1e9
    target9 = "/Z9"
    files9 = []
    sizes9 = []
    n9 = 50_000
    for i in range(n9):
        side = "A" if i % 2 == 0 else "B"
        # 形态：/Z9/A/00000_<pad>/t —— 三段目录 + 文件名，总长 128
        head = f"{target9}/{side}/{i:05d}_"
        tail = "/t"
        need = PATH_MAX - len(head) - len(tail)
        assert need >= 1
        pad = ("P" * need)[:need]
        p = head + pad + tail
        assert len(p) == PATH_MAX
        assert depth_segments(p) <= DEPTH_MAX
        files9.append(p)
        sizes9.append(10**9 if i % 17 != 0 else 0)
    cases.append(line_from_tfs(target9, files9, sizes9))

    # 10 极限：n=1e5；一级子项 c0 下极多文件、c1 少量大文件；单条路径总长 128
    target10 = "/MX"
    files10 = []
    sizes10 = []
    n0 = 99_900
    for i in range(n0):
        head = f"{target10}/c0/{i:010d}_"
        tail = "/f"
        need = PATH_MAX - len(head) - len(tail)
        assert need >= 1
        pad = ("x" * need)[:need]
        p = head + pad + tail
        assert len(p) == PATH_MAX
        assert depth_segments(p) <= DEPTH_MAX
        files10.append(p)
        sizes10.append(RNG.randint(0, 50_000))
    for i in range(100):
        p = path_join_under(target10, ["c1", f"b{i:03d}", "leaf"])
        assert depth_segments(p) <= DEPTH_MAX
        files10.append(p)
        sizes10.append(10**9)
    assert len(files10) == N_MAX
    cases.append(line_from_tfs(target10, files10, sizes10))

    assert len(cases) == 10
    return cases


def load_solution_class():
    p = Path(__file__).resolve().parent / "std.py"
    spec = importlib.util.spec_from_file_location("p4724_std", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution


def main() -> None:
    data = Path(__file__).resolve().parent / "data"
    data.mkdir(parents=True, exist_ok=True)
    Sol = load_solution_class()
    cases = build_cases()
    for i, line in enumerate(cases, start=1):
        target, files, sizes = parse_line(line)
        assert_constraints(target, files, sizes)
        want = expected(target, files, sizes)
        got = Sol().findMaxOccupiedPaths(target, files, sizes)
        if got != want:
            raise SystemExit(f"std mismatch case {i}: want={want} got={got}")
        inp = data / f"{i}.in"
        outp = data / f"{i}.out"
        inp.write_bytes(line.encode("utf-8"))
        with outp.open("w", encoding="utf-8", newline="\n") as f:
            f.write(fmt_out(want))
    for i in range(1, len(cases) + 1):
        line = (data / f"{i}.in").read_text(encoding="utf-8").strip()
        target, files, sizes = parse_line(line)
        disk = json.loads((data / f"{i}.out").read_text(encoding="utf-8"))
        got = Sol().findMaxOccupiedPaths(target, files, sizes)
        if got != disk:
            raise SystemExit(f"reverify fail {i}")
    print("ok:", len(cases), "pairs; max n=", max(len(parse_line(c)[1]) for c in cases))


if __name__ == "__main__":
    main()
