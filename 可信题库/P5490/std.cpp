#include <vector>
using namespace std;

class ParcelSlots {
  int n;
  vector<int> slot;
  int cnt;

 public:
  ParcelSlots(int n) : n(n), slot(n, 0), cnt(0) {}

  bool put(int i, int w) {
    if (i < 1 || i > n || w <= 0 || slot[i - 1] != 0) return false;
    slot[i - 1] = w;
    cnt++;
    return true;
  }

  int take(int i) {
    if (i < 1 || i > n || slot[i - 1] == 0) return 0;
    int w = slot[i - 1];
    slot[i - 1] = 0;
    cnt--;
    return w;
  }

  bool moveRight(int i) {
    if (i < 1 || i >= n || slot[i - 1] == 0 || slot[i] != 0) return false;
    slot[i] = slot[i - 1];
    slot[i - 1] = 0;
    return true;
  }

  int occupied() { return cnt; }
};
