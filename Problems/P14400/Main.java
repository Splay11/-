import java.util.HashMap;

public class Solution {
    public String processChunks(String s, int n) {
        StringBuilder res = new StringBuilder();
        for (int i = 0; i < s.length(); i += n) {
            int end = Math.min(i + n, s.length());
            String chunk = s.substring(i, end);
            HashMap<Character, Integer> last = new HashMap<>();
            for (int j = 0; j < chunk.length(); j++) last.put(chunk.charAt(j), j);
            for (int j = 0; j < chunk.length(); j++)
                if (last.get(chunk.charAt(j)) == j) res.append(chunk.charAt(j));
        }
        return res.toString();
    }
}
