/**
 * P5419 灯带电平 SPJ
 * 选手可输出任意合法 01 串；用 inf 校验每个偶数窗口 0/1 数量相等。
 * 输入协议（四级）：第一行 k，第二行 q，随后 q 行 a,b。
 */
#include "testlib.h"
#include <cstdlib>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    int k = inf.readInt();
    int q = inf.readInt();

    vector<int> A(q), B(q);
    for (int i = 0; i < q; i++) {
        string tok = inf.readToken();
        size_t p = tok.find(',');
        if (p == string::npos) {
            quitf(_fail, "interval #%d is not a,b: %s", i + 1, tok.c_str());
        }
        A[i] = atoi(tok.substr(0, p).c_str());
        B[i] = atoi(tok.substr(p + 1).c_str());
    }

    string t = ouf.readToken();
    if ((int)t.size() != k) {
        quitf(_wa, "string length %d, expected %d", (int)t.size(), k);
    }
    for (int i = 0; i < k; i++) {
        if (t[i] != '0' && t[i] != '1') {
            quitf(_wa, "t[%d] = '%c', expected 0 or 1", i + 1, t[i]);
        }
    }

    vector<int> pre(k + 1, 0);
    for (int i = 1; i <= k; i++) {
        pre[i] = pre[i - 1] + (t[i - 1] == '1');
    }
    for (int i = 0; i < q; i++) {
        int a = A[i], b = B[i];
        int ones = pre[b] - pre[a - 1];
        int len = b - a + 1;
        if (ones * 2 != len) {
            quitf(_wa, "window [%d,%d] has %d ones, length %d", a, b, ones, len);
        }
    }

    ouf.skipBlanks();
    if (!ouf.seekEof()) {
        quitf(_wa, "extra output");
    }
    quitf(_ok, "ok");
    return 0;
}
