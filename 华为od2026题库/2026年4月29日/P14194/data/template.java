import java.io.*;
import java.util.*;

public class Main {
    private static List<String> parseStringList(String s) {
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
        return list;
    }

    private static void printStringArray(String[] a) {
        System.out.print("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) System.out.print(",");
            System.out.print("\"" + a[i] + "\"");
        }
        System.out.print("]");
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        List<String> logsList = parseStringList(line);
        String[] logs = new String[logsList.size()];
        for (int i = 0; i < logsList.size(); i++) {
            logs[i] = logsList.get(i);
        }

        Solution solution = new Solution();
        String[] ans = solution.findAnomalyLogs(logs);

        if (ans.length == 0) {
            System.out.print("NONE");
        } else {
            printStringArray(ans);
        }
    }
}
