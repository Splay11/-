#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// 判断前缀和集合中是否包含 T,2T,...,kT
bool canSplit(const unordered_set<long long>& prefSet, long long T, long long k) {
    for (long long i = 1; i <= k; i++) {
        if (!prefSet.count(T * i)) return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    long long S = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        S += a[i];
    }

    if (S == 0) {
        // 每段和为 0
        long long p = 0;
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            p += a[i];
            if (p == 0) cnt++;
        }
        cout << cnt << '\n';
        return 0;
    }

    unordered_set<long long> prefSet;
    long long pref = 0;
    for (int i = 0; i < n; i++) {
        pref += a[i];
        prefSet.insert(pref);
    }

    int best = 1;
    pref = 0;
    for (int i = 0; i < n - 1; i++) {
        pref += a[i];
        long long T = pref;
        if (T == 0) continue;
        if (S % T != 0) continue;
        long long k = S / T;
        if (k <= best) continue;
        if (canSplit(prefSet, T, k)) best = (int)k;
    }
    cout << best << '\n';
    return 0;
}
