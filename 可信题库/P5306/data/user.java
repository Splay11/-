public class LeaseManager {
    public LeaseManager(int ttl) {}
    public boolean acquire(int resourceId, int nodeId, int time) { return false; }
    public boolean renew(int resourceId, int nodeId, int time) { return false; }
    public boolean release(int resourceId, int nodeId) { return false; }
    public int holder(int resourceId, int time) { return -1; }
    public int aliveCount(int time) { return 0; }
}
