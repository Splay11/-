import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Solution {
    public int[] simulateTaskQueue(int[] submitTimes, int[] execTimes, int queueCapacity,
                                   int numWorkers) {
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        int discarded = 0;
        int lastFinish = 0;
        int m = numWorkers;

        int[] freeAt = new int[m + 1];
        int n = submitTimes.length;
        int[][] subs = new int[n][2];
        for (int i = 0; i < n; i++) {
            subs[i][0] = submitTimes[i];
            subs[i][1] = execTimes[i];
        }
        Arrays.sort(subs, (a, b) -> Integer.compare(a[0], b[0]));
        int si = 0;
        final int INF = Integer.MAX_VALUE / 4;

        while (true) {
            ArrayList<Integer> busy = new ArrayList<>();
            for (int i = 1; i <= m; i++) {
                if (freeAt[i] > 0) busy.add(freeAt[i]);
            }
            if (si >= n && queue.isEmpty() && busy.isEmpty()) break;

            int nextSubmit = si < n ? subs[si][0] : INF;
            int nextFree = INF;
            for (int t : busy) nextFree = Math.min(nextFree, t);
            int time = Math.min(nextSubmit, nextFree);

            for (int i = 1; i <= m; i++) {
                if (freeAt[i] > 0 && freeAt[i] <= time) freeAt[i] = 0;
            }

            lastFinish = assignWorkers(time, m, freeAt, queue, lastFinish);

            while (si < n && subs[si][0] == time) {
                int d = subs[si][1];
                if (queue.size() >= queueCapacity) {
                    queue.pollFirst();
                    discarded++;
                }
                queue.addLast(d);
                si++;
            }

            lastFinish = assignWorkers(time, m, freeAt, queue, lastFinish);
        }

        return new int[] {lastFinish, discarded};
    }

    private int assignWorkers(int time, int m, int[] freeAt, ArrayDeque<Integer> queue,
                              int lastFinish) {
        ArrayList<Integer> idle = new ArrayList<>();
        for (int i = 1; i <= m; i++) {
            if (freeAt[i] <= time) idle.add(i);
        }
        Collections.sort(idle);
        for (int wid : idle) {
            if (queue.isEmpty()) break;
            int dur = queue.pollFirst();
            int finish = time + dur;
            lastFinish = Math.max(lastFinish, finish);
            freeAt[wid] = finish;
        }
        return lastFinish;
    }
}
