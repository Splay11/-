## 解题思路（用公式推导）

### 一、按因子聚合

$$
\begin{aligned}
g(n)
&=\sum_{i=1}^{n}\;\sum_{d\mid i} d^3
=\sum_{d=1}^{n}\; d^3\cdot \#\{\,i\le n:\, d\mid i\,\} \\
&=\sum_{d=1}^{n} d^3\left\lfloor \frac{n}{d}\right\rfloor .
\end{aligned}
$$

于是只需计算

$$
\boxed{\,g(n)=\sum_{d=1}^{n} d^3\Big\lfloor \frac{n}{d}\Big\rfloor\, } .
$$

### 二、整除分块

记 $q=\left\lfloor \frac{n}{d}\right\rfloor$。当 $d\in [L,R]$ 且

$$
q=\left\lfloor\frac{n}{L}\right\rfloor=\left\lfloor\frac{n}{R}\right\rfloor,
\quad R=\left\lfloor\frac{n}{q}\right\rfloor,
$$

则

$$
\sum_{d=L}^{R} d^3\left\lfloor \frac{n}{d}\right\rfloor
= q\cdot \sum_{d=L}^{R} d^3 .
$$

遍历区间时用 $L\leftarrow R+1$ 跳转，区间数为 $O(\sqrt n)$。

### 三、立方前缀和闭式

$$
\sum_{i=1}^{m} i^3=\left(\frac{m(m+1)}{2}\right)^2 .
$$

于是

$$
\sum_{d=L}^{R} d^3 = S(R)-S(L-1),
\quad
S(m)=\left(\frac{m(m+1)}{2}\right)^2 .
$$

所有运算在模 $M=10^9+7$ 下进行，$\frac12$ 用 $2^{-1}\equiv 500000004\bmod M$。

### 复杂度

* 时间：整除分块的区间个数 $O(\sqrt n)$，每段 $O(1)$ 计算。
* 空间：$O(1)$。


## 代码

### Python

```python
import sys
MOD = 10**9 + 7
INV2 = 500000004  # 2 的逆元

def sum_cubes(m: int) -> int:
    # S(m) = (m(m+1)/2)^2  (mod MOD)
    if m <= 0:
        return 0
    m %= MOD
    t = m * ((m + 1) % MOD) % MOD   # m(m+1)
    t = t * INV2 % MOD              # /2
    return t * t % MOD              # 平方

def solve():
    data = sys.stdin.read().strip().split()
    if not data: return
    n = int(data[0])
    ans = 0
    L = 1
    while L <= n:
        q = n // L                  # 当前商
        R = n // q                  # 该商的最右端
        part = (sum_cubes(R) - sum_cubes(L - 1)) % MOD  # 区间立方和
        ans = (ans + part * (q % MOD)) % MOD            # 加权累加
        L = R + 1
    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1_000_000_007L;
    static final long INV2 = 500_000_004L; // 2 的逆元

    // S(m) = (m(m+1)/2)^2  (mod MOD)
    static long sumCubes(long m) {
        if (m <= 0) return 0;
        m %= MOD;
        long t = m * ((m + 1) % MOD) % MOD; // m(m+1)
        t = t * INV2 % MOD;                 // /2
        return t * t % MOD;                 // 平方
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());

        long ans = 0, L = 1;
        while (L <= n) {
            long q = n / L;        // 当前商
            long R = n / q;        // 该商的最右端
            long seg = (sumCubes(R) - sumCubes(L - 1)) % MOD; // 区间立方和
            if (seg < 0) seg += MOD;
            ans = (ans + seg * (q % MOD)) % MOD;              // 加权累加
            L = R + 1;             // 下一段
        }
        System.out.println(ans % MOD);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1'000'000'007LL;
const long long INV2 = 500'000'004LL; // 2 的逆元

// S(m) = (m(m+1)/2)^2  (mod MOD)
long long sum_cubes(long long m) {
    if (m <= 0) return 0;
    m %= MOD;
    long long t = m * ((m + 1) % MOD) % MOD; // m(m+1)
    t = t * INV2 % MOD;                      // /2
    return (t * t) % MOD;                    // 平方
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n; 
    if (!(cin >> n)) return 0;

    long long ans = 0, L = 1;
    while (L <= n) {
        long long q = n / L;                 // 当前商
        long long R = n / q;                 // 该商的最右端
        long long seg = (sum_cubes(R) - sum_cubes(L - 1)) % MOD; // 区间立方和
        if (seg < 0) seg += MOD;
        ans = (ans + seg * (q % MOD)) % MOD;                    // 累加
        L = R + 1;                                              // 下一段
    }
    cout << (ans % MOD) << "\n";
    return 0;
}
```