import java.util.Arrays;
import java.util.Scanner;

public class Main {
    static final int MOD = 998244353;

    static int countArrangements(int d, int[] v) {
        // 按高度排序后，从矮到高：每人对应后缀里「高度不超过自己+d」的可选人数
        // 嵌套后继集合上的哈密顿路条数等于这些人数的乘积
        int n = v.length;
        int[] a = Arrays.copyOf(v, n);
        Arrays.sort(a);
        long ans = 1;
        int j = 0;
        for (int i = 0; i < n; i++) {
            // j 右移到第一个高度大于 a[i]+d 的位置
            while (j < n && a[j] - a[i] <= d) {
                j++;
            }
            // 后缀 a[i..] 里高度仍不超过 a[i]+d 的人数
            ans = ans * (j - i) % MOD;
        }
        return (int) ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        int d = sc.nextInt();
        int[] v = new int[m];
        for (int i = 0; i < m; i++) {
            v[i] = sc.nextInt();
        }
        System.out.println(countArrangements(d, v));
        sc.close();
    }
}
