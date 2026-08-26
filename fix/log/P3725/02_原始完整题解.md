## 解题思路

我们可以多次选择当前数组中的某个数 `x`，把所有元素同时变为 `a_i xor x`。关键观察：

* 设经过若干次操作后，整体等价于把所有元素都异或了某个值 `g`。
* 若第一步选的是 `x=a_k`，则 `g=a_k`；第二步必须从新数组中选 `x'=a_j xor a_k`，于是新的整体异或量变为 `g'=a_k xor (a_j xor a_k)=a_j`；继续下去可证明**每一步后的整体异或量始终是原数组中的某个元素**。
* 因此，最终可达的数组恰为：`{a_i xor g}`，其中 `g ∈ {0} ∪ {a_1,…,a_n}`（允许不操作时 `g=0`）。

于是问题化简为：在有限候选集合 `G={0} ∪ {a_i}` 中，选择 `g` 最大化

$$
S(g)=\sum_{i=1}^n (a_i \oplus g).
$$

接下来做按位分析（位运算 + 贪心思想按位计贡献）：

* 记第 `b` 位上原数组有 `cnt1[b]` 个 1，`cnt0[b]=n-cnt1[b]` 个 0。
* 若 `g` 的第 `b` 位取 0，则该位的 1 的个数仍为 `cnt1[b]`；若取 1，则该位的 1 的个数变为 `cnt0[b]`。
* 令

  $$
  C1[b]=cnt1[b]\cdot 2^b,\quad C0[b]=cnt0[b]\cdot 2^b,\quad d[b]=C0[b]-C1[b]=(n-2\cdot cnt1[b])\cdot 2^b.
  $$

  则

  $$
  S(g)=\sum_b C1[b]+\sum_{b:\,g_b=1} d[b]=\underbrace{\sum_i a_i}_{\text{base}}+\sum_{b:\,g_b=1} d[b].
  $$
* 因而我们只需：

  1. 统计各位的 `cnt1[b]`，得到 `base=∑a_i` 与每一位的增益 `d[b]`；
  2. 枚举候选 `g`（即枚举每个 `a_i`，另外比较一次 `g=0`），将 `g` 的每个置位的 `d[b]` 相加，取最大即可。

位数最多到 `30`（因为 `a_i ≤ 1e9 < 2^30`），总复杂度为 `O(n·B)`，`B≈30`，完全可行。

算法要点总结：

* 结论化简：可达的 `g` 仅为 `0` 或原数组元素。
* 按位计贡献：预处理 `d[b]`，枚举候选 `g` 按其置位累加增益。
* 无需线性基、DP 等复杂结构，纯位运算与简单枚举即可。

## 复杂度分析

* 时间复杂度：对每组数据 `O(n·B)`，其中 `B≈30`。
* 空间复杂度：`O(B)` 统计位信息与增益，额外为常数级。

## 代码实现

### Python

```python
import sys

MAXB = 31  # 覆盖到第30位（包含），安全起见设为31位

def max_sum_after_xor(arr):
    n = len(arr)
    # 统计每一位的1的个数
    cnt1 = [0] * MAXB
    base = 0  # 原数组元素和
    for x in arr:
        base += x
        for b in range(MAXB):
            if (x >> b) & 1:
                cnt1[b] += 1

    # 计算每一位的增益 d[b]
    d = [0] * MAXB
    for b in range(MAXB):
        cnt0 = n - cnt1[b]
        d[b] = (cnt0 - cnt1[b]) * (1 << b)  # (n - 2*cnt1) * 2^b

    # 枚举 g=0 与 g∈arr
    ans = base  # g=0 的情况
    for x in arr:
        cur = base
        # x 的每个置位叠加对应的增益
        for b in range(MAXB):
            if (x >> b) & 1:
                cur += d[b]
        if cur > ans:
            ans = cur
    return ans

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out_lines = []
    for _ in range(T):
        n = next(it)
        arr = [next(it) for _ in range(n)]
        out_lines.append(str(max_sum_after_xor(arr)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    // 为安全覆盖到第30位（含），设31位
    static final int MAXB = 31;

    // 题意功能函数：给定数组，返回最大和
    static long maxSumAfterXor(int[] arr) {
        int n = arr.length;
        int[] cnt1 = new int[MAXB]; // 每一位1的个数
        long base = 0L;             // 原数组元素和
        for (int x : arr) {
            base += x;
            for (int b = 0; b < MAXB; b++) {
                if (((x >> b) & 1) == 1) cnt1[b]++;
            }
        }
        long[] d = new long[MAXB]; // 每位增益
        for (int b = 0; b < MAXB; b++) {
            int cnt0 = n - cnt1[b];
            d[b] = (long)(cnt0 - cnt1[b]) << b; // (n - 2*cnt1) * 2^b
        }

        long ans = base; // g=0
        for (int x : arr) {
            long cur = base;
            for (int b = 0; b < MAXB; b++) {
                if (((x >> b) & 1) == 1) cur += d[b];
            }
            if (cur > ans) ans = cur;
        }
        return ans;
    }

    // 简洁快速输入（根据数据规模选择了字节流快读）
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
            int c, sgn = 1, val = 0;
            do { c = read(); } while (c <= ' '); // 跳过空白
            if (c == '-') { sgn = -1; c = read(); }
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }
            return val * sgn;
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();
        int T = fs.nextInt();
        for (int t = 0; t < T; t++) {
            int n = fs.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = fs.nextInt();
            long ans = maxSumAfterXor(arr);
            sb.append(ans).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

static const int MAXB = 31; // 覆盖到第30位（含）

// 题意功能函数：返回最大可能的数组元素和
long long maxSumAfterXor(const vector<int>& arr) {
    int n = (int)arr.size();
    long long base = 0;            // 原数组元素和
    int cnt1[MAXB] = {0};          // 每一位1的个数

    for (int x : arr) {
        base += x;
        for (int b = 0; b < MAXB; ++b) {
            if ((x >> b) & 1) cnt1[b]++;
        }
    }

    long long d[MAXB];             // 每一位的增益
    for (int b = 0; b < MAXB; ++b) {
        int cnt0 = n - cnt1[b];
        d[b] = 1LL * (cnt0 - cnt1[b]) << b; // (n - 2*cnt1) * 2^b
    }

    long long ans = base;          // g=0
    for (int x : arr) {
        long long cur = base;
        for (int b = 0; b < MAXB; ++b) {
            if ((x >> b) & 1) cur += d[b];
        }
        if (cur > ans) ans = cur;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        cin >> n;
        vector<int> arr(n);
        for (int i = 0; i < n; ++i) cin >> arr[i];
        cout << maxSumAfterXor(arr) << "\n";
    }
    return 0;
}
```