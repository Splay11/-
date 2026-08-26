## 解题思路

每次操作可以选择一个大于 $1$ 的数 $a_i$，把它除以一个素因子 $p$。设当前数为 $x$，这次操作后变成 $\dfrac{x}{p}$，数组总和减少了：

$$
x-\frac{x}{p}=x\left(1-\frac{1}{p}\right)
$$

为了让总和尽量小，每一步都应选择“当前能带来最大减少量”的操作。

对于一个数 $x$，若要让 $\dfrac{x}{p}$ 尽量小，就应除以它的最小素因子。因为 $p$ 越小，$\dfrac{x}{p}$ 越小，减少量越大。
所以一个数后续的最优操作序列其实已经确定：不断除以当前数的最小素因子。

这样问题就变成：

* 初始和为所有元素之和；
* 每个数可以不断产生若干次“收益”（本次操作能减少多少）；
* 总共最多取 $k$ 次收益；
* 每次都取当前最大的收益即可。

这就是一个典型的“贪心 + 优先队列”问题。

### 实现方法

1. 先用埃氏筛的思想预处理 $1\sim 10^6$ 每个数的最小素因子。
2. 把所有 $a_i$ 加入总和。
3. 对每个 $a_i>1$，计算它第一次操作的减少量：
   $$
   a_i-\frac{a_i}{\operatorname{spf}(a_i)}
   $$
   放入大根堆。
4. 每次从堆中取出当前减少量最大的操作：

   * 从答案中减去这次减少量；
   * 更新这个数为除以最小素因子后的新值；
   * 若新值仍大于 $1$，计算它下一次操作的减少量，再放回堆中。
5. 重复最多 $k$ 次，或堆空为止。

因为每次都选当前最优操作，所以贪心正确。

## 复杂度分析

设所有元素一共实际能进行的操作次数为 $m$，显然最多执行 $\min(k,m)$ 次。

* 预处理最小素因子时间复杂度为 $O(M\log\log M)$ 或近似看作 $O(M)$，其中 $M=10^6$
* 每次堆操作复杂度为 $O(\log n)$
* 总操作次数最多为 $k$

所以总时间复杂度为：

$$
O(M + k\log n)
$$

空间复杂度为：

$$
O(M+n)
$$

其中 $M=10^6$，在题目范围内完全可行。

## 代码实现

### Python

```python
import sys
import heapq


# 计算操作后的最小数组总和
def solve(n, k, a):
    mx = max(a)

    # 最小素因子筛
    spf = list(range(mx + 1))
    for i in range(2, int(mx ** 0.5) + 1):
        if spf[i] == i:  # i 是质数
            for j in range(i * i, mx + 1, i):
                if spf[j] == j:
                    spf[j] = i

    total = sum(a)
    heap = []

    # 堆中存 (-减少量, 当前值)
    for x in a:
        if x > 1:
            p = spf[x]
            dec = x - x // p
            heapq.heappush(heap, (-dec, x))

    # 贪心执行最多 k 次操作
    for _ in range(k):
        if not heap:
            break

        dec, x = heapq.heappop(heap)
        dec = -dec
        total -= dec  # 减去本次收益

        # 更新当前数
        x //= spf[x]

        # 如果还能继续操作，则加入下一次收益
        if x > 1:
            p = spf[x]
            nxt_dec = x - x // p
            heapq.heappush(heap, (-nxt_dec, x))

    return total


def main():
    data = list(map(int, sys.stdin.read().split()))
    n, k = data[0], data[1]
    a = data[2:2 + n]
    print(solve(n, k, a))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedInputStream;
import java.util.PriorityQueue;

public class Main {

    // 堆中保存当前值和本次操作的减少量
    static class Node {
        int x;
        int dec;

        Node(int x, int dec) {
            this.x = x;
            this.dec = dec;
        }
    }

    // 计算操作后的最小数组总和
    static long solve(int n, int k, int[] a) {
        int mx = 0;
        for (int x : a) {
            mx = Math.max(mx, x);
        }

        // 最小素因子筛
        int[] spf = new int[mx + 1];
        for (int i = 0; i <= mx; i++) {
            spf[i] = i;
        }
        for (int i = 2; i * i <= mx; i++) {
            if (spf[i] == i) { // i 是质数
                for (int j = i * i; j <= mx; j += i) {
                    if (spf[j] == j) {
                        spf[j] = i;
                    }
                }
            }
        }

        long total = 0;
        for (int x : a) {
            total += x;
        }

        // 大根堆：减少量大的优先
        PriorityQueue<Node> pq = new PriorityQueue<>((o1, o2) -> o2.dec - o1.dec);

        // 初始化每个数的第一次操作收益
        for (int x : a) {
            if (x > 1) {
                int p = spf[x];
                int dec = x - x / p;
                pq.offer(new Node(x, dec));
            }
        }

        // 贪心执行最多 k 次操作
        for (int i = 0; i < k; i++) {
            if (pq.isEmpty()) {
                break;
            }

            Node cur = pq.poll();
            total -= cur.dec; // 减去本次收益

            // 当前数更新为除以最小素因子后的值
            int nx = cur.x / spf[cur.x];

            // 若还能继续操作，计算下一次收益再入堆
            if (nx > 1) {
                int p = spf[nx];
                int dec = nx - nx / p;
                pq.offer(new Node(nx, dec));
            }
        }

        return total;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        int n = fs.nextInt();
        int k = fs.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = fs.nextInt();
        }
        System.out.println(solve(n, k, a));
    }

    // 根据数据范围使用快读
    static class FastScanner {
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        private final BufferedInputStream in = new BufferedInputStream(System.in);

        private int read() throws Exception {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) {
                    return -1;
                }
            }
            return buffer[ptr++];
        }

        int nextInt() throws Exception {
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
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

// 堆中保存当前值和本次操作的减少量
struct Node {
    int x;
    int dec;

    // 大根堆，减少量大的优先
    bool operator < (const Node& other) const {
        return dec < other.dec;
    }
};

// 计算操作后的最小数组总和
long long solve(int n, int k, vector<int>& a) {
    int mx = *max_element(a.begin(), a.end());

    // 最小素因子筛
    vector<int> spf(mx + 1);
    for (int i = 0; i <= mx; i++) {
        spf[i] = i;
    }
    for (int i = 2; i * i <= mx; i++) {
        if (spf[i] == i) { // i 是质数
            for (int j = i * i; j <= mx; j += i) {
                if (spf[j] == j) {
                    spf[j] = i;
                }
            }
        }
    }

    long long total = 0;
    for (int x : a) {
        total += x;
    }

    priority_queue<Node> pq;

    // 初始化每个数的第一次操作收益
    for (int x : a) {
        if (x > 1) {
            int p = spf[x];
            int dec = x - x / p;
            pq.push({x, dec});
        }
    }

    // 贪心执行最多 k 次操作
    for (int i = 0; i < k; i++) {
        if (pq.empty()) {
            break;
        }

        Node cur = pq.top();
        pq.pop();

        total -= cur.dec; // 减去本次收益

        // 当前数更新为除以最小素因子后的值
        int nx = cur.x / spf[cur.x];

        // 若还能继续操作，计算下一次收益再入堆
        if (nx > 1) {
            int p = spf[nx];
            int dec = nx - nx / p;
            pq.push({nx, dec});
        }
    }

    return total;
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

    cout << solve(n, k, a) << '\n';
    return 0;
}
```