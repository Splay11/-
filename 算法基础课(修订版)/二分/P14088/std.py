import bisect

def count_pairs(A, C):
    # 排序数组 A
    A.sort()
    
    # 记录数对总数
    sum_pairs = 0
    
    # 遍历数组中的每个元素
    for a in A:
        target = a + C  # 计算目标值 x = A[i] + C
        
        # 使用 bisect 查找目标值的出现次数
        # bisect_left 返回第一个不小于 target 的位置
        # bisect_right 返回第一个大于 target 的位置
        count = bisect.bisect_right(A, target) - bisect.bisect_left(A, target)
        
        # 累加数对的数量
        sum_pairs += count
    
    return sum_pairs

def main():
    # 输入处理
    n = int(input())  # 输入数组的大小 n
    A = list(map(int, input().split()))  # 输入数组 A 的元素
    C = int(input())  # 输入整数 C
    
    # 计算并输出结果
    result = count_pairs(A, C)
    print(result)

if __name__ == "__main__":
    main()
