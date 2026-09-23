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

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int split = line.indexOf("],[");
        String namesStr = line.substring(0, split + 1);
        String ballotStr = line.substring(split + 2);

        ArrayList<String> names = new ArrayList<>(parseStringList(namesStr));
        ArrayList<String> ballotTickets = new ArrayList<>(parseStringList(ballotStr));

        Solution solution = new Solution();
        System.out.println("\"" + solution.getClassMonitor(names, ballotTickets) + "\"");
    }
}
