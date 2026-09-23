#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    long long solve(vector<int>& times, vector<pair<int, int>>& mutexPairs) {
        // 请在这里实现
        return 0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int jobNum;
    cin >> jobNum;
    vector<int> times(jobNum);
    for (int i = 0; i < jobNum; ++i) {
        cin >> times[i];
    }

    int mutexNum;
    cin >> mutexNum;
    vector<pair<int, int>> mutexPairs(mutexNum);
    for (int i = 0; i < mutexNum; ++i) {
        cin >> mutexPairs[i].first >> mutexPairs[i].second;
    }

    Solution solution;
    cout << solution.solve(times, mutexPairs);
    return 0;
}
