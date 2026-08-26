"""为无管理员题解的 9 题补 02/03/03.5/04。"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
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


def run_code(code: str, stdin_text: str, timeout: int = 8) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run(
            [sys.executable, path],
            input=stdin_text if stdin_text.endswith("\n") else stdin_text + "\n",
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "")[-500:] or r.returncode)
    return r.stdout.replace("\r\n", "\n").rstrip("\n")


def dump_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------- P1694 对齐到每个目标 ----------
P1694_PY = r"""
import bisect, sys
def main():
    data = list(map(int, sys.stdin.read().split()))
    n, a = data[0], data[1:]
    b = sorted(a)
    pref = [0]
    for x in b:
        pref.append(pref[-1] + x)
    out = []
    for x in a:
        i = bisect.bisect_left(b, x)
        j = bisect.bisect_right(b, x)
        ans = x * i - pref[i] + (pref[n] - pref[j]) - x * (n - j)
        out.append(str(ans))
    print("\n".join(out))
if __name__ == "__main__":
    main()
"""
P1694_JAVA = r"""
import java.io.*;
import java.util.*;
public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] a = new long[n];
        long[] b = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(st.nextToken());
            b[i] = a[i];
        }
        Arrays.sort(b);
        long[] pref = new long[n + 1];
        for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + b[i];
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < n; t++) {
            long x = a[t];
            int i = lower(b, x);
            int j = upper(b, x);
            long ans = x * i - pref[i] + (pref[n] - pref[j]) - x * (n - j);
            sb.append(ans).append('\n');
        }
        System.out.print(sb);
    }
    static int lower(long[] b, long x) {
        int l = 0, r = b.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (b[m] < x) l = m + 1; else r = m;
        }
        return l;
    }
    static int upper(long[] b, long x) {
        int l = 0, r = b.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (b[m] <= x) l = m + 1; else r = m;
        }
        return l;
    }
}
"""
P1694_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<long long> a(n), b(n);
    for (int i = 0; i < n; i++) { cin >> a[i]; b[i] = a[i]; }
    sort(b.begin(), b.end());
    vector<long long> pref(n + 1);
    for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + b[i];
    for (int t = 0; t < n; t++) {
        long long x = a[t];
        int i = int(lower_bound(b.begin(), b.end(), x) - b.begin());
        int j = int(upper_bound(b.begin(), b.end(), x) - b.begin());
        long long ans = x * i - pref[i] + (pref[n] - pref[j]) - x * (n - j);
        cout << ans << '\n';
    }
}
"""

# ---------- P1695 游程合并 ----------
P1695_PY = r"""
import re, sys
s = sys.stdin.read().strip()
inner = s[1:-1] if s.startswith("[") else s
parts = [p.strip() for p in inner.split(",") if p.strip()]
vals, cnts = [], []
for p in parts:
    m = re.fullmatch(r"(-?\d+)\((\d+)\)", p)
    if not m:
        m = re.fullmatch(r"(-?\d+)", p)
        v, c = int(m.group(1)), 1
    else:
        v, c = int(m.group(1)), int(m.group(2))
    if vals and vals[-1] == v:
        cnts[-1] += c
    else:
        vals.append(v); cnts.append(c)
print("[" + ",".join(f"{v}({c})" for v, c in zip(vals, cnts)) + "]")
"""
P1695_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        if (s.startsWith("[")) s = s.substring(1, s.length() - 1);
        ArrayList<Long> vals = new ArrayList<>();
        ArrayList<Long> cnts = new ArrayList<>();
        if (!s.isEmpty()) {
            for (String p : s.split(",")) {
                p = p.trim();
                long v, c = 1;
                int lp = p.indexOf('(');
                if (lp >= 0) {
                    v = Long.parseLong(p.substring(0, lp));
                    c = Long.parseLong(p.substring(lp + 1, p.length() - 1));
                } else v = Long.parseLong(p);
                if (!vals.isEmpty() && vals.get(vals.size() - 1) == v)
                    cnts.set(cnts.size() - 1, cnts.get(cnts.size() - 1) + c);
                else { vals.add(v); cnts.add(c); }
            }
        }
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < vals.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append(vals.get(i)).append('(').append(cnts.get(i)).append(')');
        }
        sb.append(']');
        System.out.println(sb);
    }
}
"""
P1695_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    string s; getline(cin, s);
    if (!s.empty() && s.front()=='[') s = s.substr(1, s.size()-2);
    vector<long long> vals, cnts;
    stringstream ss(s);
    string p;
    while (getline(ss, p, ',')) {
        while (!p.empty() && isspace(p.front())) p.erase(p.begin());
        while (!p.empty() && isspace(p.back())) p.pop_back();
        if (p.empty()) continue;
        long long v, c = 1;
        auto lp = p.find('(');
        if (lp != string::npos) {
            v = stoll(p.substr(0, lp));
            c = stoll(p.substr(lp + 1, p.size() - lp - 2));
        } else v = stoll(p);
        if (!vals.empty() && vals.back() == v) cnts.back() += c;
        else { vals.push_back(v); cnts.push_back(c); }
    }
    cout << '[';
    for (size_t i = 0; i < vals.size(); i++) {
        if (i) cout << ',';
        cout << vals[i] << '(' << cnts[i] << ')';
    }
    cout << "]\n";
}
"""

# ---------- P1066 缓变最长段 ----------
P1066_PY = r"""
import sys
data = list(map(int, sys.stdin.read().split()))
n, a = data[0], data[1:]
best = cur = 1
for i in range(1, n):
    if abs(a[i] - a[i - 1]) <= 1:
        cur += 1
    else:
        cur = 1
    best = max(best, cur)
print(best)
"""
P1066_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = sc.nextInt();
        int best = 1, cur = 1;
        for (int i = 1; i < n; i++) {
            if (Math.abs(a[i] - a[i - 1]) <= 1) cur++;
            else cur = 1;
            best = Math.max(best, cur);
        }
        System.out.println(best);
    }
}
"""
P1066_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int best = 1, cur = 1;
    for (int i = 1; i < n; i++) {
        if (abs(a[i] - a[i - 1]) <= 1) cur++;
        else cur = 1;
        best = max(best, cur);
    }
    cout << best << '\n';
}
"""

# ---------- P1067 区间加倍（从右往左插） ----------
P1067_PY = r"""
n, q = map(int, input().split())
s = list(input().strip())
for _ in range(q):
    l, r = map(int, input().split())
    for i in range(r, l - 1, -1):
        s.insert(i, s[i - 1])
print(''.join(s))
"""
P1067_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), q = sc.nextInt();
        String str = sc.next();
        StringBuilder s = new StringBuilder(str);
        for (int t = 0; t < q; t++) {
            int l = sc.nextInt(), r = sc.nextInt();
            for (int i = r; i >= l; i--) s.insert(i, s.charAt(i - 1));
        }
        System.out.println(s);
    }
}
"""
P1067_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, q; cin >> n >> q;
    string s; cin >> s;
    while (q--) {
        int l, r; cin >> l >> r;
        for (int i = r; i >= l; --i) s.insert(s.begin() + i, s[i - 1]);
    }
    cout << s << '\n';
}
"""

# ---------- P1068 加油赶路 ----------
P1068_PY = r"""
import math
v0, x, y = map(int, input().split())
if v0 == 0:
    t = math.sqrt(y / x)
else:
    s = math.sqrt(x * y)
    t = 0.0 if s <= v0 else (s - v0) / x
speed = v0 + t * x
print(f"{t + y / speed:.5f}")
"""
P1068_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double v0 = sc.nextDouble(), x = sc.nextDouble(), y = sc.nextDouble();
        double t;
        if (v0 == 0) t = Math.sqrt(y / x);
        else {
            double s = Math.sqrt(x * y);
            t = s <= v0 ? 0.0 : (s - v0) / x;
        }
        double speed = v0 + t * x;
        System.out.printf("%.5f\n", t + y / speed);
    }
}
"""
P1068_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    long double v0, x, y; cin >> v0 >> x >> y;
    long double t;
    if (v0 == 0) t = sqrt(y / x);
    else {
        long double s = sqrt(x * y);
        t = s <= v0 ? 0.0 : (s - v0) / x;
    }
    long double speed = v0 + t * x;
    cout << fixed << setprecision(5) << (t + y / speed) << '\n';
}
"""

# ---------- P1222 you 子方格 ----------
P1222_PY = r"""
n, m = map(int, input().split())
g = [input().strip() for _ in range(n)]
ans = 0
need = set("you")
for i in range(n - 1):
    for j in range(m - 1):
        cells = {g[i][j], g[i][j+1], g[i+1][j], g[i+1][j+1]}
        if need <= cells:
            ans += 1
print(ans)
"""
P1222_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();
        String[] g = new String[n];
        for (int i = 0; i < n; i++) g[i] = sc.next();
        int ans = 0;
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < m - 1; j++) {
                boolean y = false, o = false, u = false;
                char[] cs = {g[i].charAt(j), g[i].charAt(j+1), g[i+1].charAt(j), g[i+1].charAt(j+1)};
                for (char c : cs) {
                    if (c=='y') y = true;
                    if (c=='o') o = true;
                    if (c=='u') u = true;
                }
                if (y && o && u) ans++;
            }
        System.out.println(ans);
    }
}
"""
P1222_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, m; cin >> n >> m;
    vector<string> g(n);
    for (int i = 0; i < n; i++) cin >> g[i];
    int ans = 0;
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < m - 1; j++) {
            bool y=false,o=false,u=false;
            char cs[4] = {g[i][j], g[i][j+1], g[i+1][j], g[i+1][j+1]};
            for (char c : cs) {
                if (c=='y') y=true;
                if (c=='o') o=true;
                if (c=='u') u=true;
            }
            if (y&&o&&u) ans++;
        }
    cout << ans << '\n';
}
"""

# ---------- P1223 a+b=n 最大 lcm ----------
P1223_PY = r"""
import math, sys
def solve(n):
    if n % 2 == 1:
        return n // 2, n - n // 2
    a = n // 2
    while math.gcd(a, n) != 1:
        a -= 1
    return a, n - a
data = list(map(int, sys.stdin.read().split()))
t = data[0]
out = []
for n in data[1:1+t]:
    a, b = solve(n)
    out.append(f"{a} {b}")
print("\n".join(out))
"""
P1223_JAVA = r"""
import java.io.*;
import java.util.*;
public class Main {
    static long gcd(long a, long b) {
        while (b != 0) { long t = a % b; a = b; b = t; }
        return a;
    }
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < t; i++) {
            long n = Long.parseLong(br.readLine().trim());
            long a;
            if (n % 2 == 1) a = n / 2;
            else {
                a = n / 2;
                while (gcd(a, n) != 1) a--;
            }
            sb.append(a).append(' ').append(n - a).append('\n');
        }
        System.out.print(sb);
    }
}
"""
P1223_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t; cin >> t;
    while (t--) {
        long long n; cin >> n;
        long long a;
        if (n % 2) a = n / 2;
        else {
            a = n / 2;
            while (__gcd(a, n) != 1) a--;
        }
        cout << a << ' ' << n - a << '\n';
    }
}
"""

# ---------- P1224 树上二进制路径 ----------
P1224_PY = r"""
import sys
sys.setrecursionlimit(10000)
n, L, R = map(int, input().split())
s = input().strip()
g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    u -= 1; v -= 1
    g[u].append(v); g[v].append(u)
ans = 0
def dfs(u, p, val, edges):
    global ans
    if edges >= 1 and L <= val <= R:
        ans += 1
    if val > R and val > 0:
        return
    for v in g[u]:
        if v == p: continue
        nval = val * 2 + (1 if s[v] == '1' else 0)
        dfs(v, u, nval, edges + 1)
for i in range(n):
    dfs(i, -1, 1 if s[i] == '1' else 0, 0)
print(ans)
"""
P1224_JAVA = r"""
import java.util.*;
public class Main {
    static ArrayList<Integer>[] g;
    static String s;
    static long L, R;
    static int ans;
    static void dfs(int u, int p, long val, int edges) {
        if (edges >= 1 && L <= val && val <= R) ans++;
        if (val > R && val > 0) return;
        for (int v : g[u]) if (v != p) {
            long nval = val * 2 + (s.charAt(v) == '1' ? 1 : 0);
            dfs(v, u, nval, edges + 1);
        }
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        L = sc.nextLong(); R = sc.nextLong();
        s = sc.next();
        g = new ArrayList[n];
        for (int i = 0; i < n; i++) g[i] = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt() - 1, v = sc.nextInt() - 1;
            g[u].add(v); g[v].add(u);
        }
        for (int i = 0; i < n; i++) dfs(i, -1, s.charAt(i) == '1' ? 1 : 0, 0);
        System.out.println(ans);
    }
}
"""
P1224_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
vector<int> g[1010];
string s;
long long L, R;
int ans;
void dfs(int u, int p, long long val, int edges) {
    if (edges >= 1 && L <= val && val <= R) ans++;
    if (val > R && val > 0) return;
    for (int v : g[u]) if (v != p) {
        long long nval = val * 2 + (s[v] == '1');
        dfs(v, u, nval, edges + 1);
    }
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n >> L >> R >> s;
    for (int i = 0; i < n - 1; i++) {
        int u, v; cin >> u >> v; --u; --v;
        g[u].push_back(v); g[v].push_back(u);
    }
    for (int i = 0; i < n; i++) dfs(i, -1, s[i] == '1', 0);
    cout << ans << '\n';
}
"""

# ---------- P1225 游程回文子串 ----------
P1225_PY = r"""
MOD = 10**9 + 7
n = int(input())
a = list(map(int, input().split()))
ans = 0
for x in a:
    ans = (ans + x * (x + 1) // 2) % MOD
for i in range(n):
    ok = True
    for j in range(i + 2, n, 2):
        mid = (i + j) // 2
        # check a[i+1..j-1] is palindrome as sequence — expand step by step
        k = (j - i) // 2
        for t in range(1, k):
            if a[i + t] != a[j - t]:
                ok = False
                break
        if not ok:
            break
        ans = (ans + min(a[i], a[j])) % MOD
print(ans)
"""
P1225_JAVA = r"""
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = sc.nextLong();
        final long MOD = 1000000007;
        long ans = 0;
        for (long x : a) ans = (ans + x * (x + 1) / 2) % MOD;
        for (int i = 0; i < n; i++) {
            boolean ok = true;
            for (int j = i + 2; j < n; j += 2) {
                int k = (j - i) / 2;
                for (int t = 1; t < k; t++) if (a[i + t] != a[j - t]) { ok = false; break; }
                if (!ok) break;
                ans = (ans + Math.min(a[i], a[j])) % MOD;
            }
        }
        System.out.println(ans);
    }
}
"""
P1225_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    const long long MOD = 1000000007;
    long long ans = 0;
    for (auto x : a) ans = (ans + x * (x + 1) / 2) % MOD;
    for (int i = 0; i < n; i++) {
        bool ok = true;
        for (int j = i + 2; j < n; j += 2) {
            int k = (j - i) / 2;
            for (int t = 1; t < k; t++) if (a[i + t] != a[j - t]) { ok = false; break; }
            if (!ok) break;
            ans = (ans + min(a[i], a[j])) % MOD;
        }
    }
    cout << ans << '\n';
}
"""

PROBLEMS = {
    "P1694": {
        "title": "对齐代价",
        "content": "给定长度为 $n$ 的数组。一次操作可以把任意一个元素加 `1` 或减 `1`。\n\n对每个下标 $i$，求把所有元素都变成与 $a_i$ 相等所需的最少操作次数。\n\n数组长度不超过 `10^5`，元素为正整数且不超过 `10^9`。",
        "input_description": "第一行一个正整数 $n$。\n第二行 $n$ 个正整数 $a_i$。\n保证 $1 \\le n \\le 10^5$，$1 \\le a_i \\le 10^9$。",
        "output_description": "输出 $n$ 行，第 $i$ 行表示目标值为 $a_i$ 时的最少操作次数。",
        "idea": "把所有数变成某个目标 $x$ 的代价是 $\\sum |a_j-x|$。对每个原来的 $a_i$ 都要求这个值。\n\n将数组排序并做前缀和后，对任意 $x$ 可用二分定位，在 $O(\\log n)$ 内算出小于 $x$ 与大于 $x$ 两部分的代价。",
        "comp": "时间复杂度 $O(n \\log n)$，空间复杂度 $O(n)$。",
        "py": P1694_PY, "java": P1694_JAVA, "cpp": P1694_CPP,
        "samples_in": ["4\n3 1 5 2", "1\n7", "5\n1 1 1 1 1"],
    },
    "P1695": {
        "title": "相邻段合并",
        "content": "用游程编码表示一个整数序列：`v(c)` 表示值 $v$ 连续出现 $c$ 次。输入可能已经部分压缩，但相邻两段的值仍可能相同，需要把它们合并。\n\n输入是形如 $[v_1(c_1),v_2(c_2),\\ldots]$ 的字符串。输出合并相邻同值段之后的同样格式。\n\n字符串长度不超过 `10^5`，每个值的绝对值不超过 `10^9`。",
        "input_description": "一行一个字符串，表示待合并的游程编码数组，格式为 $[v(c),\\ldots]$。",
        "output_description": "输出合并后的游程编码数组，格式相同。",
        "idea": "从左到右解析每一段 $v(c)$。若当前值与上一段相同，把次数累加；否则新开一段。",
        "comp": "时间复杂度 $O(|s|)$，空间复杂度 $O(|s|)$。",
        "py": P1695_PY, "java": P1695_JAVA, "cpp": P1695_CPP,
        "samples_in": ["[2(1),2(4),3(1)]", "[-3(2),-3(1),5(1),5(2)]", "[7(1)]"],
    },
    "P1066": {
        "title": "缓变最长段",
        "content": "称一段连续子数组是缓变的，当且仅当其中每一对相邻元素的差的绝对值都不超过 `1`。\n\n给定长度为 $n$ 的数组，求最长缓变连续子数组的长度。\n\n$n$ 不超过 `10^5`，元素为正整数且不超过 `10^9`。",
        "input_description": "第一行一个正整数 $n$。\n第二行 $n$ 个正整数。\n保证 $1 \\le n \\le 10^5$，$1 \\le a_i \\le 10^9$。",
        "output_description": "输出一个正整数，表示最长缓变连续子数组的长度。",
        "idea": "从左到右扫描。若 $|a_i-a_{i-1}|\\le 1$ 则当前段加一，否则从 `1` 重新开始。维护全程最大值。",
        "comp": "时间复杂度 $O(n)$，空间复杂度 $O(n)$。",
        "py": P1066_PY, "java": P1066_JAVA, "cpp": P1066_CPP,
        "samples_in": ["5\n1 2 2 4 5", "3\n10 10 10", "4\n1 3 5 7"],
    },
    "P1067": {
        "title": "区间加倍展开",
        "content": "有一个长度为 $n$ 的小写字母串。每次操作给定区间 $[l,r]$（下标从 `1` 开始），把该区间内每个字符在其后方再插入一份相同字符。为保持下标正确，应从右往左依次插入。\n\n进行 $q$ 次操作后，输出最终字符串。\n\n保证 $1 \\le n \\le 1000$，$1 \\le q \\le 10$，每次操作时 $r$ 不超过当前串长。",
        "input_description": "第一行两个正整数 $n$ 和 $q$。\n第二行一个长度为 $n$ 的小写字母串。\n接下来 $q$ 行，每行两个正整数 $l$ $r$。",
        "output_description": "输出一行，表示所有操作结束后的字符串。",
        "idea": "用可变序列存储字符串。每次从 $r$ 倒到 $l$，在位置 $i$ 处插入 $s_{i}$（1-based 的第 $i$ 个字符）。$q$ 很小，直接模拟即可。",
        "comp": "时间复杂度与最终串长及 $q$ 有关，在给定范围内可接受；空间复杂度 $O(L)$，$L$ 为最终长度。",
        "py": P1067_PY, "java": P1067_JAVA, "cpp": P1067_CPP,
        "samples_in": ["3 1\nxyz\n1 2", "4 2\nwxyz\n2 2\n1 3", "2 1\nab\n1 1"],
    },
    "P1068": {
        "title": "停站加油",
        "content": "车辆初始最高速度为 $v_0$。在出发前可以停留 $t$ 个时间单位加油，之后最高速度变为 $v_0+t\\times x$，行驶中油量不再减少。需要行驶总里程 $y$，行驶时间是里程除以当时最高速度。总耗时为停留时间加行驶时间。可以停留任意非负实数时间，求最小总耗时。\n\n$0 \\le v_0 \\le 10^9$，$1 \\le x,y \\le 10^9$。",
        "input_description": "一行三个整数 $v_0$ $x$ $y$，用空格隔开。",
        "output_description": "输出一个浮点数，保留五位小数，表示最小总耗时。",
        "idea": "总时间 $f(t)=t+y/(v_0+tx)$（$t\\ge 0$，且速度必须为正）。求导得驻点满足 $(v_0+tx)^2=xy$。若 $\\sqrt{xy}\\le v_0$ 则不必停留；否则 $t=(\\sqrt{xy}-v_0)/x$。$v_0=0$ 时取 $t=\\sqrt{y/x}$。",
        "comp": "时间复杂度 $O(1)$，空间复杂度 $O(1)$。",
        "py": P1068_PY, "java": P1068_JAVA, "cpp": P1068_CPP,
        "samples_in": ["2 4 8", "0 1 4", "10 1 1"],
    },
    "P1222": {
        "title": "三字母窗",
        "content": "给定 $n$ 行 $m$ 列的小写字母矩阵。统计有多少个 $2\\times 2$ 子矩阵，其四个格子的字符集合同时包含 `y`、`o`、`u` 三种字母。\n\n$1 \\le n,m \\le 10^3$。",
        "input_description": "第一行两个正整数 $n$ 和 $m$。\n接下来 $n$ 行，每行一个长度为 $m$ 的小写字母串。",
        "output_description": "输出一个整数，表示符合条件的 $2\\times 2$ 子矩阵个数。",
        "idea": "枚举每个 $2\\times 2$ 窗口左上角，检查四个字符组成的集合是否覆盖 `y`、`o`、`u`。",
        "comp": "时间复杂度 $O(nm)$，空间复杂度 $O(nm)$。",
        "py": P1222_PY, "java": P1222_JAVA, "cpp": P1222_CPP,
        "samples_in": ["2 2\nyo\nux", "3 3\nabc\ndef\nghi", "2 3\nyou\nouy"],
    },
    "P1223": {
        "title": "拆分最大公倍",
        "content": "给定正整数 $n$，需要把它拆成两个正整数 $a+b=n$，使得 $\\mathrm{lcm}(a,b)$ 尽可能大。多组询问。\n\n询问次数不超过 `10^5`，$2 \\le n \\le 10^{13}$。",
        "input_description": "第一行一个正整数 $t$。\n接下来 $t$ 行，每行一个正整数 $n$。\n保证 $1 \\le t \\le 10^5$，$2 \\le n \\le 10^{13}$。",
        "output_description": "对每组询问输出一行两个正整数 $a$ 和 $b$，用空格隔开。",
        "idea": "$\\mathrm{lcm}(a,n-a)=a(n-a)/\\gcd(a,n)$。奇数 $n$ 时取相邻两半即可（互质）。偶数 $n$ 时从 $n/2$ 向下找到与 $n$ 互质的 $a$，此时 $a$ 与 $n-a$ 都尽量接近且 $\\gcd(a,n)=1$。",
        "comp": "单次询问在与 $n$ 互质的间隔内扫描，总体可在时限内通过。空间复杂度 $O(1)$。",
        "py": P1223_PY, "java": P1223_JAVA, "cpp": P1223_CPP,
        "samples_in": ["3\n3\n6\n9", "1\n8", "2\n15\n16"],
    },
    "P1224": {
        "title": "路径二进制值",
        "content": "一棵 $n$ 个节点的树，每个节点权值为 `0` 或 `1`。一条至少包含一条边的路径，沿途节点权值（从起点到终点）组成一个二进制数（起点为最高位）。统计有多少条有向路径，其数值落在闭区间 $[l,r]$ 内。单节点不是合法路径。\n\n$1 \\le n \\le 10^3$，$1 \\le l \\le r \\le 10^{14}$。",
        "input_description": "第一行三个正整数 $n$ $l$ $r$。\n第二行一个长度为 $n$ 的 `01` 串，第 $i$ 个字符是节点 $i$ 的权值。\n接下来 $n-1$ 行，每行两个正整数 $u$ $v$ 表示树边。",
        "output_description": "输出一个整数，表示合法有向路径的条数。",
        "idea": "$n\\le 10^3$，从每个起点沿树 DFS 不回头，维护当前二进制值。走过至少一条边后，若值落在 $[l,r]$ 中则计数。值已超过 $r$ 且为正时可以剪枝。",
        "comp": "时间复杂度 $O(n^2)$，空间复杂度 $O(n)$。",
        "py": P1224_PY, "java": P1224_JAVA, "cpp": P1224_CPP,
        "samples_in": ["3 1 10\n101\n1 2\n2 3", "2 1 1\n10\n1 2", "4 3 8\n1110\n1 2\n1 3\n3 4"],
    },
    "P1225": {
        "title": "游程回文计数",
        "content": "一个 `01` 串被压缩成 $n$ 段交替的连续段：第 `1` 段有 $a_1$ 个 `1`，第 `2` 段有 $a_2$ 个 `0`，第 `3` 段又是 `1`，依此类推。求该串中非空回文子串的数量，对 $10^9+7$ 取模。\n\n$1 \\le n \\le 1000$，$1 \\le a_i \\le 10^9$。",
        "input_description": "第一行一个正整数 $n$。\n第二行 $n$ 个正整数 $a_i$。",
        "output_description": "输出回文子串个数对 $10^9+7$ 取模的结果。",
        "idea": "全相同的一段内部所有子串都是回文，贡献 $a(a+1)/2$。相邻两段字符不同，偶回文无法跨段。跨至少三段的奇回文：取奇数段 $i..j$（$j-i$ 为偶数），中间段的长度序列成回文时，两端各取 $x=1..\\min(a_i,a_j)$ 个字符，贡献 $\\min(a_i,a_j)$。",
        "comp": "时间复杂度 $O(n^2)$，空间复杂度 $O(n)$。",
        "py": P1225_PY, "java": P1225_JAVA, "cpp": P1225_CPP,
        "samples_in": ["3\n3 1 3", "1\n5", "5\n1 1 1 1 1"],
    },
}


def main() -> None:
    from forbid_orig_sample import original_forbidden, sample_hits_original

    for pid, spec in PROBLEMS.items():
        d = ROOT / pid
        md = wrap(spec["idea"], spec["comp"], spec["py"], spec["java"], spec["cpp"])
        (d / "02_原始完整题解.md").write_text(md, encoding="utf-8")
        (d / "02_题解代码.py").write_text(spec["py"].strip() + "\n", encoding="utf-8")
        (d / "03.5_修改后的题解.md").write_text(md, encoding="utf-8")
        dump_json(
            d / "03_LLM生成的新题面.json",
            {
                "title": spec["title"],
                "content": spec["content"],
                "input_description": spec["input_description"],
                "output_description": spec["output_description"],
            },
        )
        orig = (d / "01_原始题面.md").read_text(encoding="utf-8")
        fb = original_forbidden(orig)
        samples = []
        for inp in spec["samples_in"]:
            hit = sample_hits_original(inp, fb)
            if hit:
                print(pid, "HIT", hit, repr(inp))
                continue
            out = run_code(spec["py"], inp)
            samples.append({"input": inp, "output": out, "explanation": "按题意模拟计算得到。"})
        if len(samples) < 2:
            raise SystemExit(f"{pid}: samples {len(samples)}")
        dump_json(d / "04_LLM生成的新样例.json", {"samples": samples})
        print(pid, spec["title"], [s["output"][:40] for s in samples])


if __name__ == "__main__":
    main()
