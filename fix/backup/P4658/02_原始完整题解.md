## 解题思路

这是一道典型的二维动态规划 + 极小化极大（minimax）博弈问题。

棋子从左上角 $(1,1)$ 出发，每次只能向右或向下走一步，直到到达右下角 $(n,m)$ 为止。总步数固定为：

$$
(n-1)+(m-1)=n+m-2
$$

也就是说，游戏过程中的“走法长度”是固定的，双方只能决定每一步走右还是走下，因此本题本质上是在一张 DAG（有向无环图）上进行双人零和博弈。

### 状态含义

设棋盘中的字符 `'1'` 对应得分 $+1$，字符 `'0'` 对应得分 $-1$。

我们定义：

$$
dp[i][j]
$$

表示当前棋子位于 $(i,j)$，并且**接下来轮到当前应行动的玩家操作**时，从这个状态开始到游戏结束，最终“天才同学总分 - 蛋哥同学总分”的最优结果。

注意：题目说明起点 $(1,1)$ 不计分，因此 $dp[1][1]$ 的转移只考虑下一步走到的新格子得分。



### 谁在当前位置行动

走到位置 $(i,j)$ 时，已经走了：

$$
(i-1)+(j-1)=i+j-2
$$

步。

* 若 $i+j-2$ 为偶数，说明前面走了偶数步，下一步轮到先手“天才同学”操作；
* 若 $i+j-2$ 为奇数，说明下一步轮到后手“蛋哥同学”操作。

也就是：

* 当 $(i+j)$ 为偶数时，轮到天才同学；
* 当 $(i+j)$ 为奇数时，轮到蛋哥同学。



### 状态转移

从 $(i,j)$ 出发，下一步只能走到：

* $(i+1,j)$
* $(i,j+1)$

前提是不越界。

设走到的新格子得分为：

$$
w =
\begin{cases}
1, & \text{若该格子是 } '1' \
-1, & \text{若该格子是 } '0'
\end{cases}
$$

#### 1. 当前轮到天才同学

天才同学希望最大化最终差值，因此会在所有合法走法中取最大值。

如果走到下一个格子获得分数 $w$，那么差值会增加 $w$，再加上后续局面的最优结果：

$$
dp[i][j] = \max(dp[next] + w)
$$

#### 2. 当前轮到蛋哥同学

蛋哥同学希望最小化“天才 - 蛋哥”的差值。

如果蛋哥走到下一个格子获得分数 $w$，那么蛋哥分数增加 $w$，因此差值会减少 $w$，即：

$$
dp[i][j] = \min(dp[next] - w)
$$



### 边界条件

当棋子已经位于终点 $(n,m)$ 时，游戏结束，之后没有任何得分：

$$
dp[n][m] = 0
$$


### 实现方法

1. 读入棋盘，将 `'1'` 看作 $+1$，`'0'` 看作 $-1$。
2. 定义二维数组 `dp`。
3. 从右下角倒序枚举每个格子：

   * 若是终点，`dp[i][j]=0`
   * 若轮到天才，取所有合法转移的最大值
   * 若轮到蛋哥，取所有合法转移的最小值
4. 最终输出 `dp[0][0]`（代码中通常使用 $0$ 下标）。



## 复杂度分析

设棋盘大小为 $n \times m$。

### 时间复杂度

每个格子只会被计算一次，每次最多看两个转移方向，因此时间复杂度为：

$$
O(nm)
$$

### 空间复杂度

使用一个二维 `dp` 数组保存所有状态，因此空间复杂度为：

$$
O(nm)
$$

在题目给出的数据范围下，$n \times m \le 4 \times 10^5$，该复杂度完全可行。



## 代码实现

### Python

```python
import sys


def solve(n, m, grid):
    # dp[i][j] 表示当前棋子在 (i,j)，从这里开始在双方最优操作下，
    # 最终“天才总分 - 蛋哥总分”的结果
    dp = [[0] * m for _ in range(n)]

    # 从右下角向左上角倒序进行动态规划
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            # 终点位置已经无法继续移动，后续贡献为 0
            if i == n - 1 and j == m - 1:
                dp[i][j] = 0
                continue

            # 若 (i+j) 为偶数，说明当前轮到天才操作，他要让差值尽量大
            if (i + j) % 2 == 0:
                best = -10**18

                # 向下走
                if i + 1 < n:
                    # 走到新格子的得分：'1' 记 +1，'0' 记 -1
                    score = 1 if grid[i + 1][j] == '1' else -1
                    best = max(best, dp[i + 1][j] + score)

                # 向右走
                if j + 1 < m:
                    score = 1 if grid[i][j + 1] == '1' else -1
                    best = max(best, dp[i][j + 1] + score)

                dp[i][j] = best

            # 若 (i+j) 为奇数，说明当前轮到蛋哥操作，他要让差值尽量小
            else:
                best = 10**18

                # 向下走
                if i + 1 < n:
                    # 蛋哥得分增加 score，因此“天才 - 蛋哥”会减少 score
                    score = 1 if grid[i + 1][j] == '1' else -1
                    best = min(best, dp[i + 1][j] - score)

                # 向右走
                if j + 1 < m:
                    score = 1 if grid[i][j + 1] == '1' else -1
                    best = min(best, dp[i][j + 1] - score)

                dp[i][j] = best

    return dp[0][0]


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    print(solve(n, m, grid))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {

    public static int solve(int n, int m, String[] grid) {
        // dp[i][j] 表示当前棋子在 (i,j)，从这里开始在双方最优操作下，
        // 最终“天才总分 - 蛋哥总分”的结果
        int[][] dp = new int[n][m];

        // 从右下角向左上角倒序进行动态规划
        for (int i = n - 1; i >= 0; i--) {
            for (int j = m - 1; j >= 0; j--) {
                // 终点位置无法继续移动
                if (i == n - 1 && j == m - 1) {
                    dp[i][j] = 0;
                    continue;
                }

                // 当前轮到天才操作，他希望最终差值尽量大
                if ((i + j) % 2 == 0) {
                    int best = Integer.MIN_VALUE;

                    // 向下走
                    if (i + 1 < n) {
                        int score = grid[i + 1].charAt(j) == '1' ? 1 : -1;
                        best = Math.max(best, dp[i + 1][j] + score);
                    }

                    // 向右走
                    if (j + 1 < m) {
                        int score = grid[i].charAt(j + 1) == '1' ? 1 : -1;
                        best = Math.max(best, dp[i][j + 1] + score);
                    }

                    dp[i][j] = best;
                }
                // 当前轮到蛋哥操作，他希望最终差值尽量小
                else {
                    int best = Integer.MAX_VALUE;

                    // 向下走
                    if (i + 1 < n) {
                        int score = grid[i + 1].charAt(j) == '1' ? 1 : -1;
                        best = Math.min(best, dp[i + 1][j] - score);
                    }

                    // 向右走
                    if (j + 1 < m) {
                        int score = grid[i].charAt(j + 1) == '1' ? 1 : -1;
                        best = Math.min(best, dp[i][j + 1] - score);
                    }

                    dp[i][j] = best;
                }
            }
        }

        return dp[0][0];
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());

        String[] grid = new String[n];
        for (int i = 0; i < n; i++) {
            grid[i] = br.readLine();
        }

        System.out.println(solve(n, m, grid));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <climits>
using namespace std;

int solve(int n, int m, const vector<string>& grid) {
    // dp[i][j] 表示当前棋子在 (i,j)，从这里开始在双方最优操作下，
    // 最终“天才总分 - 蛋哥总分”的结果
    vector<vector<int>> dp(n, vector<int>(m, 0));

    // 从右下角向左上角倒序进行动态规划
    for (int i = n - 1; i >= 0; i--) {
        for (int j = m - 1; j >= 0; j--) {
            // 终点位置无法继续移动
            if (i == n - 1 && j == m - 1) {
                dp[i][j] = 0;
                continue;
            }

            // 当前轮到天才操作，他希望最终差值尽量大
            if ((i + j) % 2 == 0) {
                int best = INT_MIN;

                // 向下走
                if (i + 1 < n) {
                    int score = (grid[i + 1][j] == '1' ? 1 : -1);
                    best = max(best, dp[i + 1][j] + score);
                }

                // 向右走
                if (j + 1 < m) {
                    int score = (grid[i][j + 1] == '1' ? 1 : -1);
                    best = max(best, dp[i][j + 1] + score);
                }

                dp[i][j] = best;
            }
            // 当前轮到蛋哥操作，他希望最终差值尽量小
            else {
                int best = INT_MAX;

                // 向下走
                if (i + 1 < n) {
                    int score = (grid[i + 1][j] == '1' ? 1 : -1);
                    best = min(best, dp[i + 1][j] - score);
                }

                // 向右走
                if (j + 1 < m) {
                    int score = (grid[i][j + 1] == '1' ? 1 : -1);
                    best = min(best, dp[i][j + 1] - score);
                }

                dp[i][j] = best;
            }
        }
    }

    return dp[0][0];
}

int main() {
    int n, m;
    cin >> n >> m;

    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    cout << solve(n, m, grid) << "\n";
    return 0;
}
```