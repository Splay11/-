class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(tokens):
    if not tokens or tokens[0] == "null":
        return None
    root = TreeNode(int(tokens[0]))
    q = [root]
    i = 1
    while q and i < len(tokens):
        node = q.pop(0)
        if i < len(tokens):
            if tokens[i] != "null":
                node.left = TreeNode(int(tokens[i]))
                q.append(node.left)
            i += 1
        if i < len(tokens):
            if tokens[i] != "null":
                node.right = TreeNode(int(tokens[i]))
                q.append(node.right)
            i += 1
    return root


def width_of_binary_tree(root):
    if not root:
        return 0
    # BFS 同时记录编号；每层宽度 = 最右编号 - 最左编号 + 1
    # 每层把编号相对最左归零，避免编号爆炸
    from collections import deque
    q = deque([(root, 0)])
    ans = 0
    while q:
        size = len(q)
        _, left = q[0]
        right = left
        for _ in range(size):
            node, idx = q.popleft()
            idx -= left  # 归一化
            right = idx
            if node.left:
                q.append((node.left, idx * 2))
            if node.right:
                q.append((node.right, idx * 2 + 1))
        ans = max(ans, right + 1)
    return ans


def main():
    tokens = input().split()
    print(width_of_binary_tree(build_tree(tokens)))


if __name__ == "__main__":
    main()
