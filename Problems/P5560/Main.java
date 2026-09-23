import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static int[] segSum, segMn, segMx, lazyFlip;
    static char[] w;

    // 用孩子重算这一段的和、最小前缀、最大前缀
    static void pull(int p) {
        int left = p << 1;
        int right = left | 1;
        segSum[p] = segSum[left] + segSum[right];
        int crossMn = segSum[left] + segMn[right];
        int crossMx = segSum[left] + segMx[right];
        segMn[p] = segMn[left] < crossMn ? segMn[left] : crossMn;
        segMx[p] = segMx[left] > crossMx ? segMx[left] : crossMx;
    }

    // 整段开合对调：和取反，最小前缀与最大前缀互换后再变号
    static void apply(int p) {
        segSum[p] = -segSum[p];
        int oldMn = segMn[p];
        segMn[p] = -segMx[p];
        segMx[p] = -oldMn;
        lazyFlip[p] ^= 1;
    }

    static void push(int p) {
        if (lazyFlip[p] != 0) {
            apply(p << 1);
            apply((p << 1) | 1);
            lazyFlip[p] = 0;
        }
    }

    static void build(int p, int l, int r) {
        if (l == r) {
            int val = w[l - 1] == '[' ? 1 : -1;
            segSum[p] = val;
            segMn[p] = val;
            segMx[p] = val;
            return;
        }
        int mid = (l + r) >> 1;
        build(p << 1, l, mid);
        build((p << 1) | 1, mid + 1, r);
        pull(p);
    }

    static void flip(int p, int l, int r, int a, int b) {
        if (a <= l && r <= b) {
            apply(p);
            return;
        }
        push(p);
        int mid = (l + r) >> 1;
        if (a <= mid) {
            flip(p << 1, l, mid, a, b);
        }
        if (b > mid) {
            flip((p << 1) | 1, mid + 1, r, a, b);
        }
        pull(p);
    }

    // 返回值：这一段的区间和、最小前缀和
    static int[] ask(int p, int l, int r, int a, int b) {
        if (a <= l && r <= b) {
            return new int[] {segSum[p], segMn[p]};
        }
        push(p);
        int mid = (l + r) >> 1;
        if (b <= mid) {
            return ask(p << 1, l, mid, a, b);
        }
        if (a > mid) {
            return ask((p << 1) | 1, mid + 1, r, a, b);
        }
        int[] left = ask(p << 1, l, mid, a, b);
        int[] right = ask((p << 1) | 1, mid + 1, r, a, b);
        int cross = left[0] + right[1];
        int best = left[1] < cross ? left[1] : cross;
        return new int[] {left[0] + right[0], best};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int m = Integer.parseInt(br.readLine().trim());
        int t = Integer.parseInt(br.readLine().trim());
        w = br.readLine().trim().toCharArray();
        int cap = m * 4 + 20;
        segSum = new int[cap];
        segMn = new int[cap];
        segMx = new int[cap];
        lazyFlip = new int[cap];
        build(1, 1, m);
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < t; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int op = Integer.parseInt(st.nextToken());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            if (op == 1) {
                flip(1, 1, m, a, b);
            } else {
                int[] res = ask(1, 1, m, a, b);
                // 和为 0 且最小前缀不小于 0，这一段才配平
                out.append(res[0] == 0 && res[1] >= 0 ? 1 : 0).append('\n');
            }
        }
        System.out.print(out);
    }
}
