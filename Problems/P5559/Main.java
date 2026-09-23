import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static final int V = 1000;

    // 二分边长，并用二维前缀和判断某个边长能否框到至少 k 件货
    static int minSide(int k, int[] cols, int[] rows) {
        if (k <= 1) {
            return 1;
        }
        int width = V + 1;
        // 列、行都从 1 编号，把每件货记到对应方格
        int[] grid = new int[width * width];
        for (int i = 0; i < cols.length; i++) {
            grid[cols[i] * width + rows[i]] = 1;
        }
        // ps[c][r] 表示列 1..c、行 1..r 这一块里的件数
        int[] ps = new int[width * width];
        for (int c = 1; c <= V; c++) {
            int running = 0;
            int cur = c * width;
            int prev = (c - 1) * width;
            for (int r = 1; r <= V; r++) {
                running += grid[cur + r];
                ps[cur + r] = ps[prev + r] + running;
            }
        }
        int low = 1;
        int high = V;
        // 边长越大越容易凑够 k 件，二分最小可行边长
        while (low < high) {
            int mid = (low + high) / 2;
            if (enough(ps, width, k, mid)) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }

    // 枚举左上角，统计边长为 side 的闭区间里有多少件货
    static boolean enough(int[] ps, int width, int k, int side) {
        int span = side - 1;
        int last = V - span;
        for (int c = 1; c <= last; c++) {
            int hi = (c + span) * width;
            int lo = (c - 1) * width;
            for (int r = 1; r <= last; r++) {
                int r2 = r + span;
                int total = ps[hi + r2] - ps[hi + r - 1] - ps[lo + r2] + ps[lo + r - 1];
                if (total >= k) {
                    return true;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int k = Integer.parseInt(br.readLine().trim());
        int p = Integer.parseInt(br.readLine().trim());
        int[] cols = new int[p];
        int[] rows = new int[p];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < p; i++) {
            cols[i] = Integer.parseInt(st.nextToken());
        }
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < p; i++) {
            rows[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(minSide(k, cols, rows));
    }
}
