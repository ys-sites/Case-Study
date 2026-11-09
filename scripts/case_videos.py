"""Three narrated 1080p videos rendered from solution_spec.json.

  01_The_Case.mp4        what the case is and what it is really testing (no answer given away)
  02_How_To_Tackle.mp4   the method: solution model, issue tree, hypothesis, tools, ladder, time plan
  03_Solution_Brief.mp4  the answer, evidence, roadmap, risks, Q&A and the pre-submission checklist

Pipeline per scene: PIL frame (editorial design system) + edge-tts narration -> segment with
fades -> concat. Without network/TTS the videos still render (silent, timed by word count) and
subtitles (.srt) are always written.
"""

from __future__ import annotations

import asyncio
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

VW, VH = 1920, 1080
VOICE = "en-US-ChristopherNeural"
FONT_FILES = {"bold": "C:/Windows/Fonts/segoeuib.ttf", "reg": "C:/Windows/Fonts/segoeui.ttf",
              "semi": "C:/Windows/Fonts/seguisb.ttf", "serif": "C:/Windows/Fonts/georgia.ttf"}
COL = {"pine": (2, 44, 34), "emerald": (6, 78, 59), "card": (9, 61, 47), "mint": (16, 185, 129), "mint_l": (52, 211, 153),
       "mint_bd": (167, 243, 208), "white": (255, 255, 255), "muted": (148, 179, 168), "amber": (245, 158, 11),
       "red": (248, 113, 113), "ink": (15, 23, 42)}
_font_cache: dict = {}


def font(kind: str, size: int):
    key = (kind, size)
    if key not in _font_cache:
        path = FONT_FILES[kind]
        _font_cache[key] = ImageFont.truetype(path, size) if Path(path).exists() else ImageFont.load_default(size)
    return _font_cache[key]


# ---------------------------------------------------------------------------- text helpers
def say_cad(x) -> str:
    if x is None:
        return "not available"
    neg, a = x < 0, abs(x)
    s = f"{a / 1e6:.2f} million dollars" if a >= 1e6 else f"{a / 1e3:,.0f} thousand dollars" if a >= 1e4 else f"{a:,.0f} dollars"
    return ("minus " if neg else "") + s


def short_cad(x) -> str:
    if x is None:
        return "n/a"
    a = abs(x)
    s = f"${a / 1e6:.2f}M" if a >= 1e6 else f"${a / 1e3:.0f}K" if a >= 1e4 else f"${a:,.0f}"
    return ("-" if x < 0 else "") + s


def say_months(x) -> str:
    return f"{x:.0f} months" if x is not None else "more than five years"


def clean(s: str) -> str:
    """Make text speakable: drop symbols TTS mispronounces."""
    s = s.replace(" — ", ", ").replace("—", ", ").replace("–", " to ").replace("→", ", then ").replace("≥", "at least ").replace(">=", "at least ")
    s = re.sub(r"CAD \$?([\d,]+)", lambda m: say_cad(float(m.group(1).replace(",", ""))), s)
    return re.sub(r"\s+", " ", s).strip()


def first_words(s: str, n: int) -> str:
    words = s.split()
    return " ".join(words[:n]) + ("…" if len(words) > n else "")


def wrap(draw, text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            trial = f"{cur} {w}".strip()
            if draw.textlength(trial, font=fnt) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_text(draw, box, text, kind="reg", size=40, min_size=18, color=COL["white"], spacing=1.25, align="left"):
    x0, y0, x1, y1 = box
    while True:
        fnt = font(kind, size)
        lines = wrap(draw, text, fnt, x1 - x0)
        lh = int(size * spacing)
        if len(lines) * lh <= (y1 - y0) or size <= min_size:
            break
        size -= 2
    max_lines = max(1, (y1 - y0) // lh)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,; ") + "…"
    y = y0
    for ln in lines:
        x = x0 if align == "left" else x0 + ((x1 - x0) - draw.textlength(ln, font=fnt)) / 2
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


# ---------------------------------------------------------------------------- frame layouts
class Frame:
    def __init__(self, video_title, case_id, idx, total, kicker, heading):
        self.img = Image.new("RGB", (VW, VH), COL["pine"])
        self.d = ImageDraw.Draw(self.img)
        d = self.d
        d.ellipse((VW - 420, -260, VW + 260, 420), fill=COL["emerald"])
        d.ellipse((VW - 330, -170, VW + 170, 330), outline=COL["mint"], width=3)
        d.text((120, 70), video_title.upper(), font=font("bold", 26), fill=COL["mint_l"])
        d.text((VW - 120 - d.textlength(f"CASE {case_id}", font=font("bold", 26)), 70), f"CASE {case_id}", font=font("bold", 26), fill=COL["white"])
        seg = (VW - 240) / total
        for i in range(total):
            d.rectangle((120 + i * seg + 3, VH - 70, 120 + (i + 1) * seg - 3, VH - 64), fill=COL["mint"] if i <= idx else COL["card"])
        d.text((120, VH - 120), "Strategy Consulting Hub · synthetic training case", font=font("reg", 24), fill=COL["muted"])
        self.top = 150
        if kicker:
            d.text((120, self.top), kicker.upper(), font=font("bold", 28), fill=COL["mint"])
            self.top += 46
        if heading:
            self.top = fit_text(d, (120, self.top, VW - 200, self.top + 170), heading, "bold", 72, 44, spacing=1.1) + 30

    def card(self, box, fill=None, outline=None, stripe=None):
        self.d.rounded_rectangle(box, radius=22, fill=fill or COL["card"], outline=outline, width=3 if outline else 0)
        if stripe:
            self.d.rounded_rectangle((box[0], box[1], box[0] + 10, box[3]), radius=5, fill=stripe)

    def pill(self, x, y, text, fill=COL["mint"], fg=COL["pine"], size=24):
        w = self.d.textlength(text, font=font("bold", size)) + 40
        self.d.rounded_rectangle((x, y, x + w, y + size + 22), radius=(size + 22) // 2, fill=fill)
        self.d.text((x + 20, y + 9), text, font=font("bold", size), fill=fg)
        return x + w + 14

    def check(self, cx, cy, ok, r=22):
        self.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=COL["mint"] if ok else COL["amber"])
        if ok:
            self.d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .38)], fill=COL["pine"], width=6)
        else:
            self.d.line([(cx, cy - r * .5), (cx, cy + r * .12)], fill=COL["pine"], width=6)
            self.d.ellipse((cx - 4, cy + r * .35, cx + 4, cy + r * .35 + 8), fill=COL["pine"])

    # layouts ------------------------------------------------------------
    def title(self, big, sub, tags):
        x = 120
        for t in tags:
            x = self.pill(x, 300, t, COL["emerald"], COL["mint_l"])
        y = fit_text(self.d, (120, 380, VW - 380, 740), big, "bold", 92, 52, spacing=1.08)
        fit_text(self.d, (120, y + 30, VW - 380, 920), sub, "reg", 38, 26, color=COL["mint_bd"])

    def bullets(self, items, size=40):
        y = self.top + 10
        avail = (VH - 170 - y) / max(1, len(items))
        for it in items:
            self.d.ellipse((124, y + size * 0.42, 140, y + size * 0.42 + 16), fill=COL["mint"])
            y = max(fit_text(self.d, (170, y, VW - 200, y + avail - 12), it, "reg", size, 24), y) + 18

    def stats(self, cards, y=None):
        y = y or self.top + 20
        n = len(cards)
        w = (VW - 240 - (n - 1) * 30) / n
        for i, (val, lab, sub, accent) in enumerate(cards):
            x0 = 120 + i * (w + 30)
            self.card((x0, y, x0 + w, y + 270))
            self.d.rectangle((x0 + 20, y, x0 + w - 20, y + 8), fill=accent or COL["mint"])
            fit_text(self.d, (x0 + 34, y + 40, x0 + w - 24, y + 130), val, "bold", 76, 36, color=accent or COL["mint"])
            fit_text(self.d, (x0 + 34, y + 140, x0 + w - 24, y + 180), lab.upper(), "bold", 26, 18, color=COL["white"])
            fit_text(self.d, (x0 + 34, y + 186, x0 + w - 24, y + 260), sub, "reg", 24, 16, color=COL["muted"])
        return y + 270

    def quote(self, text, y=None, h=330):
        y = y or self.top + 10
        self.card((120, y, VW - 120, y + h), fill=COL["emerald"], stripe=COL["mint"])
        fit_text(self.d, (170, y + 40, VW - 170, y + h - 30), f"“{text}”", "serif", 52, 28, spacing=1.3)
        return y + h

    def columns(self, cols, y=None, h=None, highlight=None):
        y = y or self.top + 10
        h = h or (VH - 190 - y)
        n = len(cols)
        w = (VW - 240 - (n - 1) * 26) / n
        for i, (head, body) in enumerate(cols):
            x0 = 120 + i * (w + 26)
            hl = highlight == i
            self.card((x0, y, x0 + w, y + h), fill=COL["mint"] if hl else COL["card"])
            yy = fit_text(self.d, (x0 + 30, y + 30, x0 + w - 26, y + 140), head, "bold", 38, 24, color=COL["pine"] if hl else COL["mint_l"])
            fit_text(self.d, (x0 + 30, yy + 14, x0 + w - 26, y + h - 24), body, "reg", 30, 18, color=COL["pine"] if hl else COL["white"])

    def tree(self, root, branches):
        y = self.top
        self.card((120, y, VW - 120, y + 120), fill=COL["mint"])
        fit_text(self.d, (160, y + 26, VW - 160, y + 110), root, "bold", 40, 24, color=COL["pine"], align="center")
        top = y + 190
        w = (VW - 240 - 2 * 26) / 3
        for i, b in enumerate(branches):
            x0 = 120 + i * (w + 26)
            self.d.line([(VW / 2, y + 120), (x0 + w / 2, top)], fill=COL["mint"], width=4)
            self.card((x0, top, x0 + w, VH - 190), stripe=COL["mint"])
            yy = fit_text(self.d, (x0 + 40, top + 30, x0 + w - 24, top + 120), b["name"], "bold", 38, 24, color=COL["mint_l"])
            fit_text(self.d, (x0 + 40, yy + 10, x0 + w - 24, VH - 210), "\n".join(f"• {q}" for q in b["questions"]), "reg", 30, 18)

    def ladder(self, rungs, show_pick=True):
        n = len(rungs)
        w = (VW - 240 - (n - 1) * 26) / n
        base = VH - 190
        for i, r in enumerate(rungs):
            x0 = 120 + i * (w + 26)
            h = 300 + i * 70
            sel = show_pick and r.get("selected")
            self.card((x0, base - h, x0 + w, base), fill=COL["mint"] if sel else COL["card"])
            fg, sub = (COL["pine"], COL["pine"]) if sel else (COL["white"], COL["muted"])
            fit_text(self.d, (x0 + 30, base - h + 26, x0 + w - 20, base - h + 66), f"{r['level'].upper()} · {r['name'].upper()}", "bold", 24, 16,
                     color=COL["pine"] if sel else COL["mint_l"])
            if show_pick and r.get("option"):
                fit_text(self.d, (x0 + 30, base - h + 76, x0 + w - 20, base - h + 150), f"Option {r['option']}", "bold", 60, 36, color=fg)
                fit_text(self.d, (x0 + 30, base - h + 160, x0 + w - 20, base - 20),
                         f"{r['improvement_percent']:g}% for {short_cad(r['capex_CAD'])}\n{r['rule']}", "reg", 28, 16, color=sub)
            else:
                fit_text(self.d, (x0 + 30, base - h + 80, x0 + w - 20, base - 20), r["rule"] if not show_pick or r.get("option") else r["summary"],
                         "reg", 32, 18, color=sub)

    def bars(self, values, labels, y0=None):
        y0 = y0 or self.top + 20
        y1 = VH - 230
        lo, hi = min(min(values), 0), max(max(values), 1)
        sc = (y1 - y0) / (hi - lo)
        zero = y1 - (0 - lo) * sc
        self.d.line([(120, zero), (VW - 120, zero)], fill=COL["muted"], width=2)
        bw = (VW - 240) / len(values)
        cum, pts = 0, []
        for i, v in enumerate(values):
            x0 = 120 + i * bw + bw * 0.22
            yv = zero - v * sc
            self.d.rectangle((x0, min(yv, zero), x0 + bw * 0.56, max(yv, zero)), fill=COL["mint"] if v >= 0 else COL["red"])
            t = short_cad(v)
            self.d.text((x0, (yv - 44) if v >= 0 else min(yv + 8, y1 - 36)), t, font=font("bold", 30), fill=COL["white"])
            self.d.text((x0, y1 + 14), labels[i], font=font("reg", 26), fill=COL["muted"])

    def checklist(self, items):
        y = self.top
        step = min(64, (VH - 200 - y) / max(1, len(items)))
        for it in items:
            self.check(150, y + step / 2 - 6, it["ok"])
            fit_text(self.d, (200, y, 1060, y + step), it["item"], "semi", 32, 20)
            ev = it["evidence"] if len(it["evidence"]) <= 80 else it["evidence"][:77] + "…"
            fit_text(self.d, (1080, y + 4, VW - 120, y + step), ev, "reg", 24, 16, color=COL["muted"])
            y += step


# ---------------------------------------------------------------------------- scripts
def _scene(kind, kicker, heading, narration, **data):
    return {"kind": kind, "kicker": kicker, "heading": heading, "narration": clean(narration), "data": data}


def script_the_case(spec):
    ci, inp, intel = spec["case_identification"], spec["case_inputs"], spec["intelligence"]
    sq, opts = intel["scqa"], spec["options_evaluation"]["options"]
    unit = inp["baseline_unit"]
    return [
        _scene("title", None, None,
               f"Case {ci['id']}. {ci['title']}. In the next two minutes: the situation, what makes it hard, and what the judges are really testing.",
               big=ci["title"], sub="Video 1 of 3 · What this case is asking", tags=[ci["discipline"], ci["difficulty"], intel["family_label"]]),
        _scene("quote", "Situation", "Where we start", first_words(sq["situation"], 70), text=first_words(sq["situation"], 70)),
        _scene("stats", "Complication", "The gap we have to close",
               f"{inp['baseline_metric']} is {inp['baseline_value']:,.2f} {unit}. The target is a {inp['target_pct']:g} percent improvement, "
               f"within {inp['timeline_months']} months and a capital ceiling of {say_cad(inp['budget'])}.",
               cards=[(f"{inp['baseline_value']:,.0f}", "Baseline", unit, None), (f"{inp['target_pct']:g}%", "Target", inp["target_metric"], None),
                      (short_cad(inp["budget"]), "Budget ceiling", "capital", COL["amber"]), (f"{inp['timeline_months']} mo", "Deadline", "core implementation", None)],
               caption=sq["complication"]),
        _scene("bullets", "Constraints", "What limits the solution space",
               "And there are hard limits. " + " ".join(f"{c}." for c in inp["constraints"][:4]),
               items=inp["constraints"][:5] or ["No additional constraints stated"]),
        _scene("quote", "The question", "What we must decide", sq["question"], text=sq["question"]),
        _scene("columns", "On the table", "Three alternatives",
               "Three alternatives are on the table: " + "; ".join(f"option {o['label']}, {o['name']}" for o in opts) +
               ". Video two shows how to compare them.",
               cols=[(f"Option {o['label']}", o["name"]) for o in opts]),
        _scene("bullets", "What judges test", intel["archetype_name"],
               intel["what_the_case_tests"] + f" The scoring rewards diagnosis, rigour and a defensible recommendation.",
               items=[intel["what_the_case_tests"], f"Solution model: {intel['solution_model']}"] +
                     [f"{k.replace('_', ' ').title()}: {v}%" for k, v in list((inp.get("rubric") or {}).items())[:3]]),
    ]


def script_how_to_tackle(spec):
    ci, inp, intel = spec["case_identification"], spec["case_inputs"], spec["intelligence"]
    tree = intel["issue_tree"]
    steps = [s.strip() for s in intel["solution_model"].split("→")]
    return [
        _scene("title", None, None, f"How to tackle case {ci['id']}. A step-by-step method you can repeat on any case like this one.",
               big="How to tackle this case", sub="Video 2 of 3 · Method before answers", tags=[intel["archetype_name"]]),
        _scene("columns", "Solution model", "The path winning teams follow",
               f"Cases like this follow the {intel['archetype_name'].lower()} model: " + ", then ".join(steps) + ".",
               cols=[(f"Step {i + 1}", s) for i, s in enumerate(steps[:5])]),
        _scene("tree", "Issue tree", "Break the question into three MECE branches",
               f"Start with one question: {tree['root']} Split it into three branches with no overlap: "
               + ", ".join(b["name"] for b in tree["branches"]) + ". Each person on the team owns one branch.",
               root=tree["root"], branches=tree["branches"]),
        _scene("quote", "Hypothesis", "Commit to a guess in the first 20 minutes",
               f"Within twenty minutes, write down a hypothesis you can prove wrong. Here: {intel['hypothesis']} "
               "If the data kills it, pivot and say so. Judges reward honesty.", text=intel["hypothesis"]),
        _scene("columns", "Toolkit", "The tools that fit this problem",
               "Use only the tools that fit. " + ". ".join(intel["toolkit"][:3]) + ". Then do the quick math: " + ". ".join(intel["quick_math"][:2]) + ".",
               cols=[("Tools", "\n".join(f"• {t}" for t in intel["toolkit"])), ("Quick math", "\n".join(f"• {t}" for t in intel["quick_math"]))]),
        _scene("bullets", "Decision rules", "Compare every option on the same basis",
               "Score all three options with explicit weights: target attainment, return, payback, downside resilience and budget headroom. "
               "The budget is a hard gate: an option over budget cannot win.",
               items=[f"{c['name']}: {c['weight']:.0%}" for c in spec["options_evaluation"]["criteria"]] + ["Budget is a hard gate: over-budget options cannot win"]),
        _scene("ladder", "Solution ladder", "Look at four levels before you choose",
               "Then build a solution ladder. Level one, the quick win. Level two, the cheapest option that meets the target. "
               "Level three, the value maximiser. Level four, the stretch. Your recommendation should explain where it sits on this ladder.",
               rungs=intel["solution_ladder"], show_pick=False),
        _scene("columns", "Time plan", "Five hours, five blocks",
               "Finally, protect your time. " + ". ".join(f"{t['time'].replace('–', ' to ')}, {t['step']}" for t in intel["time_plan"]) +
               ". Video three shows the answer this method produces.",
               cols=[(t["time"], f"{t['step']}\n{t['output']}") for t in intel["time_plan"]]),
    ]


def script_solution(spec):
    ci, inp, intel, fs, sol = (spec["case_identification"], spec["case_inputs"], spec["intelligence"],
                               spec["financial_summary"], spec["approved_solution"])
    opts = spec["options_evaluation"]["options"]
    win = next(o for o in opts if o["selected"])
    bear = spec["scenarios"][0]
    top = spec["sensitivity"][0]
    warn = [c for c in intel["submission_checklist"] if not c["ok"]]
    qa = intel["qa_bank"][:3]
    return [
        _scene("title", None, None, f"The solution to case {ci['id']}, and everything to check before you submit.",
               big=f"Option {win['label']}: {win['name']}", sub="Video 3 of 3 · The answer and the pre-submission brief", tags=["Recommendation"]),
        _scene("stats", "Answer first", f"Recommend Option {win['label']}",
               f"Our answer: option {win['label']}, {win['name']}. It delivers {win['improvement_percent']:g} percent against a target of "
               f"{inp['target_pct']:g} percent, for {say_cad(win['capex_CAD'])} of a {say_cad(inp['budget'])} budget.",
               cards=[(f"{win['improvement_percent']:g}%", "Improvement", f"target {inp['target_pct']:g}%", None),
                      (short_cad(win["capex_CAD"]), "Capital", f"of {short_cad(inp['budget'])}", COL["amber"]),
                      (short_cad(fs["npv_CAD"]), "NPV", f"{fs['wacc_percent']:.1f}% WACC", None),
                      (f"{fs['payback_period_months']:.0f} mo" if fs["payback_period_months"] else "> 60 mo", "Payback", "monthly model", None)],
               caption=intel["ladder_rationale"]),
        _scene("ladder", "Why this option", "Where it sits on the solution ladder", intel["ladder_rationale"], rungs=intel["solution_ladder"], show_pick=True),
        _scene("bars", "Economics", f"Five-year cash flow · NPV {short_cad(fs['npv_CAD'])}",
               f"The economics: a run-rate benefit of {say_cad(fs['annual_run_rate_benefit_CAD'])} a year, net present value of {say_cad(fs['npv_CAD'])}, "
               f"and payback in {say_months(fs['payback_period_months'])}. "
               + ("This is a mandate-driven case, so judge it on cost per unit delivered, not profit alone." if fs["economic_case"].startswith("mandate") else ""),
               values=fs["cash_flows_CAD"], labels=[f"Year {i}" for i in range(len(fs["cash_flows_CAD"]))]),
        _scene("stats", "Stress test", "What happens when the numbers move",
               f"Now stress it. If performance falls fifteen percent and costs rise twenty, the gain is {bear['improvement']:g} percent and NPV is "
               f"{say_cad(bear['npv'])}. {'The target still holds.' if bear['meets_target'] else 'The target would be missed, which is why the pilot gate comes first.'} "
               f"The most sensitive driver is {top['driver'].split(' (')[0].lower()}.",
               cards=[(f"{s['improvement']:g}%", s["name"].split(" (")[0], f"NPV {short_cad(s['npv'])}", COL["mint"] if s["meets_target"] else COL["red"])
                      for s in spec["scenarios"]],
               caption=f"Most sensitive driver: {top['driver']}. NPV ranges {short_cad(top['low_npv'])} to {short_cad(top['high_npv'])}."),
        _scene("columns", "Roadmap", "30 / 60 / 90 days",
               " ".join(f"{p['window'].replace('–', ' to ')}: {p['focus']}. {p['actions'][0]}." for p in intel["plan_30_60_90"]),
               cols=[(f"{p['window']} · {p['focus']}", "\n".join(f"• {a}" for a in p["actions"])) for p in intel["plan_30_60_90"]], highlight=0),
        _scene("columns", "Risks", "Top three risks and their triggers",
               "The three risks to manage: " + ". ".join(f"{r['risk']}, mitigated by {r['mitigation'].split(';')[0].lower()}" for r in spec["risks"][:3]) + ".",
               cols=[(r["risk"], f"Mitigation: {r['mitigation']}\n\nTrigger: {r['trigger']}") for r in spec["risks"][:3]]),
        _scene("columns", "Judge Q&A", "Questions you will be asked",
               " ".join(f"Question: {q['question']} Answer: {q['rebuttal']}" for q in qa[:2]),
               cols=[(q["question"], q["rebuttal"]) for q in qa]),
        _scene("checklist", "Before you submit", "Pre-submission checklist",
               f"Before you submit, run the checklist. {sum(c['ok'] for c in intel['submission_checklist'])} of "
               f"{len(intel['submission_checklist'])} items are ready. "
               + (" Still open: " + "; ".join(c["item"].lower() for c in warn) + ". Replace the assumptions with real data if you can, "
                  "or state them clearly on an appendix slide." if warn else " Everything is ready."),
               items=intel["submission_checklist"]),
        _scene("title", None, None,
               f"Lead with the answer, prove it with three numbers, and own the risks. Option {win['label']}. Good luck.",
               big="Lead with the answer.", sub=f"Option {win['label']} · {short_cad(fs['npv_CAD'])} NPV · {win['improvement_percent']:g}% vs {inp['target_pct']:g}% target",
               tags=["Ready to present"]),
    ]


VIDEOS = [("01_The_Case", "The Case", script_the_case), ("02_How_To_Tackle", "How to Tackle", script_how_to_tackle),
          ("03_Solution_Brief", "Solution & Submission Brief", script_solution)]


# ---------------------------------------------------------------------------- rendering
def render_frame(scene, video_title, case_id, idx, total) -> Image.Image:
    f = Frame(video_title, case_id, idx, total, scene["kicker"], scene["heading"])
    k, dd = scene["kind"], scene["data"]
    if k == "title":
        f.title(dd["big"], dd["sub"], dd["tags"])
    elif k == "quote":
        f.quote(dd["text"])
    elif k == "stats":
        y = f.stats(dd["cards"])
        if dd.get("caption"):
            f.card((120, y + 40, VW - 120, VH - 170), fill=COL["emerald"], stripe=COL["mint"])
            fit_text(f.d, (170, y + 75, VW - 170, VH - 200), dd["caption"], "serif", 40, 22, spacing=1.3)
    elif k == "bullets":
        f.bullets(dd["items"])
    elif k == "columns":
        f.columns(dd["cols"], highlight=dd.get("highlight"))
    elif k == "tree":
        f.tree(dd["root"], dd["branches"])
    elif k == "ladder":
        f.ladder(dd["rungs"], dd["show_pick"])
    elif k == "bars":
        f.bars(dd["values"], dd["labels"])
    elif k == "checklist":
        f.checklist(dd["items"])
    return f.img


async def _tts_all(jobs):
    import edge_tts
    for text, out in jobs:
        await edge_tts.Communicate(text, VOICE, rate="+4%").save(str(out))


def _duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def _srt_time(t):
    return f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{int(t % 60):02},{int(round((t % 1) * 1000)) % 1000:03}"


def render_video(spec: dict, out_dir: Path, slug: str, title: str, scenes: list[dict], tts: bool = True) -> dict:
    work = out_dir / "source_project" / slug
    work.mkdir(parents=True, exist_ok=True)
    case_id = spec["case_identification"]["id"]
    audio_ok = False
    if tts:
        try:
            asyncio.run(_tts_all([(s["narration"], work / f"scene_{i:02d}.mp3") for i, s in enumerate(scenes)]))
            audio_ok = all((work / f"scene_{i:02d}.mp3").stat().st_size > 1000 for i in range(len(scenes)))
        except Exception as e:  # offline or service error: fall back to silent timed video
            print(f"[Agent 13] TTS unavailable ({type(e).__name__}); rendering silent video with subtitles")
    segs, cues, t = [], [], 0.0
    for i, s in enumerate(scenes):
        frame = work / f"scene_{i:02d}.png"
        render_frame(s, title, case_id, i, len(scenes)).save(frame)
        mp3 = work / f"scene_{i:02d}.mp3"
        speech = _duration(mp3) if audio_ok else len(s["narration"].split()) / 2.6
        dur = round(speech + 1.0, 2)
        seg = work / f"seg_{i:02d}.mp4"
        audio_in = ["-i", str(mp3)] if audio_ok else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", str(frame), *audio_in,
               "-filter_complex", f"[0:v]fade=t=in:st=0:d=0.35,fade=t=out:st={dur - 0.35}:d=0.35,format=yuv420p[v];"
                                  f"[1:a]adelay=350|350,apad,atrim=0:{dur},aresample=48000[a]",
               "-map", "[v]", "-map", "[a]", "-t", str(dur), "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
               "-crf", "20", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(seg)]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        segs.append(seg)
        sentences = [x for x in re.split(r"(?<=[.!?])\s+", s["narration"]) if x]
        total_chars = sum(len(x) for x in sentences) or 1
        st = t + 0.35
        for sent in sentences:
            d = speech * len(sent) / total_chars
            cues.append((st, st + d, sent))
            st += d
        t += dur
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in segs), encoding="utf-8")
    mp4 = out_dir / f"{slug}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst.name, "-c", "copy",
                    "-movflags", "+faststart", str(mp4.resolve())], cwd=work, check=True, capture_output=True, text=True)
    (out_dir / f"{slug}.srt").write_text("\n".join(f"{n + 1}\n{_srt_time(a)} --> {_srt_time(b)}\n{txt}\n" for n, (a, b, txt) in enumerate(cues)),
                                         encoding="utf-8")
    (out_dir / f"{slug}_script.md").write_text(f"# {title}\n\n" + "\n\n".join(
        f"**{i + 1}. {s['heading'] or s['data'].get('big', '')}**\n{s['narration']}" for i, s in enumerate(scenes)), encoding="utf-8")
    for p in segs + [lst]:  # keep frames + narration audio, drop intermediate segments
        p.unlink(missing_ok=True)
    return {"file": mp4.name, "duration_s": round(t, 1), "scenes": len(scenes), "narrated": audio_ok}


def render_all(spec: dict, out_dir: Path, tts: bool = True, render: bool = True) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for slug, title, fn in VIDEOS:
        scenes = fn(spec)
        if not render or not shutil.which("ffmpeg"):
            (out_dir / f"{slug}_script.md").write_text(f"# {title}\n\n" + "\n\n".join(s["narration"] for s in scenes), encoding="utf-8")
            results.append({"file": None, "scenes": len(scenes), "narrated": False})
            continue
        results.append(render_video(spec, out_dir, slug, title, scenes, tts))
    (out_dir / "videos.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results
