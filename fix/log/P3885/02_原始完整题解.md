## 解题思路

给定数组 $a_1,a_2,\ldots,a_n$。对任意区间 $[l,r]$ $(1\le l<r\le n)$，其贡献定义为区间内部所有下标 $i$（$l<i<r$）中满足

$$
a_i<a_l \quad \text{或} \quad a_i<a_r
$$

的个数。要求所有区间贡献之和。

把所有可能的三元组 $(l,i,r)$（满足 $l<i<r$）看成单位贡献。对于一个固定的三元组，它**不被计入**的充要条件是：

$$
a_i\ge a_l \ \text{且}\ a_i\ge a_r
$$

也就是两端点都不大于中间值。于是

$\text{答案}$=$\binom{n}{3}$-$\sum_{i=1}^{n} L_i\cdot R_i$

其中
$L_i=\#\{\,l<i\mid a_l\le a_i\,\}$，
$R_i=\#\{\,r>i\mid a_r\le a_i\,\}$。

因此核心是对每个位置 $i$ 统计左侧、右侧不大于 $a_i$ 的数量。由于 $a_i$ 范围大，需要**值域压缩**；统计时用树状数组维护前缀出现次数：

* 扫描左到右，用 BIT 统计 $\le a_i$ 的个数得到 $L_i$；
* 扫描右到左，用另一个 BIT 统计 $\le a_i$ 的个数得到 $R_i$。

最后按公式计算即可。

## 复杂度分析

* 值域压缩：$O(n\log n)$（排序去重）。
* 两次线性扫描 + 树状数组操作：每次 $O(n\log n)$。
* 总时间复杂度：$O(n\log n)$，满足 $\sum n\le 2\times10^5$ 的数据范围。
* 额外空间：存储压缩后的数组与两个计数数组与 BIT，$O(n)$。

## 代码实现

### Python

```python
# -*- coding: utf-8 -*-
import sys

# 树状数组（1-indexed）
class BIT:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i, v=1):
        while i <= self.n:
            self.t[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

def solve_case(a):
    n = len(a)
    # 组合数 C(n,3)
    total = n * (n - 1) * (n - 2) // 6 if n >= 3 else 0
    if n < 3:
        return 0

    # 值域压缩
    vals = sorted(set(a))
    idx = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed

    m = len(vals)
    bit = BIT(m)
    L = [0] * n
    for i in range(n):
        k = idx[a[i]]
        L[i] = bit.sum(k)  # 左侧 <= a[i]
        bit.add(k, 1)

    bit2 = BIT(m)
    R = [0] * n
    for i in range(n - 1, -1, -1):
        k = idx[a[i]]
        R[i] = bit2.sum(k)  # 右侧 <= a[i]
        bit2.add(k, 1)

    bad = 0
    for i in range(n):
        bad += L[i] * R[i]
    return total - bad

def main():
    data = list(map(int, sys.stdin.read().strip().split()))
    t = data[0]
    ans = []
    p = 1
    for _ in range(t):
        n = data[p]; p += 1
        arr = data[p:p+n]; p += n
        ans.append(str(solve_case(arr)))
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()
```

### Java

```java
// 注意：类名必须为 Main（ACM 风格）
import java.io.*;
import java.util.*;

// 简单树状数组
class BIT {
    int n;
    long[] t;
    BIT(int n) { this.n = n; t = new long[n + 1]; }
    void add(int i, long v) {
        while (i <= n) { t[i] += v; i += i & -i; }
    }
    long sum(int i) {
        long s = 0;
        while (i > 0) { s += t[i]; i -= i & -i; }
        return s;
    }
}

public class Main {
    // 快速读入，数据量较大时更稳妥
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is){ in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        int nextInt() throws IOException {
            int c, sgn = 1, x = 0;
            do { c = read(); } while (c <= 32);
            if (c == '-') { sgn = -1; c = read(); }
            while (c > 32) { x = x * 10 + c - '0'; c = read(); }
            return x * sgn;
        }
    }

    // 计算单组答案的函数：放在主函数外部
    static long solveCase(int[] a) {
        int n = a.length;
        if (n < 3) return 0L;
        long total = 1L * n * (n - 1) * (n - 2) / 6;

        // 值域压缩
        int[] b = Arrays.copyOf(a, n);
        Arrays.sort(b);
        int m = 0;
        for (int i = 0; i < n; i++) {
            if (i == 0 || b[i] != b[i - 1]) b[m++] = b[i];
        }
        // b[0..m-1] 为去重后的有序值域

        long[] L = new long[n];
        BIT bit1 = new BIT(m);
        for (int i = 0; i < n; i++) {
            int k = Arrays.binarySearch(b, 0, m, a[i]) + 1; // 1-indexed
            L[i] = bit1.sum(k);
            bit1.add(k, 1);
        }

        long[] R = new long[n];
        BIT bit2 = new BIT(m);
        for (int i = n - 1; i >= 0; i--) {
            int k = Arrays.binarySearch(b, 0, m, a[i]) + 1;
            R[i] = bit2.sum(k);
            bit2.add(k, 1);
        }

        long bad = 0;
        for (int i = 0; i < n; i++) bad += L[i] * R[i];
        return total - bad;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int T = fs.nextInt();
        StringBuilder sb = new StringBuilder();
        for (int tc = 0; tc < T; tc++) {
            int n = fs.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = fs.nextInt();
            sb.append(solveCase(a)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// -*- coding: utf-8 -*-
// ACM 风格：主函数读写，功能实现放在外部函数里
#include <bits/stdc++.h>
using namespace std;

// 简单树状数组（1-indexed）
struct BIT {
    int n;
    vector<long long> t;
    BIT(int n=0){init(n);}
    void init(int n_){ n=n_; t.assign(n+1,0); }
    void add(int i, long long v=1){
        for(; i<=n; i+=i&-i) t[i]+=v;
    }
    long long sum(int i){
        long long s=0;
        for(; i>0; i-=i&-i) s+=t[i];
        return s;
    }
};

// 计算单组答案
long long solve_case(const vector<long long>& a) {
    int n = (int)a.size();
    if (n < 3) return 0LL;
    long long total = 1LL*n*(n-1)*(n-2)/6;

    // 值域压缩
    vector<long long> b = a;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    int m = (int)b.size();

    vector<long long> L(n), R(n);
    BIT bit1(m), bit2(m);

    for (int i=0;i<n;i++){
        int k = int(lower_bound(b.begin(), b.end(), a[i]) - b.begin()) + 1; // 1-indexed
        L[i] = bit1.sum(k);
        bit1.add(k, 1);
    }
    for (int i=n-1;i>=0;i--){
        int k = int(lower_bound(b.begin(), b.end(), a[i]) - b.begin()) + 1;
        R[i] = bit2.sum(k);
        bit2.add(k, 1);
    }

    long long bad = 0;
    for (int i=0;i<n;i++) bad += L[i]*R[i];
    return total - bad;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if(!(cin>>T)) return 0;
    while(T--){
        int n; cin>>n;
        vector<long long> a(n);
        for(int i=0;i<n;i++) cin>>a[i];
        cout<<solve_case(a)<<"\n";
    }
    return 0;
}
```