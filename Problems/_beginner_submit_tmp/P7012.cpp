#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minAuditDays(vector<int>& loads) {
        // 空数组无需抽查
        if (loads.empty()) return 0;
        // 总负载用 long long，避免相加溢出
        long long total = 0;
        for (int x : loads) total += x;
        // 复制后降序排序，贪心取最大
        vector<int> a = loads;
        sort(a.begin(), a.end(), greater<int>());
        long long s = 0;
        for (int i = 0; i < (int)a.size(); i++) {
            s += a[i];
            // 2*s > total 即选出严格过半
            if (s * 2 > total) return i + 1;
        }
        return (int)a.size();
    }
};
