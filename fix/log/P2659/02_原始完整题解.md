### 题面描述

小红和小紫在一个一维坐标系上玩捉迷藏，坐标范围为$[1, r]$。初始时，小红位于$x$，小紫位于$y$。每次移动，小红可以选择向左或向右移动不超过$a$个距离，小紫可以选择向左或向右移动不超过$b$个距离。求经过$t$秒后，小红和小紫位于同一个位置的概率。答案需要对$10^9+7$取模。

### 思路

我们使用动态规划结合二维差分优化来解决这个问题。定义状态 `dp[t][i][j]` 表示经过 `t` 秒后，小红位于 `i`，小紫位于 `j` 的概率。通过二维差分数组记录每一步的移动概率更新，利用前缀和还原状态，最终累加所有 `dp[t][i][i]` 得到两人位于同一位置的概率。整个过程通过模运算和逆元计算确保结果的正确性，时间复杂度为$O(t * n^2)$，空间复杂度为$O(n^2)$。

1. **状态表示**：我们可以用动态规划来解决这个问题。定义$dp[t][i][j]$表示经过$t$秒后，小红位于$i$，小紫位于$j$的概率。

2. **状态转移**：对于每一秒，小红和小紫的移动是独立的。因此，我们可以分别计算小红和小紫的移动概率，然后相乘得到新的状态概率。

3. **二维差分优化**：为了加速状态转移，我们使用二维差分数组来记录每个状态的更新。通过差分数组，我们可以在$O(1)$时间内对一个矩形区域进行加减操作，最后通过前缀和还原出实际的值。

4. **边界条件**：初始状态$dp[0][x][y] = 1$，其余状态为0。

5. **概率计算**：对于每个位置$i$和$j$，计算小红和小紫在下一步可能到达的位置，并更新差分数组。

6. **前缀和还原**：对差分数组进行前缀和计算，得到$dp[time + 1][i][j]$。

7. **最终结果**：经过$t$秒后，所有$dp[t][i][i]$的和即为所求概率。

8. **模运算**：由于答案需要对$10^9+7$取模，我们需要在每一步计算中进行模运算，并使用费马小定理来计算概率的逆元。

## cpp
```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

// 计算逆元的函数，使用费马小定理
int inv(int a, int mod) {
    int res = 1;
    int b = mod - 2;
    while (b > 0) {
        if (b & 1) res = (long long)res * a % mod;
        a = (long long)a * a % mod;
        b >>= 1;
    }
    return res;
}

int main() {
    int l, r, x, y, a, b, t;
    cin >> l >> r >> x >> y >> a >> b >> t;

    // 计算坐标范围的长度
    int n = r - l + 1;

    // 定义动态规划数组，dp[i][j] 表示小红在 i，小紫在 j 的概率
    vector<vector<int>> dp(n, vector<int>(n, 0));
    dp[x - l][y - l] = 1; // 初始状态

    // 动态规划过程
    for (int time = 0; time < t; ++time) {
        // 定义差分数组，用于记录概率更新
        vector<vector<int>> diff(n + 2, vector<int>(n + 2, 0));

        // 遍历所有可能的位置
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dp[i][j] == 0) continue; // 如果当前状态概率为 0，跳过

                // 小红移动的范围
                int p = i + l;
                int left_p = max(l, p - a);
                int right_p = min(r, p + a);
                int cnt_p = right_p - left_p + 1; // 可移动的位置数
                int inv_p = inv(cnt_p, MOD); // 计算逆元

                // 小紫移动的范围
                int q = j + l;
                int left_q = max(l, q - b);
                int right_q = min(r, q + b);
                int cnt_q = right_q - left_q + 1; // 可移动的位置数
                int inv_q = inv(cnt_q, MOD); // 计算逆元

                // 计算移动后的概率
                int prob = (long long)dp[i][j] * inv_p % MOD * inv_q % MOD;

                // 更新差分数组
                int ni_min = left_p - l;
                int ni_max = right_p - l;
                int nj_min = left_q - l;
                int nj_max = right_q - l;

                diff[ni_min][nj_min] = (diff[ni_min][nj_min] + prob) % MOD;
                diff[ni_min][nj_max + 1] = (diff[ni_min][nj_max + 1] - prob + MOD) % MOD;
                diff[ni_max + 1][nj_min] = (diff[ni_max + 1][nj_min] - prob + MOD) % MOD;
                diff[ni_max + 1][nj_max + 1] = (diff[ni_max + 1][nj_max + 1] + prob) % MOD;
            }
        }

        // 通过前缀和还原 dp 数组
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (i > 0) diff[i][j] = (diff[i][j] + diff[i - 1][j]) % MOD;
                if (j > 0) diff[i][j] = (diff[i][j] + diff[i][j - 1]) % MOD;
                if (i > 0 && j > 0) diff[i][j] = (diff[i][j] - diff[i - 1][j - 1] + MOD) % MOD;
                dp[i][j] = diff[i][j];
            }
        }
    }

    // 计算结果：所有 dp[i][i] 的和
    int result = 0;
    for (int i = 0; i < n; ++i) {
        result = (result + dp[i][i]) % MOD;
    }

    cout << result << endl;
    return 0;
}
```
## python
```python
MOD = 10**9 + 7

# 计算逆元的函数，使用费马小定理
def inv(a, mod):
    return pow(a, mod - 2, mod)

# 输入数据
l, r, x, y, a, b, t = map(int, input().split())

# 计算坐标范围的长度
n = r - l + 1

# 定义动态规划数组，dp[i][j] 表示小红在 i，小紫在 j 的概率
dp = [[0] * n for _ in range(n)]
dp[x - l][y - l] = 1  # 初始状态

# 动态规划过程
for _ in range(t):
    # 定义差分数组，用于记录概率更新
    diff = [[0] * (n + 2) for _ in range(n + 2)]

    # 遍历所有可能的位置
    for i in range(n):
        for j in range(n):
            if dp[i][j] == 0:
                continue  # 如果当前状态概率为 0，跳过

            # 小红移动的范围
            p = i + l
            left_p = max(l, p - a)
            right_p = min(r, p + a)
            cnt_p = right_p - left_p + 1  # 可移动的位置数
            inv_p = inv(cnt_p, MOD)  # 计算逆元

            # 小紫移动的范围
            q = j + l
            left_q = max(l, q - b)
            right_q = min(r, q + b)
            cnt_q = right_q - left_q + 1  # 可移动的位置数
            inv_q = inv(cnt_q, MOD)  # 计算逆元

            # 计算移动后的概率
            prob = dp[i][j] * inv_p % MOD * inv_q % MOD

            # 更新差分数组
            ni_min = left_p - l
            ni_max = right_p - l
            nj_min = left_q - l
            nj_max = right_q - l

            diff[ni_min][nj_min] = (diff[ni_min][nj_min] + prob) % MOD
            diff[ni_min][nj_max + 1] = (diff[ni_min][nj_max + 1] - prob) % MOD
            diff[ni_max + 1][nj_min] = (diff[ni_max + 1][nj_min] - prob) % MOD
            diff[ni_max + 1][nj_max + 1] = (diff[ni_max + 1][nj_max + 1] + prob) % MOD

    # 通过前缀和还原 dp 数组
    for i in range(n):
        for j in range(n):
            if i > 0:
                diff[i][j] = (diff[i][j] + diff[i - 1][j]) % MOD
            if j > 0:
                diff[i][j] = (diff[i][j] + diff[i][j - 1]) % MOD
            if i > 0 and j > 0:
                diff[i][j] = (diff[i][j] - diff[i - 1][j - 1]) % MOD
            dp[i][j] = diff[i][j]

# 计算结果：所有 dp[i][i] 的和
result = 0
for i in range(n):
    result = (result + dp[i][i]) % MOD

print(result)
```
## java
```java
import java.util.Scanner;

public class Main {
    static final int MOD = 1000000007;

    // 计算逆元的函数，使用费马小定理
    static int inv(int a, int mod) {
        int res = 1;
        int b = mod - 2;
        while (b > 0) {
            if ((b & 1) == 1) res = (int)((long)res * a % mod);
            a = (int)((long)a * a % mod);
            b >>= 1;
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int l = sc.nextInt();
        int r = sc.nextInt();
        int x = sc.nextInt();
        int y = sc.nextInt();
        int a = sc.nextInt();
        int b = sc.nextInt();
        int t = sc.nextInt();

        // 计算坐标范围的长度
        int n = r - l + 1;

        // 定义动态规划数组，dp[i][j] 表示小红在 i，小紫在 j 的概率
        int[][] dp = new int[n][n];
        dp[x - l][y - l] = 1; // 初始状态

        // 动态规划过程
        for (int time = 0; time < t; time++) {
            // 定义差分数组，用于记录概率更新
            int[][] diff = new int[n + 2][n + 2];

            // 遍历所有可能的位置
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (dp[i][j] == 0) continue; // 如果当前状态概率为 0，跳过

                    // 小红移动的范围
                    int p = i + l;
                    int left_p = Math.max(l, p - a);
                    int right_p = Math.min(r, p + a);
                    int cnt_p = right_p - left_p + 1; // 可移动的位置数
                    int inv_p = inv(cnt_p, MOD); // 计算逆元

                    // 小紫移动的范围
                    int q = j + l;
                    int left_q = Math.max(l, q - b);
                    int right_q = Math.min(r, q + b);
                    int cnt_q = right_q - left_q + 1; // 可移动的位置数
                    int inv_q = inv(cnt_q, MOD); // 计算逆元

                    // 计算移动后的概率
                    int prob = (int)((long)dp[i][j] * inv_p % MOD * inv_q % MOD);

                    // 更新差分数组
                    int ni_min = left_p - l;
                    int ni_max = right_p - l;
                    int nj_min = left_q - l;
                    int nj_max = right_q - l;

                    diff[ni_min][nj_min] = (diff[ni_min][nj_min] + prob) % MOD;
                    diff[ni_min][nj_max + 1] = (diff[ni_min][nj_max + 1] - prob + MOD) % MOD;
                    diff[ni_max + 1][nj_min] = (diff[ni_max + 1][nj_min] - prob + MOD) % MOD;
                    diff[ni_max + 1][nj_max + 1] = (diff[ni_max + 1][nj_max + 1] + prob) % MOD;
                }
            }

            // 通过前缀和还原 dp 数组
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (i > 0) diff[i][j] = (diff[i][j] + diff[i - 1][j]) % MOD;
                    if (j > 0) diff[i][j] = (diff[i][j] + diff[i][j - 1]) % MOD;
                    if (i > 0 && j > 0) diff[i][j] = (diff[i][j] - diff[i - 1][j - 1] + MOD) % MOD;
                    dp[i][j] = diff[i][j];
                }
            }
        }

        // 计算结果：所有 dp[i][i] 的和
        int result = 0;
        for (int i = 0; i < n; i++) {
            result = (result + dp[i][i]) % MOD;
        }

        System.out.println(result);
    }
}
```