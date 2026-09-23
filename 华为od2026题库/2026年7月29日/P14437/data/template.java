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

    private static int[][] parse2DArray(String s) {
        List<int[]> list = new ArrayList<>();
        int i = 0, n = s.length();
        // 跳过外层 [
        while (i < n && s.charAt(i) != '[') i++;
        i++; // 跳过第一个 [
        while (i < n) {
            while (i < n && s.charAt(i) != '[') {
                if (s.charAt(i) == ']') { i++; break; }
                i++;
            }
            if (i >= n || s.charAt(i - 1) == ']') break;
            i++; // 跳过内层 [
            // 解析 timestamp
            boolean neg = false;
            if (s.charAt(i) == '-') { neg = true; i++; }
            int t = 0;
            while (i < n && Character.isDigit(s.charAt(i))) {
                t = t * 10 + (s.charAt(i) - '0'); i++;
            }
            if (neg) t = -t;
            i++; // 跳过逗号
            // 解析 value
            neg = false;
            if (s.charAt(i) == '-') { neg = true; i++; }
            int v = 0;
            while (i < n && Character.isDigit(s.charAt(i))) {
                v = v * 10 + (s.charAt(i) - '0'); i++;
            }
            if (neg) v = -v;
            list.add(new int[]{t, v});
            i++; // 跳过内层 ]
        }
        return list.toArray(new int[0][]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        String dataStr = line.substring(0, comma);
        int interval = Integer.parseInt(line.substring(comma + 1).trim());

        int[][] data = parse2DArray(dataStr);

        Solution solution = new Solution();
        int[] result = solution.getMaxValues(data, interval);

        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < result.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(result[i]);
        }
        sb.append("]");
        System.out.println(sb);
    }
}
