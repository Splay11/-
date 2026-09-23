import java.io.*;
import java.util.*;

public class Main {
    private static List<Integer> parseIntList(String s) {
        List<Integer> res = new ArrayList<>();
        int val = 0, sign = 1;
        boolean inNum = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '-') { sign = -1; inNum = true; }
            else if (c >= '0' && c <= '9') { val = val * 10 + (c - '0'); inNum = true; }
            else {
                if (inNum) { res.add(sign * val); val = 0; sign = 1; inNum = false; }
            }
        }
        return res;
    }

    private static List<List<Integer>> parseInt2DList(String s) {
        List<List<Integer>> res = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            if (s.charAt(i) == '[' && i + 1 < s.length() &&
                (Character.isDigit(s.charAt(i+1)) || s.charAt(i+1) == '-')) {
                i++;
                int a = 0, b = 0;
                boolean neg = false;
                if (s.charAt(i) == '-') { neg = true; i++; }
                while (i < s.length() && Character.isDigit(s.charAt(i)))
                    a = a * 10 + (s.charAt(i++) - '0');
                if (neg) a = -a;
                while (i < s.length() && !Character.isDigit(s.charAt(i)) && s.charAt(i) != '-') i++;
                neg = false;
                if (i < s.length() && s.charAt(i) == '-') { neg = true; i++; }
                while (i < s.length() && Character.isDigit(s.charAt(i)))
                    b = b * 10 + (s.charAt(i++) - '0');
                if (neg) b = -b;
                res.add(Arrays.asList(a, b));
                if (i < s.length() && s.charAt(i) == ']') i++;
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

        // 找顶层逗号
        int depth = 0;
        List<Integer> splits = new ArrayList<>();
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '[') depth++;
            else if (c == ']') depth--;
            else if (c == ',' && depth == 0) splits.add(i);
        }

        List<Integer> green = parseIntList(line.substring(0, splits.get(0)));
        List<Integer> carbon = parseIntList(line.substring(splits.get(0)+1, splits.get(1)));
        List<List<Integer>> edges = parseInt2DList(line.substring(splits.get(1)+1));

        Solution solution = new Solution();
        System.out.println(solution.maxCarbonReduction(green, carbon, edges));
    }
}
