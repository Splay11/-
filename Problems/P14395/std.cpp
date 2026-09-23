#include <algorithm>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<string> filterValidAClassIPs(vector<string>& ips) {
    // 存 (排序键, 原字符串)，便于按网段层级排序后还原 IP
    vector<pair<tuple<int, int, int>, string>> valid;
    for (auto& ip : ips) {
      tuple<int, int, int> key;
      if (parseValid(ip, key)) valid.push_back({key, ip});
    }
    // tuple 字典序等价于 (第二段, 第三段, 第四段) 数值升序
    sort(valid.begin(), valid.end(),
         [](const pair<tuple<int, int, int>, string>& a,
            const pair<tuple<int, int, int>, string>& b) {
           return a.first < b.first;
         });
    vector<string> ans;
    for (auto& p : valid) ans.push_back(p.second);
    return ans;
  }

 private:
  // 校验 IP 合法性；合法时通过 out 返回后三段数值
  bool parseValid(const string& ip, tuple<int, int, int>& out) {
    vector<int> nums;
    size_t i = 0;
    // 手动按 '.' 切四段，避免 split 后丢失空段信息
    for (int seg = 0; seg < 4; seg++) {
      if (i >= ip.size()) return false;
      size_t j = ip.find('.', i);
      if (j == string::npos) {
        // 仅第四段允许后面没有 '.'
        if (seg != 3) return false;
        j = ip.size();
      }
      string p = ip.substr(i, j - i);
      if (p.empty()) return false;
      // 禁止前导零（"0" 本身合法）
      if (p.size() > 1 && p[0] == '0') return false;
      int v = 0;
      for (char c : p) {
        if (c < '0' || c > '9') return false;
        v = v * 10 + (c - '0');
      }
      if (v < 0 || v > 255) return false;
      nums.push_back(v);
      // 末段后无 '.'，游标应停在串尾而非 size+1
      i = (seg == 3) ? j : j + 1;
    }
    if (i != ip.size()) return false;
    // 首段必须为 10
    if (nums[0] != 10) return false;
    out = make_tuple(nums[1], nums[2], nums[3]);
    return true;
  }
};
