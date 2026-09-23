import java.io.*;
import java.util.*;

public class Main {
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

    private static String parseQuotedString(String s) {
        int start = s.indexOf('"');
        int end = s.lastIndexOf('"');
        if (start == -1 || end == -1 || start >= end) return "";
        return s.substring(start + 1, end);
    }

    private static List<Integer> parseIntList(String s) {
        List<Integer> list = new ArrayList<>();
        int n = s.length();
        int num = 0;
        boolean hasNum = false;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                num = num * 10 + (c - '0');
                hasNum = true;
            } else if ((c == ',' || c == ']') && hasNum) {
                list.add(num);
                num = 0;
                hasNum = false;
                if (c == ']') break;
            }
        }
        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma1 = findTopLevelComma(line);
        String cidr = parseQuotedString(line.substring(0, comma1));

        String rest = line.substring(comma1 + 1).trim();
        int comma2 = findTopLevelComma(rest);
        int n = Integer.parseInt(rest.substring(0, comma2).trim());

        String reqStr = rest.substring(comma2 + 1).trim();
        List<Integer> requirements = parseIntList(reqStr);

        Solution solution = new Solution();
        List<String> result = solution.allocateSubnets(cidr, n, requirements);

        // 输出结果
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < result.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append("\"").append(result.get(i)).append("\"");
        }
        sb.append("]");
        System.out.println(sb.toString());
    }
}
