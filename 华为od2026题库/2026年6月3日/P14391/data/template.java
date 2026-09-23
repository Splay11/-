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

    private static String[] parseStringArray(String s) {
        List<String> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inString = false;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                if (inString) {
                    list.add(cur.toString());
                    cur.setLength(0);
                }
                inString = !inString;
            } else if (inString) {
                cur.append(c);
            }
        }

        return list.toArray(new String[0]);
    }

    private static int[] parseIntArray(String s) {
        List<Integer> list = new ArrayList<>();
        long num = 0;
        int sign = 1;
        boolean inNum = false;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '-') {
                sign = -1;
                num = 0;
                inNum = true;
            } else if (Character.isDigit(c)) {
                if (!inNum) {
                    sign = 1;
                    num = 0;
                    inNum = true;
                }
                num = num * 10 + (c - '0');
            } else {
                if (inNum) {
                    list.add((int)(sign * num));
                    inNum = false;
                    num = 0;
                    sign = 1;
                }
            }
        }

        if (inNum) {
            list.add((int)(sign * num));
        }

        int[] arr = new int[list.size()];
        for (int i = 0; i < list.size(); i++) {
            arr[i] = list.get(i);
        }
        return arr;
    }

    private static void printList(List<Integer> ans) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append(ans.get(i));
        }
        sb.append("]");
        System.out.print(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder input = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            input.append(line.trim());
        }

        String s = input.toString();
        int comma = findTopLevelComma(s);
        String opsStr = s.substring(0, comma);
        String valsStr = s.substring(comma + 1);

        String[] ops = parseStringArray(opsStr);
        int[] vals = parseIntArray(valsStr);

        Solution solution = new Solution();
        printList(solution.monitor(ops, vals));
    }
}
