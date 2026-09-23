import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;

class PickupDesk {
    private Deque<Integer> q = new ArrayDeque<>();
    private Set<Integer> waitingIds = new HashSet<>();

    public PickupDesk() {}

    public boolean order(int ticketId) {
        // 已经在等待队列里，重复取号失败
        if (waitingIds.contains(ticketId)) return false;
        q.addLast(ticketId);
        waitingIds.add(ticketId);
        return true;
    }

    public int serve() {
        // 队列为空返回 -1
        if (q.isEmpty()) return -1;
        int ticketId = q.pollFirst();
        // 出队后同步从等待集合中删掉
        waitingIds.remove(ticketId);
        return ticketId;
    }

    public int waiting() {
        return waitingIds.size();
    }
}
