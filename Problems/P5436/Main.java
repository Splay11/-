import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // 扫描线求最少卡数，以及占用等于最大值的时长之和
    static long[] minCardsAndFullLoad(int[] beg, int[] fin, int m) {
        int tot = m * 2;
        long[] time = new long[tot];
        int[] delta = new int[tot];
        for (int i = 0; i < m; i++) {
            time[i] = beg[i];
            delta[i] = 1;
            time[m + i] = fin[i];
            delta[m + i] = -1;
        }
        // 按下标间接排序：时刻升序，同时刻结束优先
        Integer[] order = new Integer[tot];
        for (int i = 0; i < tot; i++) {
            order[i] = i;
        }
        java.util.Arrays.sort(order, (a, b) -> {
            if (time[a] != time[b]) {
                return Long.compare(time[a], time[b]);
            }
            return Integer.compare(delta[a], delta[b]);
        });

        int cur = 0;
        int mx = 0;
        for (int i = 0; i < tot; i++) {
            cur += delta[order[i]];
            if (cur > mx) {
                mx = cur;
            }
        }

        cur = 0;
        long total = 0;
        boolean hasLast = false;
        long last = 0;
        int p = 0;
        while (p < tot) {
            long t = time[order[p]];
            if (hasLast && cur == mx) {
                total += t - last;
            }
            while (p < tot && time[order[p]] == t) {
                cur += delta[order[p]];
                p++;
            }
            last = t;
            hasLast = true;
        }
        return new long[] {mx, total};
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int m = Integer.parseInt(br.readLine().trim());
        int[] beg = new int[m];
        int[] fin = new int[m];
        for (int i = 0; i < m; i++) {
            String line = br.readLine().trim();
            int comma = line.indexOf(',');
            fin[i] = Integer.parseInt(line.substring(0, comma));
            beg[i] = Integer.parseInt(line.substring(comma + 1));
        }
        long[] ans = minCardsAndFullLoad(beg, fin, m);
        System.out.println(ans[0]);
        System.out.println(ans[1]);
    }
}
