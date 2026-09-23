class Node:
    def __init__(self, val):
        # 二叉搜索树节点：值、左孩子、右孩子
        self.val = val
        self.left = None
        self.right = None


def build_tree(tokens):
    """按层序（含 null）还原二叉树。题目保证结果是合法 BST。"""
    if not tokens or tokens[0] == "null":
        return None
    # 用列表当队列：只把非空节点入队，空位置跳过
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


def kth_largest(root, cnt):
    """BST 的中序是升序。用栈模拟「右-根-左」，等价于从大到小走，走到第 cnt 个停下。
    不用递归，避免链状树把调用栈撑爆。
    """
    stack = []
    cur = root
    while cur is not None or stack:
        # 一路向右，把沿途节点压栈（右边全是更大的值）
        while cur is not None:
            stack.append(cur)
            cur = cur.right
        cur = stack.pop()
        cnt -= 1
        if cnt == 0:
            return cur.val
        # 再转向左子树，那里全是更小的值
        cur = cur.left
    return None


def solve(tokens, cnt):
    root = build_tree(tokens)
    return kth_largest(root, cnt)


def main():
    # 第一行：层序长度 n、要求的第 cnt 大
    n, cnt = map(int, input().split())
    # 第二行：n 个记号，数字或 null
    tokens = input().split()
    # n 是层序记号个数，与第二行一一对应
    print(solve(tokens, cnt))


if __name__ == "__main__":
    main()
