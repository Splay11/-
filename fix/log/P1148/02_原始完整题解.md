## 思路:
区间乘积的因数个数显然符合单调性。区间越长，其因数个数越多。所以双指针一下即可。

复杂度:$O(n*p(a_i))$

其中函数$p(a_i)$ 代表$a_i$唯一分解定理表示法中本质不同的质数的个数.可以发现他显然是小于 $log a_i$的。所以复杂度够

还有个知识点你可能需要知道：[约数个数定理](https://baike.baidu.com/item/%E7%BA%A6%E6%95%B0%E4%B8%AA%E6%95%B0%E5%AE%9A%E7%90%86/4926961)

~~~python
from collections import defaultdict
n , k = list(map(int , input().split()))
a = list(map(int , input().split()))
maxa = 200005
f = [defaultdict(int) for i in range(maxa)]
p = [True] * maxa
# 类似埃氏筛的去转移，求解每个数其唯一分解定理表示法(质数,指数大小)。用dict存储
for i in range (2 , maxa):
	if not p[i]:
		continue
	f[i][i] = 1
	for j in range (i + i, maxa , i):
		if i in f[j // i]:
			f[j][i] = f[j // i][i] + 1
		else:
			f[j][i] = 1
		p[j] = False
# 双指针 - now_f 代表当前区间累积的唯一分解表示法 , now_val 代表当前区间累积的约数个数
now_f = defaultdict(int)
now_val = 1
ans = 0
i = 0
j = 0
while j < n:
    # 根据<约数个数定理>,进行转移更新
	for x in f[a[j]]:
		now_val //= now_f[x] + 1
		now_f[x] += f[a[j]][x]
		now_val *= now_f[x] + 1
	while now_val >= k and i <= j:
        # 根据<约数个数定理>,进行转移更新
		for x in f[a[i]]:
			now_val //= now_f[x] + 1
			now_f[x] -= f[a[i]][x]
			now_val *= now_f[x] + 1
		i += 1
	ans += i
	j += 1
	
print(ans)
~~~