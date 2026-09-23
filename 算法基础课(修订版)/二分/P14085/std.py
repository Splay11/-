def binary_search(A, x):
    # 初始化查找范围的左右边界
    left = 0
    right = len(A) - 1
	# 将数组分为: <= x 和 > x的部分
    # 这里取 <= 而不是 <  ，因为我们的目的是让L,R错开，而不是让L == R
    while left <= right:
        mid = (left + right) // 2
        # 如果mid 坐落于 > x 的部分， 让right 往前移动
        if A[mid] > x:
            right = mid - 1
        # 如果mid 坐落于 <= x 的部分， 让left 往后移动
        else:
            left = mid + 1
    # 整个算法结束，right 一定会落在 <= x 区域的最后一个位置
    # 此时目标值要出现，也一定出现于right所在的位置。
    # 当然有一些边界情况:
    # 1.如果 x < a[0] , 此时right 会被推向 -1
    # 2.如果 x 不存在 ，则A[right] 不会是x
    return right != -1 and A[right] == x

def main():
    # 读取数组长度n和查询次数Q
    n, Q = map(int, input().split())
    
    # 读取升序数组A
    A = list(map(int, input().split()))
    
    # 对每个查询进行二分查找
    for _ in range(Q):
        x = int(input())  # 每次查询的目标值
        # 调用二分查找函数，输出查询结果
        if binary_search(A, x):
            print("YES")
        else:
            print("NO")
    
if __name__ == "__main__":
    main()
