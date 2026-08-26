## 解题思路

### 关键观察

把整张 $n\times m$ 的网格按“蛇形路径（snake）”依次走过（第一行从左到右，第二行从右到左，第三行再从左到右……），就得到了一条**基于四相邻的哈密顿路径**：相邻访问的两个格子一定四邻接。
若令每个编号占据相同长度的一个连续片段，那么该编号对应的格子集合就是这条路径上的一个连续段，因此**天然是连通的**。

已知 $k\mid (n\cdot m)$，设

$$
s=\frac{n\cdot m}{k}.
$$

只需沿蛇形顺序把格子依次编号：先写 $s$ 个 1，再写 $s$ 个 2，…，直到 $k$。
这样：

* 每个编号出现次数恰为 $s$；
* 同一编号的格子在蛇形路径上连续，因此四连通；
* 构造对任意满足条件的 $(n,m,k)$ 都有效。

### 构造方法

1. 计算块大小 $s=\frac{n\cdot m}{k}$。
2. 遍历行 $i=0..n-1$：

   * 若 $i$ 为偶数行：列 $j=0..m-1$；
   * 若 $i$ 为奇数行：列 $j=m-1..0$。
     这就是蛇形顺序。
3. 维护当前编号 `cur` 与其已填数量 `cnt`：把当前格子赋为 `cur`；`cnt++`；若 `cnt==s`，则 `cur++，cnt=0`。
4. 输出整个网格。

### 正确性证明（简要）

蛇形遍历构成一条覆盖所有格子的路径，路径上相邻格子均四邻接。对任一编号 $a$，其格子集合正是这条路径上的一个连续长度为 $s$ 的片段。任何路径上的连续片段对应的格子集合在四邻接意义下必连通，故满足题意。

## 复杂度分析

* 时间复杂度：每个测试用例一次遍历所有格子，$O(nm)$。
* 空间复杂度：存一张 $n\times m$ 的答案矩阵，$O(nm)$。
  给定约束下（所有用例 $\sum nm \le 3\times10^5$），可轻松通过。

## 代码实现

### Python

```python
import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out_lines = []
    for _ in range(t):
        n, m, k = data[idx], data[idx+1], data[idx+2]
        idx += 3
        s = (n * m) // k  # 每个编号的出现次数

        g = [[0] * m for _ in range(n)]
        cur, cnt = 1, 0  # 当前编号及其已填数量

        for i in range(n):
            if i % 2 == 0:
                js = range(m)            # 左->右
            else:
                js = range(m - 1, -1, -1)  # 右->左
            for j in js:
                g[i][j] = cur
                cnt += 1
                if cnt == s:
                    cur += 1
                    cnt = 0

        # 输出本用例
        for i in range(n):
            out_lines.append(" ".join(map(str, g[i])))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) throws Exception {
        Scanner in = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        int t = Integer.parseInt(in.next());
        while (t-- > 0) {
            int n = in.nextInt();
            int m = in.nextInt();
            int k = in.nextInt();
            int s = (n * m) / k; // 每个编号份额

            int[][] g = new int[n][m];
            int cur = 1, cnt = 0;

            // 蛇形遍历
            for (int i = 0; i < n; i++) {
                if (i % 2 == 0) {
                    for (int j = 0; j < m; j++) {
                        g[i][j] = cur;
                        cnt++;
                        if (cnt == s) { cur++; cnt = 0; }
                    }
                } else {
                    for (int j = m - 1; j >= 0; j--) {
                        g[i][j] = cur;
                        cnt++;
                        if (cnt == s) { cur++; cnt = 0; }
                    }
                }
            }

            // 输出
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    if (j > 0) sb.append(' ');
                    sb.append(g[i][j]);
                }
                sb.append('\n');
            }
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n, m, k;
        cin >> n >> m >> k;
        int s = (n * m) / k; // 每个编号出现次数
        vector<vector<int>> g(n, vector<int>(m, 0));
        int cur = 1, cnt = 0;

        // 蛇形遍历填充
        for (int i = 0; i < n; ++i) {
            if (i % 2 == 0) {
                for (int j = 0; j < m; ++j) {
                    g[i][j] = cur;
                    if (++cnt == s) { ++cur; cnt = 0; }
                }
            } else {
                for (int j = m - 1; j >= 0; --j) {
                    g[i][j] = cur;
                    if (++cnt == s) { ++cur; cnt = 0; }
                }
            }
        }

        // 输出
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                if (j) cout << ' ';
                cout << g[i][j];
            }
            cout << '\n';
        }
    }
    return 0;
}
```