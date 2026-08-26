## 解题思路

一次操作本质上是把盘面中的 $1$ 单位晶石从一个格子移动到另一个格子，因此整个盘面的晶石总数始终不变。

反过来，只要目标盘面 $B$ 的所有元素都是非负整数，并且满足：

$$
\sum B_{i,j}=\sum a_{i,j}
$$

那么一定可以从初始盘面变成 $B$。因为可以把所有 $a_{i,j}>B_{i,j}$ 的格子作为“供给方”，把所有 $a_{i,j}<B_{i,j}$ 的格子作为“需求方”，逐单位搬运即可，过程中不会把某个格子的晶石数减成负数。

所以问题转化为：

给定总和 $S$，是否存在一个上下、左右都对称的非负整数矩阵 $B$，使得元素总和为 $S$。

考虑对称性带来的格子分组。对于一个格子 $(i,j)$，它必须和以下格子相等：

$$
(i,j),\ (n+1-i,j),\ (i,m+1-j),\ (n+1-i,m+1-j)
$$

这些格子组成一个对称轨道。一个轨道内所有值必须相同。

轨道大小只可能是 $1,2,4$：

1. 如果 $n,m$ 都是偶数，所有轨道大小都是 $4$，因此总和必须能被 $4$ 整除。
2. 如果 $n,m$ 中恰好一个是奇数，会存在大小为 $2$ 的轨道，其余为 $4$，因此总和必须能被 $2$ 整除。
3. 如果 $n,m$ 都是奇数，中间格子单独构成大小为 $1$ 的轨道，因此任意总和都可以构造。

实现时不需要复杂分配，只需要把总和放到一个合法的对称轨道上即可：

1. $n,m$ 都是奇数：把 $S$ 放在中心格子。
2. $n$ 是奇数，$m$ 是偶数：把 $S/2$ 放在中间行的最左和最右两个格子。
3. $n$ 是偶数，$m$ 是奇数：把 $S/2$ 放在中间列的最上和最下两个格子。
4. $n,m$ 都是偶数：把 $S/4$ 放在四个角上。

这样构造出的矩阵显然上下、左右都对称，并且总和等于原矩阵总和。

## 复杂度分析

设当前测试数据矩阵大小为 $n \times m$。

读取原矩阵并求和需要遍历所有元素，时间复杂度为：

$$
O(nm)
$$

构造和输出矩阵也需要处理 $nm$ 个元素，时间复杂度为：

$$
O(nm)
$$

因此单组测试数据总时间复杂度为：

$$
O(nm)
$$

所有测试数据的 $n \cdot m$ 总和不超过 $5 \times 10^5$，所以总复杂度可以接受。

需要存储输出矩阵 $B$，空间复杂度为：

$$
O(nm)
$$

## 代码实现

### Python

```python
import sys


def build_matrix(n, m, total_sum):
    # 创建全 0 矩阵，之后只在一个对称轨道上放置总和
    b = [[0] * m for _ in range(n)]

    # n 和 m 都是奇数，中心格子单独对称，可以放任意总和
    if n % 2 == 1 and m % 2 == 1:
        b[n // 2][m // 2] = total_sum
        return b

    # n 是奇数，m 是偶数，只能使用大小为 2 的左右对称轨道
    if n % 2 == 1 and m % 2 == 0:
        if total_sum % 2 != 0:
            return None
        value = total_sum // 2
        row = n // 2
        b[row][0] = value
        b[row][m - 1] = value
        return b

    # n 是偶数，m 是奇数，只能使用大小为 2 的上下对称轨道
    if n % 2 == 0 and m % 2 == 1:
        if total_sum % 2 != 0:
            return None
        value = total_sum // 2
        col = m // 2
        b[0][col] = value
        b[n - 1][col] = value
        return b

    # n 和 m 都是偶数，所有对称轨道大小都是 4
    if total_sum % 4 != 0:
        return None
    value = total_sum // 4
    b[0][0] = value
    b[0][m - 1] = value
    b[n - 1][0] = value
    b[n - 1][m - 1] = value
    return b


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    index = 0
    t = data[index]
    index += 1

    ans = []

    for _ in range(t):
        n = data[index]
        m = data[index + 1]
        index += 2

        # 读取原矩阵时只需要求元素总和
        total_sum = 0
        for _ in range(n * m):
            total_sum += data[index]
            index += 1

        b = build_matrix(n, m, total_sum)

        # 无法构造时输出 -1
        if b is None:
            ans.append("-1")
        else:
            # 输出构造出的对称矩阵
            for row in b:
                ans.append(" ".join(map(str, row)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    static long[][] buildMatrix(int n, int m, long totalSum) {
        // 创建全 0 矩阵，之后只在一个对称轨道上放置总和
        long[][] b = new long[n][m];

        // n 和 m 都是奇数，中心格子单独对称，可以放任意总和
        if (n % 2 == 1 && m % 2 == 1) {
            b[n / 2][m / 2] = totalSum;
            return b;
        }

        // n 是奇数，m 是偶数，只能使用大小为 2 的左右对称轨道
        if (n % 2 == 1 && m % 2 == 0) {
            if (totalSum % 2 != 0) {
                return null;
            }
            long value = totalSum / 2;
            int row = n / 2;
            b[row][0] = value;
            b[row][m - 1] = value;
            return b;
        }

        // n 是偶数，m 是奇数，只能使用大小为 2 的上下对称轨道
        if (n % 2 == 0 && m % 2 == 1) {
            if (totalSum % 2 != 0) {
                return null;
            }
            long value = totalSum / 2;
            int col = m / 2;
            b[0][col] = value;
            b[n - 1][col] = value;
            return b;
        }

        // n 和 m 都是偶数，所有对称轨道大小都是 4
        if (totalSum % 4 != 0) {
            return null;
        }
        long value = totalSum / 4;
        b[0][0] = value;
        b[0][m - 1] = value;
        b[n - 1][0] = value;
        b[n - 1][m - 1] = value;
        return b;
    }

    public static void main(String[] args) throws Exception {
        BufferedInputStream in = new BufferedInputStream(System.in);
        StringBuilder out = new StringBuilder();

        int t = nextInt(in);

        for (int caseId = 0; caseId < t; caseId++) {
            int n = nextInt(in);
            int m = nextInt(in);

            // 读取原矩阵时只需要求元素总和
            long totalSum = 0;
            for (int i = 0; i < n * m; i++) {
                totalSum += nextLong(in);
            }

            long[][] b = buildMatrix(n, m, totalSum);

            // 无法构造时输出 -1
            if (b == null) {
                out.append("-1\n");
            } else {
                // 输出构造出的对称矩阵
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < m; j++) {
                        if (j > 0) {
                            out.append(' ');
                        }
                        out.append(b[i][j]);
                    }
                    out.append('\n');
                }
            }
        }

        System.out.print(out.toString());
    }

    static int nextInt(InputStream in) throws IOException {
        return (int) nextLong(in);
    }

    static long nextLong(InputStream in) throws IOException {
        int c;
        do {
            c = in.read();
        } while (c <= ' ' && c != -1);

        long sign = 1;
        if (c == '-') {
            sign = -1;
            c = in.read();
        }

        long num = 0;
        while (c > ' ') {
            num = num * 10 + c - '0';
            c = in.read();
        }

        return num * sign;
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<long long>> buildMatrix(int n, int m, long long totalSum, bool &ok) {
    // 创建全 0 矩阵，之后只在一个对称轨道上放置总和
    vector<vector<long long>> b(n, vector<long long>(m, 0));
    ok = true;

    // n 和 m 都是奇数，中心格子单独对称，可以放任意总和
    if (n % 2 == 1 && m % 2 == 1) {
        b[n / 2][m / 2] = totalSum;
        return b;
    }

    // n 是奇数，m 是偶数，只能使用大小为 2 的左右对称轨道
    if (n % 2 == 1 && m % 2 == 0) {
        if (totalSum % 2 != 0) {
            ok = false;
            return b;
        }
        long long value = totalSum / 2;
        int row = n / 2;
        b[row][0] = value;
        b[row][m - 1] = value;
        return b;
    }

    // n 是偶数，m 是奇数，只能使用大小为 2 的上下对称轨道
    if (n % 2 == 0 && m % 2 == 1) {
        if (totalSum % 2 != 0) {
            ok = false;
            return b;
        }
        long long value = totalSum / 2;
        int col = m / 2;
        b[0][col] = value;
        b[n - 1][col] = value;
        return b;
    }

    // n 和 m 都是偶数，所有对称轨道大小都是 4
    if (totalSum % 4 != 0) {
        ok = false;
        return b;
    }
    long long value = totalSum / 4;
    b[0][0] = value;
    b[0][m - 1] = value;
    b[n - 1][0] = value;
    b[n - 1][m - 1] = value;
    return b;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, m;
        cin >> n >> m;

        // 读取原矩阵时只需要求元素总和
        long long totalSum = 0;
        for (int i = 0; i < n * m; i++) {
            long long x;
            cin >> x;
            totalSum += x;
        }

        bool ok;
        vector<vector<long long>> b = buildMatrix(n, m, totalSum, ok);

        // 无法构造时输出 -1
        if (!ok) {
            cout << -1 << '\n';
        } else {
            // 输出构造出的对称矩阵
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    if (j > 0) {
                        cout << ' ';
                    }
                    cout << b[i][j];
                }
                cout << '\n';
            }
        }
    }

    return 0;
}
```