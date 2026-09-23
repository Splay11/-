class ShardLeaseManager {
    public ShardLeaseManager(int shardCount, int maxHold) {}

    public boolean acquire(int clientId, int shardId, int now, int ttl) {
        return false;
    }

    public boolean renew(int clientId, int shardId, int now, int ttl) {
        return false;
    }

    public boolean release(int clientId, int shardId, int now) {
        return false;
    }

    public int owner(int shardId, int now) {
        return -1;
    }

    public int heldCount(int clientId, int now) {
        return -1;
    }
}

public class Solution {}
