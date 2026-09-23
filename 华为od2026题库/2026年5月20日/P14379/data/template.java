import java.io.*;

public class Main {
    private static String parsePythonStringLiteral(String line) throws Exception {
        line = line.trim();
        if (line.length() < 2 || line.charAt(0) != '"') throw new Exception("bad");
        StringBuilder sb = new StringBuilder();
        int i = 1;
        while (i < line.length()) {
            char c = line.charAt(i);
            if (c == '"') {
                if (i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    sb.append('"');
                    i += 2;
                    continue;
                }
                if (i != line.length() - 1) throw new Exception("bad");
                break;
            }
            if (c == '\\') {
                if (i + 1 >= line.length()) throw new Exception("bad");
                char n = line.charAt(i + 1);
                if (n == 'n') sb.append('\n');
                else if (n == 't') sb.append('\t');
                else if (n == 'r') sb.append('\r');
                else if (n == '\\') sb.append('\\');
                else if (n == '"') sb.append('"');
                else sb.append(n);
                i += 2;
                continue;
            }
            sb.append(c);
            i++;
        }
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        String story = parsePythonStringLiteral(line);
        Solution sol = new Solution();
        System.out.println(sol.lengthOfLongestSubstring(story));
    }
}
