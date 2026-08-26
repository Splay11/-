# 题解

## 题面描述

给定两个整数 $n$ 和 $k$，要求构造一个长度为 $n$ 的数组 $[a_1,a_2,\dots,a_n]$，满足：  
1. 每个元素满足 $0 \le a_i < 2^k$；  
2. 数组所有元素的异或和 $\oplus_{i=1}^{n} a_i$ 小于等于所有元素的与和 $\&_{i=1}^{n} a_i$。  

要求统计满足条件的数组方案数，并对 $10^9+7$ 取模。
## 思路分析

由于数组中每个元素均为 $k$ 位二进制数，考虑按每个位（从最高位到最低位）分解问题。记  
- $X = \oplus_{i=1}^{n} a_i$ 为数组所有元素的异或和，  
- $Y = \&_{i=1}^{n} a_i$ 为数组所有元素的与和。  

**分析每一位的情况：**  
对于某个位 $b$（共 $k$ 位，其中 $b=k-1$ 为最高位），设所有 $n$ 个数在该位的取值为 $x_{1},x_{2},\dots,x_{n}\in\{0,1\}$，有：
- 若所有数该位均为 $1$，则 $Y_b=1$；否则 $Y_b=0$。  
- 异或值 $X_b$ 为这 $n$ 个数在该位的奇偶性（奇则 $1$，偶则 $0$）。

设在某一位上，若选择“全 1”则必然有 $Y_b=1$，而 $X_b$ 等于 $n$ 个 $1$ 的异或结果（当 $n$ 为偶数时为 $0$，为奇数时为 $1$）；若不全为 $1$（即至少存在一个 $0$），要求最终整体满足 $X\le Y$。由于比较二进制数从最高位开始，第一个出现不同时必须满足 $X_b=0$ 且 $Y_b=1$。  
因此对于最高位第一次出现 $X_b\ne Y_b$ 的位置，我们必须有：
- $Y_b=1$（即该位所有数均为 $1$），  
- 同时 $X_b=0$。  

对每个位如果没有“决胜位”（即之前所有位均相等），则当前位仍然处于“紧（tight）”状态。分状态讨论：  
- **紧状态（tight）：** 上一位均满足 $X=Y$。在当前位，若选择：
  - “全 1”：则该位变为 $(X_b,Y_b)=(\delta,1)$，其中 $\delta = n\mod 2$；  
    - 当 $n$ 为偶数时 $(0,1)$，满足 $0<1$，从紧状态转为“松弛状态（less）”；  
    - 当 $n$ 为奇数时 $(1,1)$，仍然相等，状态不变。  
  - “非全1”：此时该位 $Y_b=0$，要求若当前位处于紧状态，则不能出现 $(X_b,Y_b)=(1,0)$（否则最高不同位就为 $1>0$，违反 $X\le Y$）。因此在紧状态下，只允许“非全1且异或为 $0$”。  
- **松弛状态（less）：** 已经有高位满足 $X<Y$，则后续各位可以任意赋值，不受 $X\le Y$ 限制（只需满足本位的组合来自合法的赋值方式）。

**统计每个位的合法赋值数：**

对于某个位，对 $n$ 个数的该位赋值共有 $2^n$ 种可能，我们根据是否全 1 和奇偶性进行分类。记 $T=2^{n-1}$。  
- 若 $n$ 为偶数，则：
  - “全 1”：唯一方案，结果为 $(X_b,Y_b)=(0,1)$；  
  - “非全1且异或为 $0$”：方案数为 $T-1$（因为 $2^{n-1}$ 种偶数个 $1$ 中要排除全 1的情况）；  
  - “非全1且异或为 $1$”：方案数为 $T$。  
- 若 $n$ 为奇数，则：
  - “全 1”：唯一方案，结果为 $(X_b,Y_b)=(1,1)$；  
  - “非全1且异或为 $0$”：方案数为 $T$；  
  - “非全1且异或为 $1$”：方案数为 $T-1$（全 1不属于这一类）。

**状态转移：**

- 当 $n$ 为奇数时，由于“全 1”产生的 $(1,1)$与“非全1且异或为 $0$”产生的 $(0,0)$都使得 $X_b=Y_b$，故数组整体必须满足 $X=Y$。因此每个位有 $1+T$ 种选择，答案为 $(1+T)^k$。

- 当 $n$ 为偶数时，高位若选择“全 1”会使当前位出现 $(0,1)$，从紧状态转为松弛状态；在紧状态下只允许选择“非全1且异或为 $0$”。设从最高位开始连续有 $j$ 位处于紧状态后，第 $j+1$ 位选择“全 1”转为松弛状态（$0\le j\le k-1$），那么前 $j$ 位每位有 $(T-1)$ 种选择；转折位有 $1$ 种；之后每一位在松弛状态下可以任意选择三个合法方案，总数为 $2T$（即 $1+(T-1)+T=2T$）。此外还有一种情况是所有位都保持紧状态，即每位都选“非全1且异或为 $0$”，方案数为 $(T-1)^k$。因此答案为  
$\text{ans}$=$(T-1)^k$+$\sum_{j=0}^{k-1}(T-1)^j$,$(2T)^{k-1-j}.$
将求和化简可得最终公式  
$\text{ans}=\frac{(T-1)^k\cdot T+(2T)^k}{T+1}.$

其中 $T=2^{n-1}\mod (10^9+7)$。



## C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll MOD = 1000000007;

// 快速幂求模
ll modPow(ll base, ll exp, ll mod) {
    ll res = 1;
    base %= mod;
    while(exp) {
        if(exp & 1) res = res * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return res;
}

// 求模逆元，mod 为质数
ll modInv(ll a, ll mod) {
    return modPow(a, mod - 2, mod);
}

class Solution {
public:
    void solve() {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int n, k;
        cin >> n >> k;
        // T = 2^(n-1) mod MOD
        ll T = modPow(2, n - 1, MOD);
        ll ans = 0;
        if(n % 2 == 1) {
            // n 为奇数时答案为 (T + 1)^k mod MOD
            ans = modPow(T + 1, k, MOD);
        } else {
            // n 为偶数时答案为 ((T-1)^k * T + (2T)^k) / (T+1) mod MOD
            ll term1 = modPow((T + MOD - 1) % MOD, k, MOD); // (T-1)^k
            term1 = term1 * T % MOD;
            ll term2 = modPow(2 * T % MOD, k, MOD); // (2T)^k
            ll numerator = (term1 + term2) % MOD;
            ll invDenom = modInv((T + 1) % MOD, MOD);
            ans = numerator * invDenom % MOD;
        }
        cout << ans << "\n";
    }
};

int main(){
    Solution sol;
    sol.solve();
    return 0;
}
```
## Python 

```python
MOD = 10**9 + 7

# 快速幂求模
def mod_pow(base: int, exp: int, mod: int) -> int:
    res = 1
    base %= mod
    while exp:
        if exp & 1:
            res = res * base % mod
        base = base * base % mod
        exp //=  2
    return res

# 求模逆元，mod 为质数时使用快速幂
def mod_inv(a: int, mod: int) -> int:
    return mod_pow(a, mod - 2, mod)

class Solution:
    def solve(self):
        import sys
        input_data = sys.stdin.read().split()
        n = int(input_data[0])
        k = int(input_data[1])
        # T = 2^(n-1) mod MOD
        T = mod_pow(2, n - 1, MOD)
        if n % 2 == 1:
            # 当 n 为奇数时，答案为 (T + 1)^k mod MOD
            ans = mod_pow(T + 1, k, MOD)
        else:
            # 当 n 为偶数时，答案为 ((T - 1)^k * T + (2T)^k) / (T + 1) mod MOD
            term1 = mod_pow((T - 1) % MOD, k, MOD)  # (T-1)^k mod MOD
            term1 = term1 * T % MOD
            term2 = mod_pow((2 * T) % MOD, k, MOD)    # (2T)^k mod MOD
            numerator = (term1 + term2) % MOD
            inv_denom = mod_inv(T + 1, MOD)
            ans = numerator * inv_denom % MOD
        sys.stdout.write(str(ans))
        
if __name__ == "__main__":
    sol = Solution()
    sol.solve()
```
## Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1000000007;
    
    // 快速幂求模
    static long modPow(long base, long exp, long mod) {
        long res = 1;
        base %= mod;
        while(exp > 0) {
            if((exp & 1) == 1)
                res = res * base % mod;
            base = base * base % mod;
            exp >>= 1;
        }
        return res;
    }
    
    // 求模逆元，利用 Fermat 小定理（mod 为质数）
    static long modInv(long a, long mod) {
        return modPow(a, mod - 2, mod);
    }
    
    static class Solution {
        public void solve() throws IOException {
            BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
            String[] parts = in.readLine().split(" ");
            int n = Integer.parseInt(parts[0]);
            int k = Integer.parseInt(parts[1]);
            // T = 2^(n-1) mod MOD
            long T = modPow(2, n - 1, MOD);
            long ans;
            if(n % 2 == 1) {
                // n 为奇数时答案为 (T + 1)^k mod MOD
                ans = modPow(T + 1, k, MOD);
            } else {
                // n 为偶数时答案为 ((T-1)^k * T + (2T)^k) / (T+1) mod MOD
                long term1 = modPow((T - 1 + MOD) % MOD, k, MOD); // (T-1)^k mod MOD
                term1 = term1 * T % MOD;
                long term2 = modPow(2 * T % MOD, k, MOD);           // (2T)^k mod MOD
                long numerator = (term1 + term2) % MOD;
                long invDenom = modInv((T + 1) % MOD, MOD);
                ans = numerator * invDenom % MOD;
            }
            System.out.println(ans);
        }
    }
    
    public static void main(String[] args) throws IOException {
        new Solution().solve();
    }
}
```