import java.io.*;
import java.util.*;

public class Main {
    private static String trim(String s) {
        int a = 0, b = s.length() - 1;
        while (a <= b && Character.isWhitespace(s.charAt(a))) a++;
        while (b >= a && Character.isWhitespace(s.charAt(b))) b--;
        return s.substring(a, b + 1);
    }

    private static String[] parseStringArray(String line) throws Exception {
        String s = trim(line);
        if (s.isEmpty() || s.charAt(0) != '[') throw new Exception("bad");
        ArrayList<String> out = new ArrayList<>();
        int i = 1;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != '"') throw new Exception("bad");
            i++;
            StringBuilder cur = new StringBuilder();
            while (i < s.length() && s.charAt(i) != '"') {
                cur.append(s.charAt(i));
                i++;
            }
            if (i >= s.length() || s.charAt(i) != '"') throw new Exception("bad");
            i++;
            out.add(cur.toString());
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
            i++;
        }
        return out.toArray(new String[0]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        String line2 = br.readLine();
        if (line1 == null || line2 == null) return;
        String[] charMatrix = parseStringArray(line1);
        String[] words = parseStringArray(line2);
        System.out.println(new Solution().countMatchedWords(charMatrix, words));
    }
}
