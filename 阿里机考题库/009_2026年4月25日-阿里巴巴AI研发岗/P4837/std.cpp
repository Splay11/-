#include <bits/stdc++.h>
using namespace std;

const int MAX_MASK = 1023;
const int SIZE = 1024;

int countDistinctMasks(vector<int>& feat) {
    // g[mask]：所有包含 mask 的超集特征值的按位与结果
    vector<int> g(SIZE, MAX_MASK);

    // exist[mask]：是否存在原初值恰好为 mask
    vector<bool> exist(SIZE, false);

    for (int x : feat) {
        g[x] = x;
        exist[x] = true;
    }

    // 超集 DP：合并更大掩码的按位与信息
    for (int bit = 0; bit < 10; bit++) {
        for (int mask = 0; mask < SIZE; mask++) {
            if ((mask & (1 << bit)) == 0) {
                int superMask = mask | (1 << bit);
                if (exist[superMask]) {
                    g[mask] &= g[superMask];
                    exist[mask] = true;
                }
            }
        }
    }

    int ans = 0;
    for (int mask = 0; mask < SIZE; mask++) {
        // 可达当且仅当存在超集且其按位与恰好为 mask
        if (exist[mask] && g[mask] == mask) {
            ans++;
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int tc;
    cin >> tc;

    while (tc--) {
        int m;
        cin >> m;

        vector<int> feat(m);
        for (int i = 0; i < m; i++) {
            cin >> feat[i];
        }

        cout << countDistinctMasks(feat) << '\n';
    }

    return 0;
}
