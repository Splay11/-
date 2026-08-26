## 关键等价

对任意排列，记 $N_k$ 为“包含所有 $0,1,\dots,k-1$ 的子数组数量”。则

$$
\sum_{\text{所有子数组}} mex = \sum_{k=1}^{n} N_k.
$$

理由：某个子数组若 $mex = m$，它恰好对 $k=1,2,\dots,m$ 各贡献 $1$ 次（因为包含 $0,\dots,k-1$），对更大的 $k$ 不贡献，故总贡献为 $m$。

因此最大化目标等价于对每个$k$ 最大化 $N_k$。而 $N_k$ 仅由 $0,1,\dots,k-1$ 的位置决定，与更大的数无关——这允许我们“按 $k$ 从小到大逐步最优”。

设 $0,1,\dots,k-1$ 的位置区间为 $[L\_k,R\_k]$（用 $1$ 到 $n$ 的下标）。能覆盖该区间的子数组数量为

$$
N_k=L_k\cdot (n-R_k+1).
$$

## 最优构造的贪心思路

令 $m=\left\lfloor \dfrac{n+1}{2}\right\rfloor$。将 $0$ 放在第 $m$ 个位置，使

$$
N_1 = m\cdot (n-m+1)
$$

最大（乘积在和固定为 $n+1$ 时，当两因子尽量均衡最大）。

对于一般的 $k$，$N_k$ 只依赖于 $0,1,\dots,k-1$ 的位置。要最大化 $N_{k+1}$，只需把新元素 $k$ 放在当前区间 $[L_k,R_k]$ 的相邻一格处，选择能使

$$
N_{k+1}=L_{k+1}\cdot (n-R_{k+1}+1)
$$

更大的那一侧。这样不断扩张，始终让 ${0,1,\dots,k}$ 占据一个以中位为中心、长度为 $k+1$ 的连续块。

由此得到一个简单的**显式排列**：

* 当 $n$ 为奇数：排列为

  $$
  [\,n-2,n-4,\dots,3,1,0,2,4,\dots,n-1\,].
  $$
* 当 $n$ 为偶数：排列为

  $$
  [\,n-2,n-4,\dots,2,0,1,3,5,\dots,n-1\,].
  $$

直观上：把 $0$ 放中间；左侧放与 $n-2$ 同奇偶性的数按降序；右侧放剩余数按升序。这样每次把更小的数贴着当前块扩张，且优先向“可选端点数更多”的一侧扩张。

## 最大值的闭式公式

记 $B=n-m+1$。当块长度为 $s$ 时：

* 若 $s=2t+1$（奇数），则 $N_s=(m-t)\cdot(B-t)$。
* 若 $s=2t$（偶数），则 $N_s=(m-t+1)\cdot(B-t)$。

将 $s=1,2,\dots,n$ 求和后可化简为仅关于 $n$ 的闭式：

* 若 $n=2q$ 为偶数：

  ![](/file/2/F7BsfE3CjYFPBJRkeN9OZ.png)

* 若 $n=2q+1$ 为奇数：

  ![](/file/2/WYYv1Yu16wgF0QPh76yFQ.png)


# C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;
using int64 = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; 
    if(!(cin >> T)) return 0;
    while (T--) {
        long long n; 
        cin >> n;

        // 计算最大值（用 long long 足够）
        long long ans;
        if (n % 2 == 0) {
            // 偶数 n=2q: S = n(n+2)(2n+5)/24
            ans = n * (n + 2) * (2 * n + 5) / 24;
        } else {
            // 奇数 n=2q+1: S = (n+1)(n+3)(2n+1)/24
            ans = (n + 1) * (n + 3) * (2 * n + 1) / 24;
        }

        cout << ans << "\n";

        // 构造最优排列：
        // 规则：输出 [n-2, n-4, ..., (>0), 0, 剩余按升序]
        // 当 n 为奇数，左侧是奇数降序；当 n 为偶数，左侧是偶数降序。
        vector<int> a;
        for (long long x = n - 2; x > 0; x -= 2) a.push_back((int)x); // 左侧
        a.push_back(0);                                              // 中间
        // 右侧：把未出现的 1..n-1 剩余数按升序补上
        vector<char> used(n, 0);
        for (int v : a) used[v] = 1;
        for (int v = 1; v <= (int)n - 1; ++v) if (!used[v]) a.push_back(v);

        // 输出排列
        for (int i = 0; i < (int)a.size(); ++i) {
            if (i) cout << ' ';
            cout << a[i];
        }
        cout << "\n";
    }
    return 0;
}
```
# Python 

```python
import sys

def max_sum(n: int) -> int:
    # 计算最大值的闭式
    if n % 2 == 0:
        # 偶数：n(n+2)(2n+5)/24
        return n * (n + 2) * (2 * n + 5) // 24
    else:
        # 奇数：(n+1)(n+3)(2n+1)/24
        return (n + 1) * (n + 3) * (2 * n + 1) // 24

def build_perm(n: int):
    # 构造最优排列：左侧放 n-2, n-4, ... (>0)，中间 0，右侧补剩余升序
    a = []
    x = n - 2
    while x > 0:
        a.append(x)
        x -= 2
    a.append(0)
    used = [False] * n
    for v in a:
        used[v] = True
    for v in range(1, n):
        if not used[v]:
            a.append(v)
    return a

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        n = int(next(it))
        out_lines.append(str(max_sum(n)))
        out_lines.append(' '.join(map(str, build_perm(n))))
    print('\n'.join(out_lines))

if __name__ == "__main__":
    main()
```
# Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    static long maxSum(long n) {
        // 计算最大值闭式
        if ((n & 1) == 0) {
            // 偶数：n(n+2)(2n+5)/24
            return n * (n + 2) * (2 * n + 5) / 24;
        } else {
            // 奇数：(n+1)(n+3)(2n+1)/24
            return (n + 1) * (n + 3) * (2 * n + 1) / 24;
        }
    }

    static int[] buildPerm(int n) {
        // 构造最优排列：左侧 n-2, n-4, ... (>0)，中间 0，右侧补剩余升序
        ArrayList<Integer> list = new ArrayList<>();
        for (int x = n - 2; x > 0; x -= 2) list.add(x);
        list.add(0);
        boolean[] used = new boolean[n];
        for (int v : list) used[v] = true;
        for (int v = 1; v <= n - 1; ++v) if (!used[v]) list.add(v);
        int[] a = new int[n];
        for (int i = 0; i < n; ++i) a[i] = list.get(i);
        return a;
    }

    public static void main(String[] args) throws Exception {
        // 读入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            sb.append(maxSum(n)).append('\n');
            int[] a = buildPerm(n);
            for (int i = 0; i < n; ++i) {
                if (i > 0) sb.append(' ');
                sb.append(a[i]);
            }
            sb.append('\n');
        }
        System.out.print(sb.toString());
    }
}
```