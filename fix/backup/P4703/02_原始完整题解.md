## 解题思路

题目中的关键点有两个：

$1.$ 每个人在每道题上的得分，只取历史提交中的最大值。
$2.$ 每次提交结束后，都要立刻求出编号为 $1$ 的用户当前排名。

由于题目范围里用户编号 $a_i \le 100$，题目编号 $b_i \le 100$，所以总人数和题目数都很小。虽然提交次数 $n$ 很大，但我们完全可以直接维护每个人每道题的最好成绩。

具体做法如下：

* 用二维数组 $best[u][p]$ 表示用户 $u$ 在题目 $p$ 上的历史最高分。
* 用数组 $sum[u]$ 表示用户 $u$ 当前总分。
* 处理一条提交 $(a,b,c)$ 时：

  * 如果 $c \le best[a][b]$，说明这次提交不会提升该题得分，总分不变。
  * 如果 $c > best[a][b]$，则这道题的贡献增加了 $c - best[a][b]$，于是：

    * $sum[a] += c - best[a][b]$
    * 更新 $best[a][b] = c$
* 然后统计有多少人的总分严格大于用户 $1$ 的总分，设人数为 $cnt$，那么用户 $1$ 的排名就是 $cnt + 1$。

这里用到的算法本质上是：

* 数组维护
* 模拟
* 每次线性统计排名

因为总用户数最多只有 $100$，所以每次提交后扫一遍所有用户求排名，复杂度完全可以接受。

## 复杂度分析

设提交次数为 $n$。

* 每次更新成绩是 $O(1)$
* 每次统计排名需要扫描最多 $100$ 个用户，是 $O(100)$

所以总时间复杂度为：

$O(n \times 100)$

在 $n \le 2 \times 10^5$ 时，最多约为 $2 \times 10^7$ 级别操作，可以通过。

空间复杂度为：

$O(100 \times 100)$

用于维护每个人每道题的最高分，空间很小。

## 代码实现

### Python

```python
import sys


def solve(records):
    # best[u][p] 表示用户 u 在题目 p 上的最高分
    best = [[0] * 101 for _ in range(101)]
    # sum_score[u] 表示用户 u 的总分
    sum_score = [0] * 101

    ans = []

    for a, b, c in records:
        # 如果这次提交提高了该题最高分，则更新总分
        if c > best[a][b]:
            sum_score[a] += c - best[a][b]
            best[a][b] = c

        # 统计总分严格高于 1 号用户的人数
        rank = 1
        for user in range(1, 101):
            if sum_score[user] > sum_score[1]:
                rank += 1

        ans.append(rank)

    return ans


def main():
    input = sys.stdin.readline
    n = int(input())
    records = []
    for _ in range(n):
        a, b, c = map(int, input().split())
        records.append((a, b, c))

    ans = solve(records)
    print("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {

    // 处理所有提交记录，返回每次提交后 1 号用户的排名
    public static List<Integer> solve(List<int[]> records) {
        // best[u][p] 表示用户 u 在题目 p 上的最高分
        int[][] best = new int[101][101];
        // sumScore[u] 表示用户 u 的总分
        int[] sumScore = new int[101];

        List<Integer> ans = new ArrayList<>();

        for (int[] record : records) {
            int a = record[0];
            int b = record[1];
            int c = record[2];

            // 如果这次提交提高了该题最高分，则更新总分
            if (c > best[a][b]) {
                sumScore[a] += c - best[a][b];
                best[a][b] = c;
            }

            // 统计总分严格高于 1 号用户的人数
            int rank = 1;
            for (int user = 1; user <= 100; user++) {
                if (sumScore[user] > sumScore[1]) {
                    rank++;
                }
            }

            ans.add(rank);
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        List<int[]> records = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            int a = sc.nextInt();
            int b = sc.nextInt();
            int c = sc.nextInt();
            records.add(new int[]{a, b, c});
        }

        List<Integer> ans = solve(records);
        StringBuilder sb = new StringBuilder();
        for (int x : ans) {
            sb.append(x).append('\n');
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

// 处理所有提交记录，返回每次提交后 1 号用户的排名
vector<int> solve(const vector<vector<int>>& records) {
    // best[u][p] 表示用户 u 在题目 p 上的最高分
    int best[101][101] = {0};
    // sumScore[u] 表示用户 u 的总分
    int sumScore[101] = {0};

    vector<int> ans;

    for (const auto& record : records) {
        int a = record[0];
        int b = record[1];
        int c = record[2];

        // 如果这次提交提高了该题最高分，则更新总分
        if (c > best[a][b]) {
            sumScore[a] += c - best[a][b];
            best[a][b] = c;
        }

        // 统计总分严格高于 1 号用户的人数
        int rank = 1;
        for (int user = 1; user <= 100; user++) {
            if (sumScore[user] > sumScore[1]) {
                rank++;
            }
        }

        ans.push_back(rank);
    }

    return ans;
}

int main() {
    int n;
    cin >> n;

    vector<vector<int>> records;
    for (int i = 0; i < n; i++) {
        int a, b, c;
        cin >> a >> b >> c;
        records.push_back({a, b, c});
    }

    vector<int> ans = solve(records);
    for (int x : ans) {
        cout << x << '\n';
    }

    return 0;
}
```