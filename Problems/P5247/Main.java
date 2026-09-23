import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Main {
    static List<List<Long>> enumSums(long[] arr) {
        int n = arr.length;
        List<List<Long>> byCnt = new ArrayList<List<Long>>();
        for (int i = 0; i <= n; i++) {
            byCnt.add(new ArrayList<Long>());
        }
        for (int mask = 0; mask < (1 << n); mask++) {
            long s = 0;
            int c = 0;
            for (int i = 0; i < n; i++) {
                if (((mask >> i) & 1) == 1) {
                    s += arr[i];
                    c++;
                }
            }
            byCnt.get(c).add(s);
        }
        for (int c = 0; c <= n; c++) {
            Collections.sort(byCnt.get(c));
        }
        return byCnt;
    }

    static long minDiff(long[] vals) {
        int n = vals.length;
        int half = n / 2;
        long tot = 0;
        for (int i = 0; i < n; i++) {
            tot += vals[i];
        }
        long[] left = new long[half];
        long[] right = new long[n - half];
        for (int i = 0; i < half; i++) {
            left[i] = vals[i];
        }
        for (int i = half; i < n; i++) {
            right[i - half] = vals[i];
        }
        List<List<Long>> sl = enumSums(left);
        List<List<Long>> sr = enumSums(right);
        long best = tot;
        for (int k = 0; k <= half; k++) {
            List<Long> A = sl.get(k);
            List<Long> B = sr.get(half - k);
            if (A.isEmpty() || B.isEmpty()) {
                continue;
            }
            for (int p = 0; p < A.size(); p++) {
                long x = A.get(p);
                long t = tot / 2 - x;
                int i = Collections.binarySearch(B, t);
                if (i < 0) {
                    i = -i - 1;
                }
                for (int j = i - 1; j <= i + 1; j++) {
                    if (j >= 0 && j < B.size()) {
                        long s = x + B.get(j);
                        long d = tot - 2 * s;
                        if (d < 0) {
                            d = -d;
                        }
                        if (d < best) {
                            best = d;
                        }
                    }
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        for (int t = 0; t < q; t++) {
            int n = sc.nextInt();
            long[] vals = new long[n];
            for (int i = 0; i < n; i++) {
                vals[i] = sc.nextLong();
            }
            System.out.println(minDiff(vals));
        }
        sc.close();
    }
}
