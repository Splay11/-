import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int S = Integer.parseInt(br.readLine().trim());
        // dp[s]：当前已打若干枪得到总分 s 的方案数
        long[] dp = new long[S + 1];
        dp[0] = 1;
        for (int shot = 0; shot < 10; shot++) {
            long[] ndp = new long[S + 1];
            for (int s = 0; s <= S; s++) {
                if (dp[s] == 0) continue;
                for (int v = 0; v <= 10; v++) {
                    if (s + v <= S) ndp[s + v] += dp[s];
                }
            }
            dp = ndp;
        }
        System.out.println(dp[S]);
    }
}
