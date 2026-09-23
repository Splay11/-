# 配电箱最小联调

一句话总结：区间 DP 求连续段最小联调代价，单峰可整段直通，否则枚举切口并网。

算法标签：区间 DP、动态规划

算法难度：$6 / 10$

## 解题思路

把下标 $l\sim r$ 这一段全部联调的最小代价记为 $dp[l][r]$。长度为 $1$ 时已经接通，规定 $dp[i][i]=0$。

1. 整段直通只在该段单峰时合法，代价是 $(p_l+p_r)\times (r-l+1)$。单峰判定：从左先尽量非降，再尽量非升，若能走到右端则存在合法峰值位置。相邻相等允许，峰也不要求唯一。长度为 $2$ 的段一定单峰。
2. 中剖并网：枚举切点 $t$（$l\le t<r$），先各自最优联调左右两段，再付并网代价 $p_t\times p_{t+1}$。转移为
   $$dp[l][r]=\min_t\bigl(dp[l][t]+dp[t+1][r]+p_t\cdot p_{t+1}\bigr)$$
   若该段还是单峰，再和整段直通代价取 $\min$。
3. 按区间长度从小到大填表。长度为 $1$ 已知，长度为 $k$ 时左右子段更短，已经算完。答案是 $dp[1][n]$。
4. 常见假解：能直通就一定直通（样例 $1$ 说明切开更便宜）；把单峰理解成严格单峰或唯一峰；用 $32$ 位整数累加代价。

## 复杂度分析

- 时间复杂度：$O(n^3)$。$O(n^2)$ 个区间，每个区间枚举 $O(n)$ 个切点，单峰判定 $O(n)$，总次数仍是 $O(n^3)$。
- 空间复杂度：$O(n^2)$。存 $dp$ 表。

$n\le 200$，$p_i\le 100$。评测时限 $3$ 秒、内存 $512$ MB。

## 代码实现

### Python

```python
def is_unimodal(p, left, right):
    # 先尽量爬升，再尽量下降，能走到右端就是单峰
    i = left
    while i < right and p[i] <= p[i + 1]:
        i += 1
    while i < right and p[i] >= p[i + 1]:
        i += 1
    return i == right


def min_cost(p):
    n = len(p)
    inf = 10**18
    # dp[l][r]：把下标 l..r 这段全部联调的最小代价
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for left in range(0, n - length + 1):
            right = left + length - 1
            best = inf
            # 单峰时可以整段直通
            if is_unimodal(p, left, right):
                best = (p[left] + p[right]) * length
            # 枚举切点，先调好左右段再并网
            for t in range(left, right):
                cur = dp[left][t] + dp[t + 1][right] + p[t] * p[t + 1]
                if cur < best:
                    best = cur
            dp[left][right] = best
    return dp[0][n - 1]


def main():
    # 第一行 n，第二行 n 个额定功率
    n = int(input())
    p = list(map(int, input().split()))
    print(min_cost(p[:n]))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    static final long INF = 1L << 60;

    // 先尽量爬升，再尽量下降，能走到右端就是单峰
    static boolean isUnimodal(int[] p, int left, int right) {
        int i = left;
        while (i < right && p[i] <= p[i + 1]) {
            i++;
        }
        while (i < right && p[i] >= p[i + 1]) {
            i++;
        }
        return i == right;
    }

    // dp[l][r]：把下标 l..r 这段全部联调的最小代价
    static long minCost(int[] p) {
        int n = p.length;
        long[][] dp = new long[n][n];
        for (int length = 2; length <= n; length++) {
            for (int left = 0; left + length - 1 < n; left++) {
                int right = left + length - 1;
                long best = INF;
                // 单峰时可以整段直通
                if (isUnimodal(p, left, right)) {
                    best = (p[left] + p[right]) * 1L * length;
                }
                // 枚举切点，先调好左右段再并网
                for (int t = left; t < right; t++) {
                    long cur = dp[left][t] + dp[t + 1][right] + 1L * p[t] * p[t + 1];
                    if (cur < best) {
                        best = cur;
                    }
                }
                dp[left][right] = best;
            }
        }
        return dp[0][n - 1];
    }

    public static void main(String[] args) {
        // n 只有 200，Scanner 足够
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] p = new int[n];
        for (int i = 0; i < n; i++) {
            p[i] = sc.nextInt();
        }
        System.out.println(minCost(p));
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

const long long INF = (1LL << 60);

// 先尽量爬升，再尽量下降，能走到右端就是单峰
bool isUnimodal(const vector<int>& p, int left, int right) {
    int i = left;
    while (i < right && p[i] <= p[i + 1]) {
        i++;
    }
    while (i < right && p[i] >= p[i + 1]) {
        i++;
    }
    return i == right;
}

// dp[l][r]：把下标 l..r 这段全部联调的最小代价
long long minCost(const vector<int>& p) {
    int n = (int)p.size();
    vector<vector<long long> > dp(n, vector<long long>(n, 0));
    for (int length = 2; length <= n; length++) {
        for (int left = 0; left + length - 1 < n; left++) {
            int right = left + length - 1;
            long long best = INF;
            // 单峰时可以整段直通
            if (isUnimodal(p, left, right)) {
                best = (p[left] + p[right]) * 1LL * length;
            }
            // 枚举切点，先调好左右段再并网
            for (int t = left; t < right; t++) {
                long long cur = dp[left][t] + dp[t + 1][right] + 1LL * p[t] * p[t + 1];
                if (cur < best) {
                    best = cur;
                }
            }
            dp[left][right] = best;
        }
    }
    return dp[0][n - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n，第二行 n 个额定功率
    int n;
    cin >> n;
    vector<int> p(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i];
    }
    cout << minCost(p) << "\n";
    return 0;
}
```
