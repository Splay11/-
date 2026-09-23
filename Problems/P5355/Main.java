import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

public class Main {
    static final long INF = 1000000000000000000L;

    static class Fenwick {
        int n;
        long[] a0, a1;

        Fenwick(int n_) {
            n = n_;
            a0 = new long[n + 2];
            a1 = new long[n + 2];
            for (int i = 0; i < n + 2; i++) {
                a0[i] = INF;
                a1[i] = 0;
            }
        }

        static int cmp(long x0, long x1, long y0, long y1) {
            if (x0 != y0) {
                return x0 < y0 ? -1 : 1;
            }
            if (x1 != y1) {
                return x1 < y1 ? -1 : 1;
            }
            return 0;
        }

        void upd(int i, long v0, long v1) {
            // 单点与 (v0,v1) 取更小
            while (i <= n) {
                if (cmp(v0, v1, a0[i], a1[i]) < 0) {
                    a0[i] = v0;
                    a1[i] = v1;
                }
                i += i & -i;
            }
        }

        long[] qry(int i) {
            // 前缀 1..i 的最小值
            long r0 = INF, r1 = 0;
            while (i > 0) {
                if (cmp(a0[i], a1[i], r0, r1) < 0) {
                    r0 = a0[i];
                    r1 = a1[i];
                }
                i -= i & -i;
            }
            return new long[] {r0, r1};
        }
    }

    static int lowerBound(List<Long> a, long x) {
        int l = 0, r = a.size();
        while (l < r) {
            int mid = (l + r) / 2;
            if (a.get(mid) >= x) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }

    static int upperBound(List<Long> a, long x) {
        int l = 0, r = a.size();
        while (l < r) {
            int mid = (l + r) / 2;
            if (a.get(mid) > x) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }

    static long minOps(long[] h) {
        // 把数组分成尽量多段、段和单调不减；答案 = 长度 - 段数
        int m = h.length;
        long[] pre = new long[m + 1];
        for (int i = 0; i < m; i++) {
            pre[i + 1] = pre[i] + h[i];
        }
        HashSet<Long> set = new HashSet<Long>();
        for (int i = 0; i <= m; i++) {
            set.add(pre[i]);
        }
        List<Long> uniq = new ArrayList<Long>(set);
        Collections.sort(uniq);
        Fenwick fw = new Fenwick(uniq.size() + 2);
        long[] last = new long[m + 1];
        long[] dp = new long[m + 1];
        fw.upd(lowerBound(uniq, 0L) + 1, 0L, 0L);
        for (int i = 1; i <= m; i++) {
            long[] best = fw.qry(upperBound(uniq, pre[i]));
            dp[i] = (i - 1) + best[0];
            long pj = -best[1];
            last[i] = pre[i] - pj;
            long key = last[i] + pre[i];
            fw.upd(lowerBound(uniq, key) + 1, dp[i] - i, -pre[i]);
        }
        return dp[m];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        for (int t = 0; t < q; t++) {
            int m = sc.nextInt();
            long[] h = new long[m];
            for (int i = 0; i < m; i++) {
                h[i] = sc.nextLong();
            }
            System.out.println(minOps(h));
        }
        sc.close();
    }
}
