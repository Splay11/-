#include <iostream>
#include <vector>
using namespace std;

// 工位不撤走，左右不会贴合，最少勾取次数等于极大等值段段数
int countRuns(const vector<int>& xs) {
    if (xs.empty()) {
        return 0;
    }
    int runs = 1;
    for (int i = 1; i < (int)xs.size(); i++) {
        // 零件个数一变，当前这段就不能再往后勾
        if (xs[i] != xs[i - 1]) {
            runs++;
        }
    }
    return runs;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> ans;
    ans.reserve(q);
    for (int t = 0; t < q; t++) {
        int m;
        cin >> m;
        vector<int> xs(m);
        for (int i = 0; i < m; i++) {
            cin >> xs[i];
        }
        ans.push_back(countRuns(xs));
    }
    // q 个答案放在同一行
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
