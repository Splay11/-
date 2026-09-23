#include <vector>
using namespace std;

class ParcelSlots {
 public:
  ParcelSlots(int n) { (void)n; }

  bool put(int i, int w) {
    (void)i;
    (void)w;
    return false;
  }

  int take(int i) {
    (void)i;
    return 0;
  }

  bool moveRight(int i) {
    (void)i;
    return false;
  }

  int occupied() { return 0; }
};
