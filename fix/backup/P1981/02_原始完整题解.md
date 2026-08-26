## 思路:模拟

考虑我们的边一定是从小的数连接到大的数，那么这张图不会有环，即有向无环图.那么我们直接模拟移动，

当u < v时,u往上移动，反之v往上移动，

直到到出现 max(u,v) > n 或者 u = v 结束。过程类似树上求最近公共祖先(LCA)。

如果u和v连通，还要判断是否和n也连通。


## 代码

### python
```python
n , u , v = map(int, input().split())
ans = 0
while u != v and max(u,v) <= n:
    if u < v:
        u += sum([int(x) for x in str(u)])
    else:
        v += sum([int(x) for x in str(v)])
    ans += 1
if u == v:
    while u < n:
        u += sum([int(x) for x in str(u)])
    if u == n:
        print(ans)
    else:
        print("NO")
else:
    print("NO")


```


OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。