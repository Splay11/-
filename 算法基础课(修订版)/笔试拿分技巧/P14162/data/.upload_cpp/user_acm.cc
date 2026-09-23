#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int solve(int n, int k, vector<pair<int, int>>& intervals) {
        // 请在这里实现
        return 0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<pair<int, int>> intervals(n);
    for (int i = 0; i < n; ++i) {
        cin >> intervals[i].first >> intervals[i].second;
    }

    Solution solution;
    cout << solution.solve(n, k, intervals);
    return 0;
}
