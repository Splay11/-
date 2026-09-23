#include <iostream>
#include <vector>
using namespace std;

long long solve(const vector<long long>& a) {
    int n = (int)a.size();
    long long s = 0;
    for (auto x : a) s += x;
    if (n % 2 == 0 && s % 2 == 1) return -1;
    long long diff = 0;
    for (int i = 0; i < n / 2; i++)
        diff += abs(a[i] - a[n - 1 - i]);
    return (diff + 1) / 2;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<long long> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];
        cout << solve(a) << '\n';
    }
    return 0;
}
