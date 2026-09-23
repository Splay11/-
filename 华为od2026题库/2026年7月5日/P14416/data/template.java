import java.io.*;
import java.util.*;

public class Main {
    private static int findTopLevelComma(String s) {
        int bracket = 0;
        boolean inString = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') inString = !inString;
            else if (!inString) {
                if (c == '[') bracket++;
                else if (c == ']') bracket--;
                else if (c == ',' && bracket == 0) return i;
            }
        }
        return -1;
    }

    private static List<String> parseStringArray(String s) {
        List<String> res = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inStr = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                inStr = !inStr;
                if (!inStr) {
                    res.add(cur.toString());
                    cur.setLength(0);
                }
            } else if (inStr) {
                cur.append(c);
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
        int splitLine = Integer.parseInt(line.substring(0, comma).trim());
        String rest = line.substring(comma + 1).trim();

        List<String> sqlText = parseStringArray(rest);

        Solution solution = new Solution();
        System.out.println(solution.splitSQLToFiles(splitLine, sqlText));
    }
}
