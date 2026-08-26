## 解题思路

采用贪心算法与排序。

假设当前有两个可操作的数，满足 $x\ge y>1$：

* 将 $x$ 减一，乘积变为原来的 $\frac{x-1}{x}$；
* 将 $y$ 减一，乘积变为原来的 $\frac{y-1}{y}$。

由于 $\frac{x-1}{x}\ge\frac{y-1}{y}$，所以每次将当前最大的数减一，乘积损失最小。

因此，最优策略是不断降低最大的元素，使较大的若干元素逐渐相等。直接执行 $k$ 次可能超时，可以排序后批量处理：

1. 将数组从小到大排序。

2. 从最大值开始，维护当前被一起降低的元素数量 $cnt$ 和它们的值 $level$。

3. 将这 $cnt$ 个元素全部降低到下一个较小值，需要的操作次数为：

   $$
   (level-a_i)\times cnt
   $$

4. 若剩余操作次数足够，则整体降低并扩大处理范围。

5. 否则，设：

   $$
   q=\left\lfloor\frac{k}{cnt}\right\rfloor,\qquad r=k\bmod cnt
   $$

   最终有 $cnt-r$ 个元素等于 $level-q$，有 $r$ 个元素等于 $level-q-1$。

6. 若 $k\ge\sum(a_i-1)$，所有元素最终都会变成 $1$，答案为 $1$。

乘积使用模快速幂计算，并对 $10^9+7$ 取模。

## 复杂度分析

每组数据需要排序，时间复杂度为 $O(n\log n)$。

计算最终乘积需要 $O(n)$，因此总时间复杂度为 $O(n\log n)$。

排序数组需要 $O(n)$ 的空间，空间复杂度为 $O(n)$。

## 代码实现

### Python

```python
import sys

MOD = 1000000007


def max_product(a, k):
    """计算执行操作后的最大乘积"""
    a.sort()
    n = len(a)

    # 所有元素最多能够减少的总次数
    total = sum(x - 1 for x in a)
    if k >= total:
        return 1

    level = a[-1]
    cnt = 1

    # 从大到小批量降低较大的元素
    for i in range(n - 2, -1, -1):
        cost = (level - a[i]) * cnt

        if k >= cost:
            k -= cost
            level = a[i]
            cnt += 1
        else:
            q, r = divmod(k, cnt)
            high = level - q

            ans = 1

            # 前面的元素保持不变
            for j in range(i + 1):
                ans = ans * a[j] % MOD

            # 当前最大的 cnt 个元素只相差一
            ans = ans * pow(high, cnt - r, MOD) % MOD
            ans = ans * pow(high - 1, r, MOD) % MOD
            return ans

    # 所有元素已经被降低到相同值
    q, r = divmod(k, n)
    high = level - q

    ans = pow(high, n - r, MOD)
    ans = ans * pow(high - 1, r, MOD) % MOD
    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    T = data[pos]
    pos += 1
    answers = []

    for _ in range(T):
        n = data[pos]
        k = data[pos + 1]
        pos += 2

        a = data[pos:pos + n]
        pos += n

        answers.append(str(max_product(a, k)))

    print("\n".join(answers))


if __name__ == "__main__":
    main()
```

### c++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const long long MOD = 1000000007LL;

// 模快速幂
long long modPow(long long base, long long exp) {
    long long result = 1;
    base %= MOD;

    while (exp > 0) {
        if (exp & 1LL) {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        exp >>= 1LL;
    }

    return result;
}

// 计算执行操作后的最大乘积
long long maxProduct(vector<long long>& a, long long k) {
    sort(a.begin(), a.end());
    int n = (int)a.size();

    // 所有元素最多能够减少的总次数
    long long total = 0;
    for (long long value : a) {
        total += value - 1;
    }

    if (k >= total) {
        return 1;
    }

    long long level = a[n - 1];
    long long cnt = 1;

    // 从大到小批量降低较大的元素
    for (int i = n - 2; i >= 0; i--) {
        long long cost = (level - a[i]) * cnt;

        if (k >= cost) {
            k -= cost;
            level = a[i];
            cnt++;
        } else {
            long long q = k / cnt;
            long long r = k % cnt;
            long long high = level - q;

            long long ans = 1;

            // 前面的元素保持不变
            for (int j = 0; j <= i; j++) {
                ans = ans * (a[j] % MOD) % MOD;
            }

            // 当前最大的 cnt 个元素只相差一
            ans = ans * modPow(high, cnt - r) % MOD;
            ans = ans * modPow(high - 1, r) % MOD;
            return ans;
        }
    }

    // 所有元素已经被降低到相同值
    long long q = k / n;
    long long r = k % n;
    long long high = level - q;

    long long ans = modPow(high, n - r);
    ans = ans * modPow(high - 1, r) % MOD;
    return ans;
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

        vector<long long> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << maxProduct(a, k) << '\n';
    }

    return 0;
}
```


### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static final long MOD = 1000000007L;

    // 模快速幂
    static long modPow(long base, long exp) {
        long result = 1;
        base %= MOD;

        while (exp > 0) {
            if ((exp & 1) == 1) {
                result = result * base % MOD;
            }
            base = base * base % MOD;
            exp >>= 1;
        }

        return result;
    }

    // 计算执行操作后的最大乘积
    static long maxProduct(long[] a, long k) {
        Arrays.sort(a);
        int n = a.length;

        // 所有元素最多能够减少的总次数
        long total = 0;
        for (long value : a) {
            total += value - 1;
        }

        if (k >= total) {
            return 1;
        }

        long level = a[n - 1];
        long cnt = 1;

        // 从大到小批量降低较大的元素
        for (int i = n - 2; i >= 0; i--) {
            long cost = (level - a[i]) * cnt;

            if (k >= cost) {
                k -= cost;
                level = a[i];
                cnt++;
            } else {
                long q = k / cnt;
                long r = k % cnt;
                long high = level - q;

                long ans = 1;

                // 前面的元素保持不变
                for (int j = 0; j <= i; j++) {
                    ans = ans * (a[j] % MOD) % MOD;
                }

                // 当前最大的 cnt 个元素只相差一
                ans = ans * modPow(high, cnt - r) % MOD;
                ans = ans * modPow(high - 1, r) % MOD;
                return ans;
            }
        }

        // 所有元素已经被降低到相同值
        long q = k / n;
        long r = k % n;
        long high = level - q;

        long ans = modPow(high, n - r);
        ans = ans * modPow(high - 1, r) % MOD;
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(
                new InputStreamReader(System.in)
        );

        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder answer = new StringBuilder();

        for (int test = 0; test < T; test++) {
            StringTokenizer st = new StringTokenizer(br.readLine());

            int n = Integer.parseInt(st.nextToken());
            long k = Long.parseLong(st.nextToken());

            long[] a = new long[n];
            int index = 0;

            // 读取当前测试的 n 个元素
            while (index < n) {
                st = new StringTokenizer(br.readLine());

                while (st.hasMoreTokens() && index < n) {
                    a[index++] = Long.parseLong(st.nextToken());
                }
            }

            answer.append(maxProduct(a, k)).append('\n');
        }

        System.out.print(answer);
    }
}
```