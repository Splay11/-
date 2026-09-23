# -*- coding: utf-8 -*-
"""P7142 造数：Unix 风格绝对路径化简。

stdin：一行 path。输出规范路径。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(714220260915)

N_MAX = 3000
ALPH = string.ascii_letters + string.digits + "._"


def naive(path):
    """另一种写法：先按 / 切开再过滤，与手写扫描对拍。"""
    st = []
    for part in path.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            if st:
                st.pop()
            continue
        st.append(part)
    return "/" if not st else "/" + "/".join(st)


def write_case(idx, path):
    assert 1 <= len(path) <= N_MAX
    assert path[0] == "/"
    for ch in path:
        assert ch.isalnum() or ch in "./_"
    (DATA / f"{idx}.in").write_bytes(path.encode("utf-8"))
    ans = solve(path)
    expect = naive(path)
    assert ans == expect, (idx, ans, expect)
    assert ans.startswith("/")
    if ans != "/":
        assert not ans.endswith("/")
        assert "//" not in ans
        assert "/./" not in ans and "/../" not in ans
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def rand_name():
    k = RNG.randint(1, 6)
    # 偶尔造 ... 和 .... ，但不要单独造出恰好是 . 或 .. 的名字（那些有专门语义）
    if RNG.random() < 0.15:
        return RNG.choice(["...", "....", "_tmp", "a_b"])
    s = "".join(RNG.choice(string.ascii_lowercase + string.digits + "_") for _ in range(k))
    if s in (".", ".."):
        s = "x"
    return s


def rand_path(n_parts):
    parts = []
    for _ in range(n_parts):
        r = RNG.random()
        if r < 0.15:
            parts.append(".")
        elif r < 0.3:
            parts.append("..")
        else:
            parts.append(rand_name())
    # 段与段之间随机塞 1～3 个斜杠，覆盖连续斜杠
    s = "/"
    for i, p in enumerate(parts):
        s += p
        if i + 1 < n_parts:
            s += "/" * RNG.randint(1, 3)
    if RNG.random() < 0.5:
        s += "/"
    return s[:N_MAX] if len(s) > N_MAX else s


def long_slash_dots():
    # 压满：大量 / 和 . / ..
    chunks = []
    while sum(len(x) for x in chunks) < N_MAX - 10:
        r = RNG.random()
        if r < 0.4:
            chunks.append("/" * RNG.randint(1, 5))
        elif r < 0.55:
            chunks.append(".")
        elif r < 0.7:
            chunks.append("..")
        else:
            chunks.append(rand_name())
    s = "".join(chunks)
    if not s.startswith("/"):
        s = "/" + s
    return s[:N_MAX]


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = rand_path(12)
    p9 = long_slash_dots()
    p10 = "/" + "/".join(["a", ".", "..", "b"] * 200)
    # 压满上限：后面补普通目录名，避免截断落在非法位置
    while len(p10) + 3 <= N_MAX:
        p10 += "/x"
    if len(p10) < N_MAX:
        p10 += "/" * (N_MAX - len(p10))
    p10 = p10[:N_MAX]
    if not p10.startswith("/"):
        p10 = "/" + p10[: N_MAX - 1]

    plan = [
        ("/home/",
         "样例 1", "去掉末尾斜杠得到 $/home$",
         "末尾仍留 $/home/$"),
        ("/home//foo/",
         "样例 2", "合并连续斜杠得到 $/home/foo$",
         "中间留下空目录名"),
        ("/home/user/Documents/../Pictures",
         "样例 3，$..$ 回到上一级", "$/home/user/Pictures$",
         "没有弹出 $Documents$"),
        ("/../",
         "样例 4，根目录再往上", "仍是 $/$",
         "弹出后变成空串"),
        ("/.../a/../b/c/../d/./",
         "样例 5，$...$ 是普通目录名", "$/.../b/d$",
         "把 $...$ 当成 $..$ 得到 $/b/d$"),
        ("/",
         "已经是根目录", "答案 $/$",
         "输出空串"),
        ("/a/./b/../../c/",
         "经典组合：当前目录和两级返回", "$/c$",
         "少弹一次得到 $/a/c$"),
        (p8,
         "小随机目录名、$.$、$..$ 与多余斜杠", "栈模拟与 split 过滤对拍",
         "把下划线目录名拆坏"),
        (p9,
         "压满约 $3000$，大量斜杠与点", "线性扫一遍",
         "$O(n^2)$ 反复拼接字符串可能 TLE"),
        (p10,
         "压满重复模式 $a/./../b$", "最终只剩规范路径",
         "栈弹出写错导致越界"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (path, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, path))

    for i, (path, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        assert ib.decode("utf-8") == path
        got = ob.decode("utf-8")[:-1]
        assert got == answers[i - 1] == naive(path)

    assert answers[0] == "/home"
    assert answers[1] == "/home/foo"
    assert answers[2] == "/home/user/Pictures"
    assert answers[3] == "/"
    assert answers[4] == "/.../b/d"
    assert answers[5] == "/"
    assert answers[6] == "/c"

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7142 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行 Unix 绝对路径 $path$。",
        "输出：化简后的规范路径。",
        "",
        r"约束：$1\le |path|\le 3000$，仅含字母、数字、点、斜杠和下划线。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：手写扫描必须等于 $split('/')$ 后用栈过滤。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans[:60], "len_in", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
