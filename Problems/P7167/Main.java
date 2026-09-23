import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {
    // 回答 x 表示该颜色一共 x+1 只；同回答尽量塞进同一颜色组
    static int solve(int[] answers) {
        HashMap<Integer, Integer> cnt = new HashMap<Integer, Integer>();
        for (int i = 0; i < answers.length; i++) {
            Integer old = cnt.get(answers[i]);
            if (old == null) {
                cnt.put(answers[i], 1);
            } else {
                cnt.put(answers[i], old + 1);
            }
        }
        int ans = 0;
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            int x = e.getKey();
            int c = e.getValue();
            int size = x + 1;
            int groups = (c + size - 1) / size;
            ans += groups * size;
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] answers = new int[n];
        for (int i = 0; i < n; i++) {
            answers[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(answers));
    }
}
