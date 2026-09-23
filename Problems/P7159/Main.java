import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 正数数组上的滑动窗口：找总和 >= target 的最短连续段
    static int solve(int[] nums, int target) {
        int n = nums.length;
        int left = 0;
        long s = 0;
        int ans = n + 1;
        for (int right = 0; right < n; right++) {
            s += nums[right];
            // 窗口和已经达标，左端能缩就缩，得到更短的合法段
            while (s >= target) {
                int length = right - left + 1;
                if (length < ans) {
                    ans = length;
                }
                s -= nums[left];
                left++;
            }
        }
        // 从未出现合法窗口
        if (ans == n + 1) {
            return 0;
        }
        return ans;
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
