## 解题思路

先把题意转成更容易处理的形式。

一次压缩把一段长度为 $k\ (k\ge 2)$ 的同字符连续子串压成 $1$ 个新符号，所以：

* 原长度减少了 $k-1$
* 花费为 $a_k$

最终要求字符串长度恰好变成 $m$，也就是总共需要减少

$$
d=n-m
$$

个字符。

### 关键观察

只有“由相同字符组成的连续段”才能压缩，所以原串可以先拆成若干个极长连续段（也就是若干个 run）。

例如串 `0011100` 可拆成：

* `00`
* `111`
* `00`

压缩操作一定完全发生在某一个 run 内，不会跨 run。
因此问题变成：

* 对每个长度为 $L$ 的 run，求“在这个 run 里减少 $x$ 个字符的最小代价”
* 再把所有 run 的结果做一次分组背包，凑出总减少量 $d$

### 单个 run 的动态规划

设某个 run 长度为 $L$。

定义：

$$
f[i][j]
$$

表示考虑这个 run 的前 $i$ 个字符，恰好减少了 $j$ 个字符时的最小代价。

转移分两种：

1. 第 $i+1$ 个字符不参与压缩
   那么：

$$
f[i+1][j]=\min(f[i+1][j],f[i][j])
$$

2. 从第 $i+1$ 个字符开始，压缩一段长度为 $k$ 的子串，其中 $k\ge 2$ 且 $i+k\le L$
   这样会减少 $k-1$ 个字符，代价增加 $a_k$：

$$
f[i+k][j+k-1]=\min(f[i+k][j+k-1],f[i][j]+a_k)
$$

这样就能求出这个 run 内，减少 $0\sim L-1$ 个字符的最小代价。

### 所有 run 合并

设所有 run 分别求出了各自的最小代价数组 `costRun[x]`。

再做一次分组背包：

定义：

$$
dp[t]
$$

表示处理完前若干个 run，总共减少 $t$ 个字符的最小代价。

对每个 run 做转移即可。

最后看 $dp[d]$：

* 若无穷大，输出 $-1$
* 否则输出最小代价

### 相关算法

本题核心使用的是：

* 动态规划
* 分组背包
* 区间拆分后的逐段处理

---

## 复杂度分析

设字符串长度为 $n$。

### 时间复杂度

* 枚举每个 run，单个 run 的转移复杂度为 $O(L^3)$ 以内
* 所有 run 长度和为 $n$，总复杂度可记为 $O(n^3)$

在数据范围 $n\le 500$，且所有测试的 $n$ 总和不超过 $1000$ 时，完全可以通过。

### 空间复杂度

* 单个 run 的 DP 需要 $O(L^2)$
* 总背包数组需要 $O(n)$

所以总空间复杂度为：

$$
O(n^2)
$$

---

## 代码实现

### Python

```python
# 01串压缩
# 动态规划 + 分组背包

import sys


INF = 10 ** 18


# 计算一个长度为L的连续段中，减少x个字符的最小代价
def calc_run_cost(L, a):
    # f[i][j]：前i个字符，恰好减少j个字符的最小代价
    f = [[INF] * L for _ in range(L + 1)]
    f[0][0] = 0

    for i in range(L):
        for j in range(L):
            if f[i][j] == INF:
                continue

            # 不压缩当前位置
            if f[i + 1][j] > f[i][j]:
                f[i + 1][j] = f[i][j]

            # 从当前位置开始压缩一段长度k
            for k in range(2, L - i + 1):
                nj = j + (k - 1)
                cost = f[i][j] + a[k]
                if f[i + k][nj] > cost:
                    f[i + k][nj] = cost

    res = [INF] * L
    for j in range(L):
        res[j] = f[L][j]
    return res


# 求解单组测试
def solve_case(n, m, s, a):
    need = n - m

    # 拆分连续段
    runs = []
    cnt = 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)

    # 分组背包
    dp = [INF] * (need + 1)
    dp[0] = 0

    for L in runs:
        cost_run = calc_run_cost(L, a)
        ndp = [INF] * (need + 1)

        for old in range(need + 1):
            if dp[old] == INF:
                continue
            for dec in range(min(L - 1, need - old) + 1):
                if cost_run[dec] == INF:
                    continue
                val = dp[old] + cost_run[dec]
                if ndp[old + dec] > val:
                    ndp[old + dec] = val

        dp = ndp

    return -1 if dp[need] == INF else dp[need]


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        s = input().strip()
        arr = list(map(int, input().split()))

        # 方便按长度直接取代价，a[k]表示压缩长度k的代价
        a = [0] * (n + 1)
        for i in range(1, n + 1):
            a[i] = arr[i - 1]

        ans.append(str(solve_case(n, m, s, a)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static final long INF = (long) 4e18;

    // 计算一个长度为L的连续段中，减少x个字符的最小代价
    static long[] calcRunCost(int L, long[] a) {
        // f[i][j]：前i个字符，恰好减少j个字符的最小代价
        long[][] f = new long[L + 1][L];
        for (int i = 0; i <= L; i++) {
            for (int j = 0; j < L; j++) {
                f[i][j] = INF;
            }
        }
        f[0][0] = 0;

        for (int i = 0; i < L; i++) {
            for (int j = 0; j < L; j++) {
                if (f[i][j] == INF) {
                    continue;
                }

                // 不压缩当前位置
                if (f[i + 1][j] > f[i][j]) {
                    f[i + 1][j] = f[i][j];
                }

                // 从当前位置开始压缩长度为k的一段
                for (int k = 2; k <= L - i; k++) {
                    int nj = j + k - 1;
                    long cost = f[i][j] + a[k];
                    if (f[i + k][nj] > cost) {
                        f[i + k][nj] = cost;
                    }
                }
            }
        }

        long[] res = new long[L];
        for (int j = 0; j < L; j++) {
            res[j] = f[L][j];
        }
        return res;
    }

    // 求解单组测试
    static long solveCase(int n, int m, String s, long[] a) {
        int need = n - m;

        // 拆分连续段
        int[] runs = new int[n];
        int runCount = 0;
        int cnt = 1;
        for (int i = 1; i < n; i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                cnt++;
            } else {
                runs[runCount++] = cnt;
                cnt = 1;
            }
        }
        runs[runCount++] = cnt;

        // 分组背包
        long[] dp = new long[need + 1];
        for (int i = 0; i <= need; i++) {
            dp[i] = INF;
        }
        dp[0] = 0;

        for (int idx = 0; idx < runCount; idx++) {
            int L = runs[idx];
            long[] costRun = calcRunCost(L, a);
            long[] ndp = new long[need + 1];
            for (int i = 0; i <= need; i++) {
                ndp[i] = INF;
            }

            for (int old = 0; old <= need; old++) {
                if (dp[old] == INF) {
                    continue;
                }
                int maxDec = Math.min(L - 1, need - old);
                for (int dec = 0; dec <= maxDec; dec++) {
                    if (costRun[dec] == INF) {
                        continue;
                    }
                    long val = dp[old] + costRun[dec];
                    if (ndp[old + dec] > val) {
                        ndp[old + dec] = val;
                    }
                }
            }
            dp = ndp;
        }

        return dp[need] == INF ? -1 : dp[need];
    }

    public static void main(String[] args) throws Exception {
        FastReader fr = new FastReader();
        StringBuilder sb = new StringBuilder();

        int T = fr.nextInt();
        while (T-- > 0) {
            int n = fr.nextInt();
            int m = fr.nextInt();
            String s = fr.next();
            long[] a = new long[n + 1];
            for (int i = 1; i <= n; i++) {
                a[i] = fr.nextLong();
            }

            long ans = solveCase(n, m, s, a);
            sb.append(ans).append('\n');
        }

        System.out.print(sb.toString());
    }

    // 默认不用快读，这里用较常规的BufferedReader + StringTokenizer
    static class FastReader {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws IOException {
            while (st == null || !st.hasMoreElements()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }

        long nextLong() throws IOException {
            return Long.parseLong(next());
        }
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long INF = (long long)4e18;

// 计算一个长度为L的连续段中，减少x个字符的最小代价
vector<long long> calcRunCost(int L, const vector<long long>& a) {
    // f[i][j]：前i个字符，恰好减少j个字符的最小代价
    vector<vector<long long> > f(L + 1, vector<long long>(L, INF));
    f[0][0] = 0;

    for (int i = 0; i < L; i++) {
        for (int j = 0; j < L; j++) {
            if (f[i][j] == INF) continue;

            // 不压缩当前位置
            f[i + 1][j] = min(f[i + 1][j], f[i][j]);

            // 从当前位置开始压缩长度为k的一段
            for (int k = 2; k <= L - i; k++) {
                int nj = j + k - 1;
                f[i + k][nj] = min(f[i + k][nj], f[i][j] + a[k]);
            }
        }
    }

    vector<long long> res(L, INF);
    for (int j = 0; j < L; j++) {
        res[j] = f[L][j];
    }
    return res;
}

// 求解单组测试
long long solveCase(int n, int m, const string& s, const vector<long long>& a) {
    int need = n - m;

    // 拆分连续段
    vector<int> runs;
    int cnt = 1;
    for (int i = 1; i < n; i++) {
        if (s[i] == s[i - 1]) {
            cnt++;
        } else {
            runs.push_back(cnt);
            cnt = 1;
        }
    }
    runs.push_back(cnt);

    // 分组背包
    vector<long long> dp(need + 1, INF);
    dp[0] = 0;

    for (int L : runs) {
        vector<long long> costRun = calcRunCost(L, a);
        vector<long long> ndp(need + 1, INF);

        for (int old = 0; old <= need; old++) {
            if (dp[old] == INF) continue;
            int maxDec = min(L - 1, need - old);
            for (int dec = 0; dec <= maxDec; dec++) {
                if (costRun[dec] == INF) continue;
                ndp[old + dec] = min(ndp[old + dec], dp[old] + costRun[dec]);
            }
        }

        dp = ndp;
    }

    return dp[need] == INF ? -1 : dp[need];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, m;
        cin >> n >> m;
        string s;
        cin >> s;

        vector<long long> a(n + 1);
        for (int i = 1; i <= n; i++) {
            cin >> a[i];
        }

        cout << solveCase(n, m, s, a) << '\n';
    }

    return 0;
}
```