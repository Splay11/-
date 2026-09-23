#include <algorithm>
#include <vector>

using namespace std;

class Solution {
   public:
    int countValidPlans(vector<int>& timestamps, int minInterval) {
        vector<int> ts = timestamps;
        sort(ts.begin(), ts.end());
        int n = (int)ts.size();
        int ans = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            bool ok = true;
            vector<int> picked;
            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) {
                    picked.push_back(ts[i]);
                }
            }
            for (int i = 0; i < (int)picked.size(); i++) {
                for (int j = i + 1; j < (int)picked.size(); j++) {
                    if (picked[j] - picked[i] < minInterval) {
                        ok = false;
                        break;
                    }
                }
                if (!ok) {
                    break;
                }
            }
            if (ok) {
                ans++;
            }
        }
        return ans;
    }
};
