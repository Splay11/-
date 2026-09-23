import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) { return s.trim(); }

    private static int[][] parseArray2d(String line) throws Exception {
        String s = trim(line);
        if (s.isEmpty() || s.charAt(0) != '[') throw new Exception("bad");
        ArrayList<int[]> rows = new ArrayList<>();
        int i = 1;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') { i++; break; }
            if (i >= s.length() || s.charAt(i) != '[') throw new Exception("bad");
            i++;
            ArrayList<Integer> row = new ArrayList<>();
            while (true) {
                while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                if (i < s.length() && s.charAt(i) == ']') { i++; break; }
                int sign = 1;
                if (i < s.length() && s.charAt(i) == '-') { sign = -1; i++; }
                int v = 0; boolean ok = false;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    ok = true; v = v * 10 + (s.charAt(i) - '0'); i++;
                }
                if (!ok) throw new Exception("bad");
                row.add(sign * v);
                while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
                if (i < s.length() && s.charAt(i) == ']') { i++; break; }
                if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
                i++;
            }
            int[] rr = new int[row.size()];
            for (int t = 0; t < row.size(); t++) rr[t] = row.get(t);
            rows.add(rr);
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') { i++; break; }
            if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
            i++;
        }
        return rows.toArray(new int[0][]);
    }

    private static String parseQuoted(String line) {
        String s = trim(line);
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"')
            return s.substring(1, s.length() - 1);
        return s;
    }

    private static String fmtCards(int[][] cards) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < cards.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append('[');
            for (int j = 0; j < cards[i].length; j++) {
                if (j > 0) sb.append(", ");
                sb.append(cards[i][j]);
            }
            sb.append(']');
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        String line2 = br.readLine();
        if (line1 == null || line2 == null) return;
        int[][] cards = parseArray2d(line1);
        String align = parseQuoted(line2);
        System.out.println(fmtCards(new Solution().alignCards(cards, align)));
    }
}
