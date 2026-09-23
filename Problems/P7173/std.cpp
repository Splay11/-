#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 全体异或得到 a^b，用最低的 1 把两个落单数分到两堆
pair<int, int> solve(const vector<int>& nums) {
    int xor_all = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        xor_all ^= nums[i];
    }
    unsigned int bit = (unsigned int)xor_all & -(unsigned int)xor_all;
    int a = 0, b = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if ((unsigned int)nums[i] & bit) {
            a ^= nums[i];
        } else {
            b ^= nums[i];
        }
    }
    if (a > b) {
        int t = a;
        a = b;
        b = t;
    }
    return make_pair(a, b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    pair<int, int> ans = solve(nums);
    cout << ans.first << ' ' << ans.second << '\n';
    return 0;
}
