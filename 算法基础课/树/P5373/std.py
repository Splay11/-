import sys

sys.setrecursionlimit(10000)


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


def preorder(root, res):
    # 前序：根 -> 左 -> 右
    if root is None:
        return
    res.append(root.val)
    preorder(root.left, res)
    preorder(root.right, res)


def inorder(root, res):
    # 中序：左 -> 根 -> 右
    if root is None:
        return
    inorder(root.left, res)
    res.append(root.val)
    inorder(root.right, res)


def postorder(root, res):
    # 后序：左 -> 右 -> 根
    if root is None:
        return
    postorder(root.left, res)
    postorder(root.right, res)
    res.append(root.val)


def main():
    n = int(input())
    raw = list(map(int, input().split()))
    # 题面用 -1 表示空，转成 None 后再按层序数组建树
    tree_arr = [None if x == -1 else x for x in raw]
    root = build_tree(tree_arr)

    pre_res, in_res, post_res = [], [], []
    preorder(root, pre_res)
    inorder(root, in_res)
    postorder(root, post_res)

    print(" ".join(str(x) for x in pre_res))
    print(" ".join(str(x) for x in in_res))
    print(" ".join(str(x) for x in post_res))


if __name__ == "__main__":
    main()
