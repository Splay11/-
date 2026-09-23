import java.io.*;
import java.util.*;

public class Main {
    // 解析形如 ["a","b","c"] 的字符串数组（提取所有引号内的内容）
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

        // 整行即 JSON 字符串数组，提取所有字符串
        List<String> dates = parseStringList(line);

        Solution solution = new Solution();
        List<String> ans = solution.normalizeDates(dates);

        // 按题面格式输出：["a","b",...]（无空格）
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append('"').append(ans.get(i)).append('"');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
