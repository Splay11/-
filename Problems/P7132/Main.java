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

    // 按层序（含 null）还原二叉树。空序列表示空树
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
            // 先读左孩子，null 表示这个位置没有节点
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

    // DFS + 回溯：从根走到叶子，和等于 target 就记下路径。先左后右
    static void dfs(Node node, int remain, List<Integer> path, List<List<Integer>> ans) {
        if (node == null) {
            return;
        }
        path.add(node.val);
        remain -= node.val;
        // 叶子：没有左右孩子
        if (node.left == null && node.right == null) {
            if (remain == 0) {
                ans.add(new ArrayList<>(path));
            }
        } else {
            dfs(node.left, remain, path, ans);
            dfs(node.right, remain, path, ans);
        }
        // 回溯，把当前节点从路径里拿掉
        path.remove(path.size() - 1);
    }

    static List<List<Integer>> pathSum(Node root, int target) {
        List<List<Integer>> ans = new ArrayList<>();
        // 节点值有负数，不能因为当前和已经超过就剪枝
        dfs(root, target, new ArrayList<>(), ans);
        return ans;
    }

    static List<List<Integer>> solve(String[] tokens, int target) {
        Node root = buildTree(tokens);
        return pathSum(root, target);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int target = Integer.parseInt(st.nextToken());
        String[] tokens = new String[n];
        // n=0 时没有第二行，不要再 readLine
        if (n > 0) {
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                tokens[i] = st.nextToken();
            }
        }
        List<List<Integer>> paths = solve(tokens, target);
        StringBuilder sb = new StringBuilder();
        sb.append(paths.size()).append('\n');
        for (List<Integer> p : paths) {
            for (int j = 0; j < p.size(); j++) {
                if (j > 0) {
                    sb.append(' ');
                }
                sb.append(p.get(j));
            }
            sb.append('\n');
        }
        System.out.print(sb);
    }
}
