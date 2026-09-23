import java.io.*;
import java.util.*;

public class Main {
    // 解析形如 [1,5,3] 的整数列表（忽略括号、空格，按逗号切分）
    private static List<Integer> parseIntList(String s) {
        List<Integer> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[' || c == ']' || c == ' ') continue;
            if (c == ',') {
                if (cur.length() > 0) {
                    list.add(Integer.parseInt(cur.toString()));
                    cur.setLength(0);
                }
            } else {
                cur.append(c);
            }
        }
        if (cur.length() > 0) list.add(Integer.parseInt(cur.toString()));
        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 顶层逗号：分隔 N 与已交卷列表
        int comma = line.indexOf(',');
        int n = Integer.parseInt(line.substring(0, comma).trim());
        String rest = line.substring(comma + 1).trim();

        List<Integer> submitted = parseIntList(rest);

        Solution solution = new Solution();
        List<Integer> ans = solution.findMissingStudents(n, submitted);

        // 按题面格式输出：[a,b,c]（无空格）
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append(ans.get(i));
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
