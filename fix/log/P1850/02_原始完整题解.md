## 题解

`前缀和优化DP`

对于这种计数类问题，而且还需要取模的情况下，往 DP 方面想准没错了。



### 朴素DP

定义 $dp[i][j][k]$ 为，前 $i$ 个数的异或和为 $k$ (其中 $k \le 2 \times m $) ，并且最后一个数为 $j$ 的方案数是多少

**状态转移**：$dp[i][j][k]$ = $\sum_{p = 0}^{j}dp[i - 1][p][k \oplus p]$，其中 $p \le j$ 

**复杂度计算**：时间复杂为状态量 * 转移，总复杂度为 $O(n m ^ 3)$，这样显然会 T

### 前缀和优化

考虑当前的 $j$ 可以由上一个状态中所有的 $p \le j$ 转移而来，那我们可以预处理出

$\sum_{p = 0}^{j}dp[i - 1][p][k \oplus p]$，这一段前缀和，将其中转移的复杂度由 $O(m)$ 优化到 $O(1)$

这样的复杂度变成了 $O(nm^2)$，可以接受。





## AC代码

- Cpp

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int mod = 1e9 + 7;
const int N = 310;

// dp[i][j][k]: 前i个数,异或和为k,最后一个数为j的方案数
int dp[N][N][N << 1]; 
// s[j][k]: dp[i-1][0~j][k]的前缀和
int s[N][N << 1];  

int main() {
    int n, m;
    cin >> n >> m;

    // 初始化:只有一种方案,即什么都不选
    dp[0][0][0] = 1;

    for (int i = 1; i <= n; i++) {
        // 计算前缀和
        for (int j = 0; j <= m; j++) {
            for (int k = 0; k <= m + m; k++) {
                s[j][k] = dp[i - 1][j][k];
                if (j) {
                    s[j][k] += s[j - 1][k];
                    s[j][k] %= mod;
                }
            }
        }
        // 状态转移
        for (int j = 0; j <= m; j++) {
            for (int k = 0; k <= m + m && (k ^ j) <= 2 * m; k++) {
                dp[i][j][k] = s[j][k ^ j];
            }
        }
    }

    // 计算最终结果
    int res = 0;
    for (int j = 0; j <= m; ++j)
        res = (res + dp[n][j][m]) % mod;

    cout << res << "\n";

    return 0;
}
```

- Java

  ```java
  import java.util.Scanner;
  
  public class Main {
      static final int mod = 1000000007;
      static final int N = 310;
  
      // dp[i][j][k]: 前i个数,异或和为k,最后一个数为j的方案数
      static int[][][] dp = new int[N][N][N << 1];
      // s[j][k]: dp[i-1][0~j][k]的前缀和
      static int[][] s = new int[N][N << 1];
  
      public static void main(String[] args) {
          Scanner scanner = new Scanner(System.in);
          int n = scanner.nextInt();
          int m = scanner.nextInt();
  
          // 初始化:只有一种方案,即什么都不选
          dp[0][0][0] = 1;
  
          for (int i = 1; i <= n; i++) {
              // 计算前缀和
              for (int j = 0; j <= m; j++) {
                  for (int k = 0; k <= m + m; k++) {
                      s[j][k] = dp[i - 1][j][k];
                      if (j > 0) {
                          s[j][k] = (s[j][k] + s[j - 1][k]) % mod;
                      }
                  }
              }
              // 状态转移
              for (int j = 0; j <= m; j++) {
                  for (int k = 0; k <= m + m && (k ^ j) <= 2 * m; k++) {
                      dp[i][j][k] = s[j][k ^ j];
                  }
              }
          }
  
          // 计算最终结果
          int res = 0;
          for (int j = 0; j <= m; ++j)
              res = (res + dp[n][j][m]) % mod;
  
          System.out.println(res);
      }
  }
  ```

  

- Python

  ```python
  mod = 10**9 + 7
  N = 301
  
  # dp[i][j][k]: 前i个数,异或和为k,最后一个数为j的方案数
  dp = [[[0 for _ in range(N << 1)] for _ in range(N)] for _ in range(N)]
  # s[j][k]: dp[i-1][0~j][k]的前缀和
  s = [[0 for _ in range(N << 1)] for _ in range(N)]
  
  n, m = map(int, input().split())
  
  # 初始化:只有一种方案,即什么都不选
  dp[0][0][0] = 1
  
  for i in range(1, n + 1):
      # 计算前缀和
      for j in range(m + 1):
          for k in range(2 * m + 1):
              s[j][k] = dp[i - 1][j][k]
              if j > 0:
                  s[j][k] = (s[j][k] + s[j - 1][k]) % mod
      
      # 状态转移
      for j in range(m + 1):
          for k in range(2 * m + 1):
              if k ^ j <= 2 * m:
                  dp[i][j][k] = s[j][k ^ j]
  
  # 计算最终结果
  res = sum(dp[n][j][m] for j in range(m + 1)) % mod
  
  print(res)
  ```