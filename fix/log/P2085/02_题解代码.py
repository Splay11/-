## 解题思路

先注意到题目里真正起作用的是$k \bmod 10$，因为观察到的值为：

$A[i] \times k \bmod 10$

而$A[i] \in [0,9]$，所以只和$k$的个位有关。

对于一个询问$(l,r,k)$，如果我们知道区间$[l,r]$中原始数字$0\sim 9$各出现了多少次，那么设原数字$x$在区间内出现次数为$cnt[x]$，放大后它会全部变成：

$(x \times (k \bmod 10)) \bmod 10$

于是我们只需要把原本的计数按照这个映射转移到答案数组里即可。

所以可以先做前缀统计：

设$pre[i][d]$表示前$i$个数中，数字$d$出现了多少次。

那么任意区间$[l,r]$中数字$d$的出现次数就是：

$pre[r][d] - pre[l-1][d]$

这样每次询问时：

1. 先求出区间内原始数字$0\sim 9$的数量；
2. 设$t = k \bmod 10$；
3. 对每个原始数字$d$，把它的出现次数累加到目标数字$(d \times t) \bmod 10$中。

这属于前缀和 + 模拟映射统计。

为了让实现更简洁，还可以预处理$map[t][d] = (d \times t) \bmod 10$，其中$t \in [0,9]$，这样查询时直接使用即可。

## 复杂度分析

预处理前缀计数需要遍历一次数组，每个位置维护$10$个数字的出现次数，时间复杂度为：

$O(10n)$

每次询问需要统计$10$个原数字并映射到答案中，时间复杂度为：

$O(10)$

总时间复杂度为：

$O(10n + 10q)$

由于常数很小，可视为$O(n+q)$。

空间复杂度主要是前缀数组：

$O(10n)$

在$n \le 10^5$ 时完全可行。

## 代码实现

### Python

```python
def solve(n, arr, queries):
    # pre[i][d] 表示前 i 个数中数字 d 出现的次数
    pre = [[0] * 10 for _ in range(n + 1)]

    for i in range(1, n + 1):
        # 先继承前一个位置的统计结果
        for d in range(10):
            pre[i][d] = pre[i - 1][d]
        # 当前数字出现次数加一
        pre[i][arr[i - 1]] += 1

    # 预处理个位映射
    trans = [[0] * 10 for _ in range(10)]
    for k in range(10):
        for d in range(10):
            trans[k][d] = (d * k) % 10

    ans_list = []

    for l, r, k in queries:
        t = k % 10
        ans = [0] * 10

        # 统计区间内原始数字，再映射到结果中
        for d in range(10):
            cnt = pre[r][d] - pre[l - 1][d]
            ans[trans[t][d]] += cnt

        ans_list.append(ans)

    return ans_list


def main():
    n = int(input())
    arr = list(map(int, input().split()))
    q = int(input())

    queries = []
    for _ in range(q):
        l, r, k = map(int, input().split())
        queries.append((l, r, k))

    res = solve(n, arr, queries)

    for row in res:
        print(*row)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {

    // 处理所有询问，返回每次询问的结果
    public static List<int[]> solve(int n, int[] arr, int[][] queries) {
        // pre[i][d] 表示前 i 个数中数字 d 出现的次数
        int[][] pre = new int[n + 1][10];

        for (int i = 1; i <= n; i++) {
            // 先继承前一个位置的统计结果
            for (int d = 0; d < 10; d++) {
                pre[i][d] = pre[i - 1][d];
            }
            // 当前数字出现次数加一
            pre[i][arr[i - 1]]++;
        }

        // 预处理个位映射
        int[][] trans = new int[10][10];
        for (int k = 0; k < 10; k++) {
            for (int d = 0; d < 10; d++) {
                trans[k][d] = (d * k) % 10;
            }
        }

        List<int[]> res = new ArrayList<>();

        for (int[] query : queries) {
            int l = query[0];
            int r = query[1];
            int k = query[2] % 10;

            int[] ans = new int[10];

            // 统计区间内原始数字，再映射到结果中
            for (int d = 0; d < 10; d++) {
                int cnt = pre[r][d] - pre[l - 1][d];
                ans[trans[k][d]] += cnt;
            }

            res.add(ans);
        }

        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        int q = sc.nextInt();
        int[][] queries = new int[q][3];
        for (int i = 0; i < q; i++) {
            queries[i][0] = sc.nextInt();
            queries[i][1] = sc.nextInt();
            queries[i][2] = sc.nextInt();
        }

        List<int[]> res = solve(n, arr, queries);

        StringBuilder sb = new StringBuilder();
        for (int[] row : res) {
            for (int i = 0; i < 10; i++) {
                if (i > 0) sb.append(" ");
                sb.append(row[i]);
            }
            sb.append("\n");
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 处理所有询问，返回每次询问的结果
vector<vector<int>> solve(int n, const vector<int>& arr, const vector<vector<int>>& queries) {
    // pre[i][d] 表示前 i 个数中数字 d 出现的次数
    vector<vector<int>> pre(n + 1, vector<int>(10, 0));

    for (int i = 1; i <= n; i++) {
        // 先继承前一个位置的统计结果
        for (int d = 0; d < 10; d++) {
            pre[i][d] = pre[i - 1][d];
        }
        // 当前数字出现次数加一
        pre[i][arr[i - 1]]++;
    }

    // 预处理个位映射
    int trans[10][10];
    for (int k = 0; k < 10; k++) {
        for (int d = 0; d < 10; d++) {
            trans[k][d] = (d * k) % 10;
        }
    }

    vector<vector<int>> res;

    for (const auto& query : queries) {
        int l = query[0];
        int r = query[1];
        int k = query[2] % 10;

        vector<int> ans(10, 0);

        // 统计区间内原始数字，再映射到结果中
        for (int d = 0; d < 10; d++) {
            int cnt = pre[r][d] - pre[l - 1][d];
            ans[trans[k][d]] += cnt;
        }

        res.push_back(ans);
    }

    return res;
}

int main() {
    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    int q;
    cin >> q;

    vector<vector<int>> queries(q, vector<int>(3));
    for (int i = 0; i < q; i++) {
        cin >> queries[i][0] >> queries[i][1] >> queries[i][2];
    }

    vector<vector<int>> res = solve(n, arr, queries);

    for (const auto& row : res) {
        for (int i = 0; i < 10; i++) {
            if (i > 0) cout << " ";
            cout << row[i];
        }
        cout << "\n";
    }

    return 0;
}
```