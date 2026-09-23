import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
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

    // 锯齿形层序：奇层左->右，偶层右->左
    static List<List<Integer>> zigzag(TreeNode root) {
        List<List<Integer>> ans = new ArrayList<>();
        if (root == null) return ans;
        ArrayDeque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        boolean leftToRight = true;
        while (!q.isEmpty()) {
            int size = q.size();
            Integer[] level = new Integer[size];
            for (int i = 0; i < size; i++) {
                TreeNode node = q.poll();
                int idx = leftToRight ? i : size - 1 - i;
                level[idx] = node.val;
                if (node.left != null) q.add(node.left);
                if (node.right != null) q.add(node.right);
            }
            List<Integer> row = new ArrayList<>();
            for (Integer x : level) row.add(x);
            ans.add(row);
            leftToRight = !leftToRight;
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        String[] tokens = new String[n];
        for (int i = 0; i < n; i++) tokens[i] = st.nextToken();
        List<List<Integer>> levels = zigzag(buildTree(tokens));
        System.out.println(levels.size());
        for (List<Integer> row : levels) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < row.size(); i++) {
                if (i > 0) sb.append(' ');
                sb.append(row.get(i));
            }
            System.out.println(sb.toString());
        }
    }
}
