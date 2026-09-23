import java.util.Scanner;

public class Main {
    static final long MOD = 1000000007L;

    // 计算 H(d)=sum (i mod d)*v[i] （d=1..n），答案对 MOD 取模
    static long[] phaseContrib(int n, long[] v) {
        // n=1 时倍数循环不进入，H(1)=0，与 0 mod 1 = 0 一致
        // 后缀和：suf[i] = v[i]+...+v[n-1]（已取模）
        long[] suf = new long[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            suf[i] = suf[i + 1] + v[i];
            if (suf[i] >= MOD) {
                suf[i] -= MOD;
            }
        }
        // S = sum i*v[i]；由 i mod d = i - d*floor(i/d) 得 H(d)=S-d*g(d)
        long S = 0;
        for (int i = 0; i < n; i++) {
            S = (S + (long) i % MOD * (v[i] % MOD)) % MOD;
        }
        long[] ans = new long[n];
        for (int d = 1; d <= n; d++) {
            long g = 0;
            // 枚举 m*d < n 的倍数，调和级数合计 O(n log n)
            for (int md = d; md < n; md += d) {
                g += suf[md];
                if (g >= MOD) {
                    g -= MOD;
                }
            }
            ans[d - 1] = (S - (long) d % MOD * g % MOD + MOD) % MOD;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();  // 彩灯盏数
        long[] v = new long[n];
        for (int i = 0; i < n; i++) {
            v[i] = sc.nextLong();  // 第 i 盏标定亮度
        }
        long[] ans = phaseContrib(n, v);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans[i]);
        }
        System.out.println(sb.toString());
        sc.close();
    }
}
