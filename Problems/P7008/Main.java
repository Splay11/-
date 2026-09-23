import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Main {
    static List<List<Integer>> parseLists(String s) {
        String inner = s.substring(1, s.length() - 1);
        List<List<Integer>> lists = new ArrayList<List<Integer>>();
        int n = inner.length();
        int i = 0;
        while (i < n) {
            if (inner.charAt(i) == ',') {
                i++;
                continue;
            }
            int j = i + 1;
            while (j < n && inner.charAt(j) != '}') j++;
            String body = inner.substring(i + 1, j);
            List<Integer> cur = new ArrayList<Integer>();
            if (body.length() > 0) {
                int x = 0;
                boolean inNum = false;
                for (int k = 0; k < body.length(); k++) {
                    char c = body.charAt(k);
                    if (c == ',') {
                        cur.add(x);
                        x = 0;
                        inNum = false;
                    } else {
                        x = x * 10 + (c - '0');
                        inNum = true;
                    }
                }
                if (inNum) cur.add(x);
            }
            lists.add(cur);
            i = j + 1;
        }
        return lists;
    }

    static List<Integer> mergeRev(List<List<Integer>> lists) {
        List<Integer> out = new ArrayList<Integer>();
        for (int i = lists.size() - 1; i >= 0; i--) {
            out.addAll(lists.get(i));
        }
        return out;
    }

    static String formatList(List<Integer> vals) {
        if (vals.isEmpty()) return "{}";
        StringBuilder sb = new StringBuilder();
        sb.append('{');
        for (int i = 0; i < vals.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append(vals.get(i));
        }
        sb.append('}');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        System.out.println(formatList(mergeRev(parseLists(line))));
    }
}
