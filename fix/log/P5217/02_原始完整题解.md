## 解题思路

本题考查**排列的环分解**与**字符串最小周期**，答案是各环贡献的最小公倍数。

1. 一次操作把位置 $i$ 上的字符换成原串位置 $p_i$ 上的字符。反复操作等价于沿置换 $p$ 的函数图移动。
2. 将 $p$ 拆成若干互不相交的环。对长度为 $L$ 的环，环上字符形成一个长度为 $L$ 的圆串；操作一次相当于把圆串旋转一格。
3. 该环恢复原状的最小正旋转步数，等于圆串的最小周期 $d$：在整除 $L$ 的因子中，找最小的 $d$，使环上字符串由长度为 $d$ 的块重复 $L/d$ 次得到。若环上字符全相同，则 $d=1$。
4. 整串恢复当且仅当每个环都恢复，故总次数 $k$ 为所有环的 $d$ 的最小公倍数。输出 $k \bmod (10^9+7)$。注意 $k$ 可能远超 $64$ 位，需用高精度或质因数分解累乘取模。

常见假解：

- 直接对环长取 LCM，忽略环上字符串自身周期（如全相同字符时答案应为 $1$）；
- 只取最长环长度；
- 用 $32/64$ 位整数直接累乘 LCM 导致溢出；
- 把「已经不变」误判为 $0$ 次（题目要求最少正整数次数）。

## 复杂度分析

- 时间复杂度：$O(n\log n)$ 量级（遍历环；对每个环长 $L$ 检查约 $O(\sqrt L)$ 个因子并 $O(L)$ 验证，总和可接受）；取 LCM 时质因数分解或高精度另计。
- 空间复杂度：$O(n)$。

## 代码实现

### Python

```python
import math

MOD = 10**9 + 7


def cycle_period(chars: list[str]) -> int:
    # 环上字符串的最小正旋转周期
    m = len(chars)
    for d in range(1, m + 1):
        if m % d != 0:
            continue
        if all(chars[i] == chars[i % d] for i in range(m)):
            return d
    return m


def solve(n: int, u: str, p: list[int]) -> int:
    vis = [False] * n
    ans = 1
    for i in range(n):
        if vis[i]:
            continue
        cycle = []
        x = i
        while not vis[x]:
            vis[x] = True
            cycle.append(u[x])
            x = p[x]
        per = cycle_period(cycle)
        ans = ans // math.gcd(ans, per) * per  # 高精度 LCM
    return ans % MOD


def main() -> None:
    n = int(input())
    u = input().strip()
    p = [int(x) - 1 for x in input().split()]
    print(solve(n, u, p))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.math.BigInteger;
import java.util.*;

public class Main {
    static final int MOD = 1_000_000_007;

    static int cyclePeriod(String s) {
        int m = s.length();
        for (int d = 1; d <= m; d++) {
            if (m % d != 0) continue;
            boolean ok = true;
            for (int i = 0; i < m; i++) {
                if (s.charAt(i) != s.charAt(i % d)) {
                    ok = false;
                    break;
                }
            }
            if (ok) return d;
        }
        return m;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String u = br.readLine().trim();
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] p = new int[n];
        for (int i = 0; i < n; i++) p[i] = Integer.parseInt(st.nextToken()) - 1;

        boolean[] vis = new boolean[n];
        BigInteger ans = BigInteger.ONE;
        for (int i = 0; i < n; i++) {
            if (vis[i]) continue;
            StringBuilder cyc = new StringBuilder();
            int x = i;
            while (!vis[x]) {
                vis[x] = true;
                cyc.append(u.charAt(x));
                x = p[x];
            }
            BigInteger bp = BigInteger.valueOf(cyclePeriod(cyc.toString()));
            ans = ans.divide(ans.gcd(bp)).multiply(bp);
        }
        System.out.println(ans.mod(BigInteger.valueOf(MOD)));
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int cycle_period(const string& s) {
    int m = (int)s.size();
    for (int d = 1; d <= m; ++d) {
        if (m % d != 0) continue;
        bool ok = true;
        for (int i = 0; i < m; ++i) {
            if (s[i] != s[i % d]) { ok = false; break; }
        }
        if (ok) return d;
    }
    return m;
}

void factor_max(int x, map<int, int>& mx) {
    for (int p = 2; 1LL * p * p <= x; ++p) {
        if (x % p == 0) {
            int e = 0;
            while (x % p == 0) { x /= p; ++e; }
            mx[p] = max(mx[p], e);
        }
    }
    if (x > 1) mx[x] = max(mx[x], 1);
}

long long mod_pow(long long a, int e) {
    long long r = 1;
    while (e > 0) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    string u;
    cin >> u;
    vector<int> p(n);
    for (int i = 0; i < n; ++i) { cin >> p[i]; --p[i]; }

    vector<char> vis(n, false);
    map<int, int> mx;
    for (int i = 0; i < n; ++i) {
        if (vis[i]) continue;
        string cyc;
        int x = i;
        while (!vis[x]) {
            vis[x] = true;
            cyc.push_back(u[x]);
            x = p[x];
        }
        factor_max(cycle_period(cyc), mx);
    }
    long long ans = 1;
    for (map<int, int>::iterator it = mx.begin(); it != mx.end(); ++it) {
        ans = ans * mod_pow(it->first, it->second) % MOD;
    }
    cout << ans << '\n';
    return 0;
}
```