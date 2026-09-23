#include <string>

using namespace std;

class Solution {
 public:
  int minDistinctAfterSwap(string resA, string resB) {
    int countA[26] = {}, countB[26] = {};
    for (char c : resA) countA[c - 'a']++;
    for (char c : resB) countB[c - 'a']++;

    int dA = 0, dB = 0;
    for (int i = 0; i < 26; i++) {
      if (countA[i]) dA++;
      if (countB[i]) dB++;
    }

    int ans = -1;
    for (int a = 0; a < 26; a++) {
      if (!countA[a]) continue;
      for (int b = 0; b < 26; b++) {
        if (!countB[b]) continue;
        int cand;
        if (a == b) {
          if (dA != dB) continue;
          cand = dA;
        } else {
          int da = dA - (countA[a] == 1 ? 1 : 0) + (countA[b] == 0 ? 1 : 0);
          int db = dB - (countB[b] == 1 ? 1 : 0) + (countB[a] == 0 ? 1 : 0);
          if (da != db) continue;
          cand = da;
        }
        if (ans == -1 || cand < ans) ans = cand;
      }
    }
    return ans;
  }
};
