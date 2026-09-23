#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string a, b, c;
    cin >> a >> b >> c;
    int n = (int)a.size(), m = (int)b.size(), p = (int)c.size();

    // f[i][j][k]：后缀 LCS 长度
    vector<vector<vector<int>>> f(n + 1, vector<vector<int>>(m + 1, vector<int>(p + 1, 0)));
    for (int i = n; i >= 0; i--) {
        for (int j = m; j >= 0; j--) {
            for (int k = p; k >= 0; k--) {
                if (i == n || j == m || k == p) {
                    f[i][j][k] = 0;
                } else if (a[i] == b[j] && b[j] == c[k]) {
                    f[i][j][k] = 1 + f[i + 1][j + 1][k + 1];
                } else {
                    f[i][j][k] = max({f[i + 1][j][k], f[i][j + 1][k], f[i][j][k + 1]});
                }
            }
        }
    }

    int L = f[0][0][0];
    cout << L << '\n';

    // 贪心构造字典序最小 LCS
    int i = 0, j = 0, k = 0, remain = L;
    string res;
    while (remain > 0) {
        for (char ch = 'a'; ch <= 'z'; ch++) {
            int ni = -1, nj = -1, nk = -1;
            for (int t = i; t < n; t++) if (a[t] == ch) { ni = t; break; }
            for (int t = j; t < m; t++) if (b[t] == ch) { nj = t; break; }
            for (int t = k; t < p; t++) if (c[t] == ch) { nk = t; break; }
            if (ni < 0 || nj < 0 || nk < 0) continue;
            if (f[ni + 1][nj + 1][nk + 1] == remain - 1) {
                res.push_back(ch);
                i = ni + 1; j = nj + 1; k = nk + 1;
                remain--;
                break;
            }
        }
    }
    cout << res << '\n';
    return 0;
}
