## 思路：set + 简单模拟
使用一个set维护当前被占用的点。每次插入/删除的时候检查是否值域在[1,x] , [y , n]内，更新答案，每次输出即可。
## 代码

### python
```python
t = int(input())
for _ in range(t):
    n , m , x , y = map(int , input().split())
    ans1 , ans2 = 0 , 0
    st = set()
    for i in range(m):
        p = int(input())
        if p not in st:
            st.add(p)
            if p <= x:
                ans1 += 1
            if p >= y:
                ans2 += 1
        else:
            st.remove(p)
            if p <= x:
                ans1 -= 1
            if p >= y:
                ans2 -= 1
        print(x - ans1 , n - y + 1 - ans2)
```


OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。