import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

class MicQueue {
    private Map<Integer, Long> heat = new HashMap<>();
    private PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> {
        if (a[0] != b[0]) return Long.compare(b[0], a[0]);
        return Long.compare(a[1], b[1]);
    });

    public MicQueue() {}

    public boolean enroll(int songId, int h) {
        if (heat.containsKey(songId)) return false;
        heat.put(songId, (long) h);
        heap.offer(new long[] {h, songId});
        return true;
    }

    public int nextPlay() {
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            Long cur = heat.get((int) top[1]);
            if (cur != null && cur == top[0]) {
                heat.remove((int) top[1]);
                return (int) top[1];
            }
        }
        return -1;
    }

    public boolean boost(int songId, int addHeat) {
        if (!heat.containsKey(songId)) return false;
        long nh = heat.get(songId) + addHeat;
        heat.put(songId, nh);
        heap.offer(new long[] {nh, songId});
        return true;
    }

    public boolean cancel(int songId) {
        if (!heat.containsKey(songId)) return false;
        heat.remove(songId);
        return true;
    }

    public int waiting() {
        return heat.size();
    }
}
