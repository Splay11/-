#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long solve_case(int m, vector<int>& vals) {
    // 按优先级分值从高到低排序
    sort(vals.begin(), vals.end(), greater<int>());

    long long team_a = 0;  // 甲组累计分值
    long long team_b = 0;  // 乙组累计分值

    // 排序后双方轮流取：偶数下标归甲组，奇数下标归乙组
    for (int i = 0; i < m; i++) {
        if (i % 2 == 0) {
            team_a += vals[i];
        } else {
            team_b += vals[i];
        }
    }

    return team_a - team_b;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int m;
        cin >> m;

        vector<int> vals(m);
        for (int i = 0; i < m; i++) {
            cin >> vals[i];
        }

        cout << solve_case(m, vals) << '\n';
    }

    return 0;
}
