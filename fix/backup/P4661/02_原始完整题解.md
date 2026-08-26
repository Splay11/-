## 解题思路

因为 $p,q$ 都是 $1\sim n$ 的排列，所以每个数字只出现一次。

设数字 $x$ 在排列 $p$ 中的位置为 $posP[x]$，在排列 $q$ 中的位置为 $posQ[x]$。

如果一个序列是公共子序列，那么它对应的每个数字在两个排列中的出现位置都必须同时严格递增。

现在题目要求的是：在所有公共子序列中，找到字典序最大的那一条。

核心贪心思想如下：

1. 当前已经选到两个排列的位置分别为 $i,j$，接下来只能从

   * $p$ 的后缀 $[i,n]$
   * $q$ 的后缀 $[j,n]$

   中继续选数。

2. 一个数字 $x$ 还能被继续选，当且仅当：
   $$
   posP[x]\ge i \quad 且 \quad posQ[x]\ge j
   $$

3. 为了让字典序最大，下一位一定要尽量大。
   所以每一步都应当选择当前还能选的最大数字。

4. 选完数字 $x$ 后，后续只能在它之后继续选，于是更新：
   $$
   i=posP[x]+1,\quad j=posQ[x]+1
   $$

5. 由于我们每次都只关心“当前还能选的最大数字”，可以直接从 $n$ 到 $1$ 扫描一遍。
   如果某个数字 $x$ 在当前条件下可选，就加入答案并更新位置。

为什么这样扫描是对的？

* 每一步选当前可选的最大数字，这是字典序贪心。
* 如果某个较小数字在当前时刻都不能选，那么之后 $i,j$ 只会变大，它更不可能再变得可选，所以不会漏答案。
* 因此从大到小扫描一次即可完成。

这里用到的算法本质是：

* 位置预处理
* 贪心
* 一次线性扫描

## 复杂度分析

预处理两个位置数组需要 $O(n)$。

之后从 $n$ 到 $1$ 扫描一次，每个数字只判断一次，因此也是 $O(n)$。

所以总时间复杂度为：
$$
O(n)
$$

额外使用了位置数组和答案数组，空间复杂度为：
$$
O(n)
$$

这个复杂度对于 $n\le 2\times 10^5$ 是完全可行的。

## 代码实现

### Python

```python
def solve(n, p, q):
    # 记录每个数字在 p 和 q 中的位置（下标从 1 开始）
    posP = [0] * (n + 1)
    posQ = [0] * (n + 1)

    for i in range(n):
        posP[p[i]] = i + 1
        posQ[q[i]] = i + 1

    ans = []
    i, j = 1, 1  # 当前在两个排列中允许选择的最早位置

    # 从大到小扫描，贪心选择当前还能选的最大数字
    for x in range(n, 0, -1):
        if posP[x] >= i and posQ[x] >= j:
            ans.append(x)
            # 更新后续可选位置
            i = posP[x] + 1
            j = posQ[x] + 1

    return ans


def main():
    n = int(input())
    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    ans = solve(n, p, q)

    print(len(ans))
    print(*ans)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    public static List<Integer> solve(int n, int[] p, int[] q) {
        // 记录每个数字在 p 和 q 中的位置（下标从 1 开始）
        int[] posP = new int[n + 1];
        int[] posQ = new int[n + 1];

        for (int i = 0; i < n; i++) {
            posP[p[i]] = i + 1;
            posQ[q[i]] = i + 1;
        }

        List<Integer> ans = new ArrayList<>();
        int i = 1, j = 1; // 当前在两个排列中允许选择的最早位置

        // 从大到小扫描，贪心选择当前还能选的最大数字
        for (int x = n; x >= 1; x--) {
            if (posP[x] >= i && posQ[x] >= j) {
                ans.add(x);
                // 更新后续可选位置
                i = posP[x] + 1;
                j = posQ[x] + 1;
            }
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] p = new int[n];
        int[] q = new int[n];

        for (int i = 0; i < n; i++) {
            p[i] = sc.nextInt();
        }
        for (int i = 0; i < n; i++) {
            q[i] = sc.nextInt();
        }

        List<Integer> ans = solve(n, p, q);

        System.out.println(ans.size());
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(ans.get(i));
        }
        System.out.println();

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

vector<int> solve(int n, const vector<int>& p, const vector<int>& q) {
    // 记录每个数字在 p 和 q 中的位置（下标从 1 开始）
    vector<int> posP(n + 1), posQ(n + 1);

    for (int i = 0; i < n; i++) {
        posP[p[i]] = i + 1;
        posQ[q[i]] = i + 1;
    }

    vector<int> ans;
    int i = 1, j = 1; // 当前在两个排列中允许选择的最早位置

    // 从大到小扫描，贪心选择当前还能选的最大数字
    for (int x = n; x >= 1; x--) {
        if (posP[x] >= i && posQ[x] >= j) {
            ans.push_back(x);
            // 更新后续可选位置
            i = posP[x] + 1;
            j = posQ[x] + 1;
        }
    }

    return ans;
}

int main() {
    int n;
    cin >> n;

    vector<int> p(n), q(n);
    for (int i = 0; i < n; i++) cin >> p[i];
    for (int i = 0; i < n; i++) cin >> q[i];

    vector<int> ans = solve(n, p, q);

    cout << ans.size() << "\n";
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << " ";
        cout << ans[i];
    }
    cout << "\n";

    return 0;
}
```