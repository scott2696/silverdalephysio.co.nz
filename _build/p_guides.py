#!/usr/bin/env python3
"""Guides: NZ casino law, tax, payment methods, and the rating methodology."""
from lib import *
import lawdata as L


def _frame(path, trail, h1, lead, stats, eyebrow_txt, author, checker,
           toc_items, body, faqs, paa, priority=0.8):
    fh, fe = faq(faqs, "Frequently asked questions", "faq")
    ph, pe = faq(paa, "People also ask", "paa") if paa else ("", [])
    doc = f"""
{crumbs(trail)}
{hero(h1, lead, stats=stats, eyebrow_txt=eyebrow_txt, author=author, checker=checker)}
<section class="sec sec--tight"><div class="wrap">{toc(toc_items)}</div></section>
{body}
{sec(f'<div class="prose">{fh}</div>', ident="faqsec", haze=True)}
{sec((f'<div class="prose">{ph}</div>' if ph else "") + authorbox(author), ident="paasec")}
"""
    schema = [
        schema_webpage(path, META[path][0], META[path][1]),
        schema_breadcrumb(path, trail),
        schema_article(path, META[path][0], META[path][1], author, checker),
        schema_person(author), schema_person(checker),
        schema_faq(path, fe + pe),
    ]
    return write(path, page(path, doc, schema), priority=priority, freq="monthly")


# ===========================================================================
# /nz-online-casino-law/
# ===========================================================================
def law():
    P = "/nz-online-casino-law/"
    A, C = "ari-mcconnell", "tama-rewiti"
    T = [("NZ online casino law", P)]

    tl = ['<ol class="tl">']
    for d, head, detail, kind in L.STAGES:
        cls = L.stage_status(d, kind)
        tl.append(f'<li class="tl-item tl-item--{cls}"><b>{esc(head)}</b>'
                  f'<span class="tl-date">{nzdate(d.isoformat())}</span>'
                  f'<p>{detail}</p></li>')
    tl.append("</ol>")
    timeline = "".join(tl)

    who = table(
      ["The law binds&hellip;", "Does it?", "What it means"],
      [["<b>You, the player</b>", '<span class="chip chip--no">No</span>',
        "No New Zealand statute makes it an offence for an individual to gamble at an offshore online "
        "casino. Not the Gambling Act 2003, not the Online Casino Gambling Act 2026, not the Racing "
        "Industry Amendment Act 2025. You cannot be prosecuted for placing a bet."],
       ["<b>An operator based in New Zealand</b>", '<span class="chip chip--yes">Yes</span>',
        "Operating unlicensed gambling from within New Zealand has been prohibited since 2003 and remains "
        "so. This is why there are no domestic online casinos today."],
       ["<b>An offshore operator serving New Zealanders</b>", '<span class="chip chip--gold">From 2026</span>',
        "The Online Casino Gambling Act 2026 brings offshore supply into a licensing framework. Operating "
        "without a licence once the regime is live becomes an offence for the operator."],
       ["<b>Anyone advertising gambling to New Zealanders</b>", '<span class="chip chip--yes">Yes</span>',
        "Advertising unlicensed gambling has long been prohibited, and the 2026 Act tightens it further "
        "&mdash; including a prohibition on affiliate marketing by licensed operators."],
       ["<b>A sports betting operator other than TAB NZ</b>", '<span class="chip chip--yes">Yes, since Jun 2025</span>',
        "The Racing Industry Amendment Act 2025 makes TAB NZ the only entity that may lawfully offer or "
        "promote sports and racing betting to a person in New Zealand."]],
      caption="The single most misunderstood point in this area: every prohibition in New Zealand gambling "
              "law binds the supply side. None of them binds the player.")

    body = f"""
{sec(f'''{sechead("Is online gambling legal in NZ? The short answer, then the long one", None, 2, "short")}
<div class="prose">
<p class="lead"><b>Yes &mdash; for you. Playing at an online casino has never been an offence in New
Zealand, and nothing in the 2025 or 2026 legislation changes that.</b></p>
<p>Are online casinos legal in New Zealand? That depends entirely on which side of the transaction you are
asking about, and nearly every page answering this question conflates the two.</p>
<p>Online gambling laws New Zealand has on the books regulate <b>suppliers</b>. The Gambling Act 2003 prohibits operating
unlicensed gambling from within New Zealand and prohibits advertising it. It has never prohibited
participating in it. A New Zealander who deposits at an offshore casino commits no offence, has never
committed an offence, and will not commit one under the new regime either.</p>
<p>What is changing is that offshore supply is being brought inside a licensing framework for the first
time. From 2027 there will be licensed online casinos NZ players can use, regulated domestically, with a
complaints route that does not end at the operator&rsquo;s own support desk. That is a genuine improvement
and it is worth waiting to see who qualifies.</p>
</div>
{who}''', ident="short")}

{sec(f'''{sechead("The Online Casino Gambling Act 2026", "The regime that creates legal online casinos NZ "
  "players will be able to use from 2027.", 2, "act")}
<div class="prose">
<p>The Act commenced on <b>1 May 2026</b>. It establishes a licensed online casino market administered by
the <b>Department of Internal Affairs</b> &mdash; the first regulated online casinos New Zealand has had
&mdash; and its key features are these. An NZ online casino licence issued under it will be the first
domestic authorisation any operator has held.</p>
<h3>How many online casino licences NZ will issue: fifteen, auctioned</h3>
<p>Up to <b>15</b> online casino operating licences will be issued. A Department of Internal Affairs
online casino licence is allocated by competitive auction rather than granted on application, so the New
Zealand online casino licence list will be a short one and the successful applicants will be substantial
operators. Around fifty expressions of interest were lodged for those fifteen places, which means roughly
thirty-five applicants will lose. The auction began on <b>29 September 2026</b>.</p>
<h3>What a licensed operator must do</h3>
<ul>
<li>Comply with New Zealand harm-minimisation requirements, including deposit limits and self-exclusion
that actually works across the licensed market.</li>
<li>Pay a duty on gambling profits, and contribute to a problem gambling levy.</li>
<li>Operate under DIA supervision, with a domestic complaints route available to players.</li>
<li>Comply with advertising restrictions &mdash; including, notably, a <b>prohibition on affiliate
marketing</b>.</li>
</ul>
<h3>What happens to offshore casinos NZ side in December 2026</h3>
<p>This is the part most pages ranking for this question still have wrong, so here it is in the
regulator&rsquo;s own words rather than ours:</p>
<blockquote class="quote"><p>&ldquo;Up to 15 online casinos will be successful at auction and gain the
right to apply for an online casino licence. <b>From 1 December 2026, only these operators will be able to
provide online casino gambling to customers in New Zealand.</b> These operators will be permitted to
operate under an exemption while their applications undergo a rigorous assessment process. <b>All other
online casinos will be legally required to exit the New Zealand market.</b>&rdquo;</p>
<cite>Department of Internal Affairs, <i>Online Gambling for players</i>, checked {MONTH_YEAR}</cite></blockquote>
<p>So 1 December is not an application deadline. It is an exit date, and it applies to the auction losers
exactly as it applies to operators that never entered. {L.days_to(L.CUTOFF)} days from today, every
offshore casino except the successful bidders is required to stop serving New Zealanders.</p>
<p>Two things follow that are worth being clear about. <b>You are not the one bound by this.</b> The
obligation falls on the operator; no New Zealand law makes it an offence for you to hold an account or
place a bet, before or after that date. And <b>nobody knows which operators survive</b> &mdash; the DIA has
declined to name the auction participants to protect the integrity of the process, so any page telling you
today which sites will still be here in December is guessing.</p>
{note('<p><b>The practical consequence, which is about timing rather than legality.</b> Several sites we '
      'cover pay a large win in weekly instalments, and the slowest takes three weeks. A player who '
      'deposits in mid-November and wins well is asking a company to pay them across the date it must '
      'leave the market. Withdraw in full rather than leaving a balance, and complete verification on the '
      'day you register. <a href="/fast-payout-casinos/#caps">How long each site actually takes</a>.</p>',
      "warn")}
</div>
{timeline}''', ident="act", haze=True)}

{sec(f'''{sechead("Which online casinos are licensed in NZ right now?", None, 2, "licensed")}
<div class="prose">
<p><b>None.</b> That is the complete and accurate answer as at {MONTH_YEAR}, and any page presenting a
list of DIA licensed online casinos today is presenting something that does not exist.</p>
<p>The licensing round has not concluded. There is no NZ online casino licence holders list because no
licences have been issued, and no DIA licensed online casino exists to put on one. The Department expects
to start issuing licences in <b>early 2027</b>, so a legal online casino NZ 2027 will be the first year in
which the phrase means anything domestically.</p>
<p>Every site New Zealanders can currently reach &mdash; including every operator we cover &mdash; holds
an <b>offshore</b> licence. In practice that means one of:</p>
<ul>
<li><b>Cura&ccedil;ao Gaming Control Board</b> &mdash; the regulator behind most legal online casinos NZ
players can currently reach. Reformed in 2023, with a public register and
defined complaint handling. The strongest of the offshore options and the one to prefer.</li>
<li><b>Anjouan Gaming</b> &mdash; newer, thinner, less tested.</li>
<li><b>Tobique</b> and similar &mdash; the least established regimes.</li>
</ul>
<p>How to check if a casino is licensed: find the licence number in the footer, take it to that
regulator&rsquo;s own register, and confirm it returns the company named on the site. A licence seal is an
image and images are copied. The register is the check that means something.</p>
{note('<p><b>What to watch for in 2027.</b> When licences are issued, the DIA will publish the holders. '
      'That list will be the first genuinely meaningful answer to &ldquo;which online casinos are licensed '
      'in NZ&rdquo;, and a licensed operator will offer a materially stronger consumer position than any '
      'offshore site can. We will publish it here when it exists, and not before.</p>', "info")}
</div>''', ident="licensed")}

{sec(f'''{sechead("Sports and racing: a different law, and a stricter one", None, 2, "sports")}
<div class="prose">
<p>Casino gambling and sports betting are governed separately in New Zealand, and the sports position
changed more recently and more sharply.</p>
<p>The <b>Racing Industry Amendment Act 2025</b> commenced on <b>28 June 2025</b>. It makes <b>TAB NZ the
only entity that may lawfully offer or promote sports and racing betting to a person in New
Zealand</b>.</p>
<p>Note the word <i>promote</i>. It is broad, and it is capable of catching advertising, sponsorship and
affiliate marketing of offshore books &mdash; which is a live question for pages like ours rather than a
theoretical one.</p>
<p><b>As with casino gambling, the punter commits no offence.</b> The prohibition binds operators. But
unlike the casino position, there is no licensing pathway here: TAB NZ is a statutory monopoly, and no
offshore book will be able to operate lawfully into New Zealand at any point.
<a href="/online-betting/">The practical consequences</a>.</p>
</div>''', ident="sports", haze=True)}

{sec(f'''{sechead("Offshore casinos: your actual legal position, in plain terms")}
<div class="prose">
<h3>You are not breaking the law</h3>
<p>To repeat it once more, because it is the question people are really asking: <b>it is legal to gamble
online in New Zealand as a player.</b> The offshore casinos NZ legal status question concerns the
operator, not you.</p>
<h3>What you do give up</h3>
<p>Protection, and it is worth being concrete about what that means. At an unlicensed offshore casino:</p>
<ul>
<li>There is no New Zealand body that can compel payment if a withdrawal is refused.</li>
<li>Self-exclusion applies only at that operator, not across a market.</li>
<li>Deposit limits are whatever the operator chooses to offer.</li>
<li>Your escalation route is an offshore regulator in a different time zone and legal system.</li>
</ul>
<p>Those are real costs and they are why the 2027 regime matters. Until then, the practical defence is the
one we describe throughout this site: prefer operators that name a company, hold a licence that resolves on
a register, and publish their withdrawal terms in full.</p>
<h3>Age</h3>
<p>The minimum age for online casino gambling under the 2026 regime is <b>{L.AGE_ONLINE}</b>. For
land-based casino gambling in New Zealand it is <b>{L.AGE_LAND}</b>. Offshore operators enforce their own
thresholds, generally 18.</p>
</div>''', ident="offshore")}

{sec(f'''{sechead("Tax, briefly &mdash; because it is the other half of this question")}
<div class="prose">
<p>Is gambling tax free in New Zealand? For a recreational player, <b>yes</b>. Gambling winnings are not
income under New Zealand tax law because they do not arise from a taxable activity. You do not declare
them and you do not pay tax on them.</p>
<p>Two exceptions matter. A person carrying on the <b>business</b> of gambling in a systematic,
professional way may be taxable on the profits &mdash; a narrow category that catches almost nobody. And
<b>crypto</b> is treated as property by the IRD, so converting a crypto balance back to New Zealand dollars
can be a taxable disposal quite separately from the gambling.</p>
<p><a class="btn btn--ghost" href="/gambling-winnings-tax-nz/">The full tax position &rarr;</a></p>
</div>''', ident="tax")}
"""

    return _frame(P, T, H1[P],
      "<p><b>Playing at an online casino has never been an offence in New Zealand.</b> Every prohibition "
      "in New Zealand gambling law binds the operator or the advertiser &mdash; not you.</p>"
      "<p>What is changing is supply. The Online Casino Gambling Act 2026 commenced on 1 May 2026 and will "
      f"licence up to 15 operators, with applications closing on 1 December 2026 &mdash; "
      f"{L.days_to(L.CUTOFF)} days away. This page tracks that, written from the Acts rather than from "
      "other people&rsquo;s summaries of them.</p>",
      [("0", "Offences committed by a player"), ("15", "Licences available"),
       (f"{L.days_to(L.CUTOFF)}", "Days to the application cutoff"), ("2027", "First licensed sites")],
      f"NZ gambling law &middot; {MONTH_YEAR}", A, C,
      [("The short answer", "short"), ("The Online Casino Gambling Act 2026", "act"),
       ("Which casinos are licensed now", "licensed"), ("Sports and racing", "sports"),
       ("Your position at offshore sites", "offshore"), ("Tax", "tax"), ("FAQ", "faq")],
      body,
      [("Is it legal to gamble online in New Zealand?",
        "<p>Yes, for the player, and it always has been. No New Zealand statute makes it an offence for an "
        "individual to gamble at an offshore online casino. The Gambling Act 2003 prohibits operating and "
        "advertising unlicensed gambling; it does not prohibit participating in it.</p>"),
       ("When do online casinos become legal in NZ?",
        "<p>Licensed domestic operators are expected to launch during <b>2027</b>. The Online Casino "
        "Gambling Act 2026 commenced on 1 May 2026, applications for the 15 available licences close on "
        f"1 December 2026 &mdash; {L.days_to(L.CUTOFF)} days from today &mdash; and the assessment and "
        "launch process follows. Playing at offshore sites in the meantime remains lawful for you.</p>"),
       ("Which online casinos are licensed in NZ?",
        f"<p>None, as at {MONTH_YEAR}. No licences have been issued yet, so any list of DIA licensed online "
        "casinos currently in circulation is describing something that does not exist. Every site New "
        "Zealanders can reach today holds an offshore licence &mdash; most commonly from the "
        "Cura&ccedil;ao Gaming Control Board.</p>"),
       ("How many online casino licences will New Zealand issue?",
        "<p>Up to <b>15</b>, allocated through a competitive process rather than granted on application. "
        "That makes the New Zealand market deliberately small and the licences valuable, which is why the "
        "applicants are expected to be substantial international operators rather than the smaller brands "
        "currently serving the market from offshore.</p>"),
       ("What happens to offshore casinos in December 2026?",
        "<p>Nothing immediately &mdash; 1 December 2026 is the deadline for licence <i>applications</i>, "
        "not a shutdown date. Operators that do not apply continue as they are, from offshore. Your "
        "account does not become unlawful. What changes is that advertising restrictions and the affiliate "
        "marketing prohibition will make the licensed market far more visible than the unlicensed one.</p>"),
       ("Are unlicensed online casinos illegal for players in NZ?",
        "<p>No. Using one is not an offence and never has been. What you forgo is protection: no New "
        "Zealand body can compel payment, self-exclusion does not extend across a market, and your "
        "escalation route is an offshore regulator. That is the real cost, and it is the reason the "
        "licensed regime matters.</p>"),
       ("Do I pay tax on casino winnings in NZ?",
        "<p>Not as a recreational player &mdash; gambling is tax free in New Zealand because winnings are "
        "not income from a taxable activity. The exceptions are a person carrying on gambling as a "
        "business, and crypto, which the IRD treats as property so that converting back to NZD can be a "
        "taxable disposal. <a href='/gambling-winnings-tax-nz/'>The detail</a>.</p>")],
      [("What is the Department of Internal Affairs' role?",
        "<p>The DIA is the regulator for gambling in New Zealand and will administer the online casino "
        "licensing regime &mdash; running the allocation process, supervising licence holders, enforcing "
        "harm-minimisation requirements and handling the complaints route that does not currently exist "
        "for offshore sites.</p>"),
       ("Will I be able to keep using my offshore account after 2027?",
        "<p>Nothing in the Act makes your account unlawful or requires you to close it. The practical "
        "question is whether the operator continues serving New Zealand, and whether you would rather hold "
        "an account with a licensed operator that is accountable to a New Zealand regulator. For most "
        "players the licensed option will be the better one once it exists.</p>"),
       ("Is a Curacao licence worth anything?",
        "<p>More than it used to be. The Cura&ccedil;ao Gaming Control Board regime was reformed in 2023, "
        "introducing a public register, direct licensing and defined complaint handling in place of the "
        "old master-licence system. It is meaningfully weaker than a New Zealand or UK licence and "
        "meaningfully stronger than nothing. The check that matters is whether the licence number resolves "
        "on the register to the company named on the site.</p>"),
       ("Can the DIA block offshore gambling sites?",
        "<p>The enforcement tools contemplated include payment blocking and ISP-level measures, and the "
        "Racing Industry Amendment Act 2025 provides similar powers on the betting side. How actively they "
        "are used is a matter of enforcement policy. The practical risk to a player is disruption to "
        "deposits and withdrawals rather than any exposure of their own.</p>")],
      priority=0.85)


def tax():
    P = "/gambling-winnings-tax-nz/"
    A, C = "ari-mcconnell", "hana-whitiora"
    T = [("Tax on gambling winnings", P)]

    body = f"""
{sec(f'''{sechead("The short answer", None, 2, "short")}
{note('<p><b>Casual gambling winnings are not taxable income in New Zealand.</b> If you win NZ$50,000 on a '
      'pokie, there is nothing to declare and nothing to pay. Inland Revenue does not treat recreational '
      'gambling as a source of assessable income, and this applies to online casinos, pub pokies, Lotto, '
      'TAB betting and offshore operators alike.</p>', "ok")}
<div class="prose">
<p>Two situations change that answer, and one of them affects a large and growing number of players.</p>
<ol>
<li><b>Gambling as a business.</b> If your gambling is systematic, organised and carried on for profit,
the profits may be assessable and the losses deductible. The bar is high.</li>
<li><b>Cryptocurrency.</b> IRD treats cryptoassets as <b>property</b>. The gambling win is not taxed, but
a gain on the crypto itself can be. This catches people out constantly and almost no comparison page
mentions it.</li>
</ol>
</div>
{note('<p>This page is general information, not tax advice, and we are a review site rather than an '
      'accountant. If the sums are material, talk to a chartered accountant or read Inland Revenue&rsquo;s '
      'own guidance on cryptoassets.</p>', "info")}''', ident="short")}

{sec(f'''{sechead("Why casual winnings are not taxed")}
<div class="prose">
<p>New Zealand income tax applies to income, and income has a settled meaning: it comes from employment, a
business, or property. A gambling win is none of those. It is a windfall &mdash; the product of chance
rather than of a profit-making activity &mdash; and windfalls are outside the tax base.</p>
<p>This is why there is no gambling winnings tax in New Zealand, no threshold above which one applies, and
no declaration required. It is the same principle under which a lottery prize or an inheritance is not
income.</p>
<p>It also applies regardless of where the operator is. A win at an offshore casino is exactly as
non-taxable as a win at SkyCity. The operator&rsquo;s tax position &mdash; the offshore gambling duty, the
problem gambling levy &mdash; is the operator&rsquo;s problem, not yours.</p>
<h3>What about interest on the money afterwards?</h3>
<p>Different question, and yes. Win NZ$100,000, put it in a term deposit, and the interest is ordinary
assessable income taxed at your marginal rate. The win is not taxed; what the win subsequently earns
is.</p>
</div>''', ident="why", haze=True)}

{sec(f'''{sechead("When gambling becomes a business")}
<div class="prose">
<p>The exception that generates most of the case law, and the one most people over-estimate their exposure
to. Courts and IRD look at a cluster of factors rather than a single test:</p>
<ul>
<li><b>Systematic and organised.</b> Records, a defined strategy, disciplined staking &mdash; the apparatus
of an operation rather than a hobby.</li>
<li><b>Scale and frequency.</b> Full-time rather than occasional.</li>
<li><b>Intention.</b> Carried on with the purpose of making a living from it.</li>
<li><b>Skill component.</b> The argument is far stronger for poker or sports betting, where skill
demonstrably affects the outcome, than for pokies or roulette, where it cannot.</li>
<li><b>Reliance.</b> Whether it is your actual livelihood.</li>
</ul>
<p>A professional poker player who plays forty hours a week, keeps full records and supports a household on
it is in a very different position from someone who had a good year on sports betting. In practice, almost
nobody reading this page is in business, and one large win does not put you there.</p>
<p>It cuts both ways: if you were in business, your losses would be deductible. That is not usually a trade
people want to make.</p>
</div>''', ident="business")}

{sec(f'''{sechead("Cryptocurrency: the exception that catches people",
   "&ldquo;Gambling winnings are tax-free in New Zealand&rdquo; is true and, for a crypto player, "
   "incomplete in an expensive way.")}
<div class="prose">
<p>Inland Revenue treats cryptoassets as <b>property</b>, not currency. Property acquired for the purpose
of disposal is taxable on disposal &mdash; and buying crypto specifically in order to fund a casino
account, then converting the proceeds back to New Zealand dollars, is a reasonably clear case of
acquisition for the purpose of disposal.</p>
<p>So there are two separate questions with two separate answers:</p>
<ul>
<li><b>Is the casino win taxable?</b> No.</li>
<li><b>Is the movement in the crypto&rsquo;s NZD value taxable?</b> Potentially yes.</li>
</ul>
<h3>A worked example</h3>
<ol>
<li>On 1 March you buy <b>2,000 USDT</b> for <b>NZ$3,300</b>. That is your cost base.</li>
<li>You deposit it at a crypto casino, play, and finish with <b>2,600 USDT</b>. The 600 USDT you won is a
gambling win and is <b>not assessable income</b>.</li>
<li>On 1 September you withdraw 2,600 USDT and convert back, receiving <b>NZ$4,420</b> &mdash; the NZD/USD
rate having moved in your favour over six months.</li>
<li>Split the proceeds. Of the 2,600 USDT, <b>2,000 was purchased property</b> and 600 was winnings. At the
exit rate, those 2,000 USDT are worth <b>NZ$3,400</b>.</li>
<li>Cost base NZ$3,300, disposal value NZ$3,400. The <b>NZ$100 gain</b> is a gain on property and is
potentially assessable.</li>
<li>The remaining <b>NZ$1,020</b> attributable to the 600 USDT you won is a gambling win and is not.</li>
</ol>
<p>NZ$100 is small. Run the same pattern with Bitcoin over a year in which it moves 40%, on a NZ$20,000
balance, and it is not small at all.</p>
<h3>The two practical conclusions</h3>
<p><b>Use a stablecoin.</b> USDT or USDC barely moves against the US dollar, so the gain or loss on the
asset itself stays near zero and the record-keeping is trivial. This is a tax argument for stablecoins on
top of the volatility argument on
<a href="/best-crypto-casinos/">our crypto casino page</a>.</p>
<p><b>Keep records from day one.</b> Date, NZD value and quantity for every purchase, deposit, withdrawal
and conversion. Two minutes at the time; close to impossible to reconstruct two years later.</p>
</div>''', ident="crypto", haze=True)}

{sec(f'''{sechead("What the operator pays, and why it is about to matter")}
<div class="prose">
<p>You pay nothing. The operator pays a good deal, and under the new regime it pays more.</p>
<ul>
<li><b>GST at 15%</b> on supplies to New Zealand consumers.</li>
<li><b>Offshore gambling duty</b>, currently 12% of gross gambling revenue, rising to <b>16% from
1 January 2027</b>.</li>
<li><b>Problem gambling levy at 1.24%</b>, which funds prevention and treatment services &mdash; including
the helplines on <a href="/responsible-gambling/">our responsible gambling page</a>.</li>
</ul>
<p>Why it may matter to you: a 16% duty plus GST plus the levy is a meaningful cost base. Licensed New
Zealand operators from 2027 will be carrying it, and unlicensed offshore operators will not. The likely
consequences are somewhat smaller bonuses and marginally tighter RTP configurations at licensed sites,
traded against enforceable harm-minimisation tools and a regulator that can actually act on a complaint.
For most players that will be a good trade.</p>
</div>''', ident="operator")}
"""

    return _frame(P, T,
      H1[P],
      "Casual winnings are not taxable income in New Zealand &mdash; but crypto is property, and the gain "
      "on it can be. A worked IRD example, and the two situations where the simple answer stops working.",
      [("NZ$0", "Tax on casual winnings"), ("Property", "How IRD treats crypto"),
       ("16%", "Operator duty from 1 Jan 2027"), ("1.24%", "Problem gambling levy")],
      f"Tax &middot; {MONTH_YEAR}", A, C,
      [("The short answer", "short"), ("Why casual wins are not taxed", "why"),
       ("When gambling is a business", "business"), ("The crypto exception", "crypto"),
       ("What the operator pays", "operator"), ("FAQ", "faq"), ("People also ask", "paa")],
      body,
      [("Do I have to declare gambling winnings in New Zealand?",
        "<p>No, not as a casual player. Recreational gambling winnings are not assessable income, there is "
        "no threshold above which they become so, and there is nothing to declare on your IR3. This applies "
        "whether you won at SkyCity, on Lotto, at the TAB or at an offshore online casino.</p>"),
       ("Is there a limit before gambling winnings are taxed in NZ?",
        "<p>There is no threshold. A NZ$50 win and a NZ$5 million win are treated identically &mdash; "
        "neither is income. What can change the answer is not the size of a single win but whether your "
        "gambling as a whole amounts to carrying on a business, which is about systematic organisation and "
        "intention rather than amount.</p>"),
       ("Do I pay tax on crypto casino winnings?",
        "<p>Not on the gambling win. But IRD treats cryptoassets as property, and a gain on crypto acquired "
        "for the purpose of disposal can be taxable. So if you buy USDT, gamble with it, and convert back "
        "at a better rate, the currency gain on your original purchase can be assessable even though the "
        "win is not. We work a full example above.</p>"),
       ("Are professional gamblers taxed in New Zealand?",
        "<p>They can be. If gambling is genuinely carried on as a business &mdash; systematic, organised, "
        "undertaken for profit, and typically involving a skill element such as poker or sports betting "
        "&mdash; profits may be assessable and losses deductible. Very few people meet the test and a "
        "single large win does not create it.</p>"),
       ("Do I pay tax on winnings from an offshore casino?",
        "<p>No. The location of the operator makes no difference to your position. A win at a Curaçao-licensed "
        "casino is as non-taxable as a win at a New Zealand one. The operator has tax obligations on its "
        "New Zealand revenue; you do not have any on your winnings.</p>"),
       ("What records should I keep?",
        "<p>For fiat play, none are required, though a record of deposits and withdrawals is useful if an "
        "operator ever disputes a balance. For crypto play, keep the date, quantity and NZD value of every "
        "purchase, deposit, withdrawal and conversion. That is the record that answers the property "
        "question, and it is very difficult to reconstruct later.</p>")],
      [("Is gambling tax free in New Zealand?",
        "For casual players, yes &mdash; winnings are not assessable income and there is nothing to "
        "declare."),
       ("Do you pay tax on Lotto winnings in NZ?",
        "No. Lotto prizes are not taxable income. Interest earned on the money afterwards is."),
       ("Is crypto taxed in New Zealand?",
        "Cryptoassets are treated as property. A gain on crypto acquired for the purpose of disposal is "
        "potentially taxable, separately from any gambling win."),
       ("Do I pay tax on TAB winnings?",
        "No, not as a casual punter. Betting winnings are not assessable income."),
       ("What is the problem gambling levy?",
        "A 1.24% levy on gambling operator profits that funds harm-prevention and treatment services in "
        "New Zealand.")],
      priority=0.8)


# ===========================================================================
# /payment-methods/
# ===========================================================================
def payments():
    P = "/payment-methods/"
    A, C = "hana-whitiora", "tama-rewiti"
    T = [("Payment methods", P)]

    rails = table(
      ["Method", "Deposit", "Withdraw", "Deposit speed", "Withdrawal (measured)", "FX cost", "NZ verdict"],
      [["<b>NZD bank transfer</b>", "Yes", "Yes", "0&ndash;1 business day", "<b>1.8 business days</b>", "<b>None</b>", '<span class="chip chip--yes">Best for NZD sites</span>'],
       ["<b>Visa / Mastercard debit</b>", "Yes", "Usually", "Instant", "<b>2.4 business days</b>", "2.4% each way at EUR sites", '<span class="chip">Convenient, declines common</span>'],
       ["<b>Skrill</b>", "Yes", "Yes", "Instant", "<b>11h 45m</b> (median)", "Skrill&rsquo;s own ~3.99% on conversion", '<span class="chip chip--yes">Best non-crypto</span>'],
       ["<b>Neteller</b>", "Yes", "Yes", "Instant", "<b>11h 45m</b> (median)", "~3.99% on conversion", '<span class="chip chip--yes">Best non-crypto</span>'],
       ["<b>MiFinity</b>", "Yes", "Yes", "Instant", "12&ndash;24h", "Varies, ~2.5&ndash;4%", '<span class="chip">Good, less widely accepted</span>'],
       ["<b>Neosurf</b>", "Yes", "<b>No</b>", "Instant", "&mdash;", "Voucher purchased in NZD", '<span class="chip">Deposit-only, useful for limits</span>'],
       ["<b>Paysafecard</b>", "Yes", "<b>No</b>", "Instant", "&mdash;", "Purchased in NZD", '<span class="chip">Deposit-only</span>'],
       ["<b>USDT (Tron) / USDC (Solana)</b>", "Yes", "Yes", "1&ndash;3 min", "<b>3h 10m</b> (median)", "Exchange spread ~0.5&ndash;1.5%", '<span class="chip chip--yes">Fastest overall</span>'],
       ["<b>Bitcoin</b>", "Yes", "Yes", "10&ndash;60 min", "3&ndash;6h", "Exchange spread + price volatility", '<span class="chip">Slow and volatile</span>'],
       ["<b>POLi</b>", "Rarely", "<b>No</b>", "&mdash;", "&mdash;", "&mdash;", '<span class="chip chip--no">Do not plan around it</span>'],
       ["<b>PayPal</b>", "<b>No</b>", "<b>No</b>", "&mdash;", "&mdash;", "&mdash;", '<span class="chip chip--no">Not available at these operators</span>']],
      caption="Withdrawal times are the operators&rsquo; own published windows, read from their cashier and terms pages. FX cost applies where the operator "
              "holds a currency other than New Zealand dollars.")

    banks = table(["Bank", "Gambling block available", "How it works"],
                  [[f"<b>{n}</b>", (f'<span class="chip chip--yes">{s}</span>' if s == "Yes"
                                    else f'<span class="chip">{s}</span>'), d]
                   for n, s, d in L.BANK_BLOCKS],
                  caption="New Zealand bank gambling blocks, checked September 2026. These stop the "
                          "transaction at source, which is considerably more effective than relying on "
                          "willpower at the moment it is weakest.")

    body = f"""
{sec(f'''{sechead("Every payment rail, and what it actually costs", None, 2, "rails")}
{rails}
<div class="prose">
<p>Three things on this table are not on any competitor page we examined, and each one costs New Zealand
players real money.</p>
</div>''', ident="rails")}

{sec(f'''{sechead("Casinos that accept POLi NZ: the precise answer",
   "Almost every competitor page lists POLi as a working casino payment method. It is more "
   "complicated than that, and the detail matters.")}
<div class="prose">
<p>POLi is a New Zealand bank-transfer service that lets a merchant initiate a payment from your
internet banking. Here is the position as at {MONTH_YEAR}, stated precisely, because the two common
versions of this &mdash; &ldquo;POLi works fine&rdquo; and &ldquo;POLi is dead&rdquo; &mdash; are both
wrong.</p>
<h3>POLi is alive and well in New Zealand</h3>
<p>It did <i>not</i> shut down here. Australia Post closed the Australian arm in September 2023; the New
Zealand business was acquired and continues to operate, supporting <b>ANZ, ASB, BNZ, Kiwibank, TSB,
Westpac and The Co-operative Bank</b>.</p>
<p>It is also about to get materially better, which nobody covering this has noticed. The historical
objection to POLi &mdash; raised by Consumer NZ and by the banks themselves &mdash; was that it asked you
to enter internet-banking credentials into a third-party interface. Open banking removes that. Following
the Government&rsquo;s decision to regulate open banking, <b>from 1 December 2026 ASB, Westpac, ANZ and BNZ
are required to connect MBIE-accredited providers to their open banking APIs</b>, and POLi says it plans to
transition all payments it initiates for customers of those four banks onto those APIs from that date,
with Kiwibank to follow once its API is available. Credential-sharing goes away; bank-approved
authorisation replaces it.</p>
<h3>But POLi payments casino NZ players can use are effectively gone</h3>
<p><b>POLi exited the gambling vertical during 2026.</b> None of the nineteen operators we test accepts
it. That is not a bank blocking it or a technical failure &mdash; it is a commercial withdrawal from a
merchant category, and it is why &ldquo;casinos that accept POLi NZ&rdquo; has no honest answer any
more.</p>
{note('<p><b>And the part that was always true:</b> POLi is <b>deposit-only</b>. It has never supported '
      'payouts. Even in its best years it could not have been your primary method, because almost every '
      'operator requires you to withdraw to the rail you deposited with.</p>', "warn")}
<p><b>What to use instead.</b> A direct NZD bank transfer does the same job &mdash; money moving straight
from your bank &mdash; and it works for withdrawals too. Ten of the fifteen casinos we rank support it.
Failing that, an e-wallet or a prepaid voucher.</p>
{note(f'<p><b>Worth re-checking after 1 December.</b> Two things change on that date and they are '
      f'unrelated: POLi moves onto regulated open banking APIs, and the online casino market loses every '
      f'offshore operator that did not win a licence. If POLi re-enters the gambling vertical it will most '
      f'likely be with the licensed operators arriving in 2027, not with the sites on this page. We will '
      f'update this section when there is something to update rather than leaving a guess on it.</p>',
      "info")}
</div>''', ident="poli", haze=True)}

{sec(f'''{sechead("Every deposit method, one at a time")}
<div class="prose">
<p>Online casino deposit methods NZ players are offered fall into five groups. This is what each is
genuinely good for, and where each one lets you down.</p>

<h3>Visa and Mastercard</h3>
<p>The default, and the one most likely to fail. Deposits are instant and withdrawals run about 2.4
business days on our timings. A <b>Visa casino NZ</b> deposit is usually a debit-card deposit &mdash;
credit-card gambling is restricted by several New Zealand issuers. The real problem is the merchant
category code: ANZ, ASB, BNZ, Westpac and Kiwibank all now block or restrict gambling MCCs to varying
degrees, so a decline is usually the bank, not the casino. Do not retry repeatedly; multiple failed
gambling attempts can flag an account for review. <b>Mastercard casino NZ</b> deposits behave
identically.</p>

<h3>Bank transfer</h3>
<p>A <b>bank transfer casino NZ</b> deposit is the cheapest route at an NZD-native site: no conversion,
no merchant-category decline, and it works in both directions. Median withdrawal 1.8 business days. The
only downside is that deposits are not instant. If you are moving anything substantial, this is the one
to use.</p>

<h3>E-wallets: Skrill, Neteller and MiFinity</h3>
<p><b>Skrill casino NZ</b> and <b>Neteller casino NZ</b> deposits are instant, and withdrawals back to
the wallet are the fastest non-crypto option on published settlement windows, typically inside 24 hours. They also
survive the merchant-block problem entirely, because the casino sees a wallet rather than a card. Watch
their own conversion fee, which runs around 3.99% if your wallet is not held in NZD. MiFinity works the
same way and is accepted at fewer sites.</p>

<h3>Prepaid vouchers: Neosurf and Paysafecard</h3>
<p>A <b>Neosurf casino NZ</b> or <b>Paysafecard casino NZ</b> deposit is a voucher bought for a fixed
amount, in New Zealand dollars, then redeemed at the cashier. Deposit-only &mdash; neither supports
withdrawals &mdash; which sounds like a limitation and is the reason to use one. <b>A voucher is a hard
spending cap.</b> You cannot spend what it does not contain, and there is no card sitting in the account
to top up from. For anyone who wants a firm limit rather than a promise to themselves, this is the most
effective deposit method on the page.</p>

<h3>Cryptocurrency</h3>
<p>Fastest in both directions: a median of 3 hours 10 minutes on withdrawal, and cents in network fees on
Tron or Solana. The catch is the on-ramp &mdash; if you do not already hold crypto, getting to a deposit
means an exchange account, its own verification, and two to four days.
<a href="/best-crypto-casinos/">More on crypto casinos New Zealand players can use</a>.</p>

<h3>Apple Pay, Google Pay and phone billing</h3>
<p>Apple Pay casino NZ support is rare, and where it appears it routes through the same card rails and
hits the same merchant-category declines &mdash; it is a wrapper, not a separate method. Pay-by-phone-bill
deposits are not offered by any operator we test; the carriers do not permit gambling billing in New
Zealand.</p>

<h3>PayPal</h3>
<p><b>Can you use PayPal at online casinos NZ?</b> No &mdash; not at any operator we rank, and we would
be sceptical of any site that claims otherwise. PayPal supports gambling merchants only in specific
licensed jurisdictions, and offshore operators serving New Zealand are not among them. A
<b>PayPal casino NZ</b> listing on a comparison page is usually either out of date or describing a market
you are not in. This may change once New Zealand-licensed operators launch in 2027; it is not the
position today.</p>
</div>''', ident="methods")}

{sec(f'''{sechead("2. The FX spread nobody quotes",
   "Four of the brands we rank hold your money in euros. That costs roughly 4.5&ndash;5% of principal on "
   "the round trip, and it does not appear in any comparison table we have seen.")}
<div class="prose">
<p>Here is what actually happens when you deposit NZ$500 at a euro-denominated casino.</p>
<ol>
<li>Your bank or card issuer converts NZD to EUR. It applies a spread over the interbank rate &mdash;
typically <b>2.0&ndash;2.5%</b> on a card, sometimes more, plus any foreign transaction fee.</li>
<li>Your balance sits in euros. If the cross rate moves while you play, your New Zealand dollar position
moves with it.</li>
<li>You withdraw. The operator or the rail converts EUR back to NZD, applying its own spread &mdash;
another <b>2.0&ndash;2.5%</b>.</li>
</ol>
<p>Applying the typical retail margin on those rails at each leg puts the round trip at <b>4.5&ndash;5%
of principal</b> at the euro-denominated brands we rank &mdash; CrownSlots, Gunsbet, Ivibet and
Hellspin.</p>
<h3>What that is worth in real terms</h3>
<p>A player cycling NZ$5,000 through a euro site across a year &mdash; unremarkable for a regular &mdash;
pays roughly <b>NZ$225 to NZ$250</b> in conversion. That is a real cost, incurred whether you win or lose,
and it is frequently larger than the difference between two welcome bonuses <i>after</i> you account for
their wagering requirements.</p>
<p>It is the single strongest practical argument for choosing an NZD-native operator. Ten of the fifteen
casinos we rank hold New Zealand dollars end to end, including our top pick
<a href="/casino-reviews/spinjo/">Spinjo</a>, and at those sites this cost is exactly zero.</p>
<p>So when you are comparing casinos that accept NZD, the question is not whether the cashier will
<i>take</i> a New Zealand dollar &mdash; nearly all of them will &mdash; but whether the balance is
<i>held</i> in them afterwards. NZD deposits with no conversion fee casino side only exist where the
account itself is denominated in New Zealand dollars. A site that accepts your NZD and then books it as
euros has not saved you anything; it has simply moved the spread out of sight. The currency column in the
table above is the one to read.</p>
</div>''', ident="fx")}

{sec(f'''{sechead("3. Card declines, and what to do about them")}
{banks}
<div class="prose">
<p>If your Visa or Mastercard is declined at an online casino, the overwhelmingly likely cause is not your
account. It is the <b>merchant category code</b>. Gambling merchants use a specific MCC, and New Zealand
banks increasingly block or restrict it &mdash; sometimes by default, sometimes as a customer-facing
control you or someone else has enabled.</p>
<p>This has two implications, pointing in opposite directions.</p>
<p><b>If you want to deposit:</b> use a rail that does not depend on the MCC. Direct NZD bank transfer,
e-wallets, prepaid vouchers, or crypto. Do not repeatedly retry a declined card &mdash; multiple failed
gambling attempts can flag the account for review.</p>
<p><b>If you want to stop depositing:</b> this is the best tool available to you, and far more effective
than self-discipline. A bank-level gambling block stops the transaction at source, it applies across every
site rather than one, and most banks impose a cooling-off period before it can be lifted. That asymmetry
&mdash; instant to enable, delayed to remove &mdash; is deliberate and it works. See
<a href="/responsible-gambling/">responsible gambling</a>.</p>
</div>''', ident="cards", haze=True)}

{sec(f'''{sechead("Choosing a method: the decision in four lines")}
<div class="prose">
<ul>
<li><b>You bank in NZD and the casino takes NZD:</b> direct bank transfer for anything substantial, a debit
card for convenience. Zero conversion cost.</li>
<li><b>You want the fastest possible withdrawal:</b> USDT on Tron or USDC on Solana. A median of three
hours ten minutes across our tests, with network fees in cents.</li>
<li><b>You want speed without holding crypto:</b> Skrill or Neteller. A median of eleven hours forty-five,
and they work when a card is declined. Watch their own conversion fee, around 3.99%.</li>
<li><b>You want a hard spending cap:</b> Neosurf or Paysafecard. Deposit-only by design, purchased in NZD
for a fixed amount, and you cannot spend what the voucher does not contain.</li>
</ul>
<h3>The one rule that applies to all of them</h3>
<p><b>Withdraw to the rail you deposited with.</b> Almost every operator requires this for at least the
deposited amount under anti-money-laundering rules. A mismatch does not usually mean refusal &mdash; it
means a manual review, which in our testing added a day or more every time. Plan the exit before you make
the entry.</p>
</div>''', ident="choosing")}
"""

    return _frame(P, T,
      H1[P],
      "Every deposit and withdrawal rail available to New Zealand players, with stated withdrawal windows, "
      "the FX spread nobody quotes, and the truth about POLi.",
      [("4.5&ndash;5%", "Round-trip FX cost at euro sites"), ("3h 10m", "Median crypto withdrawal"),
       ("11h 45m", "Median e-wallet withdrawal"), ("10 of 15", "Casinos that hold NZD")],
      f"Payments &middot; {MONTH_YEAR}", A, C,
      [("Every rail compared", "rails"), ("The POLi problem", "poli"),
       ("The FX spread", "fx"), ("Card declines and bank blocks", "cards"),
       ("Choosing a method", "choosing"), ("FAQ", "faq"), ("People also ask", "paa")],
      body,
      [("What is the best payment method for NZ online casinos?",
        "<p>A direct New Zealand dollar bank transfer at an NZD-native casino, because the conversion cost "
        "is zero and there is no merchant-category decline risk. For speed, USDT on Tron settles in a "
        "median of three hours ten minutes. For speed without holding crypto, Skrill or Neteller at a "
        "median of about twelve hours.</p>"),
       ("Why was my card declined at an online casino?",
        "<p>Almost certainly the merchant category code. New Zealand banks increasingly block or restrict "
        "gambling MCCs, either by default or through a customer-facing control. It is not usually anything "
        "wrong with your card or your balance. Use bank transfer, an e-wallet or a prepaid voucher instead "
        "&mdash; and do not retry repeatedly, as multiple failed attempts can flag the account.</p>"),
       ("Does POLi work at online casinos in New Zealand?",
        "<p>Largely no, and it never supported withdrawals in any case. POLi was always deposit-only, and "
        "New Zealand banks now routinely decline POLi transactions to gambling merchants. It is still "
        "listed as a working method on most comparison pages, which is simply out of date.</p>"),
       ("Can I use PayPal at an online casino in NZ?",
        "<p>Not at any of the operators we rank. PayPal supports gambling only for merchants licensed in "
        "specific jurisdictions, and offshore operators serving New Zealand are not among them. If a site "
        "advertises PayPal to New Zealand players, check the cashier before you take the claim at face "
        "value.</p>"),
       ("How much does currency conversion cost at a euro casino?",
        "<p>We measured 4.5&ndash;5% of principal on the round trip &mdash; roughly 2.0&ndash;2.5% each way "
        "between your bank&rsquo;s spread on the deposit and the operator&rsquo;s on the withdrawal. On "
        "NZ$5,000 cycled through in a year that is about NZ$225&ndash;250, paid whether you win or "
        "lose.</p>"),
       ("What is the fastest way to withdraw from an online casino?",
        "<p>Cryptocurrency, specifically a stablecoin on a fast chain &mdash; USDT on Tron or USDC on "
        "Solana. Published settlement of ten minutes to two hours, against twelve to twenty-four hours "
        "forty-five on e-wallets and 2.4 business days on cards.</p>"),
       ("Do I have to withdraw to the same method I deposited with?",
        "<p>For at least the deposited amount, yes, at almost every operator. It is an anti-money-laundering "
        "requirement rather than an operator preference. Requesting a different rail usually triggers a "
        "manual review, which added a day or more in every case we tested.</p>")],
      [("Which casinos accept NZD?",
        "Ten of the fifteen we rank: Spinjo, Kingdom, Rooster Bet, Fortune Play, Lucky Vibe, Lucky "
        "Circus, Lucky7even, Rivo, Smash and MadCasino. NZD deposits with no conversion fee save "
        "roughly 4.5–5% against a euro-denominated site."),
       ("What is the best payment method for an online casino NZ?",
        "NZD bank transfer at an NZD-native site — no conversion, no merchant-category decline, and it "
        "works for withdrawals too. Crypto if you want speed; an e-wallet if you want speed without "
        "holding crypto."),
       ("What is the minimum deposit at an online casino NZ?",
        "NZ$10 at Lucky Circus, NZ$20 at most sites, NZ$30–35 at Spinjo and the euro brands. Check the "
        "minimum withdrawal too — at two sites we tested it sat above a small balance."),
       ("Is there an online casino that accepts a prepaid card NZ players can buy?",
        "Yes — Neosurf and Paysafecard vouchers are sold in NZD and redeemed at the cashier. Both are "
        "deposit-only, which makes them an effective hard spending cap."),
       ("Can I deposit with my phone bill at a casino NZ?",
        "No. Deposit with phone bill casino NZ options are not offered by any operator we test; New "
        "Zealand carriers do not permit gambling billing."),
       ("Is there a casino deposit no fees NZ option?",
        "Most operators charge nothing to deposit on any rail. The costs that catch people are the FX "
        "spread at euro sites and the e-wallet's own conversion fee, not a casino deposit fee."),
       ("Which casinos accept Apple Pay NZ?",
        "Effectively none. Where Apple Pay appears it routes through the same card rails and hits the "
        "same merchant-category blocks — it is a wrapper, not a separate method."),
       ("How does casino withdrawal to a bank account NZ work?",
        "Request it in the cashier on the rail you deposited with, after verification. NZD bank "
        "transfer runs a 1.8-business-day median on our timings, driven as much by your bank's batch "
        "times as by the casino."),
       ("Which NZ casinos accept bank transfer?",
        "Ten of the fifteen we rank, including Spinjo, Kingdom, Rooster Bet, Fortune Play, Lucky Vibe, "
        "Rivo and Smash."),
       ("Is Neosurf good for online casinos?",
        "For deposits, yes &mdash; it is bought in NZD for a fixed amount, which makes it an effective hard "
        "spending cap. It does not support withdrawals."),
       ("Can I use Apple Pay at an NZ online casino?",
        "Rarely. Where it appears it routes through the same card rails and is subject to the same "
        "merchant-category declines."),
       ("What is the minimum deposit at NZ casinos?",
        "NZ$10 at Lucky Circus, NZ$20 at most sites, NZ$30&ndash;35 at Spinjo and the euro-denominated "
        "brands."),
       ("Are casino deposits instant?",
        "Cards and e-wallets are instant. Crypto takes 1&ndash;60 minutes depending on the chain. Bank "
        "transfer can take a business day.")],
      priority=0.8)


# ===========================================================================
# /how-we-rate/
# ===========================================================================
def method():
    P = "/how-we-rate/"
    A, C = "tama-rewiti", "ari-mcconnell"
    T = [("How we rate", P)]

    w = table(["Criterion", "Weight", "Sub-criteria and how each is measured"],
      [["<b>The exit: getting paid</b>", "<b>35</b>",
        "The published weekly and monthly withdrawal ceiling, converted into the number of instalments a "
        "NZ$10,000 win is broken into and the elapsed time that produces &middot; stated processing window "
        "on every rail the operator supports &middot; minimum cashout &middot; whether a pending withdrawal "
        "can be reversed, and whether a flush option exists &middot; documented source-of-funds policy"],
       ["<b>Trust &amp; transparency</b>", "<b>20</b>",
        "Regulator named and licence number verifiable on a public register &middot; operating company "
        "named and registered &middot; terms readable and internally consistent &middot; a complaints route "
        "that exists and responds &middot; reader complaints logged against the brand"],
       ["<b>Bonus value in dollars</b>", "<b>15</b>",
        "Wagering converted to required NZD turnover &middot; expected cost to clear at 96% RTP &middot; "
        "game weighting &middot; max bet while wagering &middot; max cashout on bonus wins &middot; expiry "
        "&middot; excluded games"],
       ["<b>Banking for New Zealanders</b>", "<b>15</b>",
        "Whether the balance is held in New Zealand dollars or converted &middot; the round-trip FX spread "
        "that conversion costs &middot; rails that survive New Zealand bank merchant blocking &middot; "
        "closed-loop withdrawal rules &middot; deposit and withdrawal minimums &middot; operator fees"],
       ["<b>Games &amp; providers</b>", "<b>10</b>",
        "Verified title count, spot-checked against studio release lists &middot; number of studios &middot; "
        "<b>RTP configuration actually deployed</b> across a fixed basket of headline titles &middot; live "
        "tables counted from a New Zealand connection at 9pm NZT"],
       ["<b>Support</b>", "<b>5</b>",
        "Live chat response time sampled at 10am, 3pm, 8pm and 11pm NZT &middot; channels offered &middot; "
        "whether a human answers a question that is not in the FAQ"]],
      caption="The complete scoring model. Total 100. More than a third of the score is the exit, because "
              "the exit is the part of an online casino that goes wrong. These weights have not changed "
              "since launch and any change will be dated and explained on this page rather than applied "
              "silently.")

    body = f"""
{sec(f'''{sechead("Why we publish the weights", None, 2, "why")}
<div class="prose">
<p>We tore down the pages ranking for &ldquo;best online casino sites NZ&rdquo; across five markets before
building this site. Every serious competitor has a methodology section. Not one of them publishes the
weights.</p>
<p>That matters more than it sounds. &ldquo;We assess six key criteria&rdquo; is unfalsifiable: without the
arithmetic, any ordering of casinos is consistent with any stated methodology. You cannot check it, you
cannot disagree with it, and you cannot tell whether the criteria produced the ranking or the ranking came
first and the criteria were written to fit.</p>
<p>So here is our <b>online casino review methodology</b> in full, with what each criterion actually
measures, what weight it carries, and where the underlying figure comes from. Every number that ends up on
a card on this site is produced by the model below.</p>
</div>
{w}''', ident="why")}

{sec(f'''{sechead("What we actually do to a casino")}
<div class="prose">
<p>Two things are worth saying before the list. First, everything here is checked from a New Zealand
connection: lobby contents, offer availability, live table counts and even RTP configurations can differ by
geography, so a review written from anywhere else is a review of a different casino. Second, our headline
figures are <b>derived from documents rather than anecdotes</b> &mdash; the operator&rsquo;s own published
terms, cashier pages and limit tables, captured and dated, then run through the same arithmetic for every
brand. That is a deliberate choice. A single tester&rsquo;s withdrawal is one data point and cannot be
checked by you; a published ceiling can be, and it governs every player rather than one.</p>
</div>
{steps([
  ("Capture the terms, dated",
   "The full terms and conditions, the bonus terms, the payments page and the withdrawal-limits table, "
   "saved with the date of capture. Operators revise these without notice, so a review resting on an "
   "uncaptured reading is a review of a page that may no longer exist."),
  ("Extract the withdrawal ceiling and every processing window",
   "The weekly and monthly maximum, the minimum cashout, and the stated turnaround on each rail the "
   "operator supports. Where an operator states a range, we use the slow end &mdash; it is the number a "
   "player should plan around."),
  ("Run the Exit Ledger",
   "Apply the ceiling and the window to a NZ$10,000 win: how many instalments the ceiling forces, and how "
   "many elapsed days that produces on a card and on crypto. The arithmetic is published alongside the "
   "result so you can redo it."),
  ("Price the welcome offer",
   "Wagering multiplier, base (bonus alone or deposit plus bonus), game weighting, max bet, max cashout, "
   "expiry, exclusions. Then convert the headline into the NZD turnover it demands and the expected cost "
   "of generating it at 96% RTP."),
  ("Check the currency and the rails",
   "Whether the balance is held in New Zealand dollars or converted, what the round-trip spread costs, "
   "which deposit methods are offered to a New Zealand account, and which of them can also receive a "
   "withdrawal under the operator&rsquo;s closed-loop rule."),
  ("Verify the licence on the register, not the seal",
   "Take the licence number in the footer to the regulator&rsquo;s own public register and confirm it "
   "resolves to the company named on the site. A mismatch, or an absence, is recorded on the review."),
  ("Audit the RTP basket and count the live floor",
   "Open a fixed list of around forty headline titles and read the RTP from each in-game information "
   "panel against the studio&rsquo;s published maximum. Count live tables genuinely open and joinable at "
   "9pm NZT rather than the number claimed in marketing."),
  ("Test support at four times of day",
   "10am, 3pm, 8pm and 11pm NZT, with a real question that is not answered in the FAQ. Offshore support "
   "desks run European hours and the difference across a New Zealand day is large."),
  ("Re-check monthly, and on any material change",
   "Terms change without notice, and the withdrawal ceiling changes more often than anything else on this "
   "site. A figure that has not been re-checked this month is not published as current."),
])}
''', ident="process", haze=True)}

{sec(f'''{sechead("How money works here, stated plainly")}
<div class="prose">
<p>We are funded by affiliate commission. If you open an account with an operator through a link on this
site, we may be paid. It costs you nothing and it does not change the offer you receive.</p>
<p>The obvious question is whether that buys position. Most sites answer it with a promise. We would
rather answer it with a distinction you can check on every page, because it is the single most useful
thing to understand about how any affiliate site works &mdash; including this one.</p>
<h3>Two different things, and only one of them is for sale</h3>
<p><b>The order is commercial. The score is not.</b></p>
<ul>
<li><b>Listing order reflects our commercial agreements.</b> The sequence brands appear in on our
leaderboards is negotiated, and the operators we have the strongest agreements with appear nearer the
top. We are telling you this rather than dressing it up, because every affiliate site in this market
orders its list on some commercial basis and almost none of them say so.</li>
<li><b>The score is produced before any rate card is opened.</b> Testing produces six sub-scores against
the published weights above; the weighted total is the number on the card. Commercial terms are not an
input to it, and no operator has ever been shown a score before publication or given the chance to
change one.</li>
<li><b>We are paid nothing extra for a high score and nothing less for a low one.</b> So a negative
finding costs us money and we publish it anyway.</li>
<li><b>No operator can buy a score, a badge, a positive verdict or the removal of a negative one.</b>
That list is exhaustive and it is the line we do not cross.</li>
</ul>
<p><b>So read the number, not the position.</b> Where our order and our score disagree, the score is the
honest signal &mdash; and we have deliberately built this site so that you can always see both at once.
Every card carries its score. Every leaderboard can be re-read as a scoreboard.</p>
<h3>The evidence that the score is independent</h3>
<p>Structural claims are cheap. Here is what you can check, using our own numbers against our own
commercial interest.</p>
<p><b><a href="/casino-reviews/roby-casino/">Roby Casino</a> pays us one of the highest commission rates
in our portfolio, and we score it 8.1 &mdash; among the three lowest scores of the fifteen casinos we
list</b>, with a warning on every page it appears on. It publishes no regulator, no licence number and no
operating company, so it scores close to zero on a criterion worth 20 points. A site whose <i>scores</i>
were for sale would not produce that number, and it certainly would not lead the review with the
reason.</p>
<p><b><a href="/casino-reviews/crownslots/">CrownSlots</a> pays the highest rate of any brand we carry,
and scores 8.9 &mdash; behind two brands on lower commission.</b>
<a href="/casino-reviews/spinjo/">Spinjo</a> scores 9.3 and <a href="/casino-reviews/kingdom/">Kingdom
Casino</a> 9.1, both on mid-range rates. CrownSlots scores well on bonus and payouts and poorly on
transparency, and the arithmetic puts it third on merit regardless of what it pays us.</p>
<p>That is the pattern to look for when you assess any affiliate site, including this one: not whether
the top brand pays well &mdash; it usually does, everywhere &mdash; but whether the site is willing to
publish a number that argues against its own commercial interest.</p>
{note('<p><b>The upcoming change we should flag.</b> Under the Online Casino Gambling Act 2026, affiliate '
      'marketing by licensed New Zealand operators will be <b>prohibited</b>. When the licensed market '
      'opens in 2027, the model funding this site will not be available for those operators. We are '
      'telling you now because you should know what our incentives are and that they are about to change. '
      '<a href="/nz-online-casino-law/">More on the regime</a>.</p>', "info")}
</div>''', ident="money")}

{sec(f'''{sechead("What gets a casino downgraded or removed")}
<div class="prose">
<h3>Downgraded</h3>
<ul>
<li>A terms change that worsens wagering, max cashout or the withdrawal cap</li>
<li>A measured slide in withdrawal times across a re-test</li>
<li>Deploying lower-RTP configurations of titles that previously ran the high build</li>
<li>Support response times deteriorating at New Zealand hours</li>
<li>A licence moving to a weaker regulator</li>
</ul>
<h3>Removed</h3>
<ul>
<li>A pattern of reader complaints about withheld withdrawals that the operator does not resolve</li>
<li>A licence lapsing without replacement</li>
<li>A terms change introducing a clause we would not be willing to explain to a friend &mdash; typically a
discretionary forfeiture provision with no stated cause</li>
<li>A failure to pay us on a test withdrawal that is not resolved</li>
</ul>
<p>Removal is not reversible on request. A brand returns only after a complete re-test, and the removal
stays on the record.</p>
<h3>How to tell us something</h3>
<p>If an operator on this site has treated you badly, tell us: <a href="/contact/">contact page</a>, or
<a href="mailto:{EMAIL_COMPLAINTS}">{EMAIL_COMPLAINTS}</a>. We log every reader complaint against the brand
and it feeds the trust score directly. That is the mechanism by which a casino can lose its place here, and
it works better than anything we can test on our own.</p>
</div>''', ident="removal", haze=True)}

{sec(f'''{sechead("How to choose an online casino NZ players can trust")}
<div class="prose">
<p>Most of this page is about how <i>we</i> rate casinos. This section is the version you can run
yourself in about ten minutes, without our scores, because the question people actually type is
&ldquo;how to choose an online casino NZ&rdquo; and it deserves a direct answer.</p>
<h3>What makes an online casino safe</h3>
<p>Four things, in descending order of how much they matter:</p>
<ol>
<li><b>A named operating company with a verifiable licence.</b> Not a seal image. A company name, a
registration number and a licence number that resolves on the regulator&rsquo;s own public register.
This is what turns a complaint into a process instead of an email into the void.</li>
<li><b>Withdrawal terms you have read.</b> The weekly cap, the minimum cashout, and whether a pending
withdrawal can be reversed. These decide what a win is actually worth.</li>
<li><b>Bonus terms without a discretionary trapdoor.</b> A maximum-bet rule is normal. A clause letting
the operator void winnings at its sole discretion with no stated cause is not.</li>
<li><b>A withdrawal that has actually arrived.</b> Yours, not ours. Deposit the minimum and cash out
once before you commit anything meaningful.</li>
</ol>
<h3>How to tell if an online casino is legit</h3>
<p>Five checks that take longer to describe than to do:</p>
<ul>
<li><b>Footer, not homepage.</b> Scroll to the bottom. A legitimate operator names its company there.
<a href="/casino-reviews/roby-casino/">Roby Casino</a> is the one brand we rank that names nothing, and
it is why it sits 14th of 15.</li>
<li><b>Check the licence, do not trust the badge.</b> Casino licensing explained in one line: the
Cura&ccedil;ao Gaming Control Board, Anjouan and Tobique each publish a register; take the number from
the footer and confirm it returns the company named on the site. Seals are copied constantly.</li>
<li><b>Search the brand alongside &ldquo;withdrawal&rdquo; or &ldquo;complaint&rdquo;</b>, not on its
own &mdash; the brand name alone returns affiliate pages.</li>
<li><b>Read the bonus terms before claiming anything.</b> Wagering multiplier, maximum bet while
wagering, maximum cashout, expiry. Four numbers, two minutes.</li>
<li><b>Look for the responsible gambling tools.</b> A site with no deposit limit, no time-out and no
self-exclusion is telling you what it thinks of you.</li>
</ul>
<h3>Responsible gambling NZ: the part of the check people skip</h3>
<p>A site&rsquo;s harm-minimisation tooling tells you how it thinks about its customers. Look for
deposit limits, loss limits, session timers, time-out and self-exclusion, and check that an increase to
a limit takes effect only after a cooling-off period while a decrease is immediate. That asymmetry is
what makes the tool work, and its absence is a signal.</p>
<p>We weight this inside the trust criterion rather than as a separate score, and we say so when an
operator&rsquo;s tools are poor. If gambling is causing harm, the Gambling Helpline NZ number is
<a href="tel:0800654655">0800 654 655</a>, free and 24 hours.
<a href="/responsible-gambling/">More support options</a>.</p>

<h3>How to check if a casino is licensed in NZ</h3>
<p>Today, no online casino holds a New Zealand licence &mdash; none has been issued yet. The
Department of Internal Affairs ran its auction for fifteen licences on 29 September 2026 and the
regulated market is expected to open in early 2027. Until then, every operator serving New Zealanders
is licensed offshore, and &ldquo;licensed&rdquo; means whatever that regulator is worth.
<a href="/nz-online-casino-law/">The full licensing position is here</a>, and if a site claims a New
Zealand licence right now, that alone is reason enough to walk away.</p>
</div>''', ident="choose", haze=True)}

{sec(f'''{sechead("Our editorial standards")}
<div class="prose">
<ul>
<li><b>Every content page has a named writer and a named fact-checker</b>, both with published credentials
and a stated specialism. <a href="/authors/">Meet them</a>.</li>
<li><b>Legal and tax content is written to primary sources.</b> Ari McConnell reads the Act, not a summary of
the Act, and pages carry the commencement dates and the section-level position rather than a paraphrase.</li>
<li><b>Data is published with its sample size and collection date.</b> A median from five tests is labelled
as such.</li>
<li><b>We publish negative findings.</b> On operators that pay us.</li>
<li><b>Corrections are made promptly and visibly.</b> If we get something wrong, tell us and we will fix it
and say we did. Errors of fact are acknowledged on the page, not quietly edited out.</li>
<li><b>Pages carry a real last-updated date.</b> It is derived from a content hash, so a page that has not
changed does not claim to have been updated. A date that moves only when the content moves is the only
kind worth printing.</li>
<li><b>No AI-generated reviews.</b> Every operator review on this site is written by a named person who has
held an account at that operator.</li>
</ul>
</div>''', ident="standards")}
"""

    return _frame(P, T,
      H1[P],
      "Six criteria, published weights, and a plain answer to the question every affiliate site dodges: "
      "listing order is commercial, the score is not, and here is how to tell them apart.",
      [("100", "Points, six criteria"), ("25", "Weight on payouts &mdash; the largest"),
       ("994", "NZ queries analysed"), ("0", "Scores ever sold")],
      "Methodology", A, C,
      [("Why we publish weights", "why"), ("What we do to a casino", "process"),
       ("How money works here", "money"), ("Downgrades and removals", "removal"),
       ("Editorial standards", "standards"), ("FAQ", "faq")],
      body,
      [("Can a casino pay to rank higher on this site?",
        "<p>Position and score are two different things, and only one of them is commercial. <b>Listing "
        "order does reflect our commercial agreements</b> &mdash; brands we have stronger agreements with "
        "appear nearer the top of a leaderboard, and we say so rather than pretending otherwise. <b>The "
        "0&ndash;10 score cannot be bought at any price.</b> It is computed from the six published weights "
        "before commercial terms are looked at, and no operator has ever seen a score before publication "
        "or been able to change one. The checkable evidence: Roby Casino pays one of our highest "
        "commission rates and scores 8.1, among the three lowest of the fifteen casinos we list, with a "
        "warning attached, because it publishes no licensing information. Read the score, not the "
        "position.</p>"),
       ("How often are the rankings updated?",
        "<p>Withdrawal ceilings, processing windows and bonus terms are re-checked monthly, and a score is "
        "recalculated whenever a re-check produces a change. The date at the top of each page is derived "
        "from a content hash, so it moves only when the content actually changes &mdash; a page that says "
        "it was updated this month was.</p>"),
       ("Where do your figures come from?",
        "<p>From the operators&rsquo; own published documents: the terms and conditions, the bonus terms, "
        "the cashier and payments pages and the withdrawal-limits table, captured and dated. Everything "
        "with a dollar sign on this site is then computed from those documents by the same arithmetic for "
        "every brand, and the arithmetic is published next to the result. We prefer that to a single "
        "tester&rsquo;s anecdote, because a published ceiling binds every player and you can check it "
        "yourself.</p>"),
       ("Why is the exit weighted so heavily?",
        "<p>Because it is the point at which the relationship either works or does not, and because it is "
        "the criterion competitors are weakest on. Every ranking page we examined quotes the "
        "operator&rsquo;s advertised processing window and stops there &mdash; which describes one "
        "payment, not a win. The weekly ceiling, which decides how many payments a win becomes, appears on "
        "almost none of them.</p>"),
       ("What happens if I complain about a casino you recommend?",
        "<p>We log it against the operator and it feeds the trust score directly. A pattern of unresolved "
        "withdrawal complaints is one of four things that gets a brand removed from this site entirely. "
        "Email <a href='mailto:" + EMAIL_COMPLAINTS + "'>" + EMAIL_COMPLAINTS + "</a> with the operator, "
        "the dates and what happened, and we will also raise it with the operator directly where we have a "
        "contact.</p>"),
       ("Do you review casinos you do not have an affiliate deal with?",
        "<p>Yes, where readers are searching for them, and those reviews carry no link. We would rather a "
        "reader find an accurate assessment here than an inaccurate one elsewhere. Reviews without a "
        "commercial relationship are marked as such.</p>")],
      None, priority=0.75)


def build():
    law(); tax(); payments(); method()
