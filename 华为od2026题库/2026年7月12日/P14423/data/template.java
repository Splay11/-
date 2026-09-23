import java.io.*;
import java.util.*;

public class Main {
    // 找到两个顶层数组之间的逗号（括号深度为 0 且不在字符串内）
    private static int findTopLevelComma(String s) {
        boolean inString = false;
        int bracket = 0;
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

    // 解析字符串数组 ["a:v1:","b:v1:"] -> List<String>
    private static List<String> parseStringList(String s) {
        List<String> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inString = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                if (inString) {
                    list.add(cur.toString());
                    cur.setLength(0);
                }
                inString = !inString;
            } else if (inString) {
                cur.append(c);
            }
        }
        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        List<String> directDeps = parseStringList(line.substring(0, comma).trim());
        List<String> depRules = parseStringList(line.substring(comma + 1).trim());

        List<String> result = new Solution().getDependencyOrder(directDeps, depRules);

        // 按题面样例格式输出：["name:version",...]（无空格）
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < result.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append('"').append(result.get(i)).append('"');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
