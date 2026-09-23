import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Solution {
    private static class Event implements Comparable<Event> {
        int time, pri, type, id;

        Event(int time, int pri, int type, int id) {
            this.time = time;
            this.pri = pri;
            this.type = type;
            this.id = id;
        }

        public int compareTo(Event o) {
            if (time != o.time) return Integer.compare(time, o.time);
            return Integer.compare(pri, o.pri);
        }
    }

    public int countFailedCharging(int n, int[][] cars) {
        PriorityQueue<Event> events = new PriorityQueue<>();
        for (int i = 0; i < cars.length; i++) {
            events.offer(new Event(cars[i][0], 1, 1, i));
        }

        PriorityQueue<Integer> piles = new PriorityQueue<>();
        for (int i = 0; i < n; i++) piles.offer(0);

        List<Integer> waiting = new ArrayList<>();
        int failed = 0;

        while (!events.isEmpty()) {
            int t = events.peek().time;
            List<Event> batch = new ArrayList<>();
            while (!events.isEmpty() && events.peek().time == t) {
                batch.add(events.poll());
            }
            batch.sort((a, b) -> Integer.compare(a.pri, b.pri));

            for (Event e : batch) {
                if (e.type == 0) {
                    piles.offer(t);
                } else {
                    waiting.add(e.id);
                }
            }

            while (!piles.isEmpty() && piles.peek() <= t && !waiting.isEmpty()) {
                int car = waiting.get(0);
                int at = cars[car][0], ct = cars[car][1], wt = cars[car][2];
                if (t - at > wt) {
                    waiting.remove(0);
                    failed++;
                    continue;
                }
                piles.poll();
                events.offer(new Event(t + ct, 0, 0, 0));
                waiting.remove(0);
            }
        }
        return failed;
    }
}
