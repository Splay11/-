import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.StringTokenizer;

public class Main {
    // 哈希表存前缀到银行；每个卡号从长到短试前缀，第一次命中即最长匹配
    static String[] solve(String[] prefixes, String[] banks, String[] cards) {
        HashMap<String, String> mp = new HashMap<String, String>();
        for (int i = 0; i < prefixes.length; i++) {
            mp.put(prefixes[i], banks[i]);
        }
        String[] answers = new String[cards.length];
        for (int i = 0; i < cards.length; i++) {
            String card = cards[i];
            String ans = "UNKNOWN";
            int upper = card.length();
            if (upper > 20) {
                upper = 20;
            }
            // 从长到短枚举，避免取到输入顺序里较短的那条规则
            for (int L = upper; L >= 1; L--) {
                String pref = card.substring(0, L);
                String bank = mp.get(pref);
                if (bank != null) {
                    ans = bank;
                    break;
                }
            }
            answers[i] = ans;
        }
        return answers;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] prefixes = new String[n];
        String[] banks = new String[n];
        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            prefixes[i] = st.nextToken();
            banks[i] = st.nextToken();
        }
        int m = Integer.parseInt(br.readLine().trim());
        String[] cards = new String[m];
        for (int i = 0; i < m; i++) {
            cards[i] = br.readLine().trim();
        }
        String[] answers = solve(prefixes, banks, cards);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < answers.length; i++) {
            sb.append(answers[i]).append('\n');
        }
        System.out.print(sb.toString());
    }
}
