#include <iostream>
#include <vector>
using namespace std;

// 排列型完全背包：外层容量、内层数字，顺序不同算不同方案
int solve(const vector<int>& nums, int target) {
    // dp[t]：凑出 t 的有序方案数。凑出 0 视为一种空方案。
    vector<long long> dp(target + 1, 0);
    dp[0] = 1;
    // 外层容量、内层数字：最后一个数可以是任意 x，从而把排列都算进去
    for (int t = 1; t <= target; t++) {
        for (int i = 0; i < (int)nums.size(); i++) {
            int x = nums[i];
            if (t >= x) {
                dp[t] += dp[t - x];
            }
        }
    }
    // 凑不出时 dp[target] 仍为 0；题目保证答案在 32 位有符号整数范围内
    return (int)dp[target];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << solve(nums, target) << '\n';
    return 0;
}
