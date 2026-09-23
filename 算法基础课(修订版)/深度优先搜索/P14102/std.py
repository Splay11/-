def dfs(nums, path, visited, result):
    # 终止条件：路径长度等于 nums 长度，说明一个排列生成完毕
    if len(path) == len(nums):
        result.append(path[:])  # 将当前路径加入结果
        return
    
    # 遍历每个元素，尝试加入当前路径
    for i in range(len(nums)):
        if not visited[i]:  # 如果当前数字未被访问
            visited[i] = True  # 标记为已访问
            path.append(nums[i])  # 将该数字加入路径
            dfs(nums, path, visited, result)  # 递归调用
            path.pop()  # 回溯，移除路径中的最后一个数字
            visited[i] = False  # 恢复标记为未访问

def main():
    # 读取输入
    n = int(input())  # 输入数组的长度
    nums = list(map(int, input().split()))  # 输入数组

    # 按字典序排序
    nums.sort()

    result = []  # 存储所有排列
    path = []    # 当前路径
    visited = [False] * n  # 标记每个数字是否被访问

    # 调用 DFS
    dfs(nums, path, visited, result)

    # 输出所有排列
    for perm in result:
        print(" ".join(map(str, perm)))  # 输出每个排列

if __name__ == "__main__":
    main()
