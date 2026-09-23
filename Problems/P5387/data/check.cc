#include "testlib.h"
#include <vector>

using namespace std;

int main(int argc, char *argv[]) {
    registerTestlibCmd(argc, argv);

    int m = inf.readInt();
    int t = inf.readInt();
    vector<int> cnt(1000001, 0);
    int ev = 0;
    int od = 0;
    for (int i = 0; i < m; i++) {
        int x = inf.readInt();
        if (x < 1 || x > 1000000) {
            quitf(_fail, "invalid input value");
        }
        cnt[x]++;
        if ((x + t) % 2 == 0) {
            ev++;
        } else {
            od++;
        }
    }
    int opt = (od > ev) ? ev : (m / 2);

    int c = ouf.readInt();
    if (c != opt) {
        quitf(_wa, "pair count %d, expected %d", c, opt);
    }
    if (c < 0 || c > m / 2) {
        quitf(_wa, "invalid pair count");
    }
    for (int i = 0; i < c; i++) {
        int x = ouf.readInt();
        int y = ouf.readInt();
        if (x < 1 || x > 1000000 || y < 1 || y > 1000000) {
            quitf(_wa, "value out of range in pair %d", i + 1);
        }
        long long px = (long long)x + t;
        long long py = (long long)y + t;
        if ((px % 2 != 0) && (py % 2 != 0)) {
            quitf(_wa, "odd product in pair %d", i + 1);
        }
        if (cnt[x] <= 0) {
            quitf(_wa, "value %d used more times than it appears", x);
        }
        cnt[x]--;
        if (cnt[y] <= 0) {
            quitf(_wa, "value %d used more times than it appears", y);
        }
        cnt[y]--;
    }
    ouf.skipBlanks();
    if (!ouf.eof()) {
        quitf(_wa, "extra output");
    }
    quitf(_ok, "ok %d pairs", c);
    return 0;
}
