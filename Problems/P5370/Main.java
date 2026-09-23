import java.util.Scanner;

public class Main {
    static long minRange(long[] v) {
        // 枚举左右两半的分界，两半内部再各切一刀
        // 正数前缀和严格递增：半段内最优切点随边界右移只向右走
        int n = v.length;
        long[] s = new long[n + 1];
        for (int t = 0; t < n; t++) {
            s[t + 1] = s[t] + v[t];
        }
        long total = s[n];
        long ans = total;
        int i = 1;
        int k = 3;
        // j 是第二段结尾下标（第 1..j 个为左半，至少 2 个，右边也至少 2 个）
        for (int j = 2; j <= n - 2; j++) {
            // 左半切点 i∈[1,j-1]，让两段和尽量接近 s[j]/2
            if (i > j - 1) {
                i = j - 1;
            }
            while (i + 1 <= j - 1 && Math.abs(2 * s[i + 1] - s[j]) <= Math.abs(2 * s[i] - s[j])) {
                i++;
            }
            // 右半切点 k∈[j+1,n-1]，让两段和尽量接近剩余一半
            if (k <= j) {
                k = j + 1;
            }
            while (k + 1 <= n - 1 && Math.abs(2 * (s[k + 1] - s[j]) - (total - s[j])) <= Math.abs(2 * (s[k] - s[j]) - (total - s[j]))) {
                k++;
            }
            long a = s[i];
            long b = s[j] - s[i];
            long c = s[k] - s[j];
            long d = total - s[k];
            long mx = a;
            if (b > mx) {
                mx = b;
            }
            if (c > mx) {
                mx = c;
            }
            if (d > mx) {
                mx = d;
            }
            long mn = a;
            if (b < mn) {
                mn = b;
            }
            if (c < mn) {
                mn = c;
            }
            if (d < mn) {
                mn = d;
            }
            if (mx - mn < ans) {
                ans = mx - mn;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        long[] v = new long[m];
        for (int t = 0; t < m; t++) {
            v[t] = sc.nextLong();
        }
        System.out.println(minRange(v));
        sc.close();
    }
}
