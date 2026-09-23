import java.io.*;
import java.util.*;

public class Main {
    // 解析整型列表 "[a,b,c,...]"
    private static List<Integer> parseIntList(String s) {
        List<Integer> res = new ArrayList<>();
        int i = 1;  // 跳过 '['
        int n = s.length();
        while (i < n) {
            while (i < n && s.charAt(i) == ' ') i++;
            if (i >= n || s.charAt(i) == ']') break;
            int sign = 1;
            if (s.charAt(i) == '-') { sign = -1; i++; }
            int num = 0;
            while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                num = num * 10 + (s.charAt(i) - '0');
                i++;
            }
            res.add(sign * num);
            if (i < n && s.charAt(i) == ',') i++;
        }
        return res;
    }

    // 找到顶层逗号（不在括号内的逗号）
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

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(
            new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;

        // 解析 count
        int comma1 = findTopLevelComma(line);
        int count = Integer.parseInt(line.substring(0, comma1).trim());

        // 解析 total
        String rest1 = line.substring(comma1 + 1).trim();
        int comma2 = findTopLevelComma(rest1);
        int total = Integer.parseInt(rest1.substring(0, comma2).trim());

        // 解析数组部分
        String rest2 = rest1.substring(comma2 + 1).trim();
        int split = rest2.indexOf("],[");
        String valuesStr = rest2.substring(0, split + 1);
        String decaysStr = "[" + rest2.substring(split + 3);

        List<Integer> values = parseIntList(valuesStr);
        List<Integer> decays = parseIntList(decaysStr);

        Solution solution = new Solution();
        System.out.println(solution.maxMushroomValue(count, total, values, decays));
    }
}
