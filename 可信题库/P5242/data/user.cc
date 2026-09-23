#include <vector>
using namespace std;

class ParkingLot {
 public:
  ParkingLot(int n) {}
  int reserve(int carId, int start, int end) { return -1; }
  bool cancel(int carId) { return false; }
  int spotOf(int carId) { return -1; }
  int busyCount(int time) { return 0; }
};
