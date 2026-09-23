#include <queue>
#include <unordered_set>

using namespace std;

class PickupDesk {
    queue<int> q;
    unordered_set<int> waitingIds;

public:
    PickupDesk() {}

    bool order(int ticketId) {
        // 已经在等待队列里，判重失败
        if (waitingIds.count(ticketId)) return false;
        q.push(ticketId);
        waitingIds.insert(ticketId);
        return true;
    }

    int serve() {
        // 队列为空返回 -1
        if (q.empty()) return -1;
        int ticketId = q.front();
        q.pop();
        // 出队后同步从等待集合中删掉
        waitingIds.erase(ticketId);
        return ticketId;
    }

    int waiting() { return (int)waitingIds.size(); }
};
