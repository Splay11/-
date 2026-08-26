## 解题思路

题意可以概括为：

给定一个长度为 $n$ 的序列，进行 $m$ 轮操作。
每一轮都删除当前序列中的最小值；如果最小值有多个，就删除下标最小的那个。
最后输出剩余序列。

### 核心思路

这道题如果直接模拟删除过程，每次都在当前序列中找最小值，那么时间复杂度至少是 $O(nm)$，在数据范围下显然无法通过。

注意到删除规则有两个优先级：

1. 先按数值从小到大删除
2. 同一个数值内部，按原下标从小到大删除

也就是说，整个删除过程实际上等价于：

* 把所有元素按 $(a_i,\ i)$ 的字典序排序
* 删除前 $m$ 个元素
* 剩下的元素按照原顺序输出

但是如果真的排序，复杂度是 $O(n \log n)$。这题还有一个非常关键的条件：

$$
1 \le a_i \le n
$$

因此数值范围不大，可以直接按值分桶。

### 实现方法

对于每组数据：

1. 建立 $n+1$ 个桶，`bucket[x]` 存储值为 $x$ 的所有下标
2. 按原顺序扫描数组，把每个位置加入对应桶中
   由于扫描顺序就是下标从小到大，所以同一个桶里的下标天然有序
3. 从值 $1$ 到值 $n$ 依次处理：

   * 如果当前桶大小 $\le m$，说明这一整桶都要删除
   * 否则，只删除当前桶中前 $m$ 个下标，然后停止
4. 用一个布尔数组记录哪些位置被删除
5. 最后按原数组顺序输出所有未删除元素

这样就严格符合题目的删除规则，因为：

* 先处理更小的值，保证“每次删除当前最小值”
* 同值时桶中下标天然递增，保证“删除下标最小的那个”

## 复杂度分析

设一组数据长度为 $n$。

* 建桶时，每个元素进入一次桶，复杂度为 $O(n)$
* 遍历值域 $1 \sim n$，总共处理的下标数量不超过 $n$，复杂度为 $O(n)$
* 最后输出剩余元素，复杂度为 $O(n)$

因此总时间复杂度为：

$$
O(n)
$$

空间复杂度为：

$$
O(n)
$$

## 代码实现

### Python

```python
import sys


def solve_case(n, m, arr):
    # bucket[x] 存储所有值为 x 的元素下标（从小到大）
    buckets = [[] for _ in range(n + 1)]

    # 按原下标顺序放入桶中
    for i in range(n):
        buckets[arr[i]].append(i)

    # removed[i] 表示原数组下标 i 的元素是否被删除
    removed = [False] * n

    # 按值从小到大删除
    for value in range(1, n + 1):
        if m == 0:
            break

        size = len(buckets[value])

        # 如果当前值的所有元素都要被删除
        if size <= m:
            for idx in buckets[value]:
                removed[idx] = True
            m -= size
        else:
            # 只删除当前值中下标最小的前 m 个
            for i in range(m):
                removed[buckets[value][i]] = True
            m = 0
            break

    # 按原顺序收集未删除元素
    ans = []
    for i in range(n):
        if not removed[i]:
            ans.append(str(arr[i]))

    return " ".join(ans)


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    res = []

    for _ in range(t):
        n, m = map(int, input().split())
        arr = list(map(int, input().split()))
        res.append(solve_case(n, m, arr))

    sys.stdout.write("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {

    // 处理一组测试数据，返回最终序列
    public static String solveCase(int n, int m, int[] arr) {
        // buckets[x] 存储所有值为 x 的元素下标（从小到大）
        List<Integer>[] buckets = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            buckets[i] = new ArrayList<>();
        }

        // 按原下标顺序放入桶中
        for (int i = 0; i < n; i++) {
            buckets[arr[i]].add(i);
        }

        // removed[i] 表示原数组下标 i 的元素是否被删除
        boolean[] removed = new boolean[n];

        // 按值从小到大删除
        for (int value = 1; value <= n && m > 0; value++) {
            int size = buckets[value].size();

            // 如果当前值的所有元素都要被删除
            if (size <= m) {
                for (int idx : buckets[value]) {
                    removed[idx] = true;
                }
                m -= size;
            } else {
                // 只删除当前值中下标最小的前 m 个
                for (int i = 0; i < m; i++) {
                    removed[buckets[value].get(i)] = true;
                }
                m = 0;
                break;
            }
        }

        // 按原顺序收集未删除元素
        StringBuilder sb = new StringBuilder();
        boolean first = true;
        for (int i = 0; i < n; i++) {
            if (!removed[i]) {
                if (!first) {
                    sb.append(' ');
                }
                sb.append(arr[i]);
                first = false;
            }
        }

        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();

        int t = Integer.parseInt(br.readLine().trim());

        for (int caseIndex = 0; caseIndex < t; caseIndex++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            int m = Integer.parseInt(st.nextToken());

            int[] arr = new int[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                arr[i] = Integer.parseInt(st.nextToken());
            }

            out.append(solveCase(n, m, arr));
            if (caseIndex != t - 1) {
                out.append('\n');
            }
        }

        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 处理一组测试数据，返回最终序列
string solveCase(int n, int m, const vector<int>& arr) {
    // buckets[x] 存储所有值为 x 的元素下标（从小到大）
    vector<vector<int> > buckets(n + 1);

    // 按原下标顺序放入桶中
    for (int i = 0; i < n; i++) {
        buckets[arr[i]].push_back(i);
    }

    // removed[i] 表示原数组下标 i 的元素是否被删除
    vector<bool> removed(n, false);

    // 按值从小到大删除
    for (int value = 1; value <= n && m > 0; value++) {
        int size = (int)buckets[value].size();

        // 如果当前值的所有元素都要被删除
        if (size <= m) {
            for (int idx : buckets[value]) {
                removed[idx] = true;
            }
            m -= size;
        } else {
            // 只删除当前值中下标最小的前 m 个
            for (int i = 0; i < m; i++) {
                removed[buckets[value][i]] = true;
            }
            m = 0;
            break;
        }
    }

    // 按原顺序收集未删除元素
    string ans = "";
    bool first = true;
    for (int i = 0; i < n; i++) {
        if (!removed[i]) {
            if (!first) {
                ans += " ";
            }
            ans += to_string(arr[i]);
            first = false;
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
        int n, m;
        cin >> n >> m;

        vector<int> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        cout << solveCase(n, m, arr) << '\n';
    }

    return 0;
}
```