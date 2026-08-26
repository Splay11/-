## 解题思路

本题可以使用排序与分组枚举。

当阈值 $T$ 足够小时，所有元素都满足 $h_i\ge T$，因此所有元素都取高位值 $H_i$。

先计算初始总和：

$$
V=\sum_{i=1}^{n}H_i
$$

此时先用 $|V-S|$ 更新答案。

随着阈值 $T$ 不断增大，当 $T$ 越过某个判定值 $h_i$ 时，该元素会从高位值 $H_i$ 切换为低位值 $L_i$，因此总和的变化量为：

$$
L_i-H_i
$$

将所有元素按照 $h_i$ 从小到大排序，然后依次处理。

需要特别注意：如果多个元素的 $h_i$ 相同，那么阈值不可能只越过其中一部分。因此，相同 $h_i$ 的元素必须一起修改。

对于一组相同的判定值 $h$，将这一组元素全部完成：

$$
V\leftarrow V+(L_i-H_i)
$$

之后再计算：

$$
|V-S|
$$

并更新最小值。

这样就枚举了所有本质不同的阈值状态。

## 复杂度分析

排序需要 $O(n\log n)$ 的时间，之后只需要遍历所有元素一次，因此总时间复杂度为：

$$
O(n\log n)
$$

存储全部元素需要 $O(n)$ 的空间，因此空间复杂度为：

$$
O(n)
$$

## 代码实现

### Python

```python
def solve(items, S):
    # 按判定值从小到大排序
    items.sort(key=lambda x: x[0])

    # 初始时所有元素都取高位值
    total = sum(x[2] for x in items)
    ans = abs(total - S)

    n = len(items)
    i = 0

    while i < n:
        h = items[i][0]

        # 相同判定值的元素必须一起切换
        while i < n and items[i][0] == h:
            _, L, H = items[i]
            total += L - H
            i += 1

        ans = min(ans, abs(total - S))

    return ans


def main():
    n = int(input())
    S = int(input())

    items = []
    for _ in range(n):
        h, L, H = map(int, input().split())
        items.append((h, L, H))

    print(solve(items, S))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    static long solve(long[][] items, long S) {
        // 按判定值从小到大排序
        Arrays.sort(items, new Comparator<long[]>() {
            public int compare(long[] a, long[] b) {
                return Long.compare(a[0], b[0]);
            }
        });

        // 初始时所有元素都取高位值
        long total = 0;
        for (long[] item : items) {
            total += item[2];
        }

        long ans = Math.abs(total - S);
        int n = items.length;
        int i = 0;

        while (i < n) {
            long h = items[i][0];

            // 相同判定值的元素必须一起切换
            while (i < n && items[i][0] == h) {
                total += items[i][1] - items[i][2];
                i++;
            }

            ans = Math.min(ans, Math.abs(total - S));
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine());
        long S = Long.parseLong(br.readLine());

        long[][] items = new long[n][3];

        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            items[i][0] = Long.parseLong(st.nextToken());
            items[i][1] = Long.parseLong(st.nextToken());
            items[i][2] = Long.parseLong(st.nextToken());
        }

        System.out.println(solve(items, S));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

long long solve(vector<vector<long long>>& items, long long S) {
    // 按判定值从小到大排序
    sort(items.begin(), items.end());

    // 初始时所有元素都取高位值
    long long total = 0;
    for (auto& item : items) {
        total += item[2];
    }

    long long ans = llabs(total - S);
    int n = items.size();
    int i = 0;

    while (i < n) {
        long long h = items[i][0];

        // 相同判定值的元素必须一起切换
        while (i < n && items[i][0] == h) {
            total += items[i][1] - items[i][2];
            i++;
        }

        ans = min(ans, llabs(total - S));
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long S;

    cin >> n;
    cin >> S;

    vector<vector<long long>> items(n, vector<long long>(3));

    for (int i = 0; i < n; i++) {
        cin >> items[i][0] >> items[i][1] >> items[i][2];
    }

    cout << solve(items, S) << '\n';

    return 0;
}
```