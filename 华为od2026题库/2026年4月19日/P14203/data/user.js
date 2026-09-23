var networkPlanning = function(roomArrangement) {
    const n = roomArrangement.length, m = roomArrangement[0].length;
    const covered = Array.from({length: n}, () => new Array(m).fill(false));
    let count = 0;

    while (true) {
        // 找第一个未覆盖的空地
        let ri = -1, rj = -1;
        for (let i = 0; i < n && ri === -1; i++) {
            for (let j = 0; j < m && rj === -1; j++) {
                if (roomArrangement[i][j] === '.' && !covered[i][j]) {
                    ri = i; rj = j;
                }
            }
        }
        if (ri === -1) return count; // 全部覆盖

        // 枚举能覆盖 (ri,rj) 的所有 AP 位置（9 种可能的左上角）
        let bestCnt = -1;
        let bestR = -1, bestC = -1;
        for (let dr = 0; dr < 3; dr++) {
            for (let dc = 0; dc < 3; dc++) {
                const tr = ri - dr, tc = rj - dc; // AP 左上角
                if (tr < 0 || tc < 0 || tr + 2 >= n || tc + 2 >= m) continue;
                // AP 中心必须是空地
                const cr = tr + 1, cc = tc + 1;
                if (roomArrangement[cr][cc] === '#') continue;
                // 检查 3x3 是否与已覆盖区域重叠
                let ok = true;
                for (let i = tr; i <= tr + 2 && ok; i++) {
                    for (let j = tc; j <= tc + 2 && ok; j++) {
                        if (covered[i][j]) { ok = false; }
                    }
                }
                if (!ok) continue;
                // 计算能新覆盖多少空地
                let cnt = 0;
                for (let i = tr; i <= tr + 2; i++) {
                    for (let j = tc; j <= tc + 2; j++) {
                        if (roomArrangement[i][j] === '.' && !covered[i][j]) cnt++;
                    }
                }
                if (cnt > bestCnt) {
                    bestCnt = cnt;
                    bestR = tr;
                    bestC = tc;
                }
            }
        }
        if (bestR === -1) return -1;
        // 放置 AP
        count++;
        for (let i = bestR; i <= bestR + 2; i++) {
            for (let j = bestC; j <= bestC + 2; j++) {
                covered[i][j] = true;
            }
        }
    }
};
