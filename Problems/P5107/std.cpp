#include <cctype>
#include <string>
#include <vector>

using namespace std;

class Solution {
 public:
  string rearrangeSN(string sn, int m) {
    // 校验字符集：仅字母、数字、破折号合法
    for (char c : sn) {
      if (!isalnum((unsigned char)c) && c != '-') return "";
    }

    vector<char> chars;
    for (char c : sn) {
      if (isalnum((unsigned char)c)) {
        chars.push_back((char)toupper((unsigned char)c));
      }
    }
    if (chars.empty()) return "";

    int n = (int)chars.size();
    int rem = n % m;
    vector<string> groups;
    int idx = 0;
    // 不能整除 m 时，余数段放在第一段
    if (rem != 0) {
      groups.emplace_back(chars.begin(), chars.begin() + rem);
      idx += rem;
    }
    while (idx < n) {
      groups.emplace_back(chars.begin() + idx, chars.begin() + idx + m);
      idx += m;
    }

    string ans;
    for (size_t i = 0; i < groups.size(); i++) {
      if (i) ans.push_back('-');
      ans += groups[i];
    }
    return ans;
  }
};
