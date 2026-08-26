## 思路

​	不难发现，就是将$n$分成两堆，每堆$\frac{n}{2}$个数。对于一个堆，我们将其划分成$i$个正整数相加的方案就是$C(\frac{n}{2}- 1, i - 1)$ 。因为可以看作$\frac{n}{2}$个$1$摆成一排，有$\frac{n}{2}-1$个空隙，我们选择其中的$i-1$个空隙即可分成$i$个部分了。

​	所以枚举$i$,另一堆就是$k-i$ 。答案就是
$$
\sum_{i=1}^{k-1}C(\frac{n}{2}- 1, i - 1) * C(\frac{n}{2}- 1, k - i - 1)
$$


​	答案比较大，需要**取模+求逆元**。类似的题目，我出过一个视频讲解的。大家可以看这里:https://www.bilibili.com/video/BV1GY4y1y7RA/?spm_id_from=333.999.0.0.

## 代码

python

```python
def getMethods (cost , k):   
    mod = 1000000007
    fac = [1]
    for i in range(1 , 200006):
        fac.append(fac[-1] * i % mod)
    def ksm (a , b):
        ans = 1
        base = a 
        while b != 0:
            if b & 1:
                ans = ans * base % mod 
            base = base * base % mod 
            b >>= 1
        return ans 
    # 奇数不合法
    if cost % 2 != 0:
        return 0
    def comb (n , m):
		# 这里弄不明白的话先去搞清楚逆元取模!!
        if m > n:
            return 0
        x = fac[n]
        y = fac[m] * fac[n - m] % mod 
        return x * ksm(y , mod - 2) % mod
	# 公式如上
    n = cost // 2
    ans = 0
    for i in range (1 , k):
        ans = (ans + comb(n - 1 , i - 1) * comb(n - 1 , k - i - 1) % mod) % mod
    return ans  

cost , k = list(map(int , input().split()))
print (getMethods(cost , k))
```