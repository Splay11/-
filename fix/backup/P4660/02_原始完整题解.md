## 解题思路

对于第 $i$ 种糖果，共有 $c_i$ 个，要分给 $k$ 个小朋友，并且要求这种糖果在任意两个小朋友之间的数量差不超过 $1$。

这说明第 $i$ 种糖果的分法是唯一确定的：

* 每个小朋友至少得到 $\left\lfloor \dfrac{c_i}{k} \right\rfloor$ 个；
* 还剩下 $c_i \bmod k$ 个糖果，这些糖果各自再分给 $c_i \bmod k$ 个不同的小朋友，每人多拿 $1$ 个。

所以，对于任选的某一个小朋友来说，第 $i$ 种糖果可能得到的数量只有两种：

* 最少：$\left\lfloor \dfrac{c_i}{k} \right\rfloor$
* 最多：$\left\lceil \dfrac{c_i}{k} \right\rceil$

并且每一种糖果的分配彼此独立，因此：

* 这个小朋友的最小总数，就是所有种类的下取整之和；
* 这个小朋友的最大总数，就是所有种类的上取整之和。

实现时可以这样写：

* 设 $q_i = c_i \div k$，$r_i = c_i \bmod k$
* 最小值累加 $q_i$
* 最大值累加 $q_i + [r_i > 0]$

这里用到的算法本质上是一次遍历统计，也可以看成简单的数学贪心分析。

## 复杂度分析

对于每组测试数据，只需要遍历一次数组 $c$：

* 时间复杂度：$O(n)$
* 空间复杂度：$O(1)$（不计输入存储）

题目保证所有测试数据的 $n$ 之和不超过 $5 \times 10^5$，这样的复杂度完全可以通过。

## 代码实现

### Python

```python
import sys


# 计算单个小朋友可能得到的糖果总数最小值和最大值
def solve_case(n, k, c):
    mn = 0
    mx = 0
    for x in c:
        q = x // k
        r = x % k
        mn += q               # 最少只能拿到下取整
        mx += q + (1 if r > 0 else 0)  # 有余数时，最多可以多拿 1 个
    return mn, mx


def main():
    data = list(map(int, sys.stdin.read().split()))
    t = data[0]
    idx = 1
    ans = []

    for _ in range(t):
        n = data[idx]
        k = data[idx + 1]
        idx += 2
        c = data[idx:idx + n]
        idx += n

        mn, mx = solve_case(n, k, c)
        ans.append(f"{mn} {mx}")

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedInputStream;
import java.io.IOException;

public class Main {

    // 计算单个小朋友可能得到的糖果总数最小值和最大值
    static long[] solveCase(int n, long k, long[] c) {
        long mn = 0;
        long mx = 0;

        for (int i = 0; i < n; i++) {
            long q = c[i] / k;
            long r = c[i] % k;
            mn += q;                  // 最少只能拿到下取整
            mx += q + (r > 0 ? 1 : 0); // 有余数时，最多可以多拿 1 个
        }

        return new long[]{mn, mx};
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();

        int T = fs.nextInt();
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int n = fs.nextInt();
            long k = fs.nextLong();
            long[] c = new long[n];

            for (int i = 0; i < n; i++) {
                c[i] = fs.nextLong();
            }

            long[] res = solveCase(n, k, c);
            sb.append(res[0]).append(" ").append(res[1]).append("\n");
        }

        System.out.print(sb.toString());
    }

    // 简单快读，适合本题数据范围
    static class FastScanner {
        private final BufferedInputStream in = new BufferedInputStream(System.in);
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) {
                    return -1;
                }
            }
            return buffer[ptr++];
        }

        int nextInt() throws IOException {
            return (int) nextLong();
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
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 计算单个小朋友可能得到的糖果总数最小值和最大值
pair<long long, long long> solve_case(int n, long long k, const vector<long long>& c) {
    long long mn = 0;
    long long mx = 0;

    for (int i = 0; i < n; i++) {
        long long q = c[i] / k;
        long long r = c[i] % k;
        mn += q;                 // 最少只能拿到下取整
        mx += q + (r > 0 ? 1 : 0); // 有余数时，最多可以多拿 1 个
    }

    return {mn, mx};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        long long k;
        cin >> n >> k;

        vector<long long> c(n);
        for (int i = 0; i < n; i++) {
            cin >> c[i];
        }

        pair<long long, long long> res = solve_case(n, k, c);
        cout << res.first << " " << res.second << '\n';
    }

    return 0;
}
```