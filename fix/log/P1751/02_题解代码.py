# 思路：二分答案

二分出 $k$ 的值为 $mid$

每次的 check 函数为，从字符串中第一个 `W` 字符开始，使用一次连续修改 $k$ 个字符的操作。

假设第一个 `W` 字符的位置为 $p$ ，那么最早的下一个开始使用的位置一定是 $p+k$ ，
我们要知道的就是 $s[j]='W'$ 的位置 $j$ ，满足 $j\geq p+k$ ，这部分可以从后向前遍历来预处理出来。

这样至多 $\lceil\frac{n}{k}\rceil$ 次操作就可以将所有字符都修改为 `R` ，判断需要的总次数和 $m$ 的大小关系即可。

时间复杂度：$O(n\log n)$

# 代码

```python
n, m = map(int, input().split())
s = input()

if 'W' not in s:
    print(0)
    exit(0)

nextW = [n for _ in range(n)]
for i in range(n - 1, -1, -1):
    if s[i] == 'W':
        nextW[i] = i
    elif i < n - 1:
        nextW[i] = nextW[i + 1]


def check(mid):
    p = nextW[0]
    c = 0
    while p < n:
        c += 1
        if p + mid < n:
            p = nextW[p + mid]
        else:
            p = n
    return c <= m


l, r = 1, n
while l < r:
    mid = (l + r) >> 1
    if check(mid):
        r = mid
    else:
        l = mid + 1

print(l)
```