## 解题思路

使用哈希表 + 枚举二元组的算法。

将四元组 $(i,j,p,q)$ 拆成两部分：

* 左边一对下标 $(i,j)$，满足 $i<j<p$
* 右边一对下标 $(p,q)$，满足 $p<q$

原条件为：

$a_i \oplus a_j \oplus a_p \oplus a_q = k$

移项可得：

$a_i \oplus a_j = k \oplus a_p \oplus a_q$

因此可以从左到右枚举第三个下标 $p$：

1. 用哈希表 $cnt$ 维护所有满足 $i<j<p$ 的二元组异或值 $a_i \oplus a_j$ 的出现次数。
2. 枚举 $q>p$，计算需要的左侧异或值 $need=k\oplus a_p\oplus a_q$。
3. 将 $cnt[need]$ 加入答案。
4. 当前 $p$ 处理完后，把所有 $(i,p)$ 加入哈希表，供后续位置使用。

因为哈希表中只保存 $j<p$ 的二元组，所以天然保证四个下标两两不同且满足 $i<j<p<q$，不会重复计数。

## 复杂度分析

设数组长度为 $n$。

时间复杂度为 $O(n^2)$，因为每个测试数据中枚举了两类二元组。

空间复杂度为 $O(n^2)$，哈希表中最多存储 $O(n^2)$ 个二元组异或值。

由于所有测试数据中 $\sum n \le 4\times 10^3$，该复杂度可以通过。

## 代码实现

### Python

```python
import sys


def count_quadruples(a, k):
    n = len(a)
    cnt = {}
    ans = 0

    # 枚举第三个下标 p
    for p in range(n):
        # 枚举第四个下标 q
        for q in range(p + 1, n):
            # 需要左侧某个二元组异或值等于 need
            need = k ^ a[p] ^ a[q]
            ans += cnt.get(need, 0)

        # 将所有 (i, p) 加入哈希表，供后面的 p 使用
        for i in range(p):
            x = a[i] ^ a[p]
            cnt[x] = cnt.get(x, 0) + 1

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    res = []

    for _ in range(t):
        n = data[idx]
        k = data[idx + 1]
        idx += 2

        a = data[idx:idx + n]
        idx += n

        res.append(str(count_quadruples(a, k)))

    print("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {

    // 统计满足条件的四元组数量
    static long countQuadruples(int[] a, int k) {
        int n = a.length;
        Map<Integer, Long> cnt = new HashMap<>();
        long ans = 0;

        // 枚举第三个下标 p
        for (int p = 0; p < n; p++) {
            // 枚举第四个下标 q
            for (int q = p + 1; q < n; q++) {
                // 需要左侧某个二元组异或值等于 need
                int need = k ^ a[p] ^ a[q];
                ans += cnt.getOrDefault(need, 0L);
            }

            // 将所有 (i, p) 加入哈希表，供后面的 p 使用
            for (int i = 0; i < p; i++) {
                int x = a[i] ^ a[p];
                cnt.put(x, cnt.getOrDefault(x, 0L) + 1);
            }
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        for (int tc = 0; tc < T; tc++) {
            int n = sc.nextInt();
            int k = sc.nextInt();

            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = sc.nextInt();
            }

            sb.append(countQuadruples(a, k)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 统计满足条件的四元组数量
long long countQuadruples(vector<int>& a, int k) {
    int n = a.size();
    unordered_map<int, long long> cnt;
    cnt.reserve(n * n);

    long long ans = 0;

    // 枚举第三个下标 p
    for (int p = 0; p < n; p++) {
        // 枚举第四个下标 q
        for (int q = p + 1; q < n; q++) {
            // 需要左侧某个二元组异或值等于 need
            int need = k ^ a[p] ^ a[q];
            if (cnt.count(need)) {
                ans += cnt[need];
            }
        }

        // 将所有 (i, p) 加入哈希表，供后面的 p 使用
        for (int i = 0; i < p; i++) {
            int x = a[i] ^ a[p];
            cnt[x]++;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;

        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << countQuadruples(a, k) << '\n';
    }

    return 0;
}
```