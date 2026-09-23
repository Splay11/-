#include <queue>
#include <unordered_map>
#include <utility>
using namespace std;

class MicQueue {
    unordered_map<int, long long> heat;
    priority_queue<pair<long long, int>> heap;

public:
    MicQueue() {}

    bool enroll(int songId, int h) {
        if (heat.count(songId)) return false;
        heat[songId] = h;
        heap.push({(long long)h, -songId});
        return true;
    }

    int nextPlay() {
        while (!heap.empty()) {
            pair<long long, int> top = heap.top();
            heap.pop();
            long long h = top.first;
            int sid = -top.second;
            auto it = heat.find(sid);
            if (it != heat.end() && it->second == h) {
                heat.erase(it);
                return sid;
            }
        }
        return -1;
    }

    bool boost(int songId, int addHeat) {
        if (!heat.count(songId)) return false;
        heat[songId] += addHeat;
        heap.push({heat[songId], -songId});
        return true;
    }

    bool cancel(int songId) {
        if (!heat.count(songId)) return false;
        heat.erase(songId);
        return true;
    }

    int waiting() { return (int)heat.size(); }
};
