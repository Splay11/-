import java.util.*;

public class Main {
    static List<String> T;
    static int pos;

    interface Node {
        Map<String,Integer> calc();
    }

    static class TokenNode implements Node {
        String tok;
        TokenNode(String t){ tok=t; }
        public Map<String,Integer> calc(){
            return Collections.singletonMap(tok,1);
        }
    }

    static class SequenceNode implements Node {
        List<Node> ch = new ArrayList<>();
        public Map<String,Integer> calc(){
            Map<String,Integer> res = new HashMap<>();
            for (Node n: ch) {
                for (var e: n.calc().entrySet()){
                    res.put(e.getKey(), res.getOrDefault(e.getKey(),0)+e.getValue());
                }
            }
            return res;
        }
    }

    static class BranchNode implements Node {
        boolean req;
        List<Node> opts = new ArrayList<>();
        BranchNode(boolean r){ req=r; }
        public Map<String,Integer> calc(){
            List<Map<String,Integer>> ms = new ArrayList<>();
            for (Node n: opts) ms.add(n.calc());
            if (!req) ms.add(new HashMap<>()); 
            Set<String> keys = new HashSet<>();
            for (var m: ms) keys.addAll(m.keySet());
            Map<String,Integer> res = new HashMap<>();
            for (String k: keys){
                int mn = Integer.MAX_VALUE;
                for (var m: ms) mn = Math.min(mn, m.getOrDefault(k,0));
                if (mn>0) res.put(k,mn);
            }
            return res;
        }
    }

    static Node parseNode(){
        SequenceNode seq = new SequenceNode();
        while (pos < T.size()) {
            String tk = T.get(pos);
            if (tk.equals("{") || tk.equals("[")) {
                seq.ch.add(parseBranch());
            } else if (tk.equals("}")||tk.equals("]")||tk.equals("|")) {
                break;
            } else {
                seq.ch.add(new TokenNode(tk));
                pos++;
            }
        }
        return seq;
    }

    static BranchNode parseBranch(){
        boolean req = T.get(pos).equals("{");
        pos++;
        BranchNode bn = new BranchNode(req);
        while (!(T.get(pos).equals(req? "}" : "]"))) {
            SequenceNode seq = new SequenceNode();
            while (!T.get(pos).equals("|") && !T.get(pos).equals("}") && !T.get(pos).equals("]")) {
                if (T.get(pos).equals("{")||T.get(pos).equals("[")){
                    seq.ch.add(parseBranch());
                } else {
                    seq.ch.add(new TokenNode(T.get(pos)));
                    pos++;
                }
            }
            bn.opts.add(seq);
            if (T.get(pos).equals("|")) pos++;
        }
        pos++;
        return bn;
    }

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        T = Arrays.asList(sc.nextLine().split("\\s+"));
        pos = 0;
        Node root = parseNode();
        Map<String,Integer> mp = root.calc();
        List<String> keys = new ArrayList<>();
        for (var e: mp.entrySet()) if (e.getValue()>0) keys.add(e.getKey());
        Collections.sort(keys);
        for (int i=0;i<keys.size();i++){
            if (i>0) System.out.print(" ");
            System.out.print(keys.get(i));
        }
        System.out.println();
        for (int i=0;i<keys.size();i++){
            if (i>0) System.out.print(" ");
            System.out.print(mp.get(keys.get(i)));
        }
        System.out.println();
    }
}
