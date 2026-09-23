#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

string kthLargestNumber(vector<string>& nums, int k) {
    sort(nums.begin(), nums.end(), [](const string& a, const string& b) {
        if (a.size() != b.size()) {
            // 长度不同：长的数更大，排在前面
            return a.size() > b.size();
        }
        // 长度相同且无前导零：字典序大的数更大，排在前面
        return a > b;
    });
    // 第 k 大对应排序后下标 k-1（重复字符串各自占一个名次，不需要去重）
    return nums[k - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：n（数组长度）和 k（排名）
    int n, k;
    cin >> n >> k;
    // 第二行：n 个表示非负整数的字符串
    vector<string> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    // 输出第 k 大的那个字符串
    cout << kthLargestNumber(nums, k) << "\n";
    return 0;
}
