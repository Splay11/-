## 解题思路

给定长度为 `n` 的数组 `a[1..n]`（表示每块宝石的魔法印记种类），以及 `m` 个位置 `b_i`。问题是：对每个查询位置 `b_i`，询问从第 `b_i` 个宝石到第 `n` 个宝石这一段中，不同印记的种类数。

这是典型的“后缀不同元素计数”问题。
做法：从右向左遍历数组，维护一个“是否出现过”的集合（或布尔数组/哈希表）。若 `a[i]` 是第一次出现，则种类计数 `cnt++`。用数组 `f[i]` 记录从位置 `i` 到末尾的不同种类总数。遍历结束后，对于每个查询 `b_i`，直接输出 `f[b_i]` 即可。

相关算法：

* 反向扫描 + 去重集合（布尔数组或哈希集合）。
* 预处理后缀答案，单次查询 O(1)。

实现要点：

* 由于数据范围 `a_i ≤ 1e5`，可用大小为 `1e5+5` 的布尔数组 `vis` 标记是否出现，省去哈希常数。
* 预处理 `f[i]` 的时间为 O(n)，查询总时间 O(m)。

## 复杂度分析

* 时间复杂度：预处理 O(n)，每个查询 O(1)，总计 O(n + m)。
* 空间复杂度：`f` 需要 O(n)，`vis` 需要 O(U)`（U ≤ 1e5）`，总体 O(n + U)，在约束下可行。

## 代码实现

### Python

```python
# 题意：给定数组 a[1..n]，对每个查询位置 b，输出从 b 到 n 的不同数的个数
# 思路：从右往左，用布尔数组记录是否出现，得到后缀答案 f[i]

import sys

def solve(n, m, arr, queries):
    MAXV = 100000  # 根据题面 1 <= a_i <= 1e5
    vis = [False] * (MAXV + 1)  # 记录某个值是否已出现
    f = [0] * (n + 1)  # f[i] 表示从 i 到 n 的不同种类数（这里用 0-based 存 i 的答案）
    cnt = 0
    # 从右到左扫描
    for i in range(n - 1, -1, -1):
        v = arr[i]
        if not vis[v]:
            vis[v] = True
            cnt += 1
        f[i] = cnt
    # 输出每个查询
    out_lines = []
    for b in queries:
        out_lines.append(str(f[b - 1]))  # 输入是 1-based
    return "\n".join(out_lines)

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    arr = data[2:2 + n]
    queries = data[2 + n:2 + n + m]
    print(solve(n, m, arr, queries))

if __name__ == "__main__":
    main()
```

### Java

```java
// 题意同上：后缀不同元素计数
// 做法：从右往左预处理 f[i]，查询时 O(1)

import java.io.*;
import java.util.*;

public class Main {
    // 简单且高效的字节流读入（适合 1e5 级数据）
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        int nextInt() throws IOException {
            int c, sgn = 1, x = 0;
            do { c = read(); } while (c <= ' '); // 跳过空白
            if (c == '-') { sgn = -1; c = read(); }
            while (c > ' ') {
                x = x * 10 + (c - '0');
                c = read();
            }
            return x * sgn;
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder out = new StringBuilder();

        int n = fs.nextInt();
        int m = fs.nextInt();

        int[] a = new int[n];
        int MAXV = 100000; // 根据题面
        for (int i = 0; i < n; i++) a[i] = fs.nextInt();

        boolean[] vis = new boolean[MAXV + 1]; // 记录是否出现
        int[] f = new int[n + 1]; // f[i]：从 i 到 n 的不同数个数（0-based）
        int cnt = 0;

        // 从右到左预处理
        for (int i = n - 1; i >= 0; i--) {
            int v = a[i];
            if (!vis[v]) {
                vis[v] = true;
                cnt++;
            }
            f[i] = cnt;
        }

        // 逐个查询并输出
        for (int i = 0; i < m; i++) {
            int b = fs.nextInt(); // 1-based
            out.append(f[b - 1]).append('\n');
        }

        System.out.print(out.toString());
    }
}
```

### C++

```cpp
// 题意：给定数组 a[1..n]，回答 m 次查询：区间 [b, n] 中有多少个不同的数
// 解法：从右往左预处理后缀不同数 f[i]，查询直接输出 f[b]

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    const int MAXV = 100000; // 题面上限
    vector<char> vis(MAXV + 1, 0); // char 即可，节省内存
    vector<int> f(n + 1, 0);       // f[i]：从 i 到 n 的不同种类数（0-based）
    int cnt = 0;

    // 从右往左扫描并记录后缀答案
    for (int i = n - 1; i >= 0; --i) {
        int v = a[i];
        if (!vis[v]) {
            vis[v] = 1;
            ++cnt;
        }
        f[i] = cnt;
    }

    // 处理查询
    for (int i = 0; i < m; ++i) {
        int b; 
        cin >> b; // 1-based
        cout << f[b - 1] << "\n";
    }
    return 0;
}
```