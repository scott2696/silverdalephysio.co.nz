#!/usr/bin/env python3
"""The Exit Ledger: how long a real win takes to reach a New Zealand bank account.

Every competing page ranks casinos on how fast a *withdrawal* is processed and
stops there. That number answers the wrong question. A site quoting "1-6 hours"
and a NZ$5,000 weekly ceiling cannot pay a NZ$20,000 win in 1-6 hours; it pays
it in four instalments over the better part of a month, and the player is sitting
on a balance in a casino account for three of those weeks with the games one tap
away. The processing window is the smallest term in the equation.

So this module prices the exit the way bonuscalc.py prices the entrance:

    tranches      = ceil(win / weekly cap)
    elapsed days  = (tranches - 1) x 7 + first payment window
    fx cost       = win x spread, where the balance is not held in NZD

The weekly cap, the payout windows and the balance currency are the operator's
own published figures, carried in operators.json. Nothing here is estimated from
a rate card and nothing is taken from an operator's marketing.

Two reference wins are used across the site, both chosen to be ordinary rather
than dramatic: NZ$2,000 is a good night on the pokies, and NZ$10,000 is the sort
of win that makes a person read the terms for the first time.
"""
import math
import re

from bonuscalc import FX, FX_DATE, FX_SPREAD

# The reference wins. SMALL is inside almost every weekly ceiling, so it isolates
# the processing window; BIG is outside most of them, which is the whole point.
SMALL, BIG = 2_000, 10_000

# Verdict bands for a BIG win, in elapsed days.
QUICK, SLOW = 8, 28

BUSINESS_DAY = 1.4      # business days -> calendar days, allowing for weekends
UNCAPPED_DAYS = 3       # a stated cap of "none" still clears in tranches in practice


def _cap(op):
    """(currency, face amount, NZD amount) for the weekly withdrawal ceiling.

    Returns None where the operator states no weekly cap, which is a materially
    better position and is reported as such rather than as a missing value.
    """
    raw = op.get("withdrawal_limit") or ""
    if not raw or "no stated" in raw.lower() or "none" in raw.lower():
        return None
    m = re.search(r"(NZ\$|€|\$)\s*([\d,]+)", raw)
    if not m:
        return None
    cur = {"NZ$": "NZD", "€": "EUR", "$": "USD"}[m.group(1)]
    face = float(m.group(2).replace(",", ""))
    return cur, face, round(face * FX[cur])


def _window(raw):
    """(best hours, worst hours) from an operator's stated payout window.

    Handles "1-6 hours", "10 minutes - 2 hours", "2-5 business days" and
    "24-48 hours". Returns None for a rail the operator does not support.
    """
    if not raw or "not supported" in raw.lower():
        return None
    s = raw.lower().replace("–", "-").replace("—", "-")
    nums = [float(n) for n in re.findall(r"[\d.]+", s)]
    if not nums:
        return None
    lo, hi = (nums[0], nums[-1]) if len(nums) > 1 else (nums[0], nums[0])
    if "business day" in s or "working day" in s:
        return lo * 24 * BUSINESS_DAY, hi * 24 * BUSINESS_DAY
    if "day" in s:
        return lo * 24, hi * 24
    if "minute" in s and "hour" not in s:
        return lo / 60, hi / 60
    if "minute" in s and "hour" in s:
        # "10 minutes - 2 hours": the first figure is minutes, the second hours.
        return lo / 60, hi
    return lo, hi


def rails(op):
    """The operator's three payout rails, fastest first, unsupported ones dropped."""
    out = []
    for key, label in (("payout_crypto", "Crypto"),
                       ("payout_ewallet", "E-wallet"),
                       ("payout_card", "Card or bank transfer")):
        w = _window(op.get(key))
        if w:
            out.append({"key": key.replace("payout_", ""), "label": label,
                        "stated": op[key], "best": w[0], "worst": w[1]})
    return sorted(out, key=lambda r: r["worst"])


def fastest(op):
    r = rails(op)
    return r[0] if r else None


def slowest_card(op):
    """The card or bank-transfer rail, which is what most New Zealanders use."""
    for r in rails(op):
        if r["key"] == "card":
            return r
    return None


def exit_cost(op, win=BIG, rail=None):
    """The full ledger entry for getting `win` out of `op`.

    `rail` picks the payout rail; the default is the operator's fastest, which
    is the most favourable reading and the one their marketing implies.
    """
    r = rail or fastest(op)
    if not r:
        return None
    cap = _cap(op)
    cap_nzd = cap[2] if cap else None

    if cap_nzd:
        tranches = max(1, math.ceil(win / cap_nzd))
    else:
        tranches = 1

    first_best, first_worst = r["best"] / 24, r["worst"] / 24
    if tranches > 1:
        days_best = (tranches - 1) * 7 + first_best
        days_worst = (tranches - 1) * 7 + first_worst
    else:
        days_best, days_worst = first_best, first_worst
        if not cap_nzd:
            days_worst = max(days_worst, UNCAPPED_DAYS * 0.0)

    cur = cap[0] if cap else "NZD"
    fx = round(win * FX_SPREAD) if cur != "NZD" else 0

    if days_worst <= QUICK:
        verdict, tone = "Paid in days", "yes"
    elif days_worst <= SLOW:
        verdict, tone = "Paid in weeks", "warn"
    else:
        verdict, tone = "Paid over months", "no"

    return {
        "win": win, "rail": r, "tranches": tranches,
        "cap_currency": cur, "cap_face": cap[1] if cap else None,
        "cap_nzd": cap_nzd, "capped": bool(cap_nzd),
        "days_best": days_best, "days_worst": days_worst,
        "weeks": round(days_worst / 7, 1),
        "fx_cost": fx, "net": win - fx,
        "verdict": verdict, "tone": tone,
    }


def ledger(ops, win=BIG):
    """Every operator priced for the same win, fastest exit first."""
    rows = [(o, exit_cost(o, win)) for o in ops]
    rows = [(o, e) for o, e in rows if e]
    return sorted(rows, key=lambda t: (t[1]["days_worst"], t[1]["fx_cost"]))


def days(n):
    """Elapsed time in the unit a reader thinks in."""
    if n < 1:
        h = n * 24
        if h < 1:
            return f"{round(h * 60)} minutes"
        return f"{h:.0f} hours" if h >= 2 else "about an hour"
    if n < 14:
        return f"{n:.0f} days" if n >= 2 else "1 day"
    return f"{n / 7:.0f} weeks"


def money(n):
    return f"NZ${n:,.0f}"


__all__ = ["SMALL", "BIG", "FX_DATE", "FX_SPREAD", "rails", "fastest",
           "slowest_card", "exit_cost", "ledger", "days", "money"]
