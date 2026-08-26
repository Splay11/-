# 题解

## 题面描述

给定一个长度为 $n$ 的序列 $a$，要求将 $a$ 恰好划分为 $m$ 个非空的连续区间。对于每个区间求和得到一个新序列 $b$（长度恰好为 $m$），目标是最大化如下式子：

$
b_1 + b_2 \times 2 + b_3 + b_4 \times 2 + \cdots
$

也就是说，$b$ 中奇数位置的数字按原值相加，而偶数位置的数字需要乘以 $2$后再加。输入数据有多组，每组数据给出 $n$、$m$ 以及序列 $a$。

---

## 思路

将问题转化为动态规划（DP）的求解。令 $prefix[i]$ 为序列 $a$ 的前 $i$ 个数字之和。考虑状态 $dp[i][j]$ 表示将前 $i$ 个数字划分成 $j$ 个段后的最优答案，其中第 $j$ 段的权值取决于 $j$ 是奇数还是偶数（权值分别为 $1$ 或 $2$）。

设第 $j$ 段的权值为 $w_j$，则划分时如果最后一段区间为 $[l+1,i]$，区间和为 $prefix[i] - prefix[l]$，状态转移方程为：

$dp[i][j]$ = $\max_{l=j-1}^{i-1}$ $\Big\{ dp[l][j-1]$ + $w_j \times (prefix[i] - prefix[l])$ $\Big\}$

化简后可以写成：

$dp[i][j]$ = $w_j \times prefix[i]$ + $\max_{l=j-1}^{i-1}$ $\Big\{ dp[l][j-1]$ - $w_j \times prefix[l] \Big\}$

这样，在固定 $j$ 时，我们可以在遍历 $i$ 时维护一个当前的最大值，优化状态转移的求解复杂度。

由于题目中所有测试数据中 $n$ 的总和不超过 $3000$，使用 $O(n \times m)$ 的算法是可行的。

## C++ 

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>
using namespace std;

typedef long long ll;
const ll NEG_INF = -0x3f3f3f3f3f3f3f3fLL;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while(T--){
        int n, m;
        cin >> n >> m;
        vector<ll> a(n+1), prefix(n+1, 0);
        for(int i = 1; i <= n; i++){
            cin >> a[i];
            prefix[i] = prefix[i-1] + a[i]; // 计算前缀和
        }
        // dp[i][j] 表示将前 i 个数字划分成 j 段的最大答案
        vector<vector<ll>> dp(n+1, vector<ll>(m+1, NEG_INF));
        dp[0][0] = 0;
        
        // 枚举段数 j，从 1 到 m
        for(int j = 1; j <= m; j++){
            // 权值：奇数段权值为 1，偶数段权值为 2
            ll w = (j % 2 == 1 ? 1 : 2);
            // max_val 用于维护 max_{l=j-1}^{i-1} (dp[l][j-1] - w * prefix[l])
            ll max_val = NEG_INF;
            // 枚举 i，从 j 到 n（保证至少有 j 个数字）
            for(int i = j; i <= n; i++){
                // 先更新 max_val，候选分界点 l = i-1
                // 当 i == j 时，l 必须为 j-1
                if(i-1 >= j-1){
                    max_val = max(max_val, dp[i-1][j-1] - w * prefix[i-1]);
                }
                // 状态转移：最后一段为 [l+1, i]
                dp[i][j] = w * prefix[i] + max_val;
            }
        }
        cout << dp[n][m] << "\n";
    }
    return 0;
}
```
## Python 

```python
import sys

def main():
    import sys
    sys.setrecursionlimit(10000)
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        a = [0] + list(map(int, input().split()))
        prefix = [0]*(n+1)
        # 计算前缀和
        for i in range(1, n+1):
            prefix[i] = prefix[i-1] + a[i]
        NEG_INF = -10**18
        # dp[i][j] 表示将前 i 个数字划分成 j 段的最大答案
        dp = [[NEG_INF]*(m+1) for _ in range(n+1)]
        dp[0][0] = 0
        # 枚举段数 j 从 1 到 m
        for j in range(1, m+1):
            # 权值：奇数段权值为 1，偶数段为 2
            w = 1 if j % 2 == 1 else 2
            max_val = NEG_INF
            # 枚举 i 从 j 到 n
            for i in range(j, n+1):
                # 更新 max_val，候选分界点 l = i-1
                if i-1 >= j-1:
                    max_val = max(max_val, dp[i-1][j-1] - w * prefix[i-1])
                # 状态转移
                dp[i][j] = w * prefix[i] + max_val
        print(dp[n][m])
        
if __name__ == "__main__":
    main()
```
## Java

```java
import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 提高输入效率
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        while(T-- > 0) {
            String[] line = br.readLine().trim().split(" ");
            int n = Integer.parseInt(line[0]);
            int m = Integer.parseInt(line[1]);
            String[] arr = br.readLine().trim().split(" ");
            // 数组下标从 1 开始
            long[] a = new long[n+1];
            long[] prefix = new long[n+1];
            for(int i = 1; i <= n; i++){
                a[i] = Long.parseLong(arr[i-1]);
                prefix[i] = prefix[i-1] + a[i]; // 计算前缀和
            }
            long NEG_INF = Long.MIN_VALUE / 2;
            // dp[i][j] 表示将前 i 个数字划分成 j 段的最大答案
            long[][] dp = new long[n+1][m+1];
            for(int i = 0; i <= n; i++){
                Arrays.fill(dp[i], NEG_INF);
            }
            dp[0][0] = 0;
            // 枚举段数 j 从 1 到 m
            for(int j = 1; j <= m; j++){
                // 权值：奇数段权值为 1，偶数段为 2
                long w = (j % 2 == 1 ? 1 : 2);
                long maxVal = NEG_INF;
                // 枚举 i 从 j 到 n（保证至少有 j 个数字）
                for(int i = j; i <= n; i++){
                    // 更新 maxVal，候选分界点 l = i-1
                    if(i - 1 >= j - 1){
                        maxVal = Math.max(maxVal, dp[i-1][j-1] - w * prefix[i-1]);
                    }
                    // 状态转移
                    dp[i][j] = w * prefix[i] + maxVal;
                }
            }
            System.out.println(dp[n][m]);
        }
    }
}
```