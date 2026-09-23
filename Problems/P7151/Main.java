import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {
    // 先计数再排序，取前 k 个高频单词
    static List<String> solve(String[] words, int k) {
        Map<String, Integer> cnt = new HashMap<String, Integer>();
        for (int i = 0; i < words.length; i++) {
            String w = words[i];
            Integer old = cnt.get(w);
            cnt.put(w, old == null ? 1 : old + 1);
        }
        List<String> items = new ArrayList<String>(cnt.keySet());
        Collections.sort(items, new Comparator<String>() {
            public int compare(String a, String b) {
                int ca = cnt.get(a);
                int cb = cnt.get(b);
                // 次数从大到小
                if (ca != cb) {
                    return cb - ca;
                }
                // 次数相同按字典序从小到大
                return a.compareTo(b);
            }
        });
        return items.subList(0, k);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        String[] words = new String[n];
        for (int i = 0; i < n; i++) {
            words[i] = st.nextToken();
        }
        List<String> ans = solve(words, k);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb.toString());
    }
}
