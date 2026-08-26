## 解题思路

### 核心思路

先分析两个限制：

1. 交换操作的本质
   对于位置 $(i,j)$，它只能和 $(i \operatorname{xor} 1,; j \operatorname{xor} 1)$ 交换。
   因为 $j \operatorname{xor} 1$ 只会把列下标的最低位翻转，所以：

* 若 $j$ 是偶数，则它只能和 $j+1$ 这一列产生联系；
* 若 $j$ 是奇数，则它只能和 $j-1$ 这一列产生联系。

所以，整个网格会被拆成若干个彼此独立的 $2\times 2$ 小块：

$$
(0,1),\ (2,3),\ (4,5),\ \dots
$$

对于每个小块，设其四个数分别是：

$$
\begin{matrix}
x=a_{0,2k} & y=a_{0,2k+1}\
z=a_{1,2k} & w=a_{1,2k+1}
\end{matrix}
$$

可进行的交换只有两种：

* $x \leftrightarrow w$
* $z \leftrightarrow y$

并且这两个交换互不影响，因此每个小块都可以独立处理。



2. 路径的本质
   从 $(0,0)$ 到 $(1,n-1)$，只能向右或向下走。
   因为只有两行，所以整条路径一定**恰好向下走一次**。

也就是说，路径一定形如：

* 先在第 0 行一直向右走到某一列；
* 然后向下走一格；
* 再在第 1 行一直向右走到终点。

因此，决定答案的关键就是：**向下发生在哪一列**。



### 按 $2\times 2$ 小块分类讨论

考虑某个小块：

$$
\begin{matrix}
x & y \\
z & w
\end{matrix}
$$


路径与这个小块只会有两种关系。

#### 情况一：路径不在这个小块里向下

那么这个小块要么只经过上面一行两个格子，要么只经过下面一行两个格子。

* 若只经过上面两个格子，那么我们希望上面两个位置尽量大：

  * 左上位置可以在 $x,w$ 中选大的；
  * 右上位置可以在 $y,z$ 中选大的。

  所以贡献为：

  $$
  \max(x,w)+\max(y,z)
  $$

* 若只经过下面两个格子，同理贡献也是：

  $$
  \max(z,y)+\max(w,x)=\max(y,z)+\max(x,w)
  $$

所以，无论这个小块在路径的上半段还是下半段，**只要不在这里向下**，最优贡献都相同，记为：

$$
S_k=\max(a_{0,2k},a_{1,2k+1})+\max(a_{0,2k+1},a_{1,2k})
$$



#### 情况二：路径在这个小块里向下

设这个小块是：

$$
\begin{matrix}
x & y \\
z & w
\end{matrix}
$$

不管是在这一块的左列向下，还是右列向下，都会发现：

* 一定会经过左上和右下这一对对角线位置中的两个贡献总和 $x+w$；
* 另一条对角线中，只能再多取到一个较大值，即 $\max(y,z)$。

所以该小块的最大贡献为：

$$
T_k=x+w+\max(y,z)
$$

与不在此处向下时相比，多出来的增量为：

$$
T_k-S_k
= x+w+\max(y,z)-\bigl(\max(x,w)+\max(y,z)\bigr)
= x+w-\max(x,w)
= \min(x,w)
$$

也就是说：

> 若在第 $k$ 个小块内向下，那么相对“普通经过这个小块”的收益增量，恰好是
> $$
> \min(a_{0,2k},a_{1,2k+1})
> $$



### 分奇偶讨论整体答案



#### 1. 当 $n=1$

只有一列，没有任何交换，路径只能从 $(0,0)$ 向下到 $(1,0)$，答案就是：

$$
a_{0,0}+a_{1,0}
$$



#### 2. 当 $n$ 为偶数

设共有 $\frac n2$ 个完整小块。
因为路径一定在某个小块里向下，所以：

* 每个小块先都按“不在这里向下”的贡献加入基础答案；
* 然后枚举在哪个小块向下，额外加上该小块的增量。

于是答案为：

$$
\sum_k S_k + \max_k \min(a_{0,2k},a_{1,2k+1})
$$

其中

$$
S_k=\max(a_{0,2k},a_{1,2k+1})+\max(a_{0,2k+1},a_{1,2k})
$$



#### 3. 当 $n$ 为奇数

前面有若干个完整小块，最后还剩一列 $n-1$，这一列无法参与交换。

设最后一列为：

$$
a_{0,n-1},\ a_{1,n-1}
$$

这时有两种选择：

* 在前面的某个小块里向下
  那么最后一列只会经过下面那个格子，贡献是 $a_{1,n-1}$；
* 在最后一列向下
  那么最后一列会同时经过上下两个格子，额外多拿到 $a_{0,n-1}$。

所以答案为：

$$
\sum_k S_k + a_{1,n-1} + \max\left(a_{0,n-1},\ \max_k \min(a_{0,2k},a_{1,2k+1})\right)
$$



### 实现方法

直接线性扫描每个相邻列对 $(2k,2k+1)$：

1. 累加基础贡献
   $$
   \max(a_{0,2k},a_{1,2k+1})+\max(a_{0,2k+1},a_{1,2k})
   $$
2. 同时维护在这个小块里向下的额外收益
   $$
   \min(a_{0,2k},a_{1,2k+1})
   $$
   的最大值。
3. 最后按 $n$ 的奇偶性计算答案即可。

整套做法只需要一次遍历，复杂度非常合适。



## 复杂度分析

设一组数据的列数为 $n$。

* 时间复杂度：$O(n)$
  只需要遍历所有列对一次。
* 空间复杂度：$O(1)$（不计输入存储）
  只使用了若干个变量维护答案。

由于题目保证所有测试数据的 $n$ 之和不超过 $2\times 10^5$，因此该做法可以轻松通过。



## 代码实现

### Python

```python
import sys


# 计算单组测试数据的答案
def solve_case(n, row0, row1):
    # 特判 n=1，此时只能从上往下走
    if n == 1:
        return row0[0] + row1[0]

    # base 表示所有完整 2×2 小块按“普通经过”时的基础贡献之和
    base = 0
    # best_extra 表示选择某个完整小块作为“向下发生的小块”时，能获得的最大额外收益
    best_extra = 0

    # 枚举所有完整的小块：(0,1), (2,3), ...
    for j in range(0, n - 1, 2):
        # 当前小块四个位置：
        # x = row0[j], y = row0[j + 1]
        # z = row1[j], w = row1[j + 1]

        # 不在当前小块向下时，这个小块的最优贡献
        base += max(row0[j], row1[j + 1]) + max(row0[j + 1], row1[j])

        # 在当前小块向下时，相比普通经过会多出的收益
        best_extra = max(best_extra, min(row0[j], row1[j + 1]))

    # 若 n 为偶数，路径一定在某个完整小块里向下
    if n % 2 == 0:
        return base + best_extra

    # 若 n 为奇数，最后一列单独存在，无法交换
    # 可以选择：
    # 1. 在某个完整小块里向下，此时最后一列只能经过下方格子 row1[n - 1]
    # 2. 在最后一列向下，此时相当于在情况1的基础上额外多拿到 row0[n - 1]
    return base + row1[n - 1] + max(best_extra, row0[n - 1])


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    ans = []

    for _ in range(t):
        n = int(input().strip())
        row0 = list(map(int, input().split()))
        row1 = list(map(int, input().split()))
        ans.append(str(solve_case(n, row0, row1)))

    print("\n".join(ans))


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

    // 计算单组测试数据的答案
    public static long solveCase(int n, long[] row0, long[] row1) {
        // 特判 n=1，此时路径只能从上格走到下格
        if (n == 1) {
            return row0[0] + row1[0];
        }

        // base 表示所有完整 2×2 小块按“普通经过”时的基础贡献总和
        long base = 0;
        // bestExtra 表示选择某个完整小块作为向下位置时，能获得的最大额外收益
        long bestExtra = 0;

        // 枚举所有完整的小块：(0,1), (2,3), ...
        for (int j = 0; j + 1 < n; j += 2) {
            // 当前小块不作为向下位置时的最优贡献
            base += Math.max(row0[j], row1[j + 1]) + Math.max(row0[j + 1], row1[j]);

            // 当前小块作为向下位置时，相比普通经过多出的收益
            bestExtra = Math.max(bestExtra, Math.min(row0[j], row1[j + 1]));
        }

        // n 为偶数时，路径一定在某个完整小块里向下
        if (n % 2 == 0) {
            return base + bestExtra;
        }

        // n 为奇数时，最后一列无法交换
        // 若在前面某个小块向下，最后一列只能取到底部格子 row1[n-1]
        // 若在最后一列向下，则还能额外多取到顶部格子 row0[n-1]
        return base + row1[n - 1] + Math.max(bestExtra, row0[n - 1]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();

        int t = Integer.parseInt(br.readLine().trim());

        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());

            long[] row0 = new long[n];
            long[] row1 = new long[n];

            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                row0[i] = Long.parseLong(st.nextToken());
            }

            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                row1[i] = Long.parseLong(st.nextToken());
            }

            out.append(solveCase(n, row0, row1)).append('\n');
        }

        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 计算单组测试数据的答案
long long solveCase(int n, const vector<long long>& row0, const vector<long long>& row1) {
    // 特判 n=1，此时路径只能从上格走到下格
    if (n == 1) {
        return row0[0] + row1[0];
    }

    // base 表示所有完整 2×2 小块按“普通经过”时的基础贡献总和
    long long base = 0;
    // bestExtra 表示选择某个完整小块作为向下位置时，能获得的最大额外收益
    long long bestExtra = 0;

    // 枚举所有完整的小块：(0,1), (2,3), ...
    for (int j = 0; j + 1 < n; j += 2) {
        // 当前小块不作为向下位置时的最优贡献
        base += max(row0[j], row1[j + 1]) + max(row0[j + 1], row1[j]);

        // 当前小块作为向下位置时，相比普通经过多出的收益
        bestExtra = max(bestExtra, min(row0[j], row1[j + 1]));
    }

    // n 为偶数时，路径一定在某个完整小块里向下
    if (n % 2 == 0) {
        return base + bestExtra;
    }

    // n 为奇数时，最后一列无法交换
    // 若在前面某个小块向下，最后一列只能取到底部格子 row1[n-1]
    // 若在最后一列向下，则还能额外多取到顶部格子 row0[n-1]
    return base + row1[n - 1] + max(bestExtra, row0[n - 1]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<long long> row0(n), row1(n);
        for (int i = 0; i < n; i++) {
            cin >> row0[i];
        }
        for (int i = 0; i < n; i++) {
            cin >> row1[i];
        }

        cout << solveCase(n, row0, row1) << '\n';
    }

    return 0;
}
```