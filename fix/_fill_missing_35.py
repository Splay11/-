"""为缺 Python 提取的题目手写三语言 03.5。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "log"


def wrap(idea: str, comp: str, py: str, java: str, cpp: str) -> str:
    return (
        "## 解题思路\n\n"
        + idea.strip()
        + "\n\n## 复杂度分析\n\n"
        + comp.strip()
        + "\n\n## 代码实现\n\n### Python\n\n```python\n"
        + py.strip()
        + "\n```\n\n### Java\n\n```java\n"
        + java.strip()
        + "\n```\n\n### C++\n\n```cpp\n"
        + cpp.strip()
        + "\n```\n"
    )


P1960 = wrap(
    "从后往前维护前缀异或操作的累计效果。已处理的后缀不再改变，用变量 s 维护其对更前位置的影响。"
    "若当前值与 s 异或后仍不等于最后一个元素，则必须再做一次操作，并更新 s。",
    "- 时间复杂度：O(n)\n- 空间复杂度：O(n)",
    """
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    cnt = 0
    s = 0
    last = a[-1]
    for i in range(n - 2, -1, -1):
        if (a[i] ^ s) != last:
            cnt += 1
            s = a[i] ^ last
    print(cnt)
""",
    """
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner cin = new Scanner(System.in);
        int t = cin.nextInt();
        while (t-- > 0) {
            int n = cin.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; ++i) a[i] = cin.nextInt();
            int cnt = 0, s = 0, last = a[n - 1];
            for (int i = n - 2; i >= 0; --i) {
                if ((a[i] ^ s) != last) {
                    cnt++;
                    s = a[i] ^ last;
                }
            }
            System.out.println(cnt);
        }
    }
}
""",
    """
#include <iostream>
#include <vector>
using namespace std;
int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        int cnt = 0, s = 0, last = a.back();
        for (int i = n - 2; i >= 0; --i) {
            if ((a[i] ^ s) != last) {
                cnt++;
                s = a[i] ^ last;
            }
        }
        cout << cnt << endl;
    }
    return 0;
}
""",
)

P1961 = wrap(
    "若所有行异或和的总异或不等于所有列异或和的总异或，则无解。"
    "否则把第 2..n 行第 1 列填成对应行异或，把第 1 行第 2..m 列填成对应列异或，其余为 0，"
    "再由第一行或第一列的约束确定左上角元素即可。",
    "- 时间复杂度：O(n m)\n- 空间复杂度：O(n m)",
    """
n, m = map(int, input().split())
ans = [[0] * m for _ in range(n)]
row = col = 0
xs = list(map(int, input().split()))
for i, x in enumerate(xs):
    ans[i][0] = x
    row ^= x
ys = list(map(int, input().split()))
for i, x in enumerate(ys):
    if i:
        ans[0][i] = x
    col ^= x
if row != col:
    print("NO")
else:
    print("YES")
    for i in range(1, m):
        ans[0][0] ^= ans[0][i]
    for i in range(n):
        print(*ans[i])
""",
    """
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner cin = new Scanner(System.in);
        int n = cin.nextInt(), m = cin.nextInt();
        long[][] ans = new long[n][m];
        int row = 0, col = 0;
        for (int i = 0; i < n; ++i) {
            int x = cin.nextInt();
            ans[i][0] = x;
            row ^= x;
        }
        for (int i = 0; i < m; ++i) {
            int x = cin.nextInt();
            if (i > 0) ans[0][i] = x;
            col ^= x;
        }
        if (row != col) {
            System.out.println("NO");
        } else {
            System.out.println("YES");
            for (int i = 1; i < m; ++i) ans[0][0] ^= ans[0][i];
            for (int i = 0; i < n; ++i) {
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < m; ++j) {
                    if (j > 0) sb.append(' ');
                    sb.append(ans[i][j]);
                }
                System.out.println(sb);
            }
        }
    }
}
""",
    """
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> ans(n, vector<int>(m, 0));
    int row = 0, col = 0;
    for (int i = 0, x; i < n; ++i) {
        cin >> x;
        ans[i][0] = x;
        row ^= x;
    }
    for (int i = 0, x; i < m; ++i) {
        cin >> x;
        if (i) ans[0][i] = x;
        col ^= x;
    }
    if (row != col) {
        puts("NO");
    } else {
        puts("YES");
        for (int i = 1; i < m; ++i) ans[0][0] ^= ans[0][i];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                cout << ans[i][j] << " \\n"[j == m - 1];
            }
        }
    }
}
""",
)

P1962 = wrap(
    "使等式成立的选取方式要求从 a 或从 b 取出的值全部相同。因此答案就是 a、b 中某个值的最大出现次数。",
    "- 时间复杂度：O(n)\n- 空间复杂度：O(n)",
    """
from collections import Counter
T = int(input())
for _ in range(T):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    ma, mb = Counter(a), Counter(b)
    ans = 0
    for i in range(n):
        ans = max(ans, ma[a[i]], mb[b[i]])
    print(ans)
""",
    """
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int T = in.nextInt();
        while (T-- > 0) {
            int n = in.nextInt();
            int ans = 1;
            Map<Integer, Integer> cntA = new HashMap<>();
            for (int i = 0; i < n; i++) {
                int a = in.nextInt();
                cntA.put(a, cntA.getOrDefault(a, 0) + 1);
                ans = Math.max(ans, cntA.get(a));
            }
            Map<Integer, Integer> cntB = new HashMap<>();
            for (int i = 0; i < n; i++) {
                int b = in.nextInt();
                cntB.put(b, cntB.getOrDefault(b, 0) + 1);
                ans = Math.max(ans, cntB.get(b));
            }
            System.out.println(ans);
        }
    }
}
""",
    """
#include <bits/stdc++.h>
using namespace std;
int main() {
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<int> a(n), b(n);
        map<int, int> ma, mb;
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
            ++ma[a[i]];
        }
        for (int i = 0; i < n; ++i) {
            cin >> b[i];
            ++mb[b[i]];
        }
        int ans = 0;
        for (int i = 0; i < n; ++i) {
            ans = max({ans, ma[a[i]], mb[b[i]]});
        }
        cout << ans << endl;
    }
}
""",
)

P1753 = wrap(
    "每人离开队伍所需轮数是 ceil(w_i / m)。以轮数为第一关键字、原下标为第二关键字排序，"
    "得到的顺序即为离开顺序。Scanner / cin 按空白读入，n 与 m 可分行。",
    "- 时间复杂度：O(n log n)\n- 空间复杂度：O(n)",
    """
import sys
data = list(map(int, sys.stdin.read().split()))
n, m = data[0], data[1]
a = data[2:2 + n]
ans = [((x + m - 1) // m, i + 1) for i, x in enumerate(a)]
ans.sort()
print(*[idx for _, idx in ans])
""",
    """
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner cin = new Scanner(System.in);
        int n = cin.nextInt();
        int m = cin.nextInt();
        int[][] ans = new int[n][2];
        for (int i = 0; i < n; i++) {
            int x = cin.nextInt();
            ans[i][0] = (x + m - 1) / m;
            ans[i][1] = i + 1;
        }
        Arrays.sort(ans, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]));
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(ans[i][1]);
        }
        System.out.println(sb);
    }
}
""",
    """
#include<bits/stdc++.h>
using namespace std;
int main (){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n, m; cin >> n >> m;
    vector<pair<int, int>> ans;
    for(int i = 0; i < n; i ++)
    {
        int x; cin >> x;
        ans.push_back({(x + m - 1) / m, i + 1});
    }
    sort(ans.begin(), ans.end());
    for(auto i : ans)
        cout << i.second << " ";
    return 0;
}
""",
)


def main() -> None:
    items = {
        "P1960": P1960,
        "P1961": P1961,
        "P1962": P1962,
        "P1753": P1753,
    }
    for pid, text in items.items():
        path = ROOT / pid / "03.5_修改后的题解.md"
        path.write_text(text, encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
