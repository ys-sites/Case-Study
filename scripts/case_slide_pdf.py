"""Presentation slides (16:9 PDF) for structured cases, in the house booklet style.

Agenda (numbered from 2 so the pages slot in behind a team's own title and agenda slides):
  2 Problem & why it underperforms · 3 Proposed solution · 4 From congestion to flow · 5 Budget & decision matrix
  6 Financial case · 7 Implementation without disruption (Gantt) · 8 Market analysis · 9 Key risks & mitigation

Design system = Case_Study_Booklet.pdf (case_visual_pdf.py): pine header band, emerald/mint accents, Segoe UI
for structure, Georgia for editorial lines, stat cards and mint kicker labels. Colour tokens are imported, never
redefined. Every text block auto-fits. Data comes from solution_spec.json (`case_pack` holds slide blocks).
"""

from __future__ import annotations

from pathlib import Path

import pymupdf

from case_visual_pdf import C, FONTS as BOOK_FONTS, FALLBACK as BOOK_FALLBACK, FOOTER, _rgb

W, H, M = 960, 540, 42
FONTS = {**BOOK_FONTS, "serif": "C:/Windows/Fonts/georgia.ttf"}
FALLBACK = {**BOOK_FALLBACK, "serif": "tiro"}
KIND = {"plan": _rgb("#CBD5E1"), "build": C["emerald"], "pilot": C["amber"], "rollout": C["mint_l"], "live": C["mint"]}
TOP, BOT = 96, H - 36


def _m(x):
    a = abs(x)
    s = f"${a / 1e6:.1f}M" if a >= 1e6 else f"${a / 1e3:.0f}K" if a >= 1e3 else f"${a:,.0f}"
    return ("-" if x < 0 else "") + s


class Slide:
    def __init__(self, doc, n, total, case_id, section, kicker, title):
        self.p = doc.new_page(width=W, height=H)
        self.fonts = {}
        for name, path in FONTS.items():
            if Path(path).exists():
                self.p.insert_font(fontname=name, fontfile=path)
                self.fonts[name] = (name, path)
            else:
                self.fonts[name] = (FALLBACK[name], None)
        self.p.draw_rect(self.p.rect, fill=C["canvas"], width=0)
        self.p.draw_rect(pymupdf.Rect(0, 0, W, 28), fill=C["pine"], width=0)
        self.text(M, 18, f"{n:02d} · {section.upper()}", 8, "bold", C["mint_l"])
        self.text_r(W - M, 18, f"CASE {case_id}", 8, "bold", C["white"])
        self.text(M, 50, kicker.upper(), 7.5, "bold", C["mint"])
        self.box((M, 54, W - M, 88), title, 22, "bold", C["ink"], min_size=14, lh=1.1)
        self.p.draw_line((M, H - 28), (W - M, H - 28), color=C["border"], width=0.7)
        self.text(M, H - 14, FOOTER["text"], 6.8, "reg", C["muted"])
        self.text_r(W - M, H - 14, f"{n:02d} / {total:02d}", 7.5, "bold", C["emerald"])

    def width(self, s, size, font="reg"):
        name, path = self.fonts[font]
        return (pymupdf.Font(fontfile=path) if path else pymupdf.Font(name)).text_length(s, fontsize=size)

    def text(self, x, y, s, size, font="reg", color=None):
        name, path = self.fonts[font]
        self.p.insert_text((x, y), s, fontname=name, fontfile=path, fontsize=size, color=color or C["body"])

    def text_r(self, x, y, s, size, font="reg", color=None):
        self.text(x - self.width(s, size, font), y, s, size, font, color)

    def text_c(self, x, y, s, size, font="reg", color=None):
        self.text(x - self.width(s, size, font) / 2, y, s, size, font, color)

    def box(self, rect, s, size=10, font="reg", color=None, align=0, min_size=5.5, lh=1.22):
        name, path = self.fonts[font]
        rect, cur = pymupdf.Rect(rect), size
        while cur >= min_size:
            rc = self.p.insert_textbox(rect, s, fontname=name, fontfile=path, fontsize=cur, color=color or C["body"], align=align, lineheight=lh)
            if rc >= 0:
                return rect.y1 - rc
            cur -= 0.5
        self.p.insert_textbox(rect, s[: int(len(s) * 0.6)] + "…", fontname=name, fontfile=path, fontsize=min_size,
                              color=color or C["body"], align=align, lineheight=lh)
        return rect.y1

    def rect(self, r, fill=None, border=None, width=0.7, radius=None):
        self.p.draw_rect(pymupdf.Rect(r), fill=fill, color=border, width=width if border else 0, radius=radius)

    def card(self, r, fill=None, border=None, stripe=None):
        self.rect(r, fill=fill or C["white"], border=border or C["border"], radius=0.05)
        if stripe:
            self.rect((r[0], r[1], r[0] + 3.2, r[3]), fill=stripe)

    def kick(self, x, y, s, color=None):
        self.text(x, y, s.upper(), 7.5, "bold", color or C["mint"])

    def stat(self, r, value, label, sub="", accent=None):
        x0, y0, x1, y1 = r
        accent = accent or C["mint"]
        self.card(r)
        self.rect((x0, y0, x1, y0 + 3), fill=accent)
        self.box((x0 + 9, y0 + 7, x1 - 6, y0 + 27), value, 15, "bold", accent, min_size=9)
        self.box((x0 + 9, y0 + 27, x1 - 6, y0 + 37), label.upper(), 6.4, "bold", C["emerald"], min_size=5)
        if sub:
            self.box((x0 + 9, y0 + 37, x1 - 6, y1 - 3), sub, 6.4, "reg", C["muted"], min_size=5)

    def dashed_v(self, x, y0, y1, color=None):
        for yy in range(int(y0), int(y1), 6):
            self.p.draw_line((x, yy), (x, min(yy + 3, y1)), color=color or C["ink"], width=0.9)

    def diamond(self, x, y, d=5, color=None):
        col = color or C["red"]
        self.p.draw_polyline([(x, y - d), (x + d, y), (x, y + d), (x - d, y), (x, y - d)], color=col, fill=col, width=0.5)


# ------------------------------------------------------------------------------------------ slides
def s_problem(sl, spec):
    pk = spec["case_pack"]
    pr, cz = pk.get("problem", {}), pk.get("causes", {})
    L1, R0 = 452, 472
    sl.card((M, TOP, L1, 160), fill=C["mint_bg"], border=C["mint_bd"], stripe=C["emerald"])
    sl.box((M + 16, TOP + 9, L1 - 10, 156), pk.get("problem_statement", ""), 12.5, "serif", C["ink"], min_size=8, lh=1.3)
    sts = pr.get("stats", [])[:4]
    cw = (L1 - M - 8 * (len(sts) - 1)) / max(len(sts), 1)
    for i, st in enumerate(sts):
        x0 = M + i * (cw + 8)
        sl.stat((x0, 168, x0 + cw, 222), st["value"], st["label"], st.get("sub", ""), C["amber"] if i == 3 else C["mint"])
    ch = pr.get("chart")
    if ch:
        sl.card((M, 230, L1, BOT))
        sl.kick(M + 14, 248, ch["title"])
        lx, gx0, gx1 = M + 14, M + 128, L1 - 16
        vmax = max([b["value"] for b in ch["bars"]] + [l["value"] for l in ch.get("lines", [])]) * 1.04
        sc = (gx1 - gx0) / vmax
        y0, step = 274, 52
        for i, b in enumerate(ch["bars"]):
            y, last = y0 + i * step, i == len(ch["bars"]) - 1
            col = C["mint"] if last else C["red"] if b["value"] >= 100 else C["amber"] if b["value"] > 85 else C["emerald"]
            sl.box((lx, y + 4, gx0 - 6, y + 30), b["label"], 8.5, "semi" if last else "reg", C["ink"], min_size=6.5)
            sl.rect((gx0, y + 4, gx0 + b["value"] * sc, y + 28), fill=col, radius=0.12)
            sl.text(gx0 + 7, y + 20, f"{b['value']:g}{ch.get('unit', '')}", 9.5, "bold", C["white"])
        yb = y0 + len(ch["bars"]) * step - 12
        for k, l in enumerate(ch.get("lines", [])):
            x = gx0 + l["value"] * sc
            sl.dashed_v(x, y0 - 2, yb, C["pine"])
            (sl.text_r if k == 0 else sl.text)(x - 3 if k == 0 else x + 3, y0 - 5, l["label"], 7, "bold", C["pine"])
        sl.box((M + 14, yb + 6, L1 - 14, BOT - 6), pr.get("objectives", ""), 8.2, "semi", C["emerald"], min_size=6)
    # right: cause chain
    sl.kick(R0, TOP + 6, "Why it underperforms: one cause, three mechanisms")
    sl.card((R0, TOP + 12, W - M, 180), fill=C["pine"], border=C["pine"])
    sl.box((R0 + 14, TOP + 20, W - M - 12, 140), cz.get("core", ""), 15, "serif", C["white"], min_size=10)
    sl.box((R0 + 14, 140, W - M - 12, 177), cz.get("core_detail", ""), 7.8, "reg", C["mint_bd"], min_size=6)
    for i, mch in enumerate(cz.get("mechanisms", [])[:3]):
        y = 188 + i * 48
        sl.card((R0, y, W - M, y + 42), stripe=C["emerald"])
        sl.box((R0 + 12, y + 4, W - M - 96, y + 18), mch["name"], 9.5, "bold", C["ink"], min_size=7)
        sl.box((R0 + 12, y + 18, W - M - 96, y + 41), mch["effect"], 7.8, "reg", C["body"], min_size=6)
        sl.rect((W - M - 88, y + 11, W - M - 8, y + 31), fill=C["amber_bg"], radius=0.4)
        sl.box((W - M - 86, y + 15, W - M - 10, y + 30), mch["evidence"], 8, "bold", C["amber"], align=1, min_size=6)
    sl.kick(R0, 344, "Symptoms management sees", C["red"])
    sy = cz.get("symptoms", [])[:6]
    pw = (W - M - R0 - 12) / 3
    for i, t in enumerate(sy):
        x, y = R0 + (i % 3) * (pw + 6), 350 + (i // 3) * 22
        sl.rect((x, y, x + pw, y + 18), fill=C["red_bg"], radius=0.4)
        sl.box((x + 6, y + 3.5, x + pw - 4, y + 17), t, 7.8, "semi", C["red"], align=1, min_size=6)
    sl.card((R0, 400, W - M, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    sl.kick(R0 + 12, 415, "The proof, from the case data")
    sl.box((R0 + 12, 420, W - M - 10, BOT - 4), cz.get("law", ""), 10, "semi", C["ink"], min_size=6.5, lh=1.3)


def s_solution(sl, spec):
    pk, sol, fs = spec["case_pack"], spec["approved_solution"], spec["financial_summary"]
    pills = sol["pillars"][:4]
    cw = (W - 2 * M - 12 * (len(pills) - 1)) / max(len(pills), 1)
    for i, pl in enumerate(pills):
        x0 = M + i * (cw + 12)
        sl.card((x0, TOP, x0 + cw, 366))
        sl.rect((x0, TOP, x0 + cw, TOP + 46), fill=C["pine"], radius=0.05)
        sl.text(x0 + 12, TOP + 14, f"PILLAR {i + 1}", 6.8, "bold", C["mint_l"])
        sl.box((x0 + 12, TOP + 17, x0 + cw - 10, TOP + 45), pl["name"], 11, "bold", C["white"], min_size=7.5)
        y = TOP + 56
        for it in [p for p in pk.get("package", []) if p.get("pillar") == i]:
            sl.box((x0 + 12, y, x0 + cw - 62, y + 26), it["initiative"], 9.5, "semi", C["ink"], min_size=8)
            sl.text_r(x0 + cw - 12, y + 11, _m(it["capex"]), 10.5, "bold", C["emerald"])
            sl.box((x0 + 12, y + 28, x0 + cw - 12, y + 70), it["purpose"], 9.2, "reg", C["body"], min_size=6)
            y += 74
        sl.rect((x0 + 0.7, 326, x0 + cw - 0.7, 365.3), fill=C["mint_bg"])
        sl.text(x0 + 12, 338, "EXPECTED EFFECT", 6.5, "bold", C["mint"])
        sl.box((x0 + 12, 341, x0 + cw - 10, 364), pl["impact"], 8.5, "semi", C["emerald"], min_size=6.5)
    en = [p for p in pk.get("package", []) if p.get("pillar", -1) < 0]
    sl.kick(M, 384, "Enablers")
    x, ew = M, (W - 2 * M - 12 * (len(en) - 1)) / max(len(en), 1)
    for it in en:
        sl.card((x, 390, x + ew, 438), stripe=C["amber"])
        sl.box((x + 12, 394, x + ew - 62, 408), it["initiative"], 9, "semi", C["ink"], min_size=7)
        sl.text_r(x + ew - 12, 405, _m(it["capex"]), 10, "bold", C["amber"])
        sl.box((x + 12, 409, x + ew - 12, 437), it["purpose"], 7.6, "reg", C["body"], min_size=6)
        x += ew + 12
    sl.rect((M, 448, W - M, BOT), fill=C["pine"], radius=0.12)
    sl.box((M + 16, 456, 470, BOT - 4), f"{_m(fs['initial_investment_CAD'])} of {_m(fs['budget_CAD'])} upfront · "
           f"{_m(fs['annual_om_CAD'])}/yr to run · every saving has a named owner", 11, "bold", C["white"], min_size=8)
    sl.box((480, 453, W - M - 14, BOT - 3), "Set aside: " + " · ".join(pk.get("not_chosen", [])), 7.8, "reg", C["mint_bd"], min_size=5.5)


def s_flow(sl, spec):
    bars = spec["case_pack"].get("kpi_bars", [])
    sl.box((M, TOP - 4, W - M, TOP + 12), "Grey = today · green = with the package · dashed line = year-5 objective. All values at +20% volume.",
           8.5, "reg", C["muted"], min_size=7)
    top, rh = TOP + 18, (BOT - TOP - 18) / max(len(bars), 1)
    lx1, gx0, gx1 = 236, 248, 748
    for i, b in enumerate(bars):
        y = top + i * rh
        vmax = max(b["before"], b["after"], b["target"] or 0) * 1.04
        sc = (gx1 - gx0) / vmax
        sl.card((M, y + 1, W - M, y + rh - 3))
        sl.box((M + 12, y + 7, lx1, y + 23), b["label"], 10, "semi", C["ink"], min_size=7.5)
        sl.box((M + 12, y + 23, lx1, y + rh - 5), b.get("note", ""), 7.4, "reg", C["muted"], min_size=6)
        bh = (rh - 16) / 2
        sl.rect((gx0, y + 6, gx0 + b["before"] * sc, y + 6 + bh), fill=_rgb("#CBD5E1"), radius=0.15)
        sl.text(gx0 + b["before"] * sc + 5, y + 4 + bh, f"{b['before']:g}", 8.5, "semi", C["muted"])
        sl.rect((gx0, y + 8 + bh, gx0 + b["after"] * sc, y + 8 + 2 * bh), fill=C["mint"], radius=0.15)
        sl.text_r(gx0 + b["after"] * sc - 5, y + 6 + 2 * bh, f"{b['after']:g}", 8.5, "bold", C["white"])
        if b.get("target"):
            sl.dashed_v(gx0 + b["target"] * sc, y + 3, y + rh - 5, C["pine"])
        chg = (b["after"] - b["before"]) / b["before"] * 100
        sl.rect((768, y + 9, 836, y + rh - 11), fill=C["mint_bg"], radius=0.35)
        sl.text_c(802, y + rh / 2 + 3, f"{chg:+.0f}%", 11, "bold", C["emerald"])
        sl.text(846, y + rh / 2 + 3, b["unit"], 8, "reg", C["muted"])
        if b.get("target"):
            ok = b["after"] <= b["target"]
            sl.rect((880, y + rh / 2 - 7, W - M - 8, y + rh / 2 + 7), fill=C["mint"] if ok else C["red"], radius=0.5)
            sl.text_c((880 + W - M - 8) / 2, y + rh / 2 + 3, "MEETS" if ok else "MISSES", 6.5, "bold", C["white"])


def s_budget(sl, spec):
    pk, fs, ev = spec["case_pack"], spec["financial_summary"], spec["options_evaluation"]
    bud, items = fs["budget_CAD"], pk.get("package", [])
    x1 = 440
    sl.kick(M, TOP + 6, f"Where the {_m(bud)} goes")
    pal = [C["pine"], C["emerald"], C["mint"], C["mint_l"], C["amber"], _rgb("#94A3B8"), _rgb("#CBD5E1")]
    x, sc = M, (x1 - M) / bud
    for i, it in enumerate(items):
        sl.rect((x, TOP + 14, x + it["capex"] * sc, TOP + 40), fill=pal[i % len(pal)])
        x += it["capex"] * sc
    sl.rect((x, TOP + 14, x1, TOP + 40), fill=C["white"], border=C["mint"])
    sl.text_c((x + x1) / 2, TOP + 30, "spare", 7, "bold", C["emerald"])
    y = TOP + 52
    for i, it in enumerate(items):
        sl.rect((M, y + 3, M + 9, y + 12), fill=pal[i % len(pal)])
        sl.box((M + 15, y, 330, y + 15), it["initiative"], 8.6, "reg", C["body"], min_size=6.5)
        sl.text_r(390, y + 10.5, _m(it["capex"]), 9, "bold", C["ink"])
        sl.text_r(x1, y + 10.5, f"{it['capex'] / bud:.0%}", 8.5, "reg", C["muted"])
        y += 20
    sl.p.draw_line((M, y + 2), (x1, y + 2), color=C["border"], width=0.7)
    sl.text(M + 15, y + 17, "Total committed", 9.5, "bold", C["ink"])
    sl.text_r(390, y + 17, _m(fs["initial_investment_CAD"]), 10, "bold", C["emerald"])
    sl.text(M + 15, y + 33, "Unspent headroom", 9.5, "semi", C["muted"])
    sl.text_r(390, y + 33, _m(bud - fs["initial_investment_CAD"]), 10, "bold", C["muted"])
    core = sum(p["capex"] for p in items if p.get("pillar", -1) >= 0)
    sl.card((M, y + 44, x1, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    names = [p_["name"].split(":")[0] for p_ in spec["approved_solution"]["pillars"]]
    by = [(names[i] if i < len(names) else f"Pillar {i + 1}", sum(p["capex"] for p in items if p.get("pillar") == i)) for i in range(len(names))]
    by.append(("Enablers", sum(p["capex"] for p in items if p.get("pillar", -1) < 0)))
    sl.box((M + 12, y + 52, x1 - 10, BOT - 4), f"{core / fs['initial_investment_CAD']:.0%} of the spend goes straight at the core issue.\n"
           + "\n".join(f"{k}: {_m(v)}" for k, v in by)
           + f"\nRunning cost {_m(fs['annual_om_CAD'])} a year: software, support, sensors, analysts and refresher training.",
           11, "semi", C["emerald"], min_size=6.5, lh=1.35)
    mx0 = 470
    sl.kick(mx0, TOP + 6, "Decision matrix (score /10; budget is a hard gate)")
    opts, crit = ev["options"], ev["criteria"]
    cx0 = mx0 + 160
    cw, rh = (W - M - cx0) / len(opts), 27
    for j, o in enumerate(opts):
        xx = cx0 + j * cw
        sl.rect((xx + 2, TOP + 12, xx + cw - 2, TOP + 54), fill=C["pine"] if o["selected"] else C["muted_bg"], radius=0.1)
        sl.box((xx + 6, TOP + 15, xx + cw - 6, TOP + 53), f"{o['label']} · {o['name']}", 7.6, "bold",
               C["white"] if o["selected"] else C["ink"], align=1, min_size=5.5, lh=1.1)
    y = TOP + 58
    for c in crit:
        sl.box((mx0, y + 4, cx0 - 6, y + rh), f"{c['name']} ({c['weight']:.0%})", 8, "reg", C["body"], min_size=6)
        for j, o in enumerate(opts):
            v = o["scores"][c["name"]]
            col = C["emerald"] if v >= 7 else C["mint"] if v >= 5 else C["amber"] if v >= 3 else C["red"]
            xx = cx0 + j * cw
            sl.rect((xx + 2, y, xx + cw - 2, y + rh - 3), fill=col, radius=0.1)
            sl.text_c(xx + cw / 2, y + rh / 2 + 2.5, f"{v:.1f}", 9.5, "bold", C["white"])
        y += rh
    rows = [("Weighted score", lambda o: f"{o['weighted_total']}"), ("Within budget", lambda o: "yes" if o["within_budget"] else "NO"),
            ("Meets year-5 objective", lambda o: "yes" if o["meets_target"] else "no"),
            ("5-year net impact", lambda o: _m(o.get("five_year_net_impact_CAD", 0)))]
    for name, f in rows:
        sl.p.draw_line((mx0, y), (W - M, y), color=C["border"], width=0.6)
        sl.box((mx0, y + 6, cx0 - 6, y + 24), name, 8.6, "bold", C["ink"], min_size=6.5)
        for j, o in enumerate(opts):
            v = f(o)
            bad = v in ("NO", "no") or (v.startswith("$") and name.startswith("5-year"))
            sl.text_c(cx0 + j * cw + cw / 2, y + 17, v, 9.5, "bold", C["red"] if bad else C["emerald"] if o["selected"] else C["ink"])
        y += 24
    win = next(o for o in opts if o["selected"])
    sl.box((mx0, y + 8, W - M, BOT), f"Option {win['label']} is the only direction that meets the objective inside the budget, "
           "and it has the best five-year impact.", 8.8, "semi", C["emerald"], min_size=6.5)


def _fin(spec):
    """Case-formula figures shared by the finance slide and the presenter pages."""
    fs, pk = spec["financial_summary"], spec["case_pack"]
    inv, opex, ben = fs["initial_investment_CAD"], fs["annual_om_CAD"], fs["annual_run_rate_benefit_CAD"]
    f5 = lambda i, o, b: i + 5 * (o - b)  # noqa: E731
    sav = pk.get("savings", [])
    scen = [("Plan", inv, opex, ben)]
    for s in sav:
        scen.append((f"{s['label'].split(' ')[0]} savings halved", inv, opex, ben - s["value"] / 2))
    scen += [("Running cost +50%", inv, opex * 1.5, ben), ("Spend the full budget", fs["budget_CAD"], opex, ben),
             ("All savings halved", inv, opex, ben / 2)]
    return {"inv": inv, "opex": opex, "ben": ben, "net5": f5(inv, opex, ben), "bud": fs["budget_CAD"],
            "scen": [(n, f5(i, o, b)) for n, i, o, b in scen], "breakeven": inv / 5 + opex,
            "payback_yrs": inv / (ben - opex) if ben > opex else None, "sav": sav}


def s_finance(sl, spec):
    pk, fs = spec["case_pack"], spec["financial_summary"]
    F = _fin(spec)
    sl.card((M, TOP - 4, W - M, 150), fill=C["pine"], border=C["pine"])
    sl.kick(M + 16, TOP + 12, "Case formula: five-year net impact = investment + 5 x (added annual costs - annual savings)", C["mint_l"])
    sl.box((M + 16, TOP + 17, W - M - 16, 148), f"{_m(F['inv'])} + 5 x ({_m(F['opex'])} - {_m(F['ben'])}) = {_m(F['net5'])}"
           + ("   net savings" if F["net5"] < 0 else ""), 24, "bold", C["white"], min_size=13)
    # column 1: investment vs budget
    c1 = (M, 330)
    sl.kick(c1[0], 172, "Investment vs budget")
    sc = (c1[1] - c1[0]) / F["bud"]
    sl.rect((c1[0], 178, c1[1], 192), fill=C["muted_bg"], radius=0.4)
    sl.rect((c1[0], 178, c1[0] + F["inv"] * sc, 192), fill=C["mint"], radius=0.4)
    sl.text(c1[0], 204, f"{_m(F['inv'])} of {_m(F['bud'])} · {_m(F['bud'] - F['inv'])} unspent", 8.5, "bold", C["emerald"])
    names = [p_["name"].split(":")[0] for p_ in spec["approved_solution"]["pillars"]]
    items = pk.get("package", [])
    y = 212
    for i, nm in enumerate(names + ["Enablers"]):
        v = sum(p["capex"] for p in items if (p.get("pillar", -1) == i if i < len(names) else p.get("pillar", -1) < 0))
        o = sum(p["annual_opex"] for p in items if (p.get("pillar", -1) == i if i < len(names) else p.get("pillar", -1) < 0))
        sl.box((c1[0], y, c1[0] + 150, y + 15), nm, 8.6, "reg", C["body"], min_size=6.5)
        sl.text_r(c1[0] + 225, y + 10.5, _m(v), 9, "bold", C["ink"])
        sl.text_r(c1[1], y + 10.5, f"{_m(o)}/yr", 8.2, "reg", C["amber"])
        y += 19
    sl.p.draw_line((c1[0], y + 1), (c1[1], y + 1), color=C["border"], width=0.6)
    sl.text(c1[0], y + 15, "Total", 9, "bold", C["ink"])
    sl.text_r(c1[0] + 225, y + 15, _m(F["inv"]), 9.5, "bold", C["emerald"])
    sl.text_r(c1[1], y + 15, f"{_m(F['opex'])}/yr", 9, "bold", C["amber"])
    # column 2: savings with owners
    c2 = (346, 626)
    sl.kick(c2[0], 172, "Annual savings, each with an owner")
    y = 178
    for s in F["sav"]:
        sl.card((c2[0], y, c2[1], y + 64), stripe=C["mint"])
        sl.box((c2[0] + 10, y + 4, c2[1] - 70, y + 18), s["label"], 9.5, "bold", C["ink"], min_size=7)
        sl.text_r(c2[1] - 8, y + 15, _m(s["value"]), 11, "bold", C["emerald"])
        base = f"{_m(s['base'])} x {s['pct']}% · owner: {s['owner']}" if s.get("base") else f"owner: {s['owner']}"
        sl.box((c2[0] + 10, y + 19, c2[1] - 8, y + 31), base, 7.6, "semi", C["emerald"], min_size=6)
        sl.box((c2[0] + 10, y + 31, c2[1] - 8, y + 62), s.get("mechanism", ""), 7.2, "reg", C["body"], min_size=5.5)
        y += 70
    sl.text(c2[0], y + 10, f"Savings {_m(F['ben'])} - running cost {_m(F['opex'])} = {_m(F['ben'] - F['opex'])} a year", 8.8, "bold", C["ink"])
    # column 3: cumulative position (undiscounted)
    cx0, cx1, cy0, cy1 = 640, W - M, 172, 372
    sl.kick(cx0, cy0, "Cumulative position, undiscounted")
    cum = [-F["inv"]] + [-F["inv"] + (F["ben"] - F["opex"]) * k for k in range(1, 6)]
    lo, hi = min(cum + [0]), max(cum + [0])
    sc2 = (cy1 - cy0 - 56) / (hi - lo)
    zero = cy1 - 22 - (0 - lo) * sc2
    sl.p.draw_line((cx0, zero), (cx1, zero), color=C["muted"], width=0.7)
    bw = (cx1 - cx0) / len(cum)
    for k, v in enumerate(cum):
        x = cx0 + k * bw + bw * 0.18
        yv = zero - v * sc2
        sl.rect((x, min(yv, zero), x + bw * 0.64, max(yv, zero)), fill=C["mint"] if v >= 0 else C["red"], radius=0.08)
        sl.text_c(x + bw * 0.32, (yv - 4) if v >= 0 else (yv + 10), _m(v), 7.4, "bold", C["ink"])
        sl.text_c(x + bw * 0.32, cy1 + 2, "Invest" if k == 0 else f"Y{k}", 7.2, "reg", C["muted"])
    # bottom: sensitivity + uncertainty
    sl.kick(M, 396, "Sensitivity, same formula")
    sx0, sx1 = M + 150, 560
    span = max(abs(v) for _, v in F["scen"]) or 1
    y = 402
    for n, v in F["scen"]:
        sl.box((M, y, sx0 - 6, y + 13), n, 8, "semi" if n == "Plan" else "reg", C["ink"], min_size=6)
        w = abs(v) / span * (sx1 - sx0 - 60)
        sl.rect((sx0, y + 1.5, sx0 + w, y + 11.5), fill=C["pine"] if n == "Plan" else C["mint"] if v < 0 else C["red"], radius=0.2)
        sl.text(sx0 + w + 5, y + 10, _m(v), 8, "bold", C["ink"])
        y += 16
    nt = pk.get("finance_notes", {})
    sl.card((580, 392, W - M, BOT), fill=C["amber_bg"], border=C["amber"])
    sl.kick(592, 408, "One financial uncertainty", C["amber"])
    sl.box((592, 413, W - M - 10, BOT - 4), nt.get("uncertainty", "") + f" Break-even needs only {_m(F['breakeven'])} of savings a year"
           + (f"; the investment is paid back in about {F['payback_yrs'] * 12:.0f} months of operation." if F["payback_yrs"] else "."),
           9, "semi", C["ink"], min_size=6.5)


def s_gantt(sl, spec):
    g = spec["case_pack"].get("gantt")
    if not g:
        return
    n_m, streams = g["months"], g.get("streams", {})
    sx0, tx0, gx0, gx1 = M, M + 104, 330, W - M
    mw = (gx1 - gx0) / n_m
    for i, ph in enumerate(g["phases"]):
        x0, x1 = gx0 + (ph["start"] - 1) * mw, gx0 + ph["end"] * mw
        sl.rect((x0 + 1, TOP - 6, x1 - 1, TOP + 8), fill=C["pine"] if i == 1 else C["emerald"], radius=0.25)
        sl.box((x0 + 4, TOP - 4, x1 - 4, TOP + 8), ph["name"], 7.2, "bold", C["white"], align=1, min_size=5.5)
        if i < len(g.get("checkpoints", [])):
            sl.box((x0 + 3, TOP + 10, x1 - 3, TOP + 30), "KPI check: " + g["checkpoints"][i], 6.4, "semi", C["emerald"], align=1, min_size=5)
        sl.rect((x0, TOP + 42, x1, 414), fill=C["mint_bg"] if i != 1 else _rgb("#E2F5EC"))
    sl.text(sx0, TOP + 39, "WORKSTREAM", 6.4, "bold", C["mint"])
    sl.text(tx0, TOP + 39, "ACTIVITY", 6.4, "bold", C["mint"])
    for mth in range(n_m):
        sl.text_c(gx0 + (mth + 0.5) * mw, TOP + 39, f"M{mth + 1}", 7, "bold", C["muted"])
        sl.p.draw_line((gx0 + mth * mw, TOP + 42), (gx0 + mth * mw, 414), color=C["white"], width=0.8)
    rows = g["rows"]
    y_top = TOP + 44
    rh = (414 - y_top) / len(rows)
    prev, first = None, 0
    for i, r in enumerate(rows):
        y = y_top + i * rh
        if r["stream"] != prev:
            sl.p.draw_line((sx0, y), (gx1, y), color=C["border"], width=0.7)
            sl.text(sx0, y + rh * 0.72, r["stream"].upper(), 6.2, "bold", C["emerald"])
            prev, first = r["stream"], i
        elif i == first + 1 and r["stream"] in streams:
            st = streams[r["stream"]]
            sl.text(sx0, y + rh * 0.72, f"{st['owner']} · {_m(st['budget'])}", 6.2, "reg", C["muted"])
        sl.box((tx0, y + 1, gx0 - 6, y + rh + 1), r["task"], 7, "reg", C["body"], min_size=5.2, lh=1.0)
        sl.rect((gx0 + (r["start"] - 1) * mw + 2, y + 2.2, gx0 + r["end"] * mw - 2, y + rh - 2.2), fill=KIND.get(r["kind"], C["mint"]), radius=0.4)
    for ms in g.get("milestones", []):
        x = gx0 + ms["month"] * mw - 1.5
        sl.p.draw_line((x, TOP + 42), (x, 418), color=C["red"], width=1)
        sl.diamond(x, 420)
    xx = sx0
    for k, lab in [("plan", "Plan / review"), ("build", "Build"), ("pilot", "Pilot / shadow"), ("rollout", "Roll out"), ("live", "Live")]:
        sl.rect((xx, 427, xx + 12, 434), fill=KIND[k], radius=0.3)
        sl.text(xx + 16, 433.5, lab, 7, "reg", C["muted"])
        xx += sl.width(lab, 7) + 32
    sl.diamond(xx + 4, 430.5, 4)
    sl.box((xx + 14, 425.5, gx1, 437), "   ".join(f"M{ms['month']}: {ms['label']}" for ms in g.get("milestones", [])), 6.8, "semi", C["red"], min_size=5)
    sl.kick(M, 452, "How operations keep running")
    cont = g.get("continuity", [])
    cw = (W - 2 * M - 8 * (len(cont) - 1)) / max(len(cont), 1)
    for i, c in enumerate(cont):
        x0 = M + i * (cw + 8)
        sl.card((x0, 458, x0 + cw, BOT), stripe=C["emerald"])
        sl.box((x0 + 10, 462, x0 + cw - 6, BOT - 3), c, 7.6, "reg", C["body"], min_size=5.8)


def s_market(sl, spec):
    mk = spec["case_pack"].get("market")
    if not mk:
        return
    sl.box((M, TOP - 4, W - M, TOP + 14), mk["headline"], 10, "serif", C["emerald"], min_size=7.5)
    L1, R0 = 400, 420
    sl.kick(M, TOP + 30, "Market forces")
    fs_ = mk["forces"][:3]
    fh = 62
    for i, f in enumerate(fs_):
        y = TOP + 36 + i * (fh + 6)
        sl.card((M, y, L1, y + fh), stripe=C["mint"])
        sl.box((M + 12, y + 5, L1 - 28, y + 20), f["title"], 10, "bold", C["ink"], min_size=7)
        sl.text_r(L1 - 8, y + 14, f"[{f['src']}]", 7, "bold", C["muted"])
        sl.box((M + 12, y + 21, L1 - 10, y + fh - 3), f["fact"], 8.4, "reg", C["body"], min_size=6)
    y = TOP + 36 + 3 * (fh + 6) + 6
    sl.kick(M, y, "Who is piloting autonomous vehicles")
    for i, b in enumerate(mk["benchmarks"][:2]):
        yy = y + 6 + i * 50
        sl.card((M, yy, L1, yy + 44))
        sl.box((M + 10, yy + 4, M + 120, yy + 42), b["who"], 8.4, "bold", C["emerald"], min_size=6)
        sl.box((M + 124, yy + 4, L1 - 24, yy + 42), f"{b['practice']}. {b['result']}.", 7.6, "reg", C["body"], min_size=5.5)
        sl.text_r(L1 - 6, yy + 13, f"[{b['src']}]", 7, "bold", C["muted"])
    # right: AI AGV pros and cons
    sl.kick(R0, TOP + 30, "AI AGVs: what they can and cannot do  [" + "][".join(str(s) for s in mk.get("agv_src", [])) + "]")
    half = (W - M - R0 - 10) / 2
    for k, (title, key, col, bg) in enumerate([("Pros", "agv_pros", C["emerald"], C["mint_bg"]), ("Cons (go to the risk register)", "agv_cons", C["red"], C["red_bg"])]):
        x0 = R0 + k * (half + 10)
        sl.card((x0, TOP + 36, x0 + half, 330), fill=bg, border=C["mint_bd"] if k == 0 else _rgb("#FCA5A5"))
        sl.text(x0 + 12, TOP + 52, title.upper(), 7.5, "bold", col)
        sl.box((x0 + 12, TOP + 58, x0 + half - 10, 326), "\n".join(f"{'+' if k == 0 else '-'}  {t}" for t in mk.get(key, [])),
               9, "reg", C["ink"], min_size=6, lh=1.35)
    sl.card((R0, 338, W - M, 452), fill=C["pine"], border=C["pine"])
    sl.kick(R0 + 12, 353, "So what for PortFlow", C["mint_l"])
    sl.box((R0 + 12, 358, W - M - 10, 450), "\n".join(f"- {t}" for t in mk["implications"]), 9.2, "reg", C["white"], min_size=6, lh=1.3)
    src = [s for s in mk.get("sources", []) if s.get("url")]
    sl.box((R0, 456, W - M, BOT + 4), "Sources: " + "  ".join(f"[{s['id']}] {s['label']}" for s in src), 5.8, "reg", C["muted"], min_size=4.5, lh=1.1)


def s_risks(sl, spec):
    risks = spec["risks"]
    lv = {"Low": 0, "Medium": 1, "High": 2, "Critical": 2}
    gx0, gy0, cs = M + 30, TOP + 26, 64
    sl.kick(M, TOP + 6, "Risk map: likelihood x impact")
    sev = [C["mint_bg"], _rgb("#E3F3DC"), C["amber_bg"], _rgb("#FDDCC8"), _rgb("#F8B4B4")]
    for i in range(3):
        for j in range(3):
            sl.rect((gx0 + j * cs + 1, gy0 + (2 - i) * cs + 1, gx0 + (j + 1) * cs - 1, gy0 + (3 - i) * cs - 1), fill=sev[i + j])
    for k, lab in enumerate(["Low", "Med", "High"]):
        sl.text_c(gx0 + (k + 0.5) * cs, gy0 + 3 * cs + 11, lab, 7, "reg", C["muted"])
        sl.text_r(gx0 - 4, gy0 + (2 - k + 0.5) * cs + 3, lab, 7, "reg", C["muted"])
    sl.text_c(gx0 + 1.5 * cs, gy0 + 3 * cs + 24, "IMPACT", 6.8, "bold", C["ink"])
    sl.p.insert_text((M + 2, gy0 + 1.5 * cs + 22), "LIKELIHOOD", fontname=sl.fonts["bold"][0], fontfile=sl.fonts["bold"][1],
                     fontsize=6.8, color=C["ink"], rotate=90)
    cell = {}
    for idx, r in enumerate(risks, 1):
        i, j = lv.get(r["likelihood"], 1), lv.get(r["impact"], 1)
        k = cell.get((i, j), 0)
        cell[(i, j)] = k + 1
        cx, cy = gx0 + j * cs + 14 + (k % 3) * 18, gy0 + (2 - i) * cs + 16 + (k // 3) * 20
        sl.p.draw_circle((cx, cy), 8, fill=C["pine"], color=None)
        sl.text_c(cx, cy + 3, str(idx), 8, "bold", C["white"])
    pkg = spec["case_pack"].get("package", [])
    cont = next((p["capex"] for p in pkg if "ontingency" in p["initiative"]), 0)
    chg = next((p for p in pkg if "hange" in p["initiative"]), None)
    note = (f"Risk budget: {_m(cont)} contingency held by the Finance Director"
            + (f", plus {_m(chg['capex'])} upfront and {_m(chg['annual_opex'])}/yr for change management and paid training." if chg else ".")
            + " Each risk has an owner and an early-warning trigger reviewed at the monthly steering meeting.")
    sl.card((M, gy0 + 3 * cs + 34, gx0 + 3 * cs, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    sl.box((M + 10, gy0 + 3 * cs + 40, gx0 + 3 * cs - 8, BOT - 4), note, 10, "semi", C["emerald"], min_size=6, lh=1.3)
    tx0 = gx0 + 3 * cs + 20
    cols = [(tx0, "#"), (tx0 + 18, "RISK"), (tx0 + 150, "MITIGATION"), (tx0 + 370, "OWNER & FUNDING"), (tx0 + 494, "EARLY WARNING")]
    for x, hd in cols:
        sl.text(x, TOP + 6, hd, 7, "bold", C["mint"])
    rh = (BOT - TOP - 12) / max(len(risks), 1)
    for idx, r in enumerate(risks, 1):
        y = TOP + 12 + (idx - 1) * rh
        sl.card((tx0 - 4, y, W - M, y + rh - 3), fill=C["white"] if idx % 2 else C["muted_bg"])
        sl.p.draw_circle((tx0 + 6, y + 12), 7, fill=C["pine"], color=None)
        sl.text_c(tx0 + 6, y + 15, str(idx), 7.5, "bold", C["white"])
        sl.box((tx0 + 18, y + 3, tx0 + 146, y + rh - 5), f"{r['risk']}\n{r['likelihood']} / {r['impact']}", 9.2, "semi", C["ink"], min_size=6)
        sl.box((tx0 + 150, y + 3, tx0 + 366, y + rh - 5), r["mitigation"], 9, "reg", C["body"], min_size=5.5)
        sl.box((tx0 + 370, y + 3, tx0 + 490, y + rh - 5), "\n".join(x for x in (r.get("owner"), r.get("funding")) if x), 8.4, "reg", C["body"], min_size=5.5)
        sl.box((tx0 + 494, y + 3, W - M - 4, y + rh - 5), r["trigger"], 8.8, "semi", C["red"], min_size=5.5)


SLIDES = [
    (s_problem, "Problem & root cause", "The challenge", "PortFlow's problem, and why it underperforms"),
    (s_solution, "Proposed solution", "Recommended package", None),
    (s_flow, "From congestion to flow", "KPI impact at +20% volume", "From congestion to flow: every year-5 objective met"),
    (s_budget, "Budget & decision", "Budget allocation", "Budget allocation and decision matrix"),
    (s_finance, "Financial case", "Finance", "The financial case"),
    (s_gantt, "Implementation", "12 months, three gated phases", "Implementing without disrupting operations"),
    (s_market, "Market analysis", "Market context", "Market analysis: what the industry tells us"),
    (s_risks, "Risks & mitigation", "Employees, AI, partners, money", "Key risks and mitigation"),
]


def generate_slide_pdf(spec: dict, out_path: Path, first_number: int = 2) -> Path | None:
    """Eight agenda slides in the booklet style (numbered from `first_number`); structured cases only."""
    out_path = Path(out_path)
    if not spec.get("case_pack"):
        out_path.unlink(missing_ok=True)
        return None
    FOOTER["text"] = "Strategy Consulting Hub · Executive Case Simulation Team · competition brief; estimates are stated assumptions"
    doc, total = pymupdf.open(), first_number + len(SLIDES) - 1
    for i, (fn, section, kicker, title) in enumerate(SLIDES):
        sl = Slide(doc, first_number + i, total, spec["case_identification"]["id"], section, kicker,
                   title or spec["approved_solution"]["name"])
        fn(sl, spec)
    doc.set_metadata({"title": f"{spec['case_identification']['title']} — presentation slides", "author": "Strategy Consulting Hub",
                      "creator": "case_orchestrator"})
    doc.subset_fonts()
    doc.save(str(out_path), garbage=3, deflate=True)
    doc.close()
    return out_path


def _m2(x):
    """Two-decimal millions so bridge lines add up exactly on screen."""
    return f"${x / 1e6:.2f}M" if abs(x) >= 1e6 else _m(x)


CAT_COL = {"Methods": "emerald", "Technology": "navy", "People": "amber", "External coordination": "mint",
           "Outside our control": "red", "Risk reserve": "muted"}


def _cat_pill(sl, x, y, cat, size=6.6):
    col = C.get(CAT_COL.get(cat, "muted"), C["muted"])
    w = sl.width(cat.upper(), size, "bold") + 12
    sl.rect((x, y, x + w, y + 12), fill=col, radius=0.5)
    sl.text(x + 6, y + 8.6, cat.upper(), size, "bold", C["white"])
    return x + w


def generate_financial_case_pdf(spec: dict, out_path: Path) -> Path | None:
    """Financial case tied to the team's problem framing (targets, VSM stages, fishbone causes): presentable
    slide, savings bridge, investment build-up, robustness, and a presenter card. Booklet style, 16:9."""
    out_path = Path(out_path)
    pk = spec.get("case_pack")
    if not pk or not pk.get("savings_bridge"):
        out_path.unlink(missing_ok=True)
        return None
    FOOTER["text"] = "Strategy Consulting Hub · Executive Case Simulation Team · financial case; estimates are stated assumptions"
    F, fs = _fin(spec), spec["financial_summary"]
    inv, opex, ben, net5, bud = F["inv"], F["opex"], F["ben"], F["net5"], F["bud"]
    bridge, items, nt = pk["savings_bridge"], pk.get("package", []), pk.get("finance_notes", {})
    doc, cid, T = pymupdf.open(), spec["case_identification"]["id"], 5
    over50 = inv * 1.5 + 5 * (opex - ben)
    base = inv - sum(p["capex"] for p in items if "ontingency" in p["initiative"])

    # ---------------------------------------------------------------- 1. the slide
    sl = Slide(doc, 1, T, cid, "Financial case", "Finance · case formula", "The financial case: $14M a year of problems, fixed for $9.4M")
    sl.card((M, TOP - 4, W - M, 146), fill=C["pine"], border=C["pine"])
    sl.kick(M + 16, TOP + 12, "Five-year net impact = investment + 5 x (additional annual costs - annual savings)", C["mint_l"])
    sl.box((M + 16, TOP + 17, W - M - 16, 144), f"{_m(inv)} + 5 x ({_m(opex)} - {_m(ben)}) = {_m(net5)}   net savings",
           23, "bold", C["white"], min_size=13)
    sl.kick(M, 166, "What the money fixes (targets from our problem statement)")
    lk = pk.get("fin_link", [])
    cw = (W - 2 * M - 10 * (len(lk) - 1)) / max(len(lk), 1)
    for i, k in enumerate(lk):
        x0 = M + i * (cw + 10)
        sl.card((x0, 172, x0 + cw, 222))
        sl.rect((x0, 172, x0 + cw, 175), fill=C["mint"])
        sl.box((x0 + 9, 178, x0 + cw - 6, 190), k["label"].upper(), 6.6, "bold", C["emerald"], min_size=5)
        sl.box((x0 + 9, 190, x0 + cw - 6, 206), f"{k['now']}  ->  {k['plan']}", 9.2, "bold", C["ink"], min_size=6.5)
        sl.box((x0 + 9, 207, x0 + cw - 6, 220), f"target {k['target']}", 7.4, "semi", C["mint"], min_size=5.5)
    # left: investment by root cause
    L1 = 468
    sl.kick(M, 240, f"Investment {_m(inv)} of {_m(bud)}, by root cause it fixes")
    y = 248
    for it in items:
        sl.p.draw_line((M, y), (L1, y), color=C["border"], width=0.5)
        _cat_pill(sl, M, y + 4, it.get("category", ""), 5.8)
        sl.box((M + 118, y + 3, L1 - 92, y + 18), it["initiative"], 7.8, "reg", C["body"], min_size=5.8)
        sl.text_r(L1 - 46, y + 12.5, _m(it["capex"]), 8.6, "bold", C["ink"])
        sl.text_r(L1, y + 12.5, f"{_m(it['annual_opex'])}/yr", 7.4, "reg", C["amber"])
        y += 19
    sl.p.draw_line((M, y), (L1, y), color=C["pine"], width=0.8)
    sl.text(M, y + 13, f"Total {_m(inv)} · {_m(bud - inv)} unspent", 8.8, "bold", C["emerald"])
    sl.text_r(L1, y + 13, f"{_m(opex)}/yr", 8.8, "bold", C["amber"])
    sl.box((M, y + 18, L1, BOT), nt.get("cost_note", ""), 6.8, "reg", C["muted"], min_size=5.5)
    # right: savings by root cause
    R0 = 488
    sl.kick(R0, 240, f"Annual savings {_m(ben)}, by root cause removed")
    y = 248
    for pool, val in (("Overtime", 6000000), ("Penalties", 8000000)):
        rows = [b for b in bridge if b["pool"] == pool]
        tot = sum(b["saving"] for b in rows)
        sl.text(R0, y + 10, f"{pool.upper()}  {_m(tot)} of {_m(val)} ({tot / val:.0%})", 7.6, "bold", C["ink"])
        y += 14
        for b in rows:
            _cat_pill(sl, R0, y + 2, b["category"], 5.6)
            sl.box((R0 + 112, y + 1, W - M - 50, y + 15), b["driver"], 7.4, "reg", C["body"] if b["saving"] else C["muted"], min_size=5.5)
            sl.text_r(W - M, y + 10.5, _m2(b["saving"]) if b["saving"] else "not counted", 8.2, "bold", C["emerald"] if b["saving"] else C["muted"])
            y += 16
        y += 4
    sl.card((R0, y + 2, W - M, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    sl.box((R0 + 10, y + 7, W - M - 8, BOT - 3), f"Net {_m(ben - opex)} a year. Payback in about {F['payback_yrs'] * 12:.0f} months; "
           f"break-even needs only {_m(F['breakeven'])} a year.", 12, "semi", C["emerald"], min_size=6.5, lh=1.3)

    # ---------------------------------------------------------------- 2. savings bridge
    sl = Slide(doc, 2, T, cid, "Financial case · savings bridge", "How each saving is estimated",
               "From root cause to dollars: the savings bridge")
    sl.box((M, TOP - 4, W - M, TOP + 12), "Saving = cost pool x share caused by the driver x share our lever removes. Shares and cuts are "
           "stated assumptions, checked against Phase 1 data before the main spend.", 8.6, "reg", C["muted"], min_size=6.5)
    cols = [(M, "FISHBONE CAUSE"), (M + 112, "VSM STAGE"), (M + 206, "DRIVER"), (M + 420, "SHARE OF POOL"),
            (M + 500, "OUR LEVER"), (M + 700, "CUT"), (M + 748, "SAVING"), (M + 808, "OWNER")]
    y = TOP + 24
    for pool, val in (("Overtime", 6000000), ("Penalties", 8000000)):
        rows = [b for b in bridge if b["pool"] == pool]
        tot = sum(b["saving"] for b in rows)
        sl.rect((M, y, W - M, y + 20), fill=C["pine"], radius=0.1)
        sl.text(M + 10, y + 13.5, f"{pool.upper()} · {_m(val)} a year today", 8.4, "bold", C["white"])
        sl.text_r(W - M - 10, y + 13.5, f"saved {_m(tot)} ({tot / val:.0%})", 8.4, "bold", C["mint_l"])
        y += 24
        for x, h in cols:
            sl.text(x, y + 7, h, 6, "bold", C["mint"])
        y += 10
        for b in rows:
            share_val = val * b["share"] / 100
            cut = b["saving"] / share_val if share_val else 0
            sl.card((M, y, W - M, y + 30), fill=C["white"] if b["saving"] else C["muted_bg"])
            _cat_pill(sl, M + 4, y + 9, b["category"], 5.6)
            sl.box((M + 112, y + 4, M + 202, y + 29), b["vsm"], 7.4, "reg", C["body"], min_size=5.5)
            sl.box((M + 206, y + 4, M + 416, y + 29), b["driver"], 7.8, "semi", C["ink"], min_size=5.5)
            sl.box((M + 420, y + 4, M + 496, y + 29), f"{b['share']}% = {_m(share_val)}", 8, "reg", C["body"], min_size=5.5)
            sl.box((M + 500, y + 4, M + 696, y + 29), b["lever"], 7.6, "reg", C["body"], min_size=5.5)
            sl.text(M + 700, y + 18, f"{cut:.0%}" if b["saving"] else "-", 8.6, "bold", C["ink"])
            sl.text(M + 748, y + 18, _m2(b["saving"]) if b["saving"] else "$0", 9, "bold", C["emerald"] if b["saving"] else C["muted"])
            sl.box((M + 808, y + 4, W - M - 4, y + 29), b["owner"], 7, "reg", C["muted"], min_size=5.2)
            y += 33
        y += 6
    sl.box((M, y, W - M, BOT), f"Total {_m(ben)} a year = overtime {_m(sum(b['saving'] for b in bridge if b['pool'] == 'Overtime'))} + "
           f"penalties {_m(sum(b['saving'] for b in bridge if b['pool'] == 'Penalties'))}. Customs holds (40% of penalties) are left out "
           "on purpose because PortFlow cannot override them.", 9, "semi", C["emerald"], min_size=6.5)

    # ---------------------------------------------------------------- 3. investment build-up
    sl = Slide(doc, 3, T, cid, "Financial case · investment", "Upfront cost and running cost",
               "Investment build-up: every dollar aimed at a root cause")
    cols = [(M, "INITIATIVE"), (M + 228, "ROOT CAUSE IT FIXES"), (M + 430, "VSM STAGE"), (M + 552, "UPFRONT"),
            (M + 606, "PER YEAR"), (M + 662, "BASIS OF THE NUMBER")]
    for x, h in cols:
        sl.text(x, TOP + 4, h, 6.4, "bold", C["mint"])
    y = TOP + 10
    for it in items:
        sl.card((M, y, W - M, y + 32))
        sl.box((M + 8, y + 4, M + 224, y + 30), it["initiative"], 8.2, "semi", C["ink"], min_size=6)
        _cat_pill(sl, M + 228, y + 4, it.get("category", ""), 5.6)
        sl.box((M + 228, y + 17, M + 426, y + 31), it.get("fixes", ""), 7.2, "reg", C["body"], min_size=5.5)
        sl.box((M + 430, y + 4, M + 548, y + 30), it.get("vsm", ""), 7.4, "reg", C["body"], min_size=5.5)
        sl.text(M + 552, y + 19, _m(it["capex"]), 9, "bold", C["ink"])
        sl.text(M + 606, y + 19, _m(it["annual_opex"]), 9, "bold", C["amber"])
        sl.box((M + 662, y + 4, W - M - 6, y + 30), it.get("basis", ""), 7.4, "reg", C["muted"], min_size=5.5)
        y += 35
    sl.rect((M, y + 2, W - M, y + 24), fill=C["pine"], radius=0.1)
    sl.text(M + 10, y + 16.5, "TOTAL", 8.6, "bold", C["white"])
    sl.text(M + 552, y + 16.5, _m(inv), 9.5, "bold", C["mint_l"])
    sl.text(M + 606, y + 16.5, _m(opex), 9.5, "bold", C["amber"])
    sl.text(M + 662, y + 16.5, f"{_m(bud - inv)} under the {_m(bud)} budget", 8.6, "bold", C["white"])
    y += 34
    half = (W - 2 * M - 12) / 2
    sl.card((M, y, M + half, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    sl.kick(M + 12, y + 15, "Budget room for cost overruns")
    sl.box((M + 12, y + 20, M + half - 10, BOT - 4), f"Without contingency the package is {_m(base)}. Costs can overrun by "
           f"{_m(bud - base)} ({(bud - base) / base:.0%}) before reaching {_m(bud)}. Phase 1 gets fixed-price vendor quotes first.",
           12, "semi", C["emerald"], min_size=6.5)
    sl.card((M + half + 12, y, W - M, BOT), fill=C["amber_bg"], border=C["amber"])
    sl.kick(M + half + 24, y + 15, "If our cost estimates are wrong", C["amber"])
    sl.box((M + half + 24, y + 20, W - M - 10, BOT - 4), f"Even 50% higher investment ({_m(inv * 1.5)}) still gives {_m(over50)} over "
           "five years: savings drive the result far more than costs do.", 12, "semi", C["ink"], min_size=6.5)

    # ---------------------------------------------------------------- 4. robustness
    sl = Slide(doc, 4, T, cid, "Financial case · robustness", "Stress test", "How robust is the result?")
    scen = F["scen"] + [("Investment +50%", over50)]
    sl.kick(M, TOP + 2, "Same formula, one assumption changed at a time")
    span = max(abs(v) for _, v in scen) or 1
    y, bx0, bx1 = TOP + 10, M + 170, 520
    for n, v in scen:
        sl.box((M, y + 2, bx0 - 8, y + 20), n, 9.4, "semi" if n == "Plan" else "reg", C["ink"], min_size=7)
        w = abs(v) / span * (bx1 - bx0 - 70)
        sl.rect((bx0, y + 3, bx0 + w, y + 19), fill=C["pine"] if n == "Plan" else C["mint"] if v < 0 else C["red"], radius=0.2)
        sl.text(bx0 + w + 6, y + 15, _m(v), 10, "bold", C["ink"])
        y += 26
    sl.card((M, y + 8, 520, BOT), fill=C["mint_bg"], border=C["mint_bd"])
    sl.box((M + 12, y + 14, 510, BOT - 4), f"Every test stays a net saving. Break-even is {_m(F['breakeven'])} of savings a year "
           f"({F['breakeven'] / ben:.0%} of plan). Payback on the case basis is about {F['payback_yrs'] * 12:.0f} months.",
           13, "semi", C["emerald"], min_size=7)
    R0 = 540
    cum = [-inv] + [-inv + (ben - opex) * k for k in range(1, 6)]
    sl.card((R0, TOP - 4, W - M, 300))
    sl.kick(R0 + 12, TOP + 12, "Cumulative position, undiscounted")
    lo, hi = min(cum + [0]), max(cum + [0])
    cy0, cy1, cx0, cx1 = TOP + 20, 280, R0 + 14, W - M - 12
    sc2 = (cy1 - cy0 - 40) / (hi - lo)
    zero = cy1 - 30 - (0 - lo) * sc2
    sl.p.draw_line((cx0, zero), (cx1, zero), color=C["muted"], width=0.7)
    bw = (cx1 - cx0) / len(cum)
    for k, v in enumerate(cum):
        x = cx0 + k * bw + bw * 0.18
        yv = zero - v * sc2
        sl.rect((x, min(yv, zero), x + bw * 0.64, max(yv, zero)), fill=C["mint"] if v >= 0 else C["red"], radius=0.08)
        sl.text_c(x + bw * 0.32, (yv - 4) if v >= 0 else (yv + 10), _m(v), 7.6, "bold", C["ink"])
        sl.text_c(x + bw * 0.32, cy1 + 4, "Invest" if k == 0 else f"Year {k}", 7, "reg", C["muted"])
    sl.card((R0, 310, W - M, BOT), fill=C["amber_bg"], border=C["amber"])
    sl.kick(R0 + 12, 326, "The one financial uncertainty", C["amber"])
    pen_half = next((v for n, v in F["scen"] if n.startswith("Penalties")), None)
    sl.box((R0 + 12, 332, W - M - 10, BOT - 4), nt.get("uncertainty", "") + (f" Even then the result is {_m(pen_half)}." if pen_half else "")
           + " Phase 1 splits the penalty data by cause to confirm it.", 12, "semi", C["ink"], min_size=6.5, lh=1.3)

    # ---------------------------------------------------------------- 5. presenter card
    sl = Slide(doc, 5, T, cid, "Financial case · presenter card", "Get ready to present", "Your 90 seconds, numbers and answers")
    L1 = 470
    sl.card((M, TOP - 4, L1, BOT), fill=C["pine"], border=C["pine"])
    sl.kick(M + 14, TOP + 12, "Script with cues (about 90 seconds)", C["mint_l"])
    cues = ["[point at the formula bar]", "[point at the investment list]", "[point at the savings list]", "[point at the formula bar again]",
            "[close on the robustness line]"]
    lines = [f"{cues[i] if i < len(cues) else ''}\n{t}" for i, t in enumerate(nt.get("script", []))]
    sl.box((M + 14, TOP + 18, L1 - 12, BOT - 6), "\n\n".join(lines), 9.6, "reg", C["white"], min_size=6.5, lh=1.25)
    R0 = L1 + 16
    sl.kick(R0, TOP + 4, "Numbers to know by heart")
    nums = [("Investment", f"{_m(inv)} of {_m(bud)}"), ("Running cost", f"{_m(opex)} a year"),
            ("Savings", f"{_m(ben)} a year"), ("Result", f"{_m(net5)} (net savings)"),
            ("Payback", f"about {F['payback_yrs'] * 12:.0f} months"), ("Break-even", f"{_m(F['breakeven'])} a year")]
    y = TOP + 10
    for i, (k, v) in enumerate(nums):
        x0, yy = R0 + (i % 2) * ((W - M - R0) / 2), y + (i // 2) * 34
        sl.card((x0, yy, x0 + (W - M - R0) / 2 - 6, yy + 30))
        sl.text(x0 + 8, yy + 11, k.upper(), 6.4, "bold", C["mint"])
        sl.text(x0 + 8, yy + 24, v, 9.6, "bold", C["ink"])
    y += 3 * 34 + 8
    sl.kick(R0, y, "Likely judge questions")
    qa = [("Where do the costs come from?", "Our estimates; the case gives none. Phase 1 gets fixed-price quotes, and even +50% costs still save "
           f"{_m(-over50)}."),
          ("Why 40% and 50%?", "Each comes from the savings bridge: cost pool x share caused by a fishbone driver x share our lever removes."),
          ("Why leave customs out?", "PortFlow cannot override customs holds, so we do not claim those savings."),
          ("Why not discount?", "The brief says to ignore discounting; the discounted check is still positive."),
          ("Did you count AGV labour savings?", "No. It is a 2-unit pilot with no layoffs, so any AGV saving is upside.")]
    y += 6
    qh = (BOT - y) / len(qa)
    for q, a in qa:
        sl.card((R0, y, W - M, y + qh - 4), stripe=C["mint"])
        sl.box((R0 + 10, y + 3, W - M - 6, y + 16), q, 9.2, "bold", C["ink"], min_size=6)
        sl.box((R0 + 10, y + 16, W - M - 6, y + qh - 6), a, 9.2, "reg", C["body"], min_size=5.5)
        y += qh

    doc.set_metadata({"title": f"{spec['case_identification']['title']} — financial case", "author": "Strategy Consulting Hub",
                      "creator": "case_orchestrator"})
    doc.subset_fonts()
    doc.save(str(out_path), garbage=3, deflate=True)
    doc.close()
    return out_path
