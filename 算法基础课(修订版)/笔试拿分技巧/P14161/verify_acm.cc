#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    long long solve(vector<int>& times, vector<pair<int, int>>& mutexPairs) {
        int jobNum = (int)times.size();
        long long conflict[30]{};
        for (auto& p : mutexPairs) {
            int u = p.first - 1;
            int v = p.second - 1;
            conflict[u] |= 1LL << v;
            conflict[v] |= 1LL << u;
        }

        long long maxCount = 0;
        long long minTotalTime = LLONG_MAX;

        function<void(int, long long, long long, long long)> dfs =
            [&](int index, long long currentMask, long long count, long long totalTime) {
                if (count > maxCount || (count == maxCount && totalTime < minTotalTime)) {
                    maxCount = count;
                    minTotalTime = totalTime;
                }
                for (int i = index; i < jobNum; ++i) {
                    if (!(currentMask & (1LL << i)) && (conflict[i] & currentMask) == 0) {
                        dfs(i + 1, currentMask | (1LL << i), count + 1, totalTime + times[i]);
                    }
                }
            };

        dfs(0, 0, 0, 0);
        return minTotalTime;
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
