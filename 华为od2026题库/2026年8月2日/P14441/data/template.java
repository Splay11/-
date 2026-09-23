import java.io.*;
import java.util.*;

public class Main {
    // 解析整数列表 [a1,a2,...,an]，返回 int[]
    private static int[] parseIntList(String s) {
        List<Integer> list = new ArrayList<>();
        int i = 0;
        int n = s.length();
        while (i < n && s.charAt(i) != '[') i++;
        i++; // 跳过 [
        int cur = 0;
        boolean hasNum = false;
        while (i < n) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                cur = cur * 10 + (c - '0');
                hasNum = true;
            } else if (c == ',' || c == ']') {
                if (hasNum) {
                    list.add(cur);
                    cur = 0;
                    hasNum = false;
                }
                if (c == ']') break;
            }
            i++;
        }
        // 转换为 int[]
        int[] res = new int[list.size()];
        for (int j = 0; j < list.size(); j++) res[j] = list.get(j);
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析 k,m,w,[...]
        int firstComma = line.indexOf(',');
        int k = Integer.parseInt(line.substring(0, firstComma).trim());

        String rest1 = line.substring(firstComma + 1);
        int secondComma = rest1.indexOf(',');
        int m = Integer.parseInt(rest1.substring(0, secondComma).trim());

        String rest2 = rest1.substring(secondComma + 1);
        int thirdComma = rest2.indexOf(',');
        int w = Integer.parseInt(rest2.substring(0, thirdComma).trim());

        String rest3 = rest2.substring(thirdComma + 1).trim();
        int[] a = parseIntList(rest3);

        Solution solution = new Solution();
        System.out.println(solution.minSkillSegments(k, m, w, a));
    }
}
