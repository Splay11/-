import java.io.*;
import java.util.*;

public class Main {
    private static ArrayList<String> parseStringArray(String s) {
        ArrayList<String> out = new ArrayList<>();
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '[') throw new RuntimeException("bad");
        i++;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad");
            i++;
            StringBuilder val = new StringBuilder();
            while (i < s.length() && s.charAt(i) != '"') val.append(s.charAt(i++));
            if (i >= s.length() || s.charAt(i) != '"') throw new RuntimeException("bad");
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
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) sb.append(line);
        String text = sb.toString().trim();
        if (text.isEmpty()) return;
        ArrayList<String> list = parseStringArray(text);
        String[] uriReqs = list.toArray(new String[0]);
        System.out.println(new Solution().countSimilarGroups(uriReqs));
    }
}
