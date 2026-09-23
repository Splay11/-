import java.io.*;
import java.util.*;

public class Main {
    // 判断前缀和集合是否包含 T,2T,...,kT
    static boolean canSplit(Set<Long> prefSet, long T, long k) {
        for (long i = 1; i <= k; i++) {
            if (!prefSet.contains(T * i)) return false;
        }
        return true;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] sp = br.readLine().trim().split("\\s+");
        long[] a = new long[n];
        long S = 0;
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(sp[i]);
            S += a[i];
        }

        if (S == 0) {
            // 每段和为 0
            long p = 0;
            int cnt = 0;
            for (int i = 0; i < n; i++) {
                p += a[i];
                if (p == 0) cnt++;
            }
            System.out.println(cnt);
            return;
        }

        Set<Long> prefSet = new HashSet<>();
        long pref = 0;
        for (int i = 0; i < n; i++) {
            pref += a[i];
            prefSet.add(pref);
        }

        int best = 1;
        pref = 0;
        for (int i = 0; i < n - 1; i++) {
            pref += a[i];
            long T = pref;
            if (T == 0) continue;
            if (S % T != 0) continue;
            long k = S / T;
            if (k <= best) continue;
            if (canSplit(prefSet, T, k)) best = (int) k;
        }
        System.out.println(best);
    }
}
