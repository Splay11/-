## 解题思路

给定一个“洞数”$k$。我们只统计满足如下条件的**非负整数**的个数：

* 不含前导 0（唯一允许为 0 本身）；
* 数位只由数字 0、8 组成；
* 数位“洞数”之和恰为 $k$。其中 0 记 1 个洞，8 记 2 个洞。

设答案为 $f(k)$。

1. 特判 $k=1$：唯一合法数是“0”，故 $f(1)=1$。
2. 当 $k\ge 2$ 时，任意合法数的**最高位必为 8**（否则前导 0 不合法）。最高位 8 贡献 2 个洞，剩余数位（长度可以为 0）仍由 $\{0,8\}$ 组成，其“洞数”还需凑成 $k-2$。
   用 $g(n)$ 表示使用 $\{0(=1\text{洞}),\,8(=2\text{洞})\}$ 构成的“序列”（允许长度为 0）的洞数和为 $n$ 的方案数。显然有

   $$
   g(0)=1,\qquad g(n)=g(n-1)+g(n-2)\ (n\ge1)
   $$

（最后一位取 0 或 8），即经典的**斐波那契递推**。可知 $g(n)=F_{n+1}$（取 $F_0=0,F_1=1$）。
因而

$$
f(k)=
\begin{cases}
1,&k=1\\[2mm]
g(k-2)=F_{k-1},&k\ge 2
\end{cases}
$$

最终答案只与**单个斐波那契数**有关。

相关算法：**快速倍增法求斐波那契数**（Fast Doubling）。
由于 $k\le 10^9$，必须用 $O(\log k)$ 的倍增算法在模 $998244353$ 下计算 $F_{k-1}$。

## 复杂度分析

* 每个测试用例通过快速倍增计算一次斐波那契数：时间复杂度 $O(\log k)$。
* 仅使用常数个整型变量：空间复杂度 $O(1)$。
* 在 $T\le 10^4$ 的总规模下可轻松通过。

## 代码实现

### Python

```python
import sys

MOD = 998244353

def calc_answer(k: int) -> int:
    if k == 1:
        return 1
    n = k - 1  # 需要计算的 F_{k-1}
    # 迭代版快速倍增：维护 (F(m), F(m+1))，按位推进
    a, b = 0, 1  # 分别是 F(0), F(1)
    for i in range(n.bit_length() - 1, -1, -1):
        # 先做“倍增”步骤：从 m 得到 2m
        two_b = (b << 1) % MOD
        term = (two_b - a) % MOD
        c = (a * term) % MOD               # F(2m)
        d = (a * a + b * b) % MOD          # F(2m+1)
        a, b = c, d
        # 若该位为 1，再前进一步：2m -> 2m+1
        if (n >> i) & 1:
            a, b = d % MOD, (c + d) % MOD
    return a % MOD

def main():
    data = list(map(int, sys.stdin.read().split()))
    t = data[0]
    idx = 1
    out = []
    for _ in range(t):
        k = data[idx]; idx += 1
        out.append(str(calc_answer(k)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    static final long MOD = 998244353L;

    static long calcAnswer(long k) {
        if (k == 1) return 1L;
        long n = k - 1;            // 需要的 F_{k-1}
        long a = 0L, b = 1L;       // 分别是 F(0), F(1)
        for (int i = 63 - Long.numberOfLeadingZeros(n); i >= 0; i--) {
            // 倍增：从 m 得到 2m
            long twoB = (2L * b) % MOD;
            long term = (twoB - a) % MOD; if (term < 0) term += MOD;
            long c = (a * term) % MOD;                 // F(2m)
            long d = ( (a * a) % MOD + (b * b) % MOD ) % MOD; // F(2m+1)
            a = c; b = d;
            // 若该位是 1，再从 2m 走到 2m+1
            if ( ((n >> i) & 1L) == 1L ) {
                long na = d % MOD;
                long nb = (c + d) % MOD;
                a = na; b = nb;
            }
        }
        return a % MOD;
    }

    // 主函数：仅负责输入输出
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < T; i++) {
            long k = Long.parseLong(br.readLine().trim());
            sb.append(calcAnswer(k)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const long long MOD = 998244353LL;

long long calc_answer(long long k){
    if(k == 1) return 1;
    long long n = k - 1;      // 需要 F_{k-1}
    long long a = 0, b = 1;   // F(0), F(1)
    for(int i = 63 - __builtin_clzll(n); i >= 0; --i){
        // 倍增：m -> 2m
        long long twoB = (2*b) % MOD;
        long long term = (twoB - a) % MOD; if(term < 0) term += MOD;
        long long c = (a * term) % MOD;                 // F(2m)
        long long d = ( (a*a)%MOD + (b*b)%MOD ) % MOD;  // F(2m+1)
        a = c; b = d;
        // 若该位为 1，再走一步
        if( (n >> i) & 1LL ){
            long long na = d % MOD;
            long long nb = (c + d) % MOD;
            a = na; b = nb;
        }
    }
    return a % MOD;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if(!(cin >> T)) return 0;
    while(T--){
        long long k; cin >> k;
        cout << calc_answer(k) << "\n";
    }
    return 0;
}
```