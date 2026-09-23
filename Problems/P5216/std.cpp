#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 取 y = m/2 时对冲值最小：y XOR (m-y)
int64 min_hedge(int64 m) {
    return (m / 2) ^ ((m + 1) / 2);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        int64 m;
        cin >> m;
        cout << min_hedge(m) << '\n';
    }
    return 0;
}
