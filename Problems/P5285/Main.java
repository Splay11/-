import java.io.*;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt();
    long A = sc.nextLong(), B = sc.nextLong();
    long ca = 0, cb = 0;
    for (int i = 0; i < n; i++) {
      long x = sc.nextLong();
      if (x == A) ca++;
      if (x == B) cb++;
    }
    double ans = 1.0 * n * n / (ca * cb);
    System.out.printf("%.1f\n", ans);
  }
}
