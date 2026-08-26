## 思路1:数论+动态规划

### 1.切入点:一个很容易感觉到的,对我们很有启发性的事情

​	找出所有是$k$的倍数的数，假设总共$x$个。那么算下他们的子集个数$2^{x} - 1$ 

这就是答案了？并不是！ 这不是"$gcd$恰好等于$k$" 的子集个数，而是"$gcd$**是$k$的倍数**"的子集个数。观察**他们的关系**，我们可以发现：

"$gcd$**是$k$的倍数**"的子集个数 = "$gcd$恰好是k"的子集个数 +  "$gcd$恰好是$2k$"的子集个数 + .. +  "$gcd$恰好是$ck$"的子集个数

那么可以得到:

"$gcd$恰好是k"的子集个数" = "$gcd$**是$k$的倍数**"的子集个数    -  "$gcd$恰好是$2k$"的子集个数 - .. -  "$gcd$恰好是$ck$"的子集个数

这个东西显然就很dp了。

### 2.动态规划呼之欲出

状态:

令$bk_i$ 代表 序列中$i$的个数 . 桶装即可求解

令$f_i$ 代表 序列中 是$i$的倍数的数的个数

令$g_i$ 代表 序列中 $gcd$是$i$的倍数 的子集个数

令$dp_i$ 代表 序列中$gcd$恰好是$i$ 的子集个数

转移:

$bk_i$ ：桶装一下就好
$$
f_i = \sum_{i|j} bk_j
$$
$f_i$ 转移如上 , 类似埃式筛地去求即可。复杂度为$O(nlog\ n)$   
$$
g_i = 2^{f_i} - 1
$$
$g_i$  也直接求就好,但由于$f_i$ 可能比较大，实际求的时候我们需要来个快速幂或者提前预处理一下$2^{i}$ 


$$
dp_i = g_i - \sum_{j>i \wedge i|j} dp_j
$$
$dp_i$ 转移如上 , 类似埃式筛地去求即可。复杂度为$O(nlog\ n)$  。不过注意外层需要倒着扫。

## 代码
C++
```c++
#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int maxn = 1e5 + 5;
const int mod = 1e9 + 7;
ll ksm (ll a , ll b){
    ll ans = 1 , base = a;
    while (b){
        if (b & 1) ans = ans * base % mod;
        base = base * base % mod;
        b >>= 1;
    }
    return ans;
}
// 四个数组对应上面得四个状态
ll bk[maxn] , f[maxn] , g[maxn] , dp[maxn];
int main (){
    int n , k;
    cin >> n >> k;
    for (int i = 1 ; i <= n ; i++){
        int x; cin >> x;
        bk[x] ++;
    }
    // 参考上述f的转移方程
    for (int i = 1 ; i < maxn ; i++){
        for (int j = i ; j < maxn ; j += i){
            f[i] += bk[j];
        }
    }
    // 参考上述g的转移方程
    for (int i = 1 ; i < maxn ; i++){
        g[i] = (ksm(2 , f[i]) - 1 + mod) % mod;
    }
    // 参考上述dp的转移方程
    for (int i = maxn - 1 ; i >= 1 ; i --){
        dp[i] = g[i];
        for (int j = i + i ; j < maxn ; j += i){
            dp[i] = (dp[i] - dp[j] + mod) % mod;
        }
    }
    cout << dp[k] <<endl;
	return 0;
}
```

Java

```java
import java.util.*;
class Main{
    static int mod = 1000000007;
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(), k = scanner.nextInt();
        int[] a = new int[n];
        for(int i=0;i<n;i++){
            a[i] = scanner.nextInt();
        }
        int maxn = 100002;
        long[] cnt = new long[maxn], mulitiCnt = new long[maxn], subset = new long[maxn], dp = new long[maxn];
        for(int i=0;i<n;i++){
            cnt[a[i]]++;
        }
        for(int i=1;i<maxn;i++){
            for(int j=i;j<maxn;j += i){
                mulitiCnt[i] += cnt[j];
            }
        }
        for(int i=1;i<maxn;i++){
            subset[i] = (ksm(2L, mulitiCnt[i]) - 1 + mod) % mod;
        }
        for(int i=maxn-1;i>=1;i--){
            dp[i] = subset[i];
            for(int j=i+i;j<maxn;j+=i){
                dp[i] = (dp[i] - dp[j] + mod) % mod;
            }
        }
        System.out.println(dp[k]);
    }

    public static long ksm(long a, long b){
        long res = 1L;
        while(b > 0){
            if((b & 1) == 1){
                res = (res * a) % mod;
            }
            b >>= 1;
            a = (a * a) % mod;
        }
        return res;
    }
}
```

Python
```python

from random import *
import sys
from collections import * 
from math import * 
from functools import *
from heapq import *



def solve(n,k,arr):
    mx = max(arr)
    cc = [0]*(mx+1)
    for a in arr: cc[a] += 1
    fs = [1]*(n+1)
    MOD = 10**9+7
    for i in range(1,n+1):
        fs[i] = (2*fs[i-1])%MOD 
    for i in range(k,mx+1):
        for j in range(i*2,mx+1,i):
            cc[i] += cc[j]
    dp = [0]*(mx+1)
    ans = 0
    for i in range(k,mx+1)[::-1]:
        dp[i] = fs[cc[i]]-1
        for j in range(i*2,mx+1,i):
            dp[i] -= dp[j]
        dp[i] %= MOD 
    return dp[k] 


def main():
    for _ in range(1):
        n, k = list(map(int,input().split()))
        arr = list(map(int,input().split()))
        print(solve(n,k,arr))
if __name__ == "__main__":
    main()
```