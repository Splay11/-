const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/[\r\n]+$/, '').trim();
    const weights = raw ? JSON.parse(raw) : [];
    console.log(new Solution().minCircleMerge(weights));
});
