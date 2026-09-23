import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static class Node {
        int val;
        Node left;
        Node right;
        Node(int v) {
            val = v;
        }
    }

    // 按层序（含 null）还原二叉树。题目保证结果是合法 BST
    static Node buildTree(String[] tokens) {
        if (tokens.length == 0 || tokens[0].equals("null")) {
            return null;
        }
        Node root = new Node(Integer.parseInt(tokens[0]));
        List<Node> q = new ArrayList<>();
        q.add(root);
        int i = 1;
        int idx = 0;
        while (idx < q.size() && i < tokens.length) {
            Node cur = q.get(idx++);
            // 先读左孩子，null 表示没有左子树
            if (i < tokens.length) {
                if (!tokens[i].equals("null")) {
                    cur.left = new Node(Integer.parseInt(tokens[i]));
                    q.add(cur.left);
                }
                i++;
            }
            // 再读右孩子
            if (i < tokens.length) {
                if (!tokens[i].equals("null")) {
                    cur.right = new Node(Integer.parseInt(tokens[i]));
                    q.add(cur.right);
                }
                i++;
            }
        }
        return root;
    }

    // BST 反过来中序（右-根-左）就是从大到小。用栈模拟，避免链状树递归爆栈
    static int kthLargest(Node root, int cnt) {
        List<Node> stack = new ArrayList<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {
            // 一路向右压栈，右边全是更大的值
            while (cur != null) {
                stack.add(cur);
                cur = cur.right;
            }
            cur = stack.remove(stack.size() - 1);
            cnt--;
            if (cnt == 0) {
                return cur.val;
            }
            // 再转向左子树，那里全是更小的值
            cur = cur.left;
        }
        return 0;
    }

    static int solve(String[] tokens, int cnt) {
        Node root = buildTree(tokens);
        return kthLargest(root, cnt);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int cnt = Integer.parseInt(st.nextToken());
        // 第二行 n 个记号：数字或 null
        st = new StringTokenizer(br.readLine());
        String[] tokens = new String[n];
        for (int i = 0; i < n; i++) {
            tokens[i] = st.nextToken();
        }
        System.out.println(solve(tokens, cnt));
    }
}
