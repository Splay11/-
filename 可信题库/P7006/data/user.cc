#include <unordered_map>
#include <utility>

using namespace std;

class ClusterPool {
   public:
    ClusterPool() {}

    bool addNode(int nodeId, int capacity) {
        (void)nodeId;
        (void)capacity;
        return false;
    }

    bool removeNode(int nodeId) {
        (void)nodeId;
        return false;
    }

    int submit(int jobId, int size) {
        (void)jobId;
        (void)size;
        return -1;
    }

    bool kill(int jobId) {
        (void)jobId;
        return false;
    }

    int usedOf(int nodeId) {
        (void)nodeId;
        return -1;
    }

    int freeOf(int nodeId) {
        (void)nodeId;
        return -1;
    }

    int jobNode(int jobId) {
        (void)jobId;
        return -1;
    }
};
