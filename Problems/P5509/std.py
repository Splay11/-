class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(tokens):
    # 按层序序列建树，null 表示空节点
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


def zigzag(root):
    if not root:
        return []
    # 奇数层从左到右，偶数层从右到左（层号从 1 开始）
    from collections import deque
    q = deque([root])
    ans = []
    left_to_right = True
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        if not left_to_right:
            level.reverse()
        ans.append(level)
        left_to_right = not left_to_right
    return ans


def main():
    n = int(input())
    tokens = input().split()
    assert len(tokens) == n
    levels = zigzag(build_tree(tokens))
    print(len(levels))
    for row in levels:
        print(*row)


if __name__ == "__main__":
    main()
