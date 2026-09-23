#include <vector>

using namespace std;

class GCSystem {
   public:
    GCSystem(int youngSize) {}
    void createObject(int objectId) {}
    void markObjects(vector<int> objectIds) {}
    void manualGC(int generation) {}
    vector<int> getLiveObjects(int generation) { return {}; }
};
