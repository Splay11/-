#include <vector>
using namespace std;

class Solution {
public:
    long long bestCorrectedTotal(vector<int>& scores) {
        long long total = 0;
        // 数组非空，先把第一项当作最小值
        int mn = scores[0];
        // 一趟循环同时求出原总分与最小项
        for (int v : scores) {
            total += v;
            if (v < mn) mn = v;
        }
        // 订正最小项得到最大总分 total - 2 * mn；总和可能超 32 位，用 long long
        return total - 2LL * mn;
    }
};
