#include <vector>
using namespace std;

class Solution {
public:
    int minForceWindow(vector<int>& hits) {
        int n = (int)hits.size();
        int tot = 0;
        for (int x : hits) tot |= x;
        if (tot == 0) return 1;
        int ans = 1;
        for (int b = 0; b < 31; b++) {
            if (((tot >> b) & 1) == 0) continue;
            int prev = -1, mx = 0;
            for (int i = 0; i < n; i++) {
                if ((hits[i] >> b) & 1) {
                    mx = max(mx, i - prev);
                    prev = i;
                }
            }
            mx = max(mx, n - prev);
            ans = max(ans, mx);
        }
        return ans;
    }
};
