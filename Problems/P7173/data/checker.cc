#include "testlib.h"
#include <map>
#include <vector>
using namespace std;

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    setName("two single numbers any order");

    int n = inf.readInt();
    map<int, int> cnt;
    for (int i = 0; i < n; i++) {
        cnt[inf.readInt()]++;
    }
    vector<int> uniq;
    for (map<int, int>::iterator it = cnt.begin(); it != cnt.end(); ++it) {
        if (it->second == 1) {
            uniq.push_back(it->first);
        }
    }
    if ((int)uniq.size() != 2) {
        quitf(_fail, "testdata must contain exactly two unique numbers");
    }

    int x = ouf.readInt();
    int y = ouf.readInt();
    if ((x == uniq[0] && y == uniq[1]) || (x == uniq[1] && y == uniq[0])) {
        quitf(_ok, "ok");
    }
    quitf(_wa, "expected %d %d (any order), found %d %d", uniq[0], uniq[1], x, y);
}
