#include <algorithm>
#include <string>

using namespace std;

class Solution {
 public:
  string processString(string s) {
    string digits, letters;
    for (char c : s) {
      if (c >= '0' && c <= '9') digits += c;
      else if (c >= 'A' && c <= 'Z') letters += c;
    }
    if (digits.empty() || letters.empty()) return s;
    string res;
    int n = min((int)digits.size(), (int)letters.size());
    for (int i = 0; i < n; i++) {
      res += digits[i];
      int cnt = digits[i] - '0';
      if (cnt > 0) res += string(cnt, letters[i]);
    }
    if ((int)digits.size() > n) res += digits.substr(n);
    else if ((int)letters.size() > n) res += letters.substr(n);
    return res;
  }
};
