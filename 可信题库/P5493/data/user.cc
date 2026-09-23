#include <vector>
using namespace std;

class FileLogger {
 public:
  FileLogger(int fileCap, int totalCap) {
    (void)fileCap;
    (void)totalCap;
  }

  int putLog(int mid, int nbytes) {
    (void)mid;
    (void)nbytes;
    return 0;
  }

  vector<vector<int>> listFiles() { return {}; }

  int totalSize() { return 0; }
};
