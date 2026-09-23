import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 从两端拿 k 张 = 中间留下连续 n-k 张；留下段越小，拿走的点数越大
    static int solve(int[] cards, int k) {
        int n = cards.length;
        long total = 0;
        for (int i = 0; i < n; i++) {
            total += cards[i];
        }
        int leave = n - k;
        // 必须拿完全部牌时，中间不留牌
        if (leave == 0) {
            return (int) total;
        }
        long window = 0;
        for (int i = 0; i < leave; i++) {
            window += cards[i];
        }
        long best = window;
        for (int i = leave; i < n; i++) {
            window += cards[i] - cards[i - leave];
            if (window < best) {
                best = window;
            }
        }
        return (int) (total - best);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] cards = new int[n];
        for (int i = 0; i < n; i++) {
            cards[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(cards, k));
    }
}
