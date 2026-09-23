import java.util.HashMap;
import java.util.Map;

public class Solution {
    private static String normalize(String story) {
        int a = 0, b = story.length();
        while (a < b && story.charAt(a) == ' ') a++;
        while (b > a && story.charAt(b - 1) == ' ') b--;
        String s = story.substring(a, b);
        if (s.isEmpty()) return "";
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length();) {
            if (s.charAt(i) == ' ') {
                if (out.length() > 0) out.append(' ');
                while (i < s.length() && s.charAt(i) == ' ') i++;
            } else {
                out.append(s.charAt(i++));
            }
        }
        while (out.length() > 0 && out.charAt(out.length() - 1) == ' ') {
            out.setLength(out.length() - 1);
        }
        return out.toString();
    }

    public int lengthOfLongestSubstring(String story) {
        String t = normalize(story);
        if (t.isEmpty()) return 0;
        Map<Character, Integer> last = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < t.length(); right++) {
            char key = Character.toLowerCase(t.charAt(right));
            Integer prev = last.get(key);
            if (prev != null && prev >= left) left = prev + 1;
            last.put(key, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
}
