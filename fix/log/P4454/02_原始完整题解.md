## 解题思路

* 把 1…N 的数按模 d 的余数分组。若两张卡余数分别为 `r` 与 `d−r`（含 0 与 d/2 的自配对），它们之和能被 d 整除。
* 问题等价于：求一个最大规模的集合 **α(N,d)**，使得集合中任意两数之和都 **不能** 被 d 整除；则答案 `K(N,d) = α(N,d) + 1`（抽屉原理）。
* 记 `q = ⌊N/d⌋`，`rem = N % d`。在 1…N 中：

  * 余数为 0 的数有 `q` 个；
  * 余数为 `1..rem` 的每个余数组有 `q+1` 个；
  * 余数为 `rem+1..d-1` 的每个余数组有 `q` 个。
* 构造最大集合的规则（贪心/计数）：

  * 余数 0（以及 d 为偶数时的余数 d/2）最多只能取 1 个；
  * 对每一对互补余数 `(r, d−r)`（1 ≤ r < d−r），只能从两边**择一整组**拿，且选数为该余数组的**全部个数**；于是该对贡献为 `max(cnt[r], cnt[d−r])`。
* 令 `p = ⌊(d−1)/2⌋` 为互补对的个数。除去 0 和（若存在）d/2 后，其余 p 对里：

  * 若某对中至少有一个余数落在 `1..rem`，该对贡献 `q+1`；否则贡献 `q`。
  * 这等价于统计区间并集的长度：
    `S1 = [1, min(rem, p)]` 与 `S2 = [max(1, d−rem), p]`。
    令 `A=|S1|，B=|S2|，C=|S1∩S2|`，则“贡献为 q+1 的对数” `W = A + B − C`。
* 于是

  * 互补对总贡献：`p * q + W`
  * 余数 0 的贡献：`min(1, q)`
  * 若 d 为偶数，余数 `d/2` 的个数为 `q + [d/2 ≤ rem]`，贡献 `min(1, 该个数)`
* 最终：`α = min(1,q) + p*q + W + (d 为偶数 ? min(1, q + [d/2 ≤ rem]) : 0)`，答案 `K = α + 1`。
  全过程 O(1) 计算，无需遍历余数（d 可达 1e18）。

## 复杂度分析

* 时间复杂度：每组数据 O(1)。
* 空间复杂度：O(1)。

## 代码实现

### Python

```python
# 题面功能封装在函数里，主函数只做输入输出

import sys

def solve_one(N: int, d: int) -> int:
    q = N // d
    rem = N % d
    p = (d - 1) // 2  # 互补对数量

    # 统计“至少有一端在 1..rem 内”的对数 W
    A = min(rem, p)  # S1 = [1, min(rem, p)]
    lower = max(1, d - rem)  # S2 = [lower, p]
    B = 0 if lower > p else (p - lower + 1)
    C = 0 if lower > rem else (min(p, rem) - lower + 1)
    W = A + B - C

    alpha = min(1, q) + p * q + W  # 互补对 + 余数0
    if d % 2 == 0:  # 余数 d/2
        mid_cnt = q + (1 if (d // 2) <= rem else 0)
        alpha += 1 if mid_cnt > 0 else 0

    return alpha + 1  # K = α + 1

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out_lines = []
    for _ in range(t):
        N = int(data[idx]); d = int(data[idx + 1]); idx += 2
        out_lines.append(str(solve_one(N, d)))
    print("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
// ACM 风格，类名 Main。使用快读以适应最大 2e5 组数据。
import java.io.*;
import java.util.*;

public class Main {
    // 计算单组答案的函数
    static long solveOne(long N, long d) {
        long q = N / d;
        long rem = N % d;
        long p = (d - 1) / 2; // 互补对数量

        // 统计 W：至少一端在 1..rem 的对数
        long A = Math.min(rem, p); // S1 = [1, min(rem, p)]
        long lower = Math.max(1L, d - rem); // S2 = [lower, p]
        long B = (lower > p) ? 0 : (p - lower + 1);
        long C = (lower > rem) ? 0 : (Math.min(p, rem) - lower + 1);
        long W = A + B - C;

        long alpha = Math.min(1L, q) + p * q + W; // 互补对 + 余数0
        if ((d & 1L) == 0) { // d 为偶数，处理余数 d/2
            long midCnt = q + (((d / 2) <= rem) ? 1 : 0);
            if (midCnt > 0) alpha += 1;
        }
        return alpha + 1; // K = α + 1
    }

    // 简单高效的输入
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
        long nextLong() throws IOException {
            int c; do { c = read(); } while (c <= ' '); // 跳过空白
            int sign = 1;
            if (c == '-') { sign = -1; c = read(); }
            long val = 0;
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }
            return val * sign;
        }
        int nextInt() throws IOException { return (int) nextLong(); }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int T = (int) fs.nextLong();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < T; i++) {
            long N = fs.nextLong();
            long d = fs.nextLong();
            sb.append(solveOne(N, d)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// ACM 风格，主函数读写，核心逻辑在 solveOne 外部函数中
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;

// 计算单组答案
static inline long long solveOne(long long N, long long d) {
    long long q = N / d;
    long long rem = N % d;
    long long p = (d - 1) / 2; // 互补对数量

    // 统计 W：至少一端在 1..rem 的对数
    long long A = min(rem, p);                // S1 = [1, min(rem, p)]
    long long lower = max(1LL, d - rem);      // S2 = [lower, p]
    long long B = (lower > p) ? 0 : (p - lower + 1);
    long long C = (lower > rem) ? 0 : (min(p, rem) - lower + 1);
    long long W = A + B - C;

    long long alpha = min(1LL, q) + p * q + W; // 互补对 + 余数0
    if ((d & 1LL) == 0) { // 处理余数 d/2
        long long midCnt = q + ((d / 2 <= rem) ? 1 : 0);
        if (midCnt > 0) alpha += 1;
    }
    return alpha + 1; // K = α + 1
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        long long N, d;
        cin >> N >> d;
        cout << solveOne(N, d) << "\n";
    }
    return 0;
}
```