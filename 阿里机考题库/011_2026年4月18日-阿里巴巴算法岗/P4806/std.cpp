#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int solve_case(int k, int s, vector<pair<int, int>>& zones) {
    // 按禁入区间左端点排序
    sort(zones.begin(), zones.end());

    int curL = zones[0].first;
    int curR = zones[0].second;

    for (int i = 1; i < k; i++) {
        int L = zones[i].first;
        int R = zones[i].second;

        // 相交或相邻则合并禁入区间
        if (L <= curR + 1) {
            if (R > curR) {
                curR = R;
            }
        } else {
            if (curL <= s && s <= curR) {
                return min(s - curL + 1, curR - s + 1);
            }
            curL = L;
            curR = R;
        }
    }

    if (curL <= s && s <= curR) {
        return min(s - curL + 1, curR - s + 1);
    }

    // 当前坐标不在任何禁入区内
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int k, s;
        cin >> k >> s;

        vector<pair<int, int>> zones(k);
        for (int i = 0; i < k; i++) {
            cin >> zones[i].first >> zones[i].second;
        }

        cout << solve_case(k, s, zones) << '\n';
    }

    return 0;
}
