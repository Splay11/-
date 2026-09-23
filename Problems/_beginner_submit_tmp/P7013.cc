#include <climits>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    int minCoverWindow(vector<int>& events, vector<int>& need) {
        if (need.empty()) return 0;
        unordered_map<int, int> needCnt, win;
        for (int x : need) needCnt[x] = 1;
        int miss = (int)need.size();
        int ans = INT_MAX, l = 0;
        for (int r = 0; r < (int)events.size(); r++) {
            int x = events[r];
            if (needCnt.count(x)) {
                if (win[x] == 0) miss--;
                win[x]++;
            }
            while (miss == 0 && l <= r) {
                ans = min(ans, r - l + 1);
                int y = events[l];
                if (needCnt.count(y)) {
                    win[y]--;
                    if (win[y] == 0) miss++;
                }
                l++;
            }
        }
        return ans == INT_MAX ? -1 : ans;
    }
};
