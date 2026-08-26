## 解题思路

题目要求把 $1 \sim n$ 排成一个长度为 $n$ 的排列，并且对每个二元组 $(a_{i-1},a_i)$（其中 $i$ 为偶数），都满足：

* $a_{i-1}+a_i$ 不是质数；
* $|a_{i-1}-a_i|$ 不是质数。

这本质上是一个“按对构造”的题。因为只要求每两个位置组成的二元组合法，所以我们只需要把整个排列拆成若干合法数对，再顺次输出即可。

### 关键观察

如果两个数同奇偶性，那么：

* 它们的和一定是偶数；
* 只要和大于 $2$，就一定不是质数；
* 它们的差也是偶数，只要不等于 $2$，就一定不是质数。

所以，最理想的情况是：

* 尽量把同奇偶性的数配成一对；
* 并且让它们的差不是 $2$。

于是可以直接设计若干固定合法块。

### 合法块构造

#### $8$ 个数一块

对于连续的 $8$ 个数，从起点 $s$ 开始：

$
(s,s+4),(s+1,s+5),(s+2,s+6),(s+3,s+7)
$

对应输出顺序为：

$
s,\ s+4,\ s+1,\ s+5,\ s+2,\ s+6,\ s+3,\ s+7
$

因为每对的差都是 $4$，不是质数；每对的和都是大于 $2$ 的偶数，也不是质数，所以这一块一定合法。

#### 余数处理

把 $n$ 按照模 $8$ 分类讨论：

* $n=2,4,6$ 时无解；
* $n \bmod 8 = 0$：全部用 $8$ 块构造；
* $n \bmod 8 = 4$：前面尽量用 $8$ 块，最后留一个 $12$ 块：
  $
  1,5,2,6,3,9,4,10,7,11,8,12
  $
  平移后同样成立；
* $n \bmod 8 = 2$：先放一个固定的 $10$ 块：
  $
  1,5,2,6,3,9,4,10,7,8
  $
  后面再接若干个 $8$ 块；
* $n \bmod 8 = 6$：先放一个固定的 $14$ 块：
  $
  1,5,2,6,3,7,4,12,8,14,9,13,10,11
  $
  后面再接若干个 $8$ 块。

### 为什么 $2,4,6$ 无解

* $n=2$ 时只有 $(1,2)$ 或 $(2,1)$，和为 $3$，是质数；
* $n=4,6$ 可以直接验证不存在合法方案。

### 实现方法

按上面的构造直接生成答案即可，不需要搜索，不需要判质数。

---

## 复杂度分析

设单组数据长度为 $n$。

* 时间复杂度：$O(n)$
* 空间复杂度：$O(n)$

只需要顺序构造答案数组，复杂度完全满足要求。

---

## 代码实现

### Python

```python
import sys


# 构造长度为 n 的合法排列，若无解返回空列表
def build_permutation(n):
    if n == 2 or n == 4 or n == 6:
        return []

    ans = []

    # 加入一个长度为 8 的合法块，起点为 s
    def add_block8(s):
        ans.extend([s, s + 4, s + 1, s + 5, s + 2, s + 6, s + 3, s + 7])

    # 加入一个长度为 12 的合法块，起点为 s
    def add_block12(s):
        ans.extend([s, s + 4, s + 1, s + 5, s + 2, s + 8,
                    s + 3, s + 9, s + 6, s + 10, s + 7, s + 11])

    if n % 8 == 0:
        s = 1
        while s <= n:
            add_block8(s)
            s += 8

    elif n % 8 == 4:
        s = 1
        # 前面先放若干个 8 块
        while s <= n - 12:
            add_block8(s)
            s += 8
        # 最后放一个 12 块
        add_block12(n - 11)

    elif n % 8 == 2:
        # 先放一个固定的 10 块
        ans.extend([1, 5, 2, 6, 3, 9, 4, 10, 7, 8])
        s = 11
        while s <= n:
            add_block8(s)
            s += 8

    else:  # n % 8 == 6
        # 先放一个固定的 14 块
        ans.extend([1, 5, 2, 6, 3, 7, 4, 12, 8, 14, 9, 13, 10, 11])
        s = 15
        while s <= n:
            add_block8(s)
            s += 8

    return ans


def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        ans = build_permutation(n)
        if not ans:
            out.append("-1")
        else:
            out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {

    // 构造长度为 n 的合法排列，若无解返回空列表
    public static ArrayList<Integer> buildPermutation(int n) {
        ArrayList<Integer> ans = new ArrayList<>();

        if (n == 2 || n == 4 || n == 6) {
            return ans;
        }

        if (n % 8 == 0) {
            int s = 1;
            while (s <= n) {
                addBlock8(ans, s);
                s += 8;
            }
        } else if (n % 8 == 4) {
            int s = 1;
            // 前面放若干个 8 块
            while (s <= n - 12) {
                addBlock8(ans, s);
                s += 8;
            }
            // 最后放一个 12 块
            addBlock12(ans, n - 11);
        } else if (n % 8 == 2) {
            // 固定 10 块
            int[] block10 = {1, 5, 2, 6, 3, 9, 4, 10, 7, 8};
            for (int x : block10) {
                ans.add(x);
            }

            int s = 11;
            while (s <= n) {
                addBlock8(ans, s);
                s += 8;
            }
        } else { // n % 8 == 6
            // 固定 14 块
            int[] block14 = {1, 5, 2, 6, 3, 7, 4, 12, 8, 14, 9, 13, 10, 11};
            for (int x : block14) {
                ans.add(x);
            }

            int s = 15;
            while (s <= n) {
                addBlock8(ans, s);
                s += 8;
            }
        }

        return ans;
    }

    // 加入一个长度为 8 的合法块
    public static void addBlock8(ArrayList<Integer> ans, int s) {
        ans.add(s);
        ans.add(s + 4);
        ans.add(s + 1);
        ans.add(s + 5);
        ans.add(s + 2);
        ans.add(s + 6);
        ans.add(s + 3);
        ans.add(s + 7);
    }

    // 加入一个长度为 12 的合法块
    public static void addBlock12(ArrayList<Integer> ans, int s) {
        ans.add(s);
        ans.add(s + 4);
        ans.add(s + 1);
        ans.add(s + 5);
        ans.add(s + 2);
        ans.add(s + 8);
        ans.add(s + 3);
        ans.add(s + 9);
        ans.add(s + 6);
        ans.add(s + 10);
        ans.add(s + 7);
        ans.add(s + 11);
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        int t = fs.nextInt();
        StringBuilder sb = new StringBuilder();

        while (t-- > 0) {
            int n = fs.nextInt();
            ArrayList<Integer> ans = buildPermutation(n);

            if (ans.isEmpty()) {
                sb.append(-1).append('\n');
            } else {
                for (int i = 0; i < ans.size(); i++) {
                    if (i > 0) sb.append(' ');
                    sb.append(ans.get(i));
                }
                sb.append('\n');
            }
        }

        System.out.print(sb.toString());
    }
}


// 题目数据较大，使用较快的输入方式
class FastScanner {
    private BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    private StringTokenizer st;

    public String next() throws IOException {
        while (st == null || !st.hasMoreElements()) {
            st = new StringTokenizer(br.readLine());
        }
        return st.nextToken();
    }

    public int nextInt() throws IOException {
        return Integer.parseInt(next());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 加入一个长度为 8 的合法块
void addBlock8(vector<int>& ans, int s) {
    ans.push_back(s);
    ans.push_back(s + 4);
    ans.push_back(s + 1);
    ans.push_back(s + 5);
    ans.push_back(s + 2);
    ans.push_back(s + 6);
    ans.push_back(s + 3);
    ans.push_back(s + 7);
}

// 加入一个长度为 12 的合法块
void addBlock12(vector<int>& ans, int s) {
    ans.push_back(s);
    ans.push_back(s + 4);
    ans.push_back(s + 1);
    ans.push_back(s + 5);
    ans.push_back(s + 2);
    ans.push_back(s + 8);
    ans.push_back(s + 3);
    ans.push_back(s + 9);
    ans.push_back(s + 6);
    ans.push_back(s + 10);
    ans.push_back(s + 7);
    ans.push_back(s + 11);
}

// 构造长度为 n 的合法排列，若无解返回空数组
vector<int> buildPermutation(int n) {
    vector<int> ans;

    if (n == 2 || n == 4 || n == 6) {
        return ans;
    }

    if (n % 8 == 0) {
        int s = 1;
        while (s <= n) {
            addBlock8(ans, s);
            s += 8;
        }
    } else if (n % 8 == 4) {
        int s = 1;
        // 前面先放若干个 8 块
        while (s <= n - 12) {
            addBlock8(ans, s);
            s += 8;
        }
        // 最后放一个 12 块
        addBlock12(ans, n - 11);
    } else if (n % 8 == 2) {
        // 先放一个固定的 10 块
        int block10[] = {1, 5, 2, 6, 3, 9, 4, 10, 7, 8};
        for (int x : block10) {
            ans.push_back(x);
        }

        int s = 11;
        while (s <= n) {
            addBlock8(ans, s);
            s += 8;
        }
    } else { // n % 8 == 6
        // 先放一个固定的 14 块
        int block14[] = {1, 5, 2, 6, 3, 7, 4, 12, 8, 14, 9, 13, 10, 11};
        for (int x : block14) {
            ans.push_back(x);
        }

        int s = 15;
        while (s <= n) {
            addBlock8(ans, s);
            s += 8;
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

        vector<int> ans = buildPermutation(n);

        if (ans.empty()) {
            cout << -1 << '\n';
        } else {
            for (int i = 0; i < (int)ans.size(); i++) {
                if (i) cout << ' ';
                cout << ans[i];
            }
            cout << '\n';
        }
    }

    return 0;
}
```