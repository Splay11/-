#include <bits/stdc++.h>
using namespace std;

vector<long long> find_elements(const vector<long long>& a) {
    int n = (int)a.size();
    // pref_max[i] = a[0..i] 的最大值
    vector<long long> pref_max(n), suf_min(n);
    pref_max[0] = a[0];
    for (int i = 1; i < n; ++i) {
        pref_max[i] = max(pref_max[i - 1], a[i]);
    }
    suf_min[n - 1] = a[n - 1];
    for (int i = n - 2; i >= 0; --i) {
        suf_min[i] = min(suf_min[i + 1], a[i]);
    }
    vector<long long> ans;
    for (int i = 0; i < n; ++i) {
        // 比左边都大、比右边都小（严格比较）
        bool left_ok = (i == 0) || (a[i] > pref_max[i - 1]);
        bool right_ok = (i == n - 1) || (a[i] < suf_min[i + 1]);
        if (left_ok && right_ok) {
            ans.push_back(a[i]);
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    vector<long long> ans = find_elements(a);
    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
