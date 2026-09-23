import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    // 除数越大，向上取整之和越小；超过阈值就可以提前结束
    static boolean canDivide(int[] nums, int divisor, int threshold) {
        long total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += (nums[i] + (long) divisor - 1) / divisor;
            if (total > threshold) {
                return false;
            }
        }
        return true;
    }

    // 答案具有单调性，在 [1, max(nums)] 上二分最小可行除数
    static int smallestDivisor(int[] nums, int threshold) {
        int left = 1;
        int right = nums[0];
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > right) {
                right = nums[i];
            }
        }
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (canDivide(nums, mid, threshold)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    public static void main(String[] args) throws IOException {
        // n 可达 5e4，用 BufferedReader
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int threshold = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(smallestDivisor(nums, threshold));
    }
}
