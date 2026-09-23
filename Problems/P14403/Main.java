import java.util.ArrayList;
import java.util.HashSet;

public class Solution {
    private static boolean isDelim(char c) {
        return Character.isWhitespace(c) || c == ',' || c == '.' || c == '!' ||
                c == '?' || c == ';' || c == ':';
    }

    private static ArrayList<String> tokenize(String log) {
        ArrayList<String> words = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 0; i < log.length(); i++) {
            char c = log.charAt(i);
            if (isDelim(c)) {
                if (cur.length() > 0) {
                    words.add(cur.toString().toLowerCase());
                    cur.setLength(0);
                }
            } else {
                cur.append(c);
            }
        }
        if (cur.length() > 0) words.add(cur.toString().toLowerCase());
        return words;
    }

    public int[] analyzeLogKeywords(String[] logs, String[] keywords) {
        int m = keywords.length;
        String[] kws = new String[m];
        for (int i = 0; i < m; i++) kws[i] = keywords[i].toLowerCase();
        ArrayList<ArrayList<String>> tokenized = new ArrayList<>();
        for (String log : logs) tokenized.add(tokenize(log));
        int[] counts = new int[m];
        for (ArrayList<String> words : tokenized) {
            for (int ki = 0; ki < m; ki++) {
                for (String w : words) {
                    if (w.equals(kws[ki])) counts[ki]++;
                }
            }
        }
        ArrayList<boolean[]> present = new ArrayList<>();
        for (ArrayList<String> words : tokenized) {
            HashSet<String> wordSet = new HashSet<>(words);
            boolean[] row = new boolean[m];
            for (int ki = 0; ki < m; ki++) row[ki] = wordSet.contains(kws[ki]);
            present.add(row);
        }
        ArrayList<Integer> pairs = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            for (int j = i + 1; j < m; j++) {
                int co = 0;
                for (boolean[] row : present) {
                    if (row[i] && row[j]) co++;
                }
                if (co >= 2) {
                    pairs.add(i);
                    pairs.add(j);
                }
            }
        }
        int[] ans = new int[m + pairs.size()];
        System.arraycopy(counts, 0, ans, 0, m);
        for (int i = 0; i < pairs.size(); i++) ans[m + i] = pairs.get(i);
        return ans;
    }
}
