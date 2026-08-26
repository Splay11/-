## 解题思路

核心思路

设当前权重序列为 $w_1,w_2,\ldots,w_n$。

一次操作会在连续三个位置上分别增加

$$
-x,\quad 2x,\quad -x.
$$

考虑下面两个量：

$$
S=\sum_{i=1}^{n}w_i,
$$

$$
P=\sum_{i=1}^{n}i\cdot w_i.
$$

对于一次作用在 $[i,i+2]$ 上的操作，总和的变化量为

$$
-x+2x-x=0.
$$

加权和的变化量为

$$
-i x+2(i+1)x-(i+2)x=0.
$$

因此，无论进行多少次操作，$S$ 和 $P$ 都不会改变。

下面证明这两个不变量已经能够完全描述序列之间的可达关系。

记第 $i$ 种操作对应的变化向量为 $b_i$，它只在第 $i,i+1,i+2$ 个位置上分别为 $-1,2,-1$。

向量 $b_1,b_2,\ldots,b_{n-2}$ 线性无关。因为如果

$$
c_1b_1+c_2b_2+\cdots+c_{n-2}b_{n-2}=0,
$$

观察第一个位置可以得到 $c_1=0$；继续依次观察后面的位置，可以得到

$$
c_2=c_3=\cdots=c_{n-2}=0.
$$

所以这些操作向量张成的空间维数为 $n-2$。

另一方面，所有满足

$$
\sum_{i=1}^{n}d_i=0,
\qquad
\sum_{i=1}^{n}i\cdot d_i=0
$$

的向量构成一个维数为 $n-2$ 的空间。所有操作向量都属于这个空间，因此两者完全相同。

所以，只要两个序列的 $S$ 和 $P$ 相等，就一定可以通过若干次操作互相转化。

现在问题转化为：是否存在一个非负序列 $a_1,a_2,\ldots,a_n$，满足

$$
\sum_{i=1}^{n}a_i=S,
\qquad
\sum_{i=1}^{n}i\cdot a_i=P.
$$

如果所有 $a_i\geq 0$，则必然有

$$
S\geq 0.
$$

同时，

$$
P-S=\sum_{i=1}^{n}(i-1)a_i\geq 0,
$$

所以

$$
P\geq S.
$$

并且

$$
nS-P=\sum_{i=1}^{n}(n-i)a_i\geq 0,
$$

所以

$$
P\leq nS.
$$

因此必要条件为

$$
S\geq 0,\qquad S\leq P\leq nS.
$$

这个条件也是充分的。满足条件时，可以构造如下非负序列：

$$
a_1=\frac{nS-P}{n-1},
$$

$$
a_n=\frac{P-S}{n-1},
$$

其余位置全部取 $0$。

由条件可知 $a_1,a_n\geq 0$，并且

$$
a_1+a_n=S,
$$

$$
a_1+na_n=P.
$$

它与原序列拥有相同的两个不变量，因此一定可以由原序列转化得到。

实现方法

遍历序列，计算：

$$
S=\sum_{i=1}^{n}w_i,
$$

$$
P=\sum_{i=1}^{n}i\cdot w_i.
$$

最后判断是否同时满足：

$$
S\geq 0,\qquad P\geq S,\qquad P\leq nS.
$$

满足则输出 `YES`，否则输出 `NO`。

## 复杂度分析

对于每组测试数据，只需要遍历一次序列。

时间复杂度为

$$
O(n).
$$

代码中保存了输入序列，空间复杂度为

$$
O(n).
$$

除输入数组外，只使用常数个变量，额外空间复杂度为

$$
O(1).
$$

所有测试数据的 $n$ 之和不超过 $2\times 10^5$，因此该复杂度可以通过要求。

## 代码实现

### Python

```python
import sys


def check(w):
    n = len(w)
    s = 0
    p = 0

    # 计算总和不变量 S 和下标加权和不变量 P
    for i in range(n):
        s += w[i]
        p += (i + 1) * w[i]

    # 存在非负目标序列的充要条件
    return s >= 0 and p >= s and p <= n * s


def main():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        w = []

        while len(w) < n:
            w.extend(map(int, input().split()))

        if check(w):
            ans.append("YES")
        else:
            ans.append("NO")

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.math.BigInteger;
import java.util.StringTokenizer;

public class Main {
    static class Reader {
        private final BufferedReader br =
                new BufferedReader(new InputStreamReader(System.in));
        private StringTokenizer st;

        String next() throws IOException {
            while (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }
    }

    static boolean check(BigInteger[] w) {
        int n = w.length;
        BigInteger s = BigInteger.ZERO;
        BigInteger p = BigInteger.ZERO;

        // 计算总和不变量 S 和下标加权和不变量 P
        for (int i = 0; i < n; i++) {
            s = s.add(w[i]);
            BigInteger pos = BigInteger.valueOf(i + 1L);
            p = p.add(w[i].multiply(pos));
        }

        // 分别判断 S >= 0、P >= S、P <= nS
        if (s.signum() < 0) {
            return false;
        }
        if (p.compareTo(s) < 0) {
            return false;
        }

        BigInteger right = s.multiply(BigInteger.valueOf(n));
        return p.compareTo(right) <= 0;
    }

    public static void main(String[] args) throws Exception {
        Reader rd = new Reader();
        int t = rd.nextInt();
        StringBuilder ans = new StringBuilder();

        for (int test = 0; test < t; test++) {
            int n = rd.nextInt();
            BigInteger[] w = new BigInteger[n];

            for (int i = 0; i < n; i++) {
                w[i] = new BigInteger(rd.next());
            }

            if (check(w)) {
                ans.append("YES\n");
            } else {
                ans.append("NO\n");
            }
        }

        System.out.print(ans);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

bool check(const vector<long long>& w) {
    int n = static_cast<int>(w.size());
    __int128 s = 0;
    __int128 p = 0;

    // 计算总和不变量 S 和下标加权和不变量 P
    for (int i = 0; i < n; i++) {
        s += (__int128)w[i];
        p += (__int128)(i + 1) * w[i];
    }

    // 判断 S >= 0、P >= S、P <= nS
    return s >= 0 && p >= s && p <= (__int128)n * s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<long long> w(n);
        for (int i = 0; i < n; i++) {
            cin >> w[i];
        }

        if (check(w)) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}
```