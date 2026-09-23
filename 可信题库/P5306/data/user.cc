class LeaseManager {
public:
    LeaseManager(int ttl) { (void)ttl; }
    bool acquire(int resourceId, int nodeId, int time) { (void)resourceId;(void)nodeId;(void)time; return false; }
    bool renew(int resourceId, int nodeId, int time) { (void)resourceId;(void)nodeId;(void)time; return false; }
    bool release(int resourceId, int nodeId) { (void)resourceId;(void)nodeId; return false; }
    int holder(int resourceId, int time) { (void)resourceId;(void)time; return -1; }
    int aliveCount(int time) { (void)time; return 0; }
};
