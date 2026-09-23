import java.io.*;
import java.util.*;

public class Main {

    static int[][] parseTriples(String s) {
        s = s.trim();
        if (s.equals("[]") || s.isEmpty()) return new int[0][];
        ArrayList<int[]> list = new ArrayList<>();
        int i = 0, n = s.length();
        while (i < n && s.charAt(i) != '[') i++;
        if (i < n) i++;
        while (i < n) {
            while (i < n && (s.charAt(i) == ' ' || s.charAt(i) == ',')) i++;
            if (i >= n || s.charAt(i) == ']') break;
            if (s.charAt(i) != '[') { i++; continue; }
            i++;
            int[] vals = new int[3];
            int k = 0;
            while (i < n && s.charAt(i) != ']' && k < 3) {
                while (i < n && (s.charAt(i) == ' ' || s.charAt(i) == ',')) i++;
                if (i >= n || s.charAt(i) == ']') break;
                int sign = 1;
                if (s.charAt(i) == '-') { sign = -1; i++; }
                int v = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    v = v * 10 + (s.charAt(i) - '0');
                    i++;
                }
                vals[k++] = sign * v;
            }
            while (i < n && s.charAt(i) != ']') i++;
            if (i < n && s.charAt(i) == ']') i++;
            list.add(vals);
        }
        return list.toArray(new int[0][]);
    }

    static String readAll() throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        boolean first = true;
        while ((line = br.readLine()) != null) {
            if (!first) sb.append('\n');
            first = false;
            sb.append(line);
        }
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        String raw = readAll();
        String[] lines = raw.isEmpty() ? new String[0] : raw.split("\n", -1);
        int n = lines.length > 0 ? Integer.parseInt(lines[0].trim()) : 0;
        int[][] ops = lines.length > 1 ? parseTriples(lines[1]) : new int[0][];
        System.out.println(new Solution().maxLinkLoad(n, ops));
    }
}
