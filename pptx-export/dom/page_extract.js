/* Runs INSIDE the rendered Marp HTML (Chromium). Evaluates to a Promise of
 *   { slides: [ { classes, bg, ops: [...] } ], warnings: [...] }
 * All geometry is in slide px (1280 x 720) relative to the <section>.
 * ops:
 *   { t:'box',  x,y,w,h, fill:[r,g,b,a]|null, grad, radius, borders:{t,r,b,l}, name }
 *   { t:'text', x,y,w,h, align, lh, wrap, runs:[{t,br,font,size,weight,italic,color,mono,
 *               underline,strike,sup,sub,href,bg,spc}], name }
 *   { t:'image', x,y,w,h, png(base64) }
 */
(async () => {
  const W = 1280, H = 720;
  const warnings = [];
  const slidesOut = [];

  // ── helpers ────────────────────────────────────────────────────────────────
  const num = (v) => { const n = parseFloat(v); return isNaN(n) ? 0 : n; };
  // cumulative CSS opacity of an element and its ancestors
  function effOpacity(el) {
    let o = 1;
    for (let a = el; a && a.nodeType === 1; a = a.parentElement) {
      const v = parseFloat(getComputedStyle(a).opacity); if (!isNaN(v)) o *= v;
    }
    return o;
  }
  const fadeCol = (c, o) => (c && o < 0.999 ? [c[0], c[1], c[2], c[3] * o] : c);

  function parseColor(c) {
    if (!c) return null;
    let m = c.match(/^rgba?\(([^)]+)\)$/);
    if (m) {
      const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
      return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    }
    m = c.match(/^color\(srgb\s+([^)]+)\)$/);
    if (m) {
      const p = m[1].split(/[\s\/]+/).filter(Boolean).map(Number);
      return [Math.round(p[0] * 255), Math.round(p[1] * 255), Math.round(p[2] * 255),
              p.length > 3 ? p[3] : 1];
    }
    return null;
  }
  const visibleColor = (c) => { const p = parseColor(c); return p && p[3] > 0.01 ? p : null; };

  // linear-gradient(<angle>, c1 [p1], c2 [p2]) → {angle, stops:[{pos,color}]}
  function parseGradient(bgImage) {
    const m = bgImage.match(/^linear-gradient\((.*)\)$/s);
    if (!m) return null;
    const parts = []; let depth = 0, cur = '';
    for (const ch of m[1]) {
      if (ch === '(') depth++;
      if (ch === ')') depth--;
      if (ch === ',' && depth === 0) { parts.push(cur.trim()); cur = ''; } else cur += ch;
    }
    parts.push(cur.trim());
    let angle = 180;
    const first = parts[0];
    if (/^-?[\d.]+deg$/.test(first)) { angle = parseFloat(first); parts.shift(); }
    else if (/^to /.test(first)) {
      const dir = { 'to top': 0, 'to right': 90, 'to bottom': 180, 'to left': 270,
                    'to top right': 45, 'to bottom right': 135, 'to bottom left': 225,
                    'to top left': 315 };
      angle = dir[first] ?? 180; parts.shift();
    }
    const stops = parts.map((s, i) => {
      const cm = s.match(/^(rgba?\([^)]*\)|color\([^)]*\))\s*([\d.]+%)?$/);
      if (!cm) return null;
      return { color: parseColor(cm[1]),
               pos: cm[2] ? parseFloat(cm[2]) / 100 : i / Math.max(1, parts.length - 1) };
    }).filter(Boolean);
    return stops.length >= 2 ? { angle, stops } : null;
  }

  const measureCtx = document.createElement('canvas').getContext('2d');
  function textWidth(text, cs) {
    measureCtx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    return measureCtx.measureText(text).width;
  }

  // distance from the top of a line's text box to its baseline (font ascent, px)
  function ascent(cs) {
    measureCtx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    return measureCtx.measureText('H').fontBoundingBoxAscent;
  }
  const ascentCache = new WeakMap();
  function ascentOf(el) {
    if (!ascentCache.has(el)) ascentCache.set(el, ascent(getComputedStyle(el)));
    return ascentCache.get(el);
  }

  function isMono(cs) { return /mono|consolas|courier/i.test(cs.fontFamily); }

  // ── font actually used by Chrome ──────────────────────────────────────────
  // The PPTX must name the font the PDF was drawn with, not the first family of the CSS
  // stack: when a font is missing, Chrome falls back (Segoe UI, Georgia, Consolas…) and
  // PowerPoint must use the same fallback, not a substitute of its own.
  const GENERIC = new Set(['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui',
    'ui-sans-serif', 'ui-serif', 'ui-monospace', 'ui-rounded', '-apple-system',
    'blinkmacsystemfont', 'emoji', 'math']);
  const DEFAULT_FOR = { serif: 'Times New Roman', monospace: 'Courier New', 'ui-monospace': 'Courier New' };
  const installedCache = new Map();
  function installed(fam) {
    if (!installedCache.has(fam)) {
      const probe = 'mmmmmmmmmmlli1WQ@#';
      const widths = (font) => { measureCtx.font = font; return measureCtx.measureText(probe).width; };
      installedCache.set(fam, ['monospace', 'serif', 'sans-serif'].some(
        (base) => widths(`72px "${fam}", ${base}`) !== widths(`72px ${base}`)));
    }
    return installedCache.get(fam);
  }
  const faceCache = new Map();
  // CSS font-family + weight → { family, bold } for PowerPoint. Static families expose
  // their weights as separate family names (e.g. "Plex Sans Light", "Segoe UI Semibold").
  function fontFace(stack, weight) {
    const key = stack + '|' + weight;
    if (faceCache.has(key)) return faceCache.get(key);
    const fams = stack.split(',').map((f) => f.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
    let family = fams.find((f) => !GENERIC.has(f.toLowerCase()) && installed(f));
    if (!family) {
      const g = fams.find((f) => GENERIC.has(f.toLowerCase())) || 'sans-serif';
      family = DEFAULT_FOR[g.toLowerCase()] || 'Arial';
    }
    let bold = false;
    const variants = weight <= 300 ? ['Light'] : weight === 500 ? ['Medium']
      : weight === 600 ? ['SemiBold', 'Semibold'] : [];
    // A bundled web font (@font-face) has no per-weight family names in Chrome, but the
    // installed static fonts PowerPoint will use do: "<family> Light", "<family> SemiBold"…
    const webFont = [...document.fonts].some(
      (f) => f.status === 'loaded' && f.family.replace(/^["']|["']$/g, '') === family);
    const v = variants.map((s) => `${family} ${s}`).find(installed) ||
      (webFont && variants.length ? `${family} ${variants[0]}` : null);
    if (v) family = v;
    else if (weight >= 600) bold = true;
    const face = { family, bold };
    faceCache.set(key, face);
    return face;
  }
  // every run carries the resolved face
  const withFace = (run) => Object.assign(run, { face: fontFace(run.font, run.weight) });

  function applyTransform(text, cs) {
    switch (cs.textTransform) {
      case 'uppercase': return text.toUpperCase();
      case 'lowercase': return text.toLowerCase();
      case 'capitalize': return text.replace(/\b(\p{L})/gu, (c) => c.toUpperCase());
      default: return text;
    }
  }

  // ── raster of <img>/<svg> honouring CSS filter and object-fit ─────────────
  async function rasterImage(el, w, h) {
    const cs = getComputedStyle(el);
    let img;
    if (el.tagName.toLowerCase() === 'img') {
      img = el;
      try { await img.decode(); } catch (e) { /* broken image */ }
      if (!img.complete || (!img.naturalWidth && !/\.svg(\?|$)/i.test(img.src))) return null;
    } else {
      const xml = new XMLSerializer().serializeToString(el);
      img = new Image();
      img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
      try { await img.decode(); } catch (e) { return null; }
    }
    const S = 2;                                           // 2x for crisp edges
    const cv = document.createElement('canvas');
    cv.width = Math.max(1, Math.round(w * S)); cv.height = Math.max(1, Math.round(h * S));
    const ctx = cv.getContext('2d');
    ctx.globalAlpha = effOpacity(el);
    if (cs.filter && cs.filter !== 'none') ctx.filter = cs.filter;
    const nw = img.naturalWidth || w, nh = img.naturalHeight || h;
    let dw = w, dh = h, dx = 0, dy = 0;
    const fit = cs.objectFit;
    if (fit === 'contain' || fit === 'scale-down') {
      const k = Math.min(w / nw, h / nh);
      dw = nw * k; dh = nh * k;
      const pos = (cs.objectPosition || '50% 50%').split(/\s+/);
      const frac = (p) => p === 'left' || p === 'top' ? 0 : p === 'right' || p === 'bottom' ? 1
                         : p === 'center' ? 0.5 : parseFloat(p) / 100;
      dx = (w - dw) * frac(pos[0]); dy = (h - dh) * frac(pos[1] || '50%');
    }
    try {
      ctx.drawImage(img, dx * S, dy * S, dw * S, dh * S);
      return cv.toDataURL('image/png').split(',')[1];
    } catch (e) { return null; }
  }

  // ── main per-slide extraction ─────────────────────────────────────────────
  // With ![bg] images Marp emits, per slide, a `background` and a `pseudo` layer next to the
  // `content` section: only the content/plain sections are slides, the layers are merged in.
  const ADV = 'data-marpit-advanced-background';
  const sections = Array.from(document.querySelectorAll('svg[data-marpit-svg] > foreignObject > section, .marpit > section'))
    .filter((el) => !['background', 'pseudo'].includes(el.getAttribute(ADV)));
  if (!sections.length) sections.push(...document.querySelectorAll('section:not([' + ADV + '=background]):not([' + ADV + '=pseudo])'));

  for (let si = 0; si < sections.length; si++) {
    const section = sections[si];
    // reference box = the slide's <svg> (a content section may be narrower/shifted with ![bg left])
    const S = (section.closest('svg[data-marpit-svg]') || section).getBoundingClientRect();
    const k = W / S.width;                                 // 1 unless the SVG is scaled
    if (Math.abs(k - 1) > 0.01) warnings.push(`slide ${si + 1}: rendered at scale ${(1 / k).toFixed(2)}, positions may be off`);
    const ops = [];
    const slide = { classes: section.className || '', bg: null, ops };
    const rel = (r) => ({ x: (r.left - S.left) * k, y: (r.top - S.top) * k,
                          w: r.width * k, h: r.height * k });

    // ── box decoration (background, gradient, borders, radius) ──
    function decoration(el, cs, r, isRoot) {
      const o = effOpacity(el);
      const fill = fadeCol(visibleColor(cs.backgroundColor), o);
      const grad = cs.backgroundImage && cs.backgroundImage !== 'none'
        ? parseGradient(cs.backgroundImage) : null;
      if (grad && o < 0.999) grad.stops.forEach((st) => { st.color = fadeCol(st.color, o); });
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !grad &&
          !/^url\(/.test(cs.backgroundImage))
        warnings.push(`slide ${si + 1}: unsupported background-image on <${el.tagName.toLowerCase()}>`);
      const borders = {};
      let any = false;
      for (const [key, side] of [['t', 'Top'], ['r', 'Right'], ['b', 'Bottom'], ['l', 'Left']]) {
        const w = num(cs['border' + side + 'Width']);
        const st = cs['border' + side + 'Style'];
        const col = fadeCol(visibleColor(cs['border' + side + 'Color']), o);
        if (w > 0 && st !== 'none' && st !== 'hidden' && col) {
          borders[key] = { w, color: col, style: st }; any = true;
        }
      }
      let radius = 0;
      const rs = cs.borderTopLeftRadius;
      if (rs) radius = rs.endsWith('%') ? parseFloat(rs) / 100 * Math.min(r.w, r.h) : num(rs);
      if (isRoot) {
        if (!slide.bg || fill || grad) slide.bg = { fill, grad };
        if (any) ops.push({ t: 'box', ...r, fill: null, grad: null, radius: 0, borders,
                            name: 'slide border' });
        return;
      }
      if (fill || grad || any)
        ops.push({ t: 'box', ...r, fill, grad, radius, borders,
                   name: (el.className && typeof el.className === 'string' ? el.className.split(' ')[0] : el.tagName.toLowerCase()) });
    }

    // composite a translucent colour over the nearest opaque ancestor background
    function flatten(col, el, inclusive) {
      if (!col || col[3] >= 0.999) return col;
      const layers = [];
      for (let a = inclusive ? el : el.parentElement; a; a = a.parentElement) {
        const b = visibleColor(getComputedStyle(a).backgroundColor);
        if (b) { layers.unshift(b); if (b[3] >= 0.999) break; }
      }
      let base = [255, 255, 255];                          // farthest layer first
      for (const b of layers) base = base.map((v, i) => Math.round(b[i] * b[3] + v * (1 - b[3])));
      const al = col[3];
      return [0, 1, 2].map((i) => Math.round(col[i] * al + base[i] * (1 - al))).concat([1]);
    }

    // ── runs from a list of inline nodes ──
    function runsOf(nodes, blockCs) {
      const pre = /^pre/.test(blockCs.whiteSpace);
      const out = [];
      // Where Chrome wrapped the lines: a soft break is recorded wherever a character starts
      // lower than the previous one, so PowerPoint breaks the lines at the same places.
      const rg = document.createRange();
      let prevTop = null;
      const lineParts = (n) => {
        const v = n.nodeValue, parts = [];
        rg.selectNodeContents(n);
        const boxes = rg.getClientRects();
        if (!boxes.length) return [v];
        let start = 0;
        for (let i = 0; i < v.length; i++) {
          if (/\s/.test(v[i])) continue;
          let r = boxes[0];
          if (boxes.length > 1) {                           // wrapped inside this node: per character
            rg.setStart(n, i); rg.setEnd(n, i + 1);
            r = rg.getClientRects()[0];
            if (!r) continue;
          }
          // compare baselines, not tops: runs of different sizes share a line
          const base = r.top + ascentOf(n.parentElement);
          if (prevTop !== null && base - prevTop > r.height * 0.5) { parts.push(v.slice(start, i)); start = i; }
          prevTop = base;
          if (boxes.length === 1) break;                    // one line box: only the start matters
        }
        parts.push(v.slice(start));
        return parts;
      };
      const push = (text, el) => {
        const cs = getComputedStyle(el);
        const a = el.closest('a');
        const bg = cs.display === 'inline' ? flatten(visibleColor(cs.backgroundColor), el) : null;
        out.push(withFace({
          t: applyTransform(text, cs), font: cs.fontFamily, size: num(cs.fontSize) * k,
          weight: parseInt(cs.fontWeight, 10) || 400, italic: cs.fontStyle === 'italic',
          color: flatten(parseColor(cs.color), el, true), mono: isMono(cs),
          underline: /underline/.test(cs.textDecorationLine),
          strike: /line-through/.test(cs.textDecorationLine),
          sup: cs.verticalAlign === 'super', sub: cs.verticalAlign === 'sub',
          href: a ? a.getAttribute('href') : null, bg,
          spc: cs.letterSpacing !== 'normal' ? num(cs.letterSpacing) * k : 0,
        }));
      };
      const walk = (n) => {
        if (n.nodeType === Node.TEXT_NODE) {
          let t = n.nodeValue;
          if (!pre) t = t.replace(/[ \t\r\n\f]+/g, ' ');
          if (pre) {
            prevTop = null;
            t.split('\n').forEach((part, i) => {
              if (i > 0) out.push({ br: true });
              if (part) push(part, n.parentElement);
            });
          } else if (t) {
            lineParts(n).forEach((part, i) => {
              if (i > 0) out.push({ br: true, soft: true });
              const tt = part.replace(/[ \t\r\n\f]+/g, ' ');
              if (tt) push(tt, n.parentElement);
            });
          }
        } else if (n.nodeType === Node.ELEMENT_NODE) {
          if (n.tagName === 'BR') { out.push({ br: true }); prevTop = null; return; }
          if (isEmoji(n)) { push(n.alt, n); out[out.length - 1].emoji = true; return; }
          const ecs = getComputedStyle(n);
          if (ecs.display === 'none') return;
          // inline padding (e.g. inline code) -> a highlighted mono space of the same width
          const padOf = (side) => ecs.display === 'inline' ? num(ecs['padding' + side]) : 0;
          // a space of the padding's width: size it from the real advance of a space
          const spaceW = textWidth(' ', ecs) / num(ecs.fontSize) || 0.6;
          const pad = (px) => out.push(withFace({
            t: ' ', fixed: true, font: ecs.fontFamily, size: px / spaceW * k, weight: 400, italic: false,
            color: parseColor(ecs.color), mono: true, underline: false, strike: false, sup: false,
            sub: false, href: null, bg: flatten(visibleColor(ecs.backgroundColor), n), spc: 0 }));
          if (padOf('Left') > 0.5) pad(padOf('Left'));
          n.childNodes.forEach(walk);
          if (padOf('Right') > 0.5) pad(padOf('Right'));
        }
      };
      nodes.forEach(walk);
      // whitespace: collapse across runs, trim at line starts/ends
      let atStart = true;
      for (let i = 0; i < out.length; i++) {
        const r = out[i];
        if (r.br) { atStart = true; continue; }
        if (r.fixed) { atStart = false; continue; }
        if (!pre) {
          if (atStart) r.t = r.t.replace(/^ +/, '');
          else if (/^ /.test(r.t)) {
            let j = i - 1;
            while (j >= 0 && out[j].br === undefined && out[j].t === '') j--;
            // a padding space (fixed) is not text: the real space after it must stay
            if (j >= 0 && out[j].br === undefined && !out[j].fixed && / $/.test(out[j].t))
              r.t = r.t.replace(/^ +/, '');
          }
        }
        if (r.t.length) atStart = false;
      }
      // trim trailing spaces before br / at end
      for (let i = 0; i < out.length; i++) {
        if (out[i].br || out[i].fixed) continue;
        const next = out.slice(i + 1).find((x) => x.br || x.t.length);
        if (!next || next.br) out[i].t = out[i].t.replace(/ +$/, '');
      }
      return out.filter((r) => r.br || r.t.length);
    }
    // ── geometry / text helpers ──
    const BLOCKISH = /^(block|list-item|table-cell|flow-root|table-caption)$/;
    const isSkipped = (el, cs) =>
      /^(STYLE|SCRIPT|NOSCRIPT|TEMPLATE|HEAD|META|LINK)$/.test(el.tagName) ||
      cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0;

    const isEmoji = (n) => n.tagName === 'IMG' && n.classList.contains('emoji') && !!n.alt;

    function isInlineLevel(n) {
      if (n.nodeType === Node.TEXT_NODE) return true;
      if (n.nodeType !== Node.ELEMENT_NODE) return false;
      const tag = n.tagName;
      if (tag === 'BR') return true;
      if (tag === 'IMG') return isEmoji(n);
      if (tag === 'svg' || tag === 'SVG') return false;
      if (getComputedStyle(n).display !== 'inline') return false;
      return Array.from(n.querySelectorAll('*')).every((d) => {
        if (d.tagName === 'BR') return true;
        if (d.tagName === 'IMG') return isEmoji(d) && getComputedStyle(d).display === 'inline';
        if (d.tagName.toLowerCase() === 'svg') return false;
        return getComputedStyle(d).display === 'inline';
      });
    }

    // plain rect + the element whose font drew it (for its baseline)
    const box = (r, el) => ({ top: r.top, bottom: r.bottom, left: r.left, right: r.right,
                              width: r.width, height: r.height, el });
    function textRects(nodes) {
      const rects = [];
      const rg = document.createRange();
      const walk = (n) => {
        if (n.nodeType === Node.TEXT_NODE) {
          if (!n.nodeValue.trim()) return;
          rg.selectNodeContents(n);
          for (const r of rg.getClientRects()) if (r.width > 0.5 && r.height > 0.5) rects.push(box(r, n.parentElement));
        } else if (n.nodeType === Node.ELEMENT_NODE && isEmoji(n)) {
          const r = n.getBoundingClientRect();
          if (r.width > 0.5 && r.height > 0.5) rects.push(box(r, n.parentElement));
        } else if (n.nodeType === Node.ELEMENT_NODE && n.tagName !== 'BR') {
          n.childNodes.forEach(walk);
        }
      };
      nodes.forEach(walk);
      return rects;
    }

    function lineClusters(rects, lhPx) {
      const sorted = rects.slice().sort((a, b) => a.top - b.top);
      const lines = [];
      for (const r of sorted) {
        const last = lines[lines.length - 1];
        if (last && r.top - last.top < Math.max(4, lhPx * 0.5)) {
          if (r.top < last.top) last.el = r.el;
          last.top = Math.min(last.top, r.top); last.bottom = Math.max(last.bottom, r.bottom);
          last.left = Math.min(last.left, r.left); last.right = Math.max(last.right, r.right);
        } else lines.push({ top: r.top, bottom: r.bottom, left: r.left, right: r.right, h: r.height, el: r.el });
      }
      return lines;
    }

    function flushText(parent, nodes, coversAll) {
      if (!nodes.length) return;
      const pcs = getComputedStyle(parent);
      const runs = runsOf(nodes, pcs);
      const eo = effOpacity(parent);
      if (eo < 0.999) runs.forEach((r) => { if (!r.br) { r.color = flatten(fadeCol(r.color, eo), parent, true); r.bg = flatten(fadeCol(r.bg, eo), parent, true); } });
      if (!runs.some((r) => !r.br && r.t.trim())) return;
      const rects = textRects(nodes);
      if (!rects.length) return;
      const fs = num(pcs.fontSize);
      const lhRaw = pcs.lineHeight === 'normal' ? 0 : num(pcs.lineHeight);
      const lines = lineClusters(rects, lhRaw || fs * 1.2);
      const first = lines[0], last = lines[lines.length - 1];
      const half = lhRaw ? (lhRaw - first.h) / 2 : 0;
      const top = first.top - half;
      const bottom = last.bottom + (lhRaw ? (lhRaw - last.h) / 2 : 0);
      const uLeft = Math.min(...lines.map((l) => l.left)), uRight = Math.max(...lines.map((l) => l.right));
      let x = uLeft, w = uRight - uLeft;
      const pr = parent.getBoundingClientRect();
      if (coversAll && BLOCKISH.test(pcs.display)) {
        x = pr.left + num(pcs.borderLeftWidth) + num(pcs.paddingLeft);
        w = pr.width - num(pcs.borderLeftWidth) - num(pcs.borderRightWidth) -
            num(pcs.paddingLeft) - num(pcs.paddingRight);
      }
      let align = pcs.textAlign;
      if (align === 'start' || align === 'justify') align = 'left';
      if (align === 'end') align = 'right';
      ops.push({
        t: 'text', x: (x - S.left) * k, y: (top - S.top) * k, w: w * k, h: (bottom - top) * k,
        base: (first.top + ascentOf(first.el || parent) - top) * k,
        align, lh: lhRaw * k, wrap: lines.length > 1 || runs.some((r) => r.br), runs,
        lines: lines.length,
        name: parent.className && typeof parent.className === 'string'
          ? parent.className.split(' ')[0] : parent.tagName.toLowerCase(),
      });
    }

    // ── list marker ──
    function markerText(li, cs) {
      const type = cs.listStyleType;
      if (!type || type === 'none') return null;
      if (type === 'disc') return '\u2022';
      if (type === 'circle') return '\u25E6';
      if (type === 'square') return '\u25AA';
      // string markers, e.g. list-style-type: "\u2013" (computed value keeps the quotes)
      const str = /^(["'])(.*)\1$/.exec(type);
      if (str) return str[2].replace(/\\([0-9a-fA-F]{1,6})\s?/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
                            .replace(/[\uFE0E\uFE0F]/g, '');
      const parent = li.parentElement;
      let n = parent && parent.tagName === 'OL' ? (parseInt(parent.getAttribute('start'), 10) || 1) : 1;
      for (let s = li.previousElementSibling; s; s = s.previousElementSibling) if (s.tagName === 'LI') n++;
      if (type === 'lower-alpha' || type === 'upper-alpha') {
        const c = String.fromCharCode(96 + ((n - 1) % 26) + 1);
        return (type === 'upper-alpha' ? c.toUpperCase() : c) + '.';
      }
      if (type === 'lower-roman' || type === 'upper-roman') {
        const R = [[1000, 'm'], [900, 'cm'], [500, 'd'], [400, 'cd'], [100, 'c'], [90, 'xc'],
                   [50, 'l'], [40, 'xl'], [10, 'x'], [9, 'ix'], [5, 'v'], [4, 'iv'], [1, 'i']];
        let v = n, r = '';
        for (const [val, sym] of R) while (v >= val) { r += sym; v -= val; }
        return (type === 'upper-roman' ? r.toUpperCase() : r) + '.';
      }
      return n + '.';
    }

    function addMarker(li, cs) {
      const mt = markerText(li, cs);
      if (!mt) return;
      const rects = textRects([li]);
      if (!rects.length) return;
      const lhRaw = cs.lineHeight === 'normal' ? 0 : num(cs.lineHeight);
      const lines = lineClusters(rects.slice(0, 1), lhRaw || num(cs.fontSize) * 1.2);
      const top = lines[0].top - (lhRaw ? (lhRaw - lines[0].h) / 2 : 0);
      const lr = li.getBoundingClientRect();
      // an outside marker ends at the border box (inside: at the content box); keyword
      // markers ("disc", "1.") are followed by a space, string markers ("–") are not
      const inside = cs.listStylePosition === 'inside';
      const edge = inside ? lr.left + num(cs.borderLeftWidth) + num(cs.paddingLeft) : lr.left;
      const isString = /^["']/.test(cs.listStyleType);
      const mcs = getComputedStyle(li, '::marker');
      const w = textWidth(mt + (isString ? '' : ' '), cs);
      ops.push({
        t: 'text', x: (edge - w - S.left) * k, y: (top - S.top) * k, w: w * k,
        h: (lhRaw || num(cs.fontSize) * 1.2) * k, base: (lines[0].top + ascentOf(lines[0].el || li) - top) * k,
        align: 'left', lh: lhRaw * k, wrap: false,
        runs: [withFace({ t: mt, font: cs.fontFamily, size: num(cs.fontSize) * k, weight: parseInt(cs.fontWeight, 10) || 400,
                 italic: false, color: parseColor(mcs.color) || parseColor(cs.color), mono: false,
                 underline: false, strike: false, sup: false, sub: false, href: null, bg: null, spc: 0 })],
        name: 'marker',
      });
    }

    // ── CSS url() backgrounds (Marp ![bg] figures) ──
    async function bgImageOp(cs, r) {
      const m = cs.backgroundImage.match(/url\(["']?(.*?)["']?\)/);
      if (!m) return;
      const img = new Image();
      img.src = m[1];
      try { await img.decode(); } catch (e) { warnings.push(`slide ${si + 1}: background image not loadable`); return; }
      const S2 = 2, cv = document.createElement('canvas');
      cv.width = Math.max(1, Math.round(r.w * S2)); cv.height = Math.max(1, Math.round(r.h * S2));
      const ctx = cv.getContext('2d');
      const nw = img.naturalWidth || r.w, nh = img.naturalHeight || r.h;
      const size = cs.backgroundSize;
      let dw = nw, dh = nh;
      if (size === 'cover') { const f = Math.max(r.w / nw, r.h / nh); dw = nw * f; dh = nh * f; }
      else if (size === 'contain') { const f = Math.min(r.w / nw, r.h / nh); dw = nw * f; dh = nh * f; }
      else if (/%/.test(size) || /px/.test(size)) {
        const p = size.split(/\s+/);
        dw = p[0].endsWith('%') ? r.w * parseFloat(p[0]) / 100 : num(p[0]);
        dh = !p[1] || p[1] === 'auto' ? dw * nh / nw
          : p[1].endsWith('%') ? r.h * parseFloat(p[1]) / 100 : num(p[1]);
      }
      const pos = (cs.backgroundPosition || '50% 50%').split(/\s+/);
      const px = (v, free) => v.endsWith('%') ? free * parseFloat(v) / 100 : num(v);
      const dx = px(pos[0], r.w - dw), dy = px(pos[1] || '50%', r.h - dh);
      ctx.drawImage(img, dx * S2, dy * S2, dw * S2, dh * S2);
      ops.push({ t: 'image', x: r.x, y: r.y, w: r.w, h: r.h, png: cv.toDataURL('image/png').split(',')[1] });
    }

    // ── box of an absolutely positioned pseudo-element (its containing block is the
    //    padding box of a positioned element); null when it cannot be computed ──
    function pseudoBox(el, cs, pcs) {
      if (pcs.position !== 'absolute' || cs.position === 'static') return null;
      const w = num(pcs.width), h = num(pcs.height);
      if (!(w > 0 && h > 0)) return null;
      const er = el.getBoundingClientRect();
      const inL = er.left + num(cs.borderLeftWidth), inR = er.right - num(cs.borderRightWidth);
      const inT = er.top + num(cs.borderTopWidth), inB = er.bottom - num(cs.borderBottomWidth);
      const left = pcs.left !== 'auto' ? inL + num(pcs.left)
        : pcs.right !== 'auto' ? inR - num(pcs.right) - w : null;
      const top = pcs.top !== 'auto' ? inT + num(pcs.top)
        : pcs.bottom !== 'auto' ? inB - num(pcs.bottom) - h : null;
      if (left === null || top === null) return null;
      return rel({ left, top, width: w, height: h });
    }

    // ── content below the bottom padding (Marp clips it silently) ──
    function overflowCheck() {
      const scs = getComputedStyle(section);
      const limit = S.top + (S.height - num(scs.paddingBottom)) / k + 2;
      let lowest = 0;
      const outside = (el) => el.closest('footer, header') ||
        ['absolute', 'fixed'].includes(getComputedStyle(el).position);
      const walker = document.createTreeWalker(section, NodeFilter.SHOW_TEXT);
      const rg = document.createRange();
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (!n.nodeValue.trim() || outside(n.parentElement)) continue;
        rg.selectNodeContents(n);
        for (const rc of rg.getClientRects()) lowest = Math.max(lowest, rc.bottom);
      }
      for (const el of section.querySelectorAll('img, .card, .node, .step, .band, table, pre, blockquote')) {
        if (!outside(el)) lowest = Math.max(lowest, el.getBoundingClientRect().bottom);
      }
      if (lowest > limit)
        warnings.push(`slide ${si + 1}: content runs ${Math.round((lowest - limit + 2) * k)}px past the ` +
                      'bottom margin and is cut off in the PDF (shorten it, use the compact slide ' +
                      'class or split the slide)');
    }

    // ── recursive visit ──
    async function visit(el, isRoot) {
      const cs = getComputedStyle(el);
      if (isSkipped(el, cs)) return;
      const r = rel(el.getBoundingClientRect());
      // Empty pseudo-elements that only draw (a status icon as background image, a
      // fill) are exported when they are absolutely positioned, since their box can then
      // be computed; text in pseudo-elements and other cases are reported.
      const pseudoDrawings = [];
      if (!isRoot && el.tagName !== 'SECTION') {
        for (const pseudo of ['::before', '::after']) {
          const pcs = getComputedStyle(el, pseudo);
          const c = pcs.content;
          const draws = pcs.display !== 'none' &&
            ((pcs.backgroundImage && pcs.backgroundImage !== 'none') || visibleColor(pcs.backgroundColor));
          if (c && c !== 'none' && c !== 'normal' && c !== '""')
            warnings.push(`slide ${si + 1}: ${pseudo} content on <${el.tagName.toLowerCase()}> not exported`);
          else if (c === '""' && draws) {
            const box = pseudoBox(el, cs, pcs);
            if (box) pseudoDrawings.push({ pcs, box });
            else warnings.push(`slide ${si + 1}: ${pseudo} decoration on <${el.tagName.toLowerCase()}> not exported`);
          }
        }
      }
      decoration(el, cs, r, isRoot);
      if (/url\(/.test(cs.backgroundImage) && r.w > 0 && r.h > 0) await bgImageOp(cs, r);
      for (const { pcs, box } of pseudoDrawings) {
        const fill = visibleColor(pcs.backgroundColor);
        if (fill) ops.push({ t: 'box', ...box, fill, grad: null, radius: 0, borders: {}, name: 'pseudo' });
        if (/url\(/.test(pcs.backgroundImage)) await bgImageOp(pcs, box);
      }

      const tag = el.tagName.toLowerCase();
      if (/^(video|audio|iframe|canvas|object|embed)$/.test(tag)) {
        warnings.push(`slide ${si + 1}: <${tag}> is not exported`);
        return;
      }
      if (tag === 'img' || tag === 'svg') {
        if (r.w > 0 && r.h > 0) {
          const png = await rasterImage(el, el.getBoundingClientRect().width, el.getBoundingClientRect().height);
          if (png) ops.push({ t: 'image', x: r.x, y: r.y, w: r.w, h: r.h, png });
          else warnings.push(`slide ${si + 1}: image missing or unreadable (${el.getAttribute('src') || tag})`);
        }
        return;
      }
      if (cs.display === 'list-item') addMarker(el, cs);

      let group = [];
      const children = Array.from(el.childNodes);
      const coversAll = children.every((c) => c.nodeType === Node.COMMENT_NODE ||
        (c.nodeType === Node.TEXT_NODE && !c.nodeValue.trim()) || isInlineLevel(c));
      const flush = () => { if (group.length) flushText(el, group, coversAll); group = []; };
      for (const c of children) {
        if (c.nodeType === Node.COMMENT_NODE) continue;
        if (isInlineLevel(c)) { group.push(c); continue; }
        flush();
        if (c.nodeType === Node.ELEMENT_NODE) await visit(c, false);
      }
      flush();
    }

    const layer = (kind) => section.getAttribute(ADV) === 'content'
      ? section.closest('svg').querySelector(`section[${ADV}="${kind}"]`) : null;
    const bgLayer = layer('background'), pseudo = layer('pseudo');
    if (bgLayer) await visit(bgLayer, true);              // slide colour + ![bg] pictures
    if (pseudo) await visit(pseudo, false);               // header / footer
    await visit(section, true);
    overflowCheck();

    // ── slide number (section::after) ──
    const pcs = getComputedStyle(pseudo || section, '::after');
    const content = pcs.content;
    if (content && content !== 'none' && content !== 'normal' && pcs.display !== 'none') {
      const txt = content.replace(/^["']|["']$/g, '');
      if (txt) {
        const w = textWidth(txt, pcs) + 2;
        const fs = num(pcs.fontSize);
        const lh = pcs.lineHeight === 'normal' ? fs * 1.2 : num(pcs.lineHeight);
        const right = num(pcs.right), bottom = num(pcs.bottom);
        measureCtx.font = `${pcs.fontStyle} ${pcs.fontWeight} ${pcs.fontSize} ${pcs.fontFamily}`;
        const m = measureCtx.measureText('H');
        const base = (lh - m.fontBoundingBoxAscent - m.fontBoundingBoxDescent) / 2 + m.fontBoundingBoxAscent;
        ops.push({
          t: 'text', x: (S.width - right) * k - w * k, y: (S.height - bottom - lh) * k, w: w * k, h: lh * k,
          base: base * k, align: 'right', lh: lh * k, wrap: false, name: 'pagination',
          runs: [withFace({ t: txt, font: pcs.fontFamily, size: fs * k, weight: parseInt(pcs.fontWeight, 10) || 400,
                   italic: false, color: parseColor(pcs.color), mono: false, underline: false, strike: false,
                   sup: false, sub: false, href: null, bg: null, spc: 0 })],
        });
      }
    }
    slidesOut.push(slide);
  }

  return { slides: slidesOut, warnings };
})();
