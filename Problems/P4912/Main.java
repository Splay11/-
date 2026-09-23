import java.io.*;
import java.util.*;

public class Main {
    static boolean feasible(int n, long m, long[] s, long G) {
        if (G <= 0) {
            return true;
        }
        long[] gap = new long[n - 1];
        for (int i = 0; i + 1 < n; i++) {
            gap[i] = s[i + 1] - s[i];
        }
        int totBad = 0;
        for (int i = 0; i + 1 < n; i++) {
            if (gap[i] < G) {
                totBad++;
            }
        }
        int[] prefBad = new int[n - 1];
        for (int i = 0; i + 1 < n; i++) {
            prefBad[i] = (i > 0 ? prefBad[i - 1] : 0) + (gap[i] < G ? 1 : 0);
        }
        long[] prefMax = Arrays.copyOf(gap, gap.length);
        for (int i = 1; i + 1 < n; i++) {
            prefMax[i] = Math.max(prefMax[i - 1], prefMax[i]);
        }
        long[] sufMax = Arrays.copyOf(gap, gap.length);
        for (int i = gap.length - 2; i >= 0; i--) {
            sufMax[i] = Math.max(sufMax[i], sufMax[i + 1]);
        }
        int[] prefLarge = new int[n - 1];
        Arrays.fill(prefLarge, -1);
        for (int i = 0; i + 1 < n; i++) {
            if (gap[i] < G) {
                prefLarge[i] = Math.max((i > 0 ? prefLarge[i - 1] : -1), i);
            } else {
                prefLarge[i] = (i > 0 ? prefLarge[i - 1] : -1);
            }
        }
        int[] sufSmall = new int[n - 1];
        Arrays.fill(sufSmall, Integer.MAX_VALUE);
        for (int i = gap.length - 1; i >= 0; i--) {
            if (gap[i] < G) {
                int nxt = (i + 1 < sufSmall.length ? sufSmall[i + 1] : Integer.MAX_VALUE);
                sufSmall[i] = Math.min(nxt, i);
            } else {
                sufSmall[i] = (i + 1 < sufSmall.length ? sufSmall[i + 1] : Integer.MAX_VALUE);
            }
        }

        for (int k = 0; k < n; k++) {
            int bl = (k >= 2 ? prefBad[k - 2] : 0);
            int br = (k >= n - 1 ? 0 : totBad - prefBad[k]);
            int bb = 0;
            if (k > 0 && k < n - 1 && s[k + 1] - s[k - 1] < G) {
                bb = 1;
            }
            int tb = bl + br + bb;
            if (tb > 1) {
                continue;
            }
            long firstT = (k != 0 ? s[0] : s[1]);
            long lastT = (k != n - 1 ? s[n - 1] : s[n - 2]);
            if (tb == 0) {
                if (firstT >= G + 1) {
                    return true;
                }
                if (lastT <= m - G) {
                    return true;
                }
                long mx = -1;
                if (k >= 2) {
                    mx = Math.max(mx, prefMax[k - 2]);
                }
                if (k + 1 <= n - 2) {
                    mx = Math.max(mx, sufMax[k + 1]);
                }
                if (k > 0 && k < n - 1) {
                    mx = Math.max(mx, s[k + 1] - s[k - 1]);
                }
                if (mx >= 2 * G) {
                    return true;
                }
                continue;
            }
            long u = 0, v = 0;
            boolean ok = false;
            if (bb == 1 && bl == 0 && br == 0) {
                u = s[k - 1];
                v = s[k + 1];
                ok = true;
            } else if (bl == 1 && br == 0 && bb == 0) {
                int idx = prefLarge[k - 2];
                u = s[idx];
                v = s[idx + 1];
                ok = true;
            } else if (br == 1 && bl == 0 && bb == 0) {
                int idx = sufSmall[k + 1];
                if (idx == Integer.MAX_VALUE) {
                    continue;
                }
                u = s[idx];
                v = s[idx + 1];
                ok = true;
            }
            if (!ok) {
                continue;
            }
            if (v - u < 2 * G) {
                continue;
            }
            long L = Math.max(1L, u + G);
            long R = Math.min(m, v - G);
            if (L <= R) {
                return true;
            }
        }
        return false;
    }

    static long solveOne(int n, long m, long[] a) {
        Arrays.sort(a);
        long lo = 0, hi = m;
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            if (feasible(n, m, a, mid)) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        return lo;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int T = Integer.parseInt(st.nextToken());
        StringBuilder sb = new StringBuilder();
        for (int tc = 0; tc < T; tc++) {
            st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            long m = Long.parseLong(st.nextToken());
            long[] a = new long[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                a[i] = Long.parseLong(st.nextToken());
            }
            sb.append(solveOne(n, m, a)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
