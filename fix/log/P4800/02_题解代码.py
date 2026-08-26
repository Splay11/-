## 解题思路

对于固定的样本 $i$，题目要求计算每个 $j$ 对应的

$$
R(i,j)= \#\{ k \ne i,j \mid D(i,k) \le D(i,j) \}
$$

把它换一种等价的理解会更直接：

对于固定样本 $i$，只关心其它所有样本与 $i$ 的差异度。
若某个样本 $j$ 与 $i$ 的差异度为 $D(i,j)$，那么所有满足与 $i$ 的差异度 $\le D(i,j)$ 的样本（不包括 $i$）都会被统计进去，但要去掉 $j$ 自己，因此：

$$
R(i,j) = \bigl(\#{k\ne i \mid D(i,k)\le D(i,j)}\bigr)-1
$$

也就是说，问题本质上是：

* 对每个固定的样本 $i$；
* 将所有 $j\ne i$ 按照与 $i$ 的差异度从小到大排序；
* 若若干个样本差异度相同，它们对应的答案也相同。

### 核心思路

对于每个样本 $i$：

1. 枚举所有 $j\ne i$，计算差异度
   $$
   D(i,j)=(p_i-p_j)^2+(q_i-q_j)^2
   $$

2. 将这些样本按差异度从小到大排序。

3. 对排序后的数组按“相同差异度”分组。
   假设某一组在排序后的位置范围是 $[l,r]$（下标从 $0$ 开始），那么这一组任意样本 $j$ 的满足 $\le$ 当前差异度的样本一共有 $r+1$ 个（包含它自己），因此：

   $$
   R(i,j)=r
   $$

   因为要去掉 $j$ 自己 $1$ 个。

4. 最后令 $R(i,i)=0$。

### 为什么这样做是对的

对固定的样本 $i$，设某个样本 $j$ 在排序后属于某个差异度相同的分组，其最后一个位置是 $r$。

* 排序中前 $r+1$ 个样本，恰好就是所有满足
  $$
  D(i,k)\le D(i,j)
  $$
  的样本（不含 $i$）。
* 其中包含样本 $j$ 自己。
* 题目要求统计除 $i,j$ 外的样本数，所以答案就是
  $$
  (r+1)-1=r
  $$

因此同一差异度组内所有样本答案都相同，且都等于该组最后一个位置下标。

### 实现方法

* 用一个二维数组 `ans` 保存答案。
* 外层枚举固定的样本 $i$。
* 内层收集所有 $(\text{差异度}, \text{样本编号})$。
* 排序后双指针或分组扫描处理相同差异度。
* 将当前组内所有样本的答案统一赋值为当前组结束位置下标。

这样即可在满足数据范围的前提下高效求解。



## 复杂度分析

对于每组数据：

* 对每个样本 $i$，需要计算 $n-1$ 个差异度并排序，复杂度为 $O(n\log n)$；
* 一共做 $n$ 次，因此总时间复杂度为：

$$
O(n^2\log n)
$$

空间复杂度：

* 结果数组需要 $O(n^2)$；
* 排序时临时数组需要 $O(n)$；

所以总空间复杂度为：

$$
O(n^2)
$$




## 代码实现

### Python

```python
import sys


def solve_case(points):
    # 样本的数量
    n = len(points)

    # ans[i][j] 表示题目要求的 R(i,j)
    ans = [[0] * n for _ in range(n)]

    # 依次固定样本 i
    for i in range(n):
        dist_list = []

        xi, yi = points[i]

        # 计算其它所有样本与 i 的差异度
        for j in range(n):
            if i == j:
                continue
            xj, yj = points[j]
            dx = xi - xj
            dy = yi - yj
            d2 = dx * dx + dy * dy
            dist_list.append((d2, j))

        # 按差异度从小到大排序
        dist_list.sort()

        # 按相同差异度分组处理
        m = len(dist_list)
        l = 0
        while l < m:
            r = l
            # 找到与 dist_list[l] 差异度相同的这一整组
            while r + 1 < m and dist_list[r + 1][0] == dist_list[l][0]:
                r += 1

            # 这一组中任意样本 j 的答案都是 r
            for k in range(l, r + 1):
                j = dist_list[k][1]
                ans[i][j] = r

            l = r + 1

    return ans


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    out = []

    for _ in range(t):
        n = int(input().strip())
        points = []
        for _ in range(n):
            x, y = map(int, input().split())
            points.append((x, y))

        ans = solve_case(points)

        for i in range(n):
            out.append(' '.join(map(str, ans[i])))

    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.StringTokenizer;

public class Main {

    // 用来保存“差异度 + 样本编号”
    static class Node implements Comparable<Node> {
        long dist;
        int idx;

        Node(long dist, int idx) {
            this.dist = dist;
            this.idx = idx;
        }

        @Override
        public int compareTo(Node other) {
            return Long.compare(this.dist, other.dist);
        }
    }

    // 返回一组测试数据的答案矩阵
    static int[][] solveCase(long[][] points) {
        int n = points.length;
        int[][] ans = new int[n][n];

        // 依次固定样本 i
        for (int i = 0; i < n; i++) {
            ArrayList<Node> list = new ArrayList<>();

            long xi = points[i][0];
            long yi = points[i][1];

            // 计算其它样本与 i 的差异度
            for (int j = 0; j < n; j++) {
                if (i == j) {
                    continue;
                }
                long dx = xi - points[j][0];
                long dy = yi - points[j][1];
                long d2 = dx * dx + dy * dy;
                list.add(new Node(d2, j));
            }

            // 按差异度从小到大排序
            Collections.sort(list);

            // 按相同差异度分组处理
            int m = list.size();
            int l = 0;
            while (l < m) {
                int r = l;

                // 找到同一差异度的一整组
                while (r + 1 < m && list.get(r + 1).dist == list.get(l).dist) {
                    r++;
                }

                // 这一组中所有样本的答案都为 r
                for (int k = l; k <= r; k++) {
                    int j = list.get(k).idx;
                    ans[i][j] = r;
                }

                l = r + 1;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());

        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            long[][] points = new long[n][2];

            // 读入所有样本特征
            for (int i = 0; i < n; i++) {
                StringTokenizer st = new StringTokenizer(br.readLine());
                points[i][0] = Long.parseLong(st.nextToken());
                points[i][1] = Long.parseLong(st.nextToken());
            }

            int[][] ans = solveCase(points);

            // 输出答案矩阵
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (j > 0) {
                        sb.append(' ');
                    }
                    sb.append(ans[i][j]);
                }
                sb.append('\n');
            }
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 用来保存“差异度 + 样本编号”
struct Node {
    long long dist;
    int idx;

    bool operator < (const Node& other) const {
        return dist < other.dist;
    }
};

// 返回一组测试数据的答案矩阵
vector<vector<int>> solve_case(const vector<pair<long long, long long>>& points) {
    int n = (int)points.size();
    vector<vector<int>> ans(n, vector<int>(n, 0));

    // 依次固定样本 i
    for (int i = 0; i < n; i++) {
        vector<Node> dist_list;
        long long xi = points[i].first;
        long long yi = points[i].second;

        // 计算其它所有样本与 i 的差异度
        for (int j = 0; j < n; j++) {
            if (i == j) {
                continue;
            }
            long long dx = xi - points[j].first;
            long long dy = yi - points[j].second;
            long long d2 = dx * dx + dy * dy;
            dist_list.push_back({d2, j});
        }

        // 按差异度从小到大排序
        sort(dist_list.begin(), dist_list.end());

        // 按相同差异度分组处理
        int m = (int)dist_list.size();
        int l = 0;
        while (l < m) {
            int r = l;

            // 找到差异度相同的一整组
            while (r + 1 < m && dist_list[r + 1].dist == dist_list[l].dist) {
                r++;
            }

            // 这一组内所有样本的答案都为 r
            for (int k = l; k <= r; k++) {
                int j = dist_list[k].idx;
                ans[i][j] = r;
            }

            l = r + 1;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<pair<long long, long long>> points(n);

        // 读入所有样本特征
        for (int i = 0; i < n; i++) {
            cin >> points[i].first >> points[i].second;
        }

        vector<vector<int>> ans = solve_case(points);

        // 输出答案矩阵
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (j > 0) {
                    cout << ' ';
                }
                cout << ans[i][j];
            }
            cout << '\n';
        }
    }

    return 0;
}
```