import java.util.Scanner;

public class Main {
    // 统计无序对 (i,j) 使得 (w[i]+w[j]) % t == 0
    static long countPairs(int n, int t, long[] w) {
        long[] cnt = new long[t];
        for (int i = 0; i < n; i++) {
            cnt[(int) (w[i] % t)]++;  // 按余数分桶
        }
        long ans = 0;
        // 余数 0 只能和同类配对
        ans += cnt[0] * (cnt[0] - 1) / 2;
        // t 为偶数时，余数 t/2 也只能和同类配对
        if (t % 2 == 0) {
            long half = cnt[t / 2];
            ans += half * (half - 1) / 2;
        }
        // r 与 t-r 互补，每对余数类只乘一次，避免算重
        for (int r = 1; r < (t + 1) / 2; r++) {
            ans += cnt[r] * cnt[t - r];
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();  // 件数
        int t = sc.nextInt();  // 装载模数
        long[] w = new long[n];
        for (int i = 0; i < n; i++) {
            w[i] = sc.nextLong();  // 第 i 件重量
        }
        System.out.println(countPairs(n, t, w));
        sc.close();
    }
}
