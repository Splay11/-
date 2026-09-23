#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    const long long INF = (1LL << 62);
    // f：选中当前位置；g：不选当前位置且已非空
    long long f = a[0], g = INF;
    for (int i = 1; i < n; i++) {
        long long ng = min(f, g);
        long long nf = a[i] + (g >= INF / 2 ? 0 : min(0LL, g));
        f = nf;
        g = ng;
    }
    cout << min(f, g) << "\n";
    return 0;
}
