#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

// 用哈希表记录出现过的数，再次出现就是有重复
bool solve(const vector<int>& nums) {
    unordered_set<int> seen;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (seen.count(nums[i])) {
            return true;
        }
        seen.insert(nums[i]);
    }
    return false;
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
    // 题面要求输出小写 true / false
    cout << (solve(nums) ? "true" : "false") << '\n';
    return 0;
}
