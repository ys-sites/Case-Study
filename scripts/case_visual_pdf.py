"""Pinterest-style editorial case-study booklet, rendered entirely from solution_spec.json.

Structure follows the classic case-study template (Challenge → Approach → Options → Results →
Execution → Defence) using the repo's editorial design system: deep emerald + mint accents,
Segoe UI for structure, Georgia for editorial quotes, stat cards, pills and charts.
Every text block is auto-fitted (shrinks until it fits) so long case text never overflows.
"""

from __future__ import annotations

from pathlib import Path

import pymupdf

W, H, M = 612, 792, 40
FONTS = {"bold": "C:/Windows/Fonts/segoeuib.ttf", "reg": "C:/Windows/Fonts/segoeui.ttf",
         "serif": "C:/Windows/Fonts/georgia.ttf", "semi": "C:/Windows/Fonts/seguisb.ttf"}
FALLBACK = {"bold": "hebo", "reg": "helv", "serif": "tiro", "semi": "hebo"}


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


C = {k: _rgb(v) for k, v in {
    "pine": "#022C22", "emerald": "#064E3B", "mint": "#10B981", "mint_l": "#34D399", "mint_bg": "#ECFDF5",
    "mint_bd": "#A7F3D0", "canvas": "#F8FAFC", "white": "#FFFFFF", "muted_bg": "#F1F5F9", "border": "#E2E8F0",
    "ink": "#0F172A", "body": "#334155", "muted": "#64748B", "amber": "#D97706", "amber_bg": "#FEF3C7",
    "red": "#DC2626", "red_bg": "#FEE2E2", "navy": "#1E293B"}.items()}


def _cad(x):
    if x is None:
        return "n/a"
    a = abs(x)
    s = f"${a / 1e6:.2f}M" if a >= 1e6 else f"${a / 1e3:.0f}K" if a >= 1e4 else f"${a:,.0f}"
    return ("-" if x < 0 else "") + s


def _mo(x):
    return f"{x:.1f} mo" if x is not None else "> 60 mo"


FOOTER = {"text": ""}


class Page:
    def __init__(self, doc, n, total, case_id, section):
        n = doc.page_count + 1  # numbered by position, so optional pages never break the sequence
        self.p = doc.new_page(width=W, height=H)
        self.fonts = {}
        for name, path in FONTS.items():
            if Path(path).exists():
                self.p.insert_font(fontname=name, fontfile=path)
                self.fonts[name] = (name, path)
            else:
                self.fonts[name] = (FALLBACK[name], None)
        self.p.draw_rect(self.p.rect, fill=C["canvas"], width=0)
        if section:
            self.p.draw_rect(pymupdf.Rect(0, 0, W, 26), fill=C["pine"], width=0)
            self.text(M, 17, section.upper(), 7.5, "bold", C["mint_l"])
            self.text_right(W - M, 17, f"CASE {case_id}", 7.5, "bold", C["white"])
            self.p.draw_line((M, H - 30), (W - M, H - 30), color=C["border"], width=0.7)
            self.text(M, H - 17, FOOTER["text"], 6.5, "reg", C["muted"])
            self.text_right(W - M, H - 17, f"{n:02d} / {total:02d}", 7, "bold", C["emerald"])

    def _f(self, font):
        return self.fonts[font]

    def width(self, s, size, font="reg"):
        name, path = self._f(font)
        f = pymupdf.Font(fontfile=path) if path else pymupdf.Font(name)
        return f.text_length(s, fontsize=size)

    def text(self, x, y, s, size, font="reg", color=None):
        name, path = self._f(font)
        self.p.insert_text((x, y), s, fontname=name, fontfile=path, fontsize=size, color=color or C["body"])

    def text_right(self, x, y, s, size, font="reg", color=None):
        self.text(x - self.width(s, size, font), y, s, size, font, color)

    def box(self, rect, s, size=9, font="reg", color=None, align=0, min_size=5.5, lh=1.25):
        """Auto-fit text into rect; shrinks the font until it fits."""
        name, path = self._f(font)
        rect = pymupdf.Rect(rect)
        size_now = size
        while size_now >= min_size:
            rc = self.p.insert_textbox(rect, s, fontname=name, fontfile=path, fontsize=size_now,
                                       color=color or C["body"], align=align, lineheight=lh)
            if rc >= 0:
                return rect.y1 - rc
            size_now -= 0.5
        clipped = s[: max(10, int(len(s) * 0.6))].rstrip() + "…"
        self.p.insert_textbox(rect, clipped, fontname=name, fontfile=path, fontsize=min_size,
                              color=color or C["body"], align=align, lineheight=lh)
        return rect.y1

    def card(self, rect, fill=None, border=None, stripe=None, radius=0.06):
        rect = pymupdf.Rect(rect)
        self.p.draw_rect(rect, fill=fill or C["white"], color=border or C["border"], width=0.7, radius=radius)
        if stripe:
            self.p.draw_rect(pymupdf.Rect(rect.x0, rect.y0, rect.x0 + 3.2, rect.y1), fill=stripe, width=0)

    def pill(self, x, y, s, fill, fg, size=7, pad=7, h=15):
        w = self.width(s, size, "bold") + 2 * pad
        self.p.draw_rect(pymupdf.Rect(x, y, x + w, y + h), fill=fill, width=0, radius=0.5)
        self.text(x + pad, y + h / 2 + size / 2.8, s, size, "bold", fg)
        return x + w + 5

    def check(self, x, y, ok, r=6):
        """Vector status badge (Segoe UI lacks check glyphs)."""
        self.p.draw_circle((x, y), r, fill=C["mint"] if ok else C["amber"], color=None)
        if ok:
            self.p.draw_polyline([(x - r * 0.45, y), (x - r * 0.1, y + r * 0.38), (x + r * 0.5, y - r * 0.38)], color=C["white"], width=1.4)
        else:
            self.p.draw_line((x, y - r * 0.5), (x, y + r * 0.1), color=C["white"], width=1.4)
            self.p.draw_circle((x, y + r * 0.42), 0.8, fill=C["white"], color=None)

    def heading(self, y, kicker, title, sub=""):
        self.text(M, y, kicker.upper(), 7.5, "bold", C["mint"])
        bottom = self.box((M, y + 4, W - M, y + 44), title, 21, "bold", C["ink"], min_size=14, lh=1.1)
        if sub:
            bottom = self.box((M, bottom + 2, W - M, bottom + 30), sub, 9, "reg", C["muted"], min_size=7)
        return bottom + 10

    def stat(self, rect, value, label, sub="", accent=None):
        rect = pymupdf.Rect(rect)
        accent = accent or C["mint"]
        self.card(rect)
        self.p.draw_rect(pymupdf.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 3), fill=accent, width=0)
        self.box((rect.x0 + 10, rect.y0 + 9, rect.x1 - 8, rect.y0 + 33), value, 17, "bold", accent, min_size=10)
        self.box((rect.x0 + 10, rect.y0 + 34, rect.x1 - 8, rect.y0 + 46), label.upper(), 6.8, "bold", C["emerald"], min_size=5)
        if sub:
            self.box((rect.x0 + 10, rect.y0 + 46, rect.x1 - 8, rect.y1 - 4), sub, 6.5, "reg", C["muted"], min_size=5)


# ------------------------------------------------------------------------------------------
def _cover(doc, spec, total):
    ci, intel, fs, inp = spec["case_identification"], spec["intelligence"], spec["financial_summary"], spec["case_inputs"]
    pg = Page(doc, 1, total, ci["id"], None)
    p = pg.p
    p.draw_rect(pymupdf.Rect(0, 0, W, 470), fill=C["pine"], width=0)
    p.draw_circle((W - 40, 90), 150, color=None, fill=C["emerald"], width=0)
    p.draw_circle((W - 40, 90), 95, color=C["mint"], width=1.2)
    x = pg.pill(M, 48, "CASE STUDY", C["mint"], C["pine"])
    x = pg.pill(x, 48, ci["discipline"].upper()[:38], C["emerald"], C["mint_l"])
    pg.pill(x, 48, ci["difficulty"].upper(), C["emerald"], C["mint_l"])
    pg.box((M, 84, W - 120, 250), ci["title"], 34, "bold", C["white"], min_size=20, lh=1.08)
    pg.box((M, 258, W - 120, 300), intel["what_the_case_tests"], 10.5, "reg", C["mint_bd"], min_size=8)
    pg.text(M, 330, "THE ANSWER", 7.5, "bold", C["mint_l"])
    pg.box((M, 338, W - M, 450), f"“{intel['scqa']['answer']}”", 12.5, "serif", C["white"], min_size=8.5, lh=1.3)
    cw = (W - 2 * M - 30) / 4
    stats = [(f"{inp['target_pct']:g}%", "Target", inp["target_metric"][:40]), (_cad(inp["budget"]), "Budget ceiling", "capital, CAD"),
             (f"{inp['timeline_months']} mo", "Deadline", "core implementation"), (_cad(fs["npv_CAD"]), "NPV of answer", f"at {fs['wacc_percent']:.1f}% WACC")]
    for i, (v, l, s) in enumerate(stats):
        pg.stat((M + i * (cw + 10), 440, M + i * (cw + 10) + cw, 506), v, l, s, C["mint"] if i < 3 else C["amber"])
    pg.text(M, 545, "INSIDE", 7.5, "bold", C["mint"])
    sections = ["01  The Challenge", "02  The Approach", "03  The Options", "04  The Results", "05  Execution", "06  Defence & Submission"]
    if spec.get("case_pack"):
        sections[3:3] = ["03b The Package"]
        sections[6:6] = ["05b Required Analysis"]
    for i, s in enumerate(sections):
        pg.text(M + (i % 2) * 260, 568 + (i // 2) * 22, s, 11, "semi", C["ink"])
    pg.box((M, 650, W - M, 700), f"Archetype: {intel['archetype_name']} · Family: {intel['family_label']} · Model: {intel['solution_model']}",
           8, "reg", C["muted"])
    pg.text(M, H - 40, f"{ci['id']} · Strategy Consulting Hub · Executive Case Simulation Team", 7, "bold", C["emerald"])


def _challenge(doc, spec, total):
    ci, intel, inp = spec["case_identification"], spec["intelligence"], spec["case_inputs"]
    pg = Page(doc, 2, total, ci["id"], "01 · The Challenge")
    y = pg.heading(52, "Situation · Complication · Question", "What this case is really asking", intel["what_the_case_tests"])
    sq = intel["scqa"]
    cw, chh = (W - 2 * M - 12) / 2, 128
    blocks = [("S", "Situation", sq["situation"]), ("C", "Complication", sq["complication"]),
              ("Q", "Question", sq["question"]), ("A", "Answer", sq["answer"])]
    for i, (k, t, body) in enumerate(blocks):
        x0, y0 = M + (i % 2) * (cw + 12), y + (i // 2) * (chh + 12)
        dark = k == "A"
        pg.card((x0, y0, x0 + cw, y0 + chh), fill=C["emerald"] if dark else C["white"], border=C["emerald"] if dark else C["border"])
        p = pg.p
        p.draw_circle((x0 + 22, y0 + 22), 11, fill=C["mint"] if dark else C["mint_bg"], color=None)
        pg.text(x0 + 18 - (1 if k in "QC" else 0), y0 + 26, k, 11, "bold", C["pine"] if dark else C["emerald"])
        pg.text(x0 + 40, y0 + 26, t.upper(), 8, "bold", C["mint_l"] if dark else C["emerald"])
        pg.box((x0 + 14, y0 + 40, x0 + cw - 12, y0 + chh - 10), body, 9, "serif" if dark else "reg",
               C["white"] if dark else C["body"], min_size=6)
    y += 2 * chh + 30
    pg.text(M, y, "CONSTRAINTS", 7.5, "bold", C["mint"])
    x, yy = M, y + 8
    for c in inp["constraints"][:6]:
        label = c if len(c) < 70 else c[:67] + "…"
        if x + pg.width(label, 7, "bold") + 20 > W - M:
            x, yy = M, yy + 20
        x = pg.pill(x, yy, label, C["mint_bg"], C["emerald"])
    y = yy + 40
    pg.text(M, y, "WHAT THE JUDGES SCORE", 7.5, "bold", C["mint"])
    rubric = inp.get("rubric") or {"Strategy": 25, "Financials": 25, "Implementation": 20, "Risk": 15, "Q&A defence": 15}
    total_pts = sum(rubric.values()) or 1
    by = y + 14
    for k, v in list(rubric.items())[:6]:
        pg.text(M, by + 8, k.replace("_", " ").title()[:34], 8, "reg", C["ink"])
        bw = (W - 2 * M - 200) * v / max(rubric.values())
        pg.p.draw_rect(pymupdf.Rect(M + 170, by, M + 170 + bw, by + 10), fill=C["mint"], width=0, radius=0.4)
        pg.text(M + 176 + bw, by + 8.5, f"{v / total_pts:.0%}", 7.5, "bold", C["emerald"])
        by += 18


def _approach(doc, spec, total):
    ci, intel = spec["case_identification"], spec["intelligence"]
    pg = Page(doc, 3, total, ci["id"], "02 · The Approach")
    y = pg.heading(52, f"Solution model · {intel['archetype_name']}", "How we cracked it", intel["solution_model"])
    tree = intel["issue_tree"]
    pg.card((M, y, W - M, y + 40), fill=C["pine"], border=C["pine"])
    pg.box((M + 12, y + 7, W - M - 12, y + 36), tree["root"], 10, "bold", C["white"], align=1, min_size=7)
    bw = (W - 2 * M - 20) / 3
    top = y + 58
    for i, b in enumerate(tree["branches"]):
        x0 = M + i * (bw + 10)
        pg.p.draw_line(((W) / 2, y + 40), (x0 + bw / 2, top), color=C["mint"], width=1)
        pg.card((x0, top, x0 + bw, top + 120), stripe=C["mint"])
        pg.box((x0 + 12, top + 8, x0 + bw - 8, top + 30), b["name"], 9.5, "bold", C["emerald"], min_size=7)
        pg.box((x0 + 12, top + 32, x0 + bw - 8, top + 116), "\n".join(f"• {q}" for q in b["questions"]), 8, "reg", C["body"], min_size=6)
    y = top + 136
    pg.card((M, y, W - M, y + 62), fill=C["amber_bg"], border=C["amber_bg"])
    pg.text(M + 14, y + 16, "HYPOTHESIS (FORMED IN THE FIRST 20 MINUTES)", 7.5, "bold", C["amber"])
    pg.box((M + 14, y + 22, W - M - 14, y + 58), f"“{intel['hypothesis']}”", 10, "serif", C["ink"], min_size=7)
    y += 78
    half = (W - 2 * M - 14) / 2
    pg.text(M, y, "TOOLKIT", 7.5, "bold", C["mint"])
    pg.box((M, y + 6, M + half, y + 92), "\n".join(f"• {t}" for t in intel["toolkit"]), 8.5, "reg", C["body"], min_size=6.5)
    pg.text(M + half + 14, y, "QUICK MATH", 7.5, "bold", C["mint"])
    pg.box((M + half + 14, y + 6, W - M, y + 92), "\n".join(f"• {t}" for t in intel["quick_math"]), 8.5, "reg", C["body"], min_size=6.5)
    y += 104
    from case_videos import plan_hours
    pg.text(M, y, f"TIME PLAN FOR A {plan_hours(intel['time_plan'])}-HOUR CRACKING WINDOW", 7.5, "bold", C["mint"])
    steps = intel["time_plan"]
    sw = (W - 2 * M) / len(steps)
    for i, s in enumerate(steps):
        x0 = M + i * sw
        pg.p.draw_rect(pymupdf.Rect(x0 + 1, y + 8, x0 + sw - 1, y + 14), fill=C["mint"] if i % 2 == 0 else C["emerald"], width=0)
        pg.text(x0 + 2, y + 27, s["time"], 7.5, "bold", C["ink"])
        pg.box((x0 + 2, y + 31, x0 + sw - 4, y + 44), s["step"], 8, "semi", C["emerald"], min_size=6)
        pg.box((x0 + 2, y + 44, x0 + sw - 4, y + 70), s["output"], 7, "reg", C["muted"], min_size=5.5)


def _options(doc, spec, total):
    ci, intel, oe = spec["case_identification"], spec["intelligence"], spec["options_evaluation"]
    pg = Page(doc, 4, total, ci["id"], "03 · The Options")
    y = pg.heading(52, "Solution ladder", "Four levels of solution, one recommendation", intel["ladder_rationale"])
    lw = (W - 2 * M - 30) / 4
    for i, r in enumerate(intel["solution_ladder"]):
        x0 = M + i * (lw + 10)
        h = 70 + i * 22
        y0 = y + 92 - i * 22
        sel = r.get("selected")
        pg.card((x0, y0, x0 + lw, y0 + h), fill=C["emerald"] if sel else C["white"], border=C["emerald"] if sel else C["border"])
        fg = C["white"] if sel else C["ink"]
        pg.text(x0 + 10, y0 + 15, f"{r['level'].upper()} · {r['name'].upper()}", 6.5, "bold", C["mint_l"] if sel else C["mint"])
        if r["option"]:
            pg.text(x0 + 10, y0 + 36, f"Option {r['option']}", 15, "bold", fg)
            pg.box((x0 + 10, y0 + 40, x0 + lw - 8, y0 + h - (24 if sel else 4)), f"{r['improvement_percent']:g}% · {_cad(r['capex_CAD'])}\n{r['rule']}",
                   7.5, "reg", C["mint_bd"] if sel else C["muted"], min_size=5.5)
        else:
            pg.box((x0 + 10, y0 + 24, x0 + lw - 8, y0 + h - 4), r["summary"], 8, "reg", C["red"], min_size=6)
        if sel:
            pg.pill(x0 + 10, y0 + h - 22, "RECOMMENDED", C["mint"], C["pine"], size=6.5, h=14)
    y += 184
    pg.text(M, y, "DECISION MATRIX (SCORE 0-10, WEIGHTED)", 7.5, "bold", C["mint"])
    y += 8
    cols = [M, M + 190, M + 240] + [M + 240 + (i + 1) * 92 for i in range(len(oe["options"]))]
    pg.p.draw_rect(pymupdf.Rect(M, y, W - M, y + 20), fill=C["pine"], width=0)
    pg.text(cols[0] + 6, y + 13, "Criterion", 7.5, "bold", C["white"])
    pg.text(cols[1] + 4, y + 13, "Weight", 7.5, "bold", C["white"])
    for j, o in enumerate(oe["options"]):
        pg.text(cols[2] + j * 92 + 6, y + 13, f"Option {o['label']}" + ("  (chosen)" if o["selected"] else ""), 7.5, "bold",
                C["mint_l"] if o["selected"] else C["white"])
    y += 20
    rows = [(c["name"], f"{c['weight']:.0%}", [o["scores"][c["name"]] for o in oe["options"]]) for c in oe["criteria"]]
    rows.append(("Weighted total", "100%", [o["weighted_total"] for o in oe["options"]]))
    for r_i, (name, wt, vals) in enumerate(rows):
        last = r_i == len(rows) - 1
        pg.p.draw_rect(pymupdf.Rect(M, y, W - M, y + 19), fill=C["mint_bg"] if last else C["white"], color=C["border"], width=0.5)
        pg.text(cols[0] + 6, y + 13, name, 8, "bold" if last else "reg", C["ink"])
        pg.text(cols[1] + 4, y + 13, wt, 8, "reg", C["muted"])
        for j, v in enumerate(vals):
            t = min(1, max(0, v / 10))
            fill = tuple(C["white"][k] * (1 - t * 0.7) + C["mint"][k] * t * 0.7 for k in range(3))
            pg.p.draw_rect(pymupdf.Rect(cols[2] + j * 92 + 2, y + 2, cols[2] + j * 92 + 88, y + 17), fill=fill, width=0, radius=0.2)
            pg.text(cols[2] + j * 92 + 34, y + 13, f"{v:.1f}", 8, "bold", C["ink"])
        y += 19
    y += 16
    pg.text(M, y, "THE THREE ALTERNATIVES", 7.5, "bold", C["mint"])
    y += 8
    for o in oe["options"]:
        flag = ("In budget" if o["within_budget"] else "OVER BUDGET") + (" · meets target" if o["meets_target"] else " · misses target")
        pg.card((M, y, W - M, y + 34), stripe=C["mint"] if o["selected"] else C["border"])
        pg.box((M + 12, y + 4, M + 330, y + 31), f"Option {o['label']}: {o['name']}", 8.5, "semi", C["ink"], min_size=6)
        pg.box((M + 335, y + 4, W - M - 8, y + 31), f"{_cad(o['capex_CAD'])} · {o['improvement_percent']:g}% · NPV {_cad(o['npv_CAD'])}\n{flag}",
               7.5, "reg", C["body"], min_size=5.5)
        y += 40


def _results(doc, spec, total):
    ci, fs = spec["case_identification"], spec["financial_summary"]
    pg = Page(doc, 5, total, ci["id"], "04 · The Results")
    y = pg.heading(52, f"Economics · {fs['economic_case'].split(' (')[0]}", "What the recommendation is worth",
                   f"Run-rate benefit {_cad(fs['annual_run_rate_benefit_CAD'])}/yr net of {_cad(fs['annual_om_CAD'])}/yr O&M; "
                   f"levelized {fs['levelized_cost']} {fs['levelized_cost_unit']}.")
    cw = (W - 2 * M - 30) / 4
    for i, (v, l, s, a) in enumerate([(_cad(fs["npv_CAD"]), "Net present value", f"{fs['horizon_years']} yrs @ {fs['wacc_percent']:.1f}%", C["mint"]),
                                      (f"{fs['irr_percent']}%" if fs["irr_percent"] is not None else "n/a", "IRR", "annual", C["mint"]),
                                      (_mo(fs["payback_period_months"]), "Payback", "monthly cash model", C["amber"]),
                                      (f"{fs['benefit_cost_ratio']}x", "Benefit / cost", "present value", C["emerald"])]):
        pg.stat((M + i * (cw + 10), y, M + i * (cw + 10) + cw, y + 64), v, l, s, a)
    y += 84
    pg.text(M, y, "CASH FLOW BY YEAR (BARS) AND CUMULATIVE (LINE)", 7.5, "bold", C["mint"])
    flows = fs["cash_flows_CAD"]
    cum, acc = [], 0
    for f in flows:
        acc += f
        cum.append(acc)
    lo, hi = min(min(flows), min(cum), 0), max(max(flows), max(cum), 1)
    ch_top, ch_bot = y + 22, y + 170
    sc = (ch_bot - ch_top) / (hi - lo)
    zero = ch_bot - (0 - lo) * sc
    pg.p.draw_line((M, zero), (W - M, zero), color=C["border"], width=0.8)
    bw = (W - 2 * M) / len(flows)
    pts = []
    for i, (f, c) in enumerate(zip(flows, cum)):
        x0 = M + i * bw + bw * 0.25
        yv = zero - f * sc
        pg.p.draw_rect(pymupdf.Rect(x0, min(yv, zero), x0 + bw * 0.5, max(yv, zero)), fill=C["mint"] if f >= 0 else C["red"], width=0)
        pg.text(x0, (yv - 4) if f >= 0 else (yv + 10), _cad(f), 6.5, "bold", C["ink"])
        pg.text(x0 + 4, ch_bot + 26, f"Year {i}", 7, "reg", C["muted"])
        pts.append((x0 + bw * 0.25, zero - c * sc))
    for a, b in zip(pts, pts[1:]):
        pg.p.draw_line(a, b, color=C["amber"], width=1.6)
    for pt in pts:
        pg.p.draw_circle(pt, 2.6, fill=C["amber"], color=None)
    y = ch_bot + 46
    half = (W - 2 * M - 16) / 2
    pg.text(M, y, "SCENARIOS", 7.5, "bold", C["mint"])
    yy = y + 8
    for s in spec["scenarios"]:
        ok = s["meets_target"]
        pg.card((M, yy, M + half, yy + 40), stripe=C["mint"] if ok else C["red"])
        pg.box((M + 12, yy + 4, M + half - 6, yy + 18), s["name"], 8, "semi", C["ink"], min_size=6)
        pg.box((M + 12, yy + 18, M + half - 6, yy + 38), f"{s['improvement']:g}% · NPV {_cad(s['npv'])} · payback {_mo(s['payback_months'])} · "
               + ("meets target" if ok else "misses target"), 7.5, "reg", C["body"], min_size=5.5)
        yy += 46
    x1 = M + half + 16
    pg.text(x1, y, "NPV SENSITIVITY (TORNADO)", 7.5, "bold", C["mint"])
    sens = spec["sensitivity"]
    span = max(max(abs(t["low_npv"] - fs["npv_CAD"]), abs(t["high_npv"] - fs["npv_CAD"])) for t in sens) or 1
    mid = x1 + half / 2
    ty = y + 12
    pg.p.draw_line((mid, ty - 2), (mid, ty + len(sens) * 34), color=C["muted"], width=0.6)
    for t in sens:
        lo_w = (t["low_npv"] - fs["npv_CAD"]) / span * (half / 2 - 4)
        hi_w = (t["high_npv"] - fs["npv_CAD"]) / span * (half / 2 - 4)
        for wv, col in ((lo_w, C["red"]), (hi_w, C["mint"])):
            pg.p.draw_rect(pymupdf.Rect(min(mid, mid + wv), ty + 15, max(mid, mid + wv), ty + 25), fill=col, width=0)
        pg.box((x1, ty, x1 + half, ty + 12), t["driver"], 6.8, "reg", C["ink"], min_size=5)
        ty += 34


def _execution(doc, spec, total):
    ci, intel = spec["case_identification"], spec["intelligence"]
    pg = Page(doc, 6, total, ci["id"], "05 · Execution")
    y = pg.heading(52, "30 / 60 / 90 days", "From pilot to control", "One owner per workstream; every phase ends in a go/no-go gate.")
    cw = (W - 2 * M - 20) / 3
    for i, ph in enumerate(intel["plan_30_60_90"]):
        x0 = M + i * (cw + 10)
        pg.card((x0, y, x0 + cw, y + 130), fill=C["pine"] if i == 0 else C["white"], border=C["pine"] if i == 0 else C["border"])
        pg.text(x0 + 12, y + 18, ph["window"].upper(), 7.5, "bold", C["mint_l"] if i == 0 else C["mint"])
        pg.text(x0 + 12, y + 36, ph["focus"], 13, "bold", C["white"] if i == 0 else C["ink"])
        pg.box((x0 + 12, y + 44, x0 + cw - 8, y + 126), "\n".join(f"• {a}" for a in ph["actions"]), 7.8, "reg",
               C["mint_bd"] if i == 0 else C["body"], min_size=5.5)
    y += 146
    pg.text(M, y, "IMPLEMENTATION HORIZONS", 7.5, "bold", C["mint"])
    y += 8
    for h in spec["implementation_horizons"]:
        pg.card((M, y, W - M, y + 38), stripe=C["emerald"])
        pg.box((M + 12, y + 4, M + 210, y + 35), f"{h['horizon']} · {h['timeline']}\n{h['name']}", 8, "semi", C["ink"], min_size=5.5)
        pg.box((M + 215, y + 4, W - M - 70, y + 35), f"KPI: {h['kpi']}\nGate: {h['gate']}", 7.3, "reg", C["body"], min_size=5.5)
        pg.text_right(W - M - 8, y + 22, _cad(h["budget_CAD"]), 9, "bold", C["emerald"])
        y += 43
    y += 10
    half = (W - 2 * M - 16) / 2
    pg.text(M, y, "TOP RISKS", 7.5, "bold", C["mint"])
    ry = y + 8
    for r in spec["risks"][:3]:
        col = C["red"] if r["impact"] in ("High", "Critical") else C["amber"]
        pg.card((M, ry, M + half, ry + 56), stripe=col)
        pg.box((M + 12, ry + 4, M + half - 6, ry + 18), f"{r['risk']}  ({r['likelihood']} / {r['impact']})", 7.8, "semi", C["ink"], min_size=5.5)
        pg.box((M + 12, ry + 18, M + half - 6, ry + 54), f"Mitigation: {r['mitigation']}\nTrigger: {r['trigger']}", 7, "reg", C["body"], min_size=5)
        ry += 62
    x1 = M + half + 16
    pg.text(x1, y, "KPIS: BASELINE → TARGET", 7.5, "bold", C["mint"])
    ky = y + 8
    for k in intel["kpis"]:
        pg.card((x1, ky, W - M, ky + 42))
        pg.box((x1 + 10, ky + 4, W - M - 8, ky + 18), k["kpi"], 8.5, "semi", C["emerald"], min_size=6)
        pg.box((x1 + 10, ky + 19, W - M - 8, ky + 40), f"{k['baseline']}  →  {k['target']}", 8, "reg", C["body"], min_size=5.5)
        ky += 47


def _defence(doc, spec, total):
    ci, intel = spec["case_identification"], spec["intelligence"]
    pg = Page(doc, 7, total, ci["id"], "06 · Defence & Submission")
    y = pg.heading(52, "Before you submit", "Judge questions and the final checklist",
                   f"{len(intel['qa_bank'])} prepared answers, all computed from the model. Answer first, then evidence.")
    half = (W - 2 * M - 12) / 2
    for i, q in enumerate(intel["qa_bank"][:6]):
        x0, y0 = M + (i % 2) * (half + 12), y + (i // 2) * 100
        pg.card((x0, y0, x0 + half, y0 + 92))
        pg.text(x0 + 12, y0 + 14, q.get("category", "Q&A").upper(), 6.5, "bold", C["mint"])
        pg.box((x0 + 12, y0 + 18, x0 + half - 8, y0 + 44), q["question"], 8.2, "semi", C["ink"], min_size=6)
        pg.box((x0 + 12, y0 + 44, x0 + half - 8, y0 + 89), q["rebuttal"], 7.2, "reg", C["body"], min_size=5)
    y += 312
    pg.text(M, y, "PRE-SUBMISSION CHECKLIST", 7.5, "bold", C["mint"])
    y += 8
    for c in intel["submission_checklist"]:
        ok = c["ok"]
        pg.check(M + 7, y + 7, ok)
        pg.box((M + 20, y, M + 270, y + 15), c["item"], 7.8, "semi", C["ink"], min_size=5.5)
        ev = c["evidence"] if len(c["evidence"]) <= 95 else c["evidence"][:92] + "…"
        pg.box((M + 275, y, W - M, y + 15), ev, 7, "reg", C["muted"], min_size=6)
        y += 17
    y += 10
    if intel["similar_competitions"]:
        pg.text(M, y, "WHERE THIS CASE STYLE APPEARS (DIRECTORY-LISTED; WINNERS NOT VERIFIED)", 7.5, "bold", C["mint"])
        x, yy = M, y + 8
        for c in intel["similar_competitions"]:
            label = f"{c['competition']} · {c['region']}"
            if x + pg.width(label, 7, "bold") + 20 > W - M:
                x, yy = M, yy + 19
            x = pg.pill(x, yy, label, C["muted_bg"], C["navy"])


def _package(doc, spec, total):
    """Structured cases: the recommended package, budget check and the case's five-year formula."""
    ci, fs, pack = spec["case_identification"], spec["financial_summary"], spec["case_pack"]
    pg = Page(doc, 0, total, ci["id"], "03b · The Package")
    y = pg.heading(52, "Recommended package", spec["approved_solution"]["name"],
                   "Every initiative has an upfront cost, an ongoing cost and a named owner for its savings.")
    cols = [(M, "INITIATIVE & PURPOSE"), (M + 300, "UPFRONT"), (M + 368, "PER YEAR"), (M + 436, "OWNER")]
    for x, h in cols:
        pg.text(x, y, h, 6.8, "bold", C["mint"])
    y += 6
    for p in pack.get("package", []):
        pg.card((M, y, W - M, y + 37), stripe=C["emerald"])
        pg.box((M + 12, y + 3, M + 292, y + 15), p["initiative"], 8.2, "semi", C["ink"], min_size=6)
        pg.box((M + 12, y + 15, M + 292, y + 36), p["purpose"], 6.6, "reg", C["body"], min_size=5)
        pg.text(M + 300, y + 22, _cad(p["capex"]), 9, "bold", C["emerald"])
        pg.text(M + 368, y + 22, _cad(p["annual_opex"]), 9, "bold", C["amber"])
        pg.box((M + 436, y + 6, W - M - 6, y + 35), p["owner"], 7, "reg", C["body"], min_size=5)
        y += 40
    y += 8
    pg.text(M, y, "BUDGET CHECK", 7.5, "bold", C["mint"])
    y += 10
    bud, inv = fs["budget_CAD"], fs["initial_investment_CAD"]
    pg.p.draw_rect(pymupdf.Rect(M, y, W - M, y + 16), fill=C["muted_bg"], width=0, radius=0.4)
    pg.p.draw_rect(pymupdf.Rect(M, y, M + (W - 2 * M) * min(inv / bud, 1), y + 16), fill=C["mint"], width=0, radius=0.4)
    pg.text(M, y + 28, f"{_cad(inv)} committed ({inv / bud:.0%})", 7.5, "bold", C["pine"])
    pg.text_right(W - M, y + 28, f"{_cad(bud - inv)} headroom · budget {_cad(bud)}", 7.5, "bold", C["emerald"])
    y += 42
    pg.card((M, y, W - M, y + 92), fill=C["pine"], border=C["pine"])
    pg.text(M + 16, y + 20, "FIVE-YEAR NET FINANCIAL IMPACT (CASE FORMULA)", 7.5, "bold", C["mint_l"])
    pg.box((M + 16, y + 26, W - M - 16, y + 52),
           f"{_cad(inv)} + 5 x ({_cad(fs['annual_om_CAD'])} - {_cad(fs['annual_run_rate_benefit_CAD'])}) = {_cad(fs['five_year_net_impact_CAD'])}",
           17, "bold", C["white"], min_size=10)
    pg.box((M + 16, y + 56, W - M - 16, y + 88), f"{fs['five_year_formula']}. Discounted cross-check: NPV {_cad(fs['npv_CAD'])} at "
           f"{fs['wacc_percent']:.1f}%, payback {_mo(fs['payback_period_months'])}.", 8, "reg", C["mint_bd"], min_size=6)
    y += 108
    pg.text(M, y, "DIRECTIONS CONSIDERED · SAME FORMULA", 7.5, "bold", C["mint"])
    y += 8
    for o in spec["options_evaluation"]["options"]:
        if y + 46 > H - 40:
            break
        sel = o["selected"]
        pg.card((M, y, W - M, y + 42), fill=C["mint_bg"] if sel else C["white"], border=C["mint_bd"] if sel else C["border"],
                stripe=C["mint"] if sel else C["muted"])
        pg.box((M + 12, y + 4, M + 330, y + 17), f"Option {o['label']}: {o['name']}", 8, "semi", C["ink"], min_size=6)
        pg.box((M + 12, y + 17, M + 330, y + 40), "Recommended." if sel else f"Set aside: {o.get('why_not') or 'lower score'}", 6.8, "reg",
               C["body"], min_size=5)
        pg.text_right(W - M - 10, y + 18, _cad(o["five_year_net_impact_CAD"]), 12, "bold", C["emerald"] if o["five_year_net_impact_CAD"] < 0 else C["red"])
        pg.text_right(W - M - 10, y + 32, f"upfront {_cad(o['capex_CAD'])}" + ("" if o["within_budget"] else " · over budget"), 6.8, "reg", C["muted"])
        y += 47


def _analysis(doc, spec, total):
    """Structured cases: each required-analysis area from the brief, answered."""
    ci, secs = spec["case_identification"], spec["case_pack"].get("analysis_sections", [])
    pg = Page(doc, 0, total, ci["id"], "05b · Required Analysis")
    y = pg.heading(52, "What the brief asks for", "Required analysis, area by area",
                   "Operations and safety, supply chain, change management, and AI and automation, each answered from the case data.")
    rest = [s for s in secs if s["title"] != "Finance"]
    half = (W - 2 * M - 12) / 2
    rows = (len(rest) + 1) // 2
    ch = (H - 50 - y - (rows - 1) * 10) / max(rows, 1)
    for i, s in enumerate(rest):
        x0, y0 = M + (i % 2) * (half + 12), y + (i // 2) * (ch + 10)
        pg.card((x0, y0, x0 + half, y0 + ch), stripe=C["mint"])
        pg.text(x0 + 14, y0 + 18, s["title"].upper(), 8, "bold", C["emerald"])
        pg.box((x0 + 14, y0 + 26, x0 + half - 10, y0 + ch - 8), "\n".join(f"• {p}" for p in s["points"]), 10, "reg", C["body"], min_size=5, lh=1.35)


def generate_case_study_booklet(spec: dict, out_path: Path) -> Path:
    doc = pymupdf.open()
    structured = spec["case_identification"].get("source_type") == "structured_case"
    FOOTER["text"] = ("Strategy Consulting Hub · Executive Case Simulation Team · "
                      + ("competition brief; estimates are stated assumptions" if structured else "synthetic training case"))
    builders = [_cover, _challenge, _approach, _options, _results, _execution, _defence]
    if spec.get("case_pack"):
        builders.insert(4, _package)
        builders.insert(7, _analysis)
    for b in builders:
        b(doc, spec, len(builders))
    doc.set_metadata({"title": spec["case_identification"]["title"], "author": "Strategy Consulting Hub",
                      "subject": "Case study booklet", "creator": "case_orchestrator"})
    doc.subset_fonts()
    doc.save(str(out_path), garbage=3, deflate=True)
    doc.close()
    return out_path
