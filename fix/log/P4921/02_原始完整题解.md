## 解题思路

设整个数组的按位与结果为 $A$。

删除某个元素 $a_i$ 后，剩余元素的按位与结果只可能在某些二进制位上从 $0$ 变成 $1$，不会让 $A$ 中原本为 $1$ 的位变成 $0$。

因此，删除 $a_i$ 后结果严格变大，当且仅当存在某个二进制位满足：

* 该位在 $A$ 中为 $0$
* 除了 $a_i$ 以外，其他所有数这一位都是 $1$
* 也就是说，整个数组中只有 $a_i$ 这一位是 $0$

所以可以按位统计：

1. 枚举二进制位 $0$ 到 $30$
2. 统计这一位为 $0$ 的元素个数
3. 如果恰好只有 $1$ 个元素这一位为 $0$，那么删除这个元素后，该位会从 $0$ 变成 $1$
4. 用标记数组记录满足条件的下标，避免同一个下标被多个二进制位重复统计

核心算法是位运算与按位统计。

## 复杂度分析

设数组长度为 $n$，整数范围不超过 $10^9$，最多只需要检查 $31$ 个二进制位。

时间复杂度为 $O(31n)$，可以看作 $O(n)$。

空间复杂度为 $O(n)$，用于标记满足条件的下标。

## 代码实现

### Python

```python
import sys


def count_valid(a):
    n = len(a)
    ok = [False] * n  # 标记哪些下标满足条件

    # 枚举 0 到 30 位，足够覆盖 1e9
    for bit in range(31):
        zero_count = 0
        zero_pos = -1

        # 统计当前位为 0 的元素数量
        for i in range(n):
            if ((a[i] >> bit) & 1) == 0:
                zero_count += 1
                zero_pos = i

        # 如果只有一个数当前位为 0，删除它后这一位会变成 1
        if zero_count == 1:
            ok[zero_pos] = True

    return sum(ok)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + n]
        idx += n

        ans.append(str(count_valid(a)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 计算满足条件的下标数量
    static int countValid(int[] a) {
        int n = a.length;
        boolean[] ok = new boolean[n]; // 标记满足条件的下标

        // 枚举 0 到 30 位，足够覆盖 1e9
        for (int bit = 0; bit <= 30; bit++) {
            int zeroCount = 0;
            int zeroPos = -1;

            // 统计当前位为 0 的元素数量
            for (int i = 0; i < n; i++) {
                if (((a[i] >> bit) & 1) == 0) {
                    zeroCount++;
                    zeroPos = i;
                }
            }

            // 如果只有一个数当前位为 0，删除它后这一位会变成 1
            if (zeroCount == 1) {
                ok[zeroPos] = true;
            }
        }

        int ans = 0;
        for (boolean v : ok) {
            if (v) ans++;
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();

        for (int tc = 0; tc < T; tc++) {
            int n = fs.nextInt();
            int[] a = new int[n];

            for (int i = 0; i < n; i++) {
                a[i] = fs.nextInt();
            }

            sb.append(countValid(a)).append('\n');
        }

        System.out.print(sb.toString());
    }

    // 数据量较大，使用简单快读
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

        int nextInt() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + c - '0';
                c = read();
            }

            return val * sign;
        }
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 计算满足条件的下标数量
int countValid(const vector<int>& a) {
    int n = a.size();
    vector<int> ok(n, 0); // 标记满足条件的下标

    // 枚举 0 到 30 位，足够覆盖 1e9
    for (int bit = 0; bit <= 30; bit++) {
        int zeroCount = 0;
        int zeroPos = -1;

        // 统计当前位为 0 的元素数量
        for (int i = 0; i < n; i++) {
            if (((a[i] >> bit) & 1) == 0) {
                zeroCount++;
                zeroPos = i;
            }
        }

        // 如果只有一个数当前位为 0，删除它后这一位会变成 1
        if (zeroCount == 1) {
            ok[zeroPos] = 1;
        }
    }

    int ans = 0;
    for (int v : ok) {
        ans += v;
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << countValid(a) << '\n';
    }

    return 0;
}
```