import java.io.*;
import java.util.*;

public class Main {
    // 按最外层逗号切分输入行
    private static List<String> splitTopLevel(String s) {
        List<String> parts = new ArrayList<>();
        int depth = 0;
        StringBuilder cur = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') { depth++; cur.append(c); }
            else if (c == ']') { depth--; cur.append(c); }
            else if (c == ',' && depth == 0) { parts.add(cur.toString()); cur.setLength(0); }
            else cur.append(c);
        }
        parts.add(cur.toString());
        return parts;
    }

    // 解析 [[a,b],[c,d],...] 形式的边列表
    private static List<List<Integer>> parseEdges(String s) {
        // 先去掉最外层的一对中括号
        String inner = s.trim();
        if (inner.startsWith("[")) inner = inner.substring(1);
        if (inner.endsWith("]")) inner = inner.substring(0, inner.length() - 1);
        List<List<Integer>> res = new ArrayList<>();
        int i = 0, len = inner.length();
        while (i < len) {
            if (inner.charAt(i) == '[') {
                int depth = 1, j = i + 1;
                while (j < len && depth > 0) {
                    if (inner.charAt(j) == '[') depth++;
                    else if (inner.charAt(j) == ']') { depth--; if (depth == 0) break; }
                    j++;
                }
                String pairStr = inner.substring(i + 1, j);
                List<Integer> pair = new ArrayList<>();
                for (String num : pairStr.split(",")) {
                    if (!num.trim().isEmpty()) pair.add(Integer.parseInt(num.trim()));
                }
                res.add(pair);
                i = j + 1;
            } else {
                i++;
            }
        }
        return res;
    }

    // 解析 [a,b,c,...] 形式的整数列表
    private static List<Integer> parseIntList(String s) {
        List<Integer> res = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int k = 1; k < s.length(); k++) {
            char c = s.charAt(k);
            if (c == ',') {
                if (cur.length() > 0) { res.add(Integer.parseInt(cur.toString().trim())); cur.setLength(0); }
            } else if (c == ']') {
                if (cur.length() > 0) res.add(Integer.parseInt(cur.toString().trim()));
            } else if (c != ' ') {
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

        List<String> parts = splitTopLevel(line);
        int n = Integer.parseInt(parts.get(0).trim());
        List<List<Integer>> edges = parseEdges(parts.get(1).trim());
        int startA = Integer.parseInt(parts.get(2).trim());
        List<Integer> patrolPath = parseIntList(parts.get(3).trim());

        Solution solution = new Solution();
        System.out.println(solution.minMeetRounds(n, edges, startA, patrolPath));
    }
}
