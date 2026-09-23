import java.util.ArrayList;
import java.util.List;

public class Solution {
    public List<List<Integer>> selectMaxWeightPolicies(
            int n, int k, int[] weights, int[][] conflicts) {
        if (k < 0 || k > n) return new ArrayList<>();

        int[] conflictMask = new int[n];
        for (int[] e : conflicts) {
            int a = e[0] - 1;
            int b = e[1] - 1;
            conflictMask[a] |= 1 << b;
            conflictMask[b] |= 1 << a;
        }

        boolean found = false;
        int best = 0;
        List<List<Integer>> result = new ArrayList<>();

        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            if (!isIndependent(mask, conflictMask)) continue;

            int total = 0;
            List<Integer> combo = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    total += weights[i];
                    combo.add(i + 1);
                }
            }

            if (!found || total > best) {
                found = true;
                best = total;
                result.clear();
                result.add(combo);
            } else if (total == best) {
                result.add(combo);
            }
        }

        if (!found) return new ArrayList<>();
        return result;
    }

    private static boolean isIndependent(int mask, int[] conflictMask) {
        int m = mask;
        while (m != 0) {
            int lsb = m & -m;
            int i = Integer.numberOfTrailingZeros(lsb);
            if ((conflictMask[i] & mask) != 0) return false;
            m ^= lsb;
        }
        return true;
    }
}
