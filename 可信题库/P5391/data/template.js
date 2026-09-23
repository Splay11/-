const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8').replace(/[\r\n]+$/, '');
    const desks = raw ? JSON.parse(raw) : [];
    const ans = new Solution().canPassBooks(desks);
    console.log(ans ? 'true' : 'false');
});
