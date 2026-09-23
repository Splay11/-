import java.io.*;
import java.util.*;

public class Main {
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

    private static int[] parseIntArray(String s) {
        s = s.trim();
        if (s.length() <= 2) return new int[0];

        List<Integer> list = new ArrayList<>();
        int i = 1; // 跳过左中括号
        while (i < s.length() - 1) {
            while (i < s.length() && (s.charAt(i) == ' ' || s.charAt(i) == ',')) i++;

            int sign = 1;
            if (s.charAt(i) == '-') {
                sign = -1;
                i++;
            }

            int val = 0;
            while (i < s.length() && Character.isDigit(s.charAt(i))) {
                val = val * 10 + (s.charAt(i) - '0');
                i++;
            }

            list.add(sign * val);
        }

        int[] nums = new int[list.size()];
        for (int j = 0; j < list.size(); j++) nums[j] = list.get(j);
        return nums;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        int[] nums = parseIntArray(line.substring(0, comma));
        int k = Integer.parseInt(line.substring(comma + 1).trim());

        Solution solution = new Solution();
        System.out.println(solution.maxEnergyDivisibleByK(nums, nums.length, k));
    }
}
