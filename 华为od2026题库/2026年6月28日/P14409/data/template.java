import java.io.*;
import java.util.*;

public class Main {
    private static List<Integer> parseIntList(String s) {
        List<Integer> list = new ArrayList<>();
        int i = 0;
        while (i < s.length() && (s.charAt(i) == ' ' || s.charAt(i) == '\t')) i++;
        if (i >= s.length() || s.charAt(i) != '[') return list;
        i++;
        while (i < s.length()) {
            while (i < s.length() && (s.charAt(i) == ' ' || s.charAt(i) == '\t' || s.charAt(i) == ',')) {
                if (s.charAt(i) == ']') return list;
                i++;
            }
            if (i >= s.length() || s.charAt(i) == ']') break;
            int j = i;
            while (j < s.length() && (Character.isDigit(s.charAt(j)) || s.charAt(j) == '-')) j++;
            list.add(Integer.parseInt(s.substring(i, j)));
            i = j;
        }
        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        int comma = line.indexOf(',');
        if (comma < 0) return;
        int n = Integer.parseInt(line.substring(0, comma).trim());
        List<Integer> numsList = parseIntList(line.substring(comma + 1));
        if (numsList.size() != n) return;
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = numsList.get(i);
        Solution solution = new Solution();
        System.out.println(solution.minSplitRangeSum(nums));
    }
}
