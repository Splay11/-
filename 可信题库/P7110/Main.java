import java.util.*;

class Solution {
    public int minPassDays(int[] slots, int[] prep) {
        int n = slots.length, m = prep.length;
        if (!ok(slots, prep, n)) return -1;
        int lo = 1, hi = n;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (ok(slots, prep, mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    private boolean ok(int[] slots, int[] prep, int days) {
        int m = prep.length;
        int[] last = new int[m + 1];
        Arrays.fill(last, -1);
        for (int i = 0; i < days; i++) {
            int t = slots[i];
            if (t > 0) last[t] = i;
        }
        for (int t = 1; t <= m; t++) if (last[t] < 0) return false;
        Integer[] order = new Integer[m];
        for (int t = 1; t <= m; t++) order[t - 1] = t;
        Arrays.sort(order, Comparator.comparingInt(a -> last[a]));
        int free = 0, j = 0;
        for (int day = 0; day < days; day++) {
            if (j < m && last[order[j]] == day) {
                int need = prep[order[j] - 1];
                if (free < need) return false;
                free -= need;
                j++;
            } else {
                free++;
            }
        }
        return j == m;
    }
}
