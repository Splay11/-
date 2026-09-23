#include <string>

using namespace std;

class LogSystem {
   public:
    LogSystem() {}
    void enter(int spanId, bool inherit) {}
    string log(string msg) { return ""; }
    void leave(int spanId) {}
};
