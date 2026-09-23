import java.io.*;
import java.util.*;

public class Main {
    private static void skip(String s, int[] i) {
        while (i[0] < s.length() && Character.isWhitespace(s.charAt(i[0]))) i[0]++;
    }

    private static int readInt(String s, int[] i) {
        skip(s, i);
        int sign = 1;
        if (i[0] < s.length() && s.charAt(i[0]) == '-') {
            sign = -1;
            i[0]++;
        }
        int v = 0;
        boolean ok = false;
        while (i[0] < s.length() && Character.isDigit(s.charAt(i[0]))) {
            ok = true;
            v = v * 10 + (s.charAt(i[0]++) - '0');
        }
        if (!ok) throw new RuntimeException("bad int");
        return sign * v;
    }

    private static String readQuoted(String s, int[] i) {
        skip(s, i);
        if (s.charAt(i[0]++) != '"') throw new RuntimeException("bad str");
        StringBuilder sb = new StringBuilder();
        while (i[0] < s.length() && s.charAt(i[0]) != '"') {
            char c = s.charAt(i[0]++);
            if (c == '\\' && i[0] < s.length()) sb.append(s.charAt(i[0]++));
            else sb.append(c);
        }
        if (i[0] >= s.length() || s.charAt(i[0]++) != '"') throw new RuntimeException("bad str end");
        return sb.toString();
    }

    private static Cell[] parseTable(String s) {
        int[] i = {0};
        skip(s, i);
        if (s.charAt(i[0]++) != '[') throw new RuntimeException("bad");
        ArrayList<Cell> list = new ArrayList<>();
        while (true) {
            skip(s, i);
            if (i[0] < s.length() && s.charAt(i[0]) == ']') {
                i[0]++;
                break;
            }
            if (s.charAt(i[0]++) != '[') throw new RuntimeException("bad cell");
            int r = readInt(s, i);
            skip(s, i);
            if (s.charAt(i[0]++) != ',') throw new RuntimeException(",");
            int c = readInt(s, i);
            skip(s, i);
            if (s.charAt(i[0]++) != ',') throw new RuntimeException(",");
            String content = readQuoted(s, i);
            skip(s, i);
            if (s.charAt(i[0]++) != ']') throw new RuntimeException("]");
            list.add(new Cell(r, c, content));
            skip(s, i);
            if (i[0] < s.length() && s.charAt(i[0]) == ']') {
                i[0]++;
                break;
            }
            if (s.charAt(i[0]++) != ',') throw new RuntimeException(",");
        }
        return list.toArray(new Cell[0]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) sb.append(line);
        String text = sb.toString().trim();
        if (text.isEmpty()) return;
        String[] ans = new Solution().transformTable(parseTable(text));
        StringBuilder out = new StringBuilder("[");
        for (int k = 0; k < ans.length; k++) {
            if (k > 0) out.append(',');
            out.append('"');
            for (char ch : ans[k].toCharArray()) {
                if (ch == '\\' || ch == '"') out.append('\\');
                out.append(ch);
            }
            out.append('"');
        }
        out.append(']');
        System.out.println(out.toString());
    }
}
