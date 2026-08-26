## 解题思路

设灯珠状态串为 $s$，相邻权重为 $w_1,w_2,\dots,w_{n-1}$。

题目要求在至多一次翻转一个连续段 $[l,r]$ 后，使灯带的相融度最大。相融度定义为：

$$
\sum_{i=1}^{n-1} w_i \cdot [s_i=s_{i+1}]
$$

其中 $[,]$ 是指示函数，条件成立取 $1$，否则取 $0$。

### 关键结论

如果翻转一段连续区间 $[l,r]$，那么：

* 区间内部的相邻对 $(i,i+1)$，若两端都在区间内，它们会同时翻转，原来相同翻转后仍相同，原来不同翻转后仍不同，所以这部分贡献不变。
* 区间外部的相邻对显然也不变。
* 只有区间边界处的相邻对可能变化：

  * 左边界 $(l-1,l)$，前提是 $l>1$
  * 右边界 $(r,r+1)$，前提是 $r<n$

也就是说，一次翻转最多只会影响两个焊点。

---

### 把每个焊点的“变化收益”单独算出来

对每个焊点 $i$（连接 $i$ 和 $i+1$），考虑如果它成为翻转边界，那么它的贡献会怎样变化。

* 若原来 $s_i=s_{i+1}$，翻转一侧后会变成不同，贡献变化为 $-w_i$
* 若原来 $s_i\ne s_{i+1}$，翻转一侧后会变成相同，贡献变化为 $+w_i$

于是定义：

$$
a_i=
\begin{cases}
+w_i, & s_i\ne s_{i+1} \
-w_i, & s_i=s_{i+1}
\end{cases}
$$

那么：

* 翻转前缀 $[1,r]$，收益就是 $a_r$
* 翻转后缀 $[l,n]$，收益就是 $a_{l-1}$
* 翻转中间一段 $[l,r]$，收益就是 $a_{l-1}+a_r$

所以问题就变成：

> 在数组 $a_1,a_2,\dots,a_{n-1}$ 中，最多选两个不同位置，使收益和最大。

因为任意两个不同焊点都可以分别作为某个区间的左右边界，所以只需要取 $a$ 中最大的两个正数即可：

* 若没有正数，不翻转
* 若只有一个正数，取它
* 若有至少两个正数，取最大的两个

---

### 算法

1. 先计算初始相融度 $base$
2. 遍历所有焊点，计算每个 $a_i$
3. 维护最大的两个正收益 $mx_1,mx_2$
4. 答案为：

$$
base + mx_1 + mx_2
$$

其中 $mx_1,mx_2$ 默认为 $0$

这个做法本质上是一次遍历加贪心。

## 复杂度分析

设灯珠数量为 $n$。

* 时间复杂度：$O(n)$
* 空间复杂度：$O(1)$

只需线性扫描一遍，复杂度完全满足 $n\le 2\times 10^5$ 的要求。

## 代码实现

### Python

```python
def solve(n, s, w):
    # 计算初始相融度
    base = 0

    # 记录最大的两个正收益
    mx1 = 0
    mx2 = 0

    for i in range(n - 1):
        if s[i] == s[i + 1]:
            # 当前焊点原本有贡献
            base += w[i]
            gain = -w[i]
        else:
            # 当前焊点原本无贡献，若作为边界可新增贡献
            gain = w[i]

        # 维护最大的两个正收益
        if gain > mx1:
            mx2 = mx1
            mx1 = gain
        elif gain > mx2:
            mx2 = gain

    return base + mx1 + mx2


def main():
    # 输入
    n = int(input().strip())
    s = input().strip()
    w = list(map(int, input().split()))

    # 输出
    print(solve(n, s, w))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 计算翻转至多一次后的最大相融度
    public static long solve(int n, String s, int[] w) {
        long base = 0L;

        // 记录最大的两个正收益
        long mx1 = 0L, mx2 = 0L;

        for (int i = 0; i < n - 1; i++) {
            long gain;
            if (s.charAt(i) == s.charAt(i + 1)) {
                // 当前焊点原本有贡献
                base += w[i];
                gain = -w[i];
            } else {
                // 当前焊点原本无贡献，若作为边界可新增贡献
                gain = w[i];
            }

            // 维护最大的两个正收益
            if (gain > mx1) {
                mx2 = mx1;
                mx1 = gain;
            } else if (gain > mx2) {
                mx2 = gain;
            }
        }

        return base + mx1 + mx2;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入
        int n = sc.nextInt();
        String s = sc.next();
        int[] w = new int[n - 1];
        for (int i = 0; i < n - 1; i++) {
            w[i] = sc.nextInt();
        }

        // 输出
        System.out.println(solve(n, s, w));

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 计算翻转至多一次后的最大相融度
long long solve(int n, const string& s, const vector<int>& w) {
    long long base = 0;

    // 记录最大的两个正收益
    long long mx1 = 0, mx2 = 0;

    for (int i = 0; i < n - 1; i++) {
        long long gain;
        if (s[i] == s[i + 1]) {
            // 当前焊点原本有贡献
            base += w[i];
            gain = -1LL * w[i];
        } else {
            // 当前焊点原本无贡献，若作为边界可新增贡献
            gain = w[i];
        }

        // 维护最大的两个正收益
        if (gain > mx1) {
            mx2 = mx1;
            mx1 = gain;
        } else if (gain > mx2) {
            mx2 = gain;
        }
    }

    return base + mx1 + mx2;
}

int main() {
    // 输入
    int n;
    cin >> n;

    string s;
    cin >> s;

    vector<int> w(n - 1);
    for (int i = 0; i < n - 1; i++) {
        cin >> w[i];
    }

    // 输出
    cout << solve(n, s, w) << '\n';

    return 0;
}
```