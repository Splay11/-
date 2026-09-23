#include <string>
using namespace std;

class Solution {
 public:
  int firstTasteLevel(string note) {
    for (char ch : note) {
      if (ch >= '0' && ch <= '9') {
        return ch - '0';
      }
    }
    return -1;
  }
};
