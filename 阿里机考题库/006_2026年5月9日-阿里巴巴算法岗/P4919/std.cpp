#include <bits/stdc++.h>
using namespace std;

long long countBest(int s, int pL, int pR, int qL, int qR) {
    // 4 个 tight 标记：p/q 前缀是否仍贴上下界
    vector<long long> dp(16, 0);
    dp[15] = 1;
    for (int pos = 30; pos >= 0; --pos) {
        int sb = (s >> pos) & 1;
        int plb = (pL >> pos) & 1, prb = (pR >> pos) & 1;
        int qlb = (qL >> pos) & 1, qrb = (qR >> pos) & 1;
        vector<long long> nz(16, 0), no(16, 0);
        bool hasOne = false;
        for (int st = 0; st < 16; ++st) {
            long long cnt = dp[st];
            if (!cnt) continue;
            int eqPL = st & 1, eqPR = (st >> 1) & 1;
            int eqQL = (st >> 2) & 1, eqQR = (st >> 3) & 1;
            for (int pb = 0; pb <= 1; ++pb) {
                if (eqPL && pb < plb) continue;
                if (eqPR && pb > prb) continue;
                int nPL = eqPL && pb == plb, nPR = eqPR && pb == prb;
                for (int qb = 0; qb <= 1; ++qb) {
                    if (eqQL && qb < qlb) continue;
                    if (eqQR && qb > qrb) continue;
                    int nQL = eqQL && qb == qlb, nQR = eqQR && qb == qrb;
                    int ns = nPL | (nPR << 1) | (nQL << 2) | (nQR << 3);
                    int cur = sb ^ pb ^ qb;
                    if (cur == 1) { no[ns] += cnt; hasOne = true; }
                    else nz[ns] += cnt;
                }
            }
        }
        dp = hasOne ? no : nz;
    }
    long long ans = 0;
    for (long long v : dp) ans += v;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int s, pL, pR, qL, qR;
        cin >> s >> pL >> pR >> qL >> qR;
        cout << countBest(s, pL, pR, qL, qR) << '\n';
    }
    return 0;
}
