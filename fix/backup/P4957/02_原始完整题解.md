## 解题思路

放置时只关心每个桶最上面球的质量。设数组 $top$ 表示每个桶的桶顶质量（即最上面球的质量）。

由于每次选择的是第一个桶顶质量严格大于当前球质量 $x$ 的桶，因此 $top$ 始终是非递减的：

* 若找到某个位置 $pos$，则把 $top[pos]$ 改成 $x$；
* 若找不到，说明所有桶顶质量都 $\le x$，就在末尾新建一个桶。

所以可以用二分查找中的 $upper\_bound$，快速找到第一个 $>x$ 的位置。

同时维护每个桶的高度 $height$，以及当前所有高度的异或和 $ans$。

当某个桶高度从 $h$ 变成 $h+1$ 时：

$$
ans = ans \oplus h \oplus (h+1)
$$

如果是新建桶，相当于高度从 $0$ 变成 $1$，直接异或 $1$ 即可。

## 复杂度分析

每个球需要一次二分查找，时间复杂度为：

$$
O(n\log n)
$$

需要存储桶顶质量和桶高度，空间复杂度为：

$$
O(n)
$$

对于所有测试数据，$\sum n \le 4\times 10^5$，复杂度可以通过。

## 代码实现

### Python

```python
import sys
from bisect import bisect_right

# 处理单组数据，返回每次操作后的异或和
def solve_case(arr):
    top = []       # 每个桶的桶顶质量，保持非递减
    height = []    # 每个桶的高度
    cur_xor = 0    # 当前所有桶高度的异或和
    res = []

    for x in arr:
        # 找到第一个桶顶质量 > x 的桶
        pos = bisect_right(top, x)

        if pos == len(top):
            # 新建一个桶
            top.append(x)
            height.append(1)
            cur_xor ^= 1
        else:
            # 放到已有桶上，更新桶顶质量和高度
            old_h = height[pos]
            cur_xor ^= old_h
            height[pos] = old_h + 1
            cur_xor ^= height[pos]
            top[pos] = x

        res.append(str(cur_xor))

    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    output = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        arr = data[idx:idx + n]
        idx += n

        output.append(" ".join(solve_case(arr)))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
```

### c++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 处理单组数据，返回每次操作后的异或和
vector<int> solve_case(const vector<long long>& a) {
    vector<long long> top;  // 每个桶的桶顶质量，保持非递减
    vector<int> height;     // 每个桶的高度
    vector<int> res;

    int cur_xor = 0;        // 当前所有桶高度的异或和

    for (long long x : a) {
        // 找到第一个桶顶质量 > x 的桶
        int pos = upper_bound(top.begin(), top.end(), x) - top.begin();

        if (pos == (int)top.size()) {
            // 新建一个桶
            top.push_back(x);
            height.push_back(1);
            cur_xor ^= 1;
        } else {
            // 放到已有桶上，更新桶顶质量和高度
            int old_h = height[pos];
            cur_xor ^= old_h;
            height[pos] = old_h + 1;
            cur_xor ^= height[pos];
            top[pos] = x;
        }

        res.push_back(cur_xor);
    }

    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<long long> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        vector<int> ans = solve_case(a);

        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }

    return 0;
}
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 处理单组数据，返回答案字符串
    static String solveCase(int n, long[] arr) {
        long[] top = new long[n];   // 每个桶的桶顶质量
        int[] height = new int[n];  // 每个桶的高度
        int piles = 0;              // 当前桶数
        int curXor = 0;             // 当前高度异或和

        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < n; i++) {
            long x = arr[i];

            // 二分查找第一个 top[pos] > x 的位置
            int l = 0, r = piles;
            while (l < r) {
                int mid = (l + r) / 2;
                if (top[mid] > x) {
                    r = mid;
                } else {
                    l = mid + 1;
                }
            }

            int pos = l;

            if (pos == piles) {
                // 新建一个桶
                top[piles] = x;
                height[piles] = 1;
                piles++;
                curXor ^= 1;
            } else {
                // 放到已有桶上，更新桶顶质量和高度
                int oldH = height[pos];
                curXor ^= oldH;
                height[pos] = oldH + 1;
                curXor ^= height[pos];
                top[pos] = x;
            }

            if (i > 0) sb.append(' ');
            sb.append(curXor);
        }

        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder output = new StringBuilder();

        int t = fs.nextInt();

        for (int tc = 0; tc < t; tc++) {
            int n = fs.nextInt();
            long[] arr = new long[n];

            for (int i = 0; i < n; i++) {
                arr[i] = fs.nextLong();
            }

            output.append(solveCase(n, arr));
            if (tc + 1 < t) output.append('\n');
        }

        System.out.print(output.toString());
    }

    // 数据量较大，使用基于 BufferedInputStream 的输入
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        long nextLong() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            long sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            long val = 0;
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }

            return val * sign;
        }

        int nextInt() throws IOException {
            return (int) nextLong();
        }
    }
}
```