import java.util.*;

class ShardLeaseManager {
    private final int shardCount;
    private final int maxHold;
    private final Map<Integer, int[]> lease = new HashMap<>(); // shard -> {client, expire}
    private final Map<Integer, Map<Integer, Integer>> byClient = new HashMap<>();

    public ShardLeaseManager(int shardCount, int maxHold) {
        this.shardCount = shardCount;
        this.maxHold = maxHold;
    }

    private boolean validShard(int shardId) {
        return shardId >= 0 && shardId < shardCount;
    }

    private void expireShard(int shardId, int now) {
        int[] cur = lease.get(shardId);
        if (cur == null) return;
        if (now >= cur[1]) {
            lease.remove(shardId);
            Map<Integer, Integer> mp = byClient.get(cur[0]);
            if (mp != null) {
                mp.remove(shardId);
                if (mp.isEmpty()) byClient.remove(cur[0]);
            }
        }
    }

    private void expireClient(int clientId, int now) {
        Map<Integer, Integer> mp = byClient.get(clientId);
        if (mp == null) return;
        List<Integer> dead = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : mp.entrySet()) {
            if (now >= e.getValue()) dead.add(e.getKey());
        }
        for (int sid : dead) expireShard(sid, now);
    }

    private int activeCount(int clientId, int now) {
        expireClient(clientId, now);
        Map<Integer, Integer> mp = byClient.get(clientId);
        return mp == null ? 0 : mp.size();
    }

    public boolean acquire(int clientId, int shardId, int now, int ttl) {
        if (clientId <= 0 || ttl <= 0 || !validShard(shardId)) return false;
        expireShard(shardId, now);
        expireClient(clientId, now);
        if (lease.containsKey(shardId)) return false;
        if (activeCount(clientId, now) >= maxHold) return false;
        int exp = now + ttl;
        lease.put(shardId, new int[]{clientId, exp});
        byClient.computeIfAbsent(clientId, k -> new HashMap<>()).put(shardId, exp);
        return true;
    }

    public boolean renew(int clientId, int shardId, int now, int ttl) {
        if (clientId <= 0 || ttl <= 0 || !validShard(shardId)) return false;
        expireShard(shardId, now);
        if (!lease.containsKey(shardId)) return false;
        if (lease.get(shardId)[0] != clientId) return false;
        int exp = now + ttl;
        lease.put(shardId, new int[]{clientId, exp});
        byClient.computeIfAbsent(clientId, k -> new HashMap<>()).put(shardId, exp);
        return true;
    }

    public boolean release(int clientId, int shardId, int now) {
        if (clientId <= 0 || !validShard(shardId)) return false;
        expireShard(shardId, now);
        if (!lease.containsKey(shardId)) return false;
        if (lease.get(shardId)[0] != clientId) return false;
        lease.remove(shardId);
        Map<Integer, Integer> mp = byClient.get(clientId);
        if (mp != null) {
            mp.remove(shardId);
            if (mp.isEmpty()) byClient.remove(clientId);
        }
        return true;
    }

    public int owner(int shardId, int now) {
        if (!validShard(shardId)) return -1;
        expireShard(shardId, now);
        int[] cur = lease.get(shardId);
        return cur == null ? -1 : cur[0];
    }

    public int heldCount(int clientId, int now) {
        if (clientId <= 0) return -1;
        return activeCount(clientId, now);
    }
}
