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

    static class Item {
        TreeNode node;
        long idx;
        Item(TreeNode n, long i) { node = n; idx = i; }
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

    // 层序编号法求最大宽度，每层相对归零
    static int widthOfBinaryTree(TreeNode root) {
        if (root == null) return 0;
        ArrayDeque<Item> q = new ArrayDeque<>();
        q.add(new Item(root, 0));
        int ans = 0;
        while (!q.isEmpty()) {
            int size = q.size();
            long left = q.peek().idx;
            long right = left;
            for (int i = 0; i < size; i++) {
                Item cur = q.poll();
                long idx = cur.idx - left;
                right = idx;
                if (cur.node.left != null) q.add(new Item(cur.node.left, idx * 2));
                if (cur.node.right != null) q.add(new Item(cur.node.right, idx * 2 + 1));
            }
            ans = Math.max(ans, (int) (right + 1));
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        StringTokenizer st = new StringTokenizer(line);
        String[] tokens = new String[st.countTokens()];
        for (int i = 0; i < tokens.length; i++) tokens[i] = st.nextToken();
        System.out.println(widthOfBinaryTree(buildTree(tokens)));
    }
}
