def maxPathSum(arr, index, n):
    # 计算当前节点的左子节点和右子节点的索引
    left_index = 2 * index + 1
    right_index = 2 * index + 2

    # 如果是叶子节点，直接返回该节点的值
    if left_index >= n and right_index >= n:
        return arr[index]

    left_sum = 0
    right_sum = 0

    # 如果左子树存在，递归计算左子树的最大路径和
    if left_index < n:
        left_sum = maxPathSum(arr, left_index, n)

    # 如果右子树存在，递归计算右子树的最大路径和
    if right_index < n:
        right_sum = maxPathSum(arr, right_index, n)

    # 返回当前节点的值加上左右子树最大路径和
    return arr[index] + max(left_sum, right_sum)

# 主函数
if __name__ == "__main__":
    n = int(input())  # 输入节点数
    arr = list(map(int, input().split()))  # 输入完全二叉树的节点值
    
    # 从根节点开始计算最大路径和
    print(maxPathSum(arr, 0, n))
