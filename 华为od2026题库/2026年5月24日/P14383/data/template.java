import java.io.*;
import java.util.*;

public class Main {
    private static int[] parseArray1d(String s) throws Exception {
        ArrayList<Integer> vals = new ArrayList<>();
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
        if (i >= s.length() || s.charAt(i) != '[') throw new Exception("bad");
        i++;
        while (true) {
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            int sign = 1;
            if (i < s.length() && s.charAt(i) == '-') {
                sign = -1;
                i++;
            }
            int v = 0;
            boolean ok = false;
            while (i < s.length() && Character.isDigit(s.charAt(i))) {
                ok = true;
                v = v * 10 + (s.charAt(i) - '0');
                i++;
            }
            if (!ok) throw new Exception("bad");
            vals.add(sign * v);
            while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
            if (i < s.length() && s.charAt(i) == ']') {
                i++;
                break;
            }
            if (i >= s.length() || s.charAt(i) != ',') throw new Exception("bad");
            i++;
        }
        int[] a = new int[vals.size()];
        for (int t = 0; t < vals.size(); t++) a[t] = vals.get(t);
        return a;
    }

    private static Object[] parseLine(String line) throws Exception {
        line = line.trim();
        int d = 0, end = -1;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '[') d++;
            else if (c == ']') {
                d--;
                if (d == 0) {
                    end = i;
                    break;
                }
            }
        }
        if (end < 0) throw new Exception("bad");
        String arrStr = line.substring(0, end + 1);
        String tail = line.substring(end + 1).trim();
        if (tail.length() == 0 || tail.charAt(0) != ',') throw new Exception("bad");
        int k = Integer.parseInt(tail.substring(1).trim());
        return new Object[] {parseArray1d(arrStr), k};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        Object[] pk = parseLine(line);
        int[] timestamps = (int[]) pk[0];
        int minInterval = (Integer) pk[1];
        Solution sol = new Solution();
        System.out.println(sol.countValidPlans(timestamps, minInterval));
    }
}
