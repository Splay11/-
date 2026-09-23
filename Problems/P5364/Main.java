import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        int d = sc.nextInt();
        int[] v = new int[m];
        for (int i = 0; i < m; i++) {
            v[i] = sc.nextInt();
        }
        // 与 d 同奇偶的才能让 (x+d) 为偶数；diff 只能和 same 配
        List<Integer> same = new ArrayList<Integer>();
        List<Integer> diff = new ArrayList<Integer>();
        for (int i = 0; i < m; i++) {
            if (v[i] % 2 == d % 2) {
                same.add(v[i]);
            } else {
                diff.add(v[i]);
            }
        }
        List<int[]> pairs = new ArrayList<int[]>();
        int i = 0, j = 0;
        // 先把不同奇偶的配给 same
        while (i < diff.size() && j < same.size()) {
            pairs.add(new int[] {diff.get(i), same.get(j)});
            i++;
            j++;
        }
        // 剩下的 same 两两配对
        while (j + 1 < same.size()) {
            pairs.add(new int[] {same.get(j), same.get(j + 1)});
            j += 2;
        }
        System.out.println(pairs.size());
        for (int t = 0; t < pairs.size(); t++) {
            System.out.println(pairs.get(t)[0] + " " + pairs.get(t)[1]);
        }
        sc.close();
    }
}
