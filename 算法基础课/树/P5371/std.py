class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(tree_arr):
    # 空树
    if not tree_arr or tree_arr[0] is None:
        return None

    q = []
    rt = TreeNode(tree_arr[0])
    q.append(rt)

    index = 1
    while q and index < len(tree_arr):
        node = q.pop(0)

        # 左孩子
        if index < len(tree_arr) and tree_arr[index] is not None:
            node.left = TreeNode(tree_arr[index])
            q.append(node.left)
        index += 1

        # 右孩子
        if index < len(tree_arr) and tree_arr[index] is not None:
            node.right = TreeNode(tree_arr[index])
            q.append(node.right)
        index += 1

    return rt


def level_order(root):
    # 层序：只访问非空结点
    if root is None:
        return []
    q = [root]
    res = []
    while q:
        node = q.pop(0)
        res.append(node.val)
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
    return res


def main():
    n = int(input())
    raw = list(map(int, input().split()))
    # 题面用 -1 表示空，转成 None 后再按层序数组建树
    tree_arr = [None if x == -1 else x for x in raw]
    root = build_tree(tree_arr)
    print(" ".join(str(x) for x in level_order(root)))


if __name__ == "__main__":
    main()
