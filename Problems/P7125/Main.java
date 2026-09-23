import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // Boyer-Moore 投票：抵消不同元素后，剩下的一定是多数元素（题目保证存在）
    static int majorityElement(int[] nums) {
        int cand = 0;
        int cnt = 0;
        for (int x : nums) {
            // 当前没有候选人，把这个数立为候选人
            if (cnt == 0) {
                cand = x;
                cnt = 1;
            } else if (x == cand) {
                // 碰到候选人，票数加一
                cnt++;
            } else {
                // 碰到其他数，互相抵消一票
                cnt--;
            }
        }
        // 题目保证多数元素一定存在，抵消结束后候选人就是答案
        return cand;
    }

    public static void main(String[] args) throws IOException {
        // n 最大 5e4，用 BufferedReader 读入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(majorityElement(nums));
    }
}
