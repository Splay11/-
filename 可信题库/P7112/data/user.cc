#include <unordered_map>
#include <vector>
using namespace std;

class ShardLeaseManager {
public:
    ShardLeaseManager(int shardCount, int maxHold) {}
    bool acquire(int clientId, int shardId, int now, int ttl) { return false; }
    bool renew(int clientId, int shardId, int now, int ttl) { return false; }
    bool release(int clientId, int shardId, int now) { return false; }
    int owner(int shardId, int now) { return -1; }
    int heldCount(int clientId, int now) { return -1; }
};
