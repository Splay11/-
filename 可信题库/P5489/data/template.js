const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/[\r\n]+$/, '').trim();
    const scores = raw ? JSON.parse(raw) : [];
    const ans = new Solution().bestShotRecords(scores);
    console.log('[' + ans[0] + ', ' + ans[1] + ']');
});
