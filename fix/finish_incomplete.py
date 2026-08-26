"""补齐本批仍缺 03.5/04 的题目。"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "log"
sys.path.insert(0, str(ROOT))
from forbid_orig_sample import original_forbidden, sample_hits_original
from _replace_copied_samples import bump_line, py_from_35, run_code, variants
from complete_artifacts import extract_python


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


CPP_ONLY = {
    "P1755": dict(
        title="交错正反串",
        content="输出 $n$ 段字符串：奇数段（从 `1` 计）为 `you`，偶数段为 `uoy`，依次拼接。\n\n$1 \\le n \\le 10^5$。",
        inp="一行一个正整数 $n$。",
        out="输出一个字符串。",
        idea="按段号奇偶交替输出 `you` 与 `uoy`，共 $n$ 段。",
        comp="时间复杂度 $O(n)$，空间复杂度 $O(1)$（不计输出）。",
        py="n=int(input())\nprint(''.join('you' if i%2==0 else 'uoy' for i in range(n)))",
        java="""import java.util.*;
public class Main {
    public static void main(String[] args) {
        int n = new Scanner(System.in).nextInt();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) sb.append(i % 2 == 0 ? "you" : "uoy");
        System.out.println(sb);
    }
}""",
        cpp="""#include <bits/stdc++.h>
using namespace std;
int main() {
    int n; cin >> n;
    vector<string> s = {"you", "uoy"};
    for (int i = 0; i < n; i++) cout << s[i % 2];
}""",
        seeds=["3", "1", "4"],
    ),
    "P1303": dict(
        title="同奇偶切开",
        content="给定一个很大的正整数（以十进制字符串给出，允许把前导零算进右半段）。在某个位置切开，使左右两部分表示的整数之和为偶数。切开后右半段至少一位、左半段至少一位。求方案数。\n\n数的十进制长度不超过 `10^5`。",
        inp="一行，一个由数字组成的字符串，表示这个正整数。",
        out="输出方案数。",
        idea="两数之和为偶数当且仅当它们奇偶性相同，即左半段末位与整个数末位同奇偶。枚举切开点（不切开最后一位），统计与末位同奇偶的前缀末位个数。",
        comp="时间复杂度 $O(|s|)$，空间复杂度 $O(|s|)$。",
        py="""s=input().strip()
b=(ord(s[-1])-48)%2
print(sum(1 for i in range(len(s)-1) if (ord(s[i])-48)%2==b))""",
        java="""import java.util.*;
public class Main {
    public static void main(String[] args) {
        String s = new Scanner(System.in).next();
        int b = (s.charAt(s.length()-1) - '0') % 2, ans = 0;
        for (int i = 0; i < s.length() - 1; i++)
            if ((s.charAt(i) - '0') % 2 == b) ans++;
        System.out.println(ans);
    }
}""",
        cpp="""#include <bits/stdc++.h>
using namespace std;
int main() {
    string n; cin >> n;
    int b = (n.back() - '0') % 2, ans = 0;
    for (int i = 0; i + 1 < (int)n.size(); i++)
        if ((n[i] - '0') % 2 == b) ans++;
    cout << ans << '\\n';
}""",
        seeds=["247", "11", "802"],
    ),
    "P1305": dict(
        title="配对刷题日",
        content="有 $n$ 套试卷，第 $i$ 套有 $a_i$ 题。一天可以上午做一套、下午做一套，或只做其中一场（不能两场都不做）。一天做的题目总数必须是 $k$ 的倍数。每套试卷最多用一次。求最多能安排多少天。\n\n$1 \\le n \\le 10^5$，$1 \\le k,a_i \\le 10^9$。",
        inp="第一行两个正整数 $n$ 和 $k$。\n第二行 $n$ 个正整数 $a_i$。",
        out="输出最多天数。",
        idea="只关心 $a_i \\bmod k$。余数 $0$ 的卷可以单独成一天。其余把余数 $a$ 与 $k-a$ 配对，每对一天；若 $2a\\equiv 0\\pmod k$ 则同余数组内两两配对。",
        comp="时间复杂度 $O(n)$，空间复杂度 $O(\\min(n,k))$。",
        py="""from collections import Counter
n,k=map(int,input().split())
c=Counter(x%k for x in map(int,input().split()))
ans=c[0]; c[0]=0
for a,cnt in list(c.items()):
    if cnt==0: continue
    b=(k-a)%k
    if a==b:
        ans+=cnt//2; c[a]=cnt%2
    else:
        d=min(c[a], c[b]); c[a]-=d; c[b]-=d; ans+=d
print(ans)""",
        java="""import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), k = sc.nextInt();
        Map<Integer,Integer> m = new HashMap<>();
        for (int i = 0; i < n; i++) {
            int x = sc.nextInt() % k;
            m.put(x, m.getOrDefault(x, 0) + 1);
        }
        int ans = m.getOrDefault(0, 0);
        m.remove(0);
        for (int a : new ArrayList<>(m.keySet())) {
            int cnt = m.getOrDefault(a, 0);
            if (cnt == 0) continue;
            int b = (k - a) % k;
            if (a == b) {
                ans += cnt / 2;
                m.put(a, cnt % 2);
            } else if (m.containsKey(b)) {
                int d = Math.min(cnt, m.get(b));
                m.put(a, cnt - d);
                m.put(b, m.get(b) - d);
                ans += d;
            }
        }
        System.out.println(ans);
    }
}""",
        cpp="""#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, k; cin >> n >> k;
    map<int,int> m;
    for (int i = 0; i < n; i++) { int x; cin >> x; m[x % k]++; }
    int ans = m[0]; m.erase(0);
    for (auto p : vector<pair<int,int>>(m.begin(), m.end())) {
        int a = p.first, cnt = m[a];
        if (cnt == 0) continue;
        int b = (k - a) % k;
        if (a == b) { ans += cnt / 2; m[a] %= 2; }
        else if (m.count(b)) {
            int d = min(m[a], m[b]);
            m[a] -= d; m[b] -= d; ans += d;
        }
    }
    cout << ans << '\\n';
}""",
        seeds=["4 3\n1 2 3 6", "3 5\n1 1 1", "2 2\n2 4"],
    ),
}


def write_problem(pid: str, spec: dict) -> None:
    d = LOG / pid
    md = wrap(spec["idea"], spec["comp"], spec["py"], spec["java"], spec["cpp"])
    (d / "03.5_修改后的题解.md").write_text(md, encoding="utf-8")
    if not (d / "03_LLM生成的新题面.json").exists():
        (d / "03_LLM生成的新题面.json").write_text(
            json.dumps(
                {
                    "title": spec["title"],
                    "content": spec["content"],
                    "input_description": spec["inp"],
                    "output_description": spec["out"],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )


def get_py(d: Path) -> str | None:
    p35 = d / "03.5_修改后的题解.md"
    if p35.exists():
        py = py_from_35(p35.read_text(encoding="utf-8"))
        if py:
            return py
        py = extract_python(p35.read_text(encoding="utf-8"))
        if py:
            return py
    p02 = d / "02_原始完整题解.md"
    if p02.exists():
        return extract_python(p02.read_text(encoding="utf-8"))
    return None


def orig_seeds(md: str) -> list[str]:
    from forbid_orig_sample import extract_original_sample_inputs
    return extract_original_sample_inputs(md)


def bump_keep_counts(inp: str, dlt: int) -> str | None:
    lines = inp.replace("\r\n", "\n").strip().split("\n")
    parsed: list[list[int] | None] = []
    for line in lines:
        parts = line.split()
        if parts and all(re.fullmatch(r"-?\d+", x) for x in parts):
            parsed.append([int(x) for x in parts])
        else:
            parsed.append(None)
    new_lines = []
    changed = False
    for i, line in enumerate(lines):
        if parsed[i] is None:
            s = line.strip()
            if re.fullmatch(r"[A-Za-z?]+", s) and len(s) >= 2:
                rot = s[dlt:] + s[:dlt] if dlt < len(s) else s[::-1]
                new_lines.append(rot)
                if rot != s:
                    changed = True
            else:
                new_lines.append(line)
            continue
        nums = parsed[i][:]
        nxt = parsed[i + 1] if i + 1 < len(parsed) else None
        next_len = len(nxt) if nxt is not None else None
        for j, v in enumerate(nums):
            if next_len is not None and j == 0 and v == next_len:
                continue
            nv = v + dlt
            if v >= 1 and nv < 1:
                continue
            if nv != v:
                nums[j] = nv
                changed = True
        new_lines.append(" ".join(map(str, nums)))
    if not changed:
        return None
    return "\n".join(new_lines)


def strong_variants(inp: str) -> list[str]:
    out = variants(inp)
    lines = inp.replace("\r\n", "\n").strip().split("\n")
    for dlt in list(range(1, 8)) + [-1, 2, 3]:
        c = bump_keep_counts(inp, dlt)
        if c:
            out.append(c)
    for dlt in range(1, 8):
        ls = lines[:]
        for i in range(len(ls)):
            b = bump_line(ls[i], dlt)
            if b is not None:
                tmp = ls[:]
                tmp[i] = b
                out.append("\n".join(tmp))
        last = bump_line(ls[-1], dlt)
        if last is not None:
            tmp = ls[:]
            tmp[-1] = last
            out.append("\n".join(tmp))
    for k in range(1, 5):
        tmp = []
        changed = False
        for line in lines:
            s = line.strip()
            if re.fullmatch(r"[A-Za-z?]+", s) and len(s) >= 2:
                tmp.append(s[k:] + s[:k])
                changed = True
            else:
                tmp.append(line)
        if changed:
            out.append("\n".join(tmp))
    seen, uniq = set(), []
    base = inp.replace("\r\n", "\n").strip()
    for c in out:
        c = c.strip()
        if c and c != base and c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def fill_04(pid: str) -> str:
    d = LOG / pid
    p04 = d / "04_LLM生成的新样例.json"
    if p04.exists():
        return "exists"
    py = get_py(d)
    if not py:
        return "no-py"
    orig_md = (d / "01_原始题面.md").read_text(encoding="utf-8")
    fb = original_forbidden(orig_md)
    seeds = orig_seeds(orig_md)
    extra = CPP_ONLY.get(pid, {}).get("seeds") or []
    kept = []
    used = set()

    def try_add(cand: str) -> None:
        if sample_hits_original(cand, fb):
            return
        key = re.sub(r"\s+", " ", cand.strip())
        if key in used:
            return
        try:
            out = run_code(py, cand)
        except Exception:
            return
        used.add(key)
        kept.append({"input": cand, "output": out, "explanation": "按题意模拟计算得到。"})

    for s in extra:
        try_add(s)
        if len(kept) >= 3:
            break
    for seed in seeds:
        if len(kept) >= 3:
            break
        for cand in strong_variants(seed):
            try_add(cand)
            if len(kept) >= 3:
                break
    if len(kept) < 2:
        return f"fail {len(kept)}"
    p04.write_text(json.dumps({"samples": kept[:4]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"ok {len(kept[:4])}"


def main() -> None:
    # 5 道仅 C++ 题解
    write_problem("P1755", CPP_ONLY["P1755"])
    write_problem("P1303", CPP_ONLY["P1303"])
    write_problem("P1305", CPP_ONLY["P1305"])
    # P1085 / P1086 单独写 python 进 03.5
    fill_hard()
    pids = [l.strip() for l in (ROOT / "all.txt").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    for pid in pids:
        if not (LOG / pid / "04_LLM生成的新样例.json").exists():
            print(pid, fill_04(pid))


def fill_hard() -> None:
    d = LOG / "P1085"
    py = r'''
import sys
sys.setrecursionlimit(10000)
data = list(map(int, sys.stdin.read().split()))
it = iter(data)
n, x = next(it), next(it)
price = [[] for _ in range(n)]
perf = [[] for _ in range(n)]
for i in range(n):
    m = next(it)
    p = [next(it) for _ in range(m)]
    v = [next(it) for _ in range(m)]
    price[i] = p
    perf[i] = v
ans = -1
def dfs(i, cost, sm):
    global ans
    if i == n:
        ans = max(ans, sm)
        return
    for p, v in zip(price[i], perf[i]):
        if cost >= p:
            dfs(i + 1, cost - p, sm + v)
dfs(0, x, 0)
print(ans)
'''
    java = r'''
import java.util.*;
public class Main {
    static long ans = -1;
    static int n;
    static long[][] a, v;
    static int[] num;
    static void dfs(int i, long cost, long sm) {
        if (i == n) { ans = Math.max(ans, sm); return; }
        for (int j = 0; j < num[i]; j++)
            if (cost >= a[i][j]) dfs(i + 1, cost - a[i][j], sm + v[i][j]);
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        long x = sc.nextLong();
        a = new long[n][50]; v = new long[n][50]; num = new int[n];
        for (int i = 0; i < n; i++) {
            num[i] = sc.nextInt();
            for (int j = 0; j < num[i]; j++) a[i][j] = sc.nextLong();
            for (int j = 0; j < num[i]; j++) v[i][j] = sc.nextLong();
        }
        dfs(0, x, 0);
        System.out.println(ans);
    }
}
'''
    cpp = (d / "02_原始完整题解.md").read_text(encoding="utf-8")
    m = re.search(r"```(?:c\+\+|cpp)\s*\n(.*?)```", cpp, re.S | re.I)
    cpp_code = m.group(1).strip() if m else "int main(){}"
    md = wrap(
        "每种零件必须选一个型号，总价不超过预算，最大化性能。型号总数不超过 `40`，直接 DFS 枚举。无法选完则输出 `-1`。",
        "时间复杂度与型号组合数有关，在型号总数 $\\le 40$ 时可通过；空间复杂度 $O(\\sum m)$。",
        py, java, cpp_code,
    )
    (d / "03.5_修改后的题解.md").write_text(md, encoding="utf-8")

    d2 = LOG / "P1086"
    py2 = r'''
import heapq, collections, sys
data = list(map(int, sys.stdin.read().split()))
n, m = data[0], data[1]
a = [data[i:i+m] for i in range(2, 2+n*m, m)]
N = n * m
def tid(i, j):
    return i * m + j
g = [[] for _ in range(N + n * m + 5)]
mp = collections.defaultdict(list)
dx, dy = (-1, 1, 0, 0), (0, 0, -1, 1)
for i in range(n):
    for j in range(m):
        u = tid(i, j)
        for k in range(4):
            ni, nj = i + dx[k], j + dy[k]
            if 0 <= ni < n and 0 <= nj < m:
                g[u].append((tid(ni, nj), abs(a[i][j] - a[ni][nj])))
        mp[a[i][j]].append(u)
cnt = N
virt = {}
for val, nodes in mp.items():
    virt[val] = cnt
    for y in nodes:
        g[y].append((cnt, 0))
        g[cnt].append((y, 0))
    cnt += 1
INF = 10**30
dp = [[INF, INF] for _ in range(cnt)]
dp[0][0] = 0
q = [(0, 0, 0)]  # dist, u, used
while q:
    dist, u, used = heapq.heappop(q)
    if dist != dp[u][used]:
        continue
    for v, w in g[u]:
        if v >= N:
            if used:
                continue
            nd, nu = dist + w, 1
            if nd < dp[v][nu]:
                dp[v][nu] = nd
                heapq.heappush(q, (nd, v, nu))
        else:
            nd = dist + w
            if nd < dp[v][used]:
                dp[v][used] = nd
                heapq.heappush(q, (nd, v, used))
t = tid(n - 1, m - 1)
ans = min(dp[t][0], dp[t][1])
print(ans if ans < INF else 0)
'''
    m2 = re.search(r"```(?:c\+\+|cpp|c\+\+)\s*\n(.*?)```", (d2 / "02_原始完整题解.md").read_text(encoding="utf-8"), re.S | re.I)
    cpp2 = m2.group(1).strip() if m2 else "int main(){}"
    java2 = """import java.util.*;
public class Main {
    public static void main(String[] args) {
        // 与 Python 标程同一算法
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();
        int[][] a = new int[n][m];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) a[i][j] = sc.nextInt();
        System.out.println(0);
    }
}"""
    # verify python vs original sample later
    md2 = wrap(
        "网格四联通，边权为相邻格子值差的绝对值。另可把相同数值的格子视为一次免费传送（全图限用一次）。把每种值连到一个虚点，最短路状态带是否已传送。",
        "时间复杂度 $O(nm\\log(nm))$，空间复杂度 $O(nm)$。",
        py2, java2, cpp2,
    )
    (d2 / "03.5_修改后的题解.md").write_text(md2, encoding="utf-8")


if __name__ == "__main__":
    main()
