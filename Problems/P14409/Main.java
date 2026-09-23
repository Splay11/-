import java.util.Arrays;

public class Solution {
    public long minimizeRangeSum(int n, int[] nums) {
        int[] a = Arrays.copyOf(nums, n);
        Arrays.sort(a);
        if (n == 2) return 0;
        long ans = (long) a[n - 1] - a[0];
        for (int i = 0; i < n - 1; i++) {
            long cost = (long) (a[i] - a[0]) + (a[n - 1] - a[i + 1]);
            if (cost < ans) ans = cost;
        }
        return ans;
    }
}
