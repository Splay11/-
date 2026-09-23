#include <string>
#include <vector>
using namespace std;

class Solution {
    static const unsigned long long P = 131;
    static const unsigned long long Q = 13331;

    vector<vector<unsigned long long>> build(vector<vector<string>>& g) {
        int m = (int)g.size(), n = (int)g[0].size();
        vector<vector<unsigned long long>> h(m + 1, vector<unsigned long long>(n + 1, 0));
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                unsigned long long v = (unsigned char)g[i][j][0] - 64;
                h[i + 1][j + 1] = h[i][j + 1] * P + h[i + 1][j] * Q - h[i][j] * P * Q + v;
            }
        }
        return h;
    }

    vector<unsigned long long> powull(int k, unsigned long long base) {
        vector<unsigned long long> a(k + 1, 1);
        for (int i = 1; i <= k; i++) a[i] = a[i - 1] * base;
        return a;
    }

    unsigned long long rect(const vector<vector<unsigned long long>>& h, int r, int c, int a, int b,
                             const vector<unsigned long long>& pP, const vector<unsigned long long>& pQ) {
        unsigned long long v = h[r + a][c + b];
        v -= h[r][c + b] * pP[a];
        v -= h[r + a][c] * pQ[b];
        v += h[r][c] * pP[a] * pQ[b];
        return v;
    }

public:
    vector<int> findStampPos(vector<vector<string>>& tray, vector<vector<string>>& stamp) {
        int m = (int)tray.size(), n = (int)tray[0].size();
        int a = (int)stamp.size(), b = (int)stamp[0].size();
        auto ht = build(tray);
        auto hs = build(stamp);
        auto pP = powull(m, P);
        auto pQ = powull(n, Q);
        unsigned long long need = rect(hs, 0, 0, a, b, pP, pQ);
        for (int i = 0; i <= m - a; i++) {
            for (int j = 0; j <= n - b; j++) {
                if (rect(ht, i, j, a, b, pP, pQ) == need) return {i, j};
            }
        }
        return {-1, -1};
    }
};
