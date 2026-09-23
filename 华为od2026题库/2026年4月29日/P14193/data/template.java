import java.io.*;
import java.util.*;

public class Main {
    static class Parser {
        String s;
        int i;
        Parser(String s) { this.s = s; }

        void skip() {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        }

        String parseString() {
            skip();
            i++; // 跳过左引号
            StringBuilder sb = new StringBuilder();
            while (i < s.length()) {
                char c = s.charAt(i++);
                if (c == '\\') {
                    if (i < s.length()) sb.append(s.charAt(i++));
                } else if (c == '"') {
                    break;
                } else {
                    sb.append(c);
                }
            }
            return sb.toString();
        }

        String[][] parse() {
            ArrayList<String[]> res = new ArrayList<>();
            skip();
            if (i < s.length() && s.charAt(i) == '[') i++;
            while (true) {
                skip();
                if (i >= s.length() || s.charAt(i) == ']') break;
                if (s.charAt(i) == ',') { i++; continue; }
                i++; // 跳过命令数组的左中括号
                ArrayList<String> one = new ArrayList<>();
                while (true) {
                    skip();
                    if (i < s.length() && s.charAt(i) == ']') { i++; break; }
                    if (i < s.length() && s.charAt(i) == ',') { i++; continue; }
                    one.add(parseString());
                }
                res.add(one.toArray(new String[0]));
            }
            return res.toArray(new String[0][]);
        }
    }

    static String quote(String s) {
        StringBuilder sb = new StringBuilder();
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\\' || c == '"') sb.append('\\').append(c);
            else if (c == '\n') sb.append("\\n");
            else if (c == '\r') sb.append("\\r");
            else if (c == '\t') sb.append("\\t");
            else sb.append(c);
        }
        sb.append('"');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder input = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) input.append(line);
        String[][] command = new Parser(input.toString()).parse();
        String ans = new Solution().execute_command(command);
        System.out.print(quote(ans));
    }
}
