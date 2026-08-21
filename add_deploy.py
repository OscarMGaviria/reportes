with open('vite.config.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re

deploy_logic = '''
        } else if (req.url === '/api/deploy' && req.method === 'POST') {
          const { exec } = require('child_process');
          const dataDir = path.resolve(__dirname, 'src/data');
          exec('git add src/data/*.json && git commit -m "Auto-update data" && git push', { cwd: __dirname }, (error, stdout, stderr) => {
            if (error) {
              console.error(error);
              res.statusCode = 500;
              res.end(JSON.stringify({ success: false, error: stderr }));
              return;
            }
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ success: true, stdout }));
          });
        } else {
'''

c = c.replace('} else {', deploy_logic)

with open('vite.config.js', 'w', encoding='utf-8') as f:
    f.write(c)
