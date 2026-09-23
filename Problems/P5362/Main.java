import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Main {
    static int bisectRight(List<Long> a, long x) {
        // 第一个严格大于 x 的位置，即 <= x 的个数
        int l = 0, r = a.size();
        while (l < r) {
            int mid = (l + r) / 2;
            if (a.get(mid) <= x) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }
        return l;
    }

    static long minSwaps(String d) {
        // 环上把 0 挪到偶数位或奇数位；只允许循环错位
        int len = d.length();
        int m = len / 2;
        List<Integer> pos = new ArrayList<Integer>();
        for (int i = 0; i < len; i++) {
            if (d.charAt(i) == '0') {
                pos.add(i);
            }
        }
        long ans = Long.MAX_VALUE / 4;
        for (int start = 0; start <= 1; start++) {
            List<Long> a = new ArrayList<Long>();
            for (int i = 0; i < m; i++) {
                long b = (long) pos.get(i) - 2L * i - start;
                a.add(-b);
            }
            Collections.sort(a);
            long[] pref = new long[m + 1];
            for (int i = 0; i < m; i++) {
                pref[i + 1] = pref[i] + a.get(i);
            }
            for (int k = -(m - 1); k <= m - 1; k++) {
                long x = 2L * k;
                int left = bisectRight(a, x);
                long cur = x * left - pref[left] + (pref[m] - pref[left]) - x * (m - left);
                if (cur < ans) {
                    ans = cur;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        String d = sc.next();
        System.out.println(minSwaps(d));
        sc.close();
    }
}
