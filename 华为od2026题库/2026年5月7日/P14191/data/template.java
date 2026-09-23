import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line).append('\n');
        }
        String text = sb.toString();
        Parsed p = parseInput(text);
        Solution solution = new Solution();
        String[] ans = solution.FindNextKeywords(p.commands.toArray(new String[0]), p.prefix);
        System.out.println(formatOutput(ans));
    }

    static class Parsed {
        ArrayList<String> commands = new ArrayList<>();
        String prefix = "";
    }

    static int skipSpace(String t, int i) {
        while (i < t.length() && (t.charAt(i) == ' ' || t.charAt(i) == '\t' || t.charAt(i) == '\r' || t.charAt(i) == '\n')) {
            i++;
        }
        return i;
    }

    static Parsed parseInput(String t) {
        Parsed p = new Parsed();
        int i = 0;
        i = skipSpace(t, i);
        if (i >= t.length() || t.charAt(i) != '[') {
            return p;
        }
        i++;
        while (true) {
            i = skipSpace(t, i);
            if (i < t.length() && t.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= t.length() || t.charAt(i) != '"') {
                break;
            }
            i++;
            int st = i;
            while (i < t.length() && t.charAt(i) != '"') {
                i++;
            }
            p.commands.add(t.substring(st, i));
            if (i < t.length() && t.charAt(i) == '"') {
                i++;
            }
            i = skipSpace(t, i);
            if (i < t.length() && t.charAt(i) == ']') {
                i++;
                break;
            }
            if (i < t.length() && t.charAt(i) == ',') {
                i++;
                continue;
            }
            break;
        }
        i = skipSpace(t, i);
        if (i < t.length() && t.charAt(i) == ',') {
            i++;
            i = skipSpace(t, i);
            if (i < t.length() && t.charAt(i) == '"') {
                i++;
                int st = i;
                while (i < t.length() && t.charAt(i) != '"') {
                    i++;
                }
                p.prefix = t.substring(st, i);
            }
        }
        return p;
    }

    static String formatOutput(String[] ans) {
        StringBuilder o = new StringBuilder();
        o.append('[');
        for (int k = 0; k < ans.length; k++) {
            if (k > 0) o.append(',');
            o.append('"').append(ans[k]).append('"');
        }
        o.append(']');
        return o.toString();
    }
}
