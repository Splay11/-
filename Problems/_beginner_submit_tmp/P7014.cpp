#include <vector>
using namespace std;

class Solution {
public:
    int maxOnline(vector<int>& changes) {
        // 顺序模拟前缀和，并记录最大值
        int cur = 0;
        int ans = 0;
        for (int x : changes) {
            cur += x;
            if (cur > ans) ans = cur;
        }
        return ans;
    }
};
