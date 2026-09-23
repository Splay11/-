# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(r"d:\机考出题\problem-maker\Problems")
COMPILE = Path(r"d:\机考出题\problem-maker\compile.sh")


def put(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt1(a: List[int]) -> str:
    return "[" + ", ".join(map(str, a)) + "]" if len(a) <= 40 else json.dumps(a, separators=(",", ":"))


def fmt2(a: List[List[int]]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join("[" + ", ".join(map(str, r)) + "]" for r in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def config() -> str:
    cases = "\n".join(f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11))
    return (
        "type: default\n"
        "user_extra_files:\n"
        "  - template.py\n  - template.java\n  - template.cc\n  - template.c\n"
        "  - compile.sh\n  - config.yaml\n"
        "  - user.cc\n  - user.java\n  - user.py\n  - user.c\n"
        "subtasks:\n  - score: 100\n    if: []\n    id: 1\n    type: sum\n    cases:\n"
        f"{cases}\n"
        "langs:\n  - py.py3\n  - java\n  - cc.cc14o2\n  - py\n  - cc\n  - c\n"
    )


JAVA_1D = r"""
    private static String trim(String s) { return s == null ? "" : s.trim(); }
    private static int readInt(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        int sign = 1;
        if (idx[0] < s.length() && s.charAt(idx[0]) == '-') { sign = -1; idx[0]++; }
        int v = 0; boolean ok = false;
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
            row.add(readInt(line, idx));
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
static bool parseInt(const string& s, size_t& i, int& out) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    int sign = 1; if (i < s.size() && s[i] == '-') { sign = -1; i++; }
    if (i >= s.size() || !isdigit((unsigned char)s[i])) return false;
    long long v = 0; while (i < s.size() && isdigit((unsigned char)s[i])) { v = v * 10 + (s[i] - '0'); i++; }
    out = (int)(sign * v); return true;
}
static vector<int> parseArray1d(const string& line) {
    string s = trim(line); size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1); i++;
    vector<int> row;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        int v; if (!parseInt(s, i, v)) exit(1); row.push_back(v);
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


def gen_7012() -> None:
    d, data = ROOT / "P7012", ROOT / "P7012" / "data"
    put(d / "std.py", "from typing import List\n\nclass Solution:\n    def countHighRisk(self, levels: List[int], threshold: int) -> int:\n        return sum(1 for x in levels if x >= threshold)\n")
    put(data / "user.py", "from typing import List\n\nclass Solution:\n    def countHighRisk(self, levels: List[int], threshold: int) -> int:\n        return 0\n")
    put(data / "user.java", "public class Solution {\n    public int countHighRisk(int[] levels, int threshold) { return 0; }\n}\n")
    put(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\n public:\n  int countHighRisk(vector<int>& levels, int threshold) { (void)levels; (void)threshold; return 0; }\n};\n")
    put(data / "user.c", "int countHighRisk(int* levels, int levelsSize, int threshold) {\n    (void)levels; (void)levelsSize; (void)threshold; return 0;\n}\n")
    put(data / "template.py", 'import json, sys\nlines=[ln for ln in sys.stdin.read().split("\\n") if ln.strip()!=""]\nif len(lines)<2: raise SystemExit(0)\nprint(Solution().countHighRisk(json.loads(lines[0]), int(lines[1].strip())))\n')
    put(data / "template.java", "import java.io.*;\nimport java.util.*;\npublic class Main {" + JAVA_1D + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().countHighRisk(parseArray1d(l1), Integer.parseInt(trim(l2))));
    }
}
""")
    put(data / "template.cc", '#include "foo.cc"\n#include <cctype>\n#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n' + CC_1D + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto levels = parseArray1d(l1); Solution sol;
    cout << sol.countHighRisk(levels, stoi(trim(l2))) << '\\n';
}
""")
    put(data / "template.c", '#include "foo.c"\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n' + C_1D + """
int countHighRisk(int* levels, int levelsSize, int threshold);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(64);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, 64, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n=0; int* a=parseIntList(l1, &n);
    printf("%d\\n", countHighRisk(a, n, atoi(l2)));
    free(a); free(l1); free(l2); return 0;
}
""")
    rng = random.Random(7012)

    def sol(levels, th):
        return sum(1 for x in levels if x >= th)

    cases = [
        ([1, 5, 3, 5, 2], 4),
        ([1, 2, 3], 10),
        ([7], 7),
        ([], 1),
        ([1, 1, 1], 1),
        ([9, 8, 7, 6], 8),
        ([rng.randint(1, 100) for _ in range(50)], 50),
        ([1] * 100 + [100] * 5, 100),
        ([rng.randint(1, 10**6) for _ in range(20000)], 5 * 10**5),
        ([rng.randint(1, 10**9) for _ in range(100000)], 10**9),
    ]
    assert sol(*cases[0]) == 2
    for i, (levels, th) in enumerate(cases, 1):
        (data / f"{i}.in").write_bytes((fmt1(levels) + "\n" + str(th)).encode())
        (data / f"{i}.out").write_text(str(sol(levels, th)) + "\n", encoding="utf-8")
    put(data / "README.md", "stdin: levels, threshold\n")
    seal(data)
    print("P7012 ok")


def gen_7013() -> None:
    d, data = ROOT / "P7013", ROOT / "P7013" / "data"
    put(d / "std.py", "from typing import List\n\nclass Solution:\n    def countBlockedPorts(self, openPorts: List[int], blocked: List[int]) -> int:\n        bad=set(blocked)\n        return sum(1 for p in openPorts if p in bad)\n")
    put(data / "user.py", "from typing import List\n\nclass Solution:\n    def countBlockedPorts(self, openPorts: List[int], blocked: List[int]) -> int:\n        return 0\n")
    put(data / "user.java", "public class Solution {\n    public int countBlockedPorts(int[] openPorts, int[] blocked) { return 0; }\n}\n")
    put(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\n public:\n  int countBlockedPorts(vector<int>& openPorts, vector<int>& blocked) { (void)openPorts; (void)blocked; return 0; }\n};\n")
    put(data / "user.c", "int countBlockedPorts(int* openPorts, int openPortsSize, int* blocked, int blockedSize) {\n    (void)openPorts; (void)openPortsSize; (void)blocked; (void)blockedSize; return 0;\n}\n")
    put(data / "template.py", 'import json, sys\nlines=[ln for ln in sys.stdin.read().split("\\n") if ln.strip()!=""]\nif len(lines)<2: raise SystemExit(0)\nprint(Solution().countBlockedPorts(json.loads(lines[0]), json.loads(lines[1])))\n')
    put(data / "template.java", "import java.io.*;\nimport java.util.*;\npublic class Main {" + JAVA_1D + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().countBlockedPorts(parseArray1d(l1), parseArray1d(l2)));
    }
}
""")
    put(data / "template.cc", '#include "foo.cc"\n#include <cctype>\n#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n' + CC_1D + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto a = parseArray1d(l1); auto b = parseArray1d(l2); Solution sol;
    cout << sol.countBlockedPorts(a, b) << '\\n';
}
""")
    put(data / "template.c", '#include "foo.c"\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n' + C_1D + """
int countBlockedPorts(int* openPorts, int openPortsSize, int* blocked, int blockedSize);
int main() {
    char* l1=(char*)malloc(MAX_LEN); char* l2=(char*)malloc(MAX_LEN);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, MAX_LEN, stdin)) return 0;
    trim_nl(l1); trim_nl(l2); int n1=0,n2=0;
    int* a=parseIntList(l1,&n1); int* b=parseIntList(l2,&n2);
    printf("%d\\n", countBlockedPorts(a,n1,b,n2));
    free(a); free(b); free(l1); free(l2); return 0;
}
""")
    rng = random.Random(7013)

    def sol(op, bl):
        bad = set(bl)
        return sum(1 for p in op if p in bad)

    cases = [
        ([22, 80, 443, 22], [22, 3389]),
        ([80, 443], [22, 3389]),
        ([], [22]),
        ([22], []),
        ([1, 2, 3, 4, 5], [1, 3, 5]),
        ([22] * 10, [22]),
        ([rng.randint(1, 100) for _ in range(80)], sorted(set(rng.randint(1, 100) for _ in range(20)))),
        (list(range(1, 51)), list(range(25, 76))),
        ([rng.randint(1, 65535) for _ in range(30000)], sorted(set(rng.randint(1, 65535) for _ in range(5000)))),
        ([rng.randint(1, 65535) for _ in range(100000)], sorted(set(rng.randint(1, 65535) for _ in range(20000)))),
    ]
    assert sol(*cases[0]) == 2
    for i, (op, bl) in enumerate(cases, 1):
        (data / f"{i}.in").write_bytes((fmt1(op) + "\n" + fmt1(bl)).encode())
        (data / f"{i}.out").write_text(str(sol(op, bl)) + "\n", encoding="utf-8")
    put(data / "README.md", "stdin: openPorts, blocked\n")
    seal(data)
    print("P7013 ok")


def gen_7014() -> None:
    d, data = ROOT / "P7014", ROOT / "P7014" / "data"
    put(d / "std.py", "from typing import List\n\nclass Solution:\n    def bestRelay(self, relays: List[List[int]], budget: int) -> int:\n        best_id, best_lat = -1, None\n        for rid, lat, price in relays:\n            if price > budget: continue\n            if best_id < 0 or lat < best_lat or (lat == best_lat and rid < best_id):\n                best_id, best_lat = rid, lat\n        return best_id\n")
    put(data / "user.py", "from typing import List\n\nclass Solution:\n    def bestRelay(self, relays: List[List[int]], budget: int) -> int:\n        return -1\n")
    put(data / "user.java", "public class Solution {\n    public int bestRelay(int[][] relays, int budget) { return -1; }\n}\n")
    put(data / "user.cc", "#include <vector>\nusing namespace std;\nclass Solution {\n public:\n  int bestRelay(vector<vector<int>>& relays, int budget) { (void)relays; (void)budget; return -1; }\n};\n")
    put(data / "user.c", "int bestRelay(int** relays, int relaysSize, int* relaysColSize, int budget) {\n    (void)relays; (void)relaysSize; (void)relaysColSize; (void)budget; return -1;\n}\n")
    put(data / "template.py", 'import json, sys\nlines=[ln for ln in sys.stdin.read().split("\\n") if ln.strip()!=""]\nif len(lines)<2: raise SystemExit(0)\nprint(Solution().bestRelay(json.loads(lines[0]), int(lines[1].strip())))\n')
    java_2d = JAVA_1D + r"""
    private static int[][] parseArray2d(String line) {
        line = trim(line); int[] idx = {0};
        if (idx[0] >= line.length() || line.charAt(idx[0]) != '[') throw new RuntimeException("bad");
        idx[0]++; java.util.ArrayList<int[]> rows = new java.util.ArrayList<>();
        while (true) {
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != '[') throw new RuntimeException("bad row");
            java.util.ArrayList<Integer> row = new java.util.ArrayList<>();
            while (true) {
                while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
                if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
                row.add(readInt(line, idx));
                while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
                if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
                if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
            }
            int[] arr = new int[row.size()];
            for (int i = 0; i < row.size(); i++) arr[i] = row.get(i);
            rows.add(arr);
            while (idx[0] < line.length() && Character.isWhitespace(line.charAt(idx[0]))) idx[0]++;
            if (idx[0] < line.length() && line.charAt(idx[0]) == ']') { idx[0]++; break; }
            if (line.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        return rows.toArray(new int[0][]);
    }
"""
    put(data / "template.java", "import java.io.*;\nimport java.util.*;\npublic class Main {" + java_2d + """
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String l1 = br.readLine(), l2 = br.readLine();
        if (l1 == null || l2 == null) return;
        System.out.println(new Solution().bestRelay(parseArray2d(l1), Integer.parseInt(trim(l2))));
    }
}
""")
    cc_2d = CC_1D + r"""
static vector<vector<int>> parseArray2d(const string& line) {
    string s = trim(line); size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1); i++;
    vector<vector<int>> rows;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        if (i >= s.size() || s[i] != '[') exit(1); i++;
        vector<int> row;
        while (true) {
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            if (i < s.size() && s[i] == ']') { i++; break; }
            int v; if (!parseInt(s, i, v)) exit(1); row.push_back(v);
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            if (i < s.size() && s[i] == ']') { i++; break; }
            if (i >= s.size() || s[i] != ',') exit(1); i++;
        }
        rows.push_back(move(row));
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        if (i >= s.size() || s[i] != ',') exit(1); i++;
    }
    return rows;
}
"""
    put(data / "template.cc", '#include "foo.cc"\n#include <cctype>\n#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\n' + cc_2d + """
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto relays = parseArray2d(l1); Solution sol;
    cout << sol.bestRelay(relays, stoi(trim(l2))) << '\\n';
}
""")
    put(data / "template.c", r"""#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LEN 2000000
#define MAX_ROWS 200000
static void trim_nl(char* s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == '\n' || s[len - 1] == '\r')) s[--len] = '\0';
}
static int** parseInt2D(const char* s, int* outRows, int** outColSizes) {
    int** rows = (int**)malloc(MAX_ROWS * sizeof(int*));
    int* colSizes = (int*)malloc(MAX_ROWS * sizeof(int));
    *outRows = 0; int i = 0;
    while (s[i] && s[i] != '[') i++;
    if (!s[i]) { *outColSizes = colSizes; return rows; }
    i++;
    while (s[i]) {
        while (s[i] == ' ' || s[i] == ',') i++;
        if (s[i] == ']' || !s[i]) break;
        if (s[i] != '[') { i++; continue; }
        i++;
        int* row = (int*)malloc(8 * sizeof(int)); int cnt = 0, cap = 8;
        while (s[i]) {
            while (s[i] == ' ' || s[i] == ',') i++;
            if (s[i] == ']' || !s[i]) { if (s[i] == ']') i++; break; }
            int sign = 1; if (s[i] == '-') { sign = -1; i++; }
            long long v = 0; int have = 0;
            while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); have = 1; i++; }
            if (have) {
                if (cnt >= cap) { cap *= 2; row = (int*)realloc(row, cap * sizeof(int)); }
                row[cnt++] = (int)(sign * v);
            } else i++;
        }
        rows[*outRows] = row; colSizes[*outRows] = cnt; (*outRows)++;
    }
    *outColSizes = colSizes; return rows;
}
int bestRelay(int** relays, int relaysSize, int* relaysColSize, int budget);
int main() {
    char* l1 = (char*)malloc(MAX_LEN); char* l2 = (char*)malloc(64);
    if (!fgets(l1, MAX_LEN, stdin) || !fgets(l2, 64, stdin)) return 0;
    trim_nl(l1); trim_nl(l2);
    int rows = 0; int* col = NULL; int** relays = parseInt2D(l1, &rows, &col);
    printf("%d\n", bestRelay(relays, rows, col, atoi(l2)));
    for (int i = 0; i < rows; i++) free(relays[i]);
    free(relays); free(col); free(l1); free(l2); return 0;
}
""")
    rng = random.Random(7014)

    def sol(relays, budget):
        best_id, best_lat = -1, None
        for rid, lat, price in relays:
            if price > budget:
                continue
            if best_id < 0 or lat < best_lat or (lat == best_lat and rid < best_id):
                best_id, best_lat = rid, lat
        return best_id

    def rand_relays(n):
        ids = list(range(1, n + 1))
        rng.shuffle(ids)
        return [[rid, rng.randint(1, 1000), rng.randint(1, 1000)] for rid in ids]

    cases = [
        ([[3, 10, 50], [1, 20, 30], [2, 10, 40]], 45),
        ([[5, 8, 100], [6, 9, 20]], 50),
        ([[1, 5, 10], [2, 5, 8]], 10),
        ([], 10),
        ([[1, 1, 1]], 0),
        ([[9, 100, 5], [8, 50, 5], [7, 50, 6]], 5),
        (rand_relays(30), 200),
        ([[1, 1, 10**9], [2, 2, 1]], 1),
        (rand_relays(2000), 500),
        (rand_relays(10000), 800),
    ]
    assert sol(*cases[0]) == 2 and sol(*cases[1]) == 6 and sol(*cases[2]) == 1
    for i, (relays, budget) in enumerate(cases, 1):
        (data / f"{i}.in").write_bytes((fmt2(relays) + "\n" + str(budget)).encode())
        (data / f"{i}.out").write_text(str(sol(relays, budget)) + "\n", encoding="utf-8")
    put(data / "README.md", "stdin: relays, budget\n")
    seal(data)
    print("P7014 ok")


def verify() -> None:
    import importlib.util

    mapping = [
        ("P7012", lambda m, lines: m.Solution().countHighRisk(json.loads(lines[0]), int(lines[1]))),
        ("P7013", lambda m, lines: m.Solution().countBlockedPorts(json.loads(lines[0]), json.loads(lines[1]))),
        ("P7014", lambda m, lines: m.Solution().bestRelay(json.loads(lines[0]), int(lines[1]))),
    ]
    for pid, fn in mapping:
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
    gen_7012()
    gen_7013()
    gen_7014()
    verify()
