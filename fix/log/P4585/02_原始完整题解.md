## 解题思路

先设前缀和数组为 $pre$，其中

$$
pre[i]=a_1+a_2+\cdots+a_i
$$

并约定 $pre[0]=0$。

对于一个区间 $[l,r]$，如果要在位置 $mid$ 处切开，题意要求满足：

$$
\sum_{i=l}^{mid-1} a_i = \sum_{i=mid}^{r} a_i
$$

把它转成前缀和形式：

$$
pre[mid-1]-pre[l-1]=pre[r]-pre[mid-1]
$$

整理可得：

$$
pre[mid-1]=\frac{pre[l-1]+pre[r]}{2}
$$

也就是说，若区间 $[l,r]$ 可以切割，那么一定存在某个下标 $k=mid-1$，满足：

$$
pre[k]=pre[l-1]+\frac{pre[r]-pre[l-1]}{2}
$$

其中 $k \in [l,r-1]$。

### 核心性质

题目中给出：

$$
1 \le a_i \le 10^9
$$

因此数组元素全为正数，所以前缀和数组严格递增。

这会带来两个重要结论：

1. 对于固定区间 $[l,r]$，若存在合法切点，则切点唯一。
2. 可以在前缀和数组中用二分查找判断是否存在这个切点。

### 状态转移

定义 $f(l,r)$ 表示区间 $[l,r]$ 最多还能切多少次。

若区间长度不超过 $2$，显然不能切：

$$
r-l+1 \le 2 \Rightarrow f(l,r)=0
$$

若区间总和为奇数，也不可能平分：

$$
(pre[r]-pre[l-1]) \bmod 2 = 1 \Rightarrow f(l,r)=0
$$

否则，设能找到唯一切点 $k$，其中左半段是 $[l,k]$，右半段是 $[k+1,r]$，那么有：

$$
f(l,r)=1+f(l,k)+f(k+1,r)
$$

因为切开后左右两段互不影响，之后能切多少次就是左右子问题之和，再加上当前这一次切割。

### 实现方法

为了避免递归层数过深，可以用栈来模拟分治过程。

具体做法：

1. 先求前缀和数组；
2. 栈中维护待处理区间；
3. 每次弹出一个区间 $[l,r]$：

   * 若区间长度 $\le 2$，跳过；
   * 若区间和为奇数，跳过；
   * 否则计算目标值

   $$
   target=pre[l-1]+\frac{pre[r]-pre[l-1]}{2}
   $$

   * 在前缀和数组的 $[l,r-1]$ 范围内二分查找是否存在 $pre[k]=target$；
   * 若存在，则答案加 $1$，并把左右子区间压栈继续处理。

涉及的相关算法有：

* 前缀和
* 二分查找
* 栈模拟分治

## 复杂度分析

设数组长度为 $n$。

每个区间在处理时，主要做一次二分查找，复杂度为 $O(\log n)$。

整个切割过程形成一棵二叉分治树。每次成功切割会新增两个子区间，因此总处理区间数是线性的，即 $O(n)$ 级别。

所以总时间复杂度为：

$$
O(n \log n)
$$

空间方面：

* 前缀和数组需要 $O(n)$
* 栈最坏需要 $O(n)$

所以空间复杂度为：

$$
O(n)
$$


## 代码实现

### Python

```python
import sys
from bisect import bisect_left


# 计算最多切割次数
def max_cuts(arr):
    n = len(arr)

    # pre[i] 表示前 i 个元素的前缀和
    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + arr[i - 1]

    # 栈中维护当前待处理的区间 [l, r]
    stack = [(1, n)]
    ans = 0

    while stack:
        l, r = stack.pop()

        # 只有长度严格大于 2 的区间才能切割
        if r - l + 1 <= 2:
            continue

        # 当前区间和
        total = pre[r] - pre[l - 1]

        # 区间和为奇数，不可能平分
        if total % 2 == 1:
            continue

        # 目标前缀和值
        target = pre[l - 1] + total // 2

        # 在 [l, r - 1] 中二分查找切点 k
        k = bisect_left(pre, target, l, r)

        # 找到合法切点，则当前区间可以切一次
        if k < r and pre[k] == target:
            ans += 1
            stack.append((l, k))
            stack.append((k + 1, r))

    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())
    arr = list(map(int, input().split()))
    print(max_cuts(arr))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.StringTokenizer;

public class Main {

    // 计算最多切割次数
    public static int maxCuts(int[] arr) {
        int n = arr.length;

        // pre[i] 表示前 i 个元素的前缀和
        long[] pre = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            pre[i] = pre[i - 1] + arr[i - 1];
        }

        // 栈中维护当前待处理的区间 [l, r]
        ArrayDeque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{1, n});

        int ans = 0;

        while (!stack.isEmpty()) {
            int[] cur = stack.pop();
            int l = cur[0];
            int r = cur[1];

            // 只有长度严格大于 2 的区间才能切割
            if (r - l + 1 <= 2) {
                continue;
            }

            // 当前区间和
            long total = pre[r] - pre[l - 1];

            // 区间和为奇数，不可能平分
            if ((total & 1L) == 1L) {
                continue;
            }

            // 目标前缀和值
            long target = pre[l - 1] + total / 2;

            // 在 [l, r - 1] 中二分查找切点 k
            int left = l;
            int right = r - 1;
            int k = -1;

            while (left <= right) {
                int mid = left + (right - left) / 2;
                if (pre[mid] == target) {
                    k = mid;
                    break;
                } else if (pre[mid] < target) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }

            // 找到合法切点，则当前区间可以切一次
            if (k != -1) {
                ans++;
                stack.push(new int[]{l, k});
                stack.push(new int[]{k + 1, r});
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine().trim());
        int[] arr = new int[n];

        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }

        System.out.println(maxCuts(arr));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <stack>
using namespace std;

// 计算最多切割次数
int maxCuts(const vector<int>& arr) {
    int n = (int)arr.size();

    // pre[i] 表示前 i 个元素的前缀和
    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        pre[i] = pre[i - 1] + arr[i - 1];
    }

    // 栈中维护当前待处理的区间 [l, r]
    stack<pair<int, int>> st;
    st.push({1, n});

    int ans = 0;

    while (!st.empty()) {
        pair<int, int> cur = st.top();
        st.pop();

        int l = cur.first;
        int r = cur.second;

        // 只有长度严格大于 2 的区间才能切割
        if (r - l + 1 <= 2) {
            continue;
        }

        // 当前区间和
        long long total = pre[r] - pre[l - 1];

        // 区间和为奇数，不可能平分
        if (total & 1LL) {
            continue;
        }

        // 目标前缀和值
        long long target = pre[l - 1] + total / 2;

        // 在 [l, r - 1] 中二分查找切点 k
        int left = l;
        int right = r - 1;
        int k = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (pre[mid] == target) {
                k = mid;
                break;
            } else if (pre[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        // 找到合法切点，则当前区间可以切一次
        if (k != -1) {
            ans++;
            st.push({l, k});
            st.push({k + 1, r});
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    cout << maxCuts(arr) << '\n';
    return 0;
}
```