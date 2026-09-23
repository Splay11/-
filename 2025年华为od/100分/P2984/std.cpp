#include <string>
#include <vector>

using namespace std;

class Solution {
 public:
  int countFormableGroups(string a, string b) {
    vector<char> chars(a.begin(), a.end());
    int ans = 0;
    while (true) {
      int j = 0;
      vector<char> nxt;
      for (char ch : chars) {
        if (j < (int)b.size() && ch == b[j])
          j++;
        else
          nxt.push_back(ch);
      }
      if (j == (int)b.size()) {
        ans++;
        chars.swap(nxt);
      } else {
        break;
      }
    }
    return ans;
  }
};
