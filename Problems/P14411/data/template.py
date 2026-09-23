import sys
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(tree_str: str) -> Optional[TreeNode]:
    s = tree_str.strip()
    if s in ("{}", "{#}"):
        return None
    if not (s.startswith("{") and s.endswith("}")):
        raise ValueError("bad tree")
    inner = s[1:-1].strip()
    if inner == "" or inner == "#":
        return None
    tokens = [t.strip() for t in inner.split(",")]
    if tokens[0] == "#":
        return None
    root = TreeNode(int(tokens[0]))
    q = deque([root])
    i = 1
    while q and i < len(tokens):
        node = q.popleft()
        if i < len(tokens):
            t = tokens[i]
            i += 1
            if t != "#":
                node.left = TreeNode(int(t))
                q.append(node.left)
        if i < len(tokens):
            t = tokens[i]
            i += 1
            if t != "#":
                node.right = TreeNode(int(t))
                q.append(node.right)
    return root


def parse_line(line: str):
    line = line.strip("\r\n")
    if not line:
        raise SystemExit(0)
    depth = 0
    end = -1
    for idx, ch in enumerate(line):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = idx
                break
    if end < 0:
        raise ValueError("bad input")
    tree_str = line[: end + 1]
    rest = line[end + 1 :]
    if not rest.startswith(","):
        raise ValueError("bad threshold")
    threshold = int(rest[1:].strip())
    return build_tree(tree_str), threshold


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
root, threshold = parse_line(line)
ans = Solution().analyzeSpiritPaths(root, threshold)
print("[" + ",".join(str(x) for x in ans) + "]")
