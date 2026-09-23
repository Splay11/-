# -*- coding: utf-8 -*-
"""Rebuild P7012/P7013 packs after CF1200 redesign."""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(r"d:\机考出题\problem-maker\Problems")
COMPILE = Path(r"d:\机考出题\problem-maker\compile.sh")


def put(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def fmt1(a: List[int]) -> str:
    return "[" + ", ".join(map(str, a)) + "]" if len(a) <= 40 else json.dumps(a, separators=(",", ":"))


def config() -> str:
    cases = "\n".join(f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11))
    return (
        "type: default\nuser_extra_files:\n"
        "  - template.py\n  - template.java\n  - template.cc\n  - template.c\n"
        "  - compile.sh\n  - config.yaml\n"
        "  - user.cc\n  - user.java\n  - user.py\n  - user.c\n"
        "subtasks:\n  - score: 100\n    if: []\n    id: 1\n    type: sum\n    cases:\n"
        f"{cases}\nlangs:\n  - py.py3\n  - java\n  - cc.cc14o2\n  - py\n  - cc\n  - c\n"
    )


JAVA_1D = r"""
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
"""

CC_1D = r"""
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
"""

C_1D = r"""
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
"""


def seal(data: Path) -> None:
    put(data / "config.yaml", config())
    shutil.copyfile(COMPILE, data / "compile.sh")


def solve_7012(loads: List[int], limit: int) -> int:
    ans = s = l = 0
    for r, x in enumerate(loads):
        s += x
        while l <= r and s > limit:
            s -= loads[l]
            l += 1
        ans = max(ans, r - l + 1)
    return ans


def solve_7013(events: List[int], need: List[int]) -> int:
    if not need:
        return 0
    need_set = set(need)
    miss = len(need_set)
    from collections import defaultdict

    win = defaultdict(int)
    ans = 10**18
    l = 0
    for r, x in enumerate(events):
        if x in need_set:
            if win[x] == 0:
                miss -= 1
            win[x] += 1
        while miss == 0 and l <= r:
            ans = min(ans, r - l + 1)
            y = events[l]
            if y in need_set:
                win[y] -= 1
                if win[y] == 0:
                    miss += 1
            l += 1
    return -1 if ans == 10**18 else int(ans)


def build_7012() -> None:
    d, data = ROOT / "P7012", ROOT / "P7012" / "data"
    put(
        d / "std.py",
        "from typing import List\n\nclass Solution:\n"
        "    def longestSafeWindow(self, loads: List[int], limit: int) -> int:\n"
        "        ans = s = l = 0\n"
        "        for r, x in enumerate(loads):\n"
        "            s += x\n"
        "            while l <= r and s > limit:\n"
        "                s -= loads[l]\n"
        "                l += 1\n"
        "            ans = max(ans, r - l + 1)\n"
        "        return ans\n",
    )
    put(data / "user.py", "from typing import List\n\nclass Solution:\n    def longestSafeWindow(self, loads: List[int], limit: int) -> int:\n        return 0\n")
    put(data / "user.java", "public class Solution {\n    public int longestSafeWindow(int[] loads, long limit) { return 0; }\n}\n")
    put(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\n public:\n  int longestSafeWindow(vector<int>& loads, long long limit) { (void)loads; (void)limit; return 0; }\n};\n")
    put(data / "user.c", "int longestSafeWindow(int* loads, int loadsSize, long long limit) {\n    (void)loads; (void)loadsSize; (void)limit; return 0;\n}\n")
    put(
        data / "template.py",
        'import json, sys\nlines=[ln for ln in sys.stdin.read().split("\\n") if ln.strip()!=""]\n'
        "if len(lines)<2: raise SystemExit(0)\n"
        "print(Solution().longestSafeWindow(json.loads(lines[0]), int(lines[1].strip())))\n",
    )
    put(
        data / "template.java",
        "import java.io.*;\nimport java.util.*;\npublic class Main {"
        + JAVA_1D
        + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().longestSafeWindow(parseArray1d(l1), Long.parseLong(trim(l2))));
    }
}
""",
    )
    put(
        data / "template.cc",
        '#include "foo.cc"\n#include <cctype>\n#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n'
        + CC_1D
        + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto loads = parseArray1d(l1); Solution sol;
    cout << sol.longestSafeWindow(loads, stoll(trim(l2))) << '\\n';
}
""",
    )
    put(
        data / "template.c",
        '#include "foo.c"\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n'
        + C_1D
        + """
int longestSafeWindow(int* loads, int loadsSize, long long limit);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(64);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, 64, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n=0; int* a=parseIntList(l1,&n);
    printf("%d\\n", longestSafeWindow(a, n, atoll(l2)));
    free(a); free(l1); free(l2); return 0;
}
""",
    )

    rng = random.Random(7012)
    cases: List[Tuple[List[int], int]] = [
        ([2, 1, 3, 2, 1], 5),
        ([1, 1, 1], 2),
        ([10], 5),
        ([], 1),
        ([1, 2, 3, 4], 100),
        ([5, 1, 1, 1, 5], 3),
        ([rng.randint(1, 20) for _ in range(80)], 50),
        ([10**9] * 5 + [1] * 10, 10),
        ([rng.randint(1, 10**6) for _ in range(20000)], 5 * 10**6),
        ([rng.randint(1, 10**9) for _ in range(100000)], 10**14),
    ]
    assert solve_7012(*cases[0]) == 2
    assert solve_7012(*cases[1]) == 2
    assert solve_7012(*cases[2]) == 0
    for i, (loads, lim) in enumerate(cases, 1):
        (data / f"{i}.in").write_bytes((fmt1(loads) + "\n" + str(lim)).encode())
        (data / f"{i}.out").write_text(str(solve_7012(loads, lim)) + "\n", encoding="utf-8")
    put(data / "README.md", "stdin: loads, limit。正解双指针最长和<=limit。\n")
    seal(data)
    print("P7012 rebuilt")


def build_7013() -> None:
    d, data = ROOT / "P7013", ROOT / "P7013" / "data"
    put(
        d / "std.py",
        "from typing import List\nfrom collections import defaultdict\n\n"
        "class Solution:\n"
        "    def minCoverWindow(self, events: List[int], need: List[int]) -> int:\n"
        "        if not need: return 0\n"
        "        need_cnt = {x: 1 for x in need}\n"
        "        miss = len(need)\n"
        "        win = defaultdict(int)\n"
        "        ans = float('inf'); l = 0\n"
        "        for r, x in enumerate(events):\n"
        "            if x in need_cnt:\n"
        "                if win[x] == 0: miss -= 1\n"
        "                win[x] += 1\n"
        "            while miss == 0 and l <= r:\n"
        "                ans = min(ans, r - l + 1)\n"
        "                y = events[l]\n"
        "                if y in need_cnt:\n"
        "                    win[y] -= 1\n"
        "                    if win[y] == 0: miss += 1\n"
        "                l += 1\n"
        "        return -1 if ans == float('inf') else ans\n",
    )
    put(data / "user.py", "from typing import List\n\nclass Solution:\n    def minCoverWindow(self, events: List[int], need: List[int]) -> int:\n        return -1\n")
    put(data / "user.java", "public class Solution {\n    public int minCoverWindow(int[] events, int[] need) { return -1; }\n}\n")
    put(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\n public:\n  int minCoverWindow(vector<int>& events, vector<int>& need) { (void)events; (void)need; return -1; }\n};\n")
    put(data / "user.c", "int minCoverWindow(int* events, int eventsSize, int* need, int needSize) {\n    (void)events; (void)eventsSize; (void)need; (void)needSize; return -1;\n}\n")
    put(
        data / "template.py",
        'import json, sys\nlines=[ln for ln in sys.stdin.read().split("\\n") if ln.strip()!=""]\n'
        "if len(lines)<2: raise SystemExit(0)\n"
        "print(Solution().minCoverWindow(json.loads(lines[0]), json.loads(lines[1])))\n",
    )
    put(
        data / "template.java",
        "import java.io.*;\nimport java.util.*;\npublic class Main {"
        + JAVA_1D
        + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().minCoverWindow(parseArray1d(l1), parseArray1d(l2)));
    }
}
""",
    )
    put(
        data / "template.cc",
        '#include "foo.cc"\n#include <cctype>\n#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n'
        + CC_1D
        + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto events = parseArray1d(l1); auto need = parseArray1d(l2); Solution sol;
    cout << sol.minCoverWindow(events, need) << '\\n';
}
""",
    )
    put(
        data / "template.c",
        '#include "foo.c"\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n'
        + C_1D
        + """
int minCoverWindow(int* events, int eventsSize, int* need, int needSize);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, MAX_LEN, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n1=0,n2=0;
    int* a=parseIntList(l1,&n1); int* b=parseIntList(l2,&n2);
    printf("%d\\n", minCoverWindow(a,n1,b,n2));
    free(a); free(b); free(l1); free(l2); return 0;
}
""",
    )

    rng = random.Random(7013)
    cases: List[Tuple[List[int], List[int]]] = [
        ([1, 2, 1, 3, 2], [1, 3]),
        ([1, 2, 3], [1, 4]),
        ([2, 2, 2], [2]),
        ([], [1]),
        ([1, 2, 3], []),
        ([5, 1, 2, 5, 1, 2, 3, 5], [1, 2, 3]),
        ([rng.randint(1, 10) for _ in range(100)], [1, 5, 9]),
        (list(range(1, 51)) + [1], list(range(1, 21))),
        ([rng.randint(1, 1000) for _ in range(30000)], sorted(set(rng.randint(1, 1000) for _ in range(30)))),
        ([rng.randint(1, 10**6) for _ in range(100000)], sorted(set(rng.randint(1, 10**6) for _ in range(50)))),
    ]
    assert solve_7013(*cases[0]) == 2
    assert solve_7013(*cases[1]) == -1
    assert solve_7013(*cases[2]) == 1
    assert solve_7013(*cases[4]) == 0
    for i, (ev, nd) in enumerate(cases, 1):
        (data / f"{i}.in").write_bytes((fmt1(ev) + "\n" + fmt1(nd)).encode())
        (data / f"{i}.out").write_text(str(solve_7013(ev, nd)) + "\n", encoding="utf-8")
    put(data / "README.md", "stdin: events, need。最短覆盖窗。\n")
    seal(data)
    print("P7013 rebuilt")


def verify() -> None:
    import importlib.util

    for pid, fn in [
        ("P7012", lambda m, lines: m.Solution().longestSafeWindow(json.loads(lines[0]), int(lines[1]))),
        ("P7013", lambda m, lines: m.Solution().minCoverWindow(json.loads(lines[0]), json.loads(lines[1]))),
    ]:
        d = ROOT / pid
        spec = importlib.util.spec_from_file_location(pid, d / "std.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for i in range(1, 11):
            raw = (d / "data" / f"{i}.in").read_text(encoding="utf-8")
            lines = [ln for ln in raw.split("\n") if ln.strip() != ""]
            got = str(fn(mod, lines)) + "\n"
            exp = (d / "data" / f"{i}.out").read_text(encoding="utf-8")
            assert got == exp, (pid, i, got, exp)
            assert not (d / "data" / f"{i}.in").read_bytes().endswith(b"\n")
            assert (d / "data" / f"{i}.out").read_bytes().endswith(b"\n")
        print(pid, "verify ok")


if __name__ == "__main__":
    build_7012()
    build_7013()
    verify()
