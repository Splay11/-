import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
  static String src;
  static int pos;

  static void skip() {
    while (pos < src.length()) {
      char c = src.charAt(pos);
      if (c != ' ' && c != '\n' && c != '\r' && c != '\t') break;
      pos++;
    }
  }

  static void eat(char c) {
    skip();
    pos++;
  }

  static double readNum() {
    skip();
    int j = pos;
    if (src.charAt(j) == '-') j++;
    while (j < src.length()) {
      char c = src.charAt(j);
      if ((c >= '0' && c <= '9') || c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') j++;
      else break;
    }
    double v = Double.parseDouble(src.substring(pos, j));
    pos = j;
    return v;
  }

  static double[] readVec() {
    eat('[');
    skip();
    if (src.charAt(pos) == ']') {
      pos++;
      return new double[0];
    }
    double[] tmp = new double[64];
    int n = 0;
    while (true) {
      if (n == tmp.length) {
        double[] b = new double[n * 2];
        System.arraycopy(tmp, 0, b, 0, n);
        tmp = b;
      }
      tmp[n++] = readNum();
      skip();
      if (src.charAt(pos) == ',') {
        pos++;
        continue;
      }
      eat(']');
      break;
    }
    double[] a = new double[n];
    System.arraycopy(tmp, 0, a, 0, n);
    return a;
  }

  static int[] solve(double[][] feats, double[] labs, double[][] test) {
    int n = feats.length;
    int d = feats[0].length + 1;
    double[][] X = new double[n][d];
    double[] t = new double[n];
    for (int i = 0; i < n; i++) {
      X[i][0] = 1.0;
      for (int j = 0; j < feats[i].length; j++) X[i][j + 1] = feats[i][j];
      t[i] = labs[i] == 0 ? -1.0 : 1.0;
    }
    // 权向量从 0 起，固定 10 轮，分错才加一刀
    double[] h = new double[d];
    for (int ep = 0; ep < 10; ep++) {
      for (int i = 0; i < n; i++) {
        double score = 0;
        for (int j = 0; j < d; j++) score += h[j] * X[i][j];
        double pred = score >= 0 ? 1.0 : -1.0;
        if (pred != t[i]) {
          for (int j = 0; j < d; j++) h[j] += t[i] * X[i][j];
        }
      }
    }
    int[] ans = new int[test.length];
    for (int i = 0; i < test.length; i++) {
      double score = h[0];
      for (int j = 0; j < test[i].length; j++) score += h[j + 1] * test[i][j];
      ans[i] = score >= 0 ? 1 : 0;
    }
    return ans;
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringBuilder sb = new StringBuilder();
    String line;
    while ((line = br.readLine()) != null) sb.append(line);
    src = sb.toString();
    pos = 0;
    // 只解析 train / test 两个键
    double[][] feats = new double[0][];
    double[] labs = new double[0];
    double[][] test = new double[0][];
    eat('{');
    while (true) {
      skip();
      if (src.charAt(pos) == '}') break;
      eat('"');
      int keyStart = pos;
      while (src.charAt(pos) != '"') pos++;
      String key = src.substring(keyStart, pos);
      pos++;
      eat(':');
      if (key.equals("train")) {
        eat('[');
        double[][] tf = new double[16][];
        double[] tl = new double[16];
        int tn = 0;
        skip();
        if (src.charAt(pos) != ']') {
          while (true) {
            eat('[');
            double[] f = readVec();
            eat(',');
            double lab = readNum();
            eat(']');
            if (tn == tf.length) {
              double[][] nf = new double[tn * 2][];
              double[] nl = new double[tn * 2];
              System.arraycopy(tf, 0, nf, 0, tn);
              System.arraycopy(tl, 0, nl, 0, tn);
              tf = nf;
              tl = nl;
            }
            tf[tn] = f;
            tl[tn] = lab;
            tn++;
            skip();
            if (src.charAt(pos) == ',') {
              pos++;
              continue;
            }
            break;
          }
        }
        eat(']');
        feats = new double[tn][];
        labs = new double[tn];
        System.arraycopy(tf, 0, feats, 0, tn);
        System.arraycopy(tl, 0, labs, 0, tn);
      } else if (key.equals("test")) {
        eat('[');
        double[][] tt = new double[16][];
        int tn = 0;
        skip();
        if (src.charAt(pos) != ']') {
          while (true) {
            double[] f = readVec();
            if (tn == tt.length) {
              double[][] nf = new double[tn * 2][];
              System.arraycopy(tt, 0, nf, 0, tn);
              tt = nf;
            }
            tt[tn++] = f;
            skip();
            if (src.charAt(pos) == ',') {
              pos++;
              continue;
            }
            break;
          }
        }
        eat(']');
        test = new double[tn][];
        System.arraycopy(tt, 0, test, 0, tn);
      }
      skip();
      if (src.charAt(pos) == ',') pos++;
    }
    int[] ans = solve(feats, labs, test);
    StringBuilder out = new StringBuilder();
    out.append('[');
    for (int i = 0; i < ans.length; i++) {
      if (i > 0) out.append(", ");
      out.append(ans[i]);
    }
    out.append(']');
    System.out.println(out.toString());
  }
}
