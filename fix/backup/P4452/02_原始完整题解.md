## 解题思路

* 将位置视为 1…n 的点，按给定序列依次“激活”。
* 规则：若当前没有已激活点，首次激活免费；之后每次若要激活的点与某个已激活点相邻（左右相差 1），则免费，否则需要一次“冷启动”。
* 因为激活顺序固定，最少冷启动次数是**确定的**：顺序扫描序列，判断该位置左右是否已有被激活的位置。
* 算法（贪心 + 模拟）
  用长度为 n+2 的布尔数组标记已激活（两端加哨兵避免越界）。遍历序列：

  * 第一个元素直接标记为激活；
  * 其余对于 ai，若 visited\[ai-1] 或 visited\[ai+1] 为真，则免费；否则冷启动次数 +1。随后将 visited\[ai] 置真。
* 本质上等价于：动态加入点并统计新连通块的产生次数（第一次不计）。

## 复杂度分析

* 时间复杂度：对每个测试用例遍历一次序列，O(n)。
* 空间复杂度：一个标记数组，O(n)。

## 代码实现

### Python

```python
# -*- coding: utf-8 -*-
import sys

def min_cold_starts(n, seq):
    # 访问标记，左右各加一位哨兵，避免边界判断
    vis = [False] * (n + 2)
    cold = 0
    for i, a in enumerate(seq):
        if i == 0:
            vis[a] = True           # 第一次激活免费
            continue
        # 若与已激活点相邻则免费，否则需要冷启动
        if vis[a - 1] or vis[a + 1]:
            vis[a] = True
        else:
            cold += 1
            vis[a] = True
    return cold

def main():
    data = list(map(int, sys.stdin.read().strip().split()))
    t = data[0]
    idx = 1
    out = []
    for _ in range(t):
        n = data[idx]; idx += 1
        seq = data[idx: idx + n]; idx += n
        out.append(str(min_cold_starts(n, seq)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
// -*- coding: utf-8 -*-
import java.io.*;
import java.util.*;

public class Main {
    // 计算最少冷启动次数
    static int minColdStarts(int n, int[] a) {
        boolean[] vis = new boolean[n + 2]; // 两端哨兵
        int cold = 0;
        for (int i = 0; i < n; i++) {
            int x = a[i];
            if (i == 0) {           // 第一次激活免费
                vis[x] = true;
                continue;
            }
            if (vis[x - 1] || vis[x + 1]) { // 与已激活相邻则免费
                vis[x] = true;
            } else {
                cold++;
                vis[x] = true;
            }
        }
        return cold;
    }

    // 简单快读，适配 2e5 数据量
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
        StringBuilder sb = new StringBuilder();
        int t = fs.nextInt();
        for (int _case = 0; _case < t; _case++) {
            int n = fs.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = fs.nextInt();
            sb.append(minColdStarts(n, a)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// -*- coding: utf-8 -*-
#include <bits/stdc++.h>
using namespace std;

// 计算最少冷启动次数
int min_cold_starts(int n, const vector<int>& seq) {
    vector<char> vis(n + 2, 0); // 两端哨兵，char 更省空间
    int cold = 0;
    for (int i = 0; i < n; ++i) {
        int a = seq[i];
        if (i == 0) {           // 第一次激活免费
            vis[a] = 1;
            continue;
        }
        // 若与已激活点相邻则免费，否则需要冷启动
        if (vis[a - 1] || vis[a + 1]) {
            vis[a] = 1;
        } else {
            ++cold;
            vis[a] = 1;
        }
    }
    return cold;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n; cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << min_cold_starts(n, a) << '\n';
    }
    return 0;
}
```