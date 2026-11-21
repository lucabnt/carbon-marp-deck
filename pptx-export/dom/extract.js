// Usage: node extract.js <rendered.html> <out.json> [browser-path]
// Loads the Marp HTML in headless Chrome/Edge and runs page_extract.js inside it.
// dom_to_pptx.py passes the browser found by scripts/toolchain.py; CHROME_PATH is the
// fallback when the script is run by hand.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const puppeteer = require('puppeteer-core');

(async () => {
  const [html, out, browserArg] = process.argv.slice(2);
  if (!html || !out) {
    console.error('usage: node extract.js <html> <out.json> [browser-path]');
    process.exit(2);
  }
  const exe = [browserArg, process.env.CHROME_PATH].find((p) => p && fs.existsSync(p));
  if (!exe) {
    console.error('No Chrome/Edge found: pass its path or set CHROME_PATH');
    process.exit(3);
  }

  // The deck only needs its own files (fonts, pictograms, images next to it), so the
  // page gets file access but no network, and Chrome keeps its sandbox. The sandbox is
  // turned off only where Chrome cannot start with it: as root (containers) or when
  // CHROME_NO_SANDBOX=1 is set.
  const noSandbox = process.env.CHROME_NO_SANDBOX === '1' ||
    (typeof process.getuid === 'function' && process.getuid() === 0);
  const browser = await puppeteer.launch({
    executablePath: exe, headless: true,
    args: ['--allow-file-access-from-files', '--force-device-scale-factor=1', '--hide-scrollbars',
           ...(noSandbox ? ['--no-sandbox'] : [])],
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
    // Marp renders emoji as <img> from a CDN; page_extract.js turns them into text. Answer
    // those requests with a blank square image: the layout gets the same 1em x 1em box as
    // the real twemoji (an aborted request would change line and row heights). Every other
    // request that leaves the machine is refused.
    const BLANK = '<svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 72 72"/>';
    const LOCAL = /^(file|data|blob|about):/;
    const blocked = new Set();
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const url = req.url();
      if (/twemoji/.test(url)) return req.respond({ status: 200, contentType: 'image/svg+xml', body: BLANK });
      if (LOCAL.test(url)) return req.continue();
      blocked.add(url.slice(0, 120));
      return req.abort('blockedbyclient');
    });
    await page.goto(pathToFileURL(path.resolve(html)).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const src = fs.readFileSync(path.join(__dirname, 'page_extract.js'), 'utf8');
    const result = await page.evaluate(src);
    for (const url of blocked)
      result.warnings.push(`remote resource not loaded (the export uses local files only): ${url}`);
    fs.writeFileSync(out, JSON.stringify(result));
    console.log(`slides=${result.slides.length} warnings=${result.warnings.length}`);
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
