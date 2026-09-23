#include <bitset>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int CAP = 10000;
const int NEED = 4;
const int MAXN = 2005;

// suffix[i][k]：从下标 i 到末尾恰好选 k 件能凑出的总价（位集）
static bitset<CAP + 1> suffix[MAXN][NEED + 1];

vector<int> pickFour(vector<int> b, vector<int> w) {
    int n = (int)b.size();
    if (n < NEED) {
        return {};
    }
    vector<int> order(n);
    for (int i = 0; i < n; i++) {
        order[i] = i;
    }
    // 按下标对应的编号从小到大处理，保证贪心得到字典序最小
    sort(order.begin(), order.end(), [&](int i, int j) {
        return b[i] < b[j];
    });
    vector<int> bb(n), ww(n);
    for (int i = 0; i < n; i++) {
        bb[i] = b[order[i]];
        ww[i] = w[order[i]];
    }

    for (int k = 0; k <= NEED; k++) {
        suffix[n][k].reset();
    }
    suffix[n][0].set(0);
    for (int i = n - 1; i >= 0; i--) {
        for (int k = 0; k <= NEED; k++) {
            suffix[i][k] = suffix[i + 1][k];
        }
        for (int k = NEED - 1; k >= 0; k--) {
            // dp[i][k][s]：从 i 往后恰好选 k 件，总价能否为 s
            // 先拷贝 suffix[i+1]，对应不选第 i 件
            // 再或上左移 w[i] 位，对应选第 i 件后总价整体加上售价
            // k 从大到小，保证每件最多用一次
            suffix[i][k + 1] |= (suffix[i + 1][k] << ww[i]);
        }
    }
    if (suffix[0][NEED].none()) {
        return {};
    }
    int remainS = CAP;
    while (remainS >= 0 && !suffix[0][NEED].test(remainS)) {
        remainS--;
    }
    int remainK = NEED;
    vector<int> ans;
    for (int i = 0; i < n && remainK > 0; i++) {
        int ns = remainS - ww[i];
        int nk = remainK - 1;
        // 判断 dp[i+1][nk][ns] 是否可行：选完当前件后后缀还能不能凑齐
        // 编号已升序，能选就选，得到字典序最小方案
        if (ns >= 0 && suffix[i + 1][nk].test(ns)) {
            ans.push_back(bb[i]);
            remainS = ns;
            remainK = nk;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    vector<int> b(m), w(m);
    for (int i = 0; i < m; i++) {
        cin >> b[i] >> w[i];
    }
    vector<int> ans = pickFour(b, w);
    if (ans.empty()) {
        cout << 0 << '\n';
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (i) {
                cout << ' ';
            }
            cout << ans[i];
        }
        cout << '\n';
    }
    return 0;
}
