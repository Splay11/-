## 题解思路

### 1. 前缀和与二次前缀和  
- 令  
  $P[i]=\sum_{j=1}^{i}a_j$  
  （一维前缀和），  
  $Q[i]=\sum_{j=1}^{i}P[j]$  
  （前缀和的前缀和）。  
- 则任意长度为 $x$ 的子数组和的总和  
  ![](/p/2554/file/QianJianTec1745842727621.png?type=additional_file =400x60)
  可化简为  
  ![](/p/2554/file/QianJianTec1745842810145.png?type=additional_file =400x60)

### 2. 筛素数  
- 用埃氏筛在 $O(n\log\log n)$ 时间内算出长度 $1$ 到 $n$ 哪些是素数。

### 3. 针对素数长度做前缀和  
- 构造数组  
  $h[i]=$$\sum_{\substack{2\le y\le i\\y\text{ 为素数}}}g(y)$$mod M$,
   $M=998244353.$
- 每次询问 $[l,r]$ 时，答案就是  
  $\bigl(h[r]-h[l-1]\bigr)\bmod M,$  
  $O(1)$ 返回。

## 复杂度分析

- 前缀和 $P,Q$ 和所有 $g(x)$ 计算：$O(n)$  
- 埃氏筛素数：$O(n\log\log n)$  
- 构造 $h$：$O(n)$  
- 每次查询：$O(1)$，共 $m$ 次，加起来 $O(m)$  
- **总时间复杂度**：$O(n\log\log n + m)$  
- **额外空间**：$O(n)$

## 代码实现

### Python

```python
import sys
def main():
    input = sys.stdin.readline
    MOD = 998244353
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    # 1. 前缀和 P 和二次前缀和 Q
    P = [0] * (n+1)
    Q = [0] * (n+1)
    for i in range(1, n+1):
        P[i] = P[i-1] + a[i-1]
        Q[i] = Q[i-1] + P[i]
    # 2. 计算 g[x] mod M
    g = [0] * (n+1)
    for x in range(1, n+1):
        g[x] = (Q[n] - Q[x-1] - Q[n-x]) % MOD
    # 3. 埃氏筛
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    import math
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    # 4. 构造前缀和 h
    h = [0] * (n+1)
    for i in range(1, n+1):
        h[i] = h[i-1] + (g[i] if is_prime[i] else 0)
        if h[i] >= MOD:
            h[i] -= MOD
    # 5. 回答查询
    for _ in range(m):
        l, r = map(int, input().split())
        ans = (h[r] - h[l-1]) % MOD
        print(ans)

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer tk = new StringTokenizer(in.readLine());
        final int MOD = 998244353;
        int n = Integer.parseInt(tk.nextToken());
        int m = Integer.parseInt(tk.nextToken());
        long[] a = new long[n+1];
        tk = new StringTokenizer(in.readLine());
        for (int i = 1; i <= n; i++) {
            a[i] = Long.parseLong(tk.nextToken());
        }
        // 前缀和 P 和 Q
        long[] P = new long[n+1], Q = new long[n+1];
        for (int i = 1; i <= n; i++) {
            P[i] = P[i-1] + a[i];
            Q[i] = Q[i-1] + P[i];
        }
        // g[x]
        long[] g = new long[n+1];
        for (int x = 1; x <= n; x++) {
            g[x] = (Q[n] - Q[x-1] - Q[n-x]) % MOD;
            if (g[x] < 0) g[x] += MOD;
        }
        // 埃氏筛
        boolean[] isPrime = new boolean[n+1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int i = 2; i*i <= n; i++) {
            if (isPrime[i]) {
                for (int j = i*i; j <= n; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        // 构造 h
        long[] h = new long[n+1];
        for (int i = 1; i <= n; i++) {
            h[i] = h[i-1] + (isPrime[i] ? g[i] : 0);
            if (h[i] >= MOD) h[i] -= MOD;
        }
        // 回答查询
        PrintWriter out = new PrintWriter(System.out);
        for (int i = 0; i < m; i++) {
            tk = new StringTokenizer(in.readLine());
            int l = Integer.parseInt(tk.nextToken());
            int r = Integer.parseInt(tk.nextToken());
            long ans = (h[r] - h[l-1]) % MOD;
            if (ans < 0) ans += MOD;
            out.println(ans);
        }
        out.flush();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 998244353;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<ll> a(n+1);
    for(int i = 1; i <= n; i++) {
        cin >> a[i];
    }
    // 前缀和 P 和 Q
    vector<ll> P(n+1), Q(n+1);
    for(int i = 1; i <= n; i++){
        P[i] = P[i-1] + a[i];
        Q[i] = Q[i-1] + P[i];
    }
    // g[x]
    vector<ll> g(n+1);
    for(int x = 1; x <= n; x++){
        ll v = Q[n] - Q[x-1] - Q[n-x];
        v %= MOD;
        if (v < 0) v += MOD;
        g[x] = v;
    }
    // 埃氏筛
    vector<bool> isPrime(n+1, true);
    isPrime[0] = isPrime[1] = false;
    for(int i = 2; i * i <= n; i++){
        if(isPrime[i]){
            for(int j = i*i; j <= n; j += i){
                isPrime[j] = false;
            }
        }
    }
    // 构造 h
    vector<ll> h(n+1);
    for(int i = 1; i <= n; i++){
        h[i] = h[i-1] + (isPrime[i] ? g[i] : 0);
        if (h[i] >= MOD) h[i] -= MOD;
    }
    // 回答查询
    while(m--){
        int l, r;
        cin >> l >> r;
        ll ans = (h[r] - h[l-1]) % MOD;
        if(ans < 0) ans += MOD;
        cout << ans << "\n";
    }
    return 0;
}
```