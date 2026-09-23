import java.util.*;

class Solution {
    public List<List<Integer>> countKeys(String s) {
        Map<Character, Integer> cnt = new HashMap<>();
        int i = 0, n = s.length();

        while (i < n) {
            if (i + 1 < n && s.charAt(i) == 'u' && s.charAt(i + 1) == 'u') {
                cnt.put('j', cnt.getOrDefault('j', 0) + 1);
                i += 2;
            } else if (i + 1 < n && s.charAt(i) == 't' && s.charAt(i + 1) == 't') {
                cnt.put('b', cnt.getOrDefault('b', 0) + 1);
                i += 2;
            } else {
                char c = s.charAt(i);
                cnt.put(c, cnt.getOrDefault(c, 0) + 1);
                i++;
            }
        }

        List<Character> keys = new ArrayList<>(cnt.keySet());
        Collections.sort(keys, (a, b) -> {
            int ca = cnt.get(a), cb = cnt.get(b);
            if (ca != cb) return cb - ca;
            return a - b;
        });

        List<List<Integer>> ans = new ArrayList<>();
        for (char c : keys) {
            List<Integer> pair = new ArrayList<>();
            pair.add(encode(c));
            pair.add(cnt.get(c));
            ans.add(pair);
        }
        return ans;
    }

    private int encode(char c) {
        if (c >= '0' && c <= '9') return c - '0';
        return c - 'a' + 10;
    }
}
