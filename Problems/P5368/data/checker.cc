#include "testlib.h"
#include <cstdlib>
#include <string>
#include <vector>
using namespace std;

int main(int argc, char* argv[]) {
    setName("max manhattan empty cells");
    registerTestlibCmd(argc, argv);
    int h = inf.readInt();
    int w = inf.readInt();
    vector<string> g(h);
    for (int i = 0; i < h; i++) {
        g[i] = inf.readToken();
    }
    int r1 = ouf.readInt();
    int c1 = ouf.readInt();
    int r2 = ouf.readInt();
    int c2 = ouf.readInt();
    ouf.skipBlanks();
    if (!ouf.eof()) {
        quitf(_wa, "extra output");
    }
    if (r1 < 1 || r1 > h || c1 < 1 || c1 > w || r2 < 1 || r2 > h || c2 < 1 || c2 > w) {
        quitf(_wa, "coord out of range");
    }
    if (r1 == r2 && c1 == c2) {
        quitf(_wa, "same cell");
    }
    if (g[r1 - 1][c1 - 1] != '.' || g[r2 - 1][c2 - 1] != '.') {
        quitf(_wa, "not an aisle");
    }
    const int INF = 1000000000;
    int min_s = INF, max_s = -INF;
    int min_d = INF, max_d = -INF;
    for (int i = 0; i < h; i++) {
        for (int j = 0; j < w; j++) {
            if (g[i][j] != '.') {
                continue;
            }
            int r = i + 1;
            int c = j + 1;
            int s = r + c;
            int d = r - c;
            if (s < min_s) {
                min_s = s;
            }
            if (s > max_s) {
                max_s = s;
            }
            if (d < min_d) {
                min_d = d;
            }
            if (d > max_d) {
                max_d = d;
            }
        }
    }
    int best = max_s - min_s;
    if (max_d - min_d > best) {
        best = max_d - min_d;
    }
    int got = abs(r1 - r2) + abs(c1 - c2);
    if (got != best) {
        quitf(_wa, "dist %d, expected %d", got, best);
    }
    quitf(_ok, "ok");
}
