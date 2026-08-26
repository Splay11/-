## 解题思路

设 $p$ 为不超过 $M$ 的最大 $2$ 的幂，即 $p=2^m$，则 $p\le M<2p$。

一次操作可以让某个 $a_i$ 异或上一个 $x$，其中 $0\le x\le M$。多次操作等价于让 $a_i$ 异或上若干个 $x$ 的异或值。

由于 $0,1,\dots,M$ 中一定包含 $0,1,\dots,p-1$ 和 $p$，所以对于任意 $0\le y<2p$：

* 若 $y\le M$，可以直接操作一次，代价为 $y$；
* 若 $y>M$，则 $y=p+u$，其中 $0\le u<p$，可以先异或 $p$，再异或 $u$，总代价为 $p+u=y$。

因此，对于低 $m+1$ 位，我们可以任意改变，且把某个低位状态从 $s$ 改成 $t$ 的最小代价就是 $s\oplus t$。

目标函数为：

$\sum_{i=1}^{n}\sum_{j=i+1}^{n} a_i\oplus a_j$

异或和可以按位独立计算。对于某一位，若最终有 $cnt$ 个 $1$，则这一位对答案的贡献为：

$cnt\times(n-cnt)\times 2^b$

显然当 $cnt$ 尽量接近 $\frac n2$ 时最大，即最大贡献为：

$\left\lfloor \frac{n^2}{4} \right\rfloor \times 2^b$

对于可修改的低 $m+1$ 位，每一位都可以单独调整到最优数量。

同时，为了总代价最小：

* 若 $n$ 为偶数，每一位最终必须有 $\frac n2$ 个 $1$；
* 若 $n$ 为奇数，每一位最终可以有 $\lfloor\frac n2\rfloor$ 或 $\lceil\frac n2\rceil$ 个 $1$；
* 当前这一位有 $cnt$ 个 $1$，所需最小翻转次数就是到目标数量的最小差值；
* 每翻转这一位一次，代价为 $2^b$。

高于 $m+1$ 的位无法被操作改变，直接按原数组统计贡献即可。

## 复杂度分析

设值域位数为 $B=30$。

时间复杂度为 $O(nB)$，只需要统计每一位的 $1$ 的数量。

空间复杂度为 $O(1)$，除输入数组外只使用常数额外空间。

## 代码实现

### Python

```python
import sys


def solve(n, k, a):
    # p 是不超过 M 的最大 2 的幂
    p = 1
    while (p << 1) <= k:
        p <<= 1

    # low_bits 表示可以任意改变的低位数量
    low_bits = p.bit_length()

    max_sum = 0
    min_cost = 0

    # 题目中 ai 和 M 都小于 2^30
    for b in range(30):
        bit = 1 << b
        cnt = 0

        # 统计第 b 位为 1 的个数
        for x in a:
            if x & bit:
                cnt += 1

        if b < low_bits:
            # 这一位可以被操作改变，最大贡献为尽量均分
            max_sum += (n // 2) * ((n + 1) // 2) * bit

            # 为了达到最大值，计算最少需要翻转多少个数的这一位
            if n % 2 == 0:
                target = n // 2
                flips = abs(cnt - target)
            else:
                target1 = n // 2
                target2 = n // 2 + 1
                flips = min(abs(cnt - target1), abs(cnt - target2))

            min_cost += flips * bit
        else:
            # 这一位无法改变，直接计算原始贡献
            max_sum += cnt * (n - cnt) * bit

    return max_sum, min_cost


def main():
    data = list(map(int, sys.stdin.read().split()))
    n, k = data[0], data[1]
    a = data[2:2 + n]

    ans, cost = solve(n, k, a)
    print(ans, cost)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    // 题目功能写在外部函数中
    static long[] solve(int n, int k, int[] a) {
        // p 是不超过 M 的最大 2 的幂
        int p = 1;
        while ((p << 1) > 0 && (p << 1) <= k) {
            p <<= 1;
        }

        // lowBits 表示可以任意改变的低位数量
        int lowBits = 0;
        int temp = p;
        while (temp > 0) {
            lowBits++;
            temp >>= 1;
        }

        long maxSum = 0;
        long minCost = 0;

        // 题目中 ai 和 M 都小于 2^30
        for (int b = 0; b < 30; b++) {
            int bit = 1 << b;
            int cnt = 0;

            // 统计第 b 位为 1 的个数
            for (int x : a) {
                if ((x & bit) != 0) {
                    cnt++;
                }
            }

            if (b < lowBits) {
                // 这一位可以被操作改变，最大贡献为尽量均分
                maxSum += 1L * (n / 2) * ((n + 1) / 2) * bit;

                // 为了达到最大值，计算最少需要翻转多少个数的这一位
                int flips;
                if (n % 2 == 0) {
                    int target = n / 2;
                    flips = Math.abs(cnt - target);
                } else {
                    int target1 = n / 2;
                    int target2 = n / 2 + 1;
                    flips = Math.min(Math.abs(cnt - target1), Math.abs(cnt - target2));
                }

                minCost += 1L * flips * bit;
            } else {
                // 这一位无法改变，直接计算原始贡献
                maxSum += 1L * cnt * (n - cnt) * bit;
            }
        }

        return new long[]{maxSum, minCost};
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int k = sc.nextInt();

        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }

        long[] ans = solve(n, k, a);
        System.out.println(ans[0] + " " + ans[1]);

        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 题目功能写在外部函数中
pair<long long, long long> solve(int n, int k, vector<int>& a) {
    // p 是不超过 M 的最大 2 的幂
    int p = 1;
    while ((p << 1) <= k) {
        p <<= 1;
    }

    // lowBits 表示可以任意改变的低位数量
    int lowBits = 0;
    int temp = p;
    while (temp > 0) {
        lowBits++;
        temp >>= 1;
    }

    long long maxSum = 0;
    long long minCost = 0;

    // 题目中 ai 和 M 都小于 2^30
    for (int b = 0; b < 30; b++) {
        int bit = 1 << b;
        int cnt = 0;

        // 统计第 b 位为 1 的个数
        for (int x : a) {
            if (x & bit) {
                cnt++;
            }
        }

        if (b < lowBits) {
            // 这一位可以被操作改变，最大贡献为尽量均分
            maxSum += 1LL * (n / 2) * ((n + 1) / 2) * bit;

            // 为了达到最大值，计算最少需要翻转多少个数的这一位
            int flips;
            if (n % 2 == 0) {
                int target = n / 2;
                flips = abs(cnt - target);
            } else {
                int target1 = n / 2;
                int target2 = n / 2 + 1;
                flips = min(abs(cnt - target1), abs(cnt - target2));
            }

            minCost += 1LL * flips * bit;
        } else {
            // 这一位无法改变，直接计算原始贡献
            maxSum += 1LL * cnt * (n - cnt) * bit;
        }
    }

    return {maxSum, minCost};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    pair<long long, long long> ans = solve(n, k, a);
    cout << ans.first << " " << ans.second << '\n';

    return 0;
}
```