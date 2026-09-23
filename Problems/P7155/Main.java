import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 排列型完全背包：外层容量、内层数字，顺序不同算不同方案
    static int solve(int[] nums, int target) {
        // dp[t]：凑出 t 的有序方案数。凑出 0 视为一种空方案。
        long[] dp = new long[target + 1];
        dp[0] = 1;
        // 外层容量、内层数字：最后一个数可以是任意 x，从而把排列都算进去
        for (int t = 1; t <= target; t++) {
            for (int i = 0; i < nums.length; i++) {
                int x = nums[i];
                if (t >= x) {
                    dp[t] += dp[t - x];
                }
            }
        }
        // 凑不出时 dp[target] 仍为 0；题目保证答案在 32 位有符号整数范围内
        return (int) dp[target];
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int target = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(nums, target));
    }
}
