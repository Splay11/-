## 解题思路

对每个采样点 $p$，需要判断右侧是否存在某个采样值 $s_q$，满足 $q>p$ 且：

$$s_p \text{ xor } s_q \ge T$$

这是一个典型的「在一组数中寻找与当前数异或最大值」的问题，可以使用二进制字典树。

核心做法：

1. 从右往左遍历采样序列，维护一个只包含当前位置右侧元素的二进制字典树。
2. 对于当前位置 $p$：

   * 在字典树中查询与 $s_p$ 异或能得到的最大值 $best$。
   * 如果 $best \ge T$，说明存在右侧采样值满足条件，该点有效，答案为 `1`。
   * 否则该点无效，答案为 `0`。
   * 最后将 $s_p$ 插入字典树，供左侧采样点使用。

因为 $s_p \le 1000000000$，使用二进制第 $30$ 位到第 $0$ 位即可覆盖所有数。

## 复杂度分析

设采样序列长度为 $m$，数值范围不超过 $1000000000$。

每个数插入字典树需要遍历 $31$ 个二进制位，每次查询也需要遍历 $31$ 个二进制位。

- 时间复杂度：$O(m \log C)$，其中 $C$ 为数值上限，这里 $\log C \le 31$，因此可以看作 $O(31m)$。
- 空间复杂度：$O(m \log C)$，用于存储二进制字典树，最多插入 $m$ 个数。

## 代码实现

### Python

```python
import sys


# 计算每个采样点是否有效
def solve_array(s):
    m = len(s)
    T = max(s)  # 阈值（序列最大值）

    # 二进制字典树：ch0[x]、ch1[x] 分别表示节点 x 的 0/1 儿子，-1 表示不存在
    ch0 = [-1]
    ch1 = [-1]

    def insert(x):
        # 将一个采样值插入二进制字典树
        node = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if bit == 0:
                if ch0[node] == -1:
                    ch0[node] = len(ch0)
                    ch0.append(-1)
                    ch1.append(-1)
                node = ch0[node]
            else:
                if ch1[node] == -1:
                    ch1[node] = len(ch1)
                    ch0.append(-1)
                    ch1.append(-1)
                node = ch1[node]

    def query_max_xor(x):
        # 查询与 x 异或能得到的最大值
        node = 0
        res = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            # 优先走相反位，使当前位异或结果为 1
            if bit == 0:
                if ch1[node] != -1:
                    res |= 1 << b
                    node = ch1[node]
                else:
                    node = ch0[node]
            else:
                if ch0[node] != -1:
                    res |= 1 << b
                    node = ch0[node]
                else:
                    node = ch1[node]
        return res

    ans = ['0'] * m

    # 从右往左维护后缀字典树
    for p in range(m - 1, -1, -1):
        if p < m - 1:
            best = query_max_xor(s[p])
            if best >= T:
                ans[p] = '1'

        # 当前采样值插入，供左侧采样点查询
        insert(s[p])

    return ''.join(ans)


def main():
    input = sys.stdin.readline
    m = int(input())
    s = list(map(int, input().split()))
    print(solve_array(s))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    static int[][] child;
    static int nodeCnt;

    // 将一个采样值插入二进制字典树
    static void insert(int x) {
        int node = 0;
        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (child[node][bit] == 0) {
                child[node][bit] = nodeCnt++;
            }
            node = child[node][bit];
        }
    }

    // 查询与 x 异或能得到的最大值
    static int queryMaxXor(int x) {
        int node = 0;
        int res = 0;

        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            int want = bit ^ 1;

            // 优先走相反位，使当前位异或结果为 1
            if (child[node][want] != 0) {
                res |= 1 << b;
                node = child[node][want];
            } else {
                node = child[node][bit];
            }
        }

        return res;
    }

    // 计算每个采样点是否有效
    static String solveArray(int[] s) {
        int m = s.length;
        int T = 0;  // 阈值（序列最大值）

        for (int x : s) {
            T = Math.max(T, x);
        }

        // 最多 m * 31 个节点，0 号节点作为根
        child = new int[m * 31 + 5][2];
        nodeCnt = 1;

        char[] ans = new char[m];
        Arrays.fill(ans, '0');

        // 从右往左维护后缀字典树
        for (int p = m - 1; p >= 0; p--) {
            if (p < m - 1) {
                int best = queryMaxXor(s[p]);
                if (best >= T) {
                    ans[p] = '1';
                }
            }

            // 当前采样值插入，供左侧采样点查询
            insert(s[p]);
        }

        return new String(ans);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int m = sc.nextInt();
        int[] s = new int[m];

        for (int p = 0; p < m; p++) {
            s[p] = sc.nextInt();
        }

        System.out.println(solveArray(s));
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<array<int, 2>> child;

// 将一个采样值插入二进制字典树
void insertNumber(int x) {
    int node = 0;

    for (int b = 30; b >= 0; b--) {
        int bit = (x >> b) & 1;

        if (child[node][bit] == -1) {
            child[node][bit] = (int)child.size();
            child.push_back({-1, -1});
        }

        node = child[node][bit];
    }
}

// 查询与 x 异或能得到的最大值
int queryMaxXor(int x) {
    int node = 0;
    int res = 0;

    for (int b = 30; b >= 0; b--) {
        int bit = (x >> b) & 1;
        int want = bit ^ 1;

        // 优先走相反位，使当前位异或结果为 1
        if (child[node][want] != -1) {
            res |= 1 << b;
            node = child[node][want];
        } else {
            node = child[node][bit];
        }
    }

    return res;
}

// 计算每个采样点是否有效
string solveArray(vector<int>& s) {
    int m = (int)s.size();
    int T = *max_element(s.begin(), s.end());  // 阈值（序列最大值）

    child.clear();
    child.push_back({-1, -1});

    string ans(m, '0');

    // 从右往左维护后缀字典树
    for (int p = m - 1; p >= 0; p--) {
        if (p < m - 1) {
            int best = queryMaxXor(s[p]);
            if (best >= T) {
                ans[p] = '1';
            }
        }

        // 当前采样值插入，供左侧采样点查询
        insertNumber(s[p]);
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;

    vector<int> s(m);
    for (int p = 0; p < m; p++) {
        cin >> s[p];
    }

    cout << solveArray(s) << '\n';

    return 0;
}
```