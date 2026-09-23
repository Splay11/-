#!/usr/bin/env python3
"""生成层序数组建树题的 10 组测试数据。"""
from __future__ import annotations

from pathlib import Path
import random
import sys

sys.setrecursionlimit(10000)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(tree_arr):
    if not tree_arr or tree_arr[0] is None:
        return None
    q = []
    rt = TreeNode(tree_arr[0])
    q.append(rt)
    index = 1
    while q and index < len(tree_arr):
        node = q.pop(0)
        if index < len(tree_arr) and tree_arr[index] is not None:
            node.left = TreeNode(tree_arr[index])
            q.append(node.left)
        index += 1
        if index < len(tree_arr) and tree_arr[index] is not None:
            node.right = TreeNode(tree_arr[index])
            q.append(node.right)
        index += 1
    return rt


def serialize(root, keep_trailing_null: bool = False) -> list[int]:
    if root is None:
        return []
    arr = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            arr.append(-1)
            continue
        arr.append(node.val)
        q.append(node.left)
        q.append(node.right)
    if not keep_trailing_null:
        while arr and arr[-1] == -1:
            arr.pop()
    return arr


def traverse(root: TreeNode | None) -> str:
    pre, inn, post = [], [], []

    def preorder(u):
        if u is None:
            return
        pre.append(u.val)
        preorder(u.left)
        preorder(u.right)

    def inorder(u):
        if u is None:
            return
        inorder(u.left)
        inn.append(u.val)
        inorder(u.right)

    def postorder(u):
        if u is None:
            return
        postorder(u.left)
        postorder(u.right)
        post.append(u.val)

    preorder(root)
    inorder(root)
    postorder(root)
    return (
        " ".join(map(str, pre))
        + "\n"
        + " ".join(map(str, inn))
        + "\n"
        + " ".join(map(str, post))
        + "\n"
    )


def solve_arr(arr: list[int]) -> str:
    tree_arr = [None if x == -1 else x for x in arr]
    return traverse(build_tree(tree_arr))


def format_in(arr: list[int]) -> str:
    return str(len(arr)) + "\n" + " ".join(map(str, arr))


def write_in(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n")
    if text.endswith("\n"):
        text = text[:-1]
    path.write_text(text, encoding="utf-8")


def write_out(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def random_tree(n_nodes: int, rng: random.Random) -> TreeNode:
    nodes = [TreeNode(rng.randint(1, 10**9)) for _ in range(n_nodes)]
    open_nodes = [nodes[0]]
    for i in range(1, n_nodes):
        parent = rng.choice(open_nodes)
        free = []
        if parent.left is None:
            free.append("L")
        if parent.right is None:
            free.append("R")
        side = rng.choice(free)
        if side == "L":
            parent.left = nodes[i]
        else:
            parent.right = nodes[i]
        if parent.left is not None and parent.right is not None:
            open_nodes.remove(parent)
        open_nodes.append(nodes[i])
    return nodes[0]


def left_chain(n_nodes: int, rng: random.Random) -> TreeNode:
    nodes = [TreeNode(rng.randint(1, 10**9)) for _ in range(n_nodes)]
    for i in range(n_nodes - 1):
        nodes[i].left = nodes[i + 1]
    return nodes[0]


def right_chain(n_nodes: int, rng: random.Random) -> TreeNode:
    nodes = [TreeNode(rng.randint(1, 10**9)) for _ in range(n_nodes)]
    for i in range(n_nodes - 1):
        nodes[i].right = nodes[i + 1]
    return nodes[0]


def complete_tree(n_nodes: int, rng: random.Random) -> TreeNode:
    nodes = [TreeNode(rng.randint(1, 10**9)) for _ in range(n_nodes)]
    for i in range(n_nodes):
        li, ri = 2 * i + 1, 2 * i + 2
        if li < n_nodes:
            nodes[i].left = nodes[li]
        if ri < n_nodes:
            nodes[i].right = nodes[ri]
    return nodes[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260906)

    cases: list[list[int]] = []

    # 1 样例1
    cases.append([1, 2, 3, 4, 5])
    # 2 样例2：中间有空
    cases.append([1, -1, 2, 3])
    # 3 单结点
    cases.append([7])
    # 4 只有左儿子的小树
    cases.append([1, 2, -1, 3, -1])
    # 5 只有右儿子的链（保留末尾 -1）
    root = right_chain(8, rng)
    cases.append(serialize(root, keep_trailing_null=True))
    # 6 完全二叉树
    cases.append(serialize(complete_tree(15, rng), keep_trailing_null=False))
    # 7 随机，带空洞
    cases.append(serialize(random_tree(40, rng), keep_trailing_null=False))
    # 8 hack：根右空、左子树很深；卡把 -1 当结点 / 空结点还入队
    cases.append(serialize(left_chain(30, rng), keep_trailing_null=True))
    # 9 大随机
    cases.append(serialize(random_tree(800, rng), keep_trailing_null=False))
    # 10 大右链（数组接近 2n，卡层序下标）
    cases.append(serialize(right_chain(1000, rng), keep_trailing_null=False))

    assert len(cases) == 10
    for idx, arr in enumerate(cases, 1):
        if not arr or arr[0] == -1:
            raise SystemExit(f"illegal root in case {idx}")
        if len(arr) > 2000:
            raise SystemExit(f"n too large in case {idx}: {len(arr)}")
        for x in arr:
            if x != -1 and not (1 <= x <= 10**9):
                raise SystemExit(f"value out of range in case {idx}")
        inn = format_in(arr)
        out = solve_arr(arr)
        write_in(DATA / f"{idx}.in", inn)
        write_out(DATA / f"{idx}.out", out)

    for idx, arr in enumerate(cases, 1):
        got = solve_arr(arr)
        want = (DATA / f"{idx}.out").read_text(encoding="utf-8")
        if got != want:
            raise SystemExit(f"校验失败: {idx}")
    print("generated 10 cases OK")
    for idx, arr in enumerate(cases, 1):
        print(f"  {idx}: n={len(arr)}")


if __name__ == "__main__":
    main()
