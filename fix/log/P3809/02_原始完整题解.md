## 解题思路

给定长度为 $n$ 的数组 $a_1,\dots,a_n$ 与被染成红色的下标序列 $b_1,\dots,b_k$（两两不同，1 基下标）。要求所有未被染红元素的和。

核心想法：
先求整个数组元素和 `total`，再把被染红位置上的值逐一减去，即答案为

$$
\text{ans}=\sum_{i=1}^{n} a_i-\sum_{j=1}^{k} a_{b_j}.
$$

由于下标互不相同，不会出现重复减的问题。实现时将数组存成 1 基下标，读取 $k$ 个下标时直接访问并扣减即可。

注意：数值范围可能达到 $2\times10^5 \times 10^9$，总和需使用 64 位整型（Python 自然支持大整数，Java 用 `long`，C++ 用 `long long`）。

## 复杂度分析

* 时间复杂度：$O(n+k)$。一次求和 + 扣掉 $k$ 个位置。
* 空间复杂度：$O(n)$。需要存储数组以便按下标访问（也可视为额外 $O(1)$ 临时空间）。

## 代码实现

### Python

```python
import sys

# 功能函数：计算未染色元素之和
def sum_uncolored(a, idxs):
    total = sum(a)  # 整体求和
    for pos in idxs:  # 减去被染红的元素
        total -= a[pos - 1]  # 输入为1基下标，列表为0基
    return total

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it)); k = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    b = [int(next(it)) for _ in range(k)]
    ans = sum_uncolored(a, b)
    print(ans)

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {

    // 功能函数：计算未染色元素之和（a 为 1 基数组）
    public static long solve(long[] a, int[] b, int n, int k) {
        long total = 0L;
        for (int i = 1; i <= n; i++) total += a[i]; // 整体求和
        for (int i = 0; i < k; i++) total -= a[b[i]]; // 减去被染红的元素
        return total;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读 n 和 k
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        // 读数组 a（1 基下标）
        long[] a = new long[n + 1];
        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) {
            a[i] = Long.parseLong(st.nextToken());
        }

        // 读被染红的下标
        int[] b = new int[k];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < k; i++) {
            b[i] = Integer.parseInt(st.nextToken());
        }

        long ans = solve(a, b, n, k);
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 功能函数：计算未染色元素之和（a 为 1 基数组）
long long solve(const vector<long long>& a, const vector<int>& b, int n, int k) {
    long long total = 0;
    for (int i = 1; i <= n; ++i) total += a[i];      // 整体求和
    for (int i = 0; i < k; ++i) total -= a[b[i]];    // 减去被染红的元素
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    if (!(cin >> n >> k)) return 0;

    // 读数组 a（1 基下标）
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];

    // 读被染红的下标
    vector<int> b(k);
    for (int i = 0; i < k; ++i) cin >> b[i];

    long long ans = solve(a, b, n, k);
    cout << ans << "\n";
    return 0;
}
```