import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {
    static final int MOD = 1000000007;
    static final int MAXN = 200000;
    // f1/f2/f3：长度为 i、末尾恰好连续 1/2/3 个相同字母的方案数
    static int[] f1 = new int[MAXN + 1];
    static int[] f2 = new int[MAXN + 1];
    static int[] f3 = new int[MAXN + 1];
    static int[] ans = new int[MAXN + 1];

    static void precompute() {
        // 长度为 1：26 种字母，末尾连续段长度只能是 1
        f1[1] = 26;
        ans[1] = 26;
        for (int i = 2; i <= MAXN; i++) {
            // 换一个与末尾不同的字母，连续段变成 1，有 25 种选择
            f1[i] = (int) (((f1[i - 1] + (long) f2[i - 1] + f3[i - 1]) % MOD) * 25 % MOD);
            // 再重复一次末尾字母：只能接在「恰好 1 个」后面
            f2[i] = f1[i - 1];
            // 再重复一次：只能接在「恰好 2 个」后面
            f3[i] = f2[i - 1];
            ans[i] = (int) ((f1[i] + (long) f2[i] + f3[i]) % MOD);
        }
    }

    static int countStr(int m) {
        return ans[m];
    }

    public static void main(String[] args) throws Exception {
        precompute();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(System.out);
        int q = Integer.parseInt(br.readLine().trim());
        for (int t = 0; t < q; t++) {
            int m = Integer.parseInt(br.readLine().trim());
            out.println(countStr(m));
        }
        out.flush();
    }
}
