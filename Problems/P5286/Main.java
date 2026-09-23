import java.io.*;
import java.util.*;

public class Main {
  static long solve(int n, long k, long[] a) {
    HashMap<Long, Integer> cnt = new HashMap<>();
    for (long x : a) cnt.put(x, cnt.getOrDefault(x, 0) + 1);
    long ans = 0;
    HashSet<Long> seen = new HashSet<>();
    for (Map.Entry<Long, Integer> e : cnt.entrySet()) {
      long x = e.getKey();
      if (seen.contains(x)) continue;
      long y = k - x;
      if (x == y) {
        ans += Math.max(0, e.getValue() - 1);
        seen.add(x);
      } else if (cnt.containsKey(y)) {
        ans += Math.min(e.getValue(), cnt.get(y));
        seen.add(x);
        seen.add(y);
      }
    }
    return ans;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] nk = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(nk[0]);
    long k = Long.parseLong(nk[1]);
    String[] sp = br.readLine().trim().split("\\s+");
    long[] a = new long[n];
    for (int i = 0; i < n; i++) a[i] = Long.parseLong(sp[i]);
    System.out.println(solve(n, k, a));
  }
}
