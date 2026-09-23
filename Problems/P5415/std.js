const START = "Core-SW-01";

function findPath(hops) {
    const g = {};
    for (let i = 0; i < hops.length; i++) {
        const u = hops[i][0];
        const v = hops[i][1];
        if (!g[u]) {
            g[u] = [];
        }
        g[u].push(v);
    }
    for (const u in g) {
        g[u].sort();
        g[u].reverse();
    }
    const route = [];
    const st = [START];
    while (st.length) {
        const u = st[st.length - 1];
        if (g[u] && g[u].length) {
            // 出边已按终点名字从大到小排，弹出末尾就是当前更小的终点
            // 有未用跳转就继续往前走，把终点压栈
            // 没有出边才记下当前点，相当于后序，死胡同会先出现在答案尾部
            // 这样不会像纯贪心那样走进死胡同就再也回不来
            st.push(g[u].pop());
        } else {
            route.push(u);
            st.pop();
        }
    }
    route.reverse();
    return route;
}

function main() {
    const fs = require("fs");
    const raw = fs.readFileSync(0, "utf8");
    const hops = [];
    const parts = raw.trim().split(/\s+/);
    for (let i = 0; i + 1 < parts.length; i += 2) {
        hops.push([parts[i], parts[i + 1]]);
    }
    const ans = findPath(hops);
    console.log(ans.join(" "));
}

main();
