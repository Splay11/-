## 思路

考虑对于每个查询，我们先二分找到最小的区间，满足 $k$ 中所有二进制位都存在，这个区间为 $[l, r_1]$

然后判断 $[l, r_1]$ 的区间或运算和是否为 $k$ 即可。

这里的二分中的 check 函数需要枚举 30 个二进制位。

所以我们需要先预处理出每个二进制位的前缀和，这样就可以 $O(1)$ 进行区间二进制位数量的查询。

时间复杂度为：$O(30q\log n)$

-------------
考虑如何优化。

考虑预处理出对于二进制位 $j$ ，对于每个下标 $i$ ，

找到大于等于 $i$ 的第一个下标 $next_i$ ，满足 $[i, next_i]$ 这个区间内的二进制位 $j$ 为 $1$ 的这个数量恰好为一。

这样，我们就可以将二分给优化掉。

预处理出这个 $next[i][j]$ 数组即可

时间复杂度：$O(30q)$

## 代码
### python
```python
n, q = map(int, input().split())
a = list(map(int, input().split()))

MAXBIT = 30
MAXV = 2**30 - 1
pre = [[0 for _ in range(MAXBIT)] for i in range(n + 1)]
for i in range(1, n + 1):
    for j in range(MAXBIT):
        pre[i][j] = pre[i - 1][j]
        if a[i - 1] >> j & 1:
            pre[i][j] += 1


for i in range(q):
    l, r, k = map(int, input().split())
    if k > MAXV:
        print(-1)
        continue

    kbit = [0] * MAXBIT
    for j in range(MAXBIT):
        kbit[j] = k >> j & 1

    left, right = l, r
    while left < right:
        mid = (left + right) >> 1
        ok = True
        for j in range(MAXBIT):
            if kbit[j] == 1 and pre[mid][j] - pre[l - 1][j] == 0:
                ok = False
                break
        if ok:
            right = mid
        else:
            left = mid + 1

    ok = True
    for j in range(MAXBIT):
        if kbit[j] == 1 and pre[right][j] - pre[l - 1][j] == 0:
            ok = False
            break
        if kbit[j] == 0 and pre[right][j] - pre[l - 1][j] > 0:
            ok = False
            break
    if ok:
        print(right)
    else:
        print(-1)

```


### c++
``` c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, q;
    cin >> n >> q;

    vector<long long> a(n); // 将a数组的类型改为long long
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    const int MAXBIT = 30;
    const long long MAXV = (1LL << 30) - 1; // 将MAXV的类型改为long long

    vector<vector<long long>> pre(n + 1, vector<long long>(MAXBIT, 0)); // 将pre数组的类型改为long long
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < MAXBIT; ++j) {
            pre[i][j] = pre[i - 1][j];
            if (a[i - 1] >> j & 1) {
                pre[i][j] += 1;
            }
        }
    }

    for (int i = 0; i < q; ++i) {
        int l, r;
        long long k; // 将k的类型改为long long
        cin >> l >> r >> k;

        if (k > MAXV) {
            cout << -1 << endl;
            continue;
        }

        vector<long long> kbit(MAXBIT, 0); // 将kbit数组的类型改为long long
        for (int j = 0; j < MAXBIT; ++j) {
            kbit[j] = k >> j & 1;
        }

        int left = l, right = r;
        while (left < right) {
            int mid = (left + right) >> 1;
            bool ok = true;
            for (int j = 0; j < MAXBIT; ++j) {
                if (kbit[j] == 1 && pre[mid][j] - pre[l - 1][j] == 0) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        bool ok = true;
        for (int j = 0; j < MAXBIT; ++j) {
            if (kbit[j] == 1 && pre[right][j] - pre[l - 1][j] == 0) {
                ok = false;
                break;
            }
            if (kbit[j] == 0 && pre[right][j] - pre[l - 1][j] > 0) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << right << endl;
        } else {
            cout << -1 << endl;
        }
    }

    return 0;
}
```