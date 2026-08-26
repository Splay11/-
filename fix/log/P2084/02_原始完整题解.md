## 解题思路

先设 $f[i][j]$ 表示 $1 \sim i$ 的所有排列中，逆序对个数恰好为 $j$ 的方案数。

这是一个经典的“逆序对计数”动态规划。

把数字 $i$ 插入到 $1 \sim i-1$ 的某个排列中：

* 如果插在最后面，新增逆序对是 $0$
* 如果插在倒数第二个位置，新增逆序对是 $1$
* ...
* 如果插在最前面，新增逆序对是 $i-1$

所以有转移：

$$
f[i][j] = \sum_{t=0}^{\min(j,i-1)} f[i-1][j-t]
$$

这个式子可以用前缀和优化到 $O(nk)$。

---

接下来处理条件 $a_1 < a_2$。

设：

* $A_j$：逆序对恰好为 $j$，且满足 $a_1 < a_2$ 的排列数
* $B_j$：逆序对恰好为 $j$，且满足 $a_1 > a_2$ 的排列数

显然：

$$
f[n][j] = A_j + B_j
$$

考虑把一个排列的前两个数交换：

* 若原来满足 $a_1 < a_2$，交换后变成 $a_1 > a_2$
* 并且逆序对数恰好增加 $1$

因为除了第 $1,2$ 个位置这一对之外，前两个数和后面所有数形成的逆序对总数不会变化。

所以有一一对应关系：

$$
B_j = A_{j-1}
$$

于是：


$A_j$ = $f[n][j]$ - $A_{j-1}$



初值：

$A_0 = 1$，因为逆序对为 $0$ 时只有升序排列 $1,2,\dots,n$，且一定满足 $a_1<a_2$

最后答案就是：

$$
\sum_{j=0}^{k} A_j
$$

---

核心算法：

1. 用动态规划求出 $f[n][0 \sim k]$
2. 再用递推式 $A_j=f[n][j]-A_{j-1}$ 求出每个逆序对数下满足 $a_1<a_2$ 的方案数
3. 累加得到答案

## 复杂度分析

求逆序对计数的动态规划使用前缀和优化后：

* 时间复杂度：$O(nk)$
* 空间复杂度：$O(k)$

由于 $n \le 200,\ k \le 200$，复杂度完全可以通过。

## 代码实现

### Python

```python
MOD = 10 ** 9 + 7

def solve(n, k):
    # dp[j] 表示当前长度下，逆序对恰好为 j 的排列数
    dp = [0] * (k + 1)
    dp[0] = 1

    # 经典逆序对 DP，使用前缀和优化
    for i in range(2, n + 1):
        ndp = [0] * (k + 1)
        prefix = 0
        for j in range(k + 1):
            prefix = (prefix + dp[j]) % MOD
            if j >= i:
                prefix = (prefix - dp[j - i]) % MOD
            ndp[j] = prefix
        dp = ndp

    # 计算 A[j]：逆序对恰好为 j 且 a1 < a2 的方案数
    ans = 0
    prev = 0  # A[j-1]
    for j in range(k + 1):
        cur = dp[j] if j == 0 else (dp[j] - prev) % MOD
        ans = (ans + cur) % MOD
        prev = cur

    return ans

def main():
    n, k = map(int, input().split())
    print(solve(n, k))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    static final int MOD = 1000000007;

    // 计算答案
    static int solve(int n, int k) {
        // dp[j] 表示当前长度下，逆序对恰好为 j 的排列数
        int[] dp = new int[k + 1];
        dp[0] = 1;

        // 经典逆序对 DP，使用前缀和优化
        for (int i = 2; i <= n; i++) {
            int[] ndp = new int[k + 1];
            long prefix = 0;
            for (int j = 0; j <= k; j++) {
                prefix += dp[j];
                if (j >= i) {
                    prefix -= dp[j - i];
                }
                prefix %= MOD;
                if (prefix < 0) {
                    prefix += MOD;
                }
                ndp[j] = (int) prefix;
            }
            dp = ndp;
        }

        // 计算 A[j]：逆序对恰好为 j 且 a1 < a2 的方案数
        long ans = 0;
        long prev = 0; // A[j-1]
        for (int j = 0; j <= k; j++) {
            long cur;
            if (j == 0) {
                cur = dp[j];
            } else {
                cur = (dp[j] - prev) % MOD;
                if (cur < 0) {
                    cur += MOD;
                }
            }
            ans = (ans + cur) % MOD;
            prev = cur;
        }

        return (int) ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();
        System.out.println(solve(n, k));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

// 计算答案
int solve(int n, int k) {
    // dp[j] 表示当前长度下，逆序对恰好为 j 的排列数
    vector<int> dp(k + 1, 0);
    dp[0] = 1;

    // 经典逆序对 DP，使用前缀和优化
    for (int i = 2; i <= n; i++) {
        vector<int> ndp(k + 1, 0);
        long long prefix = 0;
        for (int j = 0; j <= k; j++) {
            prefix += dp[j];
            if (j >= i) {
                prefix -= dp[j - i];
            }
            prefix %= MOD;
            if (prefix < 0) {
                prefix += MOD;
            }
            ndp[j] = (int)prefix;
        }
        dp = ndp;
    }

    // 计算 A[j]：逆序对恰好为 j 且 a1 < a2 的方案数
    long long ans = 0;
    long long prev = 0; // A[j-1]
    for (int j = 0; j <= k; j++) {
        long long cur;
        if (j == 0) {
            cur = dp[j];
        } else {
            cur = (dp[j] - prev) % MOD;
            if (cur < 0) {
                cur += MOD;
            }
        }
        ans = (ans + cur) % MOD;
        prev = cur;
    }

    return (int)ans;
}

int main() {
    int n, k;
    cin >> n >> k;
    cout << solve(n, k) << '\n';
    return 0;
}
```