#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

vector<int> solve(vector<int> p, long long k) {
    int n = (int)p.size();
    long long limit = 1LL * n * (n - 1) / 2;
    if (k >= limit) {
        sort(p.begin(), p.end());
        return p;
    }
    for (long long t = 0; t < k; t++) {
        bool swapped = false;
        for (int i = 0; i + 1 < n; i++) {
            if (p[i] > p[i + 1]) {
                swap(p[i], p[i + 1]);
                swapped = true;
                break;
            }
        }
        if (!swapped) break;
    }
    return p;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n;
        long long k;
        cin >> n >> k;
        vector<int> p(n);
        for (int i = 0; i < n; i++) cin >> p[i];
        auto ans = solve(p, k);
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }
    return 0;
}
