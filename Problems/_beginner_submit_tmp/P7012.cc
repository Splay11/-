#include <vector>
using namespace std;

class Solution {
public:
    int longestSafeWindow(vector<int>& loads, long long limit) {
        int n = (int)loads.size();
        int ans = 0;
        long long s = 0;
        int l = 0;
        // 右端扩展；超限则收缩左端
        for (int r = 0; r < n; r++) {
            s += loads[r];
            while (l <= r && s > limit) {
                s -= loads[l];
                l++;
            }
            ans = max(ans, r - l + 1);
        }
        return ans;
    }
};
