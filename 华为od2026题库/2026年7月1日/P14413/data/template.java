import java.io.*;
import java.util.*;

public class Main {
    // 找到顶层逗号（不在嵌套括号内）
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

    // 解析整数数组 "[a1,a2,...,an]"
    private static List<Integer> parseIntList(String s) {
        List<Integer> res = new ArrayList<>();
        s = s.substring(1, s.length() - 1); // 去掉首尾 []
        if (s.isEmpty()) return res;
        String[] parts = s.split(",");
        for (String p : parts) {
            res.add(Integer.parseInt(p.trim()));
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        List<Integer> nums = parseIntList(line.substring(0, comma));
        int target = Integer.parseInt(line.substring(comma + 1).trim());

        Solution solution = new Solution();
        List<List<Integer>> result = solution.threeSumWithParity(nums, target);
        System.out.println(result.toString().replace(" ", ""));
    }
}
