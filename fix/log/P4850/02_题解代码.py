## 解题思路

消除相邻相同物品，可以用栈模拟：

从左到右扫描序列：

* 若栈顶和当前物品相同，则二者消除，栈顶弹出；
* 否则当前物品入栈。

最终栈中剩下的序列就是无法继续消除的序列，记为 $b$，长度为 $m$。

原序列中已经能消除的次数为：

$base=\frac{n-m}{2}$

接下来考虑最多插入 $1$ 个物品。

在化简后的序列 $b$ 中，任意相邻元素都不同。若在某个位置插入一个和某个中心元素相同的物品，就可以先消掉这个中心元素和新插入的物品，然后可能继续向两边连锁消除。

例如：

$b=[1,2,3,2,1]$

在 $3$ 旁边插入 $3$，先消掉 $3,3$，然后两边的 $2,2$ 消掉，再两边的 $1,1$ 消掉。

因此，插入一次带来的最大额外消除次数，等于 $b$ 中最长奇数长度回文半径。

也就是说，需要在 $b$ 中求最长奇回文半径。可以使用 Manacher 算法的奇回文版本，在线性时间内求出每个位置作为中心的最大回文半径。

最终答案为：

$base+maxRadius$

特殊情况：

* 若 $b$ 为空，说明原序列已经全部消完，此时再插入 $1$ 个物品无法消除，所以额外次数为 $0$。

## 复杂度分析

设单组数据长度为 $n$。

栈化简需要 $O(n)$ 时间。

Manacher 求最长奇回文半径需要 $O(m)$ 时间，其中 $m \le n$。

所以总时间复杂度为：

$O(n)$

空间复杂度为：

$O(n)$

所有测试数据的 $n$ 之和不超过 $400000$，复杂度可以通过。

## 代码实现

### Python

```python
import sys


def odd_manacher(arr):
    # 求整数数组 arr 的最长奇回文半径
    n = len(arr)
    d = [0] * n
    l, r = 0, -1
    ans = 0

    for i in range(n):
        # 初始化当前位置的半径
        if i > r:
            k = 1
        else:
            k = min(d[l + r - i], r - i + 1)

        # 向两边扩展
        while i - k >= 0 and i + k < n and arr[i - k] == arr[i + k]:
            k += 1

        d[i] = k
        ans = max(ans, k)

        # 更新当前最右回文区间
        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1

    return ans


def solve_one(n, c):
    stack = []

    # 用栈模拟原序列的全部消除
    for x in c:
        if stack and stack[-1] == x:
            stack.pop()
        else:
            stack.append(x)

    m = len(stack)

    # 原本已经可以消除的次数
    base = (n - m) // 2

    # 若已经全部消完，插入一个物品也不能产生新消除
    if m == 0:
        return base

    # 插入一次带来的最大额外消除次数
    extra = odd_manacher(stack)

    return base + extra


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        c = data[idx:idx + n]
        idx += n
        ans.append(str(solve_one(n, c)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 快速输入，适合本题较大的数据范围
    static class FastScanner {
        private final InputStream in = System.in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

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

    // 求整数数组 arr 的最长奇回文半径
    static int oddManacher(int[] arr, int n) {
        int[] d = new int[n];
        int l = 0, r = -1;
        int ans = 0;

        for (int i = 0; i < n; i++) {
            int k;

            // 初始化当前位置的半径
            if (i > r) {
                k = 1;
            } else {
                k = Math.min(d[l + r - i], r - i + 1);
            }

            // 向两边扩展
            while (i - k >= 0 && i + k < n && arr[i - k] == arr[i + k]) {
                k++;
            }

            d[i] = k;
            ans = Math.max(ans, k);

            // 更新当前最右回文区间
            if (i + k - 1 > r) {
                l = i - k + 1;
                r = i + k - 1;
            }
        }

        return ans;
    }

    static int solveOne(int n, int[] c) {
        int[] stack = new int[n];
        int top = 0;

        // 用栈模拟原序列的全部消除
        for (int i = 0; i < n; i++) {
            if (top > 0 && stack[top - 1] == c[i]) {
                top--;
            } else {
                stack[top++] = c[i];
            }
        }

        int m = top;

        // 原本已经可以消除的次数
        int base = (n - m) / 2;

        // 若已经全部消完，插入一个物品也不能产生新消除
        if (m == 0) {
            return base;
        }

        int[] reduced = Arrays.copyOf(stack, m);

        // 插入一次带来的最大额外消除次数
        int extra = oddManacher(reduced, m);

        return base + extra;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();

        for (int tc = 0; tc < T; tc++) {
            int n = fs.nextInt();
            int[] c = new int[n];

            for (int i = 0; i < n; i++) {
                c[i] = fs.nextInt();
            }

            sb.append(solveOne(n, c)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 求整数数组 arr 的最长奇回文半径
int oddManacher(const vector<int>& arr) {
    int n = arr.size();
    vector<int> d(n);
    int l = 0, r = -1;
    int ans = 0;

    for (int i = 0; i < n; i++) {
        int k;

        // 初始化当前位置的半径
        if (i > r) {
            k = 1;
        } else {
            k = min(d[l + r - i], r - i + 1);
        }

        // 向两边扩展
        while (i - k >= 0 && i + k < n && arr[i - k] == arr[i + k]) {
            k++;
        }

        d[i] = k;
        ans = max(ans, k);

        // 更新当前最右回文区间
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    return ans;
}

int solveOne(int n, const vector<int>& c) {
    vector<int> st;

    // 用栈模拟原序列的全部消除
    for (int x : c) {
        if (!st.empty() && st.back() == x) {
            st.pop_back();
        } else {
            st.push_back(x);
        }
    }

    int m = st.size();

    // 原本已经可以消除的次数
    int base = (n - m) / 2;

    // 若已经全部消完，插入一个物品也不能产生新消除
    if (m == 0) {
        return base;
    }

    // 插入一次带来的最大额外消除次数
    int extra = oddManacher(st);

    return base + extra;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<int> c(n);
        for (int i = 0; i < n; i++) {
            cin >> c[i];
        }

        cout << solveOne(n, c) << '\n';
    }

    return 0;
}
```