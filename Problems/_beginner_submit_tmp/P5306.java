import java.util.*;

public class LeaseManager {
    private final int ttl;
    private final Map<Integer, int[]> mp; // rid -> {node, last}

    public LeaseManager(int ttl) {
        this.ttl = ttl;
        this.mp = new HashMap<>();
    }

    private boolean alive(int resourceId, int time) {
        int[] e = mp.get(resourceId);
        if (e == null) return false;
        // 注意用 long 防 last+ttl 溢出
        return time < (long) e[1] + ttl;
    }

    public boolean acquire(int resourceId, int nodeId, int time) {
        if (alive(resourceId, time) && mp.get(resourceId)[0] != nodeId) return false;
        mp.put(resourceId, new int[]{nodeId, time});
        return true;
    }

    public boolean renew(int resourceId, int nodeId, int time) {
        if (!alive(resourceId, time) || mp.get(resourceId)[0] != nodeId) return false;
        mp.put(resourceId, new int[]{nodeId, time});
        return true;
    }

    public boolean release(int resourceId, int nodeId) {
        int[] e = mp.get(resourceId);
        if (e == null || e[0] != nodeId) return false;
        mp.remove(resourceId);
        return true;
    }

    public int holder(int resourceId, int time) {
        if (!alive(resourceId, time)) return -1;
        return mp.get(resourceId)[0];
    }

    public int aliveCount(int time) {
        int cnt = 0;
        for (int rid : mp.keySet()) if (alive(rid, time)) cnt++;
        return cnt;
    }
}
