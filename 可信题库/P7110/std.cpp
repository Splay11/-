#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int minPassDays(vector<int>& slots, vector<int>& prep) {
        int n = (int)slots.size();
        int m = (int)prep.size();
        auto ok = [&](int days) {
            vector<int> last(m + 1, -1);
            for (int i = 0; i < days; ++i) {
                int t = slots[i];
                if (t > 0) last[t] = i;
            }
            for (int t = 1; t <= m; ++t)
                if (last[t] < 0) return false;
            vector<int> order(m);
            for (int t = 1; t <= m; ++t) order[t - 1] = t;
            sort(order.begin(), order.end(), [&](int a, int b) {
                return last[a] < last[b];
            });
            int freeDays = 0, j = 0;
            for (int day = 0; day < days; ++day) {
                if (j < m && last[order[j]] == day) {
                    int need = prep[order[j] - 1];
                    if (freeDays < need) return false;
                    freeDays -= need;
                    ++j;
                } else {
                    ++freeDays;
                }
            }
            return j == m;
        };
        if (!ok(n)) return -1;
        int lo = 1, hi = n;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (ok(mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
