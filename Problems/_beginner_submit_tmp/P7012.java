import java.util.*;

public class Solution {
    public int minAuditDays(int[] loads) {
        // 空数组无需抽查
        if (loads == null || loads.length == 0) {
            return 0;
        }
        // 计算总负载（用 long 防止溢出）
        long total = 0;
        Integer[] a = new Integer[loads.length];
        for (int i = 0; i < loads.length; i++) {
            total += loads[i];
            a[i] = loads[i];
        }
        // 降序排序：优先选大的
        Arrays.sort(a, Collections.reverseOrder());
        long s = 0;
        for (int i = 0; i < a.length; i++) {
            s += a[i];
            // 选出之和严格大于未选之和
            if (s * 2 > total) {
                return i + 1;
            }
        }
        return a.length;
    }
}
