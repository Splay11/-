#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
using namespace std;

string maxOfLen(int L, const vector<int>& digits) {
    // 构造长度 L 的最大合法数
    vector<int> nz;
    for (int d : digits) if (d > 0) nz.push_back(d);
    if (L <= 0) return "";
    if (nz.empty()) {
        if (L == 1 && find(digits.begin(), digits.end(), 0) != digits.end()) return "0";
        return "";
    }
    int mx = *max_element(digits.begin(), digits.end());
    int first = *max_element(nz.begin(), nz.end());
    return string(1, char('0' + first)) + string(L - 1, char('0' + mx));
}

string maxSameLenLt(const string& s, const vector<int>& digits) {
    // 迭代：从右往左找可减小位，避免长串递归爆栈
    bool has[10] = {};
    int mx = 0;
    for (int d : digits) {
        has[d] = true;
        mx = max(mx, d);
    }
    int n = (int)s.size();
    vector<int> sdig(n);
    for (int i = 0; i < n; i++) sdig[i] = s[i] - '0';

    for (int i = n - 1; i >= 0; i--) {
        bool ok = true;
        for (int j = 0; j < i; j++) {
            if (!has[sdig[j]]) { ok = false; break; }
            if (j == 0 && n > 1 && sdig[j] == 0) { ok = false; break; }
        }
        if (!ok) continue;
        int bestD = -1;
        for (int d = 0; d < sdig[i]; d++) {
            if (!has[d]) continue;
            if (i == 0 && n > 1 && d == 0) continue;
            bestD = d;
        }
        if (bestD < 0) continue;
        string res;
        for (int j = 0; j < i; j++) res.push_back(char('0' + sdig[j]));
        res.push_back(char('0' + bestD));
        res.append(n - i - 1, char('0' + mx));
        return res;
    }
    return "";
}

string better(const string& a, const string& b) {
    if (a.empty()) return b;
    if (b.empty()) return a;
    if (a.size() != b.size()) return a.size() > b.size() ? a : b;
    return a >= b ? a : b;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    set<int> st;
    for (int i = 0; i < n; i++) {
        int x; cin >> x; st.insert(x);
    }
    vector<int> digits(st.begin(), st.end());
    string s;
    cin >> s;

    string best = maxSameLenLt(s, digits);
    if ((int)s.size() > 1) {
        string shorter = maxOfLen((int)s.size() - 1, digits);
        best = better(best, shorter);
    }
    if (best.empty()) cout << -1 << '\n';
    else cout << best << '\n';
    return 0;
}
