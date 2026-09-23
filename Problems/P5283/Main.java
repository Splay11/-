import java.io.*;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] nk = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(nk[0]);
    long k = Long.parseLong(nk[1]);
    TreeMap<Long, Long> mp = new TreeMap<>();
    for (int i = 0; i < n; i++) {
      String[] sp = br.readLine().trim().split("\\s+");
      long a = Long.parseLong(sp[0]), b = Long.parseLong(sp[1]);
      mp.put(a, mp.getOrDefault(a, 0L) + b);
    }
    long s = 0;
    for (long v : mp.values()) s += v;
    if (s <= k) {
      System.out.println(0);
      return;
    }
    for (Map.Entry<Long, Long> e : mp.entrySet()) {
      s -= e.getValue();
      if (s <= k) {
        System.out.println(e.getKey() + 1);
        return;
      }
    }
    System.out.println(mp.lastKey() + 1);
  }
}
