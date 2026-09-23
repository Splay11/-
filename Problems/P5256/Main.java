import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static class Job {
        int s, e;
        long v;
        Job(int s, int e, long v) {
            this.s = s;
            this.e = e;
            this.v = v;
        }
    }

    static int upperBound(int[] a, int to, int x) {
        int l = 0, r = to;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (a[mid] <= x) l = mid + 1;
            else r = mid;
        }
        return l;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Job[] jobs = new Job[n];
        for (int i = 0; i < n; ++i) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int s = Integer.parseInt(st.nextToken());
            int e = Integer.parseInt(st.nextToken());
            long v = Long.parseLong(st.nextToken());
            jobs[i] = new Job(s, e, v);
        }
        Arrays.sort(jobs, (a, b) -> Integer.compare(a.e, b.e));
        int[] ends = new int[n];
        for (int i = 0; i < n; ++i) ends[i] = jobs[i].e;
        long[] dp = new long[n + 1];
        for (int i = 1; i <= n; ++i) {
            int k = upperBound(ends, i - 1, jobs[i - 1].s);
            long take = dp[k] + jobs[i - 1].v;
            dp[i] = Math.max(dp[i - 1], take);
        }
        System.out.println(dp[n]);
    }
}
