import java.io.*;
import java.util.*;

public class Main {
  static class FastScanner {
    private final InputStream in;
    private final byte[] buf = new byte[1 << 16];
    private int ptr, len;

    FastScanner(InputStream in) {
      this.in = in;
    }

    private int read() throws IOException {
      if (ptr >= len) {
        len = in.read(buf);
        ptr = 0;
        if (len <= 0) return -1;
      }
      return buf[ptr++];
    }

    String next() throws IOException {
      StringBuilder sb = new StringBuilder();
      int c;
      while ((c = read()) <= ' ') {
        if (c == -1) return null;
      }
      do {
        sb.append((char) c);
        c = read();
      } while (c > ' ');
      return sb.toString();
    }

    int nextInt() throws IOException {
      return Integer.parseInt(next());
    }

    long nextLong() throws IOException {
      return Long.parseLong(next());
    }
  }

  static TreeMap<Long, Integer> posCnt = new TreeMap<>();
  static Map<Long, Integer> gapCnt = new HashMap<>();
  static PriorityQueue<Long> gapHeap = new PriorityQueue<>(Comparator.reverseOrder());

  static void addGap(long diff) {
    long g = diff / 2;
    if (g > 0) {
      gapCnt.merge(g, 1, Integer::sum);
      gapHeap.offer(g);
    }
  }

  static void removeGap(long diff) {
    long g = diff / 2;
    if (g > 0) {
      int c = gapCnt.getOrDefault(g, 0) - 1;
      if (c == 0) gapCnt.remove(g);
      else gapCnt.put(g, c);
    }
  }

  static void insertPos(long y) {
    if (posCnt.containsKey(y)) {
      posCnt.merge(y, 1, Integer::sum);
      return;
    }
    Long succ = posCnt.ceilingKey(y);
    Long pred = posCnt.lowerKey(y);
    if (pred != null && succ != null) removeGap(succ - pred);
    if (pred != null) addGap(y - pred);
    if (succ != null) addGap(succ - y);
    posCnt.put(y, 1);
  }

  static void removePos(long v) {
    int c = posCnt.get(v);
    if (c == 1) {
      posCnt.remove(v);
      Long pred = posCnt.lowerKey(v);
      Long succ = posCnt.higherKey(v);
      if (pred != null) removeGap(v - pred);
      if (succ != null) removeGap(succ - v);
      if (pred != null && succ != null) addGap(succ - pred);
    } else {
      posCnt.put(v, c - 1);
    }
  }

  static long maxG() {
    while (!gapHeap.isEmpty() && gapCnt.getOrDefault(gapHeap.peek(), 0) == 0) {
      gapHeap.poll();
    }
    return gapHeap.isEmpty() ? 0 : gapHeap.peek();
  }

  public static void main(String[] args) throws Exception {
    FastScanner fs = new FastScanner(System.in);
    int n = fs.nextInt();
    int m = fs.nextInt();
    long[] b = new long[n];
    for (int i = 0; i < n; i++) {
      b[i] = fs.nextLong();
      posCnt.merge(b[i], 1, Integer::sum);
    }
    List<Long> sorted = new ArrayList<>(posCnt.keySet());
    for (int i = 0; i < sorted.size() - 1; i++) {
      addGap(sorted.get(i + 1) - sorted.get(i));
    }

    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < m; i++) {
      int x = fs.nextInt() - 1;
      long y = fs.nextLong();
      long old = b[x];
      if (old != y) {
        removePos(old);
        insertPos(y);
        b[x] = y;
      }
      sb.append(maxG()).append('\n');
    }
    System.out.print(sb);
  }
}
