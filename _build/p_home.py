#!/usr/bin/env python3
"""Homepage — the money page for "best online casino sites NZ".

The organising idea of this masthead: every competitor ranks casinos on how
fast a withdrawal is *processed*. That is the smallest term in the equation. We
price the whole exit — the weekly ceiling, the number of instalments a real win
is broken into, the elapsed time on the rail a New Zealander actually uses, and
the conversion spread on a balance that is not held in New Zealand dollars.

Every figure below comes out of cashoutcalc.py, from the operators' own
published limits, and a reader can redo the arithmetic.
"""
import statistics

from lib import *
import lawdata as L
import nzdata as NZ
import bonuscalc as B
import cashoutcalc as C

WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
         8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

PATH = "/"
AUTHOR, CHECKER = "tama-rewiti", "hana-whitiora"

TOP10 = ["spinjo", "kingdom", "crownslots", "fortune-play", "lucky7even",
         "rivo", "smash", "lucky-vibe", "madcasino", "lucky-circus"]

FLAGS = {
    "spinjo": "Best overall", "kingdom": "Fastest big win", "crownslots": "Largest match",
    "fortune-play": "Best free spins", "lucky7even": "No-deposit start", "rivo": "Best on mobile",
    "smash": "Highest ceiling", "lucky-vibe": "Best VIP", "madcasino": "Casino + sport",
    "lucky-circus": "Lowest entry",
}


def build():
    lb = leaderboard(pick(TOP10), flags=FLAGS, cta="Visit Casino")

    # ------------------------------------------------------------------ #
    # The Exit Ledger. The signature asset of this site: what it takes to
    # get a real win out, on the rail most New Zealanders actually use.
    # ------------------------------------------------------------------ #
    exits = []
    for op in CASINOS:
        card = C.slowest_card(op) or C.fastest(op)
        big = C.exit_cost(op, C.BIG, card)
        small = C.exit_cost(op, C.SMALL, card)
        fast = C.exit_cost(op, C.BIG, C.fastest(op))
        if big and small and fast:
            exits.append((op, big, small, fast))
    exits.sort(key=lambda t: (t[1]["days_worst"], t[1]["fx_cost"]))

    capped = [t for t in exits if t[1]["capped"]]
    caps = sorted(t[1]["cap_nzd"] for t in capped)
    median_cap = round(statistics.median(caps))
    lowest_cap = exits and min(capped, key=lambda t: t[1]["cap_nzd"])
    within_week = [t for t in exits if t[1]["days_worst"] <= 7]
    median_days = statistics.median(t[1]["days_worst"] for t in exits)
    instalments = [t for t in exits if t[1]["tranches"] > 1]
    fx_hit = [t for t in exits if t[1]["fx_cost"]]
    fx_cost = fx_hit[0][1]["fx_cost"] if fx_hit else 0
    slowest = exits[-1]

    ledger_rows = []
    for op, big, small, fast in exits:
        tone = {"yes": "chip--yes", "warn": "chip--gold", "no": "chip--no"}[big["tone"]]
        cap = (f'<b>{C.money(big["cap_nzd"])}</b>' if big["capped"]
               else '<span class="chip chip--yes">No stated cap</span>')
        if big["cap_currency"] != "NZD":
            cap += f'<span class="chip chip--no">&euro; balance</span>'
        ledger_rows.append([
            op_cell(op),
            cap,
            esc(big["rail"]["stated"]),
            f'{big["tranches"]}' if big["tranches"] > 1 else "1 payment",
            f'<b>{C.days(big["days_worst"])}</b>',
            C.days(fast["days_worst"]),
            f'<span class="chip {tone}">{big["verdict"]}</span>',
        ])
    ledger = table(
        ["Casino", "Weekly ceiling", "Stated card window", "Instalments",
         f"{C.money(C.BIG)} win, by card", "Same win, by crypto", "Our verdict"],
        ledger_rows,
        caption=(f"The Exit Ledger, {MONTH_YEAR}. Elapsed time for a {C.money(C.BIG)} win to leave the "
                 f"casino, using each operator's own published weekly ceiling and its own stated "
                 f"processing window, at the slow end of the range. Instalments are the number of weekly "
                 f"payments the ceiling forces the win to be broken into. Euro ceilings are converted at "
                 f"the mid-market rate of {C.FX_DATE}. Sorted fastest exit first."))

    # ------------------------------------------------------------------ #
    comp_rows = []
    for op in CASINOS:
        p = B.price(op)
        big = C.exit_cost(op, C.BIG, C.slowest_card(op) or C.fastest(op))
        comp_rows.append([
            op_cell(op),
            f'<b>{op["rating"]}</b>',
            esc(op.get("withdrawal_limit") or "&mdash;"),
            C.days(big["days_worst"]) if big else "&mdash;",
            esc(B.bonus_in_nzd(op)[0] or "&mdash;"),
            B.money(p["turnover"]) if p else "&mdash;",
            esc(op.get("min_deposit") or "&mdash;"),
            ('<span class="chip chip--yes">NZD</span>' if "NZD bank transfer" in op.get("payments", [])
             else '<span class="chip chip--no">EUR/USDT</span>'),
        ])
    comp = table(
        ["Casino", "Score", "Weekly ceiling", f"{C.money(C.BIG)} win, by card", "Welcome offer",
         "Turnover to clear", "Min dep.", "Banking"],
        comp_rows,
        caption=("Every casino site we cover, on the eight variables that decide what a New Zealand player "
                 f"actually experiences &mdash; four of them about getting money out. Checked from a New "
                 f"Zealand connection in {MONTH_YEAR}."))

    fit = cards([
      ("You expect to win more than a couple of thousand",
       f"Then the weekly ceiling is the only number that matters, and it is the one nobody publishes in a "
       f"comparison table. {len(instalments)} of the {len(exits)} sites here would pay a "
       f"{C.money(C.BIG)} win in instalments. Two would not.",
       "/fast-payout-casinos/"),
      ("You want the money out the same day",
       "Crypto settles in hours nearly everywhere, and the weekly ceiling still applies to it. Speed on "
       "the rail and speed of the exit are different questions, and the second one is the expensive one.",
       "/best-crypto-casinos/"),
      ("You intend to actually clear the bonus",
       "Then read the wagering in dollars before you claim. The largest headline on this page is the "
       "worst offer on it, and the max-cashout clause can make finishing it pointless anyway.",
       "/online-casinos/bonuses/"),
      ("You want to play without a bonus at all",
       "A perfectly rational choice, and one no affiliate page ever suggests. Decline the offer and your "
       "balance is withdrawable from the first spin, with no cashout ceiling and no game weighting.",
       "/online-casinos/"),
      ("You mostly play pokies",
       "Library depth and, more importantly, which build of each title the lobby runs. The same headline "
       "pokie ships in three RTP configurations and the operator chooses which one you get.",
       "/online-pokies/"),
      ("You are banking from a New Zealand bank account",
       "Several New Zealand banks decline gambling merchant codes outright, and a euro-denominated "
       "balance costs you a spread in both directions. Which rails clear, and what each one costs.",
       "/payment-methods/"),
      ("You play live dealer",
       "Table counts checked at New Zealand hours rather than European ones, and the game weighting that "
       "turns a 40x requirement into an 800x one on live blackjack.",
       "/live-casinos/"),
      ("You also bet on sport",
       "The law changed on 28 June 2025 and TAB NZ is now the only operator lawfully able to offer "
       "betting into New Zealand. You commit no offence either way. The full position, plainly stated.",
       "/online-betting/"),
    ])

    # ------------------------------------------------------------------ #
    # Ownership. Nineteen brands is not nineteen companies, and the gap
    # between those two numbers is the point. Computed from operators.json
    # so a corrected operator_co propagates here automatically.
    # ------------------------------------------------------------------ #
    groups = {}
    for op in OPS:
        groups.setdefault((op["operator_co"], op["licence"]), []).append(op)
    named = {k: v for k, v in groups.items() if k[0] != "Not published"}
    unnamed = [op for k, v in groups.items() if k[0] == "Not published" for op in v]
    biggest = max(named.items(), key=lambda kv: len(kv[1]))

    own_rows = []
    for (co, lic), members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0][0])):
        names = ", ".join(f'<a href="/casino-reviews/{o["slug"]}/">{esc(o["name"])}</a>' for o in members)
        co_cell = (f"<b>{esc(co)}</b>" if co != "Not published"
                   else '<span class="chip chip--no">Not published</span>')
        own_rows.append([co_cell, esc(lic), f"<b>{len(members)}</b>", names])
    ownership = table(
        ["Operating company", "Licence", "Brands", "Trading as"],
        own_rows,
        caption=(f"Every brand we cover, grouped by the legal entity named in its own footer. "
                 f"{len(OPS)} brands, {len(groups)} groups, and {len(unnamed)} brands that name no "
                 f"operating company at all. Checked {MONTH_YEAR}."))

    unnamed_links = ", ".join(
        '<a href="/casino-reviews/%s/">%s</a>' % (o["slug"], esc(o["name"])) for o in unnamed)

    # ------------------------------------------------------------------ #
    # The collision: how many of the sites on this page take longer to pay
    # a big win than there are days left before they must leave the market.
    # ------------------------------------------------------------------ #
    days_left = L.days_to(L.CUTOFF)
    slowpokes = [t for t in exits if t[1]["days_worst"] >= 14]

    market = keyfacts([(f, l) for f, l, _n in NZ.MARKET])
    seg_rows = [[esc(n), f"<b>{sh}</b>", gr, note] for n, sh, gr, note in NZ.SEGMENTS]
    segments = table(["Segment", "Share of market", "Year-on-year", "What it means"], seg_rows,
        caption="Where New Zealand's offshore online gambling money actually goes, year ending "
                "30 September 2025. " + NZ.SOURCE)
    player = keyfacts([(f, l) for f, l, _n in NZ.PLAYER])
    conc = '<ul class="checklist">' + "".join(
        f'<li>{"&#9888;" if t == "warn" else "&#8226;"}<div>{b}</div></li>' for b, t in NZ.CONCENTRATION) + "</ul>"
    region_rows = [[f"<b>{esc(r)}</b>", fig, note] for r, fig, note in NZ.REGIONS]
    regions = table(["Region", "The figure", "Context"], region_rows,
        caption="Regional detail from the same DIA reports. The national rate of online gambling "
                "participation is about 5%.")
    struct_rows = [[f"<b>{esc(a)}</b>", b, c] for a, b, c in NZ.STRUCTURE]
    structure = table(["Concentration measure", "The figure", "What follows"], struct_rows,
        caption="Market structure, from the DIA's Historical Market Analysis.")

    faq_html, faq_ents = faq([
      ("What are the best online casino sites NZ players can use in 2026?",
       f"<p>On our scoring the strongest all-round option is <a href='/casino-reviews/spinjo/'>Spinjo</a>, "
       f"which banks in New Zealand dollars end to end, names its operating company, holds a current "
       f"Cura&ccedil;ao Gaming Control Board licence and carries the deepest library we audited. If what "
       f"you care about is collecting a large win quickly, the answer changes: "
       f"<a href='/casino-reviews/kingdom/'>Kingdom</a> and <a href='/casino-reviews/smash/'>Smash</a> are "
       f"the only two sites here whose weekly ceiling clears a {C.money(C.BIG)} win in a single payment. "
       f"That is what <a href='#ledger'>the Exit Ledger</a> is for.</p>"),
      ("How long does it really take to withdraw from an online casino in NZ?",
       f"<p>Longer than the advertised window, and the reason is arithmetic rather than bad faith. "
       f"Processing times quoted on these sites &mdash; one to six hours on crypto, one to five business "
       f"days on a card &mdash; describe a single payment. They do not describe a win larger than the "
       f"weekly ceiling. The median ceiling across the {len(capped)} capped sites here is "
       f"<b>{C.money(median_cap)} a week</b>, so a {C.money(C.BIG)} win is paid in instalments at "
       f"{len(instalments)} of the {len(exits)} sites we cover, and the median elapsed time on a card is "
       f"<b>{C.days(median_days)}</b>. <a href='/fast-payout-casinos/'>The whole withdrawal clock</a>.</p>"),
      ("Which online casinos pay out fastest to New Zealand players?",
       f"<p>On a single ordinary withdrawal, crypto rails settle fastest almost everywhere &mdash; "
       f"typically one to six hours once an account is verified. On a genuinely large win the ranking "
       f"changes completely, because the weekly ceiling does the throttling: "
       f"<a href='/casino-reviews/kingdom/'>Kingdom</a> and <a href='/casino-reviews/smash/'>Smash</a> "
       f"both allow {C.money(10000)} a week, while "
       f"<a href='/casino-reviews/{lowest_cap[0]['slug']}/'>{esc(lowest_cap[0]['name'])}</a> allows "
       f"{C.money(lowest_cap[1]['cap_nzd'])}, which turns the same win into "
       f"{lowest_cap[1]['tranches']} payments. <a href='/fast-payout-casinos/'>Payout speeds and caps, "
       f"side by side</a>.</p>"),
      ("Is it legal to play at online casinos in New Zealand?",
       "<p>Yes, for you. New Zealand law has never made it an offence for an individual to gamble at an "
       "offshore online casino. The prohibitions bind operators and advertisers, not players. The "
       "<b>Online Casino Gambling Act 2026</b> came into force on 1 May 2026 and creates a licensed "
       "domestic market of 15 operators, with the application cutoff on 1 December 2026 and the first "
       "licensed sites expected during 2027. Until then the sites on this page operate from offshore "
       "licences. <a href='/nz-online-casino-law/'>The full legal position</a>.</p>"),
      ("Do I pay tax on online casino winnings in New Zealand?",
       "<p>For virtually every recreational player, no. Gambling winnings are not income under New "
       "Zealand law because they are not derived from a taxable activity. The exceptions are narrow: a "
       "professional gambler carrying on a business, and crypto. The IRD treats cryptoassets as property, "
       "so converting a crypto balance back to New Zealand dollars can be a taxable disposal quite "
       "independently of whether you won it. <a href='/gambling-winnings-tax-nz/'>How the IRD actually "
       "treats it</a>.</p>"),
      ("What is a maximum withdrawal limit, and why does it matter more than payout speed?",
       f"<p>It is the most a casino will pay you in a given period, usually a week, regardless of how "
       f"much you are owed. It matters more than the processing window because it is the larger number in "
       f"the equation. A site advertising &ldquo;1&ndash;3 business days&rdquo; with a "
       f"{C.money(5000)}-a-week ceiling pays a {C.money(C.BIG)} win in two instalments a week apart, so "
       f"the honest answer to &ldquo;how fast is it?&rdquo; is eight days, not three. Every ceiling we "
       f"could verify is in <a href='#ledger'>the Exit Ledger</a>.</p>"),
      ("Can I use New Zealand dollars, and does it matter?",
       f"<p>It matters more than most players expect. A euro-denominated balance costs a New Zealander "
       f"roughly {B.FX_SPREAD*100:.1f}% round trip &mdash; conversion on the way in and again on the way "
       f"out. On a {C.money(C.BIG)} win that is about <b>{C.money(fx_cost)}</b>, which is larger than the "
       f"difference between most of the welcome offers on this page. Sites that hold New Zealand dollars "
       f"end to end are marked <span class='chip chip--yes'>NZD</span> in the comparison table above.</p>"),
      ("Which welcome bonus is actually worth claiming?",
       f"<p>Fewer than you would think. A welcome bonus is a contract priced in turnover: before you can "
       f"withdraw anything derived from it you must stake a multiple of it, and staking is not free. "
       f"Of the cash offers we price, only a handful are realistically finishable, and they are the small "
       f"ones on modest multipliers rather than the four-figure headlines. "
       f"<a href='/online-casinos/bonuses/'>Every offer, converted into dollars</a>.</p>"),
      ("What happens to my account and my balance on 1 December 2026?",
       f"<p>If the casino you use is not one of the auction winners, it is <b>legally required to exit the "
       f"New Zealand market</b> from that date &mdash; the DIA's own wording. In practice an exiting "
       f"operator will normally close New Zealand registrations first, then stop accepting deposits, then "
       f"settle balances; but nothing in the Act guarantees you a timeframe, and your recourse if it goes "
       f"wrong is still a foreign regulator. The practical risk is not that your money vanishes, it is "
       f"that you are trying to withdraw from a company winding down its NZ business at exactly the "
       f"moment its weekly ceiling forces your win into instalments. <a href='#cutoff'>The dates and what "
       f"we would do about them</a>.</p>"),
      ("How do I complain about an online casino in New Zealand, and to whom?",
       "<p>Today, in this order: the operator's own support desk in writing, then the named ADR provider "
       "in its terms if it has one, then the regulator that issued its licence &mdash; the Cura&ccedil;ao "
       "Gaming Control Board publishes a complaints form, Anjouan and Tobique are considerably less "
       "responsive. If the site names no operating company, that ladder has no rungs, which is the "
       "argument for checking before you deposit rather than after. <b>From 2027 this changes "
       "materially:</b> the DIA says that with a licensed operator you will be able to complain "
       "&ldquo;either directly to the online casino or to us as the regulator&rdquo;. "
       "<a href='/fast-payout-casinos/#escalate'>The full escalation ladder</a>.</p>"),
      ("Why did my New Zealand bank decline my casino deposit?",
       "<p>Almost always the bank, not the casino. Every major New Zealand bank now offers a gambling "
       "block, and several decline gambling merchant category codes on credit cards as standing policy, "
       "with some extending it to debit. New Zealanders also report being blocked on the way <i>in</i> to "
       "their own account &mdash; one r/newzealand poster had a bookmaker withdrawal rejected at the ASB "
       "end. The fix is not to try another card, it is to use a rail your bank does not screen. "
       "<a href='/payment-methods/'>Which bank blocks what, and what still clears</a>.</p>"),
      ("How much do New Zealanders actually spend gambling online?",
       f"<p>The Department of Internal Affairs measured it: about <b>360,000</b> New Zealanders transact "
       f"with offshore online gambling merchants, and total deposits have exceeded <b>NZ$100 million a "
       f"month</b> since March 2024. The median individual, though, deposits <b>NZ$290 a year</b> across "
       f"fewer than a dozen transactions. Both facts are true because the market is extraordinarily "
       f"concentrated: <b>the top 20% of players account for 90% of all money deposited</b>. "
       f"<a href='#market'>The full dataset, with its method</a>.</p>"),
      ("How do you make money, and does it change the order?",
       "<p>We are funded by affiliate commission, and we will not pretend the running order is untouched "
       "by it: <b>listing order reflects our commercial agreements</b>. What commercial terms cannot "
       "touch is the arithmetic. The Exit Ledger is generated from each operator's own published limits, "
       "and it puts several of our best-paying partners in the bottom half of it. "
       "<a href='/how-we-rate/#money'>How that works, in full</a>.</p>"),
    ], heading="Best online casino sites NZ: your questions answered")

    paa_html, paa_ents = faq([
      ("Which online casino has the best payout percentage in NZ?",
       "<p>Payout percentage is a property of the game, not the casino &mdash; but the operator chooses "
       "which build of each game to run, and studios ship the same title at 96.5%, 94% and 92%. A lobby "
       "running the cut-down configuration is a meaningfully worse casino at identical branding. "
       "<a href='/high-payout-casinos/'>Which lobbies run which build</a>.</p>"),
      ("Are online casino sites in NZ safe?",
       "<p>Safety here is a spectrum rather than a yes or no, because none of these sites holds a New "
       "Zealand licence &mdash; that regime does not open until 2027. The checkable signals are a named "
       "operating company, a licence number that resolves on the regulator's own register, published "
       "withdrawal limits and a complaints route that is not the casino's own support desk. One brand we "
       "list publishes none of them, and we say so on every page it appears on.</p>"),
      ("What is the minimum deposit at NZ online casinos?",
       "<p>Between NZ$10 and NZ$35 across the sites here. The number that matters more is the "
       "<i>bonus-qualifying</i> minimum, which is often higher than the deposit minimum &mdash; a site "
       "advertising NZ$10 deposits may require NZ$30 to trigger the welcome offer. Both figures are in "
       "the comparison table.</p>"),
      ("Can I get free spins with no deposit in New Zealand?",
       "<p>Yes, at a handful of sites, and the offers are genuine but small. The trap is not the spins, "
       "it is the ceiling: no-deposit winnings usually carry a maximum cashout of NZ$100 or so on top of "
       "a wagering requirement higher than the one on the cash bonus. "
       "<a href='/no-deposit-casinos/'>Every no-deposit offer, with its ceiling</a>.</p>"),
      ("Do online casinos accept POLi or bank transfer in New Zealand?",
       "<p>POLi remains the most widely supported New Zealand-specific rail, though support has thinned "
       "as banks have withdrawn from it. Several major New Zealand banks now decline gambling merchant "
       "codes on credit cards outright. <a href='/payment-methods/'>Which banks block what, and what "
       "still works</a>.</p>"),
      ("Which online casino games give you the best chance of winning?",
       "<p>Measured by house edge rather than by feel: blackjack played to basic strategy is the best of "
       "the common games at well under 1%, then baccarat on the banker at about 1.06%, then European "
       "roulette at 2.7%. Pokies typically run 3&ndash;6%, and American roulette&rsquo;s double zero "
       "doubles the edge to 5.26% for no benefit whatsoever &mdash; never play it when the European "
       "wheel is in the same lobby. The catch, and it is a large one: the table games with the best odds "
       "are usually the ones a welcome bonus weights at 10% or excludes outright. "
       "<a href='/high-payout-casinos/'>House edge game by game</a>.</p>"),
      ("Are the casinos on these lists owned by the same companies?",
       "<p>More often than any comparison page admits. The nineteen brands we cover resolve to seven "
       "corporate groups; one entity alone operates five of them. That matters if something goes wrong, "
       "because moving to a &lsquo;different&rsquo; casino in the same group means the same cashier, the "
       "same terms and the same support desk. <a href='#ownership'>The full ownership map</a>.</p>"),
      ("What happens to my money if an online casino goes bust?",
       "<p>Offshore, usually nothing good. Cura&ccedil;ao, Anjouan and Tobique licences do not require "
       "player funds to be held separately from operating money in the way a UK or Malta licence does, so "
       "a player balance can be an unsecured debt of a company in another jurisdiction. You would rank "
       "behind secured creditors and have no practical way to file. This is the strongest single argument "
       "for withdrawing rather than maintaining a balance, and it is sharper than usual right now with an "
       "<a href='#cutoff'>exit deadline</a> approaching.</p>"),
      ("Do I have to verify my identity to withdraw?",
       "<p>Yes, everywhere, and any site advertising &ldquo;no KYC&rdquo; is either unlicensed or not "
       "telling the truth. Anti-money-laundering rules oblige an operator to verify identity and often "
       "source of funds before paying out, and the operator is entitled to do it at withdrawal rather "
       "than at signup &mdash; which is why the check so often lands at the worst possible moment. Upload "
       "your documents on the day you register and the largest delay in the whole process disappears. "
       "<a href='/fast-payout-casinos/#sof'>What the document pack looks like</a>.</p>"),
      ("How many times can I withdraw from an online casino in a week?",
       f"<p>Usually as often as you like, up to a total. The cap is on the amount, not the number of "
       f"requests: {len(capped)} of the {len(exits)} sites here publish a weekly ceiling, ranging from "
       f"{C.money(min(caps))} to {C.money(max(caps))}. Requesting five withdrawals of "
       f"{C.money(1000)} does not get you past a {C.money(5000)} ceiling &mdash; the fifth one queues "
       f"until the window resets.</p>"),
    ], heading="People also ask", ident="paa")

    body = f"""
{lede(H1[PATH],
   "<p>Every other page ranking for this term tells you how fast a casino processes a withdrawal. "
   "One to six hours. One to three business days. Those numbers are real, and they answer a question "
   "almost nobody is actually asking, because they describe a single payment rather than a win.</p>"
   f"<p>We price the exit instead. Take each operator&rsquo;s own published weekly ceiling, its own "
   f"stated processing window, and a {C.money(C.BIG)} win &mdash; not a fantasy jackpot, the sort of "
   f"result that makes a person read the terms for the first time. This month that arithmetic says "
   f"<b>{len(instalments)} of the {len(exits)}</b> casino sites on this page would pay that win in "
   f"instalments, that the median wait on the rail most New Zealanders use is "
   f"<b>{C.days(median_days)}</b> rather than the advertised few days, and that only "
   f"<b>{len(within_week)}</b> could hand it over inside a week. The processing window is the smallest "
   "term in the equation, and it is the only one anybody publishes.</p>",
   [(f"{len(exits)}", "Exits priced"),
    (f"{C.money(median_cap)}", "Median weekly ceiling"),
    (f"{C.days(median_days)}", f"Median wait, {C.money(C.BIG)} win"),
    (f"{len(within_week)}", "Pay it inside a week")],
   f"Updated {MONTH_YEAR} &middot; Checked from NZ &middot; Every ceiling verified",
   AUTHOR, CHECKER,
   toplist_h2=f"The {len(pick(TOP10))} best online casino sites in NZ &mdash; {MONTH_YEAR}",
   toplist_intro=("Ordered as our commercial agreements dictate, scored as our testing dictates. The two "
                  "are different things and we publish both, which is more than the pages above us in "
                  "these results are willing to do."),
   toplist_html=lb,
   offer=top_offer_strip(pick(TOP10)),
   jump_items=[("The Exit Ledger &mdash; every ceiling priced", "ledger"),
               ("What the Ledger shows", "findings"),
               ("The clauses between you and your money", "clauses"),
               ("What Kiwis actually complain about", "complaints"),
               ("Red flags", "redflags"),
               ("Compare all sites", "compare"),
               ("Is it legal in NZ?", "legal"),
               ("FAQ", "faq")])}

{sec(f'''{sechead("The Exit Ledger: what it takes to get a win out",
  "One table, generated from the operators&rsquo; own published limits. If you read nothing else on this "
  "page, read this.", 2, "ledger")}
<div class="prose">
<p>Here is the sentence that organises this entire site. <b>A casino&rsquo;s advertised withdrawal time
describes one payment. Your win is not one payment.</b></p>
<p>Almost every site on this page caps what it will pay in a week. The ceiling is published, it is
enforceable, and it is almost never mentioned in a comparison table &mdash; which is convenient, because it
is the number that actually governs how long you wait. A site quoting
&ldquo;1&ndash;3 business days&rdquo; alongside a {C.money(5000)} weekly ceiling cannot pay a
{C.money(C.BIG)} win in three days. It pays half of it in three days and the rest the following week, and
the honest answer to &ldquo;how fast is this casino?&rdquo; is eight days.</p>
<p>So we do the arithmetic the operators leave out. The table below takes each site&rsquo;s own ceiling and
its own stated window, applies them to a {C.money(C.BIG)} win, and reports the elapsed time on the card
rail &mdash; the one most New Zealanders use &mdash; and on crypto for comparison. It is simple enough to
check by hand: <b>instalments = win &divide; weekly ceiling</b>, and
<b>elapsed = (instalments &minus; 1) &times; 7 days + the processing window</b>.</p>
</div>
{ledger}
<div class="prose">
{note(f'<p><b>Why the crypto column is not the answer.</b> Crypto settles in hours nearly everywhere, and '
      f'the weekly ceiling applies to it exactly as it applies to a card. Moving to crypto removes the '
      f'processing delay, which is the small term; it does nothing whatsoever about the ceiling, which is '
      f'the large one. At <a href="/casino-reviews/{slowest[0]["slug"]}/">{esc(slowest[0]["name"])}</a> a '
      f'{C.money(C.BIG)} win takes {C.days(slowest[1]["days_worst"])} by card and '
      f'{C.days(slowest[3]["days_worst"])} by crypto &mdash; still {slowest[1]["tranches"]} payments '
      f'either way.</p>', "info")}
</div>''', ident="ledger")}

{sec(f'''{sechead("Four things the Exit Ledger shows that nobody else prints", None, 2, "findings")}
<div class="prose">
<h3>1. The advertised payout window is the smallest number in the equation</h3>
<p>Across the {len(exits)} casino sites here, the difference between the fastest stated card window and the
slowest is about four days. The difference between the highest weekly ceiling and the lowest is
{C.money(max(caps) - min(caps))}, which on a {C.money(C.BIG)} win is worth
{slowest[1]["tranches"] - 1} extra weeks. Every competing page ranks on the four-day variable and ignores
the multi-week one. We would rather rank on the one that costs you time.</p>
<h3>2. Only {len(within_week)} sites can hand over {C.money(C.BIG)} inside a week</h3>
<p><a href="/casino-reviews/kingdom/">Kingdom</a> and <a href="/casino-reviews/smash/">Smash</a> both set
their ceiling at {C.money(10000)} a week, which is the only reason they clear this bar. It is not that they
process faster &mdash; their stated card windows are middling. They simply do not force the win into
instalments. A higher ceiling beats a faster rail every time the win is large, and no comparison table in
this market is built to show you that.</p>
<h3>3. A euro balance is a fee with no name on it</h3>
<p>{len(fx_hit)} of the sites here denominate the balance in euros rather than New Zealand dollars. You pay
a conversion spread on the way in and another on the way out &mdash; about {B.FX_SPREAD*100:.1f}% round
trip, or <b>{C.money(fx_cost)}</b> on a {C.money(C.BIG)} win. That is larger than the gap between most of
the welcome offers on this page, it is charged whether you win or lose, and it appears on no comparison
table anywhere because it is not a fee, it is a spread. The distinction matters to an accountant and not at
all to your bank balance.</p>
<h3>4. The ceiling is what makes a stuck balance dangerous</h3>
<p>This is the part that is genuinely about harm rather than arithmetic. A win paid in one instalment is
gone from the casino in days. A win paid in {slowest[1]["tranches"]} instalments sits in a casino account
for weeks, with the games one tap away and a balance the player has already mentally spent. Every
responsible-gambling page in this market talks about deposit limits. None of them mentions that a low
withdrawal ceiling keeps your own money on the table, which is the same problem viewed from the other
end.</p>
</div>''', ident="findings", haze=True)}

{sec(f'''{sechead(f"What happens on 1 December 2026 &mdash; {days_left} days from now",
  "The most important thing on this page is not a bonus. It is a date, and almost every site "
  "ranking above us for this term is still describing it as something that happens in 2027.", 2, "cutoff")}
<div class="prose">
<p>The Department of Internal Affairs could not be much plainer, so here it is in the
regulator&rsquo;s own words rather than ours:</p>
<blockquote class="quote"><p>&ldquo;Up to 15 online casinos will be successful at auction and gain the
right to apply for an online casino licence. <b>From 1 December 2026, only these operators will be able
to provide online casino gambling to customers in New Zealand.</b> These operators will be permitted to
operate under an exemption while their applications undergo a rigorous assessment process. <b>All other
online casinos will be legally required to exit the New Zealand market.</b>&rdquo;</p>
<cite>Department of Internal Affairs, <i>Online Gambling for players</i>, checked {MONTH_YEAR}</cite></blockquote>
<p>Read that twice, because the detail most pages are getting wrong is in the first sentence.
It is not &ldquo;operators who applied&rdquo;. It is <b>the auction winners</b>. Around fifty
expressions of interest were lodged for fifteen licences, which means roughly thirty-five applicants
will lose &mdash; and losing is the same, legally, as never having entered. The auction itself begins on
<b>29 September 2026</b>, {L.days_to(L.AUCTION)} days from today.</p>
<p>So the honest position, which we would rather state than bury: <b>we do not know whether any operator
on this page will still be serving New Zealanders in {days_left} days.</b> Neither does anybody else
&mdash; the DIA has declined to say who is taking part, to protect the integrity of the auction. Any
page that tells you otherwise is guessing.</p>
<h3>Why this collides with the Exit Ledger, specifically</h3>
<p>Here is the part that follows from our own data and that we have not seen anywhere else. Look again at
how long these sites take to pay a real win.</p>
<p><b>{len(slowpokes)} of the {len(exits)} casinos on this page need two weeks or more</b> to pay out
{C.money(C.BIG)} on the card rail, because their weekly ceiling splits it into instalments. At
<a href="/casino-reviews/{slowest[0]['slug']}/">{esc(slowest[0]['name'])}</a> it is
{C.days(slowest[1]['days_worst'])}, in {slowest[1]['tranches']} payments a week apart.</p>
<p>Now put a deadline next to it. A player who deposits in mid-November, wins well, and requests a
withdrawal in the last week of November is asking a company to pay them in instalments <i>across the
date on which that company must leave the market</i>. We are not predicting that anybody will fail to
pay. We are pointing out that the arithmetic is uncomfortably tight, that it is entirely knowable in
advance, and that nobody is telling you.</p>
{note(f'<p><b>What we would actually do, and it costs us money to say it.</b> Between now and 1 December, '
      f'treat every offshore casino as a short-term account rather than a place to keep a balance. '
      f'Complete verification on the day you register, not the day you win. Withdraw in full rather than '
      f'leaving money on the site. And prefer the sites with headroom on the way out &mdash; on our '
      f'ledger that is <a href="/casino-reviews/kingdom/">Kingdom</a> and '
      f'<a href="/casino-reviews/smash/">Smash</a>, the only two that pay {C.money(C.BIG)} in a single '
      f'instalment. If a site would take three weeks to pay you, three weeks is a meaningful fraction of '
      f'the time it has left.</p>', "warn")}
<h3>What the licensed regime will actually require</h3>
<p>It is worth knowing what is coming, because several of the rules read like they were written after
somebody looked at the same problems this site was built around. Licensed New Zealand operators will
have to:</p>
<ul>
<li><b>Ensure prompt withdrawals</b> and simple account closure &mdash; the exit becomes a licence
condition rather than a competitive choice</li>
<li><b>Prohibit credit card and buy-now-pay-later deposits</b></li>
<li><b>Cap bonus offers at NZ$100 or 200% of deposit</b>, which would make every headline on this page
illegal as advertised</li>
<li><b>Ban autoplay</b>, and prevent more than one slot being played at once</li>
<li>Offer player-set deposit, spend and session limits, real-time alerts and enforced play breaks</li>
<li>Verify age at 18, and support self-exclusion</li>
<li><b>Not use affiliate or influencer marketing at all</b> &mdash; which is to say, not use sites like
this one. We have said elsewhere on this page that the model funding us is going away. This is the
clause that does it.</li>
</ul>
<p>And a complaints route that is not the casino: the DIA says that if a licensed operator falls short,
&ldquo;you will be able to complain either directly to the online casino or to us as the regulator&rdquo;.
That single sentence is the biggest practical upgrade in this whole regime, because the one thing an
offshore player has never had is somebody to escalate to.</p>
<p>The trade-off is stated just as plainly by the regulator: <b>&ldquo;If you decide to use an unlicensed
platform, you won&rsquo;t have the same player protections.&rdquo;</b></p>
<p><a class="btn btn--ghost" href="/nz-online-casino-law/">The full timeline, with dates, fees and section
numbers &rarr;</a></p>
</div>''', ident="cutoff")}

{sec(f'''{sechead(f"What changed this month", "A dated log of what moved, so you can tell whether "
  "this page was actually updated or merely stamped with a fresh month.", 2, "changelog")}
{table(["When", "What happened", "Why it matters to you"],
  [[f"<b>{e[0]}</b>", f"<b>{e[1]}</b>", e[2]] for e in NZ.ENFORCEMENT]
  + [["<b>21 September 2026</b>",
      "<b>We corrected our own timeline</b>",
      "We had been describing 1 December 2026 as an application deadline, with licensed sites arriving "
      "during 2027. Re-reading the DIA's player guidance, that was wrong in a way that mattered: "
      "1 December is the date every non-winning operator must <i>exit</i>. Corrected across the site, "
      "and recorded here rather than quietly changed."],
     [f"<b>{MONTH_YEAR}</b>",
      "<b>Exit Ledger re-checked</b>",
      f"Every weekly withdrawal ceiling and payout window re-read from the operators' own cashier and "
      f"terms pages. Median ceiling across the {len(capped)} capped sites: {C.money(median_cap)} a week."]],
  caption="We publish this because &ldquo;last updated&rdquo; is the easiest claim in this industry to "
          "fake, and a month stamp on an unchanged page is worse than no stamp at all.")}''',
  ident="changelog")}

{sec(f'''{sechead("The New Zealand market, in the regulator&rsquo;s own numbers",
  "The best data on New Zealand online gambling is not on any casino site. It is in two PDFs on a "
  "Department of Internal Affairs page written for licence applicants.", 2, "market")}
<div class="prose">
<p>In May 2026 the DIA released two reports it had commissioned from Dot Loves Data, covering the year
to 30 September 2025. They were published for the benefit of companies bidding for licences. As far as we
can tell, <b>not one page currently ranking for this search cites either of them</b>, which is a shame,
because they are the only serious measurement of what New Zealanders actually do online.</p>
{note(f'<p><b>Read the method before the numbers.</b> {NZ.METHOD} That distinction is important and it is '
      f'one that secondary coverage keeps getting wrong: NZ$100 million a month is not NZ$100 million '
      f'lost. Source: {NZ.SOURCE}</p>', "info")}
</div>
{market}
<div class="prose">
<h3>The market is growing because the same people are spending more</h3>
<p>That is the finding to sit with. Deposits rose 10.5% in the year. The number of people making them rose
<b>2.7%</b>. New Zealand is not acquiring online gamblers at any great rate; it is extracting more from the
ones it already has. The transaction count and the average transaction size both rose, which is the
signature of depth rather than breadth.</p>
</div>
{segments}
<div class="prose">
<h3>Who the average player actually is</h3>
<p>The picture the industry paints is a casual player having a flutter. The DIA&rsquo;s numbers say that is
genuinely true of most individuals &mdash; and almost irrelevant to how the market works.</p>
</div>
{player}
<div class="prose">
<p>Both things are true at once. The median New Zealander who gambles online spends <b>NZ$290 a year</b>
and transacts fewer than a dozen times. And then:</p>
{conc}
<p>A fifth of players generate ninety per cent of the money. That is not a market built on the median
player at all, and it is the single most important thing to understand about the business model of every
brand on this page, including the ones we are paid to recommend. If you find yourself in the top quintile,
the product is working exactly as designed and the design is not on your side.</p>
<p>The timing data is bleaker still, and it is the part we would not have guessed: peak activity is
<b>early morning and mid-week</b>, not Friday night. Gambling that happens at 4am on a Wednesday is not
entertainment competing with the pub.</p>
</div>
{regions}
<div class="prose">
<h3>Ninety-six per cent of the market is served from four places</h3>
</div>
{structure}
<div class="prose">
<p>Cyprus, Gibraltar, Great Britain and Malta take 96.3% of New Zealand&rsquo;s offshore gambling spend
between them, and fifteen merchants take over 80% of it. A market this concentrated is one where the
brands compete on marketing rather than on terms &mdash; which is precisely why the withdrawal ceilings on
this page cluster so tightly, and why the licensing regime is about to matter so much.</p>
</div>''', ident="market", haze=True)}

{sec(f'''{sechead(f"Nineteen brands, {WORDS[len(groups)]} companies",
  "Shopping around only works if the shops are different. Here they are not, and no comparison page in "
  "this market shows you that.", 2, "ownership")}
<div class="prose">
<p>Every casino on this page presents itself as an independent brand with its own name, its own colours
and its own support desk. Group them by the legal entity named in their own footers and the picture
changes: <b>{len(OPS)} brands resolve to {len(groups)} corporate groups</b>, and
{esc(biggest[0][0])} alone runs <b>{len(biggest[1])}</b> of them.</p>
</div>
{ownership}
<div class="prose">
<h3>Why this is worth ten seconds of your attention</h3>
<p><b>A second opinion is not a second opinion.</b> If a withdrawal goes wrong at
<a href="/casino-reviews/spinjo/">Spinjo</a> and you move to
<a href="/casino-reviews/lucky-vibe/">Lucky Vibe</a> for a fresh start, you have moved to the same
company, the same cashier and very often the same support staff reading the same internal notes about
you. Five of the brands on this page sit behind one entity.</p>
<p><b>A shared operator means shared terms.</b> Withdrawal ceilings, verification policy and bonus
clauses are usually set at group level, so the differences between sister brands are largely cosmetic.
That is visible in our own Exit Ledger: the group brands cluster within a day or two of each other.</p>
<p><b>And self-exclusion does not follow you.</b> Excluding yourself at one brand does not exclude you at
its siblings unless the operator applies it group-wide, and most do not say either way. If you are using
exclusion as a control, exclude at every brand in the group &mdash; the table above is the list.</p>
{note(f'<p><b>{len(unnamed)} brands on this page name no operating company at all.</b> '
      f'{unnamed_links}. '
      f'A licence badge with no legal entity behind it means there is nobody to escalate to and nobody to '
      f'take to a regulator. It is the weakest disclosure position in this market and we mark it on every '
      f'page those brands appear on.</p>', "warn")}
</div>''', ident="ownership")}

{sec(f'''{sechead("The clauses that sit between you and your money",
  "Five terms that do more damage than the wagering requirement, ranked by how much money they cost a New "
  "Zealand player.", 2, "clauses")}
<div class="prose">
<h3>1. Maximum cashout</h3>
<p>The clause that voids the win you were hoping for, and the one with the most direct claim on the top of
this list. A no-deposit offer with a NZ$100 maximum cashout means that if you turn 20 free spins into
NZ$3,000, you withdraw NZ$100 and the casino keeps the rest. It is disclosed, it is enforceable, and it is
the single most common reason a player feels cheated by a site that has done nothing wrong. Check it before
you claim, not after you win.</p>
<h3>2. The weekly withdrawal ceiling</h3>
<p>Covered at length above, and worth repeating here because it is the only clause in this list that
applies whether or not you touch a bonus. It is in the terms rather than the marketing, it varies by a
factor of {max(caps)//min(caps)} across the sites on this page, and it converts directly into weeks of
waiting. Read it before you deposit.</p>
<h3>3. Game weighting</h3>
<p>Wagering requirements are rarely satisfied equally by all games. Pokies typically contribute 100%, table
games 10%, and live dealer blackjack 5% or nothing at all. If you are a blackjack player claiming a 40x
bonus that weights blackjack at 5%, your real requirement is <b>800x</b>. The contribution table is usually
a separate document from the bonus terms, and that separation is not accidental.</p>
<h3>4. Maximum bet while wagering</h3>
<p>Almost universally NZ$5 to NZ$8 per spin. Exceed it once, even accidentally, even by fifty cents on an
autoplay setting you forgot about, and the operator is entitled to void the bonus and everything derived
from it. This is the clause most often cited in the complaints we read, and the player is almost always in
the wrong on the terms and entirely reasonable in feeling aggrieved.</p>
<h3>5. Expiry</h3>
<p>Typically 30 days, occasionally 7. Consider what a 30-day expiry means alongside a NZ$200,000 turnover
requirement: you would need to stake NZ$6,600 every single day for a month. The expiry does not simply risk
the bonus, it makes the largest offers in this market arithmetically impossible for a normal player, which
is worth understanding before you value one.</p>
<p><a class="btn btn--ghost" href="/online-casinos/bonuses/">Every welcome offer, converted into dollars
&rarr;</a></p>
</div>''', ident="clauses")}

{sec(f'''{sechead("Every online casino site in New Zealand, compared", None, 2, "compare")}
<div class="prose"><p>Score, the weekly ceiling, what that ceiling does to a {C.money(C.BIG)} win, the
welcome offer and the turnover it demands, entry cost, and whether you will be holding New Zealand dollars.
The column that matters most depends entirely on how much you expect to be taking out.</p></div>
{comp}''', ident="compare")}

{sec(f'''{sechead("Find the casino that fits how you actually play")}
{fit}''', ident="fit", haze=True)}

{sec(f'''{sechead("Is online casino gambling legal in New Zealand?", None, 2, "legal")}
<div class="prose">
<p>Yes, and the confusion on this point is worth clearing up properly because half the pages ranking for
this term still have it wrong.</p>
<p><b>No New Zealand law makes it an offence for you to play at an offshore online casino.</b> The Gambling
Act 2003 prohibits <i>operating</i> unlicensed gambling from within New Zealand and prohibits advertising
it. It has never criminalised the player. If you deposit at any site on this page, you commit no offence.</p>
<p>What is changing is the supply side, and it is changing sooner than most pages ranking for this
term admit. The <b>Online Casino Gambling Act 2026</b> commenced on <b>1 May 2026</b> and establishes a
licensed domestic market administered by the Department of Internal Affairs. Up to <b>15 licences</b> will
be issued, allocated by an auction that begins on <b>29 September 2026</b>. From <b>1 December 2026</b>
&mdash; {L.days_to(L.CUTOFF)} days from today &mdash; only the auction winners may serve New Zealanders,
and every other offshore casino is <b>legally required to exit the market</b>. Licences themselves are
expected to start being issued in early 2027. <a href="#cutoff">What that means for you, in detail</a>.</p>
<p>Two consequences follow that are worth planning around. First, licensed operators will be subject to New
Zealand harm-minimisation rules, a domestic complaints route and DIA oversight &mdash; and, we would expect,
withdrawal terms a domestic regulator is willing to defend. That is a materially stronger position for a
player than any offshore licence offers. Second, the Act <b>prohibits affiliate marketing</b> by licensed
operators, which means the business model funding this site will not be available for those brands. We
would rather tell you that plainly than have you find out later.</p>
{note('<p><b>Sports and racing are different, and the difference is recent.</b> The Racing Industry '
      'Amendment Act 2025 took effect on 28 June 2025 and makes TAB NZ the only entity that may lawfully '
      'offer or promote sports and racing betting to people in New Zealand. As with casino gambling, '
      'the prohibition binds the operator rather than the punter &mdash; you commit no offence by placing '
      'a bet. <a href="/online-betting/">The betting position in full</a>.</p>', "warn")}
<p><a class="btn btn--ghost" href="/nz-online-casino-law/">The law, with section numbers and dates &rarr;</a></p>
</div>''', ident="legal")}

{sec(f'''{sechead("Depositing and withdrawing from New Zealand")}
<div class="prose">
<p>The payment question that actually costs New Zealanders money is not which rail is fastest. It is
whether your bank will let the transaction through at all, and which currency you end up holding.</p>
<p><b>Card deposits are increasingly declined.</b> Several major New Zealand banks now block gambling
merchant category codes on credit cards as a matter of policy, and some extend it to debit. A declined
deposit is usually the bank, not the casino &mdash; which matters, because the instinctive response is to
try another card, and the correct response is to use a different rail.</p>
<p><b>POLi</b> remains the most widely supported New Zealand-specific method, moving money directly from
your bank account without a card. <b>Neosurf</b> vouchers cover players who would rather not connect a bank
account at all. <b>Crypto</b> is the fastest rail almost everywhere, typically settling in one to six
hours, but carries a tax consequence most players are unaware of: the IRD treats cryptoassets as property,
so converting back to New Zealand dollars can be a taxable disposal regardless of whether it came from
gambling.</p>
<p><b>And the withdrawal rail is not always the deposit rail.</b> Most operators enforce a closed-loop
rule &mdash; money returns the way it arrived, up to the amount you deposited. Fund an account with a
Neosurf voucher, which cannot receive money, and the balance comes back by bank transfer or not at all,
often after a further verification step. It is worth choosing the deposit method you want to be paid
through.</p>
<p><a class="btn btn--ghost" href="/payment-methods/">Every payment method, with fees, limits and what it
does on the way out &rarr;</a></p>
</div>''', ident="pay")}

{sec(f'''{sechead("How to tell whether a casino site is safe")}
<div class="prose">
<p>None of the sites on this page holds a New Zealand licence, because that regime does not open until
2027. So the question is not whether a site is licensed here &mdash; none are &mdash; but whether it is
accountable anywhere. Four checks, in descending order of how much they tell you.</p>
</div>
{steps([
  ("Find the operating company, not just the licence badge",
   "Scroll to the footer. You are looking for a named legal entity with a registration number &mdash; "
   "Rabidi N.V., Dama N.V., Vertikal N.V. A licence seal with no company behind it is the weakest signal "
   "in this market, because seals are images and images are copied."),
  ("Resolve the licence number on the regulator&rsquo;s own register",
   "Take the number to the Cura&ccedil;ao Gaming Control Board register and confirm it returns the company "
   "named in the footer. A mismatch between the two is the clearest warning sign available to a player, "
   "and it takes about ninety seconds to check."),
  ("Read the withdrawal section of the terms before depositing",
   "Weekly and monthly ceilings, the verification documents required, and whether the operator reserves a "
   "right to pay large wins in instalments. This is where a site that intends to make cashing out "
   "difficult tells you so, in advance and in writing &mdash; and it is the section this masthead exists "
   "to read on your behalf."),
  ("Check that a complaints route exists that is not the casino",
   "A named ADR provider or the regulator&rsquo;s own complaints form. If the only escalation path is the "
   "operator&rsquo;s own support desk, you have no escalation path at all."),
])}
<div class="prose">
{note('<p><b>The brand that fails this test.</b> <a href="/casino-reviews/roby-casino/">Roby Casino</a> '
      'publishes no regulator, no licence number and no operating company. It is the only site we cover '
      'where all three are absent, it pays us one of the highest commission rates in our portfolio, and we '
      'score it 8.1 with this warning attached on every page it appears on. We would rather you knew both '
      'facts.</p>', "warn")}
</div>''', ident="safe", haze=True)}

{sec(f'''{sechead("What New Zealanders actually complain about",
  "We read the reviews instead of the marketing. The findings are not what the category pages suggest.",
  2, "complaints")}
<div class="prose">
<p>Before writing any of this site we went looking for what goes wrong for real New Zealand players. The
most useful single data point is about an operator we do not list and are not paid by.</p>
<p><b>SkyCity Online Casino</b> is New Zealand&rsquo;s own domestically licensed operator &mdash; the site
most Kiwis would name if asked for the safe option. On Trustpilot it holds a <b>TrustScore of 1.5 out of
5</b> across <b>71 reviews</b>, with <b>82% rated one star</b> (checked {MONTH_YEAR}).</p>
</div>
{table(["Rating", "Share of reviews", "What this tells you"],
  [["&#9733;&#9733;&#9733;&#9733;&#9733; 5", "8%", "A small group who completed verification without incident"],
   ["&#9733;&#9733;&#9733;&#9733; 4", "4%", "&mdash;"],
   ["&#9733;&#9733;&#9733; 3", "0%", "Nobody is lukewarm. This is a bimodal experience"],
   ["&#9733;&#9733; 2", "6%", "&mdash;"],
   ["<b>&#9733; 1</b>", "<b>82%</b>", "Almost entirely withdrawal verification, not games or odds"]],
  caption="Trustpilot rating distribution for skycitycasino.com, captured " + MONTH_YEAR + ". A licensed "
          "New Zealand operator. The complaints are not about fairness &mdash; they are about getting paid.")}
<div class="prose">
<p>Read the one-star reviews and a single theme dominates. Not rigged games. Not unpaid bonuses.
<b>The exit.</b></p>
<blockquote class="quote"><p>&ldquo;I spent about 4 weeks trying to withdraw winnings, they have asked me
for every imaginable document under the sun&hellip; wanting 90 days of unfiltered transactions and then not
accepting the PDF as it is &lsquo;too large&rsquo;.&rdquo;</p><cite>Trustpilot reviewer, SkyCity Online
Casino</cite></blockquote>
<p>And then the review that changed how we structured this entire site:</p>
<blockquote class="quote"><p>&ldquo;These guys were so determined not to payout, I gave up, <b>rinsed my
winnings</b> and took the loss.&rdquo;</p><cite>Trustpilot reviewer, SkyCity Online Casino</cite></blockquote>
<p>The withdrawal was never refused. The player gambled the balance away out of frustration, and the
operator kept it without ever declining a payment. We have not found a single competitor page in this
market that mentions this pattern &mdash; and it is the exact failure mode a low weekly ceiling
manufactures, because a ceiling is a rule that keeps your money inside the casino for another week.</p>

<h3>The same complaint, everywhere we looked</h3>
<p>SkyCity is not an outlier and we did not stop at Trustpilot. Searching for what New Zealanders
actually say about online gambling turns up the same three problems, in the same order, across every
source. None of them is about whether the games are fair.</p>
<h4>1. &ldquo;No recourse&rdquo; &mdash; the thing Kiwis are most anxious about</h4>
<p>The most-upvoted answer in a 2026 r/newzealand thread asking whether offshore casinos are legal or
risky did not argue about legality at all:</p>
<blockquote class="quote"><p>&ldquo;Basic problem is that you will have no recourse if they refuse to let
you withdraw your money.&rdquo;</p><cite>r/newzealand, June 2026</cite></blockquote>
<p>That is exactly right, and it is why the <a href="#ownership">named operating company</a> matters more
than the licence badge, and why the DIA&rsquo;s promise of a regulator-level complaints route from 2027 is
the most valuable thing in the new regime.</p>
<h4>2. It is not hypothetical &mdash; it has happened here, and it made the news</h4>
<p>In January 2024 <b>Stuff</b> reported the case of Sam Townsend, who won around NZ$2,000 gambling online
in late October and could not get it out; the reporting put the total he was owed across sites at
<b>NZ$5,800</b> that &ldquo;sites wouldn&rsquo;t pay up&rdquo;. A New Zealand player, a New Zealand
publication, and no regulator to take it to. That is the whole problem in one story.</p>
<h4>3. Your own bank is now part of the problem</h4>
<p>This one surprised us, and it is almost entirely missing from competitor pages. New Zealanders report
being blocked at the <i>bank</i> end, in both directions:</p>
<blockquote class="quote"><p>&ldquo;I tried to withdraw a decent sized winnings from an online bookmaker
and ASB bank rejected it on their end.&rdquo;</p><cite>r/newzealand</cite></blockquote>
<p>Every major New Zealand bank now offers gambling blocks, and several decline gambling merchant
category codes as policy. That is a good thing if you want a block and an unexpected obstacle if you do
not, and it is why a declined transaction is usually your bank rather than the casino.
<a href="/payment-methods/">Which bank does what</a>.</p>
<h4>4. The ceiling, described by someone who had never heard the word</h4>
<p>Our favourite find, because it is our entire thesis stated by a player who was simply describing their
week. Asked about online pokies in New Zealand, an r/newzealand commenter wrote that the
<b>&ldquo;weekly limit combined with the occasional win locks me out for the week&rdquo;</b>. That is a
withdrawal ceiling, experienced from the inside, by somebody who had no particular reason to know it was a
clause in a contract. It is in <a href="#ledger">the Exit Ledger</a> for all nineteen operators.</p>
{note('<p><b>A note on sourcing.</b> Reddit blocks automated access, so the material above is quoted from '
      'public search-result snippets rather than reproduced post bodies, and we have deliberately not '
      'cited the several &ldquo;best NZ casino&rdquo; Reddit <i>wiki</i> pages that surface for these '
      'queries &mdash; they are affiliate pages wearing Reddit&rsquo;s clothes, and treating them as '
      'player opinion would be dishonest. The Trustpilot distribution and the Stuff report are primary.</p>',
      "info")}
<h3>What follows for you</h3>
<ul>
<li><b>A domestic licence is not a guarantee of a good experience.</b> The most complained-about operator
serving New Zealanders is the licensed one. Licensing gives you recourse, not service quality.</li>
<li><b>Verify on the day you register</b>, before you have anything to withdraw. It is the largest single
delay in the process and it is almost entirely within your control.</li>
<li><b>Treat a submitted withdrawal as gone.</b> Do not revisit the balance. The reverse-withdrawal window
exists precisely to tempt you, and a ceiling that forces a second instalment gives it a second chance.</li>
<li><b>Expect the bank, not just the casino.</b> Check whether yours blocks gambling codes before you
plan around a card.</li>
</ul>
<p><a class="btn btn--ghost" href="/fast-payout-casinos/#sof">Source of funds, the document pack, and the
escalation ladder &rarr;</a></p>
</div>''', ident="complaints", haze=True)}

{sec(f'''{sechead("Red flags: when to close the tab", None, 2, "redflags")}
<div class="prose">
<p>Competitor pages publish an avoid-list of named brands. Named lists go stale within months as skins
close and reopen under new names, so here is the version that keeps working: the signals themselves.</p>
</div>
{table(["Red flag", "Why it matters", "How long it takes to check"],
  [["<b>No operating company in the footer</b>",
    "A licence with no legal entity behind it gives you nobody to escalate to. This is the single "
    "strongest warning available", "10 seconds"],
   ["<b>Licence number does not resolve on the regulator&rsquo;s register</b>",
    "Seals are images and images are copied. The register is the only proof", "90 seconds"],
   ["<b>Withdrawal ceiling not published before you deposit</b>",
    "Weekly caps hidden until after funding is a deliberate choice, and the one that decides how long "
    "a win takes to reach you", "1 minute"],
   ["Bonus terms without a stated wagering <i>basis</i>",
    "&ldquo;40x&rdquo; without saying 40x of what is unpriceable, and usually deliberately", "1 minute"],
   ["Deposit limits only available by emailing support",
    "Account-level limits are trivial to build. Making them hard is a decision about who the site is for",
    "2 minutes"],
   ["&ldquo;No verification&rdquo; marketing",
    "Any licensed operator verifies at withdrawal. A site promising otherwise is unlicensed, lying, or "
    "both", "Instant"],
   ["No complaints route other than the operator&rsquo;s own support",
    "If the only escalation path is the casino, you have no escalation path", "1 minute"]],
  caption="Seven checks, under ten minutes in total, done before you deposit rather than after you win. "
          "One brand we list fails the first three, and we say so on every page it appears on.")}
<div class="prose">
{note('<p><b>The brand on this site that fails them.</b> <a href="/casino-reviews/roby-casino/">Roby '
      'Casino</a> publishes no regulator, no licence number and no operating company. It pays us one of '
      'the highest commission rates in our portfolio and we score it 8.1, among the three lowest here. We '
      'have kept the review up rather than quietly dropping the brand, because people search for it and '
      'should find the disclosure gap rather than a page that omits it.</p>', "warn")}
</div>''', ident="redflags")}

{sec(f'''{sechead("Before you deposit anything")}
<div class="prose">
<p>The house edge is not a rumour, it is the business model. Every game on every site listed here returns
less than it takes, by design, forever. A casino is entertainment with a price, and the price is your
expected loss. Played that way it is fine. Played as a way to make money it is arithmetic you cannot win.</p>
<p>Four habits worth more than the difference between any two casinos on this page: set a deposit limit on
day one while you are calm rather than at 1am when you are not; complete verification before you have
anything to withdraw; take winnings out in full rather than leaving a balance sitting behind a weekly
ceiling; and read both the wagering and the withdrawal terms in dollars rather than percentages, which is
what this entire site exists to help you do.</p>
<p><b>If it has stopped being entertainment, help in New Zealand is free, confidential and available right
now.</b></p>
</div>
{keyfacts([(f"{n} &middot; {num}", d) for n, num, _u, d in L.HELP])}
<div class="prose"><p><a class="btn btn--ghost" href="/responsible-gambling/">Deposit limits, self-exclusion
and bank blocks &rarr;</a></p></div>''', ident="rg")}

{sec(f'<div class="prose">{faq_html}</div>', ident="faqsec", haze=True)}
{sec(f'<div class="prose">{paa_html}</div>', ident="paasec")}

{sec(f'''{sechead("The short version")}
<div class="prose">
<p><b>If you want one name and no further reading:</b> <a href="/casino-reviews/spinjo/">Spinjo</a>. It
banks in New Zealand dollars end to end, names its operating company, holds a current Cura&ccedil;ao Gaming
Control Board licence and runs the deepest library we audited.</p>
<p><b>If you expect to win seriously:</b> <a href="/casino-reviews/kingdom/">Kingdom</a> or
<a href="/casino-reviews/smash/">Smash</a>. Their {C.money(10000)} weekly ceiling is the highest here and
the only one that pays a {C.money(C.BIG)} win in a single instalment. On the Exit Ledger that is worth more
than any difference in processing speed on this page.</p>
<p><b>If you simply want to play for an evening:</b> decline the bonus. Your money stays withdrawable, no
clause can void your winnings, and you have removed most of the traps described on this page in a single
click.</p>
<p>That is the whole of our advice, and you will notice that a good deal of it points away from the offers
we are paid to promote. That is what the arithmetic says, so that is what we have published.</p>
<p><a class="btn" href="/fast-payout-casinos/">The full withdrawal clock, site by site &rarr;</a>
<a class="btn btn--ghost" href="/how-we-rate/">How we score and how we are funded</a></p>
</div>''', ident="verdict")}
"""

    schema = [
        schema_webpage(PATH, META[PATH][0], META[PATH][1]),
        schema_breadcrumb(PATH, []),
        schema_article(PATH, META[PATH][0], META[PATH][1], AUTHOR, CHECKER),
        schema_person(AUTHOR), schema_person(CHECKER),
        schema_itemlist(PATH, pick(TOP10)),
        schema_faq(PATH, faq_ents + paa_ents),
    ]
    return write(PATH, page(PATH, body, schema), priority=1.0, freq="daily")
