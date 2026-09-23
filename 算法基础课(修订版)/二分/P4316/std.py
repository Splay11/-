def check(x, n, m, k):
    """
    检查给小明分配 x 个苹果是否可行
    n: 小孩总数, m: 苹果总数, k: 小明编号
    """
    if x == 0:
        return True
    
    needed = x  # 小明自己需要 x 个

    # 计算左边小孩需要的苹果数
    left_kids = k - 1
    if left_kids > 0:
        # 苹果数从 x-1 递减到 1 的小孩数量
        l = min(left_kids, x - 1)
        # 等差数列求和 (x-1 + x-l) * l // 2，简化为 l*x - l*(l+1)//2
        needed += l * x - l * (l + 1) // 2
        # 剩下的小孩每人一个
        if left_kids > l:
            needed += (left_kids - l)

    # 计算右边小孩需要的苹果数
    right_kids = n - k
    if right_kids > 0:
        # 苹果数从 x-1 递减到 1 的小孩数量
        r = min(right_kids, x - 1)
        # 等差数列求和
        needed += r * x - r * (r + 1) // 2
        # 剩下的小孩每人一个
        if right_kids > r:
            needed += (right_kids - r)

    return needed <= m

def solve():
    n, m, k = map(int, input().split())

    low, high = 1, m
    ans = 0

    # 二分查找答案
    while low <= high:
        mid = low + (high - low) // 2
        if mid == 0: # 至少一个苹果
            low = mid + 1
            continue
        
        if check(mid, n, m, k):
            # 如果 mid 可行，尝试更大的值
            ans = mid
            low = mid + 1
        else:
            # 如果 mid 不可行，需要减小
            high = mid - 1

    print(ans)

solve()
