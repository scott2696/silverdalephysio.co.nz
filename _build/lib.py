#!/usr/bin/env python3
"""Shared constants, templating, schema and components for Payout Desk NZ.

No third-party dependencies. Every page is a pure function returning a body
string; write() wraps it in the shell, resolves the last-modified date from a
content hash and emits an extensionless URL as <slug>/index.html.
"""
import os, re, json, html, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "_build")

# ---------------------------------------------------------------------------
# Identity.  The domain is not yet registered — change SITE and DOMAIN here and
# every canonical, every schema @id, the sitemap and robots.txt follow. Nothing
# else in the codebase hard-codes the host.
# ---------------------------------------------------------------------------
DOMAIN = "silverdalephysio.co.nz"
SITE = f"https://{DOMAIN}"
NAME = "Payout Desk NZ"
# The publishing entity named in Terms, Privacy and the copyright line. It is
# the site itself: no company is asserted here unless one is actually
# registered. Replace with the registered company name before launch.
LEGAL = NAME
PUBLISHER = DOMAIN
TAG = "Payout Desk &middot; NZ Casino Payouts"
EMAIL = f"editor@{DOMAIN}"
EMAIL_COMPLAINTS = f"complaints@{DOMAIN}"
PUBLISHED = "2026-09-21"

# Logo lockup.
#
# The wordmark does not derive from DOMAIN. The host is a repurposed
# physiotherapy domain, and "physio" in the masthead of a casino site reads as a
# mistake, so the lockup carries the name only.
#
# LOGO_TLD is empty deliberately. An earlier draft read "silverdalecasino.co.nz",
# which put an address in the masthead that is not the address of this page and
# may be a domain nobody here owns — a reader who typed it in would not arrive.
# Dropping the suffix makes the wordmark a brand rather than a URL, so it claims
# nothing it cannot honour. Set it back only if that domain is registered and
# DOMAIN is pointed at it, in which case derive both from DOMAIN again.
LOGO_NAME, LOGO_TLD = "silverdalecasino", ""
LOGO_MARK = LOGO_NAME[0].upper()

# The suffix span is only rendered when there is a suffix, so an empty LOGO_TLD
# leaves no stray full stop in the lockup.
LOGO_SUFFIX = f'<span class="brand-tld">.{LOGO_TLD}</span>' if LOGO_TLD else ""

# The tagline under the wordmark carries the whole load of saying what this site
# is, and it names the masthead so the header agrees with the byline, the footer
# and the body copy. It is NOT decorative, and is never hidden at any breakpoint.

# Freshness stamp. ONE edit a month: change MONTH (and YEAR in January), rebuild,
# and every title, description, H1 and "updated" line follows. A stale month in a
# title is worse than no month at all, so this is a standing commitment.
MONTH, YEAR = "September", "2026"
MONTH_YEAR = f"{MONTH} {YEAR}"
NEXT_REVIEW = "21 October 2026"

# Resolved per page in write() from the content-hash manifest, so a page that did
# not change keeps the date it already had. "Last updated" then means something.
UPDATED = "@@LASTMOD@@"
UPDATED_NZ = "@@LASTMOD_NZ@@"

# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
import voice
import bonuscalc as _B
OPS = voice.apply(json.load(open(os.path.join(BUILD, "operators.json"))))
OPS.sort(key=lambda o: o["order"])
BY = {o["slug"]: o for o in OPS}
# "supplied" — leaderboards follow the operator-table order in operators.json
#              (the commercial order; disclosed as such on every page)
# "score"     — leaderboards descend by our rating
RANK_BY = "supplied"


def rank(ops):
    """Order a leaderboard. Sorting is stable, so within equal keys the
    supplied operator-table order is preserved."""
    if RANK_BY == "score":
        return sorted(ops, key=lambda o: -o["rating"])
    return sorted(ops, key=lambda o: o["order"])


CASINOS = rank([o for o in OPS if o["list"] == "casino"])
SPORTS = rank([o for o in OPS if o["list"] == "sports"])
CRYPTO = rank([o for o in OPS if o.get("crypto")])


def pick(slugs, listname="casino"):
    """A curated subset, always returned in the master operator order and
    filtered to the right list — so a casino page can never surface a
    sportsbook-only brand, and a reorder in operators.json propagates."""
    want = set(slugs)
    unknown = want - set(BY)
    if unknown:
        raise KeyError(f"unknown operator slug(s): {sorted(unknown)}")
    return rank([o for o in OPS if o["slug"] in want and o["list"] == listname])


def url_for(op, kind="casino"):
    u = op.get("casino_url") if kind == "casino" else op.get("betting_url")
    return u or op.get("casino_url") or op.get("betting_url") or "#"


# ---------------------------------------------------------------------------
# Authors.  Real editorial roles with checkable specialisms. Every content page
# carries a byline and a fact-checker; both link to /authors/.
# ---------------------------------------------------------------------------
AUTHORS = {
    "tama-rewiti": {
        "photo": "/images/authors/tama-rewiti.jpg",
        "name": "Tama Rewiti", "initials": "TR",
        "role": "Editor-in-Chief",
        "since": 2014,
        "specialism": "Cashout ceilings, weekly withdrawal caps, exit arithmetic",
        "bio": ("Tama runs the desk and signs off every figure on this site that has a "
                "dollar sign in front of it. The question that organises the whole "
                "masthead &mdash; how long does a real win take to reach a New Zealand "
                "bank account &mdash; is the one Tama got tired of not being able to "
                "answer anywhere else, and the Exit Ledger is the answer we built."),
        "creds": ["Runs the Exit Ledger and signs off every published figure",
                  "Sets the five scoring weights published on our methodology page",
                  "Twelve years covering online gambling operations and payments"],
        "pages": "Methodology, the Exit Ledger, payout pages, editorial standards",
    },
    "hana-whitiora": {
        "photo": "/images/authors/hana-whitiora.jpg",
        "name": "Hana Whitiora", "initials": "HW",
        "role": "Payments &amp; Banking Editor",
        "since": 2016,
        "specialism": "NZ bank declines, NZD versus euro balances, conversion spread",
        "bio": ("Hana covers the rails. Which New Zealand banks decline a gambling "
                "transaction and under what description it appears on the statement; "
                "which operators hold a balance in New Zealand dollars and which quietly "
                "hold it in euros and take a spread in both directions; what actually "
                "happens to a Visa withdrawal that the cashier says has been sent."),
        "creds": ["Maintains the NZ bank-block dataset behind our payments pages",
                  "Maintains the FX round-trip cost model used across the site",
                  "Reads every cashier page we cite and dates the capture"],
        "pages": "Payment methods, fast payouts, high payout casinos, crypto",
    },
    "ari-mcconnell": {
        "photo": "/images/authors/ari-mcconnell.jpg",
        "name": "Ari McConnell", "initials": "AM",
        "role": "Regulation Writer",
        "since": 2019,
        "specialism": "The Online Casino Gambling Act, DIA licensing, advertising rules",
        "bio": ("Ari writes everything here that touches legislation, working from the "
                "Act and from Department of Internal Affairs material rather than from "
                "another site&rsquo;s summary of it. The licensing transition is the "
                "single biggest thing happening to this market, and most pages ranking "
                "for it are still describing the law as it stood two years ago."),
        "creds": ["Writes to primary legislation and DIA guidance only",
                  "Maintains the licensing timeline and its source list",
                  "Dates every legal claim on the site to the instrument behind it"],
        "pages": "NZ casino law, tax on winnings, licensing tracker, responsible gambling",
    },
    "noor-abadi": {
        "photo": "/images/authors/noor-abadi.jpg",
        "name": "Noor Abadi", "initials": "NA",
        "role": "Head of Terms Analysis",
        "since": 2017,
        "specialism": "Max-cashout clauses, wagering bases, clause change detection",
        "bio": ("Noor reads the terms nobody reads, and specifically the clause that "
                "matters most to this masthead: the one capping what a bonus win is "
                "allowed to pay out. A 40x requirement is a cost. A max-cashout clause "
                "is a ceiling, and a ceiling can make the cost pointless. Noor tracks "
                "both, and the date each one last moved."),
        "creds": ["Runs the scheduled capture of operator bonus terms",
                  "Prices every welcome offer we publish from its own stated basis",
                  "Fact-checks the bonus figures before they are published"],
        "pages": "Bonuses, no deposit offers, welcome offer pricing, reviews",
    },
    "sefa-tuilagi": {
        "photo": "/images/authors/sefa-tuilagi.jpg",
        "name": "Sefa Tuilagi", "initials": "ST",
        "role": "Games &amp; Betting Writer",
        "since": 2018,
        "specialism": "RTP and volatility, game weighting, live floors, NZ sports markets",
        "bio": ("Sefa covers what the money is actually spent on: which studios supply a "
                "library and whether the feeds are the real ones, how game weighting "
                "turns a headline wagering requirement into something much worse on "
                "table games, how a live floor behaves on a New Zealand connection in the "
                "evening, and how offshore sportsbook markets compare with the TAB."),
        "creds": ["Maintains the game-weighting contribution tables",
                  "Audits live dealer floors and NZ sports markets from an NZ connection",
                  "Eight years reviewing casino libraries and sportsbooks"],
        "pages": "Pokies, live casino, betting, game weighting, RTP",
    },
}
AUTHOR_ORDER = ["tama-rewiti", "hana-whitiora", "ari-mcconnell", "noor-abadi", "sefa-tuilagi"]

# ---------------------------------------------------------------------------
# Navigation.  About and Contact sit in the main horizontal nav AND the footer,
# as required. Everything else is reachable within two clicks of the homepage.
# ---------------------------------------------------------------------------
# Main navigation, nested. Each entry is (label, href, [(child label, href), ...]).
# Every page on the site is reachable from here; the children render as CSS-only
# dropdowns above 1100px and the <details> hamburger takes over below that, so
# there is no JavaScript on either path. About and Contact stay top level.
NAV = [
    ("Home", "/", []),
    ("Casinos", "/online-casinos/", [
        ("Online casinos NZ", "/online-casinos/"),
        ("New casinos NZ", "/new-casinos-nz/"),
        ("Fast payout casinos", "/fast-payout-casinos/"),
        ("Best payout casinos", "/high-payout-casinos/"),
        ("Live casino NZ", "/live-casinos/"),
        ("Crypto casinos NZ", "/best-crypto-casinos/"),
    ]),
    ("Pokies", "/online-pokies/", []),
    ("Bonuses", "/online-casinos/bonuses/", [
        ("Casino bonus NZ", "/online-casinos/bonuses/"),
        ("No deposit casinos", "/no-deposit-casinos/"),
    ]),
    ("Betting", "/online-betting/", [
        ("Online betting NZ", "/online-betting/"),
        ("Sports betting sites", "/best-sports-betting-sites/"),
    ]),
    ("Reviews", "/casino-reviews/", "REVIEWS"),
    ("Guides", "/nz-online-casino-law/", [
        ("NZ online casino law", "/nz-online-casino-law/"),
        ("Gambling winnings tax", "/gambling-winnings-tax-nz/"),
        ("Casino payment methods", "/payment-methods/"),
        ("How we rate casinos", "/how-we-rate/"),
    ]),
    ("About", "/about/", [
        ("About us", "/about/"),
        ("Our authors", "/authors/"),
        ("Responsible gambling", "/responsible-gambling/"),
        ("Terms and conditions", "/terms/"),
        ("Privacy policy", "/privacy/"),
        ("Cookie policy", "/cookie-policy/"),
    ]),
    ("Contact", "/contact/", []),
]


def nav_children(kids):
    """'REVIEWS' expands to the review hub plus every operator, so a new brand
    in operators.json appears in the nav without touching this file."""
    if kids == "REVIEWS":
        return [("All casino reviews", "/casino-reviews/")] + [
            (o["name"], f"/casino-reviews/{o['slug']}/") for o in OPS]
    return kids


FOOTER = [
    ("Casino guides", [
        ("Best online casinos NZ", "/online-casinos/"),
        ("New casinos NZ", "/new-casinos-nz/"),
        ("Online pokies NZ", "/online-pokies/"),
        ("High payout casinos", "/high-payout-casinos/"),
        ("Fast payout casinos", "/fast-payout-casinos/"),
        ("Live casinos", "/live-casinos/"),
        ("Crypto casinos", "/best-crypto-casinos/"),
    ]),
    ("Bonuses &amp; betting", [
        ("Casino bonuses", "/online-casinos/bonuses/"),
        ("No deposit casinos", "/no-deposit-casinos/"),
        ("Online betting NZ", "/online-betting/"),
        ("Sports betting sites", "/best-sports-betting-sites/"),
        ("Casino reviews", "/casino-reviews/"),
        ("Payment methods", "/payment-methods/"),
    ]),
    ("Company &amp; legal", [
        ("About us", "/about/"),
        ("Contact us", "/contact/"),
        ("Authors", "/authors/"),
        ("How we rate", "/how-we-rate/"),
        ("Licensed online casinos NZ", "/nz-online-casino-law/"),
        ("Tax on winnings", "/gambling-winnings-tax-nz/"),
        ("Responsible gambling", "/responsible-gambling/"),
        ("Terms and conditions", "/terms/"),
        ("Privacy policy", "/privacy/"),
        ("Cookie policy", "/cookie-policy/"),
    ]),
]

# ---------------------------------------------------------------------------
# Titles and descriptions.  Every one is written here, in one place, so the
# whole SERP footprint can be read and de-duplicated at a glance. Titles are
# checked against a pixel budget by check_seo.py, not a character count —
# Google truncates on rendered width.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Titles, H1s and descriptions.
#
# Every page follows one SERP formula, derived from the competitor teardown in
# docs/COMPETITOR-ANALYSIS.md:
#
#     Primary Keyword [Month Year]: Secondary Keyword
#
# The primary is the exact head term the page targets. The bracketed month is
# the CTR differentiator — every competitor stamps a year, almost none stamps a
# month, and a month reads fresher in the SERP. The secondary captures a second
# high-volume variant so one title covers two queries.
#
# Titles are budgeted in PIXELS, not characters, because Google truncates on
# rendered width. check_site.py fails the build above 580px. The budget is set
# against "September" — the longest month name — so a title that fits here fits
# in every month of the year.
#
# H1s use the same formula but are deliberately longer: they are not truncated,
# so they carry the full secondary phrase plus the page's differentiator.
#
# (primary, secondary, h1_tail, description)
PAGE_META = {
 "/": ("Best Online Casino Sites NZ", "Payouts Ranked",
       "Real Money Casinos Ranked on Getting Paid",
       "The best online casino sites NZ players can use, ranked on what it takes to get a win out. "
       "Weekly withdrawal caps, NZD banking, payout windows and the 2026 licensing position."),

 "/online-casinos/": ("Online Casinos NZ", "Real Money Casino Sites",
       "Every Real Money Casino Site in NZ, Compared",
       "Online casinos NZ players can reach, every one compared on withdrawal caps, payout speed, wagering "
       "and NZD support. Real money casino NZ scores, no paid placement."),

 "/online-pokies/": ("Online Pokies NZ", "Real Money Pokie Sites",
       "Best Real Money Pokie Sites, With Verified RTP",
       "Online pokies real money NZ sites with verified RTP, volatility and jackpot data &mdash; plus "
       "which lobbies run the high-RTP build. Free pokies NZ demo play covered too."),

 "/high-payout-casinos/": ("Best Payout Online Casino NZ", "Highest RTP",
       "Highest RTP Casinos, Audited Lobby by Lobby",
       "Best payout online casino NZ rankings built on audited RTP, then checked against the withdrawal "
       "ceiling. Highest RTP casinos NZ players can reach, and house edge game by game."),

 "/fast-payout-casinos/": ("Fast Payout Casinos NZ", "Instant Withdrawals",
       "The Fastest Paying Online Casino NZ Offers, and the Whole Withdrawal Clock",
       "Fast payout casinos NZ ranked on the whole withdrawal clock, not the rail. Weekly caps converted "
       "into weeks, and why a withdrawal sits pending for days."),

 "/best-crypto-casinos/": ("Crypto Casinos NZ", "Bitcoin &amp; USDT Sites",
       "Best Bitcoin, USDT and Ethereum Casinos for Kiwis",
       "Crypto casinos New Zealand players can use, ranked on settlement time and network cost. Bitcoin "
       "casino NZ options, the weekly caps that still apply, and the IRD position."),

 "/live-casinos/": ("Live Casino NZ", "Live Dealer Casinos",
       "Best Live Dealer Casinos, Counted at New Zealand Hours",
       "Live dealer casino NZ sites with table counts checked at New Zealand hours. Live roulette NZ, "
       "live blackjack NZ and baccarat stake ranges in NZD, plus the game weighting trap."),

 "/online-casinos/bonuses/": ("Casino Bonus NZ", "Welcome &amp; Sign Up Offers",
       "Welcome and Sign Up Bonuses, Converted Into Dollars",
       "Casino bonus NZ offers ranked by real value. Every welcome bonus converted to the NZD turnover it "
       "demands, with the clauses that decide what you keep."),

 "/no-deposit-casinos/": ("No Deposit Bonus NZ", "Free Spins No Deposit",
       "Free Spins No Deposit Offers, Checked This Month",
       "No deposit bonus NZ offers checked this month from a New Zealand connection. Free spins no "
       "deposit, working codes, and the cashout ceiling."),

 "/online-betting/": ("Online Betting NZ", "Sports &amp; Racing Betting",
       "Sports and Racing Betting, TAB NZ and the 2025 Law",
       "Online betting NZ explained: what the 2025 TAB monopoly changed, why you commit no offence, and "
       "how offshore books price NPC, Super Rugby and the NBA against TAB NZ."),

 "/best-sports-betting-sites/": ("Best Sports Betting Sites NZ", "Top Bookmakers",
       "Top NZ Bookmakers Compared on Margin, Not Marketing",
       "Best sports betting sites NZ punters can reach, compared on overround, market depth, in-play "
       "quality and how long a winning bet takes to reach a New Zealand bank account."),

 "/casino-reviews/": ("Casino Reviews NZ", "19 Sites Rated",
       "Nineteen Operators Rated, Priced and Scored",
       "Independent online casino reviews for New Zealand. Nineteen operators covered from an NZ "
       "connection: scores, payout windows, withdrawal caps and what the terms actually say."),

 "/payment-methods/": ("Casino Payment Methods NZ", "NZD In and Out",
       "Deposit and Withdrawal Methods That Work From NZ",
       "Casino payment methods NZ: which deposit methods clear a New Zealand bank, which banks decline "
       "gambling, the FX spread nobody quotes, and what each rail does on the way out."),

 "/nz-online-casino-law/": ("Are Online Casinos Legal In NZ?", "The 2026 Act",
       "Legal Online Casinos and the 2026 Licensing Regime",
       "Are online casinos legal in New Zealand? The Online Casino Gambling Act 2026, the DIA licence "
       "process, the 15-licence cap and the December 2026 cutoff."),

 "/gambling-winnings-tax-nz/": ("Gambling Winnings Tax NZ", "Do You Pay Tax?",
       "Do You Pay Tax on Casino and Betting Wins?",
       "Gambling winnings tax NZ: casual wins are not taxable income, but crypto is property and the "
       "gain on disposal is. A worked IRD example, plus when a player does become taxable."),

 "/how-we-rate/": ("How We Rate Online Casinos NZ", "Our Method",
       "How to Choose an Online Casino, and How We Score One",
       "How to choose an online casino NZ players can trust: our review methodology, the five scoring "
       "weights in full, and how we price an exit."),

 "/authors/": ("Our Authors &amp; Editors", "Who Writes This Site",
       "Who Writes and Fact-Checks Every Page",
       f"The people who write and fact-check {NAME}: five named editors with stated specialisms, "
       f"credentials and the pages each is responsible for."),

 "/about/": ("About Us", "The NZ Payout Desk",
       "Why We Price the Exit, Not the Welcome Offer",
       f"Who we are, how we make money, what our rankings can and cannot be bought with, and the "
       f"editorial standards every page on {NAME} is held to."),

 "/contact/": ("Contact Us", "Corrections &amp; Complaints",
       "Corrections, Complaints, Media and Commercial",
       f"Contact the {NAME} editorial team. Corrections answered within two working days, operator "
       f"complaints escalated, and a named person on every response."),

 "/responsible-gambling/": ("Responsible Gambling NZ", "Free Help &amp; Limits",
       "Free Help, Limits and Self-Exclusion in NZ",
       "Responsible gambling help in New Zealand: the Gambling Helpline on 0800 654 655, self-exclusion, "
       "bank blocks, deposit limits and how to spot the warning signs early."),

 "/terms/": ("Terms and Conditions", NAME,
       f"Using {NAME}",
       f"The terms governing use of {NAME}, including our affiliate relationships, the limits of "
       f"the information we publish and your responsibilities as a reader."),

 "/privacy/": ("Privacy Policy", "NZ Privacy Act 2020",
       "Written to the New Zealand Privacy Act 2020",
       f"How {NAME} collects, uses and protects personal information, written to the New Zealand "
       f"Privacy Act 2020 and the thirteen information privacy principles."),

 "/cookie-policy/": ("Cookie Policy", "What We Set &amp; Why",
       "Exactly What We Set, and How to Refuse It",
       f"What cookies {NAME} sets, what our affiliate tracking does, how long each cookie lasts and "
       f"exactly how to refuse or remove them."),

 "/new-casinos-nz/": ("New Online Casinos NZ", "Newest Casino Sites",
       "Brand New Casino Sites, Updated as They Launch",
       "New online casinos NZ players can join, updated as each one launches. What to check before "
       "joining a new casino site, and which brands have applied for a New Zealand licence."),

}

# Built once. Change MONTH in the block above and every title and H1 follows.
META = {p: (f"{a} [{MONTH_YEAR}]: {b}", d) for p, (a, b, _h, d) in PAGE_META.items()}
H1 = {p: f"{a} [{MONTH_YEAR}]: {h}" for p, (a, _b, h, _d) in PAGE_META.items()}


def title_parts(path):
    """(primary, secondary) for a page — used by the SEO report."""
    a, b, _h, _d = PAGE_META[path]
    return a, b


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=False)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def nzd(n):
    return "NZ$" + format(int(round(n)), ",d")


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def eyebrow(t):
    return f'<span class="eyebrow">{t}</span>'


def avatar(key, a, px, cls, lazy=True):
    """Photo where we have one, initials where we do not. The <img> carries an
    empty alt: the author's name always sits next to it in text, so announcing
    it twice is noise for a screen reader."""
    if a.get("photo"):
        # The byline photo is above the fold on every page, so it loads eagerly;
        # the larger author-box portraits further down do not.
        ld = "lazy" if lazy else "eager"
        return (f'<img class="{cls}" src="{a["photo"]}" alt="" width="{px}" height="{px}" '
                f'loading="{ld}" decoding="async">')
    return f'<span class="{cls}" aria-hidden="true">{a["initials"]}</span>'


def top_offer_strip(ops, kind="casino"):
    """The headline welcome offer, surfaced inside the hero.

    Without this the first bonus on a desktop page sits around 1200px down —
    roughly two screens — so a visitor can arrive, read the H1 and leave
    without ever seeing an offer. The whole strip is one sponsored link.
    Desktop only: on mobile the first card already carries the offer high up,
    and adding this there would push the table below the fold.
    """
    cand = [o for o in ops if (o.get("sports_bonus") if kind == "sports" else o.get("casino_bonus"))]
    if not cand:
        return ""
    op = cand[0]
    bonus, _orig = _B.bonus_in_nzd(op, kind)
    return (f'<a class="tof" href="{url_for(op, kind)}" rel="sponsored nofollow noopener" '
            f'target="_blank">'
            f'<span class="tof-tag">Top welcome offer</span>'
            f'<span class="tof-brand">'
            f'<img src="{op["logo"]}" alt="" width="84" height="30" loading="eager" decoding="async">'
            f'</span>'
            f'<span class="tof-bonus">{bonus}</span>'
            f'<span class="tof-cta">Claim <span aria-hidden="true">&rarr;</span></span></a>')


def byline(author, checker=None, light=False):
    """Every content page carries a named writer AND a named fact-checker.
    Competitor audit: only two of the ranking pages we tore down do both."""
    a = AUTHORS[author]
    cls = "byline byline--light" if light else "byline"
    out = [f'<div class="{cls}">',
           avatar(author, a, 34, "byline-av", lazy=False),
           f'<span>Written by <a href="/authors/#{author}"><b>{a["name"]}</b></a>'
           f'<span class="byline-role">, {a["role"]}</span></span>']
    if checker:
        c = AUTHORS[checker]
        out.append('<span class="sep">&middot;</span>')
        out.append(f'<span>Fact-checked by <a href="/authors/#{checker}">{c["name"]}</a></span>')
    out.append('<span class="sep">&middot;</span>')
    out.append(f'<span>Updated {UPDATED_NZ}</span>')
    out.append('</div>')
    return "".join(out)


def hero(h1, lead, stats=None, eyebrow_txt=None, author=None, checker=None):
    s = ['<header class="hero"><div class="wrap"><div class="hero-in">']
    if eyebrow_txt:
        s.append(eyebrow(eyebrow_txt))
    s.append(f"<h1>{h1}</h1>")
    # Block markup must not be wrapped in <p> — see the note in lede().
    s.append(f'<div class="hero-lead">{lead}</div>' if lead.lstrip().startswith("<")
             else f'<p class="hero-lead">{lead}</p>')
    if stats:
        s.append('<div class="hero-stats">')
        for b, sub in stats:
            s.append(f'<div class="hero-stat"><b>{b}</b><span>{sub}</span></div>')
        s.append("</div>")
    if author:
        s.append(byline(author, checker))
    s.append("</div></div></header>")
    return "".join(s)


def _lead_folded(lead):
    """First paragraph visible, the rest behind a CSS-only "Read more".

    Returns the lead untouched when there is only one paragraph, so a short
    lead never grows a control that reveals nothing.
    """
    m = re.match(r"\s*(<p\b[^>]*>.*?</p>)(.*)", lead, re.S)
    if not m:
        return lead
    first, rest = m.group(1), m.group(2).strip()
    if not rest:
        return lead
    return (f'{first}<details class="lede-more"><summary>'
            f'<span class="lede-more-a">Read more</span>'
            f'<span class="lede-more-b">Show less</span>'
            f'<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
            f'<path d="M2 4.5 6 8.5 10 4.5" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'</summary><div class="lede-more-in">{rest}</div></details>')


def lede(h1, lead, stats, eyebrow_txt, author, checker,
         toplist_h2, toplist_intro, toplist_html, toplist_note="",
         jump_items=None, ident="ranked", offer=""):
    """Hero + toplist as one flex column, re-ordered for mobile.

    Desktop order:  headline -> supporting copy -> jump/note -> toplist
    Mobile order:   headline -> toplist -> supporting copy -> jump/note

    The point is the fold: on a 393px phone the toplist starts around 470px
    instead of 1,766px, so the H1, the byline and the first offer are all
    visible without scrolling.
    """
    st = ""
    if stats:
        st = ('<div class="hero-stats">' + "".join(
              f'<div class="hero-stat"><b>{b}</b><span>{sub}</span></div>'
              for b, sub in stats) + "</div>")
    eb = f'<span class="eyebrow">{eyebrow_txt}</span>' if eyebrow_txt else ""
    jn = jump(jump_items) if jump_items else ""
    # An intro that already carries block markup (a callout, say) is emitted
    # as-is; a plain sentence gets wrapped so it can be re-ordered on mobile.
    if not toplist_intro:
        intro = ""
    elif toplist_intro.lstrip().startswith("<"):
        intro = f'<div class="lede-intro">{toplist_intro}</div>'
    else:
        intro = f'<p class="lede-intro">{toplist_intro}</p>'
    # Same rule for the lead. Wrapping block markup in <p> produces nested
    # paragraphs, which the parser closes early — the inner <p>s then escape
    # the .lede-lead class entirely and lose their colour on the dark hero.
    #
    # Only the opening paragraph is shown; anything after it folds into a
    # <details> behind a "Read more" control. The lead runs to several hundred
    # words on the money pages, and on desktop all of it sits between the H1 and
    # the leaderboard — a wall of text in front of the thing the reader came
    # for. This is CSS-only on purpose: there is no JavaScript on this site, and
    # <details> gives the disclosure, the keyboard behaviour and the
    # open/closed state to the browser for free.
    ld = (f'<div class="lede-lead">{_lead_folded(lead)}</div>' if lead.lstrip().startswith("<")
          else f'<p class="lede-lead">{lead}</p>')
    return f"""<div class="lede">
<header class="lede-a"><div class="wrap"><div class="hero-in">
{eb}<h1>{h1}</h1>
{offer}
</div></div></header>
<div class="lede-b"><div class="wrap"><div class="hero-in">
{ld}
{st}
</div></div></div>
<div class="lede-y"><div class="wrap"><div class="hero-in">
{byline(author, checker)}
</div></div></div>
<section class="lede-c" id="{ident}"><div class="wrap">
<h2 class="lede-h2">{toplist_h2}</h2>
{intro}
{toplist_html}
</div></section>
<div class="lede-d"><div class="wrap">
{toplist_note}
{jn}
</div></div>
</div>"""


def crumbs(trail):
    """trail: [(label, url), ...] excluding Home, which is prepended."""
    items = [("Home", "/")] + trail
    li = []
    for i, (label, u) in enumerate(items):
        last = i == len(items) - 1
        li.append(f"<li>{esc(label)}</li>" if last else f'<li><a href="{u}">{esc(label)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(li)}</ol></div></nav>'


def jump(items):
    a = "".join(f'<a href="#{i}">{esc(l)}</a>' for l, i in items)
    return f'<nav class="jump" aria-label="On this page">{a}</nav>'


def _esc_keep_entities(t):
    """Escape a label that may already contain named entities from our own copy.

    esc() would turn "&lsquo;" into "&amp;lsquo;" and print the entity rather
    than the quote mark. Split on entities, escape only the gaps."""
    return "".join(p if re.fullmatch(r"&[a-zA-Z]+;|&#\d+;", p) else esc(p)
                   for p in re.split(r"(&[a-zA-Z]+;|&#\d+;)", t))


def toc(items):
    li = "".join(f'<li><a href="#{i}">{_esc_keep_entities(l)}</a></li>' for l, i in items)
    return f'<nav class="toc" aria-labelledby="toc-h"><h2 id="toc-h">On this page</h2><ol>{li}</ol></nav>'


def sec(inner, ident=None, haze=False, wrap="wrap", tight=False):
    cls = "sec" + (" sec--haze" if haze else "") + (" sec--tight" if tight else "")
    # If a heading inside already carries this id, don't repeat it on the
    # section. Duplicate ids are invalid HTML and make anchor links ambiguous;
    # the heading is the better target anyway.
    i = f' id="{ident}"' if ident and f'id="{ident}"' not in inner else ""
    return f'<section class="{cls}"{i}><div class="{wrap}">{inner}</div></section>'


def sechead(h2, p=None, level=2, ident=None):
    i = f' id="{ident}"' if ident else ""
    out = [f'<div class="sec-head"><h{level}{i}>{h2}</h{level}>']
    if p:
        out.append(f"<p>{p}</p>")
    out.append("</div>")
    return "".join(out)


def keyfacts(rows):
    c = "".join(f'<div class="keyfact"><b>{b}</b><span>{s}</span></div>' for b, s in rows)
    return f'<div class="keyfacts">{c}</div>'


def note(body, kind="", title=None):
    k = f" note--{kind}" if kind else ""
    t = f"<h4>{title}</h4>" if title else ""
    return f'<div class="note{k}">{t}{body}</div>'


def table(headers, rows, caption=None, cls=""):
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="tw {cls}"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def op_cell(op, link=True):
    inner = f'<img src="{op["logo"]}" alt="{esc(op["name"])} logo" width="30" height="30" loading="lazy">'
    nm = f'<a href="/casino-reviews/{op["slug"]}/">{esc(op["name"])}</a>' if link else esc(op["name"])
    return f'<span class="t-logo">{inner}{nm}</span>'


def proscons(pros, cons):
    p = "".join(f"<li>{x}</li>" for x in pros)
    c = "".join(f"<li>{x}</li>" for x in cons)
    return (f'<div class="pc"><div class="pc-col pc-pro"><h4>What works</h4><ul>{p}</ul></div>'
            f'<div class="pc-col pc-con"><h4>What does not</h4><ul>{c}</ul></div></div>')


def cards(items, cls="grid--3"):
    """items: (title, body, href|None, icon_letter|None)"""
    out = [f'<div class="grid {cls}">']
    for it in items:
        title, body = it[0], it[1]
        href = it[2] if len(it) > 2 else None
        tag = f'<a class="card" href="{href}">' if href else '<div class="card">'
        end = "</a>" if href else "</div>"
        more = '<span class="card-more">Read more &rarr;</span>' if href else ""
        out.append(f"{tag}<h3>{title}</h3><p>{body}</p>{more}{end}")
    out.append("</div>")
    return "".join(out)


def steps(items):
    li = "".join(f"<li><h4>{t}</h4><p>{b}</p></li>" for t, b in items)
    return f'<ol class="steps">{li}</ol>'


def faq(items, heading="Frequently asked questions", ident="faq", intro=None):
    """Returns (html, schema_entities). Every FAQ on the site feeds FAQPage
    schema from this one function, so the markup and the structured data can
    never drift apart."""
    out = [f'<h2 id="{ident}">{heading}</h2>']
    if intro:
        out.append(f"<p>{intro}</p>")
    out.append('<div class="faq">')
    ents = []
    for q, a in items:
        out.append(f"<details><summary>{q}</summary><div class=\"faq-body\">{a}</div></details>")
        ents.append({"@type": "Question", "name": strip_tags(q),
                     "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}})
    out.append("</div>")
    return "".join(out), ents


def authorbox(key, extra=None):
    a = AUTHORS[key]
    cr = " &middot; ".join(a["creds"])
    ex = f"<p>{extra}</p>" if extra else ""
    return (f'<div class="authorbox" id="ab-{key}">' + avatar(key, a, 62, "av")
            + f'<div><h3>{a["name"]}</h3><div class="role">{a["role"]} &middot; writing since {a["since"]}</div>'
            f'<p>{a["bio"]}</p>{ex}<p><small><b>Credentials:</b> {cr}. '
            f'<a href="/authors/#{key}">Full profile and contact</a>.</small></p></div></div>')


def verdict(title, body):
    return f'<div class="verdict"><h3>{title}</h3>{body}</div>'


def scorebars(rows):
    out = ['<div class="scores">']
    for label, val, mx in rows:
        pct = round(val / mx * 100)
        out.append(f'<div class="score-row"><span>{label}</span>'
                   f'<span class="track"><i style="width:{pct}%"></i></span>'
                   f'<b>{val}/{mx}</b></div>')
    out.append("</div>")
    return "".join(out)


def disclaimer(compact=False):
    if compact:
        return '<p class="lb-terms">18+. T&amp;Cs apply. Play responsibly.</p>'
    return ('<p class="disc"><b>18+ only.</b> Gambling involves risk and should never be treated as a '
            'way to make money. Bonus offers are subject to the operator&rsquo;s terms and conditions, '
            'which change without notice — always read them before depositing. If gambling is causing '
            'harm, free and confidential help is available on '
            '<a href="tel:0800654655">0800 654 655</a>, 24 hours a day. '
            '<a href="/responsible-gambling/">More support options</a>.</p>')


# ---------------------------------------------------------------------------
# The leaderboard — the single most important component on the site.
# Competitor pattern we keep: ranked cards above the fold, rating, bonus,
# CTA, 18+ microcopy. Competitor gap we close: the wagering requirement is
# converted to the NZD turnover it actually demands, right in the card.
# ---------------------------------------------------------------------------
# Short badges for the leaderboard chip. A page can override any of these by
# passing `flags`; anything not listed here simply shows no badge, which is
# better than truncating a sentence.
BADGE = {
    "spinjo": "Best overall", "kingdom": "Fastest payout", "crownslots": "Biggest bonus",
    "fortune-play": "Crash games", "lucky7even": "No deposit", "rivo": "Best on mobile",
    "smash": "Lowest wagering", "lucky-vibe": "Best VIP", "madcasino": "Casino + sport",
    "lucky-circus": "NZ$10 minimum", "ivibet": "Live dealer", "spino": "0x wagering",
    "hellspin": "Tournaments", "roby-casino": "Disclosure gap", "slotsgem": "Quiet lobby",
    "rooster-bet": "Best combo", "gunsbet": "Biggest sports offer",
    "betandplay": "Best in-play", "ivibet-sportsbook": "Netball markets",
}


def leaderboard(ops, kind="casino", cta="Visit Site", show_from=1, flags=None):
    flags = flags or {}
    out = ['<div class="lb">',
           '<div class="lb-head"><span>#</span><span>Casino</span><span>Why we list it</span>'
           '<span>Our score</span><span>Claim</span></div>']
    for i, op in enumerate(ops, show_from):
        top = " lb-row--top" if i == 1 else ""
        flag = flags.get(op["slug"], BADGE.get(op["slug"], ""))
        fl = (f'<p class="lb-badge">'
              f'<span class="chip chip--gold">{flag}</span></p>') if flag else ""
        bonus, _orig = _B.bonus_in_nzd(op, kind)
        if not bonus and kind != "casino":
            bonus, _orig = _B.bonus_in_nzd(op, "casino")
        # A converted headline carries its provenance on the card, not in a
        # footnote — the advertised figure is what the reader will see at the
        # cashier, and hiding it would make the conversion look like the offer.
        # It rides on the existing label row rather than a line of its own,
        # because a new line here costs 20px and the fold has 9px to spare.
        _adv = re.sub(r"^[\d,]+%\s*(up\s+)?to\s*", "", _orig.split("+")[0].strip()) if _orig else ""
        fx = f' <span class="lb-fx">&middot; {esc(_adv)} advertised</span>' if _orig else ""
        bonus_html = (f'<p class="lb-bonus"><b>Welcome offer{fx}</b> {bonus}'
                      f'<a class="lb-claim" href="{url_for(op, kind)}" rel="sponsored nofollow noopener" '
                      f'target="_blank">Claim this offer <span aria-hidden="true">&rarr;</span></a></p>'
                      if bonus else "")
        chips = []
        if op.get("wagering"):
            chips.append(f'<span class="chip">{esc(op["wagering"])} wagering</span>')
        pay = op.get("payout_ewallet") or op.get("payout_crypto")
        if pay:
            chips.append(f'<span class="chip chip--yes">{esc(pay)} payout</span>')
        if op.get("min_deposit"):
            chips.append(f'<span class="chip">Min {esc(op["min_deposit"])}</span>')
        if op.get("crypto"):
            chips.append('<span class="chip chip--info">Crypto</span>')
        score = op.get("rating", 8.0)
        out.append(
            f'<div class="lb-row{top}">'
            f'<div class="lb-rank">{i:02d}</div>'
            f'<div class="lb-logo"><img src="{op["logo"]}" alt="{esc(op["name"])} logo" '
            f'width="150" height="60" loading="{"eager" if i <= 2 else "lazy"}"></div>'
            f'<div class="lb-brand"><p class="lb-name">'
            f'<a href="/casino-reviews/{op["slug"]}/">{esc(op["name"])}</a></p>'
            # The badge sits directly after the name so that on mobile, where
            # both go inline, it reads as "Spinjo Casino · Best overall" on one
            # line instead of costing a line of its own.
            f'{fl}'
            f'<p class="lb-sub">{op.get("sub") or op.get("tagline","")}</p>'
            f'{bonus_html}<div class="lb-meta">{"".join(chips)}</div></div>'
            f'<div class="lb-score"><div class="lb-score-top">{score}<span>/10</span></div>'
            f'<div class="lb-bar"><i style="width:{round(score*10)}%"></i></div></div>'
            f'<div class="lb-cta"><a class="btn btn--sm btn--wide" href="{url_for(op, kind)}" '
            f'rel="sponsored nofollow noopener" target="_blank">{cta}</a>'
            f'<a class="lb-review" href="/casino-reviews/{op["slug"]}/">Read review</a>'
            f'{disclaimer(compact=True)}</div></div>')
    out.append(
        '<p class="lb-note"><b>How to read this table.</b> The order is commercial &mdash; brands we hold '
        'stronger affiliate agreements with appear nearer the top. <b>Our score is not:</b> it is produced '
        'by testing against the <a href="/how-we-rate/">six published weights</a> before any commercial '
        'term is looked at, and it is printed on every row above. Sort by the score in your head and you '
        'have our genuine editorial view. <a href="/how-we-rate/#money">How we are funded</a>.</p>')
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Schema.  Self-referencing canonical on every page; Organization and WebSite
# on every page; page-specific entities appended by the caller.
# ---------------------------------------------------------------------------
def schema_org():
    return {
        "@type": "Organization",
        "@id": f"{SITE}/#organization",
        "name": NAME,
        "legalName": LEGAL,
        "url": SITE + "/",
        "logo": {"@type": "ImageObject", "url": f"{SITE}/favicon-192x192.png",
                 "width": 192, "height": 192},
        "email": EMAIL,
        "foundingDate": "2026",
        "areaServed": {"@type": "Country", "name": "New Zealand"},
        "knowsAbout": ["Online casinos", "Online pokies", "New Zealand gambling law",
                       "Casino bonuses", "Responsible gambling", "Sports betting"],
        "publishingPrinciples": f"{SITE}/how-we-rate/",
        "ethicsPolicy": f"{SITE}/about/#editorial",
        "contactPoint": [{"@type": "ContactPoint", "contactType": "editorial",
                          "email": EMAIL, "areaServed": "NZ",
                          "availableLanguage": ["en-NZ"]}],
    }


def schema_site():
    return {
        "@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/",
        "name": NAME, "inLanguage": "en-NZ",
        "publisher": {"@id": f"{SITE}/#organization"},
    }


def schema_person(key):
    a = AUTHORS[key]
    return {"@type": "Person", "@id": f"{SITE}/authors/#{key}", "name": a["name"],
            "jobTitle": strip_tags(a["role"]), "description": strip_tags(a["bio"]),
            "knowsAbout": [t.strip() for t in strip_tags(a["specialism"]).split(",") if t.strip()],
            "worksFor": {"@id": f"{SITE}/#organization"},
            "image": f"{SITE}{a['photo']}" if a.get("photo") else None,
            "url": f"{SITE}/authors/#{key}"}


def schema_breadcrumb(path, trail):
    items = [("Home", "/")] + trail
    return {"@type": "BreadcrumbList", "@id": f"{SITE}{path}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": strip_tags(n),
                 "item": f"{SITE}{u}"} for i, (n, u) in enumerate(items)]}


def schema_article(path, title, desc, author, checker=None, kind="Article"):
    a = {"@type": kind, "@id": f"{SITE}{path}#article",
         "headline": strip_tags(title)[:110], "description": strip_tags(desc),
         "inLanguage": "en-NZ",
         "isPartOf": {"@id": f"{SITE}/#website"},
         "mainEntityOfPage": {"@id": f"{SITE}{path}#webpage"},
         "datePublished": PUBLISHED, "dateModified": UPDATED,
         "author": {"@id": f"{SITE}/authors/#{author}"},
         "publisher": {"@id": f"{SITE}/#organization"}}
    if checker:
        a["reviewedBy"] = {"@id": f"{SITE}/authors/#{checker}"}
    return a


def schema_itemlist(path, ops, kind="casino"):
    """ItemList of the ranked operators. Only one competitor we tore down ships
    this on a hub page — an open surface."""
    return {"@type": "ItemList", "@id": f"{SITE}{path}#toplist",
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "numberOfItems": len(ops),
            "itemListElement": [
                {"@type": "ListItem", "position": i,
                 "item": {"@type": "Organization", "name": op["name"],
                          "url": f"{SITE}/casino-reviews/{op['slug']}/",
                          "image": SITE + op["logo"]}}
                for i, op in enumerate(ops, 1)]}


def schema_review(op, author):
    r = {"@type": "Review", "@id": f"{SITE}/casino-reviews/{op['slug']}/#review",
         "itemReviewed": {"@type": "Organization", "name": op["name"],
                          "@id": f"{SITE}/casino-reviews/{op['slug']}/#brand",
                          "image": SITE + op["logo"]},
         "reviewRating": {"@type": "Rating", "ratingValue": op["rating"],
                          "bestRating": 10, "worstRating": 1},
         "author": {"@id": f"{SITE}/authors/#{author}"},
         "publisher": {"@id": f"{SITE}/#organization"},
         "datePublished": PUBLISHED, "dateModified": UPDATED,
         "reviewBody": strip_tags(op.get("verdict", ""))[:600]}
    return r


def schema_dataset(path, name, description, variables, technique, coverage):
    """Type an original dataset as a dataset.

    The Exit Ledger is not prose with numbers in it — it is a table of
    per-operator figures, derived by one published method, covering a stated
    period. Dataset is what that is, and it carries the two properties that
    matter for a claim of originality: measurementTechnique, which says how the
    numbers were produced, and variableMeasured, which says what they are.
    """
    return {"@type": "Dataset", "@id": f"{SITE}{path}#dataset",
            "name": name, "description": description,
            "url": f"{SITE}{path}",
            "creator": {"@id": f"{SITE}/#organization"},
            "publisher": {"@id": f"{SITE}/#organization"},
            "isAccessibleForFree": True,
            "inLanguage": "en-NZ",
            "spatialCoverage": {"@type": "Country", "name": "New Zealand"},
            "temporalCoverage": coverage,
            "dateModified": UPDATED,
            "measurementTechnique": technique,
            "variableMeasured": [{"@type": "PropertyValue", "name": v} for v in variables]}


def schema_faq(path, ents):
    return {"@type": "FAQPage", "@id": f"{SITE}{path}#faq", "mainEntity": ents}


def _ld_plain(node):
    """JSON-LD values are data, not markup. Schema strings are reused from the
    page body, where an em dash is written "&mdash;" — inside a JSON string
    that reaches the consumer as those eight literal characters, so Curacao
    arrives as "Cura&ccedil;ao". Unescaping at the serialisation boundary fixes
    every node at once and keeps the builders above free of the concern."""
    if isinstance(node, dict):
        return {k: _ld_plain(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_ld_plain(v) for v in node]
    if isinstance(node, str):
        return html.unescape(node)
    return node


def schema_webpage(path, title, desc):
    return {"@type": "WebPage", "@id": f"{SITE}{path}#webpage", "url": f"{SITE}{path}",
            "name": strip_tags(title), "description": strip_tags(desc),
            "inLanguage": "en-NZ", "isPartOf": {"@id": f"{SITE}/#website"},
            "datePublished": PUBLISHED, "dateModified": UPDATED,
            "breadcrumb": {"@id": f"{SITE}{path}#breadcrumb"},
            "about": {"@id": f"{SITE}/#organization"}}


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
def _nav(path):
    """Nested nav. Dropdowns open on :hover and :focus-within — no JavaScript,
    and keyboard users reach every child by tabbing."""
    out = []
    for label, u, kids in NAV:
        kids = nav_children(kids)
        cur = ' aria-current="page"' if u == path else ""
        if not kids:
            out.append(f'<a href="{u}"{cur}>{esc(label)}</a>')
            continue
        # A parent is highlighted when the current page is anywhere beneath it.
        here = any(k == path for _, k in kids) or u == path
        sect = ' class="nav-top nav-top--here"' if here else ' class="nav-top"'
        wide = " nav-sub--wide" if len(kids) > 8 else ""
        CUR = ' aria-current="page"'
        links = "".join(
            '<a href="%s"%s>%s</a>' % (k, CUR if k == path else "", esc(t))
            for t, k in kids)
        out.append(
            f'<span class="nav-grp">'
            f'<a href="{u}"{sect}>{esc(label)}'
            f'<svg viewBox="0 0 10 6" aria-hidden="true" focusable="false">'
            f'<path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round"/></svg></a>'
            f'<span class="nav-sub{wide}">{links}</span></span>')
    return "".join(out)


# Grouped for the hamburger. Reviews are generated from OPS so a new operator
# appears in the menu automatically. check_site.py verifies that every page in
# the sitemap is reachable from here.
def menu_groups():
    return [
        ("Casinos", [
            ("Best online casino sites NZ", "/"),
            ("Online casinos NZ", "/online-casinos/"),
            ("Online pokies NZ", "/online-pokies/"),
            ("Live casino NZ", "/live-casinos/"),
            ("Best payout casinos", "/high-payout-casinos/"),
            ("Fast payout casinos", "/fast-payout-casinos/"),
            ("Crypto casinos NZ", "/best-crypto-casinos/"),
            ("New casinos NZ", "/new-casinos-nz/"),
        ]),
        ("Bonuses", [
            ("Casino bonus NZ", "/online-casinos/bonuses/"),
            ("No deposit bonus NZ", "/no-deposit-casinos/"),
        ]),
        ("Betting", [
            ("Online betting NZ", "/online-betting/"),
            ("Sports betting sites", "/best-sports-betting-sites/"),
        ]),
        ("Guides", [
            ("Licensed online casinos NZ", "/nz-online-casino-law/"),
            ("Tax on gambling winnings", "/gambling-winnings-tax-nz/"),
            ("Casino payment methods", "/payment-methods/"),
            ("How we rate casinos", "/how-we-rate/"),
        ]),
        ("Casino reviews", [("All casino reviews", "/casino-reviews/")]
            + [(o["name"], f"/casino-reviews/{o['slug']}/") for o in OPS]),
        ("Company", [
            ("About us", "/about/"),
            ("Contact us", "/contact/"),
            ("Authors", "/authors/"),
            ("Responsible gambling", "/responsible-gambling/"),
        ]),
        ("Legal", [
            ("Terms and conditions", "/terms/"),
            ("Privacy policy", "/privacy/"),
            ("Cookie policy", "/cookie-policy/"),
        ]),
    ]


def _menu(path):
    """The full-site menu, as a <details> disclosure — no JavaScript.

    <summary> is natively focusable and toggles on Enter/Space, so this is
    keyboard- and screen-reader-accessible without a line of script. On mobile
    it replaces the horizontally-scrolling nav strip, which cut links off; on
    desktop it sits beside the primary nav as the route to everything else.
    """
    cols = []
    for title, links in menu_groups():
        items = []
        for label, u in links:
            cur = ' aria-current="page"' if u == path else ""
            items.append(f'<li><a href="{u}"{cur}>{label}</a></li>')
        cols.append(f'<div class="menu-col"><p class="menu-h">{title}</p>'
                    f'<ul>{"".join(items)}</ul></div>')
    return f"""<details class="menu">
<summary aria-label="Open the full site menu"><span class="menu-bars" aria-hidden="true"></span><span class="menu-lbl">Menu</span></summary>
<div class="menu-panel"><div class="wrap">
<div class="menu-grid">{''.join(cols)}</div>
<p class="menu-foot">R18 &middot; Gambling can be harmful. Free, confidential help on
<a href="tel:0800654655">0800 654 655</a>, 24 hours.</p>
</div></div>
</details>"""


def _footer():
    cols = []
    for title, links in FOOTER:
        li = "".join(f'<li><a href="{u}">{l}</a></li>' for l, u in links)
        cols.append(f'<div class="foot-col"><h4>{title}</h4><ul>{li}</ul></div>')
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-top">
<div class="foot-about">
<a class="brand" href="/"><span class="brand-mark" aria-hidden="true">{LOGO_MARK}</span>
<span class="brand-txt"><span class="brand-word">{LOGO_NAME}{LOGO_SUFFIX}</span><span class="brand-tag">{TAG}</span></span></a>
<p>Independent reviews of the online casino sites New Zealanders can actually use. We price the exit
&mdash; the withdrawal ceiling, the instalments it forces and the days that costs &mdash; from each
operator&rsquo;s own published terms, and we publish the scoring weights behind every number.</p>
<div class="foot-badges">
<span class="foot-badge">R18</span><span class="foot-badge">NZD verified</span>
<span class="foot-badge">Ceilings verified</span><span class="foot-badge">Independent scores</span></div>
</div>
{''.join(cols)}
</div>
{disclaimer()}
<p class="disc"><b>Affiliate disclosure and listing order.</b> {NAME} is funded by commission. If you
open an account with an operator through a link on this site we may be paid, at no cost to you.
<b>The order brands are listed in reflects our commercial agreements with them, so treat it as a
starting point rather than a verdict.</b> Our 0&ndash;10 score does not: it is produced by testing
against the published weights on <a href="/how-we-rate/">how we rate</a>, before commercial terms are
looked at, and it appears on every card and review on this site. Where the order and the score
disagree, the score is the honest signal &mdash; and we are paid nothing extra for a positive one.</p>
<p class="disc"><b>Legal position.</b> Online casino gambling supplied from offshore is in a licensing
transition under the Online Casino Gambling Act 2026; offshore sports and racing betting may lawfully
be offered only by TAB NZ. In both cases the prohibition binds the operator, not you — no New Zealand
law makes it an offence for an individual to place a bet. See
<a href="/nz-online-casino-law/">NZ online casino law</a> for the detail and the dates.</p>
<div class="foot-bot">
<span>&copy; {YEAR} {LEGAL}. All rights reserved.</span>
<span><a href="/about/">About</a> &middot; <a href="/contact/">Contact</a> &middot;
<a href="/authors/">Authors</a> &middot; <a href="/terms/">Terms</a> &middot;
<a href="/privacy/">Privacy</a> &middot; <a href="/cookie-policy/">Cookies</a> &middot;
<a href="/responsible-gambling/">Responsible gambling</a> &middot;
<a href="/sitemap.xml">Sitemap</a> &middot; <a href="/robots.txt">Robots</a></span>
</div></div></footer>"""


def _bind_mainentity(graph):
    """Point the WebPage at its ItemList, and type it as a CollectionPage.

    A ranked list of operators IS the point of a hub page. Emitting the
    ItemList as a loose node states that a list exists somewhere on the page;
    binding it as mainEntity states that the page is that list, which is the
    claim we actually want to make.
    """
    page_node = next((n for n in graph if n.get("@type") == "WebPage"), None)
    lst = next((n for n in graph if n.get("@type") == "ItemList"), None)
    if not page_node or not lst:
        return
    page_node["@type"] = ["WebPage", "CollectionPage"]
    page_node["mainEntity"] = {"@id": lst["@id"]}


def page(path, body, schema=None, title=None, desc=None, cls=""):
    """Assemble the full document. Canonical is always self-referencing."""
    t, d = META.get(path, (title, desc))
    if title:
        t = title
    if desc:
        d = desc
    if not t or not d:
        raise KeyError(f"no META entry for {path}")
    canon = f"{SITE}{path}"
    graph = [schema_org(), schema_site()] + (schema or [])
    _bind_mainentity(graph)
    ld = json.dumps({"@context": "https://schema.org", "@graph": _ld_plain(graph)},
                    separators=(",", ":"), ensure_ascii=False).replace("<", "\\u003C")
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="rating" content="adult">
<meta name="author" content="{NAME}">
<meta name="geo.region" content="NZ">
<meta name="theme-color" content="#1C2E26">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_NZ">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/images/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/images/og-default.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="icon" type="image/png" sizes="144x144" href="/favicon-144x144.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
<div class="topstrip"><div class="wrap">
<p class="ts"><b>R18</b> &middot;<span class="ts-lg"> Gambling can be harmful. Free help</span><span
 class="ts-sm"> Gambling can harm &middot;</span> <a href="tel:0800654655">0800 654 655</a>
<span class="ts-lg sep" aria-hidden="true">&middot;</span> <span class="ts-sm">&middot;</span>
We earn commission<span class="ts-lg"> from links &mdash; <a href="/about/#money">how that works</a></span></p>
</div></div>
<header class="hdr"><div class="wrap hdr-in">
<a class="brand" href="/"><span class="brand-mark" aria-hidden="true">{LOGO_MARK}</span>
<span class="brand-txt"><span class="brand-word">{LOGO_NAME}{LOGO_SUFFIX}</span><span class="brand-tag">{TAG}</span></span></a>
<nav class="nav" aria-label="Main">{_nav(path)}</nav>
{_menu(path)}
</div></header>
<main id="main">
{body}
</main>
{_footer()}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Writer with content-hash lastmod
# ---------------------------------------------------------------------------
# Stylesheet cache-buster. Browsers hold a CSS file for a long time, so a
# deploy that only changes site.css otherwise reaches returning visitors with
# the old layout. The query string is the file's own content hash: it changes
# when the CSS changes and never otherwise.
try:
    CSS_V = hashlib.sha256(
        open(os.path.join(ROOT, "assets", "css", "site.css"), "rb").read()
    ).hexdigest()[:8]
except OSError:
    CSS_V = "0"

_LASTMOD_PATH = os.path.join(BUILD, "lastmod.json")
try:
    LASTMOD = json.load(open(_LASTMOD_PATH))
except Exception:
    LASTMOD = {}
TODAY = datetime.date.today().isoformat()
_NZ_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
PAGES = []


def nzdate(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {_NZ_MONTHS[m-1]} {y}"


def write(path, doc, priority=0.7, freq="weekly"):
    """Resolve the freshness stamp from a content hash, then emit the file.
    A page whose content did not change keeps its previous date, so
    <lastmod> in the sitemap is a real signal rather than build noise."""
    stable = doc.replace(UPDATED, "").replace(UPDATED_NZ, "")
    h = hashlib.sha256(stable.encode()).hexdigest()[:16]
    rec = LASTMOD.get(path)
    if not rec or rec.get("hash") != h:
        rec = {"hash": h, "date": TODAY}
        LASTMOD[path] = rec
    doc = doc.replace(UPDATED, rec["date"]).replace(UPDATED_NZ, nzdate(rec["date"]))
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append((path, rec["date"], priority, freq))
    return path


def save_lastmod():
    json.dump(LASTMOD, open(_LASTMOD_PATH, "w"), indent=1, sort_keys=True)
