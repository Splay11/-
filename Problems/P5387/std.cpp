#include <iostream>
#include <vector>
using namespace std;

// 按 (v+t) 的奇偶分成两类：奇类只能配偶类，偶类之间可以互配
vector<pair<int, int> > max_pairs(int t, const vector<int> &v) {
    vector<int> ev, od;
    for (size_t i = 0; i < v.size(); i++) {
        if ((v[i] + t) % 2 == 0) {
            ev.push_back(v[i]);
        } else {
            od.push_back(v[i]);
        }
    }
    vector<pair<int, int> > pairs;
    if ((int)od.size() > (int)ev.size()) {
        // 偶类不够，全部拿去配奇类
        for (size_t i = 0; i < ev.size(); i++) {
            pairs.push_back(make_pair(ev[i], od[i]));
        }
    } else {
        // 先把奇类配完，剩下的偶类两两互配
        for (size_t i = 0; i < od.size(); i++) {
            pairs.push_back(make_pair(od[i], ev[i]));
        }
        vector<int> rest(ev.begin() + od.size(), ev.end());
        for (size_t i = 0; i + 1 < rest.size(); i += 2) {
            pairs.push_back(make_pair(rest[i], rest[i + 1]));
        }
    }
    return pairs;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, t;
    cin >> m >> t;
    vector<int> v(m);
    for (int i = 0; i < m; i++) {
        cin >> v[i];
    }
    vector<pair<int, int> > pairs = max_pairs(t, v);
    cout << pairs.size() << "\n";
    for (size_t i = 0; i < pairs.size(); i++) {
        cout << pairs[i].first << " " << pairs[i].second << "\n";
    }
    return 0;
}
