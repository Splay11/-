import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 两个轴对齐矩形面积之和减去重叠
    static int solve(int ax1, int ay1, int ax2, int ay2,
                     int bx1, int by1, int bx2, int by2) {
        long areaA = (long) (ax2 - ax1) * (ay2 - ay1);
        long areaB = (long) (bx2 - bx1) * (by2 - by1);
        int w = Math.min(ax2, bx2) - Math.max(ax1, bx1);
        int h = Math.min(ay2, by2) - Math.max(ay1, by1);
        long overlap = 0;
        if (w > 0 && h > 0) {
            overlap = (long) w * h;
        }
        return (int) (areaA + areaB - overlap);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int ax1 = Integer.parseInt(st.nextToken());
        int ay1 = Integer.parseInt(st.nextToken());
        int ax2 = Integer.parseInt(st.nextToken());
        int ay2 = Integer.parseInt(st.nextToken());
        int bx1 = Integer.parseInt(st.nextToken());
        int by1 = Integer.parseInt(st.nextToken());
        int bx2 = Integer.parseInt(st.nextToken());
        int by2 = Integer.parseInt(st.nextToken());
        System.out.println(solve(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2));
    }
}
