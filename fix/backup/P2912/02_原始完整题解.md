## 解题思路

### 可达性分析
由于允许任意次相邻格子间交换“0”和“1”，且“1”们不可区分，只要保持“1”的总数 $K$ 不变，就能把这 $K$ 个“1”放到任意 $K$ 个格子上。因此，可达的所有状态就是：在 $N=n\times m$ 个格子中任取 $K$ 个位置放“1”。

### 奇偶性判定
定义权值

$W=\frac12\sum_{u\sim v}|x_u-x_v|.$

注意在网格图中，内部点度数为4（偶），角点度2（偶），只有“非角的边界点”度数3（奇）。由代数化简可知

$W\equiv\sum_{v\in S}x_v\pmod2,$

其中 $S$ 是所有非角边界格子，$|S|=2n+2m-8$。要使网格为“偶网格”，即在 $S$ 中放偶数个“1”。

### 计数方法
设
- $N=n\,m$；
- $K$ 初始“1”数；
- $s=|S|=2n+2m-8$，$t=N-s$。

方案数就是
$\sum_{\substack{0\le j\le s\\j\equiv0\!\!\pmod2}}$$\binom{s}{j}\binom{t}{K-j}.$
用预处理阶乘和逆元阶乘，在 $O(N)$ 时间内预compute，再 $O(s)$ 累加即可。


## 复杂度分析
- **时间复杂度**：预处理阶乘和逆阶乘 $O(N)$，循环累加 $O(s)\le O(N)$，总 $O(N)$；  
- **空间复杂度**：存阶乘与逆阶乘数组各 $O(N)$。

其中 $N=n\times m\le5\times10^5$，完全可行。


## 代码实现

### Python

```python
MOD = 10**9 + 7

def modpow(a, b):
    r = 1
    while b:
        if b & 1:
            r = r * a % MOD
        a = a * a % MOD
        b >>= 1
    return r

def prepare(n):
    # 预处理阶乘和逆阶乘
    fact = [1] * (n+1)
    invf = [1] * (n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1] * i % MOD
    invf[n] = modpow(fact[n], MOD-2)
    for i in range(n, 0, -1):
        invf[i-1] = invf[i] * i % MOD
    return fact, invf

def comb(n, k, fact, invf):
    if k < 0 or k > n:
        return 0
    return fact[n] * invf[k] % MOD * invf[n-k] % MOD

def main():
    n, m = map(int, input().split())
    k = 0
    for _ in range(n):
        row = input().strip()
        k += row.count('1')
    N = n * m
    # 计算奇度点数 S
    if n == 1 and m == 1:
        S = 0
    elif n == 1 or m == 1:
        S = 2
    else:
        S = 2 * (n + m - 4)
    fact, invf = prepare(N)
    ans = 0
    # 枚举放在 S 中的 1 的个数 t，要求 t 为偶
    for t in range(0, S+1, 2):
        ans = (ans + comb(S, t, fact, invf) * comb(N-S, k-t, fact, invf)) % MOD
    print(ans)

if __name__ == '__main__':
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final int MOD = 1_000_000_007;
    static long[] fact, invf;

    static long modpow(long a, long b) {
        long r = 1;
        while (b > 0) {
            if ((b & 1) == 1) r = r * a % MOD;
            a = a * a % MOD;
            b >>= 1;
        }
        return r;
    }

    static void prepare(int n) {
        fact = new long[n+1];
        invf = new long[n+1];
        fact[0] = 1;
        for (int i = 1; i <= n; i++) {
            fact[i] = fact[i-1] * i % MOD;
        }
        invf[n] = modpow(fact[n], MOD-2);
        for (int i = n; i > 0; i--) {
            invf[i-1] = invf[i] * i % MOD;
        }
    }

    static long comb(int n, int k) {
        if (k < 0 || k > n) return 0;
        return fact[n] * invf[k] % MOD * invf[n-k] % MOD;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String[] parts = in.readLine().split("\\s+");
        int n = Integer.parseInt(parts[0]), m = Integer.parseInt(parts[1]);
        int k = 0;
        for (int i = 0; i < n; i++) {
            String row = in.readLine().trim();
            for (char c : row.toCharArray()) if (c == '1') k++;
        }
        int N = n * m;
        int S;
        if (n == 1 && m == 1) S = 0;
        else if (n == 1 || m == 1) S = 2;
        else S = 2 * (n + m - 4);

        prepare(N);
        long ans = 0;
        for (int t = 0; t <= S; t += 2) {
            ans = (ans + comb(S, t) * comb(N-S, k-t) % MOD) % MOD;
        }
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
static const int MOD = 1e9+7;

long long modpow(long long a, long long b) {
    long long r = 1;
    while (b) {
        if (b & 1) r = r * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return r;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    int k = 0;
    int x;
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            cin >> x;
            if(x == 1) k++;
        }
    }

    int N = n * m;
    int S;
    if (n == 1 && m == 1) S = 0;
    else if (n == 1 || m == 1) S = 2;
    else S = 2 * (n + m - 4);

    // 预处理阶乘及逆元
    vector<long long> fact(N+1), invf(N+1);
    fact[0] = 1;
    for(int i = 1; i <= N; i++){
        fact[i] = fact[i-1] * i % MOD;
    }
    invf[N] = modpow(fact[N], MOD-2);
    for(int i = N; i > 0; i--){
        invf[i-1] = invf[i] * i % MOD;
    }

    auto comb = [&](int a, int b){
        if (b < 0 || b > a) return 0LL;
        return fact[a] * invf[b] % MOD * invf[a-b] % MOD;
    };

    long long ans = 0;
    for(int t = 0; t <= S; t += 2){
        ans = (ans + comb(S, t) * comb(N-S, k-t) % MOD) % MOD;
    }
    cout << ans << "\n";
    return 0;
}
```