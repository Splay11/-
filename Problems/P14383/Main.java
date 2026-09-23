import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    public int countValidPlans(int[] timestamps, int minInterval) {
        int[] ts = timestamps.clone();
        Arrays.sort(ts);
        int n = ts.length;
        int ans = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            List<Integer> picked = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    picked.add(ts[i]);
                }
            }
            for (int i = 0; i < picked.size(); i++) {
                for (int j = i + 1; j < picked.size(); j++) {
                    if (picked.get(j) - picked.get(i) < minInterval) {
                        ok = false;
                        break;
                    }
                }
                if (!ok) {
                    break;
                }
            }
            if (ok) {
                ans++;
            }
        }
        return ans;
    }
}
