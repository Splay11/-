const fs = require("fs");

// 按层搭建三角栈道，求从 start 出发的无向欧拉回路
function solve(h, start) {
    const n = h * (h + 1) / 2;
    const g = Array.from({ length: n + 1 }, () => []);
    const eu = [];
    const ev = [];

    function add(a, b) {
        // 无向边存一次，两端邻接表都记下边号
        const eid = eu.length;
        eu.push(a);
        ev.push(b);
        g[a].push(eid);
        g[b].push(eid);
    }

    for (let r = 2; r <= h; r++) {
        // base / prev 分别是本层、上一层「编号减一」的偏移
        const base = r * (r - 1) / 2;
        const prev = (r - 1) * (r - 2) / 2;
        for (let c = 1; c < r; c++) {
            const u = base + c;
            const v = base + c + 1;
            const w = prev + c;
            add(u, v);
            add(u, w);
            add(v, w);
        }
    }

    const used = new Array(eu.length).fill(false);
    const ptr = new Array(n + 1).fill(0);
    const stack = [start];
    const circ = [];
    // Hierholzer：沿未用边走，走不通时把点弹入回路（得到逆序）
    while (stack.length) {
        const u = stack[stack.length - 1];
        while (ptr[u] < g[u].length && used[g[u][ptr[u]]]) {
            ptr[u]++;
        }
        if (ptr[u] === g[u].length) {
            circ.push(u);
            stack.pop();
        } else {
            const eid = g[u][ptr[u]];
            ptr[u]++;
            used[eid] = true;
            const a = eu[eid];
            const b = ev[eid];
            stack.push(a === u ? b : a);
        }
    }
    circ.reverse();
    return circ;
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
    let p = 0;
    const k = tokens[p++];
    const out = [];
    for (let t = 0; t < k; t++) {
        const h = tokens[p++];
        const s = tokens[p++];
        out.push(solve(h, s).join(" "));
    }
    console.log(out.join("\n"));
}

main();
