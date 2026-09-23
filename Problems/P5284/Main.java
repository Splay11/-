import java.io.*;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int n = Integer.parseInt(br.readLine().trim());
    int[] e = parse(br.readLine(), n);
    int[] a = parse(br.readLine(), n);
    int[] b = parse(br.readLine(), n);

    PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(x -> x[0]));
    long ans = 0;
    for (int i = 1; i <= n; i++) {
      int exp = e[i - 1] - 1;
      if (a[i - 1] > 0 && exp >= i) pq.add(new long[] {exp, a[i - 1]});
      while (!pq.isEmpty() && pq.peek()[0] < i) pq.poll();
      long need = b[i - 1];
      while (need > 0 && !pq.isEmpty()) {
        long[] top = pq.poll();
        if (top[0] < i) continue;
        long take = Math.min(need, top[1]);
        need -= take;
        top[1] -= take;
        if (top[1] > 0) pq.add(top);
      }
      ans += need;
    }
    System.out.println(ans);
  }

  static int[] parse(String line, int n) {
    String[] sp = line.trim().split("\\s+");
    int[] arr = new int[n];
    for (int i = 0; i < n; i++) arr[i] = Integer.parseInt(sp[i]);
    return arr;
  }
}
