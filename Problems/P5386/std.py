from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def parse_tokens(line):
    # 去掉首尾花括号，按逗号拆成权值或空位 #
    s = line.strip()
    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]
    if not s:
        return []
    toks = []
    for p in s.split(","):
        p = p.strip()
        if p == "#":
            toks.append(None)
        else:
            toks.append(int(p))
    return toks


def build_tree(toks):
    # 层序建树：空位不入队，因此也不会再展开它的儿子
    if not toks or toks[0] is None:
        return None
    rt = TreeNode(toks[0])
    q = deque([rt])
    i = 1
    while q and i < len(toks):
        node = q.popleft()
        if i < len(toks):
            if toks[i] is not None:
                node.left = TreeNode(toks[i])
                q.append(node.left)
            i += 1
        if i < len(toks):
            if toks[i] is not None:
                node.right = TreeNode(toks[i])
                q.append(node.right)
            i += 1
    return rt


def tree_depth(root):
    # 广度优先：根到最远叶子经过的结点数
    if root is None:
        return 0
    q = deque([root])
    d = 0
    while q:
        d += 1
        sz = len(q)
        for _ in range(sz):
            node = q.popleft()
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
    return d


def solve_line(line):
    return tree_depth(build_tree(parse_tokens(line)))


def main():
    line = input()
    print(solve_line(line))


if __name__ == "__main__":
    main()
