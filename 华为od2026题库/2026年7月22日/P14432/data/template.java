import java.io.*;
import java.util.*;

public class Main {
    // 找到括号深度为 0 的第一个逗号（用于切分顶层字段 n,m,files,cost）
    private static int findTopLevelComma(String s) {
        int bracket = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
        return -1;
    }

    // 解析一维整数列表，如 [1,2,2]
    private static List<Integer> parseIntVector(String s) {
        List<Integer> list = new ArrayList<>();
        int i = 0, n = s.length();
        while (i < n && s.charAt(i) != '[') i++;
        i++;  // 跳过 '['
        StringBuilder cur = new StringBuilder();
        while (i < n) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                cur.append(c);
            } else if (c == ',' || c == ']') {
                // 遇到逗号或 ']' 时结算当前整数
                if (cur.length() > 0) {
                    list.add(Integer.parseInt(cur.toString()));
                    cur.setLength(0);
                }
                if (c == ']') break;  // 列表结束
            }
            i++;
        }
        return list;
    }

    // 解析二维整数列表，如 [[0,1],[1,2],[0,2]]
    private static List<List<Integer>> parseIntMatrix(String s) {
        List<List<Integer>> res = new ArrayList<>();
        int i = 0, n = s.length();
        while (i < n && s.charAt(i) != '[') i++;
        i++;  // 跳过外层 '['
        while (i < n && s.charAt(i) != ']') {
            if (s.charAt(i) == '[') {
                int depth = 0, j = i;
                for (; j < n; j++) {
                    if (s.charAt(j) == '[') depth++;
                    else if (s.charAt(j) == ']') {
                        depth--;
                        if (depth == 0) break;
                    }
                }
                res.add(parseIntVector(s.substring(i, j + 1)));
                i = j + 1;
                while (i < n && (s.charAt(i) == ',' || s.charAt(i) == ' ')) i++;
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

        // 依次按顶层逗号切分为 n, m, files, cost 四段
        int c1 = findTopLevelComma(line);
        int n = Integer.parseInt(line.substring(0, c1).trim());
        String rest1 = line.substring(c1 + 1).trim();

        int c2 = findTopLevelComma(rest1);
        int m = Integer.parseInt(rest1.substring(0, c2).trim());
        String rest2 = rest1.substring(c2 + 1).trim();

        int c3 = findTopLevelComma(rest2);
        String filesStr = rest2.substring(0, c3).trim();
        String costStr = rest2.substring(c3 + 1).trim();

        List<List<Integer>> files = parseIntMatrix(filesStr);
        List<Integer> cost = parseIntVector(costStr);

        Solution solution = new Solution();
        System.out.println(solution.minCost(n, m, files, cost));
    }
}
