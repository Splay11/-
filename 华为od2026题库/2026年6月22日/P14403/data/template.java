import java.io.*;
import java.util.*;

public class Main {
    private static String readAllInput(BufferedReader br) throws IOException {
        StringBuilder sb = new StringBuilder();
        String chunk;
        while ((chunk = br.readLine()) != null) sb.append(chunk);
        return sb.toString().trim();
    }

    private static ArrayList<String> parseStringArray(String s, int[] idx) {
        ArrayList<String> out = new ArrayList<>();
        while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
        if (idx[0] >= s.length() || s.charAt(idx[0]) != '[') throw new RuntimeException("bad array");
        idx[0]++;
        while (true) {
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (idx[0] >= s.length() || s.charAt(idx[0]) != '"') throw new RuntimeException("bad string");
            idx[0]++;
            StringBuilder val = new StringBuilder();
            while (idx[0] < s.length() && s.charAt(idx[0]) != '"') val.append(s.charAt(idx[0]++));
            if (idx[0] >= s.length() || s.charAt(idx[0]) != '"') throw new RuntimeException("bad string end");
            idx[0]++;
            out.add(val.toString());
            while (idx[0] < s.length() && Character.isWhitespace(s.charAt(idx[0]))) idx[0]++;
            if (idx[0] < s.length() && s.charAt(idx[0]) == ']') {
                idx[0]++;
                break;
            }
            if (s.charAt(idx[0]++) != ',') throw new RuntimeException("bad comma");
        }
        return out;
    }

    private static ArrayList<String> splitTopLevel(String line) {
        ArrayList<String> parts = new ArrayList<>();
        int start = 0, depth = 0;
        boolean inStr = false;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (inStr) {
                if (ch == '"') inStr = false;
                continue;
            }
            if (ch == '"') {
                inStr = true;
            } else if (ch == '[') {
                depth++;
            } else if (ch == ']') {
                depth--;
            } else if (ch == ',' && depth == 0) {
                parts.add(line.substring(start, i));
                start = i + 1;
            }
        }
        parts.add(line.substring(start));
        return parts;
    }

    private static String formatArray(int[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(a[i]);
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = readAllInput(br);
        if (line.isEmpty()) return;
        ArrayList<String> parts = splitTopLevel(line);
        if (parts.size() < 2) throw new RuntimeException("bad input");
        int[] idx = {0};
        ArrayList<String> logs = parseStringArray(parts.get(0), idx);
        idx[0] = 0;
        ArrayList<String> keywords = parseStringArray(parts.get(1), idx);
        Solution sol = new Solution();
        System.out.println(formatArray(sol.analyzeLogKeywords(
                logs.toArray(new String[0]), keywords.toArray(new String[0]))));
    }
}
