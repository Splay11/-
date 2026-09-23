import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.StringTokenizer;

public class Main {
    static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int v) { val = v; }
    }

    static TreeNode buildTree(String[] tokens) {
        if (tokens.length == 0 || tokens[0].equals("null")) return null;
        TreeNode root = new TreeNode(Integer.parseInt(tokens[0]));
        ArrayDeque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < tokens.length) {
            TreeNode node = q.poll();
            if (i < tokens.length) {
                if (!tokens[i].equals("null")) {
                    node.left = new TreeNode(Integer.parseInt(tokens[i]));
                    q.add(node.left);
                }
                i++;
            }
            if (i < tokens.length) {
                if (!tokens[i].equals("null")) {
                    node.right = new TreeNode(Integer.parseInt(tokens[i]));
                    q.add(node.right);
                }
                i++;
            }
        }
        return root;
    }

    static boolean same(TreeNode a, TreeNode b) {
        if (a == null && b == null) return true;
        if (a == null || b == null || a.val != b.val) return false;
        return same(a.left, b.left) && same(a.right, b.right);
    }

    // 判断 sub 是否为 root 的子树
    static boolean isSubtree(TreeNode root, TreeNode sub) {
        if (sub == null) return true;
        if (root == null) return false;
        if (same(root, sub)) return true;
        return isSubtree(root.left, sub) || isSubtree(root.right, sub);
    }

    static String[] readTokens(BufferedReader br, int n) throws IOException {
        StringTokenizer st = new StringTokenizer(br.readLine());
        String[] tokens = new String[n];
        for (int i = 0; i < n; i++) tokens[i] = st.nextToken();
        return tokens;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n1 = Integer.parseInt(br.readLine().trim());
        String[] t1 = readTokens(br, n1);
        int n2 = Integer.parseInt(br.readLine().trim());
        String[] t2 = readTokens(br, n2);
        System.out.println(isSubtree(buildTree(t1), buildTree(t2)) ? "true" : "false");
    }
}
