# -*- coding: utf-8 -*-
"""Rebuild P7013 (binary search) and P7014 (simulation/prefix max). P7012 stays greedy."""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
COMPILE_SRC = REPO / "compile.sh"

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


def count_need_upgrade(versions: list[int], baseline: int) -> int:
    a = sorted(versions)
    # first index with a[i] >= baseline
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < baseline:
            lo = mid + 1
        else:
            hi = mid
    return len(a) - lo


def max_online(changes: list[int]) -> int:
    cur = ans = 0
    for x in changes:
        cur += x
        if cur > ans:
            ans = cur
    return ans


def setup_p7013() -> None:
    d = ROOT / "P7013"
    data = d / "data"
    write(d / "标题.txt", "标题：补丁基线待升级计数\n算法标签：二分查找\n难度：3\n")
    write(
        d / "题面.md",
        """# 题目内容

漏洞库中记录了若干已安装补丁的版本号 `versions`（下标从 $0$ 开始，未必有序）。安全基线为整数 `baseline`。

凡版本号 **大于等于** `baseline` 的补丁，都视为「相对基线仍需纳入升级巡检」。

请返回需要纳入巡检的补丁数量。

请实现：

```text
countNeedUpgrade(versions: int[], baseline: int) -> int
```

## 输入描述

两行：

- 第一行：整型数组 `versions`，形如 `[1, 5, 3, 8, 5]`
- 第二行：整数 `baseline`

约束：

- $0 \\le n \\le 10^5$，$n=\\texttt{versions.length}$
- $1 \\le \\texttt{versions}[i] \\le 10^9$
- $1 \\le \\textit{baseline} \\le 10^9$

## 输出描述

一个整数：版本号 $\\ge \\textit{baseline}$ 的个数。

## 样例1

输入：

```
[1, 5, 3, 8, 5]
5
```

输出：

```
3
```

说明：$5,8,5$ 均 $\\ge 5$，共 $3$ 个。

## 样例2

输入：

```
[2, 2, 2]
3
```

输出：

```
0
```

说明：全部小于基线。

## 样例3

输入：

```
[10]
10
```

输出：

```
1
```

说明：恰好等于基线也要计入。
""",
    )

    sol_py = '''from typing import List


class Solution:
    def countNeedUpgrade(self, versions: List[int], baseline: int) -> int:
        # 先排序，才能二分找「第一个 >= baseline」的位置
        a = sorted(versions)
        n = len(a)
        lo, hi = 0, n
        # 标准 lower_bound：找到最左满足 a[i] >= baseline 的下标
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < baseline:
                # 中点仍偏小，答案在右半
                lo = mid + 1
            else:
                # 中点可能就是答案，或还在左边
                hi = mid
        # [lo, n) 都是 >= baseline
        return n - lo
'''

    sol_java = '''import java.util.*;

class Solution {
    public int countNeedUpgrade(int[] versions, int baseline) {
        // 复制后排序，便于二分
        int n = versions.length;
        int[] a = Arrays.copyOf(versions, n);
        Arrays.sort(a);
        // lower_bound：第一个 >= baseline 的下标
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (a[mid] < baseline) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        // 从 lo 到末尾均需巡检
        return n - lo;
    }
}
'''

    sol_cc = '''#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int countNeedUpgrade(vector<int>& versions, int baseline) {
        // 排序后用 lower_bound 找第一个 >= baseline
        vector<int> a = versions;
        sort(a.begin(), a.end());
        auto it = lower_bound(a.begin(), a.end(), baseline);
        // 距离末尾即为答案个数
        return (int)(a.end() - it);
    }
};
'''

    sol_c = '''#include <stdlib.h>

static int cmp_asc(const void* pa, const void* pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

int countNeedUpgrade(int* versions, int versionsSize, int baseline) {
    /* 空数组 */
    if (versionsSize <= 0) return 0;
    int* a = (int*)malloc(versionsSize * sizeof(int));
    for (int i = 0; i < versionsSize; i++) a[i] = versions[i];
    /* 升序排序 */
    qsort(a, versionsSize, sizeof(int), cmp_asc);
    /* 手写二分 lower_bound */
    int lo = 0, hi = versionsSize;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < baseline) lo = mid + 1;
        else hi = mid;
    }
    int ans = versionsSize - lo;
    free(a);
    return ans;
}
'''

    write(
        d / "题解.md",
        f"""## 解题思路

需要统计「版本号 $\\ge$ 基线」的个数。数据可达 $10^5$，不宜对每个元素反复扫描以外的低效做法；正解是：

1. 将 `versions` **升序排序**
2. 用**二分查找**（`lower_bound`）找到第一个 $\\ge \\textit{{baseline}}$ 的下标 `lo`
3. 答案为 $n - lo$

也可以排序后暴力从左扫到第一个满足条件的位置，复杂度同为 $O(n\\log n)$ 主导；题解强调二分以体现查找思想。

## 复杂度分析

- 时间复杂度：$O(n\\log n)$
- 空间复杂度：$O(n)$

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
    write(data / "user.py", "from typing import List\n\nclass Solution:\n    def countNeedUpgrade(self, versions: List[int], baseline: int) -> int:\n        return 0\n")
    write(data / "user.java", "import java.util.*;\npublic class Solution {\n    public int countNeedUpgrade(int[] versions, int baseline) { return 0; }\n}\n")
    write(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int countNeedUpgrade(vector<int>& versions, int baseline) { (void)versions; (void)baseline; return 0; }\n};\n")
    write(data / "user.c", "int countNeedUpgrade(int* versions, int versionsSize, int baseline) { (void)versions; (void)versionsSize; (void)baseline; return 0; }\n")
    write(data / "template.py", "import json, sys\nlines=[ln for ln in sys.stdin.read().split(\"\\n\") if ln.strip()!=\"\"]\nif len(lines)<2: raise SystemExit(0)\nprint(Solution().countNeedUpgrade(json.loads(lines[0]), int(lines[1].strip())))\n")
    write(data / "template.java", PARSE_JAVA + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().countNeedUpgrade(parseArray1d(l1), Integer.parseInt(trim(l2))));
    }
}
""")
    write(data / "template.cc", PARSE_CC + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto versions = parseArray1d(l1); Solution sol;
    cout << sol.countNeedUpgrade(versions, stoi(trim(l2))) << '\\n';
}
""")
    write(data / "template.c", PARSE_C + """
int countNeedUpgrade(int* versions, int versionsSize, int baseline);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(64);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, 64, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n=0; int* a=parseIntList(l1,&n);
    printf("%d\\n", countNeedUpgrade(a, n, atoi(l2)));
    free(a); free(l1); free(l2); return 0;
}
""")
    write(data / "config.yaml", CONFIG)
    write(data / "README.md", "P7013: binary search count >= baseline\n")
    shutil.copyfile(COMPILE_SRC, data / "compile.sh")

    rng = random.Random(7013)
    cases = [
        ([1, 5, 3, 8, 5], 5),
        ([2, 2, 2], 3),
        ([10], 10),
        ([], 1),
        ([1, 2, 3, 4, 5], 1),
        ([1, 2, 3, 4, 5], 6),
        ([7, 7, 7, 7], 7),
        ([rng.randint(1, 1000) for _ in range(40)], 500),
        (list(range(1, 2001)), 1500),
        ([rng.randint(1, 10**9) for _ in range(5000)], rng.randint(1, 10**9)),
    ]
    for i, (v, b) in enumerate(cases, 1):
        write(data / f"{i}.in", json.dumps(v, separators=(",", ":")) + "\n" + str(b) + "\n")
        write(data / f"{i}.out", str(count_need_upgrade(v, b)) + "\n")


def setup_p7014() -> None:
    d = ROOT / "P7014"
    data = d / "data"
    write(d / "标题.txt", "标题：网关在线连接峰值\n算法标签：模拟\n难度：3\n")
    write(
        d / "题面.md",
        """# 题目内容

零信任网关按时间顺序记录连接数变化序列 `changes`（下标从 $0$ 开始）：

- `changes[i] > 0`：该时刻新建立的连接数
- `changes[i] < 0`：该时刻断开的连接数
- `changes[i] = 0`：无变化

初始在线连接数为 $0$。请按顺序模拟，返回过程中**在线连接数的历史最大值**。

保证：任意前缀和均 $\\ge 0$（不会出现「断开数多于当前在线」的非法数据）。

请实现：

```text
maxOnline(changes: int[]) -> int
```

## 输入描述

一行：整型数组 `changes`，形如 `[1, 2, -1, 3, -2]`

约束：

- $0 \\le n \\le 10^5$，$n=\\texttt{changes.length}$
- $-10^4 \\le \\texttt{changes}[i] \\le 10^4$
- 保证任意前缀和 $\\ge 0$，且答案可用 $32$ 位有符号整数表示

## 输出描述

一个整数：历史最大在线连接数；若 `changes` 为空，返回 $0$。

## 样例1

输入：

```
[1, 2, -1, 3, -2]
```

输出：

```
5
```

说明：在线数变化为 $1 \\to 3 \\to 2 \\to 5 \\to 3$，峰值为 $5$。

## 样例2

输入：

```
[3, -1, -1, -1]
```

输出：

```
3
```

说明：一开始升到 $3$，之后只减不增。

## 样例3

输入：

```
[]
```

输出：

```
0
```

说明：无事件，峰值为 $0$。
""",
    )

    sol_py = '''from typing import List


class Solution:
    def maxOnline(self, changes: List[int]) -> int:
        # cur：当前在线；ans：历史峰值
        cur = 0
        ans = 0
        for x in changes:
            # 按时间顺序累加变化量
            cur += x
            # 维护前缀最大值
            if cur > ans:
                ans = cur
        return ans
'''

    sol_java = '''class Solution {
    public int maxOnline(int[] changes) {
        // cur 当前在线，ans 历史峰值
        int cur = 0;
        int ans = 0;
        for (int x : changes) {
            // 模拟每一时刻的增减
            cur += x;
            if (cur > ans) {
                ans = cur;
            }
        }
        return ans;
    }
}
'''

    sol_cc = '''#include <vector>
using namespace std;

class Solution {
public:
    int maxOnline(vector<int>& changes) {
        // 顺序模拟前缀和，并记录最大值
        int cur = 0;
        int ans = 0;
        for (int x : changes) {
            cur += x;
            if (cur > ans) ans = cur;
        }
        return ans;
    }
};
'''

    sol_c = '''int maxOnline(int* changes, int changesSize) {
    /* 空序列峰值 0 */
    int cur = 0;
    int ans = 0;
    for (int i = 0; i < changesSize; i++) {
        /* 累加并更新峰值 */
        cur += changes[i];
        if (cur > ans) ans = cur;
    }
    return ans;
}
'''

    write(
        d / "题解.md",
        f"""## 解题思路

这是一道**顺序模拟 / 前缀最大值**题：

1. 用变量 `cur` 维护当前在线连接数，初始为 $0$
2. 按时间依次加上 `changes[i]`
3. 用 `ans` 记录过程中出现过的最大 `cur`

题面保证前缀和非负，因此不必处理负数在线。

## 复杂度分析

- 时间复杂度：$O(n)$，单次遍历
- 空间复杂度：$O(1)$

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
    write(data / "user.py", "from typing import List\n\nclass Solution:\n    def maxOnline(self, changes: List[int]) -> int:\n        return 0\n")
    write(data / "user.java", "public class Solution {\n    public int maxOnline(int[] changes) { return 0; }\n}\n")
    write(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int maxOnline(vector<int>& changes) { (void)changes; return 0; }\n};\n")
    write(data / "user.c", "int maxOnline(int* changes, int changesSize) { (void)changes; (void)changesSize; return 0; }\n")
    write(data / "template.py", "import json, sys\nlines=[ln for ln in sys.stdin.read().split(\"\\n\") if ln.strip()!=\"\"]\nif not lines: raise SystemExit(0)\nprint(Solution().maxOnline(json.loads(lines[0])))\n")
    write(data / "template.java", PARSE_JAVA + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine();
        if (l1 == null) return;
        System.out.println(new Solution().maxOnline(parseArray1d(l1)));
    }
}
""")
    write(data / "template.cc", PARSE_CC + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1; if (!getline(cin, l1)) return 0;
    auto changes = parseArray1d(l1); Solution sol;
    cout << sol.maxOnline(changes) << '\\n';
}
""")
    write(data / "template.c", PARSE_C + """
int maxOnline(int* changes, int changesSize);
int main() {
    char* l1=(char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin)) return 0;
    trim_nl(l1); int n=0; int* a=parseIntList(l1,&n);
    printf("%d\\n", maxOnline(a, n));
    free(a); free(l1); return 0;
}
""")
    write(data / "config.yaml", CONFIG)
    write(data / "README.md", "P7014: simulation prefix max online\n")
    shutil.copyfile(COMPILE_SRC, data / "compile.sh")

    rng = random.Random(7014)

    def gen_valid(n: int) -> list[int]:
        cur = 0
        out = []
        for _ in range(n):
            # random delta keeping cur >= 0
            up = rng.randint(0, 20)
            down = rng.randint(0, cur)
            if rng.random() < 0.55:
                x = up
            else:
                x = -down if down > 0 else up
            cur += x
            out.append(x)
        return out

    cases = [
        [1, 2, -1, 3, -2],
        [3, -1, -1, -1],
        [],
        [5],
        [1, 1, 1, 1, -4],
        gen_valid(30),
        gen_valid(100),
        [10, -3, -3, 5, -9],
        gen_valid(2000),
        gen_valid(8000),
    ]
    for i, ch in enumerate(cases, 1):
        write(data / f"{i}.in", json.dumps(ch, separators=(",", ":")) + "\n")
        write(data / f"{i}.out", str(max_online(ch)) + "\n")


def main() -> None:
    setup_p7013()
    setup_p7014()
    assert count_need_upgrade([1, 5, 3, 8, 5], 5) == 3
    assert count_need_upgrade([2, 2, 2], 3) == 0
    assert count_need_upgrade([10], 10) == 1
    assert max_online([1, 2, -1, 3, -2]) == 5
    assert max_online([3, -1, -1, -1]) == 3
    assert max_online([]) == 0
    print("OK: rebuilt P7013 (binary) & P7014 (simulation)")


if __name__ == "__main__":
    main()
