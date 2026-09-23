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
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        ArrayList<String> commands = parseStringArray(line);
        String[] arr = commands.toArray(new String[0]);
        Solution sol = new Solution();
        System.out.println(sol.queryNetEnergy(arr));
    }
}
