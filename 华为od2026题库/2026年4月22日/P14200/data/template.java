import java.io.*;
import java.util.*;
import java.util.Arrays;
public class Main {
    private static String[] parseStringArray(String s) {
        List<String> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inString = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') {
                if (inString) {
                    list.add(cur.toString());
                    cur.setLength(0);
                }
                inString = !inString;
            } else if (inString) {
                cur.append(c);
            }
        }
        return list.toArray(new String[0]);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        String[] docs = parseStringArray(line);

        Solution solution = new Solution();
        System.out.println(solution.featureExtraction(docs));
    }
}
