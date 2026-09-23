n = int(input())  # 读入关卡数
# 读入两个数组 arr 和 brr
arr = list(map(int , input().split()))
brr = list(map(int , input().split()))

# 计算差分数组
diff_a = []
for i in range(n - 1):
    diff_a.append(arr[i + 1] - arr[i])
    
diff_b = []
for i in range(n - 1):
    diff_b.append(brr[i + 1] - brr[i])

# 滑动窗口方法
left = 0
right = 0
ans = 0
m = len(diff_a)  # 差分数组的长度

while left < m:
    # 右指针移动到相等区间的最右边
    while right < m and diff_a[right] == diff_b[right]:
        right += 1
    # 计算该区间的长度
    ans = max(ans , right - left)
    # 左指针移动到右指针的位置，开始新的检查
    left = right + 1
    right = left

# 输出最大长度加 1（因为差分数组少一个元素）
print(ans + 1)
