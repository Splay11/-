## 思路：暴力模拟

枚举x从小到大,从第一个数开始，每隔x个数，将这些数循环移位，直到最后一个数。

为什么复杂度过得去？

考虑每次会取$\frac{n}{x}$ 个数出来进行操作，那么总的操作次数是一个**调和级数**:$\sum_{x=1}^{n} \frac{n}{x} = nlogn$


## 代码
### python
```python
n = int(input())
# 得到一个长度为n的数组，1~n
a = [i for i in range(1, n+1)]
for x in range (1 , n - 1):
    # 得到一个长度为n//x的数组，从x-1开始，间隔为x
    tmp = [a[i] for i in range(x - 1, n , x)]
    # 将tmp数组循环左移一位
    tmp = [tmp[-1]] + tmp[:-1]
    # 将tmp数组的值赋给a数组
    for i in range(x - 1 , n , x):
        a[i] = tmp[i // x]
# 输出a数组
print(*a)
```


OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。