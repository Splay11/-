# 题解思路

**关键观察**
如果某个敌方（`'x'`）连通块的“气”（上下左右相邻的空位 `'.'`）**只有 1 个**，那么把我方子（`'o'`）下在这唯一气上，立刻吃掉该连通块全部棋子。
因此问题化简为：

1. 扫描棋盘，按 4 联通把所有敌方连通块分组（BFS/DFS）。
2. 对每个敌方连通块统计：

   * 该块**大小**（棋子数）。
   * 该块**所有气**（相邻的 `'.'` 位置，需去重）。
3. 若某块的气数恰为 1，设唯一气为位置 `p`，则把 `p` 标记为一个“可吃点”，其可吃子数累加该块大小。
   多个敌方块可能共享同一个唯一气 `p`，下在 `p` 会**同时吃掉**这些块（累加大小）。
4. 将所有这样的 `p` 输出：横坐标、纵坐标（均 **1 基**）、以及累计能吃的棋子总数。输出顺序题面未强制，通常按坐标升序输出更稳定。

**去重技巧（高效统计唯一气）**
为避免在每个连通块里为气建局部 `set`（可能开销较大），可维护一个全局整型数组 `mark`，长度为 `n*n`，初值为 `-1`。
处理第 `gid` 个连通块时，遇到一个空位索引 `idx`，若 `mark[idx] != gid` 则说明**本块尚未计过**该气：

* 令 `mark[idx] = gid`，本块气数 `+1`，并记下“最后一个气”的索引（用于判断是否恰为 1）。

## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<string> g(n);
    for (int i = 0; i < n; ++i) cin >> g[i];

    auto idx = [&](int r, int c){ return r * n + c; };
    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};

    vector<char> visX(n * n, 0);      // 敌方'x'是否已分组访问
    vector<int> mark(n * n, -1);      // 记录每个空位上次计入的连通块id
    unordered_map<int,int> capture;   // 空位索引 -> 累计可吃子数
    int gid = 0;                      // 连通块编号（仅用于mark去重）

    for (int r = 0; r < n; ++r) {
        for (int c = 0; c < n; ++c) {
            if (g[r][c] != 'x') continue;
            int id = idx(r, c);
            if (visX[id]) continue;

            // BFS 找到一个敌方连通块
            gid++;
            queue<pair<int,int>> q;
            q.push({r, c});
            visX[id] = 1;
            int size = 0;
            int libCount = 0;
            int lastLib = -1;

            while (!q.empty()) {
                auto [ur, uc] = q.front(); q.pop();
                size++;
                for (int k = 0; k < 4; ++k) {
                    int vr = ur + dr[k], vc = uc + dc[k];
                    if (vr < 0 || vr >= n || vc < 0 || vc >= n) continue;
                    char ch = g[vr][vc];
                    if (ch == 'x') {
                        int nid = idx(vr, vc);
                        if (!visX[nid]) {
                            visX[nid] = 1;
                            q.push({vr, vc});
                        }
                    } else if (ch == '.') {
                        int e = idx(vr, vc);
                        if (mark[e] != gid) { // 本块首次计到这个气
                            mark[e] = gid;
                            libCount++;
                            lastLib = e;
                        }
                    }
                    // 'o' 忽略
                }
            }

            if (libCount == 1) {
                capture[lastLib] += size;
            }
        }
    }

    // 汇总与输出（按坐标升序）
    vector<tuple<int,int,int>> ans;
    ans.reserve(capture.size());
    for (auto &kv : capture) {
        int e = kv.first, cnt = kv.second;
        int r = e / n, c = e % n;
        ans.push_back({r + 1, c + 1, cnt}); // 1-based
    }
    sort(ans.begin(), ans.end());

    cout << ans.size() << "\n";
    for (auto &t : ans) {
        int a,b,cnt; tie(a,b,cnt) = t;
        cout << a << ' ' << b << ' ' << cnt << "\n";
    }
    return 0;
}
```
## Python

```python
from collections import deque
import sys

def main():
    data = sys.stdin.read().strip().splitlines()
    n = int(data[0])
    g = data[1:1+n]

    def idx(r, c): return r * n + c
    dr = (-1, 1, 0, 0)
    dc = (0, 0, -1, 1)

    visX = [False] * (n * n)   # 敌方连通块访问标记
    mark = [-1] * (n * n)      # 空位唯一气去重（按连通块id）
    capture = {}               # 空位索引 -> 累计可吃子数
    gid = 0

    for r in range(n):
        for c in range(n):
            if g[r][c] != 'x':
                continue
            id0 = idx(r, c)
            if visX[id0]:
                continue

            gid += 1
            q = deque()
            q.append((r, c))
            visX[id0] = True
            size = 0
            libCount = 0
            lastLib = -1

            while q:
                ur, uc = q.popleft()
                size += 1
                for k in range(4):
                    vr = ur + dr[k]
                    vc = uc + dc[k]
                    if not (0 <= vr < n and 0 <= vc < n):
                        continue
                    ch = g[vr][vc]
                    if ch == 'x':
                        nid = idx(vr, vc)
                        if not visX[nid]:
                            visX[nid] = True
                            q.append((vr, vc))
                    elif ch == '.':
                        e = idx(vr, vc)
                        if mark[e] != gid:
                            mark[e] = gid
                            libCount += 1
                            lastLib = e
                    # 'o' 忽略

            if libCount == 1:
                capture[lastLib] = capture.get(lastLib, 0) + size

    ans = []
    for e, cnt in capture.items():
        r, c = divmod(e, n)
        ans.append((r + 1, c + 1, cnt))
    ans.sort()

    print(len(ans))
    for a, b, cnt in ans:
        print(a, b, cnt)

if __name__ == "__main__":
    main()
```
## Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    static int n;
    static char[][] g;
    static boolean[] visX;    // 敌方连通块访问
    static int[] mark;        // 空位唯一气去重
    static final int[] dr = {-1, 1, 0, 0};
    static final int[] dc = {0, 0, -1, 1};

    static int idx(int r, int c) { return r * n + c; }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine().trim());
        g = new char[n][];
        for (int i = 0; i < n; i++) {
            g[i] = br.readLine().trim().toCharArray();
        }

        visX = new boolean[n * n];
        mark = new int[n * n];
        Arrays.fill(mark, -1);

        HashMap<Integer, Integer> capture = new HashMap<>();
        int gid = 0;

        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if (g[r][c] != 'x') continue;
                int id0 = idx(r, c);
                if (visX[id0]) continue;

                gid++;
                ArrayDeque<int[]> q = new ArrayDeque<>();
                q.add(new int[]{r, c});
                visX[id0] = true;

                int size = 0;
                int libCount = 0;
                int lastLib = -1;

                while (!q.isEmpty()) {
                    int[] cur = q.poll();
                    int ur = cur[0], uc = cur[1];
                    size++;
                    for (int k = 0; k < 4; k++) {
                        int vr = ur + dr[k], vc = uc + dc[k];
                        if (vr < 0 || vr >= n || vc < 0 || vc >= n) continue;
                        char ch = g[vr][vc];
                        if (ch == 'x') {
                            int nid = idx(vr, vc);
                            if (!visX[nid]) {
                                visX[nid] = true;
                                q.add(new int[]{vr, vc});
                            }
                        } else if (ch == '.') {
                            int e = idx(vr, vc);
                            if (mark[e] != gid) {
                                mark[e] = gid;
                                libCount++;
                                lastLib = e;
                            }
                        }
                        // 'o' 忽略
                    }
                }

                if (libCount == 1) {
                    capture.put(lastLib, capture.getOrDefault(lastLib, 0) + size);
                }
            }
        }

        // 整理输出：按坐标升序
        List<int[]> ans = new ArrayList<>();
        for (Map.Entry<Integer, Integer> kv : capture.entrySet()) {
            int e = kv.getKey(), cnt = kv.getValue();
            int r = e / n, c = e % n;
            ans.add(new int[]{r + 1, c + 1, cnt});
        }
        ans.sort(Comparator.<int[]>comparingInt(a -> a[0]).thenComparingInt(a -> a[1]));

        StringBuilder sb = new StringBuilder();
        sb.append(ans.size()).append('\n');
        for (int[] t : ans) {
            sb.append(t[0]).append(' ').append(t[1]).append(' ').append(t[2]).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```