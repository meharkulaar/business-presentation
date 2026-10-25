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
| 3–8 | Cancer by the numbers | Host | 3 | 5:00 |
| 9 | Foresters Financial | Foresters partner | 2 | 7:00 |
| 10 | The preparedness gap | Host | 2 | 9:00 |
| 11 | Today's 8 challenges | Host | 4 | 13:00 |
| 12 | Amplified 10x | Host | 2 | 15:00 |
| 13 | Live client story | Client on Zoom | 6 | 21:00 |
| 14–16 | Prepared vs unprepared family | Host | 2 | 23:00 |
| 17–18 | Mission and transition | Host | 2 | 25:00 |
| | **Total** | | **25** | |
"""

KEYS = """| Key | Action |
| --- | --- |
| Right, Down, Space, PageDown | Next build step, then next slide |
| Left, Up, PageUp | Back one step |
| S | Presenter view (current and next, notes, timers) |
| E | Edit mode: click any text to change it; Save copy downloads an edited file |
| T | Table of contents (also the button at top right) |
| + / − / 0 | Zoom in, out, reset |
| Caps Lock | Laser pointer |
| Gear (bottom left) | Full screen, restart, presenter view, edit mode, motion, zoom |
| A | Reveal every build on the current slide |
| G, then number, then Enter | Go to slide |
| Z | Jump to the live Zoom slide (13) |
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
        "- Canadian Cancer Society, Cancer statistics, and Canadian Cancer Statistics 2025 (42% lifetime probability, about 2 in 5): https://cancer.ca/en/research/cancer-statistics",
        "- Brenner et al., “Projected estimates of cancer in Canada in 2026”, CMAJ 198(14), April 13, 2026 (254,100 new cases and 87,900 deaths projected for 2026): https://www.cmaj.ca/content/198/14/E526",
        "- Canadian Cancer Statistics 2021 release notice, Public Health Agency of Canada (about 64% five-year net survival): https://www.canada.ca/en/public-health/services/reports-publications/health-promotion-chronic-disease-prevention-canada-research-policy-practice/vol-41-no-11-2021/canadian-cancer-statistics-2021.html",
        "- Canadian Cancer Society and Angus Reid Institute survey, February 4, 2025 (nearly $33,000; 80%, 66%, 28%; Steven Hodges's story): https://cancer.ca/en/about-us/media-releases/2025/new-canadian-cancer-society-survey-reveals-working-age",
        "- RBC Insurance poll conducted by Ipsos, 2,001 Canadians aged 18+, August 18–21, 2025 (9% have critical illness insurance; 57% worried about serious illness): https://www.rbcinsurance.com/en-ca/advice-learning/newsroom/whats-the-plan-when-life-happens-most-canadians-dont-have-one-rbc-insurance-poll/",
        "- RBC Emergency Readiness Poll, July 16, 2026 (32% have no emergency fund; 38% for households under $100,000; 76% cite cost of living): https://www.newswire.ca/news-releases/no-emergency-fund-rbc-poll-finds-over-40-of-canadians-worry-even-one-major-unexpected-expense-could-derail-their-finances-811532406.html",
        "- Canada Life client story, “Anyone can get sick: Sandra's story” (Sandra and Warren). The original page is no longer online; confirm with the partner before showing names.",
        "",
    ]
    (ROOT / "speaker-notes.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    t = build_html()
    build_notes(t)
    print(f"index.html {len(t) / 1024:.0f} KB, speaker-notes.md written")
