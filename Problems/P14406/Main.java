import java.util.HashMap;
import java.util.HashSet;

public class Solution {
    public int countProfilePairs(int[] profiles, int diff) {
        if (diff == 0) {
            HashMap<Integer, Integer> freq = new HashMap<>();
            for (int x : profiles) freq.merge(x, 1, Integer::sum);
            int ans = 0;
            for (int c : freq.values())
                if (c >= 2) ans++;
            return ans;
        }
        HashSet<Integer> seen = new HashSet<>();
        for (int x : profiles) seen.add(x);
        int ans = 0;
        for (int v : seen) {
            long nxt = (long) v + diff;
            if (nxt >= Integer.MIN_VALUE && nxt <= Integer.MAX_VALUE && seen.contains((int) nxt))
                ans++;
        }
        return ans;
    }
}
