import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    static final int OFFSET = 10000;

    // 值域只有 -10000 到 10000，计数后从大到小数第 k 个
    static int solve(int[] nums, int k) {
        int[] cnt = new int[2 * OFFSET + 1];
        for (int i = 0; i < nums.length; i++) {
            cnt[nums[i] + OFFSET]++;
        }
        int need = k;
        // 从大到小扫，减掉该值出现次数
        for (int v = OFFSET; v >= -OFFSET; v--) {
            need -= cnt[v + OFFSET];
            if (need <= 0) {
                return v;
            }
        }
        return 0;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(nums, k));
    }
}
