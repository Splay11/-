#include <string>
#include <vector>

using namespace std;

class Solution {
 public:
  int maxBracketDepth(string s) {
    vector<char> stack;
    int depth = 0, best = 0;
    for (char ch : s) {
      if (ch == '(' || ch == '[' || ch == '{') {
        stack.push_back(ch);
        depth++;
        if (depth > best) best = depth;
      } else if (ch == ')' || ch == ']' || ch == '}') {
        char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
        if (stack.empty() || stack.back() != need) return 0;
        stack.pop_back();
        depth--;
      } else {
        return 0;
      }
    }
    return stack.empty() ? best : 0;
  }
};
