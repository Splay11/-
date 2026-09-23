import java.io.*;
import java.util.*;

public class Main {
    private static int findTopLevelComma(String s) {
        int bracket = 0;
        boolean inString = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                inString = !inString;
            } else if (!inString) {
                if (c == '[') bracket++;
                else if (c == ']') bracket--;
                else if (c == ',' && bracket == 0) return i;
            }
        }
        return -1;
    }

    private static List<List<String>> parseMatches(String s) {
        List<List<String>> res = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            if (s.charAt(i) == '[') {
                i++;  // 跳过 [
                List<String> match = new ArrayList<>();
                StringBuilder cur = new StringBuilder();
                boolean inStr = false;
                while (i < s.length() && s.charAt(i) != ']') {
                    char c = s.charAt(i);
                    if (c == '"') {
                        if (inStr) {
                            match.add(cur.toString());
                            cur.setLength(0);
                        }
                        inStr = !inStr;
                    } else if (inStr) {
                        cur.append(c);
                    }
                    i++;
                }
                if (!match.isEmpty()) {
                    res.add(match);
                }
                i++;  // 跳过 ]
            } else {
                i++;
            }
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        int teamNum = Integer.parseInt(line.substring(0, comma).trim());
        String rest = line.substring(comma + 1).trim();

        List<List<String>> matches = parseMatches(rest);

        Solution solution = new Solution();
        List<String> result = solution.getTopThree(teamNum, matches);

        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < result.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append('"').append(result.get(i)).append('"');
        }
        sb.append("]");
        System.out.println(sb);
    }
}
