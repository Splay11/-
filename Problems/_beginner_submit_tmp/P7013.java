import java.util.*;

public class Solution {
    public int countNeedUpgrade(int[] versions, int baseline) {
        // 复制后排序，便于二分
        int n = versions.length;
        int[] a = Arrays.copyOf(versions, n);
        Arrays.sort(a);
        // lower_bound：第一个 >= baseline 的下标
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (a[mid] < baseline) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        // 从 lo 到末尾均需巡检
        return n - lo;
    }
}
