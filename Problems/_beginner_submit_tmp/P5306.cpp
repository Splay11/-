#include <unordered_map>
#include <utility>
using namespace std;

class LeaseManager {
    int ttl;
    unordered_map<int, pair<int,int>> mp; // rid -> {node,last}
public:
    LeaseManager(int ttl): ttl(ttl) {}

    bool alive(int resourceId, int time) {
        auto it = mp.find(resourceId);
        if (it == mp.end()) return false;
        return time < (long long)it->second.second + ttl;
    }

    bool acquire(int resourceId, int nodeId, int time) {
        if (alive(resourceId, time) && mp[resourceId].first != nodeId) return false;
        mp[resourceId] = {nodeId, time};
        return true;
    }

    bool renew(int resourceId, int nodeId, int time) {
        if (!alive(resourceId, time) || mp[resourceId].first != nodeId) return false;
        mp[resourceId] = {nodeId, time};
        return true;
    }

    bool release(int resourceId, int nodeId) {
        auto it = mp.find(resourceId);
        if (it == mp.end() || it->second.first != nodeId) return false;
        mp.erase(it);
        return true;
    }

    int holder(int resourceId, int time) {
        if (!alive(resourceId, time)) return -1;
        return mp[resourceId].first;
    }

    int aliveCount(int time) {
        int cnt = 0;
        for (auto& kv : mp) if (alive(kv.first, time)) cnt++;
        return cnt;
    }
};
