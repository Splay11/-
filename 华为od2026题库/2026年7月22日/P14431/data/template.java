import java.io.*;
import java.util.*;

public class Main {
    // 解析形如 [1,2,3] 的整数数组
    private static List<Integer> parseArray(String s) {
        List<Integer> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                cur.append(c);
            } else if (c == ',' || c == ']') {
                if (cur.length() > 0) {
                    list.add(Integer.parseInt(cur.toString()));
                    cur.setLength(0);
                }
            }
        }
        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        List<Integer> nums = parseArray(line);
        Solution solution = new Solution();
        System.out.println(solution.longestSubarray(nums));
    }
}
