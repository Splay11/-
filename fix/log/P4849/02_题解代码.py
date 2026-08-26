## 解题思路

设相邻差分为：

$d_i = v_{i+1} - v_i$

对于数组中的内部位置 $i$，要满足 $v_i$ 是波峰或波谷，即：

$(v_{i-1} \ge v_i 且 v_{i+1} \ge v_i)$ 或 $(v_{i-1} \le v_i 且 v_{i+1} \le v_i)$

等价于相邻两个差分方向相反或至少有一个为 $0$：

$d_{i-1} \times d_i \le 0$

所以，一个长度至少为 $3$ 的子数组是好的，当且仅当它对应的差分区间中，任意相邻两个差分都满足乘积 $\le 0$。

问题转化为：

在差分数组中，找到所有满足相邻乘积 $\le 0$ 的连续段。假设某个最长合法差分段长度为 $s$，那么它内部任意长度至少为 $2$ 的差分子段都对应一个好的原数组子数组。

若差分子段长度为 $q$，对应原子数组长度为 $q+1$，贡献的波峰/波谷数量为：

$q - 1$

因此该最长合法差分段的总贡献为：

$\sum_{q=2}^{s} (s-q+1)(q-1)$

化简得到：

$\frac{s(s-1)(s+1)}{6}$

遍历差分数组，维护当前最长合法差分段长度 $s$，遇到不合法位置时结算即可。

长度为 $1$ 或 $2$ 的原数组子数组贡献为 $0$，不影响答案。

## 复杂度分析

对于每组测试数据，只需要遍历一遍数组。

时间复杂度：$O(m)$

空间复杂度：$O(1)$，除输入数组外只使用常数额外空间。

由于所有测试数据的 $m$ 之和不超过 $200000$，该复杂度可以通过。

## 代码实现

### Python

```python
MOD = 10 ** 9 + 7


def calc(s):
    # 长度为 s 的合法差分段贡献为 s * (s - 1) * (s + 1) / 6
    return s * (s - 1) * (s + 1) // 6


def solve(m, v):
    if m < 3:
        return 0

    ans = 0

    # 当前合法差分段长度，至少包含第一个差分
    cur = 1

    for i in range(1, m - 1):
        d1 = v[i] - v[i - 1]
        d2 = v[i + 1] - v[i]

        # 相邻差分乘积 <= 0，说明当前位置可以作为波峰或波谷
        if d1 * d2 <= 0:
            cur += 1
        else:
            # 当前合法差分段结束，结算贡献
            ans = (ans + calc(cur)) % MOD
            cur = 1

    # 结算最后一段
    ans = (ans + calc(cur)) % MOD
    return ans


def main():
    import sys
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    res = []

    for _ in range(t):
        m = data[idx]
        idx += 1
        v = data[idx:idx + m]
        idx += m
        res.append(str(solve(m, v)))

    print("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    static final long MOD = 1000000007L;

    static long calc(long s) {
        // 长度为 s 的合法差分段贡献为 s * (s - 1) * (s + 1) / 6
        return s * (s - 1) * (s + 1) / 6;
    }

    static long solve(int m, long[] v) {
        if (m < 3) {
            return 0;
        }

        long ans = 0;
        long cur = 1; // 当前合法差分段长度

        for (int i = 1; i < m - 1; i++) {
            long d1 = v[i] - v[i - 1];
            long d2 = v[i + 1] - v[i];

            // 相邻差分乘积 <= 0，说明当前位置满足波峰或波谷条件
            if (d1 * d2 <= 0) {
                cur++;
            } else {
                // 当前合法差分段结束，结算贡献
                ans = (ans + calc(cur)) % MOD;
                cur = 1;
            }
        }

        // 结算最后一段
        ans = (ans + calc(cur)) % MOD;
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int m = sc.nextInt();
            long[] v = new long[m];

            for (int i = 0; i < m; i++) {
                v[i] = sc.nextLong();
            }

            sb.append(solve(m, v)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

long long calc(long long s) {
    // 长度为 s 的合法差分段贡献为 s * (s - 1) * (s + 1) / 6
    return s * (s - 1) * (s + 1) / 6;
}

long long solve(int m, vector<long long>& v) {
    if (m < 3) {
        return 0;
    }

    long long ans = 0;
    long long cur = 1; // 当前合法差分段长度

    for (int i = 1; i < m - 1; i++) {
        long long d1 = v[i] - v[i - 1];
        long long d2 = v[i + 1] - v[i];

        // 相邻差分乘积 <= 0，说明当前位置满足波峰或波谷条件
        if (d1 * d2 <= 0) {
            cur++;
        } else {
            // 当前合法差分段结束，结算贡献
            ans = (ans + calc(cur)) % MOD;
            cur = 1;
        }
    }

    // 结算最后一段
    ans = (ans + calc(cur)) % MOD;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int m;
        cin >> m;

        vector<long long> v(m);
        for (int i = 0; i < m; i++) {
            cin >> v[i];
        }

        cout << solve(m, v) << '\n';
    }

    return 0;
}
```