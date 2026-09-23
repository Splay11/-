import java.io.*;
import java.util.*;

public class Main {
    private static String[] parseTwoQuotedStrings(String line) {
        ArrayList<String> res = new ArrayList<>();
        int i = 0;
        for (int k = 0; k < 2; k++) {
            while (i < line.length() && line.charAt(i) != '"') i++;
            if (i >= line.length()) throw new RuntimeException("bad input");
            i++;
            int start = i;
            while (i < line.length() && line.charAt(i) != '"') i++;
            res.add(line.substring(start, i));
            if (i < line.length() && line.charAt(i) == '"') i++;
            if (k == 0 && i < line.length() && line.charAt(i) == ',') i++;
        }
        return res.toArray(new String[0]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        String[] parts = parseTwoQuotedStrings(line);
        int ans = new Solution().minDistinctAfterSwap(parts[0], parts[1]);
        System.out.println(ans);
    }
}
