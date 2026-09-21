#!/usr/bin/env python3
"""New Zealand online gambling market data, from the regulator's own reports.

Every figure here comes from two Department of Internal Affairs reports
released on 19 May 2026 and published as PDFs on the DIA's "Online Gambling for
Providers" page, where almost nobody will ever find them:

  2025 New Zealand Market Insights Report — Historical Market Analysis
  2025 New Zealand Market Insights Report — User Behaviour

Both cover the year ending 30 September 2025 and were prepared for the DIA by
Dot Loves Data. Their stated method matters and is reproduced on the page: the
numbers are built from consumer card transactions at one bank, upweighted to
estimate the whole market, and they measure *deposits* rather than amounts
wagered, with no account taken of winnings. So they describe money going in,
not money lost — a distinction every secondary source we found gets wrong.

Not one page ranking for "best online casino sites NZ" in September 2026 cites
either report. They are the best New Zealand-specific gambling data in
existence and they are sitting in a PDF on a page written for licence
applicants.
"""

SOURCE = ("Department of Internal Affairs, <i>2025 New Zealand Market Insights "
          "Report</i> (Historical Market Analysis, and User Behaviour), prepared by "
          "Dot Loves Data and released 19 May 2026. Year ending 30 September 2025.")
SOURCE_URL = "https://www.dia.govt.nz/Online-Gambling-for-Providers"
METHOD = ("Built from consumer card transactions at one bank, upweighted to estimate the "
          "whole market. The figures measure <b>deposits, not losses</b>: money moving into "
          "gambling accounts, with no account taken of anything paid back out.")

# (figure, label, note) — the size and shape of the market
MARKET = [
    ("360,000", "New Zealanders gambling online",
     "Unique customers transacting with offshore online gambling merchants, as at September 2025."),
    ("NZ$100m+", "Spent every month",
     "Total monthly online gambling deposits have exceeded NZ$100 million every month since March 2024."),
    ("+10.5%", "Market growth in a year",
     "Deposits rose NZ$129.6m in the year to September 2025."),
    ("+2.7%", "Growth in people",
     "Only 9,400 more individuals. The market is growing because existing customers deposit more, "
     "not because many more New Zealanders are starting."),
]

# (segment, share, growth, note)
SEGMENTS = [
    ("Hybrid — casino and sportsbook on one account", "77%", "+22%",
     "The dominant shape of the market by a distance, and the model most of the brands on this page run."),
    ("Casino", "14%", "+38%",
     "The fastest-growing segment in the country, up from 11% of the market a year earlier."),
    ("Lottery", "flat", "&mdash;",
     "Neither growing nor shrinking materially."),
    ("Sports betting", "declining", "&minus;37%",
     "Deposits fell by more than a third, alongside a 36% fall in transactions &mdash; the clearest "
     "measurable effect of the June 2025 TAB NZ monopoly on offshore books."),
]

# (figure, label, note) — who the average player actually is
PLAYER = [
    ("NZ$290", "Median annual spend",
     "Up 5% on the previous year. In a month they actually gamble, the median is NZ$80."),
    ("55%", "Gamble 12 times a year or fewer",
     "The typical New Zealander who gambles online dabbles. They are not the ones the market runs on."),
    ("25&ndash;34", "The typical age",
     "Lives in Auckland, and is in the most deprived fifth of the population."),
    ("NZ$170", "Median spend in a typical month",
     "The <i>mean</i> is NZ$840, dragged up by a long high-value tail. Where a mean is five times "
     "the median, the average is not describing anybody."),
]

# The concentration finding, which is the one that matters most.
CONCENTRATION = [
    ("The top 20% of gamblers account for <b>90%</b> of all money deposited", "no"),
    ("<b>20%</b> of players have a median gap of <b>under an hour</b> between transactions", "no"),
    ("<b>17%</b> transacted 100 or more times in the year; <b>5%</b> transacted 365 or more", "no"),
    ("The overall median gap between transactions is <b>23 hours</b>, and over half of players "
     "transact more than once a day when they are gambling", "warn"),
    ("Peak gambling hours are <b>early morning and mid-week</b> &mdash; not evenings and weekends", "warn"),
]

# (region, figure, note) — where the money comes from
REGIONS = [
    ("Gisborne", "Nearly 10% of the population gambles online",
     "Roughly double the national rate of about 5%, and the highest spend per head in the country "
     "at NZ$372 a year."),
    ("Auckland", "NZ$420m+ deposited in the year",
     "116,000 unique customers, at NZ$254 per person &mdash; a third less per head than Gisborne."),
    ("Nelson", "+32% year on year", "The fastest-growing region in the country, followed by Southland at +21.6%."),
    ("Waikato and Canterbury", "+19.8% and +19.1%", "The largest increases outside the small regions."),
]

# Market structure, from the Historical Market Analysis.
STRUCTURE = [
    ("Top 15 merchants", "over 80% of all market spend",
     "A highly concentrated market. Fifteen brands take four dollars in every five."),
    ("Top 4 licensing jurisdictions", "96.3% of market spend",
     "Cyprus, Gibraltar, Great Britain and Malta. Almost the entire New Zealand market is served "
     "from four places, none of them New Zealand."),
]

# Recent, checkable enforcement activity — evidence the regulator is active.
ENFORCEMENT = [
    ("September 2026", "NZ$11.5m recovered from the pokies sector",
     "The DIA recovered NZ$11.5 million after an investigation into class 4 (pub pokies) compliance, "
     "finding what it called widespread issues in how proceeds were handled &mdash; in some cases money "
     "owed to community grants was retained instead. Section 106 of the Gambling Act 2003 requires a "
     "corporate society to distribute net proceeds to authorised purposes."),
    ("12 September 2026", "Auction date announced",
     "The DIA confirmed the online casino licence auction begins on 29 September 2026. It has declined "
     "to say how many operators are taking part or name them, to protect the integrity of the process. "
     "Trina Lowry, its Programme Director of Online Gambling Implementation, has confirmed that being "
     "accepted through the expressions-of-interest stage does not guarantee an operator will be invited "
     "to apply for a licence."),
]
