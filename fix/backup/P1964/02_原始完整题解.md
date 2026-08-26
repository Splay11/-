## 思路:暴力模拟

观察到n很小，可以使用一个二维数组f[i][j]代表i是否出现在过位置j.

然后每次移动数组时，直接模拟这个过程。然后用数组[l,n]这一段更新即可。

## 代码

### python
```python

# 读取输入的 n 和 q，分别表示数组大小和查询次数
n, q = map(int, input().split())

# 初始化数组 a，存储 1 到 n 的元素
a = [i for i in range(n + 1)]

# 创建一个二维布尔数组 f，f[i][j] 表示 i 是否出现在位置 j
f = [[False] * (n + 1) for _ in range(n + 1)]

# 初始化对角线，表示每个数 i 在位置 i 出现
for i in range(1, n + 1):
    f[i][i] = True

# 临时数组 b 用于存储移动过程中需要的值
b = [0] * (n + 1)

# 处理每个查询
for _ in range(q):
    # 读取查询的左右边界 l 和 r
    l, r = map(int, input().split())

    # 将 a[l:r+1] 的值复制到临时数组 b
    for i in range(l, r + 1):
        b[i] = a[i]

    j = l  # j 用于追踪新数组 a 的写入位置

    # 将 a[r+1:n] 的元素移动到 a[l:n]
    for i in range(r + 1, n + 1):
        a[j] = a[i]
        j += 1
    
    # 将临时数组 b 的元素从 l 开始写入 a
    for i in range(l, n + 1):
        a[j] = b[i]
        j += 1
        if j > n:  # 如果超出数组范围，停止写入
            break
    
    # 更新布尔数组 f，记录新的位置关系
    for i in range(l, n + 1):
        f[a[i]][i] = True

# 计算结果
result = []
for i in range(1, n + 1):
    # 对于每个 i，统计它在所有位置 j 的出现次数
    ans = sum(f[i][j] for j in range(1, n + 1))
    result.append(str(ans))

# 输出结果
print(" ".join(result))
```

OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。