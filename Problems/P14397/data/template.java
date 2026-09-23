import java.io.*;

public class Main {
    private static String parseQuotedString(String s) {
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad string");
        i++;
        StringBuilder val = new StringBuilder();
        while (i < s.length() && s.charAt(i) != '"') val.append(s.charAt(i++));
        if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad string end");
        return val.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        String s = parseQuotedString(line);
        Solution sol = new Solution();
        String ans = sol.processString(s);
        System.out.println('"' + ans + '"');
    }
}
