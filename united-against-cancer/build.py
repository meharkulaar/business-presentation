#!/usr/bin/env python3
"""Build the self-contained deck and speaker notes from src/.

    python3 build.py          -> index.html, speaker-notes.md
    node export.js            -> deck.pdf (+ QA screenshots with --qa)
"""
import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build_html():
    text = (SRC / "deck.html").read_text(encoding="utf-8")
    fonts = SRC / "fonts"
    subs = {
        "FONT_GLOOCK": b64(fonts / "gloock-latin-400-normal.woff2"),
        "FONT_FIG400": b64(fonts / "figtree-latin-400-normal.woff2"),
        "FONT_FIG500": b64(fonts / "figtree-latin-500-normal.woff2"),
        "FONT_FIG600": b64(fonts / "figtree-latin-600-normal.woff2"),
        "FORESTERS_LOGO": "data:image/webp;base64," + b64(SRC / "foresters-logo.webp"),
        "WFG_LOGO": "data:image/png;base64," + b64(SRC / "wfg-logo.png"),
    }
    for key, value in subs.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[A-Z_0-9]+\}\}", text)
    if leftover:
        raise SystemExit(f"Unfilled template keys: {leftover}")
    if re.search(r"""(src|href)=["']https?://""", text):
        raise SystemExit("External URL found; the deck must run offline")
    (ROOT / "index.html").write_text(text, encoding="utf-8")
    return text


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


TIMING = """| Slides | Segment | Speaker | Minutes | Finish by |
| --- | --- | --- | --- | --- |
| 1–2 | Welcome and reflection | Host | 2 | 2:00 |
| 3–12 | Cancer by the numbers | Host | 6 | 8:00 |
| 13 | Foresters Financial | Foresters partner | 2 | 10:00 |
| 14 | The preparedness gap | Host | 1 | 11:00 |
| 15 | Today's 8 challenges | Host | 2 | 13:00 |
| 16 | Add a cancer diagnosis | Host | 1 | 14:00 |
| 17 | Live client story | Client on Zoom | 4 | 18:00 |
| 18–20 | Prepared vs unprepared family | Host | 2 | 20:00 |
| 21–22 | Mission and transition | Host | 1 | 21:00 |
| | **Total** | | **21** | |
"""

KEYS = """| Key | Action |
| --- | --- |
| Right, Down, Space, PageDown | Next build step, then next slide |
| Left, Up, PageUp | Back one step |
| S | Presenter view (current and next, notes, timers) |
| E | Edit mode: click any text to change it; Save copy downloads an edited file |
| T | Table of contents (button at top right); the eye icon on each row hides or shows that slide |
| + / − / 0 | Zoom in, out, reset |
| Caps Lock | Laser pointer |
| Gear (bottom left) | Full screen, restart, presenter view, edit mode, motion, zoom |
| A | Reveal every build on the current slide |
| G, then number, then Enter | Go to slide |
| Z | Jump to the live Zoom story slide |
| B / W | Black screen / resume |
| F | Fullscreen |
| M | Motion on or off |
| ? | Key help |
"""


def build_notes(text):
    out = [
        "# United Against Cancer · Part 1 speaker notes",
        "",
        "November 1, 2026 · Team ALL IN with Foresters Financial · 25 minutes",
        "",
        "## Timing",
        "",
        TIMING,
        "## Keys",
        "",
        KEYS,
        "## Slides",
        "",
    ]
    sections = re.findall(r'<section class="slide[^"]*"([^>]*)>(.*?)</section>', text, re.S)
    for n, (attrs, body) in enumerate(sections, 1):
        a = {k: html.unescape(v) for k, v in re.findall(r'data-([a-z]+)="([^"]*)"', attrs)}
        heading = re.search(r"<h[12][^>]*>(.*?)</h[12]>", body, re.S)
        title = a.get("title") or (strip_tags(heading.group(1)) if heading else f"Slide {n}")
        notes = re.search(r'<aside class="notes">(.*?)</aside>', body, re.S)
        steps = int(a.get("steps", "0"))
        out.append(f"### {n}. {title}")
        out.append("")
        out.append(f"*{a.get('who', '')} · {a.get('seg', '')} · "
                   f"{steps} click{'s' if steps != 1 else ''} · finish by {a.get('end', '')}:00*")
        out.append("")
        if notes:
            for line in strip_tags(notes.group(1)).splitlines():
                line = line.strip()
                if line:
                    out.append(line)
                    out.append("")
        src = re.search(r'<p class="source">(.*?)</p>', body, re.S)
        if src:
            out.append(f"> {strip_tags(src.group(1))}")
            out.append("")
    out += [
        "## Sources",
        "",
        "- Canadian Cancer Society, Canadian Cancer Statistics 2025 (42% lifetime probability of diagnosis, about 2 in 5; 22% lifetime probability of dying from cancer): https://cancer.ca/en/research/cancer-statistics",
        "- Brenner et al., “Projected estimates of cancer in Canada in 2026”, CMAJ 198(14), April 13, 2026 (254,100 new cases and 87,900 deaths; lung 32,900, breast 32,700, prostate 29,300, colorectal 25,300 new cases; top four = 47%; lung 19,300, colorectal 9,200, pancreas 6,500 deaths): https://www.cmaj.ca/content/198/14/E526",
        "- Canadian Cancer Society, Bladder cancer statistics (12,600 new cases estimated for 2025; fifth most common cancer): https://cancer.ca/en/cancer-information/cancer-types/bladder/statistics",
        "- Statistics Canada, Leading causes of death, 2023, released March 5, 2025 (malignant neoplasms 84,629 deaths, rank 1; diseases of the heart 57,890, rank 2): https://www150.statcan.gc.ca/n1/daily-quotidien/250305/t001a-eng.htm",
        "- Canadian Cancer Statistics 2021 release notice, Public Health Agency of Canada (about 64% five-year net survival): https://www.canada.ca/en/public-health/services/reports-publications/health-promotion-chronic-disease-prevention-canada-research-policy-practice/vol-41-no-11-2021/canadian-cancer-statistics-2021.html",
        "- Canadian Cancer Society and Angus Reid Institute survey, February 4, 2025 (nearly $33,000; 80%, 66%, 28%; Steven Hodges's story): https://cancer.ca/en/about-us/media-releases/2025/new-canadian-cancer-society-survey-reveals-working-age",
        "- iA Financial Group, Transition critical illness insurance client guide (F13-1195A): distribution of critical illness claims paid, cancer 69%, heart attack 10%, stroke 4%, citing the Munich Re individual insurance survey, 2022; cancer, heart attack, stroke and coronary bypass = 85% of claims paid. “All other illnesses” (17%) is the remainder: https://ia.ca/individuals/-/media/files/ia/formulaires/assind/en/f13-1195a-transition-client-guide_20230518.pdf",
        "- Canadian Cancer Society, Prostate cancer statistics (2025: about 1 in 9 men; 30,400 diagnosed; 5,200 deaths; second leading cause of cancer death in men): https://cancer.ca/en/cancer-information/cancer-types/prostate/statistics",
        "- Canadian Cancer Society, Breast cancer statistics (about 1 in 8 women; 2026: 32,400 diagnosed, about 89 a day; 5,400 deaths, about 15 a day; 89% five-year net survival): https://cancer.ca/en/cancer-information/cancer-types/breast/statistics",
        "- Public Health Agency of Canada, Cancer in Young People in Canada program (925 to 1,000 children under 15 diagnosed each year; about 84% five-year survival): https://www.canada.ca/en/public-health/services/chronic-diseases/cancer/cancer-young-people-canada-program.html",
        "- Public Health Agency of Canada, Trends in the incidence of childhood cancer in Canada, 1992–2006 (cancer is the leading cause of disease-related death in children aged 1 to 14): https://www.canada.ca/en/public-health/services/reports-publications/health-promotion-chronic-disease-prevention-canada-research-policy-practice/vol-32-no-3-2012/trends-incidence-childhood-cancer-canada-1992-2006.html",
        "- Canadian Institute of Actuaries, Critical illness morbidity study, policy years 2012–2020, 11 insurers including iA (cancer 67% of claims by lives insured; average benefit paid $86,518), as reported by Insurance Portal: https://insurance-portal.ca/article/critical-illness-insurance-cancer-and-heart-attack-dominate-claims/",
        "- iA Financial Group, Transition (25 critical illnesses and 5 childhood illnesses covered): https://ia.ca/individuals/insurance/health-disability-insurance/critical-illness-insurance/transition-en",
        "- Manulife, Lifecheque covered conditions (up to 25 conditions): https://www.manulife.ca/personal/support/insurance/lifecheque-covered-conditions.html",
        "- Foresters Financial, Canada Protection Plan critical illness advisor brochure (top 8 conditions covered make up more than 90% of critical illness claims): https://ezbizcanada.foresters.com/-/media/ezbiz-ca/documents/english/critical-illness-insurance/506591-can-1025-cpp-critical-illness-insurance-advisor-brochure.pdf",
        "- Equitable, EquiLiving critical illness insurance, advisor piece 1828_EN (2026/03/15): Equitable claims data January 2013 to December 2025 (average claim $70,600; average age at claim 49; 60% of claimants aged 30 to 55; example claims by age). Also cites Heart and Stroke Foundation (a stroke every 5 minutes; 80% of stroke survivors live with impairment). Marked “Advisor use only”.",
        "- Equitable, EquiLiving Critical Illness Insurance for children, 1287 (2023/07/20): 26 adult conditions plus 5 childhood conditions covered to age 25; 1 in 3,600 children born in Canada has cystic fibrosis (Cystic Fibrosis Canada).",
        "- Canada Life client story, “Anyone can get sick: Sandra's story” (Sandra and Warren). The original page is no longer online; confirm with the partner before showing names.",
        "",
        "### Fact-check notes",
        "",
        "- “1 in 2 Canadians will develop cancer” and “1 in 4 will die from cancer” are from Canadian Cancer Statistics 2017. The current estimates are 42% (about 2 in 5) and 22% (more than 1 in 5), which the deck uses.",
        "- Cancer is the leading cause of death in Canada (Statistics Canada, 2023).",
        "- Nearly 700 diagnoses a day is 254,100 ÷ 365 ≈ 696.",
        "- Prostate: “1 in 8 men” is the 2024 figure; the Canadian Cancer Society's 2025 figure is about 1 in 9.",
        "- Childhood: the national count is a range (925 to 1,000 a year); the slide says “up to 1,000”. The leading-cause finding comes from a 2012 PHAC analysis of 1992–2005 deaths.",
        "- Critical illness benefits are generally tax-free when the policy is personally owned and premiums are paid personally.",
        "",
    ]
    (ROOT / "speaker-notes.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    t = build_html()
    build_notes(t)
    print(f"index.html {len(t) / 1024:.0f} KB, speaker-notes.md written")
