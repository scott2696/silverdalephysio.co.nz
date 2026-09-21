# The mobile fold contract

**The requirement:** on a phone, without scrolling, a visitor must see

1. the **H1**,
2. the **byline** — author, fact-checker and the **updated date**,
3. the **toplist H2**, and
4. the **affiliate table** — meaning the whole of the first card, offer panel *and* CTA, not just
   the top edge of it.

This is enforced by measurement, not by eye. The numbers below were taken on **21 September 2026**
and should be re-taken after any change to the hero, the byline or the leaderboard card.

---

## The card layout, and what it costs

There are two shapes the mobile card can take, and they trade against each other. **The stacked,
centred card is the one currently in use, by request.**

### Stacked and centred — current

Rank beside a large logo tile, badge right-aligned below it, brand name and sub-line centred, a
full-width score bar with "Our score" and the value on one line, then the offer panel and CTA. It is
the more generous, more branded shape, and it is what the leaderboard looks like today.

**Card height: 464px.** It was 501px before being tightened; the tightening changed sizes only, not
the shape.

### Two-column header — the compact alternative

Logo beside the name and score instead of stacked above them, text left-aligned. Same elements, same
reading order, less air.

**Card height: 384px — 80px shorter.**

### The trade

The block above the first card — sticky header, H1, byline, toplist H2 — costs about **310px** at
phone widths. What is left of the fold has to hold the card down to its CTA:

| Width | Visible fold | Space for card | Stacked (464px) | Two-column (384px) |
|---|---|---|---|---|
| 360px | ~560 | ~250px | ❌ CTA at 644 | ❌ CTA at 555 — *just* clears |
| 375px | ~579 | ~270px | ❌ CTA at 651 | ✅ CTA at 562 |
| 390px | ~660 | ~350px | ✅ CTA at 631 | ✅ CTA at 542 |
| 414px | ~680 | ~370px | ✅ CTA at 631 | ✅ CTA at 517 |
| 600px | ~760 | ~450px | ✅ CTA at 640 | ✅ CTA at 551 |

**With the stacked card, the H1, byline and H2 clear the fold at every width, and the first CTA
clears it from 390px up.** On 360px and 375px phones the offer panel is partly visible and the
button needs a short scroll. That is not a bug to be tuned away — the card needs 464px and those
phones have ~250–270px below the H2. No amount of size-shaving closes a 200px gap; only the
two-column header does.

### Switching between them

Both live in `assets/css/site.css` in the second `@media(max-width:760px)` block. The difference is
`grid-template-areas` on `.lb-row` plus the handful of per-area rules under it. To go back to the
compact header, replace the stacked area map with:

```css
grid-template-columns:56px minmax(0,1fr) auto;
grid-template-areas:
  "logo  name   score"
  "logo  badge  bar"
  "sub   sub    sub"
  "bonus bonus  bonus"
  "cta   cta    cta"
  "review review review"
  "meta  meta   meta"
  "terms terms  terms";
align-items:center;text-align:left;
```

…and set `.lb-rank` to sit in the `logo` area as a small corner marker rather than a column of its
own. Git history has the full block.

---

## Where the rules live

`assets/css/site.css`, in cascade order — **order matters**, and it was the cause of two bugs found
during this pass:

| Block | Holds |
|---|---|
| `@media(max-width:760px)` (first) | The base card: table becomes a stacked card, `display:contents` flattens `.lb-brand` / `.lb-score` / `.lb-cta` so their children become grid items |
| `@media(max-width:430px)` | **Sizes only.** Anything structural here is overridden by the blocks below it |
| `@media(max-width:760px)` (second) | **The card layout that clears the fold** — the `grid-template-areas` header. Applies across the whole card range so there is no visual jump at a breakpoint |
| `@media(max-width:560px)` | Phone-only type and spacing: header height, H1 size, byline size, H2 size. Hides `.byline-role` |
| `@media(max-width:360px)` | Smallest-phone re-assertions |

### Two cascade bugs this pass fixed

1. **`.lb-logo` was 30px taller than intended.** The ≤430px block set `height:44px`, but the ≤760px
   block's `min-height:74px` is more specific in effect and won. Both are now reset together.
2. **The compact card stopped at 560px**, so 561–760px still got the old stacked card — a visible
   jump at the breakpoint. The layout rules moved to ≤760px; only type sizing stayed at ≤560px.

### What is hidden on phones, and what is not

Only **`.byline-role`** (the author's job title) is hidden, below 560px. The author's name, the
fact-checker's name and the updated date all stay — they are the reason the byline is above the fold
at all. The role remains in the `Person` schema and on `/authors/`.

`.lb-sub` is clamped to two lines rather than hidden.

The masthead **tagline** (`.brand-tag`) used to be hidden below 760px too. It is not any more: the
wordmark is the domain, which says nothing about the subject, so the tagline is the only thing in the
header identifying the site. It shrinks at each breakpoint instead of disappearing, and it costs
nothing at the fold — header height is unchanged at 75–78px, and the first CTA still ends at 542px on
a 390px phone.

---

## The measurement harness

The browser's own window cannot be resized reliably from automation here, and a CSS media query
responds to the *viewport*, so `document.body.style.width` proves nothing. Measure in an iframe
instead: an iframe's width is a viewport for the document inside it.

Serve the site first (`python3 -m http.server 8912` from the repo root), open
`http://localhost:8912/` in a tab, then run this in the console:

```js
window.__probe = async function (w, h) {
  document.querySelectorAll('.probe').forEach(n => n.remove());
  const f = document.createElement('iframe');
  f.className = 'probe';
  f.style.cssText = `position:fixed;top:0;left:0;width:${w}px;height:${h}px;
                     border:0;z-index:2147483647;background:#fff`;
  f.src = 'http://localhost:8912/?v=' + Date.now();   // bust the page cache
  document.body.appendChild(f);
  await new Promise(r => (f.onload = r));
  await new Promise(r => setTimeout(r, 700));         // let fonts settle
  const d = f.contentDocument;
  const g = sel => {
    const e = d.querySelector(sel);
    if (!e) return null;
    const r = e.getBoundingClientRect();
    return [Math.round(r.top), Math.round(r.bottom)];
  };
  const out = {
    w,
    h1:     g('.lede-a h1'),
    byline: g('.lede-y .byline'),
    h2:     g('.lede-c h2.lede-h2'),
    offer:  g('.lede-c .lb-row .lb-bonus'),
    cta:    g('.lede-c .lb-row .btn'),
  };
  f.remove();
  return out;
};

const FOLDS = {320: 460, 360: 560, 375: 579, 390: 660, 414: 680, 600: 760, 700: 800};
for (const w of Object.keys(FOLDS).map(Number)) {
  const r = await window.__probe(w, 900), F = FOLDS[w];
  const s = v => (!v ? 'n/a' : v[1] <= F ? 'OK ' : v[0] < F ? 'CUT' : 'BEL');
  console.log(w, F, 'H1', s(r.h1), 'byline', s(r.byline),
              'H2', s(r.h2), 'offer', s(r.offer), 'CTA', s(r.cta), r.cta && r.cta[1]);
}
```

**Two traps:**

- The iframe carries its own scrollbar, so the effective viewport is roughly 15px narrower than the
  width you set. A 561px iframe gets ≤560px rules. Test a breakpoint from both sides.
- The stylesheet is served with a **content-hash query string** (`site.css?v=…`), and the hash only
  changes on `build.py`. Editing the CSS without rebuilding leaves the old hash in the HTML — the
  server still returns current file contents, but a browser that cached the old response will not
  re-request it. Rebuild, or swap the `<link>` href for a fresh one inside the probe.
