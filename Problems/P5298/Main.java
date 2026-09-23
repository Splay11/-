import java.io.*;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 读入长度
    int n = Integer.parseInt(br.readLine().trim());
    // 读入仅含小写字母的报文
    char[] s = br.readLine().trim().toCharArray();
    int i = 0;
    // 前缀 z 已经是最大字母，不能再后继
    while (i < n && s[i] == 'z') i++;
    if (i == n) {
      // 全 z，输出原串
      System.out.println(new String(s));
      return;
    }
    // 让第一个非 z 变成 z，后面同一段必须加相同次数
    int k = 'z' - s[i];
    int j = i;
    // 延伸到再纳入就会越过 z 的位置之前
    while (j < n && s[j] + k <= 'z') j++;
    for (int p = i; p < j; p++) {
      // 子串 [i, j) 同时做 k 次后继，z 之后回到 a
      s[p] = (char) ('a' + (s[p] - 'a' + k) % 26);
    }
    System.out.println(new String(s));
  }
}
