#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int countNeedUpgrade(vector<int>& versions, int baseline) {
        // 排序后用 lower_bound 找第一个 >= baseline
        vector<int> a = versions;
        sort(a.begin(), a.end());
        auto it = lower_bound(a.begin(), a.end(), baseline);
        // 距离末尾即为答案个数
        return (int)(a.end() - it);
    }
};
