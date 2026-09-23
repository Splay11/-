#include <algorithm>
#include <string>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<string> sortConvertedNums(vector<int>& nums, int base) {
    int n = (int)nums.size();
    vector<string> converted(n);
    for (int i = 0; i < n; i++) converted[i] = toBase(nums[i], base);
    vector<int> order(n);
    for (int i = 0; i < n; i++) order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b) {
      return nums[a] > nums[b];
    });
    vector<string> ans(n);
    for (int i = 0; i < n; i++) ans[i] = converted[order[i]];
    return ans;
  }

 private:
  string toBase(int n, int base) {
    if (n == 0) return "0";
    const string digits = "0123456789abcdef";
    string s;
    while (n > 0) {
      s.push_back(digits[n % base]);
      n /= base;
    }
    reverse(s.begin(), s.end());
    return s;
  }
};
