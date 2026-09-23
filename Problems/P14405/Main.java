public class Solution {
    public int minimumLatency(int[] nums, int k) {
        int lo = 0, hi = 0;
        for (int x : nums) {
            lo = Math.max(lo, x);
            hi += x;
        }

        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canSplit(nums, k, mid))
                hi = mid;
            else
                lo = mid + 1;
        }
        return lo;
    }

    private boolean canSplit(int[] nums, int k, int limit) {
        int cnt = 1;
        long s = 0;
        for (int x : nums) {
            if (s + x > limit) {
                cnt++;
                s = 0;
            }
            s += x;
        }
        return cnt <= k;
    }
}
