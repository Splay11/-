# -*- coding: utf-8 -*-
"""Rebuild P7012/P7013 at CF ~800: sort+greedy / sort+window."""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
COMPILE_SRC = REPO / "compile.sh"

# ---------- solvers ----------


def min_audit_days(loads: list[int]) -> int:
    if not loads:
        return 0
    total = sum(loads)
    a = sorted(loads, reverse=True)
    s = 0
    for i, x in enumerate(a, 1):
        s += x
        if s * 2 > total:
            return i
    return len(a)


def min_score_spread(scores: list[int], k: int) -> int:
    if k <= 0:
        return 0
    n = len(scores)
    if k > n:
        return -1
    if k == 1:
        return 0
    a = sorted(scores)
    ans = a[k - 1] - a[0]
    for i in range(1, n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])
    return ans


# ---------- shared templates ----------

CONFIG = """type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.c
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
  - user.c
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
      - input: 1.in
        output: 1.out
      - input: 2.in
        output: 2.out
      - input: 3.in
        output: 3.out
      - input: 4.in
        output: 4.out
      - input: 5.in
        output: 5.out
      - input: 6.in
        output: 6.out
      - input: 7.in
        output: 7.out
      - input: 8.in
        output: 8.out
      - input: 9.in
        output: 9.out
      - input: 10.in
        output: 10.out
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
  - c
"""

PARSE_JAVA = r'''import java.io.*;
import java.util.*;
public class Main {
    private static String trim(String s) { return s == null ? "" : s.trim(); }
    private static long readLong(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        int sign = 1;
        if (idx[0] < s.length() && s.charAt(idx[0]) == '-') { sign = -1; idx[0]++; }
        long v = 0; boolean ok = false;
        while (idx[0] < s.length() && Character.isDigit(s.charAt(idx[0]))) {
            ok = true; v = v * 10 + (s.charAt(idx[0]++) - '0');
        }
        if (!ok) throw new RuntimeException("bad int");
        return sign * v;
    }
    private static int[] parseArray1d(String line) {
        line = trim(line); int[] idx = {0};
        if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++; java.util.ArrayList<Integer> row = new java.util.ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            row.add((int) readLong(line, idx));
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        int[] a = new int[row.size()];
        for (int i = 0; i < row.size(); i++) a[i] = row.get(i);
        return a;
    }
'''

PARSE_CC = r'''#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static string trim(const string& s) {
    size_t a = 0; while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size(); while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}
static bool parseLong(const string& s, size_t& i, long long& out) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    int sign = 1; if (i < s.size() && s[i] == '-') { sign = -1; i++; }
    if (i >= s.size() || !isdigit((unsigned char)s[i])) return false;
    long long v = 0; while (i < s.size() && isdigit((unsigned char)s[i])) { v = v * 10 + (s[i] - '0'); i++; }
    out = sign * v; return true;
}
static vector<int> parseArray1d(const string& line) {
    string s = trim(line); size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1); i++;
    vector<int> row;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        long long v; if (!parseLong(s, i, v)) exit(1); row.push_back((int)v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        if (i >= s.size() || s[i] != ',') exit(1); i++;
    }
    return row;
}
'''

PARSE_C = r'''#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 2000000
#define MAX_N 200000
static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_N * sizeof(int)); *outCount = 0; int i = 0;
    while (s[i] && s[i] != '[') i++; if (!s[i]) return res; i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        int sign = 1; if (s[i] == '-') { sign = -1; i++; }
        long long v = 0; int have = 0;
        while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); have = 1; i++; }
        if (have) res[(*outCount)++] = (int)(sign * v); else i++;
    }
    return res;
}
'''


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def setup_p7012() -> None:
    d = ROOT / "P7012"
    data = d / "data"
    write(
        d / "标题.txt",
        "标题：合规抽查最少天数\n算法标签：排序,贪心\n难度：3\n",
    )
    write(
        d / "题面.md",
        """# 题目内容

合规平台要对业务线做人工抽查。给定每日风险负载数组 `loads`（下标从 $0$ 开始），你需要选出若干天进行复核。

选择规则：

1. 可以选任意天数（不必连续），目标是**天数尽量少**
2. 选出的负载之和必须**严格大于**未选天数的负载之和（等价于：选出之和 $>\\textit{总负载}/2$）
3. 若 `loads` 为空，返回 $0$

请返回最少需要抽查的天数。

请实现：

```text
minAuditDays(loads: int[]) -> int
```

## 输入描述

一行：整型数组 `loads`，形如 `[3, 3, 4, 2]`

约束：

- $0 \\le n \\le 10^5$，$n=\\texttt{loads.length}$
- $1 \\le \\texttt{loads}[i] \\le 10^9$（`n=0` 时无元素）

## 输出描述

一个整数：最少抽查天数。

## 样例1

输入：

```
[3, 3, 4, 2]
```

输出：

```
2
```

说明：总负载 $12$。选 $4$ 与 $3$，和为 $7>5$，两天即可；只选一天最大 $4$ 不够。

## 样例2

输入：

```
[1, 1]
```

输出：

```
2
```

说明：选一天和为 $1$，未选也是 $1$，不满足严格大于，必须两天都选。

## 样例3

输入：

```
[10]
```

输出：

```
1
```

说明：只选这一天，和 $10>0$。
""",
    )

    sol_py = '''from typing import List


class Solution:
    def minAuditDays(self, loads: List[int]) -> int:
        # 空数组无需抽查
        if not loads:
            return 0
        # 先算总负载；选出之和必须严格大于一半
        total = sum(loads)
        # 贪心：优先抽查负载最大的天，天数才可能最少
        a = sorted(loads, reverse=True)
        s = 0
        for i, x in enumerate(a, 1):
            s += x
            # 2*s > total 等价于 s > total - s
            if s * 2 > total:
                return i
        return len(a)
'''

    sol_java = '''import java.util.*;

class Solution {
    public int minAuditDays(int[] loads) {
        // 空数组无需抽查
        if (loads == null || loads.length == 0) {
            return 0;
        }
        // 计算总负载（用 long 防止溢出）
        long total = 0;
        Integer[] a = new Integer[loads.length];
        for (int i = 0; i < loads.length; i++) {
            total += loads[i];
            a[i] = loads[i];
        }
        // 降序排序：优先选大的
        Arrays.sort(a, Collections.reverseOrder());
        long s = 0;
        for (int i = 0; i < a.length; i++) {
            s += a[i];
            // 选出之和严格大于未选之和
            if (s * 2 > total) {
                return i + 1;
            }
        }
        return a.length;
    }
}
'''

    sol_cc = '''#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minAuditDays(vector<int>& loads) {
        // 空数组无需抽查
        if (loads.empty()) return 0;
        // 总负载用 long long，避免相加溢出
        long long total = 0;
        for (int x : loads) total += x;
        // 复制后降序排序，贪心取最大
        vector<int> a = loads;
        sort(a.begin(), a.end(), greater<int>());
        long long s = 0;
        for (int i = 0; i < (int)a.size(); i++) {
            s += a[i];
            // 2*s > total 即选出严格过半
            if (s * 2 > total) return i + 1;
        }
        return (int)a.size();
    }
};
'''

    sol_c = '''#include <stdlib.h>

static int cmp_desc(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    if (a < b) return 1;
    if (a > b) return -1;
    return 0;
}

int minAuditDays(int* loads, int loadsSize) {
    /* 空数组 */
    if (loadsSize <= 0) return 0;
    /* 复制一份以便排序，不改动原数组语义 */
    int* a = (int*)malloc(loadsSize * sizeof(int));
    long long total = 0;
    for (int i = 0; i < loadsSize; i++) {
        a[i] = loads[i];
        total += loads[i];
    }
    /* 降序：优先抽大负载 */
    qsort(a, loadsSize, sizeof(int), cmp_desc);
    long long s = 0;
    int ans = loadsSize;
    for (int i = 0; i < loadsSize; i++) {
        s += a[i];
        if (s * 2 > total) {
            ans = i + 1;
            break;
        }
    }
    free(a);
    return ans;
}
'''

    write(
        d / "题解.md",
        f"""## 解题思路

本题是典型的「过半贪心」：

1. 要天数最少，应优先抽查负载**最大**的天。
2. 将 `loads` **降序排序**，从大到小累加。
3. 一旦当前选出之和 $s$ 满足 $2s >$ 总负载（即严格大于另一半），立刻返回已选天数。

正确性：交换论证——若最优解含较小值而不含更大值，换成更大值只会更快过半，不会变差。

## 复杂度分析

- 时间复杂度：$O(n\\log n)$，主要来自排序。
- 空间复杂度：$O(n)$（排序副本；原地排序可为 $O(1)$ 额外空间）。

## 代码实现

### Python

```python
{sol_py.strip()}
```

### Java

```java
{sol_java.strip()}
```

### C++

```cpp
{sol_cc.strip()}
```

### C

```c
{sol_c.strip()}
```
""",
    )
    write(d / "std.py", sol_py)
    write(data / "user.py", "from typing import List\n\nclass Solution:\n    def minAuditDays(self, loads: List[int]) -> int:\n        return 0\n")
    write(data / "user.java", "import java.util.*;\npublic class Solution {\n    public int minAuditDays(int[] loads) { return 0; }\n}\n")
    write(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int minAuditDays(vector<int>& loads) { (void)loads; return 0; }\n};\n")
    write(data / "user.c", "int minAuditDays(int* loads, int loadsSize) { (void)loads; (void)loadsSize; return 0; }\n")
    write(data / "template.py", "import json, sys\nlines=[ln for ln in sys.stdin.read().split(\"\\n\") if ln.strip()!=\"\"]\nif not lines: raise SystemExit(0)\nprint(Solution().minAuditDays(json.loads(lines[0])))\n")
    write(
        data / "template.java",
        PARSE_JAVA
        + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine();
        if (l1 == null) return;
        System.out.println(new Solution().minAuditDays(parseArray1d(l1)));
    }
}
""",
    )
    write(
        data / "template.cc",
        PARSE_CC
        + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1; if (!getline(cin, l1)) return 0;
    auto loads = parseArray1d(l1); Solution sol;
    cout << sol.minAuditDays(loads) << '\\n';
}
""",
    )
    write(
        data / "template.c",
        PARSE_C
        + """
int minAuditDays(int* loads, int loadsSize);
int main() {
    char* l1=(char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    trim_nl(l1); int n=0; int* a=parseIntList(l1,&n);
    printf("%d\\n", minAuditDays(a, n));
    free(a); free(l1); return 0;
}
""",
    )
    write(data / "config.yaml", CONFIG)
    write(data / "README.md", "P7012 CF800: sort + greedy half-sum\n")
    shutil.copyfile(COMPILE_SRC, data / "compile.sh")

    rng = random.Random(7012)
    cases: list[list[int]] = [
        [3, 3, 4, 2],
        [1, 1],
        [10],
        [],
        [5, 5, 5],
        [1, 2, 3, 4, 5, 6],
        [1000000000] * 5 + [1],
        [1] * 20,
        [rng.randint(1, 1000) for _ in range(50)],
        [rng.randint(1, 10**9) for _ in range(2000)],
    ]
    for i, loads in enumerate(cases, 1):
        write(data / f"{i}.in", json.dumps(loads, separators=(",", ":")) + "\n")
        write(data / f"{i}.out", str(min_audit_days(loads)) + "\n")
        assert min_audit_days(loads) == min_audit_days(list(loads))


def setup_p7013() -> None:
    d = ROOT / "P7013"
    data = d / "data"
    write(
        d / "标题.txt",
        "标题：风险样本最小极差\n算法标签：排序,贪心\n难度：3\n",
    )
    write(
        d / "题面.md",
        """# 题目内容

安全团队要从候选风险样本里挑出恰好 `k` 个做对照实验。给定整型数组 `scores` 表示每个样本的风险评分。

希望选出的 `k` 个样本中，**最大值与最小值之差尽量小**（极差最小），以便实验条件更接近。

请返回能达到的最小极差。特殊约定：

- 若 `k <= 0`，返回 $0$
- 若 `k > scores.length`，无法选出，返回 $-1$
- 若 `k = 1`，单个样本极差为 $0$

请实现：

```text
minScoreSpread(scores: int[], k: int) -> int
```

## 输入描述

两行：

- 第一行：整型数组 `scores`，形如 `[10, 4, 7, 2, 9]`
- 第二行：整数 `k`

约束：

- $0 \\le m \\le 10^5$，$m=\\texttt{scores.length}$
- $-10^9 \\le \\texttt{scores}[i] \\le 10^9$
- $-10^5 \\le k \\le 10^5$

## 输出描述

一个整数：最小极差，或按约定返回 $0$ / $-1$。

## 样例1

输入：

```
[10, 4, 7, 2, 9]
3
```

输出：

```
3
```

说明：排序后为 `[2,4,7,9,10]`。连续三段长度 $3$ 的极差分别为 $5,5,3$，最小为 $3$（选 $7,9,10$）。

## 样例2

输入：

```
[1, 100]
1
```

输出：

```
0
```

说明：只选一个样本，极差为 $0$。

## 样例3

输入：

```
[5, 1, 3]
5
```

输出：

```
-1
```

说明：样本不够 $5$ 个。
""",
    )

    sol_py = '''from typing import List


class Solution:
    def minScoreSpread(self, scores: List[int], k: int) -> int:
        # k<=0：约定返回 0
        if k <= 0:
            return 0
        n = len(scores)
        # 样本不够
        if k > n:
            return -1
        # 单个样本极差为 0
        if k == 1:
            return 0
        # 排序后，最优解一定是某段长度为 k 的连续段
        a = sorted(scores)
        ans = a[k - 1] - a[0]
        for i in range(1, n - k + 1):
            # 维护长度为 k 的窗口极差，取最小
            ans = min(ans, a[i + k - 1] - a[i])
        return ans
'''

    sol_java = '''import java.util.*;

class Solution {
    public int minScoreSpread(int[] scores, int k) {
        // k<=0 约定返回 0
        if (k <= 0) {
            return 0;
        }
        int n = scores.length;
        // 不够 k 个
        if (k > n) {
            return -1;
        }
        // 单个样本
        if (k == 1) {
            return 0;
        }
        // 排序后枚举所有长度为 k 的连续窗口
        int[] a = Arrays.copyOf(scores, n);
        Arrays.sort(a);
        int ans = a[k - 1] - a[0];
        for (int i = 1; i + k - 1 < n; i++) {
            ans = Math.min(ans, a[i + k - 1] - a[i]);
        }
        return ans;
    }
}
'''

    sol_cc = '''#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int minScoreSpread(vector<int>& scores, int k) {
        // k<=0 约定返回 0
        if (k <= 0) return 0;
        int n = (int)scores.size();
        // 样本不够
        if (k > n) return -1;
        // 单样本极差 0
        if (k == 1) return 0;
        // 排序后最优必是连续 k 个
        vector<int> a = scores;
        sort(a.begin(), a.end());
        int ans = a[k - 1] - a[0];
        for (int i = 1; i + k - 1 < n; i++) {
            ans = min(ans, a[i + k - 1] - a[i]);
        }
        return ans;
    }
};
'''

    sol_c = '''#include <stdlib.h>
#include <limits.h>

static int cmp_asc(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

int minScoreSpread(int* scores, int scoresSize, int k) {
    /* k<=0 */
    if (k <= 0) return 0;
    /* 不够 */
    if (k > scoresSize) return -1;
    /* 单点 */
    if (k == 1) return 0;
    int* a = (int*)malloc(scoresSize * sizeof(int));
    for (int i = 0; i < scoresSize; i++) a[i] = scores[i];
    /* 升序，再扫长度为 k 的窗口 */
    qsort(a, scoresSize, sizeof(int), cmp_asc);
    int ans = a[k - 1] - a[0];
    for (int i = 1; i + k - 1 < scoresSize; i++) {
        int d = a[i + k - 1] - a[i];
        if (d < ans) ans = d;
    }
    free(a);
    return ans;
}
'''

    write(
        d / "题解.md",
        f"""## 解题思路

本题是典型的「排序 + 定长窗口极差」：

1. 先将 `scores` **升序排序**。
2. 最优的 $k$ 个值在排序后一定是某段**连续**子数组（否则中间空缺可收缩极差）。
3. 枚举所有长度为 $k$ 的窗口，计算 `a[i+k-1] - a[i]`，取最小值。

边界按题面处理：`k<=0` → $0$；`k>n` → $-1$；`k=1` → $0$。

## 复杂度分析

- 时间复杂度：$O(n\\log n)$。
- 空间复杂度：$O(n)$。

## 代码实现

### Python

```python
{sol_py.strip()}
```

### Java

```java
{sol_java.strip()}
```

### C++

```cpp
{sol_cc.strip()}
```

### C

```c
{sol_c.strip()}
```
""",
    )
    write(d / "std.py", sol_py)
    write(data / "user.py", "from typing import List\n\nclass Solution:\n    def minScoreSpread(self, scores: List[int], k: int) -> int:\n        return 0\n")
    write(data / "user.java", "import java.util.*;\npublic class Solution {\n    public int minScoreSpread(int[] scores, int k) { return 0; }\n}\n")
    write(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int minScoreSpread(vector<int>& scores, int k) { (void)scores; (void)k; return 0; }\n};\n")
    write(data / "user.c", "int minScoreSpread(int* scores, int scoresSize, int k) { (void)scores; (void)scoresSize; (void)k; return 0; }\n")
    write(
        data / "template.py",
        "import json, sys\nlines=[ln for ln in sys.stdin.read().split(\"\\n\") if ln.strip()!=\"\"]\nif len(lines)<2: raise SystemExit(0)\nprint(Solution().minScoreSpread(json.loads(lines[0]), int(lines[1].strip())))\n",
    )
    write(
        data / "template.java",
        PARSE_JAVA
        + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().minScoreSpread(parseArray1d(l1), Integer.parseInt(trim(l2))));
    }
}
""",
    )
    write(
        data / "template.cc",
        PARSE_CC
        + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto scores = parseArray1d(l1); Solution sol;
    cout << sol.minScoreSpread(scores, stoi(trim(l2))) << '\\n';
}
""",
    )
    write(
        data / "template.c",
        PARSE_C
        + """
int minScoreSpread(int* scores, int scoresSize, int k);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(64);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, 64, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n=0; int* a=parseIntList(l1,&n);
    printf("%d\\n", minScoreSpread(a, n, atoi(l2)));
    free(a); free(l1); free(l2); return 0;
}
""",
    )
    write(data / "config.yaml", CONFIG)
    write(data / "README.md", "P7013 CF800: sort + fixed window min range\n")
    shutil.copyfile(COMPILE_SRC, data / "compile.sh")

    rng = random.Random(7013)
    cases: list[tuple[list[int], int]] = [
        ([10, 4, 7, 2, 9], 3),
        ([1, 100], 1),
        ([5, 1, 3], 5),
        ([], 0),
        ([7, 7, 7, 7], 3),
        ([-5, -1, 0, 3, 10], 2),
        ([rng.randint(-100, 100) for _ in range(30)], 5),
        ([rng.randint(1, 1000) for _ in range(100)], 10),
        (list(range(0, 5000, 3)), 50),
        ([rng.randint(-(10**9), 10**9) for _ in range(3000)], 100),
    ]
    for i, (scores, k) in enumerate(cases, 1):
        write(data / f"{i}.in", json.dumps(scores, separators=(",", ":")) + "\n" + str(k) + "\n")
        write(data / f"{i}.out", str(min_score_spread(scores, k)) + "\n")


def main() -> None:
    setup_p7012()
    setup_p7013()
    # self-check samples
    assert min_audit_days([3, 3, 4, 2]) == 2
    assert min_audit_days([1, 1]) == 2
    assert min_audit_days([10]) == 1
    assert min_score_spread([10, 4, 7, 2, 9], 3) == 3
    assert min_score_spread([1, 100], 1) == 0
    assert min_score_spread([5, 1, 3], 5) == -1
    print("OK: rebuilt P7012 & P7013 (CF800)")


if __name__ == "__main__":
    main()
