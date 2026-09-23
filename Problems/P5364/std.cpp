#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int m, d;
    cin >> m >> d;
    vector<int> v(m);
    for (int i = 0; i < m; i++) {
        cin >> v[i];
    }
    // 与 d 同奇偶的才能让 (x+d) 为偶数；diff 只能和 same 配
    vector<int> same, diff;
    for (int i = 0; i < m; i++) {
        if (v[i] % 2 == d % 2) {
            same.push_back(v[i]);
        } else {
            diff.push_back(v[i]);
        }
    }
    vector<pair<int, int> > pairs;
    int i = 0, j = 0;
    // 先把不同奇偶的配给 same
    while (i < (int)diff.size() && j < (int)same.size()) {
        pairs.push_back(make_pair(diff[i], same[j]));
        i++;
        j++;
    }
    // 剩下的 same 两两配对
    while (j + 1 < (int)same.size()) {
        pairs.push_back(make_pair(same[j], same[j + 1]));
        j += 2;
    }
    cout << (int)pairs.size() << "\n";
    for (int t = 0; t < (int)pairs.size(); t++) {
        cout << pairs[t].first << " " << pairs[t].second << "\n";
    }
    return 0;
}
