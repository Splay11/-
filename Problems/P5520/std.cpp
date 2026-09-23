#include <iostream>
#include <iomanip>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // 前缀和与平方和
    vector<double> ps(n + 1), qs(n + 1);
    for (int i = 0; i < n; i++) {
        ps[i + 1] = ps[i] + a[i];
        qs[i + 1] = qs[i] + (double)a[i] * a[i];
    }

    double best = -1.0;
    for (int k = 1; k < n; k++) {
        double n1 = k, n2 = n - k;
        // 方差 = 二阶矩 - 均值平方
        double v1 = qs[k] / n1 - (ps[k] / n1) * (ps[k] / n1);
        double v2 = (qs[n] - qs[k]) / n2 - ((ps[n] - ps[k]) / n2) * ((ps[n] - ps[k]) / n2);
        best = max(best, v1 + v2);
    }
    cout << fixed << setprecision(6) << best << '\n';
    return 0;
}
