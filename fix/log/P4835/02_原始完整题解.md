## 解题思路

先把操作本质看清楚。

一次操作可以选择两个下标 $i,j$，如果 $a_i \mid a_j$ 或 $a_j \mid a_i$，就可以交换这两个位置上的数。
也就是说，能直接交换的两个数，必须满足“可整除”关系。

进一步考虑：

* 如果两个数不能直接交换，但它们能通过若干个数连起来，比如 $x \leftrightarrow y \leftrightarrow z$，其中每一对相邻数都满足可整除关系；
* 那么借助中间数，也可以把 $x$ 和 $z$ 的位置进行调整。

所以，本题的关键不是看两个数能不能直接交换，而是看它们是否处于同一个“可整除连通块”中。

### 核心结论

把当前序列中出现过的数看成点。
若两个数满足一个整除另一个，就在它们之间连边。

那么：

* 同一个连通块中的数，可以任意重排；
* 不同连通块之间的数，无法跨块交换。

于是问题就变成了：

1. 先求出所有数所属的连通块；
2. 对于同一个连通块中的所有位置，把这些位置上的数取出来；
3. 为了让整个序列字典序最小，应当：

   * 让这个连通块里最小的数放到最靠前的位置；
   * 次小的数放到次靠前的位置；
   * 依此类推。

这就是一个非常经典的“连通块内排序后贪心回填”。

### 相关算法

这里使用两个算法：

* 并查集：维护哪些数属于同一个连通块；
* 贪心：每个连通块内，位置升序、数值升序，再一一对应回填。

### 如何建边

数值范围满足 $1 \le a_i \le n$，因此可以直接按“倍数”枚举建边：

* 若数 $x$ 在序列中出现过；
* 就枚举它的倍数 $2x,3x,4x,\dots$；
* 如果某个倍数也在序列中出现过，就把它们并到同一个集合里。

这样就能把所有满足整除关系的数连起来。

### 实现方法

具体步骤如下：

1. 读入序列；
2. 统计哪些数出现过；
3. 用并查集把所有有整除关系的出现过的数合并；
4. 再遍历序列，把同一连通块中的：

   * 下标收集到一起；
   * 数值收集到一起；
5. 对每个连通块：

   * 下标排序；
   * 数值排序；
   * 按顺序回填；
6. 输出结果。

---

## 复杂度分析

设单组数据长度为 $n$。

### 时间复杂度

建边时，枚举所有出现过的数 $x$ 的倍数：

$\displaystyle \sum_{x=1}^{n}\frac{n}{x} = O(n\log n)$

后面分组排序的总复杂度为 $O(n\log n)$。

因此总时间复杂度为：

$O(n\log n)$

### 空间复杂度

并查集、出现标记、答案数组、分组存储等都只需线性空间。

总空间复杂度为：

$O(n)$

这个复杂度对于题目的数据范围是完全可行的。

---

## 代码实现

### Python

```python
import sys


# 并查集
class DSU:
    def __init__(self, n):
        self.fa = list(range(n + 1))

    def find(self, x):
        # 路径压缩
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def union(self, x, y):
        fx = self.find(x)
        fy = self.find(y)
        if fx != fy:
            self.fa[fy] = fx


# 处理一组测试数据，返回字典序最小的结果
def solve_case(n, a):
    dsu = DSU(n)
    exist = [False] * (n + 1)

    # 标记哪些数出现过
    for x in a:
        exist[x] = True

    # 按倍数枚举，把有整除关系的数合并
    for x in range(1, n + 1):
        if not exist[x]:
            continue
        multiple = x * 2
        while multiple <= n:
            if exist[multiple]:
                dsu.union(x, multiple)
            multiple += x

    # 按连通块收集位置和数值
    pos_group = {}
    val_group = {}

    for i, x in enumerate(a):
        root = dsu.find(x)
        if root not in pos_group:
            pos_group[root] = []
            val_group[root] = []
        pos_group[root].append(i)
        val_group[root].append(x)

    # 每个连通块内：位置排序、数值排序，然后贪心回填
    ans = a[:]
    for root in pos_group:
        pos_group[root].sort()
        val_group[root].sort()
        for i in range(len(pos_group[root])):
            ans[pos_group[root][i]] = val_group[root][i]

    return ans


def main():
    data = list(map(int, sys.stdin.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + n]
        idx += n

        ans = solve_case(n, a)
        out.append(" ".join(map(str, ans)))

    print("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    // 并查集
    static class DSU {
        int[] fa;

        DSU(int n) {
            fa = new int[n + 1];
            for (int i = 0; i <= n; i++) {
                fa[i] = i;
            }
        }

        int find(int x) {
            // 路径压缩
            if (fa[x] != x) {
                fa[x] = find(fa[x]);
            }
            return fa[x];
        }

        void union(int x, int y) {
            int fx = find(x);
            int fy = find(y);
            if (fx != fy) {
                fa[fy] = fx;
            }
        }
    }

    // 处理一组测试数据，返回答案
    static int[] solveCase(int n, int[] a) {
        DSU dsu = new DSU(n);
        boolean[] exist = new boolean[n + 1];

        // 标记出现过的数
        for (int x : a) {
            exist[x] = true;
        }

        // 按倍数枚举建边
        for (int x = 1; x <= n; x++) {
            if (!exist[x]) continue;
            for (int multiple = x * 2; multiple <= n; multiple += x) {
                if (exist[multiple]) {
                    dsu.union(x, multiple);
                }
            }
        }

        // 按连通块分组：位置和数值分别存储
        HashMap<Integer, ArrayList<Integer>> posGroup = new HashMap<>();
        HashMap<Integer, ArrayList<Integer>> valGroup = new HashMap<>();

        for (int i = 0; i < n; i++) {
            int root = dsu.find(a[i]);

            posGroup.putIfAbsent(root, new ArrayList<>());
            valGroup.putIfAbsent(root, new ArrayList<>());

            posGroup.get(root).add(i);
            valGroup.get(root).add(a[i]);
        }

        int[] ans = a.clone();

        // 每个连通块内排序后回填
        for (int root : posGroup.keySet()) {
            ArrayList<Integer> posList = posGroup.get(root);
            ArrayList<Integer> valList = valGroup.get(root);

            Collections.sort(posList);
            Collections.sort(valList);

            for (int i = 0; i < posList.size(); i++) {
                ans[posList.get(i)] = valList.get(i);
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();
        while (T-- > 0) {
            int n = fs.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = fs.nextInt();
            }

            int[] ans = solveCase(n, a);
            for (int i = 0; i < n; i++) {
                if (i > 0) sb.append(' ');
                sb.append(ans[i]);
            }
            sb.append('\n');
        }

        System.out.print(sb.toString());
    }

    // 由于数据较大，这里使用较快的输入方式
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        int nextInt() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + c - '0';
                c = read();
            }
            return val * sign;
        }
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

// 并查集
struct DSU {
    vector<int> fa;

    DSU(int n) {
        fa.resize(n + 1);
        for (int i = 0; i <= n; i++) {
            fa[i] = i;
        }
    }

    int find(int x) {
        // 路径压缩
        if (fa[x] != x) {
            fa[x] = find(fa[x]);
        }
        return fa[x];
    }

    void unite(int x, int y) {
        int fx = find(x);
        int fy = find(y);
        if (fx != fy) {
            fa[fy] = fx;
        }
    }
};

// 处理一组测试数据，返回答案
vector<int> solveCase(int n, const vector<int>& a) {
    DSU dsu(n);
    vector<bool> exist(n + 1, false);

    // 标记出现过的数
    for (int x : a) {
        exist[x] = true;
    }

    // 按倍数枚举，把有整除关系的数合并
    for (int x = 1; x <= n; x++) {
        if (!exist[x]) continue;
        for (int multiple = x * 2; multiple <= n; multiple += x) {
            if (exist[multiple]) {
                dsu.unite(x, multiple);
            }
        }
    }

    // 按连通块收集位置和数值
    unordered_map<int, vector<int>> posGroup;
    unordered_map<int, vector<int>> valGroup;

    for (int i = 0; i < n; i++) {
        int root = dsu.find(a[i]);
        posGroup[root].push_back(i);
        valGroup[root].push_back(a[i]);
    }

    vector<int> ans = a;

    // 每个连通块内部排序，再贪心回填
    for (auto& entry : posGroup) {
        int root = entry.first;
        vector<int>& posList = entry.second;
        vector<int>& valList = valGroup[root];

        sort(posList.begin(), posList.end());
        sort(valList.begin(), valList.end());

        for (int i = 0; i < (int)posList.size(); i++) {
            ans[posList[i]] = valList[i];
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
        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        vector<int> ans = solveCase(n, a);
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }

    return 0;
}
```