// Export deck.pdf (every slide fully built) and, with --qa, screenshot
// every slide at every build step at 1920x1080 and 1280x720.
//   node export.js [--qa <outdir>]
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const file = 'file://' + path.join(__dirname, 'index.html');
const qaIdx = process.argv.indexOf('--qa');
const qaDir = qaIdx > 0 ? process.argv[qaIdx + 1] : null;

(async () => {
  const browser = await chromium.launch();

  const pdfPage = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await pdfPage.goto(file + '?print');
  await pdfPage.evaluate(() => document.fonts.ready);
  await pdfPage.waitForTimeout(400);
  await pdfPage.pdf({ path: path.join(__dirname, 'deck.pdf'), width: '1920px', height: '1080px', printBackground: true });
  console.log('deck.pdf written');

  if (qaDir) {
    fs.mkdirSync(qaDir, { recursive: true });
    for (const [w, h] of [[1920, 1080], [1280, 720]]) {
      const page = await browser.newPage({ viewport: { width: w, height: h } });
      await page.goto(file + '?still');
      await page.evaluate(() => document.fonts.ready);
      const counts = await page.evaluate(() => window.__deck.slides.map(s => +s.dataset.steps || 0));
      for (let i = 0; i < counts.length; i++) {
        for (let k = 0; k <= counts[i]; k++) {
          await page.evaluate(([i, k]) => window.__deck.show(i, k, false), [i, k]);
          await page.waitForTimeout(120);
          const name = `${w}-s${String(i + 1).padStart(2, '0')}-${k}.png`;
          await page.screenshot({ path: path.join(qaDir, name) });
        }
      }
      // overflow check: any text box wider than its slide or clipped
      const issues = await page.evaluate(() => {
        const out = [];
        window.__deck.slides.forEach((s, i) => {
          window.__deck.show(i, +s.dataset.steps || 0, false);
          s.querySelectorAll('h1,h2,h3,p,li,span,blockquote,cite').forEach(e => {
            if (e.closest('.notes')) return;
            if (e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== 'visible') out.push(`slide ${i + 1}: ${e.textContent.slice(0, 40)}`);
            const r = e.getBoundingClientRect(), sr = s.getBoundingClientRect();
            if (r.width && (r.right > sr.right + 1 || r.left < sr.left - 1 || r.bottom > sr.bottom + 1)) out.push(`slide ${i + 1} off-canvas: ${e.textContent.slice(0, 40)}`);
          });
        });
        return out;
      });
      console.log(`${w}x${h}:`, issues.length ? issues : 'no overflow');
      await page.close();
    }
  }
  await browser.close();
})();
