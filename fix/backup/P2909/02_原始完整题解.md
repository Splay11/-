## 思路与方法

### 1. 可行性分析  
- 每次操作：选取两个相邻字符，翻转后交换（“00”↔“11”，“01”↔“10”）。  
- 注意：操作前后“1 的个数”模 2 不变。  
- 因此只有当字符串中 1 的个数 $M$ 为偶数时，才有可能通过若干次操作变为全 0；否则无解，不计入和。

### 2. 单串最优操作数 $f(s)$  
- 若 $s$ 中有偶数个 1，记其位置（从左到右）为 $p_1<p_2<\cdots<p_M$。  
- 最优策略：将第 $2k-1$ 个 1 与第 $2k$ 个 1 配对消除。  
- 每对所需操作数恰为两者索引差：  
  $f(s)\;=\;\sum_{k=1}^{M/2}(p_{2k}-p_{2k-1})\,. $

### 3. 全局求和 + 组合计数  
- 要对所有长度为 $n$ 且“1 的个数为偶数”的字符串累加 $f(s)$，可用组合计数或插值法推导得到简洁公式：  
   $\sum_{s}f(s)$$=(n-1)2^{n-2}\quad(\bmod\;998244353).$

### 4. 快速幂计算  
- 因为 $n$ 最大可达 $10^9$，必须用二分法快速幂在 $O(\log n)$ 内计算 $2^{n-2}\bmod998244353$。


## 复杂度分析

- 取模快幂：$O(\log n)$ 次乘法。  
- 其余常数次运算。  
- **总体时间**：$O(\log n)$，**空间**：$O(1)$。


## 代码

### Python

```python
MOD = 998244353
def solve():
    n = int(input().strip())
    if n == 1:
        print(0)
        return
    # 结果 = (n-1) * 2^(n-2) % MOD
    ans = ( (n-1) % MOD ) * pow(2, n-2, MOD) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.util.*;

public class Main {
    static final int MOD = 998244353;
    // 快速幂：计算 a^e % MOD
    static long powMod(long a, long e) {
        long r = 1;
        while (e > 0) {
            if ((e & 1) == 1) {
                r = r * a % MOD;
            }
            a = a * a % MOD;
            e >>= 1;
        }
        return r;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        sc.close();
        if (n == 1) {
            System.out.println(0);
            return;
        }
        // 结果 = (n-1) * 2^(n-2) % MOD
        long ans = ((n - 1) % MOD) * powMod(2, n - 2) % MOD;
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;

// 快速幂：计算 a^e % MOD
long long powMod(long long a, long long e) {
    long long r = 1;
    while (e) {
        if (e & 1) {
            r = r * a % MOD;
        }
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    long long n;
    cin >> n;
    if (n == 1) {
        cout << 0;
        return 0;
    }
    // 结果 = (n-1) * 2^(n-2) % MOD
    long long ans = ((n - 1) % MOD) * powMod(2, n - 2) % MOD;
    cout << ans;
    return 0;
}
```