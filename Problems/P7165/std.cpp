#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// 四个数做 24 点：每次取两个数做四则运算再递归
const double EPS = 1e-6;

bool dfs(vector<double> a) {
    if ((int)a.size() == 1) {
        return fabs(a[0] - 24.0) < EPS;
    }
    int n = (int)a.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                continue;
            }
            vector<double> rest;
            for (int k = 0; k < n; k++) {
                if (k != i && k != j) {
                    rest.push_back(a[k]);
                }
            }
            double x = a[i], y = a[j];
            double cands[4];
            int m = 3;
            cands[0] = x + y;
            cands[1] = x - y;
            cands[2] = x * y;
            if (fabs(y) > EPS) {
                cands[3] = x / y;
                m = 4;
            }
            for (int t = 0; t < m; t++) {
                vector<double> nxt = rest;
                nxt.push_back(cands[t]);
                if (dfs(nxt)) {
                    return true;
                }
            }
        }
    }
    return false;
}

bool solve(const vector<int>& cards) {
    vector<double> a;
    for (int i = 0; i < 4; i++) {
        a.push_back((double)cards[i]);
    }
    return dfs(a);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    vector<int> cards(4);
    for (int i = 0; i < 4; i++) {
        cin >> cards[i];
    }
    cout << (solve(cards) ? "true" : "false") << '\n';
    return 0;
}
