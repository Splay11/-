#include "testlib.h"
#include <map>
#include <vector>
using namespace std;

int main(int argc, char* argv[]) {
    setName("pair even product");
    registerTestlibCmd(argc, argv);
    int m = inf.readInt();
    int d = inf.readInt();
    vector<int> v(m);
    int same = 0;
    for (int i = 0; i < m; i++) {
        v[i] = inf.readInt();
        if (v[i] % 2 == d % 2) {
            same++;
        }
    }
    int opt = same;
    if (opt > m / 2) {
        opt = m / 2;
    }
    int p = ouf.readInt();
    if (p != opt) {
        quitf(_wa, "box count %d, expected %d", p, opt);
    }
    map<int, int> cnt;
    for (int i = 0; i < m; i++) {
        cnt[v[i]]++;
    }
    for (int i = 0; i < p; i++) {
        int x = ouf.readInt();
        int y = ouf.readInt();
        if (((x + d) % 2 != 0) && ((y + d) % 2 != 0)) {
            quitf(_wa, "invalid pair %d %d", x, y);
        }
        if (--cnt[x] < 0) {
            quitf(_wa, "value %d used too many times", x);
        }
        if (--cnt[y] < 0) {
            quitf(_wa, "value %d used too many times", y);
        }
    }
    ouf.skipBlanks();
    if (!ouf.eof()) {
        quitf(_wa, "extra output");
    }
    quitf(_ok, "ok");
}
