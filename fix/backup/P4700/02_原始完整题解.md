## 解题思路

设重排后的数组为 $a'$，最终得到的字符串为：

$ t = s_1^{a'_1} + s_2^{a'_2} + \cdots + s_n^{a'_n} $

其中 $s_i^{a'_i}$ 表示把字符 $s_i$ 重复 $a'_i$ 次。

题目要求重排数组 $a$，让字符串 $t$ 的字典序最小。

### 核心贪心思想

考虑当前处理到位置 $i$，还剩下一批数没有分配。

此时只有两种倾向：

* 如果希望当前位置的字符 $s_i$ 尽量多出现，就应该把当前最大的数分给它；
* 如果希望尽快跳到后面的部分，就应该把当前最小的数分给它。

那么怎么判断当前位置应该“多放”还是“少放”？

关键看两个后缀：

* $s[i..n]$
* $s[i+1..n]$

若 $s[i..n] < s[i+1..n]$，说明当前位置这个字符继续多放一些，会让整体更优，所以给它当前最大值。

若 $s[i..n] > s[i+1..n]$，说明当前位置不该停留太久，应尽快进入后面的更优后缀，所以给它当前最小值。

于是得到贪心规则：

* 若 $rank[i] < rank[i+1]$，则当前位置取当前最大值；
* 否则取当前最小值。

其中 $rank[i]$ 表示后缀 $s[i..n]$ 的字典序排名。

最后一个位置 $n$ 只能取剩下的那个数。

### 相关算法

为了快速比较相邻后缀 $s[i..n]$ 和 $s[i+1..n]$，可以先求出字符串 $s$ 的后缀数组排名 $rank$。

这里使用：

* 后缀数组的倍增算法，复杂度为 $O(n \log n)$；
* 排序数组 $a$；
* 双指针/双端贪心分配最小值和最大值。

### 实现方法

1. 读入字符串 $s$ 和数组 $a$。
2. 对 $a$ 从小到大排序。
3. 对字符串 $s$ 建后缀数组，得到每个位置的后缀排名 $rank$。
4. 设两个指针：

   * $l$ 指向当前最小值；
   * $r$ 指向当前最大值。
5. 从左到右遍历每个位置：

   * 如果 $rank[i] < rank[i+1]$，答案位置 $i$ 取 $a[r]$，然后 $r--$；
   * 否则取 $a[l]$，然后 $l++$。
6. 最后一个位置取剩余那个数。

---

## 复杂度分析

设字符串长度为 $n$。

* 排序数组 $a$ 的复杂度为 $O(n \log n)$；
* 倍增法求后缀数组复杂度为 $O(n \log n)$；
* 贪心分配复杂度为 $O(n)$。

所以总时间复杂度为：

$O(n \log n)$

空间复杂度主要为后缀数组相关辅助数组和答案数组：

$O(n)$

该复杂度可以通过题目数据范围。

---

## 代码实现

### Python

```python
# Python 3
# 题意：重排数组 a，使得按规则拼接出的字符串 t 字典序最小

import sys


# 使用倍增算法构建后缀数组排名
def build_rank(s: str):
    n = len(s)
    sa = list(range(n))
    rk = [ord(c) for c in s]
    tmp = [0] * n
    k = 1

    while True:
        # 按照 (rk[i], rk[i+k]) 排序
        sa.sort(key=lambda x: (rk[x], rk[x + k] if x + k < n else -1))

        # 重新计算排名
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            prev = (rk[a], rk[a + k] if a + k < n else -1)
            curr = (rk[b], rk[b + k] if b + k < n else -1)
            tmp[b] = tmp[a] + (1 if prev != curr else 0)

        rk, tmp = tmp, rk
        if rk[sa[-1]] == n - 1:
            break
        k <<= 1

    return rk


# 求一组测试数据的答案
def solve_one(n, s, arr):
    arr.sort()
    rank = build_rank(s)

    ans = [0] * n
    l, r = 0, n - 1

    # 从左到右贪心分配
    for i in range(n - 1):
        # 如果后缀 s[i..] 更小，说明当前位置应该尽量多放
        if rank[i] < rank[i + 1]:
            ans[i] = arr[r]
            r -= 1
        else:
            ans[i] = arr[l]
            l += 1

    # 最后一个位置放剩下的数
    ans[n - 1] = arr[l]
    return ans


def main():
    input = sys.stdin.readline
    T = int(input().strip())
    out = []

    for _ in range(T):
        n = int(input().strip())
        s = input().strip()
        arr = list(map(int, input().split()))
        ans = solve_one(n, s, arr)
        out.append(" ".join(map(str, ans)))

    print("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

/*
题意：重排数组 a，使得按规则拼接出的字符串 t 字典序最小
*/
public class Main {

    // 使用倍增算法构建后缀排名
    static int[] buildRank(String s) {
        int n = s.length();
        Integer[] sa = new Integer[n];
        int[] rk = new int[n];
        int[] tmp = new int[n];

        for (int i = 0; i < n; i++) {
            sa[i] = i;
            rk[i] = s.charAt(i);
        }

        for (int k = 1; ; k <<= 1) {
            final int kk = k;
            final int[] frk = rk;

            // 按照 (rk[i], rk[i+k]) 排序
            Arrays.sort(sa, (a, b) -> {
                if (frk[a] != frk[b]) return frk[a] - frk[b];
                int ra = (a + kk < n) ? frk[a + kk] : -1;
                int rb = (b + kk < n) ? frk[b + kk] : -1;
                return ra - rb;
            });

            // 重新计算排名
            tmp[sa[0]] = 0;
            for (int i = 1; i < n; i++) {
                int a = sa[i - 1], b = sa[i];
                int a1 = rk[a], b1 = rk[b];
                int a2 = (a + k < n) ? rk[a + k] : -1;
                int b2 = (b + k < n) ? rk[b + k] : -1;

                tmp[b] = tmp[a] + ((a1 != b1 || a2 != b2) ? 1 : 0);
            }

            // 拷贝新排名
            System.arraycopy(tmp, 0, rk, 0, n);

            // 如果排名已经唯一，结束
            if (rk[sa[n - 1]] == n - 1) break;
        }

        return rk;
    }

    // 求一组测试数据的答案
    static long[] solveOne(int n, String s, long[] arr) {
        Arrays.sort(arr);
        int[] rank = buildRank(s);

        long[] ans = new long[n];
        int l = 0, r = n - 1;

        // 从左到右贪心分配
        for (int i = 0; i < n - 1; i++) {
            // 如果后缀 s[i..] 更小，说明当前位置应该尽量多放
            if (rank[i] < rank[i + 1]) {
                ans[i] = arr[r--];
            } else {
                ans[i] = arr[l++];
            }
        }

        // 最后一个位置放剩下的数
        ans[n - 1] = arr[l];
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            String s = br.readLine().trim();

            String[] parts = br.readLine().trim().split(" ");
            long[] arr = new long[n];
            for (int i = 0; i < n; i++) {
                arr[i] = Long.parseLong(parts[i]);
            }

            long[] ans = solveOne(n, s, arr);
            for (int i = 0; i < n; i++) {
                if (i > 0) sb.append(' ');
                sb.append(ans[i]);
            }
            sb.append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

/*
题意：重排数组 a，使得按规则拼接出的字符串 t 字典序最小
*/

// 使用倍增算法构建后缀排名
vector<int> build_rank(const string &s) {
    int n = (int)s.size();
    vector<int> sa(n), rk(n), tmp(n);

    for (int i = 0; i < n; i++) {
        sa[i] = i;
        rk[i] = s[i];
    }

    for (int k = 1;; k <<= 1) {
        // 按照 (rk[i], rk[i+k]) 排序
        sort(sa.begin(), sa.end(), [&](int a, int b) {
            if (rk[a] != rk[b]) return rk[a] < rk[b];
            int ra = (a + k < n) ? rk[a + k] : -1;
            int rb = (b + k < n) ? rk[b + k] : -1;
            return ra < rb;
        });

        // 重新计算排名
        tmp[sa[0]] = 0;
        for (int i = 1; i < n; i++) {
            int a = sa[i - 1], b = sa[i];
            pair<int, int> pa = {rk[a], (a + k < n ? rk[a + k] : -1)};
            pair<int, int> pb = {rk[b], (b + k < n ? rk[b + k] : -1)};
            tmp[b] = tmp[a] + (pa != pb);
        }

        rk = tmp;

        // 如果排名已经唯一，结束
        if (rk[sa[n - 1]] == n - 1) break;
    }

    return rk;
}

// 求一组测试数据的答案
vector<long long> solve_one(int n, const string &s, vector<long long> &a) {
    sort(a.begin(), a.end());
    vector<int> rank = build_rank(s);

    vector<long long> ans(n);
    int l = 0, r = n - 1;

    // 从左到右贪心分配
    for (int i = 0; i < n - 1; i++) {
        // 如果后缀 s[i..] 更小，说明当前位置应该尽量多放
        if (rank[i] < rank[i + 1]) {
            ans[i] = a[r--];
        } else {
            ans[i] = a[l++];
        }
    }

    // 最后一个位置放剩下的数
    ans[n - 1] = a[l];
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        string s;
        cin >> n >> s;

        vector<long long> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];

        vector<long long> ans = solve_one(n, s, a);

        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }

    return 0;
}
```