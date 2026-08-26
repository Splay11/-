## 解题思路

先把题意抽象一下。

给定一个 $n \times m$ 的字符矩阵，每个位置是 `'B'` 或 `'S'`。

对于每一行，我们可以独立选择删除这一行最左侧的 $k$ 个字符，其中 $0 \le k \le m$。
要求删除后，整个矩阵中剩余的 `'B'` 和 `'S'` 数量相等。
目标是让删除的总字符数最少。

### 核心思路

设整个矩阵一开始：

* `'B'` 的总数为 $cnt_B$
* `'S'` 的总数为 $cnt_S$

定义总差值：

$$
D = cnt_B - cnt_S
$$

如果最后要让 `'B'` 和 `'S'` 数量相等，那么删除掉的那些字符中，`'B'` 和 `'S'` 的数量差也必须恰好是 $D$。

原因很直接：

* 原来总差值是 $D$
* 删除掉一部分字符后，剩余差值要变成 $0$
* 所以删除部分的差值必须正好抵消原来的 $D$



对于某一行，如果删除前缀长度为 $k$，那么这一行会产生两个信息：

1. 删除了多少个字符：$k$
2. 被删除前缀的差值是多少：

$$
\Delta = (\text{前缀中 B 的个数}) - (\text{前缀中 S 的个数})
$$

这样，每一行其实就变成了若干种“选择方案”：

* 删除长度为 $0$，贡献差值 $0$
* 删除长度为 $1$，贡献某个差值
* 删除长度为 $2$，贡献某个差值
* ...
* 删除长度为 $m$，贡献某个差值

现在问题就转化成了：

* 每一行选一个方案
* 使得所有行贡献的差值之和恰好等于 $D$
* 并且总代价（删除总长度）最小

这就是一个典型的分组背包动态规划。



### 实现方法

#### 1. 预处理每一行的所有可选方案

对于每一行，枚举前缀长度 $k=0\sim m$，维护当前前缀的差值：

* 遇到 `'B'`，差值加 $1$
* 遇到 `'S'`，差值减 $1$

于是可以得到该行每个前缀长度对应的 $(\Delta, k)$。

注意：同一行中，可能有多个不同长度的前缀得到相同的差值。
显然只保留删除长度最小的那个即可，因为它一定更优。

所以对每一行，我们先整理出：

$$
\text{该行达到某个差值时的最小删除长度}
$$



#### 2. 动态规划

设总字符数为：

$$
C = n \times m
$$

那么任意差值一定落在区间 $[-C, C]$ 内。
为了方便数组下标处理，使用偏移量：

$$
offset = C
$$

定义状态：

$$
dp[x] = \text{处理完前若干行后，得到删除差值为 } x-offset \text{ 时的最小删除总数}
$$

初始时：

* 还没有处理任何一行
* 删除差值为 $0$
* 删除总数为 $0$

所以：

$$
dp[offset] = 0
$$

接下来逐行转移。对于当前行的每个可选方案 $(\Delta, cost)$，尝试更新新状态。

转移方程为：

$$
ndp[j + \Delta] = \min(ndp[j + \Delta], dp[j] + cost)
$$

最终我们需要的目标是“删除部分差值恰好为 $D$”，也就是查看：

$$
dp[offset + D]
$$

这就是答案。

题目保证一定有删除整行的操作，因此总能删光所有字符，此时 `'B'` 和 `'S'` 都为 $0$，一定相等，所以答案一定存在。

## 复杂度分析

设总字符数为：

$$
C = \sum (n \times m)
$$

题目保证所有测试数据中：

$$
C \le 5 \times 10^3
$$

### 时间复杂度

对于每组数据：

1. 预处理每一行所有前缀，复杂度为 $O(nm)$
2. 动态规划时，差值范围大小为 $O(C)$，每一行的可选方案总数不超过该行长度加一，所有行方案总数总计为 $O(C)$

因此总时间复杂度为：

$$
O(C^2)
$$

在 $C \le 5000$ 的条件下是完全可行的。

### 空间复杂度

动态规划数组大小为差值范围：

$$
O(C)
$$

再加上每一行存储若干方案，总体空间复杂度为：

$$
O(C)
$$


## 代码实现

### Python

```python
import sys


def solve_case(n, m, grid):
    # 统计初始时整个矩阵中 B 与 S 的数量差：B 记为 +1，S 记为 -1
    total_diff = 0
    for row in grid:
        for ch in row:
            if ch == 'B':
                total_diff += 1
            else:
                total_diff -= 1

    # 最大可能差值绝对值不超过总字符数
    max_diff = n * m
    offset = max_diff
    inf = 10 ** 18

    # dp[i] 表示当前处理到某些行后，删除部分差值为 i - offset 时的最小删除字符数
    dp = [inf] * (2 * max_diff + 1)
    dp[offset] = 0

    # 逐行进行分组背包
    for row in grid:
        # best[delta] = 在当前行中，删除某个前缀后得到差值 delta 的最小删除长度
        best = {}

        # 删除长度为 0 的前缀，差值为 0，代价为 0
        cur_diff = 0
        best[0] = 0

        # 枚举当前行所有前缀
        for i, ch in enumerate(row):
            if ch == 'B':
                cur_diff += 1
            else:
                cur_diff -= 1

            length = i + 1

            # 同一个差值只保留最小删除长度
            if cur_diff not in best or length < best[cur_diff]:
                best[cur_diff] = length

        # 当前行转移后的新数组
        ndp = [inf] * (2 * max_diff + 1)

        # 枚举旧状态
        for old_idx in range(2 * max_diff + 1):
            if dp[old_idx] == inf:
                continue

            # 枚举当前行的所有可选方案
            for delta, cost in best.items():
                new_idx = old_idx + delta
                if 0 <= new_idx <= 2 * max_diff:
                    ndp[new_idx] = min(ndp[new_idx], dp[old_idx] + cost)

        dp = ndp

    # 目标：删除部分差值恰好等于 total_diff
    return dp[offset + total_diff]


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        ans.append(str(solve_case(n, m, grid)))

    print('\n'.join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

    // 计算单组测试数据的答案
    public static int solveCase(int n, int m, String[] grid) {
        // 统计初始总差值：B 记为 +1，S 记为 -1
        int totalDiff = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i].charAt(j) == 'B') {
                    totalDiff++;
                } else {
                    totalDiff--;
                }
            }
        }

        // 最大可能差值绝对值不超过总字符数
        int maxDiff = n * m;
        int offset = maxDiff;
        int size = 2 * maxDiff + 1;
        int inf = 1 << 29;

        // dp[i] 表示当前处理到某些行后，删除部分差值为 i - offset 时的最小删除字符数
        int[] dp = new int[size];
        Arrays.fill(dp, inf);
        dp[offset] = 0;

        // 逐行进行分组背包
        for (int i = 0; i < n; i++) {
            // 记录当前行中某个差值对应的最小删除长度
            Map<Integer, Integer> best = new HashMap<>();

            // 删除长度为 0 的前缀
            int curDiff = 0;
            best.put(0, 0);

            // 枚举所有前缀
            for (int j = 0; j < m; j++) {
                if (grid[i].charAt(j) == 'B') {
                    curDiff++;
                } else {
                    curDiff--;
                }

                int len = j + 1;

                // 同一差值只保留最小删除长度
                if (!best.containsKey(curDiff) || len < best.get(curDiff)) {
                    best.put(curDiff, len);
                }
            }

            int[] ndp = new int[size];
            Arrays.fill(ndp, inf);

            // 枚举旧状态
            for (int oldIdx = 0; oldIdx < size; oldIdx++) {
                if (dp[oldIdx] == inf) {
                    continue;
                }

                // 枚举当前行可选方案
                for (Map.Entry<Integer, Integer> entry : best.entrySet()) {
                    int delta = entry.getKey();
                    int cost = entry.getValue();
                    int newIdx = oldIdx + delta;

                    if (newIdx >= 0 && newIdx < size) {
                        ndp[newIdx] = Math.min(ndp[newIdx], dp[oldIdx] + cost);
                    }
                }
            }

            dp = ndp;
        }

        // 目标：删除部分差值恰好等于 totalDiff
        return dp[offset + totalDiff];
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int t = fs.nextInt();
        for (int caseId = 0; caseId < t; caseId++) {
            int n = fs.nextInt();
            int m = fs.nextInt();

            String[] grid = new String[n];
            for (int i = 0; i < n; i++) {
                grid[i] = fs.next();
            }

            sb.append(solveCase(n, m, grid)).append('\n');
        }

        System.out.print(sb.toString());
    }
}

// 使用 BufferedReader + StringTokenizer 完成输入
class FastScanner {
    private BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    private StringTokenizer st;

    public String next() throws IOException {
        while (st == null || !st.hasMoreElements()) {
            st = new StringTokenizer(br.readLine());
        }
        return st.nextToken();
    }

    public int nextInt() throws IOException {
        return Integer.parseInt(next());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

// 计算单组测试数据的答案
int solveCase(int n, int m, const vector<string>& grid) {
    // 统计初始总差值：B 记为 +1，S 记为 -1
    int totalDiff = 0;
    for (int i = 0; i < n; i++) {
        for (char ch : grid[i]) {
            if (ch == 'B') {
                totalDiff++;
            } else {
                totalDiff--;
            }
        }
    }

    // 最大可能差值绝对值不超过总字符数
    int maxDiff = n * m;
    int offset = maxDiff;
    int size = 2 * maxDiff + 1;
    const int INF = 1e9;

    // dp[i] 表示当前处理到某些行后，删除部分差值为 i - offset 时的最小删除字符数
    vector<int> dp(size, INF);
    dp[offset] = 0;

    // 逐行进行分组背包
    for (int i = 0; i < n; i++) {
        // 记录当前行中某个差值对应的最小删除长度
        unordered_map<int, int> best;

        // 删除长度为 0 的前缀
        int curDiff = 0;
        best[0] = 0;

        // 枚举所有前缀
        for (int j = 0; j < m; j++) {
            if (grid[i][j] == 'B') {
                curDiff++;
            } else {
                curDiff--;
            }

            int len = j + 1;

            // 同一差值只保留最小删除长度
            if (!best.count(curDiff) || len < best[curDiff]) {
                best[curDiff] = len;
            }
        }

        vector<int> ndp(size, INF);

        // 枚举旧状态
        for (int oldIdx = 0; oldIdx < size; oldIdx++) {
            if (dp[oldIdx] == INF) {
                continue;
            }

            // 枚举当前行的所有可选方案
            for (auto& entry : best) {
                int delta = entry.first;
                int cost = entry.second;
                int newIdx = oldIdx + delta;

                if (newIdx >= 0 && newIdx < size) {
                    ndp[newIdx] = min(ndp[newIdx], dp[oldIdx] + cost);
                }
            }
        }

        dp = ndp;
    }

    // 目标：删除部分差值恰好等于 totalDiff
    return dp[offset + totalDiff];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n, m;
        cin >> n >> m;

        vector<string> grid(n);
        for (int i = 0; i < n; i++) {
            cin >> grid[i];
        }

        cout << solveCase(n, m, grid) << '\n';
    }

    return 0;
}
```