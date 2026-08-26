## 解题思路

要在所有排列中尝试拼接再删字符并选最小，直接暴力枚举所有 $n!$ 种排列，每种排列拼接后长度最多 $L \le 80$，再枚举删除位置，复杂度约为 $O(n! \times L^2)$。

可以优化：对于给定字符序列 $S$，要删除一个字符后使得结果字典序最小，只需找到第一个使得 $S[i] > S[i+1]$ 的位置 $i$，删除 $S[i]$；若不存在这样的下降点，则删除末尾字符。该贪心策略可在线性时间 $O(L)$ 内完成。

因此总体流程：

1. 对索引 $[0,1,\dots,n-1]$ 排列全遍历（或 DFS 生成）。
2. 拼接对应字符串序列得到 $S$。
3. 在 $S$ 上执行“第一个下降点”贪心删除，得候选字符串 $T$。
4. 维护当前最小字典序字符串并更新。

## 复杂度分析

* 排列枚举：$n!$ 种。
* 每个排列拼接字符串和贪心删除：$O(L)$，其中 $L = \sum |a_i| \le 80$。
* 整体时间复杂度：$O(n! \times L)$，在 $n\le8$、$L\le80$ 下可行。
* 空间复杂度：存储拼接字符串和若干临时变量，为 $O(L)$。

## 代码实现

### Python

```python
def solve():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = data[1:1+n]
    from itertools import permutations

    best = None
    for perm in permutations(arr):
        s = "".join(perm)
        # 找到第一个下降点删除，若无则删除末尾
        idx = len(s) - 1
        for i in range(len(s)-1):
            if s[i] > s[i+1]:
                idx = i
                break
        t = s[:idx] + s[idx+1:]
        if best is None or t < best:
            best = t
    print(best)

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(in.readLine().trim());
        String[] a = in.readLine().trim().split("\\s+");
        boolean[] used = new boolean[n];
        String[] perm = new String[n];
        String[] best = {null};
        dfs(a, used, perm, 0, best);
        System.out.println(best[0]);
    }

    // 递归枚举排列
    static void dfs(String[] a, boolean[] used, String[] perm, int depth, String[] best) {
        int n = a.length;
        if (depth == n) {
            String s = String.join("", perm);
            int idx = s.length() - 1;
            for (int i = 0; i + 1 < s.length(); i++) {
                if (s.charAt(i) > s.charAt(i+1)) {
                    idx = i;
                    break;
                }
            }
            String t = s.substring(0, idx) + s.substring(idx+1);
            if (best[0] == null || t.compareTo(best[0]) < 0) {
                best[0] = t;
            }
            return;
        }
        for (int i = 0; i < n; i++) {
            if (!used[i]) {
                used[i] = true;
                perm[depth] = a[i];
                dfs(a, used, perm, depth+1, best);
                used[i] = false;
            }
        }
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> a;
string best;

void dfs(vector<bool>& used, vector<string>& perm, int depth) {
    if (depth == n) {
        string s;
        for (auto& str: perm) s += str;
        int idx = s.size() - 1;
        for (int i = 0; i + 1 < (int)s.size(); i++) {
            if (s[i] > s[i+1]) {
                idx = i;
                break;
            }
        }
        string t = s.substr(0, idx) + s.substr(idx+1);
        if (best.empty() || t < best) best = t;
        return;
    }
    for (int i = 0; i < n; i++) {
        if (!used[i]) {
            used[i] = true;
            perm[depth] = a[i];
            dfs(used, perm, depth+1);
            used[i] = false;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    a.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    vector<bool> used(n, false);
    vector<string> perm(n);
    dfs(used, perm, 0);
    cout << best << "\n";
    return 0;
}
```