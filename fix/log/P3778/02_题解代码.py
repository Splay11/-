## 解题思路

给定：

* 共 `n` 个视频，第 `i` 个视频长度为 `a_i`；
* 平台参数 `x`：一次播放要被计数，至少观看 `min(a_i, x)` 秒；
* 每个视频的播放次数 `v_i` 满足下界 `q_i` 与上界 `r_i`；
* 总播放次数为 `m`（保证可行：`∑q_i ≤ m ≤ ∑r_i`）。

一次有效播放带来的**最少时长**为 `min(a_i, x)`，**最多时长**为 `a_i`。
因此在满足 `q_i ≤ v_i ≤ r_i` 且 `∑v_i = m` 的前提下：

* 令 `c_i^L = min(a_i, x)`。要使总时长最小，就把“额外的”播放次数尽量分配给 `c_i^L` 小的那些视频；
* 令 `c_i^R = a_i`。要使总时长最大，就把“额外的”播放次数尽量分配给 `c_i^R` 大的那些视频。

做法（同一套框架，系数不同）：

1. 先给每个视频分配下界 `q_i`，得到剩余可分配次数 `left = m - ∑q_i`；
2. 计算每个视频还能再加的上限 `cap_i = r_i - q_i`；
3. 将视频按“单位播放贡献”的系数排序：

   * 最小值 `L`：按 `c_i^L` 从小到大；
   * 最大值 `R`：按 `c_i^R` 从大到小；
4. 依次把 `left` 分配给当前视频，分配量为 `add = min(left, cap_i)`，并增加时长 `add * 系数`，直至 `left = 0`。

该贪心正确性可由**交换论证**：若把一次额外播放从更差的系数移动到更优的系数，会使目标更优，因此最优分配一定满足“尽量给最优系数”的顺序。

## 复杂度分析

* 排序占主导，时间复杂度 `O(n log n)`；一次线性分配 `O(n)`。
* 只需保存若干数组与排序辅助结构，空间复杂度 `O(n)`。
* 所有累加均可能很大，需使用 64 位整型。

## 代码实现

### Python

```python
# -*- coding: utf-8 -*-
# 题意实现函数放在外部；主函数只负责输入输出（ACM风格）

from typing import List, Tuple

def calc_min_total_time(n: int, x: int, m: int,
                        a: List[int], q: List[int], r: List[int]) -> int:
    """计算最小总观看时长"""
    # 单位时长系数为 min(a_i, x)
    coeff = [min(a[i], x) for i in range(n)]
    base = 0  # 先分配下界
    caps = []
    for i in range(n):
        base += q[i] * coeff[i]
        caps.append((coeff[i], r[i] - q[i]))  # (系数, 还能加的次数)
    left = m - sum(q)
    # 按系数从小到大贪心
    caps.sort(key=lambda t: t[0])
    res = base
    for c, cap in caps:
        if left <= 0:
            break
        add = min(left, cap)
        res += add * c
        left -= add
    return res

def calc_max_total_time(n: int, x: int, m: int,
                        a: List[int], q: List[int], r: List[int]) -> int:
    """计算最大总观看时长"""
    coeff = [a[i] for i in range(n)]  # 单位时长系数为 a_i
    base = 0
    caps = []
    for i in range(n):
        base += q[i] * coeff[i]
        caps.append((coeff[i], r[i] - q[i]))
    left = m - sum(q)
    # 按系数从大到小贪心
    caps.sort(key=lambda t: -t[0])
    res = base
    for c, cap in caps:
        if left <= 0:
            break
        add = min(left, cap)
        res += add * c
        left -= add
    return res

def main():
    # 输入：n x m
    n, x, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = list(map(int, input().split()))
    r = list(map(int, input().split()))
    L = calc_min_total_time(n, x, m, a, q, r)
    R = calc_max_total_time(n, x, m, a, q, r)
    print(L, R)

if __name__ == "__main__":
    main()
```

### Java

```java
// ACM 风格，类名为 Main。读取输入，功能在外部静态函数里实现。
import java.io.*;
import java.util.*;

public class Main {

    // 计算最小总观看时长：单位系数为 min(a_i, x)
    static long calcMin(int n, int x, long m, int[] a, long[] q, long[] r) {
        long base = 0;
        long left = m;
        for (int i = 0; i < n; i++) left -= q[i];

        // (coef, cap)
        long[][] arr = new long[n][2];
        for (int i = 0; i < n; i++) {
            long coef = Math.min(a[i], x);
            base += q[i] * coef;
            arr[i][0] = coef;
            arr[i][1] = r[i] - q[i];
        }
        Arrays.sort(arr, new Comparator<long[]>() {
            public int compare(long[] p1, long[] p2) {
                return Long.compare(p1[0], p2[0]); // 从小到大
            }
        });
        long res = base;
        for (int i = 0; i < n && left > 0; i++) {
            long add = Math.min(left, arr[i][1]);
            res += add * arr[i][0];
            left -= add;
        }
        return res;
    }

    // 计算最大总观看时长：单位系数为 a_i
    static long calcMax(int n, int x, long m, int[] a, long[] q, long[] r) {
        long base = 0;
        long left = m;
        for (int i = 0; i < n; i++) left -= q[i];

        long[][] arr = new long[n][2];
        for (int i = 0; i < n; i++) {
            long coef = a[i];
            base += q[i] * coef;
            arr[i][0] = coef;
            arr[i][1] = r[i] - q[i];
        }
        Arrays.sort(arr, new Comparator<long[]>() {
            public int compare(long[] p1, long[] p2) {
                return Long.compare(p2[0], p1[0]); // 从大到小
            }
        });
        long res = base;
        for (int i = 0; i < n && left > 0; i++) {
            long add = Math.min(left, arr[i][1]);
            res += add * arr[i][0];
            left -= add;
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        // 使用 BufferedReader + StringTokenizer，兼顾可读性与性能
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int x = Integer.parseInt(st.nextToken());
        long m = Long.parseLong(st.nextToken());

        int[] a = new int[n];
        long[] q = new long[n];
        long[] r = new long[n];

        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());

        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) q[i] = Long.parseLong(st.nextToken());

        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) r[i] = Long.parseLong(st.nextToken());

        long L = calcMin(n, x, m, a, q, r);
        long R = calcMax(n, x, m, a, q, r);
        System.out.println(L + " " + R);
    }
}
```

### C++

```cpp
// ACM 风格：主函数读写，功能写在外部函数里
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 计算最小总观看时长：按 min(a_i, x) 从小到大分配
long long calc_min_total_time(int n, long long x, long long m,
                              const vector<long long>& a,
                              const vector<long long>& q,
                              const vector<long long>& r) {
    vector<pair<long long,long long>> vec; // (coef, cap)
    vec.reserve(n);
    long long base = 0;
    long long left = m;
    for (int i = 0; i < n; ++i) left -= q[i];
    for (int i = 0; i < n; ++i) {
        long long coef = min(a[i], x);
        base += q[i] * coef;
        vec.push_back({coef, r[i] - q[i]});
    }
    sort(vec.begin(), vec.end(), [](const auto& p1, const auto& p2){
        return p1.first < p2.first; // 从小到大
    });
    long long res = base;
    for (auto &p : vec) {
        if (left <= 0) break;
        long long add = min(left, p.second);
        res += add * p.first;
        left -= add;
    }
    return res;
}

// 计算最大总观看时长：按 a_i 从大到小分配
long long calc_max_total_time(int n, long long x, long long m,
                              const vector<long long>& a,
                              const vector<long long>& q,
                              const vector<long long>& r) {
    vector<pair<long long,long long>> vec; // (coef, cap)
    vec.reserve(n);
    long long base = 0;
    long long left = m;
    for (int i = 0; i < n; ++i) left -= q[i];
    for (int i = 0; i < n; ++i) {
        long long coef = a[i];
        base += q[i] * coef;
        vec.push_back({coef, r[i] - q[i]});
    }
    sort(vec.begin(), vec.end(), [](const auto& p1, const auto& p2){
        return p1.first > p2.first; // 从大到小
    });
    long long res = base;
    for (auto &p : vec) {
        if (left <= 0) break;
        long long add = min(left, p.second);
        res += add * p.first;
        left -= add;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long x, m;
    if (!(cin >> n >> x >> m)) return 0;
    vector<long long> a(n), q(n), r(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    for (int i = 0; i < n; ++i) cin >> q[i];
    for (int i = 0; i < n; ++i) cin >> r[i];

    long long L = calc_min_total_time(n, x, m, a, q, r);
    long long R = calc_max_total_time(n, x, m, a, q, r);
    cout << L << " " << R << "\n";
    return 0;
}
```