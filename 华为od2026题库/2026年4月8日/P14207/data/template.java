import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    private static final Pattern GUARD = Pattern.compile("\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)");

    private static List<List<Integer>> parseGuards(String rest) {
        List<List<Integer>> guards = new ArrayList<>();
        Matcher m = GUARD.matcher(rest);
        while (m.find()) {
            int x = Integer.parseInt(m.group(1));
            int y = Integer.parseInt(m.group(2));
            List<Integer> p = new ArrayList<>();
            p.add(x);
            p.add(y);
            guards.add(p);
        }
        return guards;
    }

    private static void printAns(List<Integer> a) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < a.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append(a.get(i));
        }
        sb.append(']');
        System.out.println(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.isEmpty()) return;
        int comma = line.indexOf(',');
        if (comma < 0) return;
        int n = Integer.parseInt(line.substring(0, comma).trim());
        String rest = line.substring(comma + 1).trim();
        List<List<Integer>> guards = parseGuards(rest);
        Solution solution = new Solution();
        List<Integer> ans = solution.countShortestPaths(n, guards);
        printAns(ans);
    }
}
