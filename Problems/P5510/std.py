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


def same(a, b):
    if not a and not b:
        return True
    if not a or not b or a.val != b.val:
        return False
    return same(a.left, b.left) and same(a.right, b.right)


def is_subtree(root, sub):
    # 在 root 中找与 sub 完全同构的子树
    if not sub:
        return True
    if not root:
        return False
    if same(root, sub):
        return True
    return is_subtree(root.left, sub) or is_subtree(root.right, sub)


def main():
    n1 = int(input())
    t1 = input().split()
    n2 = int(input())
    t2 = input().split()
    assert len(t1) == n1 and len(t2) == n2
    ok = is_subtree(build_tree(t1), build_tree(t2))
    print("true" if ok else "false")


if __name__ == "__main__":
    main()
