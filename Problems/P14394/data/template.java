import java.io.*;
import java.util.*;

public class Main {
    private static ArrayList<String> parseStringList(String s, int[] idx) {
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        if (idx[0] >= s.length() || s.charAt(idx[0]) != '[') throw new RuntimeException("bad array");
        idx[0]++;
        ArrayList<String> out = new ArrayList<>();
        while (true) {
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != '"') throw new RuntimeException("bad quote");
            StringBuilder cur = new StringBuilder();
            while (idx[0] < s.length() && s.charAt(idx[0]) != '"') cur.append(s.charAt(idx[0]++));
            if (s.charAt(idx[0]++) != '"') throw new RuntimeException("bad quote end");
            out.add(cur.toString());
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        return out;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        int[] idx = {0};
        ArrayList<String> commands = parseStringList(line, idx);
        Solution sol = new Solution();
        int[] ans = sol.processPacketCommands(commands.toArray(new String[0]));
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(ans[i]);
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
