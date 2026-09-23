#include "testlib.h"
#include <string>
using namespace std;

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    string s = inf.readToken();
    string t = ouf.readToken();
    if ((int)t.size() != (int)s.size()) {
        quitf(_wa, "length mismatch: expected %d, got %d", (int)s.size(), (int)t.size());
    }
    int cntS[256] = {0};
    int cntT[256] = {0};
    for (int i = 0; i < (int)s.size(); i++) {
        cntS[(unsigned char)s[i]]++;
        cntT[(unsigned char)t[i]]++;
    }
    for (int c = 0; c < 256; c++) {
        if (cntS[c] != cntT[c]) {
            quitf(_wa, "character count mismatch");
        }
    }
    int n = (int)t.size();
    int prevFreq = n + 1;
    bool seen[256] = {false};
    int i = 0;
    while (i < n) {
        unsigned char ch = (unsigned char)t[i];
        if (seen[ch]) {
            quitf(_wa, "same character must be consecutive");
        }
        seen[ch] = true;
        int j = i;
        while (j < n && (unsigned char)t[j] == ch) {
            j++;
        }
        int freq = j - i;
        if (freq > prevFreq) {
            quitf(_wa, "frequencies must be non-increasing");
        }
        prevFreq = freq;
        i = j;
    }
    quitf(_ok, "ok");
}
