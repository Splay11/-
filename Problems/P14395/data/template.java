import java.io.*;
import java.util.*;

public class Main {
    private static ArrayList<String> parseStringArray(String s) {
        ArrayList<String> out = new ArrayList<>();
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '[') throw new RuntimeException("bad array");
        i++;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad string");
            i++;
            StringBuilder val = new StringBuilder();
            while (i < s.length() && s.charAt(i) != '"') val.append(s.charAt(i++));
            if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad string end");
            i++;
            out.add(val.toString());
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (s.charAt(i++) != ',') throw new RuntimeException("bad comma");
        }
        return out;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        ArrayList<String> ips = parseStringArray(line);
        Solution sol = new Solution();
        String[] ans = sol.filterValidAClassIPs(ips.toArray(new String[0]));
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) sb.append(',');
            sb.append('"').append(ans[i]).append('"');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
