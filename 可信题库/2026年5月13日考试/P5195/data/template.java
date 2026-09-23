import java.io.*;
import java.util.*;

public class Main {
    private static int[] parseArray1d(String s) throws Exception {
        s = s.trim();
        if (s.isEmpty() || s.charAt(0) != '[') throw new Exception("bad");
        ArrayList<Integer> vals = new ArrayList<>();
        int i = 1;
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
        int[] arr = new int[vals.size()];
        for (int t = 0; t < vals.size(); t++) arr[t] = vals.get(t);
        return arr;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int[] numbers = parseArray1d(line);
        System.out.println(new Solution().maxConsecutiveDistance(numbers));
    }
}
