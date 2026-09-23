import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.StringTokenizer;

public class Main {
    // 元素互不相同且不为 0。只从正数这边数，避免一对算两次
    static int solve(int[] nums) {
        HashSet<Integer> s = new HashSet<Integer>();
        for (int i = 0; i < nums.length; i++) {
            s.add(nums[i]);
        }
        int ans = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] > 0 && s.contains(-nums[i])) {
                ans++;
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(nums));
    }
}
