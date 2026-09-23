#include <iostream>
#include <vector>
using namespace std;

const int OFFSET = 10000;

// 值域只有 -10000 到 10000，计数后从大到小数第 k 个
int solve(const vector<int>& nums, int k) {
    int cnt[2 * OFFSET + 1];
    for (int i = 0; i <= 2 * OFFSET; i++) {
        cnt[i] = 0;
    }
    for (int i = 0; i < (int)nums.size(); i++) {
        cnt[nums[i] + OFFSET]++;
    }
    int need = k;
    // 从大到小扫，减掉该值出现次数
    for (int v = OFFSET; v >= -OFFSET; v--) {
        need -= cnt[v + OFFSET];
        if (need <= 0) {
            return v;
        }
    }
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << solve(nums, k) << '\n';
    return 0;
}
