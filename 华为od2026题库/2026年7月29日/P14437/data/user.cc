#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> getMaxValues(vector<vector<int>>& data, int interval) {
        int n = (int)data.size();
        vector<int> result(n);
        for (int i = 0; i < n; i++) {
            long long ti = data[i][0];
            int vi = data[i][1];
            long long lower = ti - interval;
            int maxVal = vi;
            for (int j = 0; j < i; j++) {
                long long tj = data[j][0];
                int vj = data[j][1];
                if (tj >= lower && tj <= ti) {
                    if (vj > maxVal) maxVal = vj;
                }
            }
            result[i] = maxVal;
        }
        return result;
    }
};
