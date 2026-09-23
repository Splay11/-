const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/[\r\n]+$/, '');
    const hits = raw ? JSON.parse(raw) : [];
    console.log(new Solution().minForceWindow(hits));
});
