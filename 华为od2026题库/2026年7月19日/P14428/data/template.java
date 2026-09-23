import java.io.*;
import java.util.*;

public class Main {
    // 返回从 start 处的 '[' 匹配的 ']' 的下标
    private static int matchBracket(String s, int start) {
        int depth = 0;
        for (int i = start; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') depth++;
            else if (c == ']') {
                depth--;
                if (depth == 0) return i;
            }
        }
        return -1;
    }

    // 解析形如 [1, 2, -3] 的一维整型数组（忽略空格与括号）
    private static int[] parse1D(String s) {
        List<Integer> list = new ArrayList<>();
        int i = 0, n = s.length();
        while (i < n) {
            char c = s.charAt(i);
            if ((c == '-' && i + 1 < n && Character.isDigit(s.charAt(i + 1))) || Character.isDigit(c)) {
                int sign = 1;
                if (c == '-') { sign = -1; i++; }
                long val = 0;
                while (i < n && Character.isDigit(s.charAt(i))) { val = val * 10 + (s.charAt(i) - '0'); i++; }
                list.add((int) (sign * val));
            } else {
                i++;
            }
        }
        int[] res = new int[list.size()];
        for (int k = 0; k < res.length; k++) res[k] = list.get(k);
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String l;
        while ((l = br.readLine()) != null) sb.append(l);
        String line = sb.toString().trim();

        // warehouses：第一个 [...] 数组
        int p1 = line.indexOf('[');
        int e1 = matchBracket(line, p1);
        int[] warehouses = parse1D(line.substring(p1, e1 + 1));

        // queries：第二个 [[...]] 数组
        int p2 = line.indexOf('[', e1 + 1);
        int e2 = matchBracket(line, p2);
        String queriesStr = line.substring(p2, e2 + 1);
        List<int[]> qList = new ArrayList<>();
        int m = queriesStr.length();
        int j = 1; // 跳过最外层 '['
        while (j < m) {
            if (queriesStr.charAt(j) == '[') {
                int k = matchBracket(queriesStr, j);
                qList.add(parse1D(queriesStr.substring(j, k + 1)));
                j = k + 1;
            } else {
                j++;
            }
        }
        int[][] queries = qList.toArray(new int[0][]);

        // 末尾整数 numOfWarehouse
        int numOfWarehouse = Integer.parseInt(line.substring(e2 + 1).trim());

        Solution solution = new Solution();
        int[][] res = solution.getWarehouseReport(warehouses, queries, numOfWarehouse);

        // 紧凑输出 [[..],[..]]
        StringBuilder out = new StringBuilder("[");
        for (int a = 0; a < res.length; a++) {
            if (a > 0) out.append(",");
            out.append("[");
            for (int b = 0; b < res[a].length; b++) {
                if (b > 0) out.append(",");
                out.append(res[a][b]);
            }
            out.append("]");
        }
        out.append("]");
        System.out.println(out.toString());
    }
}
