import java.util.*;

class Solution {
    public int minShareOps(int[] pieces) {
        int n = pieces.length;
        if (n < 2) return 0;
        int mx = 0;
        for (int v : pieces) mx = Math.max(mx, v);
        mx += 1;
        int[] spf = new int[mx + 1];
        for (int i = 0; i <= mx; i++) spf[i] = i;
        for (int i = 2; (long) i * i <= mx; i++) {
            if (spf[i] == i) {
                for (int j = i * i; j <= mx; j += i) {
                    if (spf[j] == j) spf[j] = i;
                }
            }
        }
        List<Set<Integer>> facs = new ArrayList<>();
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int v : pieces) {
            Set<Integer> s = new HashSet<>();
            int x = v;
            while (x > 1) {
                int p = spf[x];
                s.add(p);
                while (x % p == 0) x /= p;
            }
            facs.add(s);
            for (int p : s) cnt.put(p, cnt.getOrDefault(p, 0) + 1);
        }
        for (int c : cnt.values()) {
            if (c >= 2) return 0;
        }
        for (int i = 0; i < n; i++) {
            int x = pieces[i] + 1;
            Set<Integer> s = new HashSet<>();
            while (x > 1) {
                int p = spf[x];
                s.add(p);
                while (x % p == 0) x /= p;
            }
            for (int p : s) {
                if (facs.get(i).contains(p)) {
                    if (cnt.getOrDefault(p, 0) >= 2) return 1;
                } else if (cnt.getOrDefault(p, 0) >= 1) {
                    return 1;
                }
            }
        }
        return 2;
    }
}
