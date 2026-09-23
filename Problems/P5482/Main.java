import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class Main {
    // 枚举最终种类数：按每种最大价值从大到小加入，续选部分用堆维护前 r 大
    static long maxScore(int[] types, int[] values, int k) {
        Map<Integer, ArrayList<Long>> mp = new HashMap<Integer, ArrayList<Long>>();
        for (int i = 0; i < types.length; i++) {
            ArrayList<Long> vs = mp.get(types[i]);
            if (vs == null) {
                vs = new ArrayList<Long>();
                mp.put(types[i], vs);
            }
            vs.add((long) values[i]);
        }
        List<ArrayList<Long>> arr = new ArrayList<ArrayList<Long>>();
        for (ArrayList<Long> vs : mp.values()) {
            Collections.sort(vs, Collections.reverseOrder());
            arr.add(vs);
        }
        Collections.sort(arr, new Comparator<ArrayList<Long>>() {
            public int compare(ArrayList<Long> a, ArrayList<Long> b) {
                return Long.compare(b.get(0), a.get(0));
            }
        });

        long ans = 0;
        boolean found = false;
        PriorityQueue<Long> extras = new PriorityQueue<Long>(Collections.reverseOrder());
        PriorityQueue<Long> used = new PriorityQueue<Long>();
        long sumUsed = 0;
        long head = 0;
        int total = 0;
        int d = 0;
        for (int gi = 0; gi < arr.size(); gi++) {
            d++;
            ArrayList<Long> vs = arr.get(gi);
            // 选中这一种：必须拿它最贵的一朵，剩下的进备用堆
            head += vs.get(0);
            total += vs.size();
            for (int p = 1; p < vs.size(); p++) {
                extras.add(vs.get(p));
            }
            int r = k - d;
            if (r < 0) {
                break;
            }
            // used 里只保留当前还需要的 r 朵「同种续选」
            while (!used.isEmpty() && used.size() > r) {
                long x = used.poll();
                sumUsed -= x;
                extras.add(x);
            }
            while (!extras.isEmpty() && used.size() < r) {
                long x = extras.poll();
                used.add(x);
                sumUsed += x;
            }
            while (!extras.isEmpty() && !used.isEmpty() && extras.peek() > used.peek()) {
                long bad = used.poll();
                sumUsed -= bad;
                long good = extras.poll();
                used.add(good);
                sumUsed += good;
                extras.add(bad);
            }
            // 已选种类凑得出 k 朵时，更新答案：价值和 + 种类平方
            if (total >= k && used.size() == r) {
                long cur = head + sumUsed + 1L * d * d;
                if (!found || cur > ans) {
                    ans = cur;
                    found = true;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        // n 可达 1e5，用 BufferedReader 读三行
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] types = new int[n];
        for (int i = 0; i < n; i++) {
            types[i] = Integer.parseInt(st.nextToken());
        }
        st = new StringTokenizer(br.readLine());
        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(maxScore(types, values, k));
    }
}
