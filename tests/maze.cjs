const { chromium } = require('playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.route('https://**/*', route => route.abort());
    const base = process.env.BASE_URL || 'http://127.0.0.1:8000';
    for (const [locale, title, label] of [['kk','Ақылды лабиринт','Ойнау'],['ru','Умный лабиринт','Играть'],['en','Smart Maze','Play']]) {
      await page.goto(base);
      await page.selectOption('#language', locale);
      const card = page.locator('.game-card').filter({ hasText: title });
      assert.equal(await card.count(), 1);
      assert.equal(await card.locator('svg.maze-icon').count(), 1);
      const link = card.locator('a.play');
      assert.equal(await link.getAttribute('href'), 'games/labirint/index.html');
      assert.ok((await link.textContent()).includes(label));
      const [response] = await Promise.all([page.waitForNavigation(), link.click()]);
      assert.equal(response.status(), 200);
      assert.equal(await page.locator('html').getAttribute('lang'), locale);
    }
    async function readRoute(size) {
      return page.evaluate(async size => {
        const { solveMaze } = await import('./maze.js');
        const ctx = document.querySelector('canvas').getContext('2d');
        const grid = Array.from({length:size},(_,r)=>Array.from({length:size},(_,c)=>{
          const p=ctx.getImageData(Math.floor((c+.5)*620/size),Math.floor((r+.5)*620/size),1,1).data;
          return p[0]===15 && p[1]===23 && p[2]===42 ? 1 : 0;
        }));
        if (grid.some((row,i)=>row[0]!==1||row[size-1]!==1||(i===0||i===size-1)&&row.some(v=>v!==1))) throw Error('Open boundary');
        const route = solveMaze(grid);
        if(!route.length || route.some(([r,c],i)=>grid[r][c]!==0 || i && Math.abs(r-route[i-1][0])+Math.abs(c-route[i-1][1])!==1)) throw Error('Invalid solution');
        return route;
      }, size);
    }
    for (const size of [15,31,51]) {
      await page.selectOption('#difficulty', String(size));
      assert.ok((await readRoute(size)).length > 1);
      await page.click('#solve');
      assert.match(await page.locator('#status').textContent(), /BFS route revealed/);
      assert.doesNotMatch(await page.locator('#status').textContent(), /YOU WIN/);
      assert.ok((await readRoute(size)).length > 1);
    }
    await page.selectOption('#difficulty', '15');
    const route = await readRoute(15);
    await page.locator('canvas').focus();
    await page.keyboard.press('ArrowUp'); // Entrance is bounded by walls.
    assert.match(await page.locator('#status').textContent(), /0 steps/);
    const [r,c] = route[1];
    const direction = r>1?'down':'right';
    await page.locator(`[data-move="${direction}"]`).evaluate(button=>button.click());
    assert.match(await page.locator('#status').textContent(), /1 steps/);
    await page.evaluate(route => {
      for(let i=2;i<route.length;i++) {
        const [r,c]=route[i], [pr,pc]=route[i-1];
        const key=r>pr?'ArrowDown':r<pr?'ArrowUp':c>pc?'ArrowRight':'ArrowLeft';
        document.querySelector('canvas').dispatchEvent(new KeyboardEvent('keydown',{key,bubbles:true,cancelable:true}));
      }
    }, route);
    assert.match(await page.locator('#status').textContent(), /YOU WIN/);
    await page.click('#reset');
    assert.match(await page.locator('#status').textContent(), /0 steps/);
    await page.setViewportSize({width:390,height:844});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    const mobileRoute = await readRoute(15);
    const canvas=page.locator('canvas');
    await canvas.dispatchEvent('pointerdown',{pointerId:1,clientX:100,clientY:150});
    await canvas.dispatchEvent('pointermove',{pointerId:1,clientX:mobileRoute[1][1]>1?140:100,clientY:mobileRoute[1][0]>1?190:150});
    await canvas.dispatchEvent('pointerup',{pointerId:1});
    assert.match(await page.locator('#status').textContent(), /1 steps/);
    await page.screenshot({path:'/tmp/python-games-maze-mobile.png',fullPage:true});
    assert.deepEqual(errors, []);
    console.log('PASS: 3 localized catalog links, all sizes, enclosed walls, valid BFS, hint is not victory, wall collision, direction button, keyboard route to win, reset, mobile swipe/layout, no JS errors.');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
