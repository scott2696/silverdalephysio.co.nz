# Title & H1 Research — competitor keywords, page by page

**Date:** 21 September 2026 · **Market:** New Zealand (`gl=nz`)
**Method:** Live SERP pull for each page's head term, competitor **title tags** extracted verbatim.
The title tag is the highest-signal artefact a competitor produces: it is the keyword they chose to
spend their most valuable 580 pixels on.
**Raw captures:** `.firecrawl/kw-*.json` (gitignored).

**Formula:** `Primary Keyword [Month Year]: Secondary Keyword` · titles budgeted in **pixels**
(≤580px, build-enforced by `check_site.py`) · H1s use the same formula but are **not** pixel-capped,
so they carry the fuller phrase.

Widest title on the site: **571px**. All 24 hub titles and all 19 review titles pass.

---

## The two patterns worth stealing, and the one worth avoiding

**Steal 1 — the month stamp.** `bettingtop10.co.nz` and `betiton.com` both stamp "September 2026" in
the title on their betting pages; `casino.org` and `gamblingsites.co.nz` do it on new-casino pages.
Everyone else stamps only the year. A month reads fresher in a SERP and it is the cheapest CTR edge
available. We stamp it on every page.

**Steal 2 — a number.** `casino.guru` runs "800+ Rated", `casino.org` runs "98%+ RTP" and "up to
$10,000!", `mybettingsites` runs "10+ Bookmakers We Could Withdraw From". Numerals survive truncation
and attract the eye. We use "19 Sites Rated" and the per-review score.

**Avoid — the undifferentiated head term.** Nine of the top ten for the main query title some variant
of *"Best Real Money Online Casinos NZ 2026"*. Matching that exactly buys relevance we already have
from the H1 and body, and buys zero distinctiveness in the result list. Our secondary is where the
difference goes.

---

## Page by page

Each row: the head term, what the ranking competitors actually put in their titles, and what we chose.

### `/` — best online casino sites NZ · **566px**

> **Best Online Casino Sites NZ [September 2026]: Payouts Ranked**
> H1 — …: Real Money Casinos Ranked on Getting Paid

| Competitor titles | Signal |
|---|---|
| "Best Real Money Online Casinos in New Zealand for 2026" (casino.org) | "real money" in 5 of the top 10 |
| "Best Real Money Online Casinos in NZ – 800+ Rated 2026" (casino.guru) | count as CTR device |
| "Best Online Casinos NZ 2026 - Top 9 New Zealand Casinos & Pokies" | "top N" + pokies crossover |
| "Online Casino New Zealand: $1000 Bonus + 200 Spins" (Wildz) | operators lead with the offer |

"Real Money Payouts" measured **603px** — over. Given the head term already contains *Sites*, and
"real money" is carried by the H1 and throughout the body, the secondary spends its space on the
differentiator instead.

### `/online-casinos/` — online casinos NZ · **558px**
> **Online Casinos NZ [September 2026]: Real Money Casino Sites**
> H1 — …: Every Real Money Casino Site in NZ, Compared

Competitors: "Best Online Casino NZ | Top Real Money Casino Sites in 2026" (gambling.com) · "Online
Casino NZ" (Royal Panda) · "Best Real Money Online Casinos in NZ – 800+ Rated". Matches Tier 1
`online casino real money nz` and `nz casino sites` exactly. Kept — the head term here is not the
homepage's, so exact match is the right call.

### `/new-casinos-nz/` — new online casinos NZ · **564px**
> **New Online Casinos NZ [September 2026]: Newest Casino Sites**
> H1 — …: Brand New Casino Sites, Updated as They Launch

Competitors: "New Online Casinos NZ: Best **Brand New** Casinos 2026" (gamerules) · "New Online
Casinos NZ - **Newest Sites** in September 2026" (casino.org) · "New Online Casinos in NZ of
**September 2026** - **Latest** Casino Sites". **Changed** — the old secondary was "Newest Sites
2026", which duplicated the year already in the bracket. "Brand new" moved to the H1.

### `/online-pokies/` — online pokies NZ · **534px**
> **Online Pokies NZ [September 2026]: Real Money Pokie Sites**
> H1 — …: Best Real Money Pokie Sites, With Verified RTP

Competitors: "Online Pokies New Zealand - **Best Pokies Sites** in 2026" (gambling.com) · "Play Online
**Pokies & Slots**" (BetVictor) · "New Zealand Online Pokies" (Spin, Lucky Nugget). **Changed** from
"Real Money Pokies & RTP" — *pokie sites* is the Tier 2 term competitors title on; RTP is our
differentiator and moves to the H1, where nobody else puts it.

### `/high-payout-casinos/` — best payout online casino NZ · **551px**
> **Best Payout Online Casino NZ [September 2026]: Highest RTP**
> H1 — …: Highest RTP Casinos, Audited Lobby by Lobby

Competitors: "Best Payout Casinos NZ 2026 | **98%+ RTP**" (casino.org) · "**Highest Paying** Online
Casino NZ September 2026" (bookies.com) · "Best Payout Online Casino NZ - **Highest RTP** Sites".
**Changed** to the exact Tier 1 string `best payout online casino nz`. casino.org's numeric "98%+ RTP"
is the strongest title in this SERP; we do not copy it because we will not assert a figure we have not
audited across the set.

### `/fast-payout-casinos/` — fast payout casinos NZ · **558px**
> **Fast Payout Casinos NZ [September 2026]: Instant Withdrawals**
> H1 — …: The Fastest Paying Online Casino NZ Offers, and the Whole Withdrawal Clock

| Competitor titles | Signal |
|---|---|
| "**Fast Withdrawal** Casino NZ (Under 1 Hour Payouts)" (betkiwi) | time claim in the title |
| "Fastest Payout Casino NZ 2026 \| **Instant Withdrawals**" (casino.org) | "instant" is universal |
| "Fastest Payout Online Casinos in NZ (2026) **18-Min Tested**" (betiton) | specific measured claim |
| "**250+** New Zealand Fast Withdrawal Casinos" (casino.guru) | count |
| "Instant Withdrawal Casino NZ \| Fastest Payouts New Zealand" (chipy) | both variants in one |

**Changed** from the weak "Payout Times". Every ranking page uses *instant withdrawal* or *fast
withdrawal*; it is Tier 1 (`instant withdrawal casino nz`) and the page contains a section debunking
what "instant" actually means, so we can rank for it honestly. The H1 carries the other Tier 1 string,
`fastest paying online casino nz` — the build caught its absence when the first draft dropped it.

### `/best-crypto-casinos/` — crypto casino NZ · **524px**
> **Crypto Casinos NZ [September 2026]: Bitcoin & USDT Sites**
> H1 — …: Best Bitcoin, USDT and Ethereum Casinos for Kiwis

Competitors split almost evenly between *crypto* and *bitcoin* as the head noun: "Top 10 **Bitcoin**
Casinos in New Zealand 2026" (casino.org) · "Best **Crypto** Casino NZ" (cleverbetlabs) · "Best
**Bitcoin & Crypto** Casinos" (kiwikasino) · "Crypto Casinos NZ 2026 | Best **Bitcoin & USDT** Casino
Guide" (wheretospin). Our title carries both, which is why it was already right.

### `/live-casinos/` — live casino NZ · **482px**
> **Live Casino NZ [September 2026]: Live Dealer Casinos**
> H1 — …: Best Live Dealer Casinos, Counted at New Zealand Hours

Competitors: "Best **Live Dealer** Games Online - Top Live Casinos in NZ 2026" (casino.org) · "Live
Casinos in New Zealand | Play **Live Dealer** Games in NZ" (betpack) · "Live Casino NZ - Best **Live
Dealer** Casinos 2026". **Changed** from "Live Dealer Tables" to the exact Tier 1 `live dealer casino
nz`. The most headroom of any title on the site at 482px.

### `/online-casinos/bonuses/` — casino bonus NZ · **561px**
> **Casino Bonus NZ [September 2026]: Welcome & Sign Up Offers**
> H1 — …: Welcome and Sign Up Bonuses, Converted Into Dollars

Competitors: "Best Casino Bonus 2026 | Top NZ **Sign Up** Offers **up to $10,000!**" (casino.org) ·
"Best Casino Bonuses NZ 2026 | **Welcome & Casino Sign Up Bonus**" (casinos.com) · "NZ Casino Bonuses
| Exclusive Casino Offers" (gambling.com). **Changed** from "Welcome Offers Priced" — *sign up bonus*
is Tier 1 (`casino sign up bonus nz`) and was missing from the title entirely. "Priced" moves to the
H1, where it still does the differentiating.

### `/no-deposit-casinos/` — no deposit bonus NZ · **560px**
> **No Deposit Bonus NZ [September 2026]: Free Spins No Deposit**
> H1 — …: Free Spins No Deposit Offers, Checked This Month

Competitors: "**Free Spins No Deposit** NZ | Best Free Spins Bonuses 2026" (chipy) · "**50** Free Spins
No Deposit Required" (bonus.net.nz) · "**60** Free Spins No Deposit Bonuses" (slotozilla) · "No Deposit
Bonus Casinos NZ (2026)" (gambling.com). Kept — already an exact match on both Tier 1 terms. Note the
numeric-count pattern (50/60 free spins) as a future cluster page opportunity.

### `/online-betting/` — online betting NZ · **536px**
> **Online Betting NZ [September 2026]: Sports & Racing Betting**
> H1 — …: Sports and Racing Betting, TAB NZ and the 2025 Law

**The most useful finding in this pass.** The two pages that outrank everyone are the incumbents, and
both title the same pairing: "**betcha: Racing & Sports Betting** Online in New Zealand" and "**TAB:
Racing & Sports Betting** Online in New Zealand". **Racing** was absent from our title entirely.
**Changed** to carry it. NZ Herald also ranks here with "NZ bans offshore betting, TAB gains monopoly
with new law" — confirming the legal angle is live SERP intent, not just our editorial preference.

### `/best-sports-betting-sites/` — best sports betting sites NZ · **571px**
> **Best Sports Betting Sites NZ [September 2026]: Top Bookmakers**
> H1 — …: Top NZ Bookmakers Compared on Margin, Not Marketing

Competitors: "Best NZ **Sports Betting Sites September 2026** | Top Sites Ranked" (bettingtop10) ·
"Best **Sports Betting Sites** in New Zealand (**September 2026**)" (betiton) · "Online Betting Sites
in New Zealand - **Top 100 Bookmakers**" · "Best Betting Sites NZ: **10+ Bookmakers We Could Withdraw
From**" (mybettingsites). **Changed** the primary from "Best Betting Sites NZ" to the fuller
"Best Sports Betting Sites NZ" — the exact string both month-stamping leaders use. Note mybettingsites
titles on *withdrawal*: our angle is not unique to us in the betting vertical.

### `/casino-reviews/` — online casino reviews NZ · **471px**
> **Casino Reviews NZ [September 2026]: 19 Sites Rated**
> H1 — …: Nineteen Operators Rated, Priced and Scored

Competitors: "Best Casino Reviews NZ 2026 – **Top Rated & Expert Tested**" (casino.org) · "New Zealand
Online Casino Reviews (2026)" (casinomeister) · "Casino Reviews | **Compare** Casinos in New Zealand"
(nzcasino). Position 1 is **Trustpilot**, not an affiliate. Kept the count.

### `/payment-methods/` — casino payment methods NZ · **567px**
> **Casino Payment Methods NZ [September 2026]: NZD In and Out**
> H1 — …: Deposit and Withdrawal Methods That Work From NZ

Competitors: "Top Casino Payment Methods NZ 2026 - **Deposits & Withdrawals**" (casino.org) · "Casino
Payment Methods NZ 2026, Best **Deposits & Withdrawals**" (101rtp) · "Casino Payment **Providers &
Banking Options**" (casinos.com). "Deposits & Withdrawals" is the obvious secondary and measures
**638px** — well over. "Deposits & Payouts" is 602px, also over. "NZD In and Out" fits at 567px,
covers both directions, and carries the NZD entity that Tier 2 wants (`online casinos that accept
nzd`). The full phrase lives in the H1.

### `/nz-online-casino-law/` — are online casinos legal in NZ · **571px**
> **Are Online Casinos Legal In NZ? [September 2026]: The 2026 Act**
> H1 — …: Legal Online Casinos and the 2026 Licensing Regime

**This SERP is government and charity, not commercial:** dia.govt.nz, police.govt.nz,
safergambling.org.nz, PGF, legislation.govt.nz, Wikipedia. No affiliate page ranks in the top eight.
The question-format title matches the query form and is the right play, but **expectations here should
be low** — the page's real job is topical authority and internal-link equity, not traffic.

### `/gambling-winnings-tax-nz/` — gambling winnings tax NZ · **566px**
> **Gambling Winnings Tax NZ [September 2026]: Do You Pay Tax?**
> H1 — …: Do You Pay Tax on Casino and Betting Wins?

IRD ranks first; the only strong commercial result is "New Zealand Gambling Tax: Complete Guide for
Bettors (2026)". Kept — the question format is correct for the intent.

### `/how-we-rate/` — how to choose an online casino NZ · **568px**
> **How We Rate Online Casinos NZ [September 2026]: Our Method**
> H1 — …: How to Choose an Online Casino, and How We Score One

The searchable term is `how to choose an online casino nz`, but every title built on it measured
**604–613px**. The H1 carries it instead (uncapped), and the title keeps the methodology framing the
page actually serves. The competing SERP is thin — scraped-content domains and a couple of
`.co.nz` filler sites — so this is winnable on quality alone.

### `/casino-reviews/<brand>/` — 19 pages · **461–544px**
> **{Brand} Review NZ [September 2026]: Scored X/10**
> H1 — …: The Exit Priced, Scored X/10

**No competitor review title in any SERP we sampled carries a score.** A numeral in a result listing
is a strong CTR signal and it is unclaimed on every brand query we checked. Unchanged.

---

## Company and legal pages

Not competitor-driven; titles kept short and descriptive, month-stamped for consistency with the rest
of the site. `/about/` 435px · `/contact/` 493px · `/authors/` 547px · `/responsible-gambling/` 564px ·
`/terms/` 508px · `/privacy/` 469px · `/cookie-policy/` 470px.

---

## Maintenance

Change `MONTH` (and `YEAR` each January) in `_build/lib.py` and rebuild — every title, H1, description
and "updated" line follows. The pixel budget is measured against **September**, the longest month
name, so a title that fits today fits in every month of the year.
