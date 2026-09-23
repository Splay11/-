#include "testlib.h"
#include <algorithm>
#include <vector>
using namespace std;

int main(int argc, char *argv[]) {
    registerTestlibCmd(argc, argv);
    int k = inf.readInt(1, 50, "k");
    for (int t = 1; t <= k; t++) {
        int h = inf.readInt(2, 1000, "h");
        int s = inf.readInt(1, h * (h + 1) / 2, "s");
        int n = h * (h + 1) / 2;
        int need = 3 * h * (h - 1) / 2 + 1;

        vector<vector<int> > g(n + 1);
        auto add = [&](int a, int b) {
            g[a].push_back(b);
            g[b].push_back(a);
        };
        for (int r = 2; r <= h; r++) {
            int base = r * (r - 1) / 2;
            int prev = (r - 1) * (r - 2) / 2;
            for (int c = 1; c < r; c++) {
                int u = base + c;
                int v = base + c + 1;
                int w = prev + c;
                add(u, v);
                add(u, w);
                add(v, w);
            }
        }

        vector<int> path(need);
        for (int i = 0; i < need; i++) {
            path[i] = ouf.readInt(1, n, "path");
        }
        if (path[0] != s || path[need - 1] != s) {
            quitf(_wa, "case %d: path must start and end at %d", t, s);
        }

        auto erase_edge = [&](int a, int b) {
            vector<int>::iterator it = find(g[a].begin(), g[a].end(), b);
            if (it == g[a].end()) {
                return false;
            }
            *it = g[a].back();
            g[a].pop_back();
            it = find(g[b].begin(), g[b].end(), a);
            if (it == g[b].end()) {
                return false;
            }
            *it = g[b].back();
            g[b].pop_back();
            return true;
        };

        for (int i = 0; i + 1 < need; i++) {
            if (!erase_edge(path[i], path[i + 1])) {
                quitf(_wa, "case %d: not an unused edge %d-%d", t, path[i], path[i + 1]);
            }
        }
        for (int u = 1; u <= n; u++) {
            if (!g[u].empty()) {
                quitf(_wa, "case %d: unused edges remain at vertex %d", t, u);
            }
        }
    }
    ouf.skipBlanks();
    if (!ouf.seekEof()) {
        quitf(_wa, "extra output");
    }
    quitf(_ok, "eulerian circuits ok");
}
