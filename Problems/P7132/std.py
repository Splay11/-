class Node:
    def __init__(self, val):
        # 二叉树节点：值、左孩子、右孩子
        self.val = val
        self.left = None
        self.right = None


def build_tree(tokens):
    """按层序（含 null）还原二叉树。空序列表示空树。"""
    if not tokens or tokens[0] == "null":
        return None
    # 只用非空节点入队，null 表示这个位置没有孩子
    root = Node(int(tokens[0]))
    q = [root]
    i = 1
    idx = 0
    while idx < len(q) and i < len(tokens):
        cur = q[idx]
        idx += 1
        # 先读左孩子
        if i < len(tokens):
            if tokens[i] != "null":
                cur.left = Node(int(tokens[i]))
                q.append(cur.left)
            i += 1
        # 再读右孩子
        if i < len(tokens):
            if tokens[i] != "null":
                cur.right = Node(int(tokens[i]))
                q.append(cur.right)
            i += 1
    return root


def path_sum(root, target):
    """DFS + 回溯：从根走到叶子，沿途累加，和等于 target 就记下当前路径。
    先左后右，正好符合题面要求的输出顺序。节点值有负数，不能因为当前和已经超过就剪枝。
    """
    ans = []
    path = []

    def dfs(node, remain):
        if node is None:
            return
        path.append(node.val)
        remain -= node.val
        # 叶子：没有左右孩子
        if node.left is None and node.right is None:
            if remain == 0:
                ans.append(list(path))
        else:
            dfs(node.left, remain)
            dfs(node.right, remain)
        # 回溯，把当前节点从路径里拿掉，好试其他分支
        path.pop()

    dfs(root, target)
    return ans


def solve(tokens, target):
    root = build_tree(tokens)
    return path_sum(root, target)


def main():
    # 第一行：层序长度 n、目标和 targetSum
    n, target = map(int, input().split())
    if n == 0:
        # 空树没有第二行，也不存在任何路径
        tokens = []
    else:
        tokens = input().split()
    paths = solve(tokens, target)
    # 先输出路径条数，再按 DFS 从左到右逐行输出
    print(len(paths))
    for p in paths:
        print(" ".join(str(v) for v in p))


if __name__ == "__main__":
    main()
