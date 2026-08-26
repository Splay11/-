# 思路
根据题意，我们只需要考虑每个偶数段。
问题简化为：找到每个偶数段，找到这个偶数段中，和最小的一个子区间，然后将这个子区间的值减半即可。
那么这就是一个最大子数组和的问题，只不过这里要求的是最小子数组和。
我们依旧可以按照最大子数组和的模板来解决这道题。
即贪心地，每遇到一个数，就将其加入子区间，如果可以使得最终答案变得更大，则更新答案。
如果加入后使得子区间的和大于 0，那么只会使得我们整体的值变小，所以不能留，将区间清空即可。

[力扣53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/description/)

时间复杂度：O(n)

# 代码
```python
n = int(input())
a = list(map(int, input().split()))

# 找到每个偶数段，找到这个偶数段中，和最小的一个子区间，然后将这个子区间的值减半即可。
suma = sum(a)
l, r = 0, 0
ans = suma
while l < n:
    while l < n and a[l] % 2 != 0:
        l += 1
    if l < n:
        r = l
        while r < n and a[r] % 2 == 0:
            r += 1

        # [l, r - 1]
        cur = 0
        while l < r:
            cur += a[l]
            if cur < 0:
                ans = max(ans, suma - cur // 2)
            else:
                cur = 0
            l += 1

print(ans)
```