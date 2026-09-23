import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // dp[i] 表示前 i 个字符有多少种解码方法
    static int solve(String s) {
        int n = s.length();
        int[] dp = new int[n + 1];
        dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            // 单独解码 s[i-1]
            if (s.charAt(i - 1) != '0') {
                dp[i] += dp[i - 1];
            }
            if (i >= 2) {
                // 把最后两位当成一个字母，必须是 10..26
                int x = (s.charAt(i - 2) - '0') * 10 + (s.charAt(i - 1) - '0');
                if (x >= 10 && x <= 26) {
                    dp[i] += dp[i - 2];
                }
            }
        }
        return dp[n];
    }

    public static void main(String[] args) throws IOException {
        // 一整行数字串
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
