import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    static class Node {
        Node[] ch = new Node[26];
        boolean end;
    }

    // 把一个词根插入字典树
    static void insert(Node root, String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int id = word.charAt(i) - 'a';
            if (cur.ch[id] == null) {
                cur.ch[id] = new Node();
            }
            cur = cur.ch[id];
        }
        cur.end = true;
    }

    // 沿单词往下走，第一次碰到结束标记就是最短词根；否则整词保留
    static String shortestRoot(Node root, String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int id = word.charAt(i) - 'a';
            if (cur.ch[id] == null) {
                return word;
            }
            cur = cur.ch[id];
            if (cur.end) {
                return word.substring(0, i + 1);
            }
        }
        return word;
    }

    static String solve(String[] dictionary, String sentence) {
        Node root = new Node();
        for (String w : dictionary) {
            insert(root, w);
        }
        StringBuilder ans = new StringBuilder();
        int i = 0;
        int n = sentence.length();
        while (i < n) {
            int j = i;
            while (j < n && sentence.charAt(j) != ' ') {
                j++;
            }
            String word = sentence.substring(i, j);
            String rep = shortestRoot(root, word);
            if (ans.length() > 0) {
                ans.append(' ');
            }
            ans.append(rep);
            i = j + 1;
        }
        return ans.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        String[] dictionary = new String[n];
        for (int i = 0; i < n; i++) {
            dictionary[i] = st.nextToken();
        }
        // 第三行是整句，可能接近 1e6
        String sentence = br.readLine();
        System.out.println(solve(dictionary, sentence));
    }
}
