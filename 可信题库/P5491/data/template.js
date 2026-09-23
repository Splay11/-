const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/[\r\n]+$/, '').trim();
    const seq = raw ? JSON.parse(raw) : '';
    console.log(new Solution().maxSplitProduct(seq));
});
