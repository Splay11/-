import java.util.*;
import java.io.*;

public class Main {
    static long solveIntervalScheduling(int n, long[][] intervals) {
        Arrays.sort(intervals, (a, b) -> {
            if (a[1] != b[1]) {
                return Long.compare(a[1], b[1]);
            }
            return Long.compare(a[0], b[0]);
        });
        long lastEnd = Long.MIN_VALUE / 4;
        int cnt = 0;
        for (long[] it : intervals) {
            long s = it[0];
            long e = it[1];
            if (s > lastEnd) {
                cnt++;
                lastEnd = e;
            }
        }
        return cnt;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] parts = br.readLine().trim().split("\\s+");
        long[][] intervals = new long[n][2];
        for (int i = 0; i < n; i++) {
            intervals[i][0] = Long.parseLong(parts[2 * i]);
            intervals[i][1] = Long.parseLong(parts[2 * i + 1]);
        }
        System.out.println(solveIntervalScheduling(n, intervals));
    }
}
