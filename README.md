# Payout Desk NZ — `best online casino sites NZ`

An independent New Zealand casino affiliate site built around one idea no competitor on the
target SERP does: **every withdrawal ceiling is priced in the weeks it actually costs.**

Static HTML generated from Python. No framework, no build dependencies beyond the standard
library (plus Pillow for the one-off image script). No JavaScript on the published site, no
external requests, no cookie banner.

**43 pages · ~130,500 words · 19 operators · 61/61 Tier 1 keywords · 0 errors.**

---

## ⚠️ Before you deploy

**1. The domain is a physiotherapy domain.** `CNAME` and `DOMAIN` both say
`silverdalephysio.co.nz`. Every canonical, schema `@id`, Open Graph URL, sitemap entry, robots.txt
line and email address follows from `DOMAIN` in `_build/lib.py`, so pointing this at a different
host is a one-line change plus a rebuild.

The masthead shows a **name-only wordmark**, with the brand carried by the tagline underneath it:

```python
DOMAIN = "silverdalephysio.co.nz"   # ← drives URLs, email, canonicals, sitemap, robots
NAME   = "Payout Desk NZ"           # ← brand: titles, schema, body copy
LEGAL  = NAME                       # ← the entity named in Terms and Privacy
TAG    = "Payout Desk · NZ Casino Payouts"      # ← the tagline under the wordmark
LOGO_NAME, LOGO_TLD = "silverdalecasino", ""        # ← NOT derived from DOMAIN; no suffix
```

> ### The wordmark is a brand, not an address
>
> The masthead reads **silverdalecasino** — no suffix. That is deliberate. An earlier draft read
> `silverdalecasino.co.nz`, which put an address in the header that is not the address of this page
> and may be a domain nobody here owns: a reader who typed it in would not arrive, and whoever
> registers it inherits that traffic. Dropping the TLD makes the lockup claim nothing it cannot
> honour, while still keeping "physio" out of a casino masthead.
>
> `LOGO_TLD` is an empty string and the suffix span is only rendered when it is non-empty, so there
> is no orphan full stop anywhere — header, footer or OG card. If `silverdalecasino.co.nz` is ever
> registered and `DOMAIN` pointed at it, set `LOGO_TLD` back and derive both from `DOMAIN` again.

**2. `LEGAL` names no registered company.** It currently resolves to the brand name, which is
honest but thin: Terms, Privacy and the cookie policy make statements about who is liable and who
controls personal data. Replace it with the registered company name before launch. No fictitious
"… Media Limited" is asserted anywhere — deliberately.

**3. The author portraits are in; the bios still need confirming.** `AUTHORS` in `_build/lib.py`
defines five editors with roles, specialisms and scope-of-work statements, and each now carries a
portrait supplied for that byline:

| Byline | Portrait |
|---|---|
| Tama Rewiti, Editor-in-Chief | `images/authors/tama-rewiti.jpg` |
| Hana Whitiora, Payments & Banking Editor | `images/authors/hana-whitiora.jpg` |
| Ari McConnell, Regulation Writer | `images/authors/ari-mcconnell.jpg` |
| Noor Abadi, Head of Terms Analysis | `images/authors/noor-abadi.jpg` |
| Sefa Tuilagi, Games & Betting Writer | `images/authors/sefa-tuilagi.jpg` |

The **names, roles, specialisms and bios were drafted here**, not supplied. They carry no invented
degrees or former employers — deliberately — but they are still descriptions of people, now attached
to photographs of people. Before launch, confirm that each name and each biography actually belongs
to the person in the portrait. Attaching an invented identity to a real face is a documented Google
spam pattern and would undercut the E-E-A-T the rest of the site is built on; it is also simply
unfair to the person pictured.

Originals live in `_source/authors/` (not served). Re-run `python3 _build/gen_authors.py` after
replacing any of them — it squares, face-crops and writes the 148×148 JPEGs. `avatar()` falls back
to initials for any author whose `photo` is `None`.

**4. What the site claims about its own testing.** Every figure with a dollar sign is derived from
the operators' **own published documents** — terms, bonus terms, cashier pages, withdrawal-limit
tables — and computed by the same arithmetic for every brand, with the formula printed beside the
result. The site does **not** claim timed real-money withdrawals, funded test accounts or a
withdrawal dataset, because none were performed. If the desk does run them, that is the strongest
experience signal available in this category: add it to `/how-we-rate/` and to the Experience
section of `docs/SEO-PLAYBOOK.md` at the same time.

**5. Review the ratings before launch.** The 0–10 scores carry over from the shared operator
dataset and have not been re-derived against the new weights (§ *The editorial proposition*). They
are the site's central trust claim, since the running order is openly commercial and the score is
what readers are told to judge by.

**6. Legal risk worth naming.** The Racing Industry Amendment Act 2025 makes it unlawful for anyone
other than TAB NZ to **offer or promote** racing and sports betting to a person in New Zealand.
"Promote" is capable of catching an affiliate. `/online-betting/` and `/best-sports-betting-sites/`
promote offshore sportsbooks. The site states the legal position accurately and prominently on
both, but the exposure is the publisher's. Worth a conversation with a New Zealand lawyer.

---

## The editorial proposition

Every page ranking for this term tells you how fast a casino *processes* a withdrawal — "1–6
hours", "1–3 business days". Those figures are accurate and they answer the wrong question,
because they describe **one payment**, and a win is not one payment.

Almost every operator caps what it will pay in a week. `_build/cashoutcalc.py` takes each
operator's own published ceiling and its own stated processing window and prices the exit:

```
instalments   = win ÷ weekly ceiling
elapsed days  = (instalments − 1) × 7 + the processing window
fx cost       = win × spread, where the balance is not held in NZD
```

Across the 15 casino brands we rank, **14 publish a weekly ceiling**, the median is
**NZ$6,750/week**, and a NZ$10,000 win takes a median of **two weeks** on the card rail — against
advertised windows of one to five days. **Only three sites can hand that win over inside a week.**
Kingdom and Smash clear the bar on headroom (NZ$10,000/week), not on speed. Slotsgem, on
NZ$4,000/week, turns the same win into three payments and three weeks.

Four consequences, each a section on the homepage:

1. **The advertised payout window is the smallest term in the equation** — a four-day spread across
   the set, against a multi-week spread on the ceiling.
2. **A higher ceiling beats a faster rail** whenever the win is large, and no comparison table in
   this market is built to show that.
3. **A euro-denominated balance is a fee with no name on it** — ~4.8% round trip, NZ$480 on a
   NZ$10,000 win, charged whether you win or lose.
4. **A low ceiling is a harm-minimisation problem**, not just an inconvenience: it keeps the
   player's own money inside the casino for another week, with the games one tap away. This is the
   documented "rinse it back" failure mode, and it appears on no competitor page.

The bonus side is still priced — `_build/bonuscalc.py` converts every welcome offer into the
turnover it demands — but it is the supporting argument here, not the headline.

Listing order is commercial and disclosed under every table. The score is not: our best-paying
partner scores 8.1, among the three lowest on the site, with a warning on every page.

---

## What's here

| Tier | Pages |
|---|---|
| **Money pages** | `/` · `/online-casinos/` · `/online-casinos/bonuses/` · `/online-pokies/` · `/high-payout-casinos/` · `/fast-payout-casinos/` · `/live-casinos/` · `/best-crypto-casinos/` · `/no-deposit-casinos/` · `/online-betting/` · `/best-sports-betting-sites/` · `/new-casinos-nz/` |
| **Reviews** | `/casino-reviews/` + 19 operator reviews, each carrying its own Exit Ledger |
| **Guides** | `/nz-online-casino-law/` · `/gambling-winnings-tax-nz/` · `/payment-methods/` · `/how-we-rate/` |
| **Company** | `/about/` · `/contact/` · `/authors/` · `/responsible-gambling/` |
| **Legal** | `/terms/` · `/privacy/` · `/cookie-policy/` |
| **Machine** | `/sitemap.xml` · `/robots.txt` · `/site.webmanifest` |

Strategy documents in [`docs/`](docs/):

- [`SERP-RESEARCH.md`](docs/SERP-RESEARCH.md) — live SERP teardown, competitor headings, the
  994-query NZ demand harvest, Google Trends, voice-of-customer, and the ranked content gaps
- [`COMPETITOR-ANALYSIS.md`](docs/COMPETITOR-ANALYSIS.md) — who ranks across NZ/AU/UK/US/CA, what
  they do well, and the 19 gaps this site fills
- [`KEYWORD-STRATEGY.md`](docs/KEYWORD-STRATEGY.md) — clusters, long-tail, entities, per-page
  mapping, anchor-text plan
- [`SEO-PLAYBOOK.md`](docs/SEO-PLAYBOOK.md) — architecture, page template, E-E-A-T programme,
  schema inventory, SERP plan, the full title/H1 table, scalability
- [`MONEY-PAGE-RESEARCH.md`](docs/MONEY-PAGE-RESEARCH.md) — the homepage's heading structure and
  where each section came from
- [`MOBILE-FOLD.md`](docs/MOBILE-FOLD.md) — what must clear the fold on a phone, the current
  measurements at seven widths, where the rules live, and the harness to re-measure
- [`TITLE-KEYWORD-RESEARCH.md`](docs/TITLE-KEYWORD-RESEARCH.md) — competitor title tags pulled per
  page, the keyword each one reveals, and the title/H1 chosen against it with its pixel width
- [`SERP-RESEARCH-2026-09-21.md`](docs/SERP-RESEARCH-2026-09-21.md) — the live research pass:
  current SERP, competitor headings, voice-of-customer, the DIA market dataset, the ranked gaps, and
  the timeline correction it forced. **Supersedes `SERP-RESEARCH.md` where they disagree**
- `docs/research/` and `.firecrawl/` — the raw captures behind every externally-sourced figure. Kept
  locally and **gitignored**, so they are not published with the site

---

## Design

**Palette: soft ledger green.** `--forest #1C2E26` for structure, `--emerald #3A7D60` for action,
with amber reserved for the welcome-offer panel so the two never compete: green means *do this*,
amber means *this is the bonus*. The action green sits at **55% saturation**, down from 89% — muted
rather than shouted — and that is about as soft as it can go while keeping white button text at
4.9:1. Every text/background pair on the site was re-checked against WCAG AA after the change and
all nineteen pass; the tightest are white-on-CTA at 4.9:1 and the uppercase `--faint` labels at
3.1:1, which is above the 3:1 threshold that applies at their size and weight. The register is a
financial publication rather than a casino.

**The hero** is one continuous forest panel — base gradient on the `.lede` wrapper so it runs
unbroken behind the H1, the lead copy and the byline, with the radial glows on a height-capped,
masked `::before`. Reading order differs by viewport:

```
Desktop:  H1 → top-offer strip → lead + stats → byline → toplist → disclosures
Mobile:   H1 → byline → toplist → lead + stats → disclosures
```

**The lead shows one paragraph**, with the rest folded behind a "Read more" control. On desktop the
whole lead sits between the H1 and the leaderboard, and at full length that is a wall of text in
front of the thing the reader came for — collapsing it saves 256px on the homepage. It is a
`<details>`/`<summary>` pair, so the disclosure, the keyboard behaviour and the open/closed state
come from the browser and **no JavaScript is involved**; the two labels swap on `[open]` in CSS and
both are real text, so the control is announced properly rather than relying on generated content.
A single-paragraph lead gets no control at all (`/new-casinos-nz/` is the one). The summary is
44px tall below 760px, matching the tap-target standard used elsewhere in the stylesheet.

**Above the fold on mobile** — the H1, the byline (author, fact-checker and the updated date) and
the toplist H2 clear the fold at every phone width. The first card's **CTA clears it from 390px up**;
on 360–375px phones the offer panel is partly visible and the button needs a short scroll. That is
the cost of the stacked card shape (see below) and it is a deliberate trade, not a defect — the
numbers and the alternative are in [`docs/MOBILE-FOLD.md`](docs/MOBILE-FOLD.md).

**The affiliate table becomes a card below 760px** — rank beside a large logo tile, badge
right-aligned beneath it, brand name and sub-line centred, a full-width score bar with "Our score"
and the value on one line, then the offer panel and a full-width CTA. `display:contents` flattens
the wrappers so their children become grid items of the card and can be placed by
`grid-template-areas` without duplicate markup.

This stacked shape is **464px tall**. A two-column header — logo beside the name and score — is
**384px**, and clears the fold on every phone from 375px up. Both are documented in
`docs/MOBILE-FOLD.md` with the exact swap; the stacked one is in use by request.

**Navigation** is nested — 9 top-level items, 6 CSS-only dropdowns on `:hover`/`:focus-within`, 43
links covering every page. About and Contact sit in the main horizontal nav *and* the footer. The
hamburger is mobile-only (≤1100px), and its column labels are `<p class="menu-h">` rather than
headings, so the document outline carries content headings only.

---

## Building

```bash
python3 _build/build.py          # regenerates all 43 pages + sitemap + robots (~1s)
python3 _build/check_site.py     # technical guard — must print "all checks passed"
python3 _build/check_keywords.py # coverage + anti-stuffing — must print "coverage complete"
python3 _build/gen_images.py     # one-off: favicons, apple-touch-icon, .ico, .svg, OG card
python3 _build/gen_authors.py    # one-off: author portraits, 148x148 from _source/authors/
```

Output is written in place. This directory **is** the deployed site.

### Where things live

| File | Controls |
|---|---|
| `_build/lib.py` | **Domain, brand, email, month stamp.** Authors, nested nav, footer, page titles and descriptions, schema builders, and every shared component — `lede()`, `leaderboard()`, `top_offer_strip()`, `avatar()`, tables, FAQ, cards, steps |
| `_build/cashoutcalc.py` | **The Exit Ledger.** Parses every withdrawal ceiling and payout window and prices what it costs to get a win out. The signature asset |
| `_build/bonuscalc.py` | The entrance. Parses wagering terms and prices every welcome offer |
| `_build/operators.json` | The 19 operators — links, bonuses, payout windows, ceilings, licensing, and `order` (the supplied commercial order, which drives every leaderboard). **Facts only** — two operators advertise in euros and that is recorded as-is; the NZD conversion happens at the display layer, in `bonuscalc.bonus_in_nzd()` |
| `_build/voice.py` | This masthead's own copy per operator — tagline, pros, cons, verdict, long-form review |
| `_build/lawdata.py` | Licensing timeline, legal facts, helplines, bank-block data |
| `_build/research.py` | 994 harvested NZ queries, Google Trends, market figures |
| `_build/nzdata.py` | The DIA's own market dataset — market size, segments, player behaviour, regional detail, enforcement. Every figure sourced to the 2025 New Zealand Market Insights Reports |
| `_build/p_*.py` | One module per page group |
| `_build/keywords.py` | The 253-term keyword map, per page, as data |
| `assets/css/site.css` | The entire stylesheet, no JS |
| `logos/` | Operator logos — all 19 present and referenced |

### Monthly maintenance

Change `MONTH` in `lib.py` (and `YEAR` each January) and rebuild. Every title, description, H1 and
"updated" line follows. A stale month in a title is worse than no month, so this is a standing
commitment. Re-check the withdrawal ceilings at the same time — they move more often than anything
else on this site, and they are what the whole masthead rests on.

---

## Build guard

`check_site.py` fails the build on: broken internal or asset links · missing or duplicate `<title>`
or meta description · a canonical that is not self-referencing · invalid JSON-LD · `.html` in any
URL · a page without exactly one `<h1>` · a missing responsible-gambling helpline, age statement or
affiliate disclosure · About or Contact absent from the main nav · a sitemap/filesystem mismatch ·
a missing robots.txt rule or favicon size · any title wider than 580px when rendered.

Titles are measured in **pixels**, not characters, because that is how Google truncates them.

`check_keywords.py` enforces Tier 1 coverage per page and fails on stuffing or cannibalisation.

---

## Notes

- **CSS is cache-busted by content hash** (`site.css?v=…`), but the hash is written by `build.py`.
  Edit the stylesheet without rebuilding and a warm browser cache keeps serving the old file — run
  `build.py` after any CSS change.
- **Bonuses are shown in New Zealand dollars**, converted from the operator's advertised figure at
  the dated mid-market rate in `bonuscalc.FX`. Only CrownSlots and Gunsbet need it — they advertise
  in euros. `operators.json` keeps the advertised string untouched, and every converted headline
  carries the original beside it (`€3,700 advertised`) because that is the figure the player meets
  at the cashier. A euro bonus is *not* worth its mid-market NZD equivalent to a New Zealander — the
  ~4.8% round-trip spread comes off it — so silently restating the number would be the exact error
  this site is built to point out. Re-run the rate monthly with the month stamp.
- **No `AggregateRating` on hub pages**, deliberately — Google restricts self-serving aggregate
  ratings. `Review` schema is used on the 19 operator pages, where it belongs.
- **Schema is one `@graph` per page**, assembled in `lib.page()`. Two things are bound there rather
  than in the page modules, so a new page cannot forget them: an `ItemList` is attached to its
  `WebPage` as `mainEntity` (and the page typed `CollectionPage`), and author portraits flow into
  `Person.image` automatically from `AUTHORS`. The Exit Ledger is typed as a `Dataset` on
  `/fast-payout-casinos/`. Full inventory in `docs/SEO-PLAYBOOK.md`.
- **The sitemap's `<lastmod>` is content-hash derived**, not build-time — a page that did not change
  keeps its previous date, so the value is a real signal. `/instant-withdrawals/` is excluded as a
  `noindex` redirect stub.
- **Reddit blocks automated access**, so it is cited from search-result snippets only and no post
  bodies are reproduced. The site says so on `/fast-payout-casinos/#sources`.
- **`evospin.png`** is present in `logos/` but unused — not on the supplied operator list.
- **`/new-casinos-nz/`** is this site's slug for the "new online casinos NZ" cluster. If you would
  rather it sat at `/new-online-casinos/`, change the path in `_build/p_new.py` and
  `_build/keywords.py` and add a redirect — the build handles the rest.
