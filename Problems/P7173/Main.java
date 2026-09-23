import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 全体异或得到 a^b，用最低的 1 把两个落单数分到两堆
    static int[] solve(int[] nums) {
        int xorAll = 0;
        for (int i = 0; i < nums.length; i++) {
            xorAll ^= nums[i];
        }
        int bit = xorAll & -xorAll;
        int a = 0;
        int b = 0;
        for (int i = 0; i < nums.length; i++) {
            if ((nums[i] & bit) != 0) {
                a ^= nums[i];
            } else {
                b ^= nums[i];
            }
        }
        if (a > b) {
            int t = a;
            a = b;
            b = t;
        }
        return new int[] {a, b};
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        int[] ans = solve(nums);
        System.out.println(ans[0] + " " + ans[1]);
    }
}
