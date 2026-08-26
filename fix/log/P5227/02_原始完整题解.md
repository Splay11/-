## 解题思路

将每棵已有节点能够覆盖的范围转化为区间：

$[x_i-c_i,\ x_i+c_i]$

由于只需要覆盖通道 $[0,L]$，因此将区间限制在：

$[\max(0,x_i-c_i),\ \min(L,x_i+c_i)]$

使用排序 + 贪心。

先按照已有区间的左端点从小到大排序，并维护变量 $right$，表示当前从 $0$ 开始已经连续覆盖到的最右位置。

依次处理区间 $[l,r]$：

* 如果 $r\le right$，说明这个区间完全位于已经覆盖的部分中，直接跳过。
* 如果 $l\le right$，说明当前区间能够和已经覆盖的部分连接起来，将 $right$ 更新为 $\max(right,r)$。
* 如果 $l>right$，说明 $[right,l]$ 之间存在未覆盖区域。每棵新节点最多能够连续覆盖长度 $2D$，因此至少需要：

$$
cnt=\left\lceil\frac{l-right}{2D}\right\rceil
$$

棵新节点。

为了让新增节点尽可能向右覆盖，直接从当前 $right$ 开始连续放置这些节点。加入 $cnt$ 棵后，可以将覆盖位置推进到：

$$
right+cnt\cdot 2D
$$

随后再利用当前已有区间，将 $right$ 更新为二者的较大值。

这种做法的核心是贪心：对于当前最左侧尚未覆盖的位置，一棵新节点在覆盖它的前提下，应当尽可能向右放置，这样能够覆盖最远的位置，不会使后续情况变差。

所有已有区间处理完成后，如果还有 $[right,L]$ 没有覆盖，再补：

$$
\left\lceil\frac{L-right}{2D}\right\rceil
$$

棵节点即可。

需要注意，不能简单将所有未覆盖区间分别计算答案后相加。因为一棵新增节点可能跨过一段已经被旧节点覆盖的区域，同时覆盖其左右两侧，因此必须按照上述方式维护连续覆盖到的最右位置。

## 复杂度分析

对 $m$ 个已有覆盖区间进行排序，时间复杂度为 $O(m\log m)$。

之后只需要线性遍历一次，时间复杂度为 $O(m)$。

因此总时间复杂度为：

$O(m\log m)$

存储 $m$ 个区间，空间复杂度为：

$O(m)$

在 $m\le 100000$ 的数据范围内可以顺利通过。

## 代码实现

### Python

```python
def min_trees(L, m, D, trees):
    intervals = []

    # 将已有节点转化为覆盖区间
    for x, c in trees:
        left = max(0, x - c)
        right = min(L, x + c)
        intervals.append((left, right))

    # 按左端点排序
    intervals.sort()

    right = 0
    ans = 0
    length = 2 * D

    for left, end in intervals:
        # 当前区间已经完全被覆盖
        if end <= right:
            continue

        # 中间存在空缺，需要新增节点
        if left > right:
            need = (left - right + length - 1) // length
            ans += need
            right += need * length

        # 利用已有区间继续向右扩展
        if end > right:
            right = end

        if right >= L:
            break

    # 处理最后剩余的未覆盖部分
    if right < L:
        ans += (L - right + length - 1) // length

    return ans


def main():
    L, m, D = map(int, input().split())

    trees = []
    for _ in range(m):
        x, c = map(int, input().split())
        trees.append((x, c))

    print(min_trees(L, m, D, trees))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    static long minTrees(long L, int m, long D, long[][] trees) {
        long[][] intervals = new long[m][2];

        // 将已有节点转化为覆盖区间
        for (int i = 0; i < m; i++) {
            long x = trees[i][0];
            long c = trees[i][1];

            intervals[i][0] = Math.max(0, x - c);
            intervals[i][1] = Math.min(L, x + c);
        }

        // 按区间左端点排序
        Arrays.sort(intervals, new Comparator<long[]>() {
            public int compare(long[] a, long[] b) {
                return Long.compare(a[0], b[0]);
            }
        });

        long right = 0;
        long ans = 0;
        long length = 2 * D;

        for (int i = 0; i < m; i++) {
            long left = intervals[i][0];
            long end = intervals[i][1];

            // 当前区间已经完全被覆盖
            if (end <= right) {
                continue;
            }

            // 中间存在空缺，需要新增节点
            if (left > right) {
                long need = (left - right + length - 1) / length;
                ans += need;
                right += need * length;
            }

            // 利用已有区间继续向右扩展
            if (end > right) {
                right = end;
            }

            if (right >= L) {
                break;
            }
        }

        // 处理最后剩余的未覆盖部分
        if (right < L) {
            ans += (L - right + length - 1) / length;
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        StringTokenizer st = new StringTokenizer(br.readLine());
        long L = Long.parseLong(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        long D = Long.parseLong(st.nextToken());

        long[][] trees = new long[m][2];

        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            trees[i][0] = Long.parseLong(st.nextToken());
            trees[i][1] = Long.parseLong(st.nextToken());
        }

        System.out.println(minTrees(L, m, D, trees));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long minTrees(long long L, int m, long long D,
                   vector<pair<long long, long long>>& trees) {
    vector<pair<long long, long long>> intervals;

    // 将已有节点转化为覆盖区间
    for (auto tree : trees) {
        long long x = tree.first;
        long long c = tree.second;

        long long left = max(0LL, x - c);
        long long right = min(L, x + c);

        intervals.push_back({left, right});
    }

    // 按左端点排序
    sort(intervals.begin(), intervals.end());

    long long right = 0;
    long long ans = 0;
    long long length = 2 * D;

    for (auto interval : intervals) {
        long long left = interval.first;
        long long end = interval.second;

        // 当前区间已经完全被覆盖
        if (end <= right) {
            continue;
        }

        // 中间存在空缺，需要新增节点
        if (left > right) {
            long long need = (left - right + length - 1) / length;
            ans += need;
            right += need * length;
        }

        // 利用已有区间继续向右扩展
        if (end > right) {
            right = end;
        }

        if (right >= L) {
            break;
        }
    }

    // 处理最后剩余的未覆盖部分
    if (right < L) {
        ans += (L - right + length - 1) / length;
    }

    return ans;
}

int main() {
    long long L, D;
    int m;

    cin >> L >> m >> D;

    vector<pair<long long, long long>> trees(m);

    for (int i = 0; i < m; i++) {
        cin >> trees[i].first >> trees[i].second;
    }

    cout << minTrees(L, m, D, trees) << '\n';

    return 0;
}
```