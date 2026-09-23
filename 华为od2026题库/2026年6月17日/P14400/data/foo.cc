#include <string>
#include <unordered_map>

using namespace std;

class Solution {
 public:
  string processChunks(string s, int n) {
    string res;
    for (int i = 0; i < (int)s.size(); i += n) {
      string chunk = s.substr(i, n);
      unordered_map<char, int> last;
      for (int j = 0; j < (int)chunk.size(); j++) last[chunk[j]] = j;
      for (int j = 0; j < (int)chunk.size(); j++)
        if (last[chunk[j]] == j) res += chunk[j];
    }
    return res;
  }
};
