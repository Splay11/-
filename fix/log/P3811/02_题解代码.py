## 解题思路

设数组为 $a_1,\dots,a_n$，对每个 $k(1\le k\le n)$ 要求所有长度为 $k$ 的子序列 $b$ 的最大值 $f(b)=\max(b)$ 之和，答案对 $998244353$ 取模。

关键观察（计数法）
将数组按非降序排序，记为 $A_1\le A_2\le \cdots\le A_n$。把每个长度为 $k$ 的子序列唯一地“归属”给其最大值在原序中的**最右位置** $i$。
当最大值归属在位置 $i$ 时，其余 $k-1$ 个元素只能从 $[1,\,i-1]$ 中任取（都不超过 $A_i$），共有

$$
\binom{i-1}{k-1}
$$

种选择。因此所有长度为 $k$ 的子序列的最大值之和为

$$
\text{ans}_k=\sum_{i=k}^{n} A_i \cdot \binom{i-1}{k-1}.
$$

（上述做法对相等元素同样成立，因为“最右位置”保证了划分唯一。）

实现要点

* 先对数组排序。
* 需要大量组合数，可用**杨辉三角（Pascal）**逐行递推：
  $\binom{i}{0}=\binom{i}{i}=1$，$\binom{i}{j}=\binom{i-1}{j-1}+\binom{i-1}{j}$（取模）。
  为节省内存，仅保留“上一行” `prev` 与“当前行” `cur`（空间 $O(n)$）。
* 在枚举位置 $i(1\le i\le n)$ 时，用 `prev[k-1]` 就是 $\binom{i-1}{k-1}$，将 $A_i$ 对所有 $k\le i$ 的贡献累加到答案数组中。

由于题目保证所有中间值在 32 位范围内，最终只需在模数下运算。

## 复杂度分析

* 时间复杂度：排序 $O(n\log n)$；组合数递推与累加总计 $O(n^2)$。当 $n\le 5\times10^3$ 时可行。
* 空间复杂度：仅保存两行组合数与答案数组，$O(n)$。

## 代码实现

### Python

```python
import sys

MOD = 998244353

# 计算所有 k 的答案，返回长度为 n 的列表
def solve_all(a):
    n = len(a)
    a.sort()  # 非降序
    ans = [0] * (n + 1)

    # prev[j] = C(i-1, j) 的一行表示，初始为 C(0, j)
    prev = [0] * (n + 1)
    prev[0] = 1

    for i in range(1, n + 1):
        ai = a[i - 1] % MOD
        # 对所有 k(1..i) 累加 A_i * C(i-1, k-1)
        for k in range(1, i + 1):
            ans[k] = (ans[k] + ai * prev[k - 1]) % MOD

        # 递推得到下一行组合数 C(i, j)
        cur = [0] * (n + 1)
        cur[0] = 1
        for j in range(1, i):
            cur[j] = (prev[j - 1] + prev[j]) % MOD
        cur[i] = 1
        prev = cur

    return ans[1:]  # 去掉下标0

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]
    res = solve_all(arr)
    print(" ".join(str(x) for x in res))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static final long MOD = 998244353L;

    // 计算所有 k 的答案，返回长度为 n 的 long[]
    static long[] solveAll(long[] a) {
        int n = a.length;
        Arrays.sort(a); // 非降序
        long[] ans = new long[n + 1];

        // prev[j] 表示 C(i-1, j)，初始为 C(0, j)
        long[] prev = new long[n + 1];
        prev[0] = 1;

        for (int i = 1; i <= n; i++) {
            long ai = a[i - 1] % MOD;
            // 累加贡献 A_i * C(i-1, k-1)
            for (int k = 1; k <= i; k++) {
                ans[k] = (ans[k] + ai * prev[k - 1]) % MOD;
            }
            // 递推到下一行组合数 C(i, j)
            long[] cur = new long[n + 1];
            cur[0] = 1;
            for (int j = 1; j < i; j++) {
                cur[j] = (prev[j - 1] + prev[j]) % MOD;
            }
            cur[i] = 1;
            prev = cur;
        }

        // 去掉下标0
        long[] ret = new long[n];
        for (int i = 1; i <= n; i++) ret[i - 1] = ans[i];
        return ret;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long[] a = new long[n];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) a[i] = Long.parseLong(st.nextToken());

        long[] res = solveAll(a);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < res.length; i++) {
            if (i > 0) sb.append(' ');
            sb.append(res[i]);
        }
        System.out.println(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const long long MOD = 998244353LL;

// 计算所有 k 的答案
vector<long long> solveAll(vector<long long> a) {
    int n = (int)a.size();
    sort(a.begin(), a.end());  // 非降序
    vector<long long> ans(n + 1, 0);

    // prev[j] = C(i-1, j)，初始为 C(0, j)
    vector<long long> prev(n + 1, 0);
    prev[0] = 1;

    for (int i = 1; i <= n; ++i) {
        long long ai = a[i - 1] % MOD;
        // 累加贡献 A_i * C(i-1, k-1)
        for (int k = 1; k <= i; ++k) {
            ans[k] = (ans[k] + ai * prev[k - 1]) % MOD;
        }
        // 递推到下一行组合数 C(i, j)
        vector<long long> cur(n + 1, 0);
        cur[0] = 1;
        for (int j = 1; j < i; ++j) {
            cur[j] = (prev[j - 1] + prev[j]) % MOD;
        }
        cur[i] = 1;
        prev.swap(cur);
    }

    ans.erase(ans.begin()); // 去掉下标0
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    vector<long long> res = solveAll(a);
    for (int i = 0; i < (int)res.size(); ++i) {
        if (i) cout << ' ';
        cout << res[i];
    }
    cout << '\n';
    return 0;
}
```