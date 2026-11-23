#!/usr/bin/env python3
"""Builds john-story/index.html  ("The Gift That Keeps Giving: John's Story").
Run:  python3 john-story/build.py
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ILL = {r['age']: r for r in json.load(open(os.path.join(HERE, 'illustration.json')))['rows']}
RAJ = {r['age']: r for r in json.load(open(os.path.join(HERE, 'raj.json')))['rows']}
P2 = {r['age']: r for r in json.load(open(os.path.join(HERE, 'john2.json')))['rows']}
def P2DB(a): return P2[a]['totalDB'] if a >= 51 else (P2[51]['totalDB'] if a == 50 else 0)
def P2CV(a): return P2[a]['totalCV'] if a >= 51 else 0
TOT90 = ILL[90]['totalDB'] + P2[90]['totalDB']
QR = open(os.path.join(HERE, 'source', 'qr.txt')).read().strip()

def money(v, short=True):
    if short and v >= 1_000_000:
        return f"${v/1e6:.2f}M".replace('.00M', 'M')
    if short and v >= 1000:
        return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"

# ------------------------------------------------------------------ characters
SKIN = {'john': '#F2C9A5', 'emma': '#EDBE98', 'lily': '#F4CFAE', 'max': '#F4CFAE',
        'mehar': '#C48A5C', 'david': '#EBC39C', 'sarah': '#8E5B3C', 'raj': '#B57B52', 'jake': '#F2C9A5', 'tax': '#E8BE98', 'lsp': '#D9A57E', 'msp': '#F2C9A5', 'dau': '#F0C8A4', 'rc': '#D9A57E', 'rr': '#E8BE98', 'rt': '#C48A5C'}

def hair(style, col):
    cap = 'M-37,-186 C-44,-232 -22,-246 0,-246 C22,-246 44,-232 37,-186 C33,-208 22,-220 0,-220 C-22,-220 -33,-208 -37,-186Z'
    side = 'M-37,-184 C-45,-232 -22,-248 2,-247 C26,-246 45,-230 37,-184 C34,-206 26,-218 10,-222 C-6,-212 -22,-208 -37,-184Z'
    s = {
        'short': f'<path d="{cap}" fill="{col}"/>',
        'side':  f'<path d="{side}" fill="{col}"/><path d="M-20,-232 C-6,-240 14,-240 26,-230" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="4" stroke-linecap="round"/>',
        'long':  f'<path d="M-38,-190 C-46,-236 -22,-248 0,-248 C22,-248 46,-236 38,-190 L44,-140 C38,-132 30,-136 28,-150 L30,-198 C24,-216 14,-222 0,-222 C-14,-222 -24,-216 -30,-198 L-28,-150 C-30,-136 -38,-132 -44,-140Z" fill="{col}"/>',
        'bun':   f'<circle cx="0" cy="-248" r="15" fill="{col}"/><path d="{cap}" fill="{col}"/>',
        'pony':  f'<path d="M28,-226 C62,-214 62,-170 46,-160 C50,-186 42,-206 28,-212Z" fill="{col}"/><path d="{cap}" fill="{col}"/><circle cx="30" cy="-222" r="6" fill="#C62D3A"/>',
        'curly': ''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="{col}"/>' for x, y in [(-28,-222),(-14,-236),(2,-240),(18,-236),(30,-222),(-36,-204),(36,-204)]),
        'turban': ('<g transform="translate(0,-204) scale(.9) translate(0,204)">'
                   f'<path d="M-40,-198 C-46,-246 -10,-262 6,-258 C30,-254 46,-236 40,-198 C26,-214 -26,-214 -40,-198Z" fill="{col}"/>'
                   '<path d="M-38,-206 C-20,-232 18,-244 40,-216" fill="none" stroke="rgba(0,0,0,.22)" stroke-width="4"/>'
                   '<path d="M-34,-222 C-14,-246 20,-250 34,-232" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="4"/>'
                   '<path d="M-6,-256 L0,-210 L6,-256" fill="rgba(0,0,0,.18)"/></g>'),
        'grey':  f'<path d="{cap}" fill="#D9D9D9"/>',
    }
    return s[style]

def person(kind, x, y, s=1.0, outfit=None, extra=''):
    """Flat storybook figure, feet at (x,y)."""
    P = {
        'john':  dict(hair=('side', '#5A3A22'), top='#B3202A', bottom='#2E3440'),
        'jake':  dict(hair=('side', '#5A3A22'), top='#8C939C', bottom='#3B4048'),
        'emma':  dict(hair=('long', '#A0522D'), top='#E8E4DA', bottom='#5B2A3A'),
        'lily':  dict(hair=('pony', '#7A4A26'), top='#C62D3A', bottom='#3E5C76'),
        'max':   dict(hair=('short', '#7A4A26'), top='#2F6E4C', bottom='#2E3440'),
        'mehar': dict(hair=('turban', '#1E3F7A'), top='#1F2A44', bottom='#1F2A44', acc=['tie','beard']),
        'david': dict(hair=('short', '#9A8F86'), top='#5E6B78', bottom='#2E3440', acc=['glasses', 'tie']),
        'sarah': dict(hair=('bun', '#2A1A12'), top='#6B1F2A', bottom='#2B2B33'),
        'raj':   dict(hair=('short', '#1E1A18'), top='#FAFAFA', bottom='#2E3440', acc=['coat']),
    }[kind].copy()
    P['acc'] = list(P.get('acc', []))
    if outfit == 'coat': P['acc'].append('coat')
    if outfit == 'old':
        P['hair'] = ('grey', '#D9D9D9'); P['acc'].append('cane')
    if outfit == 'adult':   # grown-up kids
        pass
    sk = SKIN[kind]
    hs, hc = P['hair']
    top, bot = P['top'], P['bottom']
    g = []
    g.append(f'<ellipse cx="0" cy="2" rx="46" ry="7" fill="rgba(0,0,0,.18)"/>')
    g.append(f'<rect x="-24" y="-82" width="19" height="82" rx="7" fill="{bot}"/><rect x="5" y="-82" width="19" height="82" rx="7" fill="{bot}"/>')
    g.append(f'<ellipse cx="-15" cy="-2" rx="15" ry="7" fill="#2a2420"/><ellipse cx="15" cy="-2" rx="15" ry="7" fill="#2a2420"/>')
    g.append(f'<rect x="-53" y="-152" width="17" height="72" rx="8" fill="{top}"/><rect x="36" y="-152" width="17" height="72" rx="8" fill="{top}"/>')
    g.append(f'<circle cx="-44" cy="-80" r="9" fill="{sk}"/><circle cx="44" cy="-80" r="9" fill="{sk}"/>')
    g.append(f'<rect x="-39" y="-164" width="78" height="92" rx="26" fill="{top}"/>')
    if 'coat' in P['acc']:
        g.append('<path d="M-41,-160 Q-41,-166 -30,-166 L-8,-166 L0,-128 L8,-166 L30,-166 Q41,-166 41,-160 L42,-64 L-42,-64Z" fill="#FBFBFB" stroke="#D8D8D8" stroke-width="2"/>')
        g.append('<path d="M-14,-150 C-24,-118 -6,-104 6,-112" fill="none" stroke="#3E4B5B" stroke-width="3"/><circle cx="7" cy="-111" r="5" fill="#9AA6B2"/>')
    if 'tie' in P['acc']:
        g.append('<path d="M-12,-164 L0,-146 L12,-164Z" fill="#FAFAFA"/><path d="M-4,-150 L4,-150 L7,-112 L0,-104 L-7,-112Z" fill="#C9A227"/>')
    g.append(f'<rect x="-8" y="-176" width="16" height="16" fill="{sk}"/>')
    g.append(f'<circle cx="0" cy="-200" r="34" fill="{sk}"/>')
    g.append(hair(hs, hc))
    g.append('<circle cx="-12" cy="-200" r="3.6" fill="#2b2420"/><circle cx="12" cy="-200" r="3.6" fill="#2b2420"/>')
    g.append('<circle cx="-20" cy="-188" r="6" fill="#E8838A" opacity=".45"/><circle cx="20" cy="-188" r="6" fill="#E8838A" opacity=".45"/>')
    g.append('<path d="M-10,-185 Q0,-176 10,-185" fill="none" stroke="#7A3B2E" stroke-width="2.6" stroke-linecap="round"/>')
    if 'beard' in P['acc']:
        g.append('<path d="M-33,-204 C-34,-178 -22,-160 0,-156 C22,-160 34,-178 33,-204 C29,-190 20,-182 0,-180 C-20,-182 -29,-190 -33,-204Z" fill="#141210"/>'
                 '<path d="M-20,-186 C-12,-192 -4,-190 0,-186 C4,-190 12,-192 20,-186 C14,-180 6,-182 0,-184 C-6,-182 -14,-180 -20,-186Z" fill="#141210"/>'
                 '')
    if 'glasses' in P['acc']:
        g.append('<circle cx="-12" cy="-200" r="9" fill="none" stroke="#333" stroke-width="2"/><circle cx="12" cy="-200" r="9" fill="none" stroke="#333" stroke-width="2"/><path d="M-3,-200 L3,-200" stroke="#333" stroke-width="2"/>')
    if 'cane' in P['acc']:
        g.append('<path d="M58,0 L58,-78 Q58,-92 46,-92" fill="none" stroke="#6B4A2E" stroke-width="5" stroke-linecap="round"/>')
    g.append(extra)
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'

def label(x, y, txt, col='#7A0F1A', size=17):
    return f'<text x="{x}" y="{y}" text-anchor="middle" class="nm" style="fill:{col};font-size:{size}px">{txt}</text>'

# ------------------------------------------------------------------ props
def tree(x, y, s=1.0, lit=True):
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         '<rect x="-12" y="-30" width="24" height="30" fill="#6B4A2E"/>',
         '<path d="M0,-250 L70,-150 L40,-150 L95,-80 L55,-80 L110,-25 L-110,-25 L-55,-80 L-95,-80 L-40,-150 L-70,-150Z" fill="#1F5E3A"/>',
         '<path d="M0,-272 L7,-256 L24,-256 L10,-246 L15,-230 L0,-240 L-15,-230 L-10,-246 L-24,-256 L-7,-256Z" fill="#E5B93C"/>']
    if lit:
        for i, (ox, oy) in enumerate([(-30,-170),(28,-160),(-55,-110),(50,-100),(0,-120),(-80,-50),(78,-45),(-20,-60),(30,-55),(0,-195)]):
            c = ['#C62D3A', '#E5B93C', '#C9CED6'][i % 3]
            o.append(f'<circle class="tw" style="animation-delay:{i*0.37:.2f}s" cx="{ox}" cy="{oy}" r="8" fill="{c}"/>')
    o.append('</g>')
    return ''.join(o)

def house(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-120" y="-150" width="240" height="150" fill="#F4EBDD" stroke="#C9B79C" stroke-width="2"/>'
            '<path d="M-140,-145 L0,-250 L140,-145Z" fill="#9E1B26"/>'
            '<path d="M-150,-148 L0,-262 L150,-148" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linejoin="round"/>'
            '<rect x="-90" y="-120" width="70" height="60" fill="#F7C96B"/><path d="M-55,-118 L-35,-70 L-75,-70Z" fill="#1F5E3A"/>'
            '<rect x="25" y="-120" width="60" height="60" fill="#F7C96B"/>'
            '<rect x="-15" y="-70" width="34" height="70" fill="#7A0F1A"/><circle cx="12" cy="-34" r="3" fill="#E5B93C"/>'
            '<circle cx="2" cy="-92" r="14" fill="none" stroke="#2F6E4C" stroke-width="6"/><circle cx="2" cy="-78" r="3" fill="#C62D3A"/>'
            '</g>')

def clinic(x, y, s=1.0, n=1):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-110" y="-170" width="220" height="170" fill="#FFFFFF" stroke="#C9CED6" stroke-width="3"/>'
            '<rect x="-120" y="-190" width="240" height="26" fill="#9E1B26"/>'
            f'<text x="0" y="-171" text-anchor="middle" style="fill:#fff;font:700 15px Georgia,serif;letter-spacing:.08em">SMILE DENTAL {"#"+str(n) if n>1 else ""}</text>'
            '<rect x="-85" y="-140" width="60" height="50" fill="#CFE3F0"/><rect x="25" y="-140" width="60" height="50" fill="#CFE3F0"/>'
            '<rect x="-22" y="-80" width="44" height="80" fill="#7A8794"/>'
            '<path d="M-6,-120 C-14,-136 6,-140 0,-128 C-6,-140 14,-136 6,-120 L4,-104 L0,-112 L-4,-104Z" fill="#9E1B26" transform="translate(0,6)"/>'
            '<path d="M-120,-190 Q-60,-176 0,-190 Q60,-176 120,-190" fill="none" stroke="#E5B93C" stroke-width="4"/>'
            '</g>')

def desk(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-170" y="-90" width="340" height="18" rx="4" fill="#7A4A2A"/>'
            '<rect x="-160" y="-72" width="14" height="72" fill="#5E3820"/><rect x="146" y="-72" width="14" height="72" fill="#5E3820"/>'
            '<rect x="-60" y="-132" width="120" height="42" rx="4" fill="#FFFFFF" stroke="#C9CED6" stroke-width="2"/>'
            '<path d="M-44,-100 L-20,-116 L4,-106 L44,-126" fill="none" stroke="#2F6E4C" stroke-width="4"/>'
            '<circle cx="120" cy="-104" r="13" fill="#9E1B26"/><rect x="113" y="-121" width="14" height="8" fill="#9E1B26"/>'
            '</g>')

def ground(w=1300, y=470):
    return f'<path d="M0,{y} Q{w*.25},{y-26} {w*.5},{y-6} T{w},{y-14} L{w},{y+80} L0,{y+80}Z" fill="#F1E9DE" stroke="#D8CBB8" stroke-width="2"/>'

def gift(x, y, s=1.0, col='#9E1B26', txt=''):
    if txt:
        return (f'<g transform="translate({x},{y}) scale({s})" class="giftO">'
            f'<rect x="-60" y="-100" width="120" height="100" fill="{col}" stroke="#FFE7A6" stroke-width="4"/>'
            '<rect x="-68" y="-118" width="136" height="24" fill="#B32533" stroke="#FFE7A6" stroke-width="4"/>'
            '<rect x="-9" y="-118" width="18" height="118" fill="#E5B93C"/>'
            '<path d="M0,-118 C-40,-160 -60,-120 0,-118 C60,-120 40,-160 0,-118Z" fill="#E5B93C" stroke="#FFE7A6" stroke-width="2"/>'
            '<rect x="-52" y="-66" width="104" height="30" rx="5" fill="#FFF4DC" stroke="#E5B93C" stroke-width="2"/>'
            f'<text x="0" y="-45" text-anchor="middle" style="fill:#6B1218;font:900 17px Georgia,serif;letter-spacing:.06em">{txt}</text></g>')
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-60" y="-100" width="120" height="100" fill="{col}"/>'
            '<rect x="-68" y="-118" width="136" height="24" fill="#B32533"/>'
            '<rect x="-9" y="-118" width="18" height="118" fill="#E5B93C"/>'
            '<path d="M0,-118 C-40,-160 -60,-120 0,-118 C60,-120 40,-160 0,-118Z" fill="#E5B93C"/></g>')

def bucket(x, y, s, fill_pct, cls=''):
    h = 200
    fy = -20 - h * fill_pct
    return (f'<g transform="translate({x},{y}) scale({s})" class="{cls}">'
            '<defs><clipPath id="bk"><path d="M-110,-230 L110,-230 L85,-20 L-85,-20Z"/></clipPath></defs>'
            f'<g clip-path="url(#bk)"><rect class="bkFill" x="-120" y="{fy}" width="240" height="{h+30}" fill="#E5B93C"/></g>'
            '<path d="M-110,-230 L110,-230 L85,-20 L-85,-20Z" fill="none" stroke="#7A0F1A" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M-110,-230 Q0,-300 110,-230" fill="none" stroke="#8C939C" stroke-width="5"/>'
            '<text x="0" y="-110" text-anchor="middle" style="fill:#7A0F1A;font:900 52px Georgia,serif">CDA</text>'
            '</g>')

exec(open(os.path.join(HERE,'props2.py')).read())
# ------------------------------------------------------------------ slide helpers
SLIDES = []
def slide(html, cls='', hud=None, notes=''):
    attrs = ''
    if hud:
        attrs = ' data-hud="1" ' + ' '.join(f'data-{k}="{v}"' for k, v in hud.items())
    SLIDES.append(f'<section class="slide {cls}"{attrs}>{html}</section>')

def scene(svg, h=470):
    return f'<svg class="scene" viewBox="0 0 1300 {h}" width="1300" height="{h}" aria-hidden="true">{svg}</svg>'

def chapter(num, when, title, svg):
    return f'''<div class="chap"><div class="chNum">{num}</div><div class="chWhen">{when}</div><h1>{title}</h1></div>{scene(svg, 430)}'''

NEEDS = ['Delayed Taxes', 'Wealth Transfer', 'Key Person', 'Buy &amp; Sell', 'Debt', 'Liquidity', 'Estate Equalization']

def H(age, nw, needs='', rules='000', cda=None):
    if cda is None:
        cda = (ILL[age]['totalDB'] if age in ILL else 0) + P2DB(age)
    return dict(age=age, nw=nw, needs=needs, rules=rules, cda=cda)

def counter(to, pre='$', suf='', cls=''):
    return f'<b class="cnt {cls}" data-to="{to}" data-pre="{pre}" data-suf="{suf}">{pre}0{suf}</b>'


# ---- John's net worth model (story bar)
TFSA_MAX, RRSP_MAX, NONREG, RET = 7000, 33810, 15000, 0.12
def ACCTS(a):
    t, r, n = 109000, 150000, 0
    for y in range(41, a + 1):
        if y <= 65: t = t*(1+RET) + TFSA_MAX; r = r*(1+RET) + RRSP_MAX; n = n*(1+RET) + NONREG
        else: t *= (1+RET)*.9; r *= (1+RET)*.9; n *= (1+RET)*.9
    return t, r, n
def NW(a):
    home = 1.6e6*1.03**(a-40); mort = 1e6*max(0, (50-a)/10); loan = 5e5*max(0, (50-a)/10)
    bv = lambda st: 9e5*1.04**(min(a, 65)-st) if a >= st else 0
    bus = bv(40) + bv(46) + bv(55)
    corp = 5e5*1.05**(a-40); cv = (ILL[a]['totalCV'] if a >= 41 else 0) + P2CV(a); ifa = 5e5 if a >= 46 else 0
    return round(home - mort + bus - loan + corp + cv - ifa + sum(ACCTS(a)), -3)

# ================================================================== SLIDES
random.seed(3)

# 1 COVER
slide(f'''
<svg class="city" viewBox="0 0 1440 810" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs><radialGradient id="moon"><stop offset="0" stop-color="#FFF6E0"/><stop offset=".25" stop-color="#FFE7B0" stop-opacity=".9"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient><linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A0A12" stop-opacity="0"/><stop offset="1" stop-color="#1A050A" stop-opacity=".95"/></linearGradient></defs><circle cx="1260" cy="150" r="170" fill="url(#moon)" opacity=".5"/><circle cx="1260" cy="150" r="40" fill="#FFF4D8"/><rect x="0" y="503" width="65" height="237" fill="#3A1420"/><path d="M-2,505 Q32.5,496 67,505 L67,509 Q32.5,502 -2,509Z" fill="#EEF2F7" opacity="0.55"/><rect x="30.5" y="463" width="4" height="40" fill="#3A1420"/><circle class="tw" cx="32.5" cy="461" r="4" fill="#FF5A5A"/><rect x="68" y="541" width="80" height="199" fill="#3A1420"/><path d="M66,543 Q108.0,534 150,543 L150,547 Q108.0,540 66,547Z" fill="#EEF2F7" opacity="0.55"/><rect x="106.0" y="501" width="4" height="40" fill="#3A1420"/><circle class="tw" cx="108.0" cy="499" r="4" fill="#FF5A5A"/><rect x="148" y="440" width="75" height="300" fill="#3A1420"/><path d="M146,442 Q185.5,433 225,442 L225,446 Q185.5,439 146,446Z" fill="#EEF2F7" opacity="0.55"/><rect x="229" y="565" width="98" height="175" fill="#3A1420"/><path d="M227,567 Q278.0,558 329,567 L329,571 Q278.0,564 227,571Z" fill="#EEF2F7" opacity="0.55"/><rect x="331" y="510" width="73" height="230" fill="#3A1420"/><path d="M329,512 Q367.5,503 406,512 L406,516 Q367.5,509 329,516Z" fill="#EEF2F7" opacity="0.55"/><rect x="410" y="513" width="56" height="227" fill="#3A1420"/><path d="M408,515 Q438.0,506 468,515 L468,519 Q438.0,512 408,519Z" fill="#EEF2F7" opacity="0.55"/><rect x="466" y="416" width="103" height="324" fill="#3A1420"/><path d="M464,418 Q517.5,409 571,418 L571,422 Q517.5,415 464,422Z" fill="#EEF2F7" opacity="0.55"/><rect x="575" y="531" width="67" height="209" fill="#3A1420"/><path d="M573,533 Q608.5,524 644,533 L644,537 Q608.5,530 573,537Z" fill="#EEF2F7" opacity="0.55"/><rect x="644" y="485" width="90" height="255" fill="#3A1420"/><path d="M642,487 Q689.0,478 736,487 L736,491 Q689.0,484 642,491Z" fill="#EEF2F7" opacity="0.55"/><rect x="687.0" y="445" width="4" height="40" fill="#3A1420"/><circle class="tw" cx="689.0" cy="443" r="4" fill="#FF5A5A"/><rect x="738" y="409" width="71" height="331" fill="#3A1420"/><path d="M736,411 Q773.5,402 811,411 L811,415 Q773.5,408 736,415Z" fill="#EEF2F7" opacity="0.55"/><rect x="810" y="517" width="61" height="223" fill="#3A1420"/><path d="M808,519 Q840.5,510 873,519 L873,523 Q840.5,516 808,523Z" fill="#EEF2F7" opacity="0.55"/><rect x="871" y="440" width="110" height="300" fill="#3A1420"/><path d="M869,442 Q926.0,433 983,442 L983,446 Q926.0,439 869,446Z" fill="#EEF2F7" opacity="0.55"/><rect x="981" y="506" width="108" height="234" fill="#3A1420"/><path d="M979,508 Q1035.0,499 1091,508 L1091,512 Q1035.0,505 979,512Z" fill="#EEF2F7" opacity="0.55"/><rect x="1091" y="450" width="104" height="290" fill="#3A1420"/><path d="M1089,452 Q1143.0,443 1197,452 L1197,456 Q1143.0,449 1089,456Z" fill="#EEF2F7" opacity="0.55"/><rect x="1198" y="507" width="88" height="233" fill="#3A1420"/><path d="M1196,509 Q1242.0,500 1288,509 L1288,513 Q1242.0,506 1196,513Z" fill="#EEF2F7" opacity="0.55"/><rect x="1287" y="502" width="64" height="238" fill="#3A1420"/><path d="M1285,504 Q1319.0,495 1353,504 L1353,508 Q1319.0,501 1285,508Z" fill="#EEF2F7" opacity="0.55"/><rect x="1357" y="560" width="52" height="180" fill="#3A1420"/><path d="M1355,562 Q1383.0,553 1411,562 L1411,566 Q1383.0,559 1355,566Z" fill="#EEF2F7" opacity="0.55"/><rect x="1414" y="448" width="67" height="292" fill="#3A1420"/><path d="M1412,450 Q1447.5,441 1483,450 L1483,454 Q1447.5,447 1412,454Z" fill="#EEF2F7" opacity="0.55"/><rect x="0" y="494" width="119" height="286" fill="#26090F"/><path d="M-2,496 Q59.5,487 121,496 L121,500 Q59.5,493 -2,500Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:5.2s" x="22" y="508" width="6" height="8" fill="#FFD27A" opacity="0.50"/><rect class="win" style="animation-delay:3.3s" x="64" y="508" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:2.3s" x="78" y="508" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:1.4s" x="8" y="526" width="6" height="8" fill="#FFD27A" opacity="0.56"/><rect class="win" style="animation-delay:1.7s" x="106" y="526" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:1.6s" x="36" y="544" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:4.9s" x="50" y="544" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:2.3s" x="92" y="544" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:2.5s" x="106" y="544" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:3.6s" x="8" y="562" width="6" height="8" fill="#FFD27A" opacity="0.56"/><rect class="win" style="animation-delay:0.0s" x="50" y="562" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:0.5s" x="78" y="562" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:3.5s" x="36" y="580" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:3.3s" x="78" y="580" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect class="win" style="animation-delay:1.6s" x="92" y="580" width="6" height="8" fill="#FFD27A" opacity="1.00"/><rect class="win" style="animation-delay:4.2s" x="8" y="598" width="6" height="8" fill="#FFD27A" opacity="0.98"/><rect class="win" style="animation-delay:3.7s" x="22" y="598" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:2.1s" x="92" y="598" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:4.8s" x="64" y="616" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:2.7s" x="92" y="616" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:3.8s" x="106" y="616" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:4.7s" x="22" y="634" width="6" height="8" fill="#FFD27A" opacity="0.90"/><rect class="win" style="animation-delay:4.4s" x="64" y="634" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:5.8s" x="78" y="634" width="6" height="8" fill="#FFD27A" opacity="0.70"/><rect class="win" style="animation-delay:5.1s" x="36" y="652" width="6" height="8" fill="#FFD27A" opacity="0.63"/><rect class="win" style="animation-delay:5.9s" x="50" y="652" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:0.4s" x="106" y="652" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:3.4s" x="64" y="670" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:3.3s" x="78" y="670" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:2.7s" x="92" y="670" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:4.3s" x="36" y="688" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:0.3s" x="78" y="688" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:3.8s" x="92" y="688" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:0.1s" x="8" y="706" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:2.9s" x="64" y="706" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:6.0s" x="106" y="706" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:3.9s" x="64" y="724" width="6" height="8" fill="#FFD27A" opacity="0.77"/><rect class="win" style="animation-delay:4.3s" x="78" y="724" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:4.2s" x="92" y="724" width="6" height="8" fill="#FFD27A" opacity="0.73"/><rect x="119" y="555" width="63" height="225" fill="#26090F"/><path d="M117,557 Q150.5,548 184,557 L184,561 Q150.5,554 117,561Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:2.8s" x="127" y="569" width="6" height="8" fill="#FFD27A" opacity="0.69"/><rect class="win" style="animation-delay:3.7s" x="127" y="587" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:2.5s" x="141" y="587" width="6" height="8" fill="#FFD27A" opacity="0.79"/><rect class="win" style="animation-delay:0.2s" x="155" y="587" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:0.2s" x="169" y="587" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:0.5s" x="169" y="605" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:2.3s" x="155" y="623" width="6" height="8" fill="#FFD27A" opacity="0.74"/><rect class="win" style="animation-delay:5.4s" x="169" y="623" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:5.8s" x="141" y="641" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:0.4s" x="155" y="641" width="6" height="8" fill="#FFD27A" opacity="0.82"/><rect class="win" style="animation-delay:0.6s" x="169" y="641" width="6" height="8" fill="#FFD27A" opacity="0.51"/><rect class="win" style="animation-delay:5.2s" x="141" y="659" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:4.6s" x="155" y="659" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:1.5s" x="169" y="659" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:5.2s" x="141" y="695" width="6" height="8" fill="#FFD27A" opacity="0.82"/><rect class="win" style="animation-delay:0.2s" x="169" y="695" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:5.9s" x="169" y="713" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:2.6s" x="141" y="731" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect x="185" y="597" width="115" height="183" fill="#26090F"/><path d="M183,599 Q242.5,590 302,599 L302,603 Q242.5,596 183,603Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:1.8s" x="193" y="611" width="6" height="8" fill="#FFD27A" opacity="0.73"/><rect class="win" style="animation-delay:0.6s" x="263" y="611" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:1.3s" x="277" y="611" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:5.8s" x="207" y="629" width="6" height="8" fill="#FFD27A" opacity="0.98"/><rect class="win" style="animation-delay:4.0s" x="193" y="647" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:4.4s" x="207" y="647" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:5.5s" x="263" y="647" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:5.9s" x="277" y="647" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:2.0s" x="291" y="647" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:5.5s" x="221" y="683" width="6" height="8" fill="#FFD27A" opacity="0.78"/><rect class="win" style="animation-delay:1.0s" x="263" y="683" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:3.1s" x="291" y="683" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:1.7s" x="221" y="701" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:0.9s" x="263" y="701" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:1.7s" x="291" y="701" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:2.5s" x="291" y="719" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect x="304" y="648" width="114" height="132" fill="#26090F"/><path d="M302,650 Q361.0,641 420,650 L420,654 Q361.0,647 302,654Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:4.8s" x="382" y="662" width="6" height="8" fill="#FFD27A" opacity="0.70"/><rect class="win" style="animation-delay:2.1s" x="382" y="680" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:3.2s" x="326" y="698" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:0.3s" x="382" y="698" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:5.0s" x="312" y="716" width="6" height="8" fill="#FFD27A" opacity="0.64"/><rect class="win" style="animation-delay:1.8s" x="326" y="716" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:1.0s" x="396" y="716" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect x="419" y="502" width="126" height="278" fill="#26090F"/><path d="M417,504 Q482.0,495 547,504 L547,508 Q482.0,501 417,508Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:6.0s" x="497" y="516" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:2.2s" x="497" y="534" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:5.2s" x="497" y="552" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:1.8s" x="525" y="552" width="6" height="8" fill="#FFD27A" opacity="0.51"/><rect class="win" style="animation-delay:5.7s" x="455" y="570" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:4.1s" x="483" y="570" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:1.3s" x="511" y="570" width="6" height="8" fill="#FFD27A" opacity="0.63"/><rect class="win" style="animation-delay:2.4s" x="483" y="588" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:1.5s" x="497" y="588" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect class="win" style="animation-delay:3.8s" x="441" y="606" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:3.3s" x="483" y="606" width="6" height="8" fill="#FFD27A" opacity="0.64"/><rect class="win" style="animation-delay:2.6s" x="497" y="606" width="6" height="8" fill="#FFD27A" opacity="0.99"/><rect class="win" style="animation-delay:2.2s" x="427" y="624" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:0.7s" x="441" y="642" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:0.5s" x="483" y="642" width="6" height="8" fill="#FFD27A" opacity="0.63"/><rect class="win" style="animation-delay:3.5s" x="497" y="642" width="6" height="8" fill="#FFD27A" opacity="0.99"/><rect class="win" style="animation-delay:4.3s" x="427" y="660" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:2.6s" x="455" y="660" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:3.1s" x="525" y="660" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:1.8s" x="455" y="678" width="6" height="8" fill="#FFD27A" opacity="0.64"/><rect class="win" style="animation-delay:3.2s" x="455" y="696" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:4.5s" x="483" y="696" width="6" height="8" fill="#FFD27A" opacity="0.92"/><rect class="win" style="animation-delay:5.7s" x="525" y="696" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect class="win" style="animation-delay:3.1s" x="483" y="714" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect x="547" y="580" width="81" height="200" fill="#26090F"/><path d="M545,582 Q587.5,573 630,582 L630,586 Q587.5,579 545,586Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:5.2s" x="555" y="594" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:5.9s" x="569" y="612" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:2.9s" x="583" y="612" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:4.8s" x="583" y="630" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect class="win" style="animation-delay:2.5s" x="611" y="630" width="6" height="8" fill="#FFD27A" opacity="0.73"/><rect class="win" style="animation-delay:1.3s" x="583" y="648" width="6" height="8" fill="#FFD27A" opacity="0.92"/><rect class="win" style="animation-delay:4.6s" x="555" y="666" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:2.9s" x="569" y="666" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:4.4s" x="583" y="666" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect class="win" style="animation-delay:5.5s" x="597" y="666" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:2.2s" x="569" y="684" width="6" height="8" fill="#FFD27A" opacity="0.61"/><rect class="win" style="animation-delay:1.5s" x="611" y="702" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:5.9s" x="555" y="720" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:0.1s" x="569" y="720" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect class="win" style="animation-delay:3.0s" x="583" y="720" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect x="634" y="616" width="102" height="164" fill="#26090F"/><path d="M632,618 Q685.0,609 738,618 L738,622 Q685.0,615 632,622Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:4.8s" x="642" y="630" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:0.0s" x="684" y="630" width="6" height="8" fill="#FFD27A" opacity="0.78"/><rect class="win" style="animation-delay:2.7s" x="670" y="648" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:1.2s" x="712" y="648" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:3.4s" x="656" y="666" width="6" height="8" fill="#FFD27A" opacity="0.90"/><rect class="win" style="animation-delay:4.2s" x="670" y="666" width="6" height="8" fill="#FFD27A" opacity="0.80"/><rect class="win" style="animation-delay:3.9s" x="642" y="684" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:0.6s" x="656" y="684" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:3.2s" x="670" y="684" width="6" height="8" fill="#FFD27A" opacity="0.50"/><rect class="win" style="animation-delay:3.5s" x="698" y="684" width="6" height="8" fill="#FFD27A" opacity="0.64"/><rect class="win" style="animation-delay:1.4s" x="712" y="684" width="6" height="8" fill="#FFD27A" opacity="0.74"/><rect class="win" style="animation-delay:4.0s" x="642" y="702" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:4.1s" x="670" y="702" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect class="win" style="animation-delay:4.6s" x="712" y="702" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:5.2s" x="642" y="720" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:5.1s" x="684" y="720" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:3.3s" x="698" y="720" width="6" height="8" fill="#FFD27A" opacity="0.90"/><rect x="736" y="569" width="87" height="211" fill="#26090F"/><path d="M734,571 Q779.5,562 825,571 L825,575 Q779.5,568 734,575Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:5.0s" x="744" y="583" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:2.2s" x="772" y="583" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:4.5s" x="800" y="583" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:4.2s" x="814" y="583" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:3.5s" x="814" y="601" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:1.2s" x="772" y="619" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:4.4s" x="744" y="637" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:6.0s" x="772" y="637" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:2.7s" x="800" y="637" width="6" height="8" fill="#FFD27A" opacity="0.74"/><rect class="win" style="animation-delay:4.9s" x="800" y="655" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:5.0s" x="814" y="655" width="6" height="8" fill="#FFD27A" opacity="0.56"/><rect class="win" style="animation-delay:2.5s" x="744" y="673" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:3.8s" x="772" y="673" width="6" height="8" fill="#FFD27A" opacity="0.91"/><rect class="win" style="animation-delay:0.9s" x="800" y="673" width="6" height="8" fill="#FFD27A" opacity="0.53"/><rect class="win" style="animation-delay:0.3s" x="814" y="673" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:5.6s" x="758" y="691" width="6" height="8" fill="#FFD27A" opacity="0.99"/><rect class="win" style="animation-delay:4.4s" x="758" y="709" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:0.3s" x="772" y="709" width="6" height="8" fill="#FFD27A" opacity="0.63"/><rect class="win" style="animation-delay:1.6s" x="786" y="709" width="6" height="8" fill="#FFD27A" opacity="0.96"/><rect class="win" style="animation-delay:0.6s" x="814" y="709" width="6" height="8" fill="#FFD27A" opacity="0.53"/><rect class="win" style="animation-delay:3.1s" x="772" y="727" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:2.8s" x="786" y="727" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect class="win" style="animation-delay:4.5s" x="800" y="727" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect x="828" y="490" width="63" height="290" fill="#26090F"/><path d="M826,492 Q859.5,483 893,492 L893,496 Q859.5,489 826,496Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:1.4s" x="850" y="522" width="6" height="8" fill="#FFD27A" opacity="0.98"/><rect class="win" style="animation-delay:2.5s" x="850" y="540" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect class="win" style="animation-delay:5.3s" x="878" y="540" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:3.4s" x="836" y="558" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:3.6s" x="878" y="558" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:1.2s" x="850" y="576" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:0.3s" x="864" y="594" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:0.8s" x="864" y="612" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:4.5s" x="878" y="612" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:1.8s" x="850" y="630" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:5.7s" x="878" y="630" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:3.9s" x="836" y="648" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:0.4s" x="864" y="648" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:1.4s" x="850" y="666" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:2.2s" x="878" y="666" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:1.9s" x="836" y="684" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:1.9s" x="836" y="702" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect x="894" y="613" width="91" height="167" fill="#26090F"/><path d="M892,615 Q939.5,606 987,615 L987,619 Q939.5,612 892,619Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:3.2s" x="972" y="627" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect class="win" style="animation-delay:4.2s" x="916" y="645" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:0.3s" x="930" y="645" width="6" height="8" fill="#FFD27A" opacity="0.99"/><rect class="win" style="animation-delay:4.1s" x="944" y="645" width="6" height="8" fill="#FFD27A" opacity="0.53"/><rect class="win" style="animation-delay:3.6s" x="972" y="645" width="6" height="8" fill="#FFD27A" opacity="0.87"/><rect class="win" style="animation-delay:0.3s" x="944" y="663" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:1.2s" x="902" y="681" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:1.7s" x="930" y="681" width="6" height="8" fill="#FFD27A" opacity="0.51"/><rect class="win" style="animation-delay:5.0s" x="944" y="681" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:4.4s" x="972" y="681" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:3.6s" x="902" y="699" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:4.4s" x="930" y="699" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:3.9s" x="944" y="699" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:4.9s" x="958" y="699" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:2.8s" x="972" y="699" width="6" height="8" fill="#FFD27A" opacity="0.79"/><rect class="win" style="animation-delay:3.1s" x="902" y="717" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect x="985" y="558" width="102" height="222" fill="#26090F"/><path d="M983,560 Q1036.0,551 1089,560 L1089,564 Q1036.0,557 983,564Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:4.1s" x="1007" y="572" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:2.7s" x="1021" y="572" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:5.5s" x="1035" y="572" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:3.2s" x="1063" y="572" width="6" height="8" fill="#FFD27A" opacity="0.92"/><rect class="win" style="animation-delay:0.4s" x="993" y="590" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:0.6s" x="1035" y="590" width="6" height="8" fill="#FFD27A" opacity="0.61"/><rect class="win" style="animation-delay:3.4s" x="1063" y="590" width="6" height="8" fill="#FFD27A" opacity="0.65"/><rect class="win" style="animation-delay:5.8s" x="1007" y="608" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:4.4s" x="1049" y="626" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect class="win" style="animation-delay:3.2s" x="1063" y="626" width="6" height="8" fill="#FFD27A" opacity="0.88"/><rect class="win" style="animation-delay:3.2s" x="993" y="644" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:5.6s" x="1007" y="644" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:4.6s" x="1021" y="644" width="6" height="8" fill="#FFD27A" opacity="0.51"/><rect class="win" style="animation-delay:0.9s" x="1063" y="644" width="6" height="8" fill="#FFD27A" opacity="0.99"/><rect class="win" style="animation-delay:3.0s" x="1021" y="680" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:3.4s" x="1049" y="680" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:0.9s" x="993" y="698" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:0.4s" x="1007" y="698" width="6" height="8" fill="#FFD27A" opacity="0.70"/><rect class="win" style="animation-delay:4.1s" x="1021" y="698" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:5.4s" x="1077" y="698" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect x="1089" y="510" width="111" height="270" fill="#26090F"/><path d="M1087,512 Q1144.5,503 1202,512 L1202,516 Q1144.5,509 1087,516Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:5.8s" x="1111" y="524" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect class="win" style="animation-delay:5.3s" x="1125" y="524" width="6" height="8" fill="#FFD27A" opacity="0.93"/><rect class="win" style="animation-delay:2.7s" x="1167" y="524" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:3.5s" x="1097" y="542" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:3.4s" x="1111" y="542" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect class="win" style="animation-delay:1.3s" x="1139" y="542" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:5.9s" x="1153" y="542" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:1.5s" x="1097" y="560" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect class="win" style="animation-delay:1.0s" x="1097" y="578" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:3.1s" x="1167" y="596" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:3.9s" x="1181" y="596" width="6" height="8" fill="#FFD27A" opacity="0.94"/><rect class="win" style="animation-delay:2.4s" x="1111" y="632" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:5.5s" x="1139" y="632" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect class="win" style="animation-delay:5.5s" x="1167" y="632" width="6" height="8" fill="#FFD27A" opacity="0.87"/><rect class="win" style="animation-delay:5.1s" x="1153" y="650" width="6" height="8" fill="#FFD27A" opacity="0.82"/><rect class="win" style="animation-delay:4.7s" x="1097" y="668" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:1.3s" x="1111" y="668" width="6" height="8" fill="#FFD27A" opacity="0.55"/><rect class="win" style="animation-delay:1.5s" x="1167" y="668" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:1.9s" x="1181" y="668" width="6" height="8" fill="#FFD27A" opacity="0.53"/><rect class="win" style="animation-delay:5.6s" x="1139" y="686" width="6" height="8" fill="#FFD27A" opacity="0.92"/><rect class="win" style="animation-delay:5.2s" x="1167" y="686" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:4.4s" x="1097" y="704" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:2.4s" x="1111" y="704" width="6" height="8" fill="#FFD27A" opacity="0.84"/><rect class="win" style="animation-delay:2.4s" x="1125" y="704" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:3.8s" x="1167" y="704" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:4.5s" x="1125" y="722" width="6" height="8" fill="#FFD27A" opacity="0.75"/><rect x="1202" y="522" width="115" height="258" fill="#26090F"/><path d="M1200,524 Q1259.5,515 1319,524 L1319,528 Q1259.5,521 1200,528Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:5.2s" x="1238" y="536" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:2.8s" x="1252" y="536" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:3.6s" x="1280" y="536" width="6" height="8" fill="#FFD27A" opacity="0.52"/><rect class="win" style="animation-delay:1.7s" x="1294" y="536" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:0.2s" x="1210" y="554" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:4.3s" x="1224" y="554" width="6" height="8" fill="#FFD27A" opacity="0.91"/><rect class="win" style="animation-delay:3.4s" x="1280" y="554" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:2.4s" x="1294" y="572" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:4.9s" x="1308" y="572" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:3.3s" x="1224" y="590" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect class="win" style="animation-delay:0.3s" x="1252" y="590" width="6" height="8" fill="#FFD27A" opacity="0.73"/><rect class="win" style="animation-delay:5.2s" x="1266" y="590" width="6" height="8" fill="#FFD27A" opacity="0.59"/><rect class="win" style="animation-delay:2.2s" x="1280" y="590" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:2.9s" x="1238" y="608" width="6" height="8" fill="#FFD27A" opacity="0.95"/><rect class="win" style="animation-delay:6.0s" x="1280" y="608" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:0.6s" x="1308" y="608" width="6" height="8" fill="#FFD27A" opacity="0.71"/><rect class="win" style="animation-delay:3.5s" x="1252" y="626" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:0.8s" x="1266" y="626" width="6" height="8" fill="#FFD27A" opacity="0.53"/><rect class="win" style="animation-delay:4.7s" x="1280" y="626" width="6" height="8" fill="#FFD27A" opacity="0.98"/><rect class="win" style="animation-delay:2.9s" x="1224" y="644" width="6" height="8" fill="#FFD27A" opacity="0.70"/><rect class="win" style="animation-delay:4.4s" x="1280" y="644" width="6" height="8" fill="#FFD27A" opacity="0.96"/><rect class="win" style="animation-delay:6.0s" x="1266" y="662" width="6" height="8" fill="#FFD27A" opacity="0.62"/><rect class="win" style="animation-delay:5.3s" x="1238" y="680" width="6" height="8" fill="#FFD27A" opacity="0.79"/><rect class="win" style="animation-delay:2.0s" x="1252" y="680" width="6" height="8" fill="#FFD27A" opacity="0.69"/><rect class="win" style="animation-delay:1.6s" x="1280" y="680" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:4.6s" x="1280" y="698" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:3.3s" x="1210" y="716" width="6" height="8" fill="#FFD27A" opacity="0.86"/><rect class="win" style="animation-delay:3.7s" x="1224" y="716" width="6" height="8" fill="#FFD27A" opacity="0.63"/><rect class="win" style="animation-delay:0.3s" x="1238" y="716" width="6" height="8" fill="#FFD27A" opacity="0.70"/><rect class="win" style="animation-delay:1.1s" x="1252" y="716" width="6" height="8" fill="#FFD27A" opacity="0.66"/><rect x="1320" y="568" width="71" height="212" fill="#26090F"/><path d="M1318,570 Q1355.5,561 1393,570 L1393,574 Q1355.5,567 1318,574Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:2.4s" x="1328" y="582" width="6" height="8" fill="#FFD27A" opacity="0.77"/><rect class="win" style="animation-delay:1.6s" x="1370" y="582" width="6" height="8" fill="#FFD27A" opacity="0.89"/><rect class="win" style="animation-delay:3.0s" x="1356" y="600" width="6" height="8" fill="#FFD27A" opacity="0.78"/><rect class="win" style="animation-delay:4.2s" x="1342" y="636" width="6" height="8" fill="#FFD27A" opacity="0.72"/><rect class="win" style="animation-delay:5.2s" x="1342" y="654" width="6" height="8" fill="#FFD27A" opacity="0.57"/><rect class="win" style="animation-delay:3.3s" x="1328" y="672" width="6" height="8" fill="#FFD27A" opacity="0.91"/><rect class="win" style="animation-delay:0.9s" x="1342" y="672" width="6" height="8" fill="#FFD27A" opacity="0.97"/><rect class="win" style="animation-delay:6.0s" x="1356" y="672" width="6" height="8" fill="#FFD27A" opacity="0.67"/><rect class="win" style="animation-delay:1.4s" x="1342" y="690" width="6" height="8" fill="#FFD27A" opacity="0.81"/><rect class="win" style="animation-delay:1.4s" x="1356" y="690" width="6" height="8" fill="#FFD27A" opacity="0.68"/><rect class="win" style="animation-delay:5.7s" x="1370" y="690" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:3.6s" x="1356" y="708" width="6" height="8" fill="#FFD27A" opacity="0.83"/><rect class="win" style="animation-delay:0.5s" x="1370" y="726" width="6" height="8" fill="#FFD27A" opacity="0.85"/><rect x="1391" y="643" width="94" height="137" fill="#26090F"/><path d="M1389,645 Q1438.0,636 1487,645 L1487,649 Q1438.0,642 1389,649Z" fill="#EEF2F7" opacity="0.8"/><rect class="win" style="animation-delay:3.0s" x="1413" y="693" width="6" height="8" fill="#FFD27A" opacity="0.54"/><rect class="win" style="animation-delay:5.1s" x="1427" y="693" width="6" height="8" fill="#FFD27A" opacity="0.77"/><rect class="win" style="animation-delay:2.4s" x="1413" y="711" width="6" height="8" fill="#FFD27A" opacity="0.76"/><rect class="win" style="animation-delay:0.6s" x="1413" y="729" width="6" height="8" fill="#FFD27A" opacity="0.60"/><rect class="win" style="animation-delay:4.1s" x="1427" y="729" width="6" height="8" fill="#FFD27A" opacity="0.58"/><rect x="0" y="560" width="1440" height="250" fill="url(#haze)"/><path d="M0,740 Q360,712 720,732 T1440,724 L1440,810 L0,810Z" fill="#F4EEE6"/><path d="M0,752 Q400,730 760,748 T1440,742 L1440,810 L0,810Z" fill="#E6DED3"/><g transform="translate(160,742)"><rect x="-2" y="-90" width="4" height="90" fill="#140408"/><circle class="lamp" cx="0" cy="-94" r="7" fill="#FFD27A"/><circle cx="0" cy="-94" r="34" fill="url(#moon)" opacity=".5"/></g><g transform="translate(520,742)"><rect x="-2" y="-90" width="4" height="90" fill="#140408"/><circle class="lamp" cx="0" cy="-94" r="7" fill="#FFD27A"/><circle cx="0" cy="-94" r="34" fill="url(#moon)" opacity=".5"/></g><g transform="translate(920,742)"><rect x="-2" y="-90" width="4" height="90" fill="#140408"/><circle class="lamp" cx="0" cy="-94" r="7" fill="#FFD27A"/><circle cx="0" cy="-94" r="34" fill="url(#moon)" opacity=".5"/></g><g transform="translate(1290,742)"><rect x="-2" y="-90" width="4" height="90" fill="#140408"/><circle class="lamp" cx="0" cy="-94" r="7" fill="#FFD27A"/><circle cx="0" cy="-94" r="34" fill="url(#moon)" opacity=".5"/></g></svg>
<div class="cover">
  <div class="kick">Team All In presents</div>
  <h1 class="ttl" id="ttl"><span class="hatL">T<svg class="hat" viewBox="0 0 120 110" aria-hidden="true"><path d="M8,92 C30,40 62,8 98,14 C108,16 112,30 104,44 C96,58 92,72 96,88Z" fill="#D11F2E"/><path d="M8,92 C30,40 62,8 98,14 C80,20 54,46 40,90Z" fill="#9E1424"/><rect x="0" y="84" width="104" height="22" rx="11" fill="#FFF"/><circle cx="104" cy="44" r="13" fill="#FFF"/></svg></span><span id="t1">he Gift That</span><br><span id="t2">Keeps Giving</span></h1>
  <div class="rule"></div>
  <p class="subt">A Christmas story about John, his business,<br>and the legacy he left behind.</p>
</div>
''', 'sCover')

# ---- v29 helpers
def STARS(n, ymax, seed):
    import random as _r; _r.seed(seed)
    return ''.join(f'<circle cx="{_r.randint(8,712)}" cy="{_r.randint(12,ymax)}" r="{_r.choice([1.3,1.8,2.3])}" fill="#fff" opacity="{_r.uniform(.35,.8):.2f}"/>' for _ in range(n))
def half_svg(inner, defs=''):
    return f'<div class="halfL"><svg viewBox="0 0 720 810" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs>{defs}</defs>{inner}</svg></div>'
def snow_floor(y=640, w=720):
    return f'<path d="M-40,{y+10} Q{w*.25},{y-14} {w*.5},{y+2} T{w+40},{y-4} V830 H-40Z" fill="url(#gSnow)"/><path d="M-40,{y+16} Q{w*.25},{y-6} {w*.5},{y+10} T{w+40},{y+4}" stroke="rgba(160,170,190,.55)" stroke-width="3" fill="none"/>'
def bubble(x, y, w, lines, tx, ty, size=19, cls='', fill='#FBF3E2', ink='#6B1218', bold_last=False):
    lh = size * 1.3; h = 22 + lh * len(lines)
    cx = x + w / 2
    tb = min(max(tx, x + 30), x + w - 30)
    g = [f'<g class="bub {cls}">',
         f'<path d="M{tb-14},{y+h-2} L{tx},{ty} L{tb+14},{y+h-2}Z" fill="{fill}" stroke="#E5B93C" stroke-width="3" stroke-linejoin="round"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="#E5B93C" stroke-width="3"/>',
         f'<path d="M{tb-12},{y+h-3} L{tb+12},{y+h-3}" stroke="{fill}" stroke-width="7"/>']
    for k, t in enumerate(lines):
        wt = 900 if (bold_last and k == len(lines) - 1) else 700
        g.append(f'<text x="{cx}" y="{y + 11 + lh*(k+1) - size*.25:.0f}" text-anchor="middle" style="font:italic {wt} {size}px Georgia;fill:{ink}">{t}</text>')
    g.append('</g>')
    return ''.join(g)

# ---- v22 illustrations
def peace_tower(x, y, s=1.0):
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    g.append('<rect x="-230" y="-120" width="460" height="120" fill="#D9C9A4"/><rect x="-230" y="-120" width="460" height="120" fill="url(#gShade)" opacity=".5"/>')
    g.append('<path d="M-240,-120 L-200,-160 L-60,-160 L-40,-120Z M240,-120 L200,-160 L60,-160 L40,-120Z" fill="#4F8A74"/>')
    g.append(''.join(f'<rect x="{-215 + k*30}" y="-100" width="14" height="36" rx="7" fill="#5A4A3A"/>' for k in range(15) if abs(-215 + k*30 + 7) > 48))
    g.append('<rect x="-42" y="-330" width="84" height="330" fill="#E4D5B0"/><rect x="-42" y="-330" width="84" height="330" fill="url(#gShade)" opacity=".4"/>')
    g.append('<circle cx="0" cy="-250" r="26" fill="#F4ECD6" stroke="#8A6510" stroke-width="4"/><path d="M0,-250 L0,-266 M0,-250 L12,-244" stroke="#3A2A1A" stroke-width="3" stroke-linecap="round"/>')
    g.append('<path d="M-46,-330 L0,-420 L46,-330Z" fill="#4F8A74"/><path d="M0,-420 L0,-446" stroke="#8A6510" stroke-width="3"/><rect x="-6" y="-446" width="18" height="11" fill="#D52B1E"/>')
    g.append('<path d="M-16,0 L-16,-60 C-16,-80 16,-80 16,-60 L16,0Z" fill="#5A4A3A"/>')
    g.append(''.join(f'<rect x="-28" y="{-200 + k*34}" width="12" height="22" rx="6" fill="#5A4A3A"/><rect x="16" y="{-200 + k*34}" width="12" height="22" rx="6" fill="#5A4A3A"/>' for k in range(4)))
    g.append('</g>')
    return ''.join(g)
def money_bag(x, y, s=1.0, txt='RRSP'):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-40,0 C-60,-10 -58,-60 -22,-78 L-30,-96 L30,-96 L22,-78 C58,-60 60,-10 40,0Z" fill="#B88A4A" stroke="#7A5A2A" stroke-width="3"/>'
            '<path d="M-24,-80 C-8,-74 8,-74 24,-80" stroke="#7A5A2A" stroke-width="5" fill="none"/>'
            f'<text y="-34" text-anchor="middle" style="font:900 26px Georgia;fill:#5A3A12">$</text><text y="-12" text-anchor="middle" style="font:900 15px Georgia;fill:#5A3A12">{txt}</text></g>')
def tax_bill(x, y, s=1.0, rot=-8):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><rect x="-58" y="-74" width="116" height="148" fill="#FBF6EA" stroke="#B9AE96" stroke-width="2"/>'
            '<text y="-46" text-anchor="middle" style="font:900 17px Georgia;fill:#B3202A">TAX BILL</text><line x1="-42" y1="-36" x2="42" y2="-36" stroke="#B3202A" stroke-width="2"/>'
            '<path d="M-42,-18 H42 M-42,-4 H30 M-42,10 H38" stroke="#C9BFA8" stroke-width="4"/>'
            '<text y="40" text-anchor="middle" style="font:900 22px Georgia;fill:#2E1E12">$660,000</text>'
            '<rect x="-46" y="48" width="92" height="18" rx="3" fill="none" stroke="#B3202A" stroke-width="2.5" transform="rotate(-6)"/><text y="62" text-anchor="middle" transform="rotate(-6)" style="font:900 11px sans-serif;fill:#B3202A;letter-spacing:.12em">DUE NOW</text></g>')
HOOK_HALF = half_svg('<rect x="-400" y="-900" width="1520" height="905" fill="#1A0810"/><rect width="720" height="810" fill="url(#hkSky)"/>' + STARS(40, 420, 3)
  + peace_tower(210, 690, 1.3) + snow_floor(680)
  + person('tax', 330, 712, 1.5, arm='hold') + money_bag(412, 538, 1.34) + tax_bill(196, 518, 1.42)
  + person('dau', 535, 712, 1.35, mood='sad') + '<circle cx="601" cy="592" r="14" fill="#E5B93C" stroke="#8A6510" stroke-width="3"/>',
  '<linearGradient id="hkSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A0810"/><stop offset="1" stop-color="#4A1520"/></linearGradient>')
HOOK_SCENE = scene(ground(620,420) + peace_tower(200,410,.82)
  + person('tax',390,410,.95,arm='hold') + money_bag(442,300,.85) + tax_bill(302,286,.9)
  + person('dau',556,410,.9,mood='sad') + '<circle cx="600" cy="330" r="10" fill="#E5B93C" stroke="#8A6510" stroke-width="2"/>'
  + label(390,448,'The taxman',size=17) + label(556,448,'Their daughter',size=17), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 620 470" width="560"')

def tug():
    g = []
    # ground centre line + skid marks + losing arrow
    g.append('<path d="M650,392 L650,448" stroke="#B3202A" stroke-width="5" stroke-dasharray="10 8"/><text x="650" y="466" text-anchor="middle" style="font:800 13px sans-serif;fill:#7A0F1A;letter-spacing:.12em">CENTRE</text>')
    g.append('<path d="M196,404 L276,402 M206,412 L270,410 M214,396 L262,395" stroke="#B9C2CC" stroke-width="4" stroke-linecap="round"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity=".9"/>' for x, y, r in ((268,392,7),(282,384,5),(256,386,4),(292,394,4))))
    g.append('<path d="M420,196 L580,196" stroke="#FF6F6B" stroke-width="6" stroke-linecap="round"/><path d="M580,182 L604,196 L580,210Z" fill="#FF6F6B"/><text x="500" y="182" text-anchor="middle" style="font:900 22px Georgia;fill:#FF8A86">Losing ground</text>')
    # people
    g.append('<g transform="translate(24,0) rotate(12 300 400)">' + person('john',300,400,1.0,arm='hold',mood='shock') + '</g>')
    xs = [850, 990, 1130]
    for k, (kind, nm) in enumerate([('rc','Compound'), ('rr','Risk'), ('rt','Tax')]):
        x = xs[k]
        g.append(f'<g transform="rotate(13 {x} 400)">' + person(kind, x, 400, .95, arm=None) + f'<rect x="{x-60}" y="232" width="120" height="34" rx="7" fill="#FBF6EA" stroke="#B3202A" stroke-width="2.5"/><text x="{x}" y="256" text-anchor="middle" style="font:900 21px Georgia;fill:#B3202A">{nm}</text></g>')
    # thick braided rope on top, at hand height
    rope = 'M372,318 C560,328 760,326 1210,316'
    g.append(f'<path d="{rope}" stroke="#6E4A22" stroke-width="22" fill="none" stroke-linecap="round"/><path d="{rope}" stroke="#C9A066" stroke-width="16" fill="none" stroke-linecap="round"/>'
             f'<path d="{rope}" stroke="#8A6236" stroke-width="16" fill="none" stroke-dasharray="7 9" stroke-linecap="butt"/>')
    # hands gripping the rope
    for hx, hy in ((372,318),(398,319),(842,322),(872,322),(982,321),(1012,321),(1122,319),(1152,318)):
        g.append(f'<circle cx="{hx}" cy="{hy}" r="12" fill="#F1C9A0" stroke="#B88A60" stroke-width="2"/>')
    # flag tied to the rope, pulled past centre toward their side
    g.append('<g class="tugFlag"><path d="M760,326 L760,392" stroke="#7A0F1A" stroke-width="4"/><path d="M760,334 L812,348 L760,364Z" fill="#E8433A" stroke="#7A0F1A" stroke-width="2"/></g>'
             '<circle cx="760" cy="326" r="9" fill="#B3202A" stroke="#FFE7A6" stroke-width="2"/>')
    g.append(label(300,442,'John',size=20))
    return scene(ground(1300,400) + ''.join(g), 470)
TUG_SCENE = tug().replace('viewBox="0 0 1300 470" width="1300" height="470"','viewBox="180 160 1080 320" width="1080" height="320"')

SAFE = ('<svg viewBox="0 0 160 130" width="150" height="122" class="safeI"><rect x="18" y="14" width="124" height="104" rx="10" fill="#5A5F68" stroke="#2E3238" stroke-width="4"/>'
        '<rect x="30" y="26" width="100" height="80" rx="6" fill="#6E747E" stroke="#3E434C" stroke-width="3"/>'
        '<circle cx="96" cy="66" r="18" fill="#9AA1AB" stroke="#2E3238" stroke-width="3"/><path d="M96,52 L96,58 M96,74 L96,80 M82,66 L88,66 M104,66 L110,66" stroke="#2E3238" stroke-width="3"/>'
        '<rect x="40" y="40" width="34" height="18" rx="2" fill="#7FB07A" stroke="#3E6B3A" stroke-width="2"/><rect x="40" y="62" width="34" height="18" rx="2" fill="#7FB07A" stroke="#3E6B3A" stroke-width="2"/>'
        '<g transform="translate(118,8)"><path d="M-12,4 V-6 a12,12 0 0 1 24,0 V4" fill="none" stroke="#C9A227" stroke-width="5"/><rect x="-17" y="2" width="34" height="26" rx="5" fill="#E5B93C" stroke="#8A6510" stroke-width="3"/><circle cy="13" r="3.5" fill="#5A3A12"/></g>'
        '<rect x="26" y="118" width="16" height="8" fill="#2E3238"/><rect x="118" y="118" width="16" height="8" fill="#2E3238"/></svg>')

def fireplace_scene():
    g = []
    g.append('<rect x="460" y="120" width="380" height="280" fill="#8A3A2A"/>' + ''.join(f'<path d="M460,{140+k*28} H840" stroke="rgba(0,0,0,.18)" stroke-width="2"/>' for k in range(9)))
    g.append('<rect x="440" y="100" width="420" height="30" rx="4" fill="#5A3A22"/><rect x="530" y="200" width="240" height="200" rx="110" fill="#1A0A06"/><rect x="530" y="300" width="240" height="100" fill="#1A0A06"/>')
    g.append('<path class="tFl" d="M600,398 C570,360 590,320 615,290 C620,320 640,330 640,350 C650,330 660,300 650,270 C690,310 700,360 690,398Z" fill="#FF8A2A"/>')
    g.append('<path class="tFl" d="M620,398 C605,370 615,345 630,330 C635,350 650,355 652,370 C660,358 664,340 660,325 C680,350 684,378 676,398Z" fill="#FFD27A"/>')
    g.append('<g transform="translate(590,330) rotate(-16)"><rect x="-38" y="-24" width="76" height="48" fill="#FBF6EA"/><text y="-2" text-anchor="middle" style="font:900 12px Georgia;fill:#2E1E12">MORTGAGE</text><text y="14" text-anchor="middle" style="font:700 11px Georgia;fill:#B3202A">PAID</text></g>')
    g.append('<g transform="translate(700,340) rotate(14)"><rect x="-38" y="-24" width="76" height="48" fill="#FBF6EA"/><text y="-2" text-anchor="middle" style="font:900 12px Georgia;fill:#2E1E12">CLINIC LOAN</text><text y="14" text-anchor="middle" style="font:700 11px Georgia;fill:#B3202A">PAID</text></g>')
    import random as _r; _r.seed(7)
    g.append(''.join(f'<rect class="conf" style="animation-delay:-{_r.uniform(0,3):.2f}s" x="{_r.randint(220,1080)}" y="{_r.randint(20,200)}" width="9" height="14" rx="2" fill="{_r.choice(["#E5B93C","#B3202A","#7BE3AE","#FFFFFF"])}" transform="rotate({_r.randint(0,90)})"/>' for _ in range(40)))
    g.append(person('john',330,400,.95,arm='up') + person('emma',990,400,.9,arm='up'))
    return scene(ground(1300,400) + ''.join(g), 430)
DEBT_SCENE = fireplace_scene()

def court():
    g = ['<g transform="translate(160,215)"><path d="M0,-150 L0,40" stroke="#C9A227" stroke-width="8"/><rect x="-50" y="40" width="100" height="14" rx="4" fill="#C9A227"/>',
         '<g class="scaleB" transform="rotate(-12)"><path d="M-110,-140 L110,-140" stroke="#C9A227" stroke-width="7" stroke-linecap="round"/>',
         '<path d="M-110,-140 L-140,-70 M-110,-140 L-80,-70 M110,-140 L80,-70 M110,-140 L140,-70" stroke="#C9A227" stroke-width="2.5"/>',
         '<path d="M-150,-70 Q-110,-40 -70,-70Z" fill="#E5B93C"/><path d="M70,-70 Q110,-40 150,-70Z" fill="#E5B93C"/>',
         '<text x="-110" y="-80" text-anchor="middle" style="font:900 13px Georgia;fill:#FFE7A6">FAMILY</text><text x="110" y="-80" text-anchor="middle" style="font:900 13px Georgia;fill:#FFE7A6">CRA</text></g>',
         '<circle cy="-150" r="10" fill="#E5B93C"/></g>',
         '<g transform="translate(300,300) rotate(-30)"><rect x="-70" y="-18" width="140" height="36" rx="10" fill="#7A4A2A"/><rect x="-22" y="-22" width="12" height="44" fill="#E5B93C"/><rect x="10" y="-22" width="12" height="44" fill="#E5B93C"/><rect x="-6" y="18" width="12" height="90" rx="5" fill="#5A3A22"/></g>',
         '<rect x="230" y="345" width="120" height="22" rx="6" fill="#5A3A22"/>']
    return '<svg viewBox="0 0 380 380" width="300" height="300" class="courtI" aria-hidden="true">' + ''.join(g) + '</svg>'
COURT = court()

# 2 HOOK
slide(f'''
{HOOK_HALF}
<div class="kick red">A real case &middot; Ontario &middot; CTV News, 2025</div>
<h2 class="lft">Every year, Canadian families give the biggest gift of their lives&hellip;</h2>
<p class="lft big f">&hellip;to the taxman. <span class="red">Most never meant to.</span></p>
<p class="lft f realC">This is not part of John&rsquo;s story. <b>This really happened to a family in Ontario.</b></p>
<div class="hookCol f">
  <div class="hookCard"><span>Their parents&rsquo; RRSPs</span><b>&asymp; $715,000</b></div>
  <div class="hookCard tax"><span>Tax bill</span><b>$660,000+</b></div>
  <div class="hookCard left"><span>What was left</span><b>Almost nothing</b></div>
</div>
<p class="lft f hkEnd">Both parents died in the same year. Their daughter used nearly all of their retirement savings to pay the tax. <b>There was no plan for it.</b></p>
<div class="src srcR">Source: CTV News Toronto, &ldquo;Daughter hit with $660,000 tax bill when both parents died in same year&rdquo; (September 2025).</div>
''', 'sHook sHalf')

# 2b HOW TONIGHT WORKS
slide('''
<div class="kick">Tonight</div>
<h2>That family didn&rsquo;t do anything wrong. <span class="gold">They just didn&rsquo;t have a plan.</span></h2>
<p class="big">So instead of slides full of rules, I&rsquo;m going to show you what a plan looks like, through one story.</p>
<div class="prec">
  <div class="pcC f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5C4.7 19 4 18.3 4 17.5Z"/><path d="M20 5.5c0-.8-.7-1.5-1.5-1.5H13v15h5.5c.8 0 1.5-.7 1.5-1.5Z"/><path d="M6.5 8h2.5M6.5 11h2.5M15 8h2.5M15 11h2.5"/></svg></i><b>The family is fictional</b><span>John, his wife and his kids are made up, so we can follow a whole lifetime in 40 minutes.</span></div>
  <div class="pcC f gold"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16"/><rect x="5" y="12" width="3" height="6" rx=".6"/><rect x="10.5" y="8" width="3" height="10" rx=".6"/><rect x="16" y="4" width="3" height="14" rx=".6"/></svg></i><b>The numbers are real</b><span>A real Equitable policy illustration, and real Canadian cases along the way.</span></div>
  <div class="pcC f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14"/><circle cx="12" cy="17.2" r=".9" fill="currentColor" stroke="none"/></svg></i><b>Ask yourself one question</b><span>As you watch, ask: <strong>&ldquo;Is this me?&rdquo;</strong></span></div>
</div>
''', 'sPrec')

# 3 TWO OWNERS
slide(f'''
<h2 class="mt">This is a story about two business owners.</h2>
<p class="big">Same life. Same income. Same chances. <b class="gold">One decision apart.</b></p>
{scene(ground(1300,430)+person('john',520,420,1.15)+person('jake',780,420,1.15)+label(520,460,'John',size=24)+'<g class="f">'+label(780,460,'Jake','#5E6670',24)+'</g>', 470)}
<p class="once f">Once upon a time&hellip;</p>
''', 'sTwo')

# 4b MEET JOHN
MEET = half_svg('<rect x="-400" y="-900" width="1520" height="905" fill="#14101E"/><rect width="720" height="810" fill="url(#mtSky)"/>' + STARS(34, 330, 8)
  + house(130, 640, 1.0) + snow_floor(630)
  + person('john', 285, 650, 1.45) + person('emma', 405, 650, 1.36) + person('lily', 500, 650, .9) + person('max', 572, 650, .76)
  + label(285, 690, 'John, 40', size=22) + label(405, 690, 'Emma, 39', size=22) + label(500, 690, 'Lily, 6', size=20) + label(574, 690, 'Max, 4', size=20),
  '<linearGradient id="mtSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14101E"/><stop offset="1" stop-color="#3A1A28"/></linearGradient>')
slide(f'''
{MEET}
<div class="meetR">
    <div class="kick" style="text-align:left">Meet John</div>
    <h2 class="lft">A dentist in BC who gives everything to his patients.</h2>
    <ul class="meetL">
      <li class="f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3.5c-2.5 0-3.5 2-3.5 4.5 0 2.5 1.2 4 1.8 6.5.5 2.5.8 6 2.4 6 1.5 0 1.6-3.5 2.3-5.5.5-1.4 1.5-1.4 2 0 .7 2 .8 5.5 2.3 5.5 1.6 0 1.9-3.5 2.4-6 .6-2.5 1.8-4 1.8-6.5 0-2.5-1-4.5-3.5-4.5-2 0-2.8 1-5 1s-3-1-5-1Z"/></svg></i><span><b>40 years old</b>, ten years into running his own clinic</span></li>
      <li class="f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10Z"/></svg></i><span>Married to <b>Emma</b> (39). <b>Lily</b> (6) wants to be a dentist like Dad. <b>Max</b> (4) wants to be a hockey player.</span></li>
      <li class="f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg></i><span>Works <b>55 hours a week</b>. This year he missed Lily&rsquo;s school concert.</span></li>
      <li class="f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="9" cy="7" rx="5" ry="2.5"/><path d="M4 7v4c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5V7"/><ellipse cx="15" cy="13.5" rx="5" ry="2.5"/><path d="M10 13.5v4c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5v-4"/></svg></i><span>A great income, a disciplined saver, and <b>no real plan</b> tying it all together</span></li>
    </ul>
    <p class="meetQ f">&ldquo;I built a great practice. I just never had time to build a plan.&rdquo;</p>
    <p class="f lft meetSF">Sound familiar?</p>
</div>
''', 'sMeet sHalf', hud=H(40, NW(40)))

# ---- full-screen chapter title pages
def full_svg(inner, defs='', top='#1A0A10'):
    inner = f'<rect x="-600" y="-900" width="2640" height="905" fill="{top}"/>' + inner
    return f'<svg class="ratSvg" viewBox="0 0 1440 810" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>{defs}</defs>{inner}</svg>'
def chap_full(num, when, title, svg, cls, hud=None, chips=''):
    ch = f'<div class="fChips">{chips}</div>' if chips else ''
    slide(f"""{svg}{ch}<div class="ratTop"><div class="chNum">{num}</div><div class="chWhen">{when}</div><h1>{title}</h1></div>""", cls + ' sFull', hud=hud)
def chips(*items):
    return ''.join(f'<div class="fChip f">{t}</div>' for t in items)
def wall_room(c1, c2, stripe='rgba(255,255,255,.04)'):
    return (f'<rect width="1440" height="810" fill="url(#wr)"/>' + ''.join(f'<path d="M{x},0 V640" stroke="{stripe}" stroke-width="20"/>' for x in range(30, 1440, 60))
            + '<rect y="640" width="1440" height="170" fill="#5A3A22"/>' + ''.join(f'<path d="M{x},640 V810" stroke="rgba(0,0,0,.25)" stroke-width="2"/>' for x in range(60, 1440, 100))
            + '<rect y="630" width="1440" height="12" fill="#E8D6B0"/>', f'<linearGradient id="wr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
def win(x, y, w, h, extra=''):
    import random as _r; _r.seed(x)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0E1A30"/>' + ''.join(f'<circle cx="{_r.randint(x+10,x+w-10)}" cy="{_r.randint(y+10,y+h-40)}" r="2.2" fill="#fff" opacity=".85"/>' for _ in range(int(w*h/2500)))
            + extra + f'<path d="M{x},{y+h-24} Q{x+w*.3},{y+h-36} {x+w*.55},{y+h-28} T{x+w},{y+h-30} V{y+h} H{x}Z" fill="#DCE6F0"/>'
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#E8D6B0" stroke-width="12"/><path d="M{x+w/2},{y} V{y+h} M{x},{y+h/2} H{x+w}" stroke="#E8D6B0" stroke-width="7"/>'
            + f'<rect x="{x-12}" y="{y+h-4}" width="{w+24}" height="14" fill="#C9B79C"/>')
def calendar(x, y, day):
    return (f'<g transform="translate({x},{y})"><rect x="-55" y="-60" width="110" height="120" rx="6" fill="#FBF6EA" stroke="#B9AE96" stroke-width="3"/><rect x="-55" y="-60" width="110" height="34" rx="6" fill="#B3202A"/>'
            f'<text y="-36" text-anchor="middle" style="font:900 18px Georgia;fill:#FFF4DC">DEC</text><text y="34" text-anchor="middle" style="font:900 54px Georgia;fill:#2E1E12">{day}</text></g>')
def office(extra_win=''):
    bg, d = wall_room('#1F3A3A', '#132626')
    shelf = '<g><rect x="1110" y="300" width="290" height="340" fill="#5A3A22"/>' + ''.join(f'<rect x="1110" y="{300+k*85}" width="290" height="10" fill="#3E2614"/>' for k in range(5))
    import random as _r; _r.seed(5)
    for k in range(4):
        x = 1122
        while x < 1386:
            w = _r.randint(14, 26); h = _r.randint(48, 70)
            shelf += f'<rect x="{x}" y="{385+k*85-h}" width="{w}" height="{h}" fill="{_r.choice(["#9E1B26","#2F6E4C","#C9962A","#3E5C76","#E8D6B0","#6B4A8A"])}"/>'
            x += w + 3
    shelf += '</g>'
    return bg + win(90, 300, 330, 240, extra_win) + shelf, d
def big_desk():
    return ('<rect x="480" y="560" width="560" height="26" rx="6" fill="#6B4226"/><rect x="500" y="586" width="520" height="230" fill="#5A3A22"/><rect x="500" y="586" width="520" height="230" fill="url(#gShade)" opacity=".45"/>'
            '<rect x="520" y="600" width="480" height="4" fill="rgba(255,255,255,.08)"/>')

# Chapter Two: The Meeting
def ch2():
    bg, d = office()
    paper = '<g transform="translate(700,552) rotate(-4)"><rect x="-70" y="-14" width="140" height="22" rx="2" fill="#F4E7C8" stroke="#C9A227" stroke-width="2"/><text y="2" text-anchor="middle" style="font:700 12px Georgia;fill:#7A0F1A">John&#8217;s wishlist</text></g>'
    return full_svg(bg + calendar(560, 380, '28') + person('john', 420, 690, 1.3, arm='hold') + person('mehar', 1020, 690, 1.3) + big_desk() + paper
                    + '<g transform="translate(900,556)"><rect x="-20" y="-18" width="40" height="22" rx="4" fill="#FFF"/><path d="M20,-12 c10,0 10,12 0,12" stroke="#FFF" stroke-width="4" fill="none"/></g>', d, '#1F3A3A')

# Chapter Three: He Starts Now
def ch3():
    fw = ''.join(f'<g transform="translate({cx},{cy})" class="fw" style="animation-delay:{dl}s">' + ''.join(f'<path d="M0,0 L{24*__import__("math").cos(k*0.785):.1f},{24*__import__("math").sin(k*0.785):.1f}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for k in range(8)) + '</g>'
                 for cx, cy, c, dl in ((170, 360, '#FFD27A', 0), (320, 340, '#FF6F6B', .6), (250, 420, '#7BE3AE', 1.2)))
    bg, d = office(fw)
    form = '<g transform="translate(740,552) rotate(-3)"><rect x="-80" y="-16" width="160" height="26" rx="2" fill="#FBF6EA" stroke="#B9AE96" stroke-width="2"/><text y="2" text-anchor="middle" style="font:700 11px Georgia;fill:#2E1E12">APPLICATION</text></g>'
    pen = '<path d="M806,548 L842,520" stroke="#1E1E24" stroke-width="6" stroke-linecap="round"/><path d="M806,548 L800,554" stroke="#E5B93C" stroke-width="4"/>'
    return full_svg(bg + calendar(480, 340, '30') + tree(1290, 640, .9) + person('john', 800, 690, 1.3, arm='hold') + person('mehar', 1000, 690, 1.25, arm='up')
                    + big_desk() + gift(600, 560, 1.15, txt='THE PLAN') + form + pen, d, '#1F3A3A')

# Chapter Four: Location #2
def street(sky1, sky2):
    d = f'<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky1}"/><stop offset="1" stop-color="{sky2}"/></linearGradient>'
    import random as _r; _r.seed(9)
    g = '<rect width="1440" height="810" fill="url(#sk)"/>' + ''.join(f'<circle cx="{_r.randint(0,1440)}" cy="{_r.randint(10,330)}" r="{_r.choice([1.2,1.8,2.4])}" fill="#fff" opacity=".7"/>' for _ in range(60))
    g += '<path d="M0,520 L120,470 L260,500 L420,450 L600,490 L780,440 L960,486 L1140,446 L1300,480 L1440,456 V640 H0Z" fill="rgba(20,20,40,.45)"/>'
    g += '<path d="M0,620 Q360,590 720,612 T1440,606 V810 H0Z" fill="#E8EEF6"/><path d="M0,640 Q360,616 720,634 T1440,630" stroke="rgba(160,170,190,.6)" stroke-width="3" fill="none"/>'
    return g, d
def ch4():
    g, d = street('#2A1E46', '#5A3A5E')
    banner = '<g transform="translate(760,640)"><path d="M-60,0 L-40,-110 M60,0 L40,-110" stroke="#5A3A22" stroke-width="8"/><rect x="-64" y="-120" width="128" height="78" rx="6" fill="#B3202A" stroke="#FFE7A6" stroke-width="3"/><text y="-88" text-anchor="middle" style="font:900 20px Georgia;fill:#FFE7A6">GRAND</text><text y="-60" text-anchor="middle" style="font:900 20px Georgia;fill:#FFE7A6">OPENING</text></g>'
    ribbon = '<path d="M820,600 C900,590 960,612 1000,598 C1060,612 1120,590 1180,600" stroke="#C62D3A" stroke-width="10" fill="none"/><path d="M990,590 l-24,30 M1010,590 l24,30" stroke="#C62D3A" stroke-width="8"/><circle cx="1000" cy="596" r="12" fill="#C62D3A"/>'
    sc = '<g transform="translate(1000,560) rotate(-20)"><path d="M0,0 L70,-14 M0,0 L70,14" stroke="#B9C2CC" stroke-width="8" stroke-linecap="round"/><circle cx="-14" cy="-10" r="12" fill="none" stroke="#E5B93C" stroke-width="6"/><circle cx="-14" cy="10" r="12" fill="none" stroke="#E5B93C" stroke-width="6"/></g>'
    return full_svg(g + clinic(330, 620, 1.35, 1) + clinic(1000, 620, 1.6, 2) + banner + person('emma', 560, 700, 1.0, arm='up') + person('lily', 640, 700, .66, arm='up') + person('max', 700, 700, .56)
                    + ribbon + person('john', 900, 710, 1.15, 'coat', arm='hold') + person('raj', 1100, 710, 1.15, 'coat', arm='hold') + sc, d, '#2A1E46')

# Chapter Five: The Storm
def ch5():
    d = '<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14141E"/><stop offset="1" stop-color="#3A3446"/></linearGradient>'
    import random as _r; _r.seed(4)
    rain = ''.join(f'<line class="rain" style="animation-delay:-{_r.uniform(0,1):.2f}s" x1="{x}" y1="{_r.randint(250,330)}" x2="{x-14}" y2="{_r.randint(360,420)}" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>' for x in range(20, 1440, 26))
    g = ('<rect width="1440" height="810" fill="url(#st)"/>' + cloud(260, 300, 1.3) + cloud(640, 270, 1.6) + cloud(1060, 300, 1.4) + cloud(1340, 320, 1.0) + rain
         + '<path d="M760,330 L720,430 L760,426 L726,520 L812,400 L770,404 L800,330Z" fill="#FFE08A" class="bolt"/>'
         + '<path d="M0,620 Q360,600 720,615 T1440,610 V810 H0Z" fill="#C9D2DC"/>'
         + clinic(250, 625, 1.25, 1) + clinic(1210, 625, 1.25, 2) + umbrella(720, 470, 1.25) + person('john', 670, 700, 1.15, arm='hold', mood='shock') + person('emma', 790, 700, 1.1))
    return full_svg(g, d, '#14141E')

# Chapter Six: Retirement
def ch6():
    g, d = street('#3A2050', '#E08A5A')
    keys = '<g transform="translate(724,560)"><circle r="12" fill="none" stroke="#E5B93C" stroke-width="5"/><path d="M8,8 L30,30 M22,22 L28,16 M26,26 L32,20" stroke="#E5B93C" stroke-width="5" stroke-linecap="round"/></g>'
    return full_svg(g + clinic(220, 610, 1.15, 1) + clinic(520, 610, 1.15, 2) + clinic(1260, 610, 1.15, 3)
                    + person('john', 680, 710, 1.2, arm='hold') + keys + person('lily', 820, 710, 1.12, arm='hold') + person('emma', 960, 710, 1.05) + person('max', 1070, 710, 1.1), d, '#3A2050')

# Chapter Seven: The Last Christmas
def ch7():
    bg, d = wall_room('#6B2A22', '#3E1610', 'rgba(255,220,170,.05)')
    fire = ('<rect x="560" y="390" width="320" height="250" fill="#8A3A2A"/><rect x="540" y="372" width="360" height="24" rx="4" fill="#5A3A22"/><rect x="630" y="460" width="180" height="180" rx="90" fill="#1A0A06"/><rect x="630" y="550" width="180" height="90" fill="#1A0A06"/>'
            '<path class="tFl" d="M680,638 C660,600 676,566 700,540 C704,566 720,574 720,592 C732,576 740,552 732,530 C762,566 768,610 758,638Z" fill="#FF9A3A"/><path class="tFl" d="M700,638 C690,614 698,594 712,582 C714,600 726,604 728,618 C736,606 738,592 736,580 C750,602 752,624 744,638Z" fill="#FFD27A"/>'
            '<path d="M540,372 Q600,392 660,372 T780,372 T900,372" stroke="#2F6E4C" stroke-width="12" fill="none"/>' + ''.join(f'<circle cx="{560+k*44}" cy="{378 + (6 if k%2 else 0)}" r="6" fill="{["#FF4D5E","#FFD27A","#7BE3AE"][k%3]}"/>' for k in range(8)))
    return full_svg(bg + win(90, 300, 300, 240) + fire + tree(1290, 640, 1.0)
                    + person('john', 200, 700, 1.15, 'old') + person('emma', 310, 700, 1.08, 'old')
                    + person('lily', 430, 700, 1.05) + person('lsp', 525, 700, 1.1)
                    + person('lily', 640, 712, .52) + person('max', 700, 712, .48) + person('lily', 770, 712, .5) + person('max', 830, 712, .44)
                    + person('max', 960, 700, 1.08) + person('msp', 1060, 700, 1.02)
                    , d, '#6B2A22')

# 4 CHAPTER 1: THE RAT RACE (full-screen split)
def rat_race():
    import random as _r; _r.seed(11)
    L = []
    # ---- left: cold office at night
    L.append('<defs><linearGradient id="rOff" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2230"/><stop offset="1" stop-color="#0E131C"/></linearGradient>'
             '<linearGradient id="rHome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A3424"/><stop offset="1" stop-color="#4A1C14"/></linearGradient>'
             '<radialGradient id="rLamp" cx=".5" cy="0" r="1"><stop offset="0" stop-color="rgba(255,226,150,.55)"/><stop offset="1" stop-color="rgba(255,226,150,0)"/></radialGradient>'
             '<radialGradient id="rFire" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="rgba(255,170,80,.55)"/><stop offset="1" stop-color="rgba(255,170,80,0)"/></radialGradient>'
             '<clipPath id="rcL"><rect width="720" height="810"/></clipPath><clipPath id="rcR"><rect x="720" width="720" height="810"/></clipPath></defs>')
    L.append('<g clip-path="url(#rcL)"><rect width="720" height="810" fill="url(#rOff)"/>')
    L.append('<g transform="translate(26,0)"><rect x="30" y="280" width="270" height="260" fill="#0A1426"/><path d="M30,500 Q100,486 165,494 T300,490 V540 H30Z" fill="#DCE6F0"/><rect x="30" y="280" width="270" height="260" fill="none" stroke="#4A5568" stroke-width="14"/><path d="M165,280 V540 M30,410 H300" stroke="#4A5568" stroke-width="8"/><rect x="20" y="536" width="290" height="14" fill="#3A4558"/></g>'
             + ''.join(f'<circle cx="{_r.randint(68,316)}" cy="{_r.randint(292,480)}" r="{_r.choice([1.5,2,2.5])}" fill="#DDE6F0" opacity=".85"/>' for _ in range(28)))
    L.append('<g transform="translate(612,372)"><circle r="46" fill="#F4ECD6" stroke="#8A6510" stroke-width="6"/>' + ''.join(f'<line y1="-38" y2="-31" stroke="#3A2A1A" stroke-width="3" transform="rotate({k*30})"/>' for k in range(12))
             + '<line y1="4" y2="-22" stroke="#3A2A1A" stroke-width="6" stroke-linecap="round" transform="rotate(229)"/><line y1="6" y2="-34" stroke="#3A2A1A" stroke-width="4" stroke-linecap="round" transform="rotate(234)"/><circle r="4" fill="#3A2A1A"/></g>')
    L.append(person('john', 360, 690, 1.35, 'coat', mood='sad', arm='hold'))
    L.append('<path d="M326,388 C318,376 322,368 330,364" stroke="#BFE3F5" stroke-width="5" fill="none" stroke-linecap="round"/>')
    L.append('<rect x="40" y="560" width="660" height="30" rx="6" fill="#5A3A22"/><rect x="60" y="590" width="620" height="230" fill="#4A2E1A"/><rect x="60" y="590" width="620" height="230" fill="url(#gShade)" opacity=".5"/>')
    for bx, n in ((95, 9), (520, 7), (600, 11)):
        L.append(''.join(f'<rect x="{bx + _r.randint(-4,4)}" y="{556 - k*13}" width="{70 + _r.randint(-6,6)}" height="12" rx="2" fill="{_r.choice(["#E8E2D2","#D9C9A4","#F4EBDD","#C9B79C"])}" stroke="#8A7A5A" stroke-width="1.5"/>' for k in range(n)))
    L.append('<rect x="200" y="470" width="150" height="90" rx="6" fill="#20262E" stroke="#4A5260" stroke-width="5"/><rect x="210" y="480" width="130" height="66" fill="#3E7FB8" opacity=".85"/><rect x="262" y="555" width="26" height="10" fill="#4A5260"/>')
    L.append('<path d="M226,525 L250,505 L270,515 L300,492 L326,500" stroke="#E8F4FF" stroke-width="3" fill="none"/>')
    L.append('<g transform="translate(440,540)"><rect x="-34" y="-14" width="68" height="20" rx="6" fill="#2A2E36"/><path d="M-28,-14 C-28,-34 28,-34 28,-14" stroke="#2A2E36" stroke-width="10" fill="none"/>'
             '<path d="M44,-40 l10,-8 M50,-26 l14,-2 M44,-12 l12,6" stroke="#FF6F6B" stroke-width="3" stroke-linecap="round" class="ring"/></g>')
    L.append('<g transform="translate(150,548)"><rect x="-14" y="-24" width="28" height="30" rx="4" fill="#E8E2D2"/><path d="M14,-16 c10,0 10,14 0,14" stroke="#E8E2D2" stroke-width="4" fill="none"/></g>')
    L.append('<rect width="720" height="810" fill="rgba(10,20,40,.18)"/></g>')
    # ---- right: warm home, sad family
    L.append('<g clip-path="url(#rcR)"><rect x="720" width="720" height="810" fill="url(#rHome)"/>'
             + ''.join(f'<path d="M{x},0 V810" stroke="rgba(255,220,170,.05)" stroke-width="18"/>' for x in range(740, 1440, 48)))
    L.append('<rect x="720" y="640" width="720" height="170" fill="#5A3A22"/>' + ''.join(f'<path d="M{x},640 V810" stroke="rgba(0,0,0,.25)" stroke-width="2"/>' for x in range(760, 1440, 90)) + '<rect x="720" y="632" width="720" height="10" fill="#E8D6B0"/>')
    L.append('<g transform="translate(880,290) scale(.85)"><circle r="62" fill="none" stroke="#2F6E4C" stroke-width="26"/><circle r="62" fill="none" stroke="#3E8A5E" stroke-width="10" stroke-dasharray="6 10"/>' + ''.join(f'<circle cx="{62*__import__("math").cos(k*0.7):.0f}" cy="{62*__import__("math").sin(k*0.7):.0f}" r="6" fill="#C62D3A"/>' for k in range(9)) + '<ellipse cx="-16" cy="58" rx="16" ry="10" fill="#C62D3A"/><ellipse cx="16" cy="58" rx="16" ry="10" fill="#C62D3A"/><circle cy="58" r="7" fill="#9E1B26"/><path d="M-4,62 L-14,88 M4,62 L14,88" stroke="#C62D3A" stroke-width="7" stroke-linecap="round"/></g>')
    L.append('<rect x="1030" y="400" width="240" height="240" fill="#8A3A2A"/><rect x="1015" y="385" width="270" height="22" rx="4" fill="#5A3A22"/><rect x="1080" y="470" width="140" height="170" rx="70" fill="#1A0A06"/><rect x="1080" y="550" width="140" height="90" fill="#1A0A06"/>'
             '<ellipse cx="1150" cy="590" rx="150" ry="110" fill="url(#rFire)"/><path class="tFl" d="M1120,638 C1100,600 1118,570 1140,548 C1144,572 1160,578 1160,595 C1170,580 1176,560 1170,540 C1196,570 1200,612 1192,638Z" fill="#FF9A3A"/>'
             '<path class="tFl" d="M1136,638 C1128,616 1136,598 1148,588 C1150,604 1160,606 1162,618 C1168,608 1170,596 1168,586 C1180,604 1182,624 1176,638Z" fill="#FFD27A"/>')
    for k, (cx, t) in enumerate(((1060, 'EMMA'), (1110, 'LILY'), (1160, 'MAX'), (1225, 'DAD'))):
        L.append(f'<g transform="translate({cx},408)"><path d="M-14,0 V40 C-14,56 4,60 16,50 L22,44 C14,40 10,34 10,26 V0Z" fill="{"#B3202A" if t != "DAD" else "#2F6E4C"}" stroke="#FFF4DC" stroke-width="2"/><rect x="-16" y="-4" width="28" height="12" rx="3" fill="#FFF4DC"/></g>')
    L.append('<text x="1225" y="448" text-anchor="middle" style="font:900 9px sans-serif;fill:#FFF4DC">DAD</text>')
    L.append(tree(1360, 640, 1.05))
    L.append('<g transform="translate(860,640)"><rect x="-80" y="-120" width="160" height="80" rx="18" fill="#3E5C76"/><rect x="-96" y="-150" width="40" height="120" rx="16" fill="#35506A"/><rect x="56" y="-150" width="40" height="120" rx="16" fill="#35506A"/><rect x="-80" y="-180" width="160" height="70" rx="20" fill="#35506A"/><rect x="-70" y="-40" width="10" height="40" fill="#2A2A2A"/><rect x="60" y="-40" width="10" height="40" fill="#2A2A2A"/></g>')
    L.append('<text x="860" y="575" text-anchor="middle" style="font:italic 700 16px Georgia;fill:rgba(255,231,166,.75)">Dad&rsquo;s chair</text>')
    L.append(person('emma', 980, 650, 1.1, mood='sad'))
    L.append(person('lily', 1070, 650, .78, mood='sad', arm='hold'))
    L.append('<g transform="translate(1108,520) rotate(6)"><rect x="-26" y="-34" width="52" height="40" fill="#FFF" stroke="#C9B79C" stroke-width="2"/><path d="M-6,-20 c-6,-8 -16,0 -8,8 l8,8 8,-8 c8,-8 -2,-16 -8,-8Z" fill="#E8433A"/><text y="2" text-anchor="middle" style="font:700 9px sans-serif;fill:#3A2A1A">FOR DAD</text></g>')
    L.append(person('max', 1250, 650, .62, mood='sad'))
    L.append(gift(1310, 650, .35) + gift(1395, 650, .3, '#2F6E4C'))
    L.append('</g>')
    # ---- divider + captions
    L.append('<rect x="714" y="0" width="12" height="810" fill="#C9962A"/><rect x="718" y="0" width="4" height="810" fill="#FFE7A6"/>')
    return '<svg class="ratSvg" viewBox="0 0 1440 810" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect x="-600" y="-900" width="1320" height="905" fill="#1A2230"/><rect x="720" y="-900" width="1320" height="905" fill="#7A3424"/>' + ''.join(L) + '</svg>'
slide(f'''
{rat_race()}
<div class="ratC l">7:39 p.m. &middot; still at the clinic</div><div class="ratC r">At home &middot; waiting for Dad</div>
<div class="ratTop"><div class="chNum">Chapter One</div><div class="chWhen">Christmas Eve, 2026 &middot; John is 40</div><h1>The Rat Race</h1></div>
''', 'sChap sRat', hud=H(40, NW(40)))

# 5 JOHN'S NUMBERS
rows = [('Clinic revenue', 'about $750K a year', ''), ('Practice loan', '$1M &middot; <b class="red">$500K still owing</b>', ''),
        ('Home', '$1.6M &middot; <b class="red">$1M mortgage</b>', ''), ('Clinic value', '$900K', ''),
        ('Corporate savings', '$500K retained earnings', ''), ('RRSP', '$150K', ''), ('TFSA', '$109K &middot; <b class="green">maxed out</b>', ''), ('Investing', '<b class="green">TFSA + RRSP maxed</b> &middot; <b class="red">nothing else</b>', ''), ('Insurance', '$500K term life &middot; $50K critical illness', '')]
rhtml = ''.join(f'<div class="bsR f"><span>{a}</span><b>{b}</b></div>' for a, b, _ in rows)
slide(f'''
<div class="kick">John&rsquo;s finances</div>
<h2>On paper, John is doing great.</h2>
<div class="split">
  <div class="bs">{rhtml}<div class="bsR tot f"><span>Net worth</span>{counter(int(NW(40)))}</div></div>
  <div class="sp">{scene(ground(520,420)+person('john',160,410,1.0,'coat')+person('emma',290,410,.92)+person('lily',380,410,.6)+person('max',450,410,.5)+label(160,452,'John')+label(290,452,'Emma, 39')+label(380,452,'Lily, 6')+label(450,452,'Max, 4'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')}</div>
</div>
''', 'sNums', hud=H(40, NW(40)))

# 6 RAT RACE: 3 RULES RED
slide(f'''
<div class="kick">The problem</div>
<h2>But inside his corporation, John&rsquo;s money is stuck.</h2>
<div class="tugW f">{TUG_SCENE}</div>
<div class="rules3">
  <div class="rc f"><div class="rI"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M19.5 8A8 8 0 0 0 5 9"/><path d="M19.5 3.5V8H15"/><path d="M4.5 16A8 8 0 0 0 19 15"/><path d="M4.5 20.5V16H9"/></svg></div><b>The Compound Effect</b><span>$500K of retained earnings sits in GICs, earning almost nothing.</span><em>Against him</em></div>
  <div class="rc f"><div class="rI"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5 21 19.5H3Z"/><path d="M12 9.5v5"/><circle cx="12" cy="17" r=".9" fill="currentColor" stroke="none"/></svg></div><b>The Risk Effect</b><span>Everything he owns is tied to one clinic and one house.</span><em>Against him</em></div>
  <div class="rc f"><div class="rI">%</div><b>The Tax Effect</b><span>Investment income in his corporation is taxed at about 50% in BC, every year.</span><em>Against him</em></div>
</div>
<p class="f mid">All three rules of money were working <b class="red">against</b> John.</p>
''', 'sRules', hud=H(40, NW(40)))

# 7 WISH LIST
def _phone(x, y, rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot})"><rect x="-9" y="-17" width="18" height="34" rx="4" fill="#1E1E24" stroke="#5A5F68" stroke-width="2"/><rect x="-6" y="-12" width="12" height="22" rx="2" fill="#7FB4E0"/></g>'
CALL = ('<svg viewBox="0 0 620 290" width="600" height="281" aria-hidden="true">'
  '<defs><clipPath id="clc"><circle cx="490" cy="150" r="100"/></clipPath></defs>'
  '<rect x="0" y="0" width="620" height="290" rx="18" fill="rgba(20,4,8,.45)" stroke="rgba(229,185,60,.45)"/>'
  + '<g transform="translate(0,-8)">' + person('john', 150, 280, .95, arm='hold') + _phone(196, 142, -18) + '</g>'
  + '<path d="M232,108 q12,-10 24,0 M240,92 q18,-16 36,0 M248,76 q24,-22 48,0" stroke="#F6D77A" stroke-width="4" fill="none" stroke-linecap="round" class="ring"/>'
  + '<circle cx="490" cy="150" r="104" fill="#E5B93C"/><g clip-path="url(#clc)"><rect x="380" y="40" width="220" height="220" fill="#1F3A3A"/>'
  + person('mehar', 490, 380, 1.3, arm='hold') + _phone(546, 205, 18) + '</g>'
  + bubble(250, 10, 210, ['&#8220;Mehar, it&#8217;s John.', 'Can we meet', 'this week?&#8221;'], 214, 120, size=16)
  + '</svg>')

wl = ['Pay off every debt in 10 years', 'Open more locations', 'Retire by 65', 'Take care of Emma and the kids, forever']
wlh = ''.join(f'<li class="f"><i class="box"></i>{w}</li>' for w in wl)
slide(f'''
<div class="split">
  <div class="scroll"><div class="scT">John&rsquo;s Christmas List</div><ul class="wl">{wlh}</ul><div class="scSig">&mdash; J.</div></div>
  <div class="sp2"><h2 class="lft">He wasn&rsquo;t asking for a sports car.</h2><p class="lft big">He wanted his <b>time</b> back, and a future his family could count on.</p><p class="lft f mid">So that same week, between Christmas and New Year&rsquo;s, <b>he called Mehar again.</b></p><div class="f callS">{CALL}</div></div>
</div>
''', 'sList', hud=H(40, NW(40)))

# 8 CHAPTER 2
chap_full('Chapter Two', 'December 28, 2026 &middot; John is 40', 'The Meeting', ch2(), 'sChap', hud=H(40, NW(40)))

# 8a TEN YEARS EARLIER
def _office_half(x0, sep):
    g = []
    g.append(f'<rect x="{x0}" y="0" width="650" height="520" fill="{"#3A3424" if sep else "#1F3A3A"}"/>' + ''.join(f'<path d="M{x},0 V440" stroke="rgba(255,255,255,.04)" stroke-width="16"/>' for x in range(x0+20, x0+650, 48)))
    g.append(f'<rect x="{x0}" y="440" width="650" height="80" fill="{"#5A4A32" if sep else "#5A3A22"}"/><rect x="{x0}" y="434" width="650" height="9" fill="#E8D6B0"/>')
    g.append(f'<rect x="{x0+40}" y="130" width="170" height="150" fill="#0E1A30" stroke="#E8D6B0" stroke-width="9"/><path d="M{x0+125},130 V280 M{x0+40},205 H{x0+210}" stroke="#E8D6B0" stroke-width="5"/>')
    g.append(f'<rect x="{x0+500}" y="150" width="130" height="290" fill="#5A3A22"/>' + ''.join(f'<rect x="{x0+508+k*20}" y="{170+r*72}" width="14" height="54" fill="{["#9E1B26","#2F6E4C","#C9962A","#3E5C76","#E8D6B0","#6B4A8A"][(k+r)%6]}"/>' for r in range(4) for k in range(6)))
    return ''.join(g)
def flash_split():
    defs = '<filter id="sepF"><feColorMatrix type="matrix" values=".39 .77 .19 0 0  .35 .69 .17 0 0  .27 .53 .13 0 0  0 0 0 1 0"/></filter>'
    L = '<g filter="url(#sepF)">' + _office_half(0, True) + person('john', 150, 470, 1.18) + person('mehar', 440, 470, 1.12) + '<rect x="160" y="380" width="360" height="20" rx="4" fill="#7A4A2A"/><rect x="175" y="400" width="330" height="120" fill="#5E3820"/>' + '</g>'
    Rh = _office_half(650, False) + person('john', 800, 470, 1.18, mood='sad') + person('mehar', 1100, 470, 1.12) + '<rect x="810" y="380" width="360" height="20" rx="4" fill="#7A4A2A"/><rect x="825" y="400" width="330" height="120" fill="#5E3820"/>'
    tags = ('<g><rect x="20" y="460" width="210" height="40" rx="20" fill="rgba(40,24,10,.85)" stroke="#C9A47A"/><text x="125" y="487" text-anchor="middle" style="font:700 21px Caveat,cursive;fill:#FFE7A6">2016 &#183; John is 30</text></g>'
            '<g><rect x="1070" y="460" width="210" height="40" rx="20" fill="rgba(10,30,30,.85)" stroke="#7BE3AE"/><text x="1175" y="487" text-anchor="middle" style="font:700 21px Caveat,cursive;fill:#CFF5E0">2026 &#183; John is 40</text></g>')
    div = '<rect x="646" y="0" width="8" height="520" fill="#C9962A"/><rect x="649" y="0" width="2" height="520" fill="#FFE7A6"/>'
    b1 = '<g class="f">' + bubble(40, 24, 280, ['&#8220;Let me think', 'about it&#8230;&#8221;'], 160, 162, size=22) + '</g>'
    b2 = '<g class="f">' + bubble(668, 18, 300, ['&#8220;I wish I&#8217;d listened', 'to you ten years ago.&#8221;'], 800, 162, size=20) + '</g>'
    b3 = '<g class="f">' + bubble(980, 10, 300, ['&#8220;That&#8217;s okay. We can&#8217;t', 'change the past. Let&#8217;s', 'focus on today, and', 'on your future.&#8221;'], 1100, 172, size=19, bold_last=True) + '</g>'
    return f'<svg class="flashSvg" viewBox="0 0 1300 520" width="1300" height="520" aria-hidden="true"><defs>{defs}</defs>{L}{Rh}{div}{tags}{b1}{b2}{b3}</svg>'
FLASH = flash_split()
slide(f'''
<div class="kick">But this wasn&rsquo;t their first meeting</div>
<h2>Ten years earlier, Mehar had shown John these same strategies.</h2>
{FLASH}
''', 'sFlash')

# 8b MEHAR'S PROCESS
STEPS = [('Listen', 'Your wishlist, your goals, your worries'),
         ('Check-up', 'The 7 key needs of your corporation'),
         ('Educate', 'The right dollar and the two buckets, explained simply'),
         ('Team up', 'Your accountant and lawyer at the same table'),
         ('Design', 'A plan built for you, with a real illustration'),
         ('Start', 'Put it in place right away, not someday'),
         ('Review', 'Every year, and whenever life changes')]
slide('''
<div class="kick">The Team All In service</div>
<h2>Mehar walked John through it, <span class="gold">step by step.</span></h2>
<p class="big">In ten years of business, nobody had ever done this for John.</p>
<div class="road">''' + ''.join(f'<div class="rdS f"><i>{k+1}</i><b>{t}</b><span>{d}</span></div>' for k, (t, d) in enumerate(STEPS)) + '''</div>
<p class="f mid roadEnd">A process, not a product. <b class="gold">That&rsquo;s the Team All In difference.</b></p>
''', 'sRoad', hud=H(40, NW(40)))

# 8c THE FUNDAMENTALS + A COMPLETE PLAN
slide('''
<div class="kick">Where Mehar started</div>
<h2>First the fundamentals. <span class="gold">Then the whole family.</span></h2>
<div class="fund">
  <div class="fdC paper f"><h3>The fundamentals of money</h3><ul>
    <li><b>Saving:</b> pay yourself first, every month, before anything else.</li>
    <li><b>The 3 rules of money:</b><div class="fdTags"><em>Compound</em><em>Risk</em><em>Tax</em></div>Make all three work <i>for</i> you, not against you.</li>
    <li><b>The 3 goals of money:</b><div class="fdTags"><em class="g">Protection</em><em class="g">Income</em><em class="g">Legacy</em></div>Every dollar should serve at least one of them.</li>
  </ul></div>
  <div class="fdC paper f famCk"><h3>A complete plan for the family</h3><ul>
    <li><i class="ck">&#10003;</i><span><b>John&rsquo;s protection:</b> from $500K term + $50K critical illness up to <b>$2.5M life (permanent + term) + $250K critical illness</b></span></li>
    <li><i class="ck">&#10003;</i><span><b>John&rsquo;s flexible plan:</b> savings and investments, <em>more on that later</em></span></li>
    <li><i class="ck">&#10003;</i><span><b>Emma:</b> her own protection, savings and retirement plan</span></li>
    <li><i class="ck">&#10003;</i><span><b>Lily &amp; Max:</b> education savings and coverage, locked in young</span></li>
  </ul></div>
</div>
<p class="focus f">A complete job means the whole family. <b>Tonight, we&rsquo;re focusing on what Mehar did for John&rsquo;s corporation.</b></p>
''', 'sFund', hud=H(40, NW(40)))

# 9 7 NEEDS: SANTA'S CHECKLIST
NEED_NOTES = [('Delayed taxes', 'corporate savings taxed every year'), ('Wealth transfer', 'big tax bill for family'),
              ('Key person', 'clinic stops if John can&rsquo;t work'), ('Buy &amp; sell', 'no funded plan if a partner dies'),
              ('Debt', '$1.5M owing, no backstop'), ('Liquidity', 'no cash when opportunity knocks'),
              ('Estate equalization', 'no fair split for Lily &amp; Max')]
def _need(k, t, d):
    box = '<svg class="hbx" viewBox="0 0 40 40" width="34" height="34"><path d="M5,6 C14,4 26,5 35,5 C36,15 35,26 36,35 C26,36 14,35 5,36 C4,26 5,15 5,6Z" fill="none" stroke="#3A2A1A" stroke-width="2.6" stroke-linecap="round"/><path class="hx" d="M9,10 L31,31 M31,9 L10,31" fill="none" stroke="#C0202E" stroke-width="4" stroke-linecap="round"/></svg>'
    return f'<li class="f">{box}<span class="hn">{t}</span><span class="hd">&mdash; {d}</span></li>'
slide('''
<div class="kick">The check-up</div>
<div class="santa paper">
  <div class="snH">The 7 Key Needs<small>of John&rsquo;s corporation</small></div>
  <ul class="snL">''' + ''.join(_need(k, t, d) for k, (t, d) in enumerate(NEED_NOTES)) + '''</ul>
  <div class="snT f">0 of 7 covered!</div>
</div>
''', 'sNeeds')

# 9a CORPORATE DOLLAR VS PERSONAL DOLLAR
def LOON(tax, cls):
    d = tax * 6.283 * 120
    return (f'<svg viewBox="-140 -140 280 280" width="300" height="300" class="lnS {cls}"><defs><clipPath id="lc{cls}"><polygon points="0.0,-120.0 64.9,-101.0 109.2,-49.8 118.8,17.1 90.7,78.6 33.8,115.1 -33.8,115.1 -90.7,78.6 -118.8,17.1 -109.2,-49.8 -64.9,-101.0"/></clipPath></defs>'
            f'<polygon points="0.0,-120.0 64.9,-101.0 109.2,-49.8 118.8,17.1 90.7,78.6 33.8,115.1 -33.8,115.1 -90.7,78.6 -118.8,17.1 -109.2,-49.8 -64.9,-101.0" fill="url(#gLoon)" stroke="#8A6510" stroke-width="5"/><polygon points="0.0,-104.0 56.2,-87.5 94.6,-43.2 102.9,14.8 78.6,68.1 29.3,99.8 -29.3,99.8 -78.6,68.1 -102.9,14.8 -94.6,-43.2 -56.2,-87.5" fill="none" stroke="rgba(120,80,10,.55)" stroke-width="3"/>'
            f'<text y="22" text-anchor="middle" style="font:900 64px Georgia;fill:#7A5A10">$1</text>'
            f'<g clip-path="url(#lc{cls})"><circle r="120" fill="none" class="tW" stroke-width="240" style="--d:{d:.0f}px" transform="rotate(-90)"/></g></svg>')
DL_MEHAR = scene(ground(220,400)+person('mehar',110,390,.95), 420).replace('viewBox="0 0 1300 420" width="1300" height="420"','viewBox="0 0 220 420" width="150" height="286"')
DL_JOHN = scene(ground(220,400)+person('john',110,390,.95), 420).replace('viewBox="0 0 1300 420" width="1300" height="420"','viewBox="0 0 220 420" width="150" height="286"')
slide(f'''
<div class="kick">First, Mehar explained one simple idea</div>
<h2>A <span class="red">personal</span> dollar vs a <span class="gold">corporate</span> dollar</h2>
<svg width="0" height="0" style="position:absolute"><defs><radialGradient id="gLoon" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#FFF0B0"/><stop offset=".5" stop-color="#E5B93C"/><stop offset="1" stop-color="#A87A12"/></radialGradient></defs></svg>
<div class="dlR">
  <div class="dlFig">{DL_MEHAR}</div>
  <div class="dlC f"><div class="dlT red">Personal dollar</div>{LOON(.5,'p')}<div class="dlV"><b class="red">50&cent;</b><span>left after personal tax</span></div></div>
  <div class="dlVs f">vs</div>
  <div class="dlC win f"><div class="dlT gold">Corporate dollar</div>{LOON(.12,'c')}<div class="dlV"><b class="green">88&cent;</b><span>left after corporate tax</span></div></div>
  <div class="dlFig">{DL_JOHN}</div>
</div>
<div class="dlTalk">
  <p class="f"><span class="who">Mehar</span>&ldquo;John, if you could pay for your future with either dollar, <b>which one would you use?</b>&rdquo;</p>
  <p class="f j"><span class="who">John</span>&ldquo;The 88-cent one. Obviously.&rdquo;</p>
</div>
<div class="src">Approximate BC rates: small business about 11%, top personal rate about 53.5%. Rounded for illustration. Not tax advice; confirm with your accountant.</div>
''', 'sDollar', hud=H(40, NW(40)))

# 9b TWO BUCKETS
_coins = ''.join(f'<g transform="translate({x},0)"><g class="coinF" style="animation-delay:{d}s"><ellipse rx="17" ry="17" fill="#F2CC5A" stroke="#A87A12" stroke-width="3"/><ellipse rx="10" ry="10" fill="none" stroke="#C99A2A" stroke-width="2"/><text y="6" text-anchor="middle" style="font:900 16px Georgia;fill:#8A6510">$</text></g></g>'
                 for x, d in [(-60,0),(30,.45),(-15,.9),(55,1.35),(-45,1.8),(10,2.25),(40,2.7),(-30,3.15)])
def cda_bucket(p, w=300, h=420, cls=''):
    coins = ''.join(f'<g transform="translate({x},0)"><g class="coinF" style="animation-delay:{d}s"><ellipse rx="17" ry="17" fill="#F2CC5A" stroke="#A87A12" stroke-width="3"/><ellipse rx="10" ry="10" fill="none" stroke="#C99A2A" stroke-width="2"/><text y="6" text-anchor="middle" style="font:900 16px Georgia;fill:#8A6510">$</text></g></g>'
                    for x, d in [(-60,0),(30,.45),(-15,.9),(55,1.35),(-45,1.8),(10,2.25),(40,2.7),(-30,3.15)])
    return (f'<svg viewBox="-160 -380 320 450" width="{w}" height="{h}" class="cdaB {cls}" style="overflow:visible">'
      f'<defs><clipPath id="cc{p}"><path d="M-117,-217 L117,-217 L92,-3 L-92,-3Z"/></clipPath>'
      f'<linearGradient id="gf{p}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A0"/><stop offset=".35" stop-color="#F2CC5A"/><stop offset="1" stop-color="#B8860B"/></linearGradient>'
      f'<radialGradient id="gh{p}"><stop offset="0" stop-color="rgba(255,215,100,.55)"/><stop offset="1" stop-color="rgba(255,215,100,0)"/></radialGradient></defs>'
      '<ellipse class="bkHalo" cx="0" cy="-100" rx="170" ry="150" fill="url(#gh{p})"/>'
      '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(229,185,60,.10)"/>'
      f'<g class="bkGlow"><g clip-path="url(#cc{p})"><g class="bkFill"><rect x="-130" y="-225" width="260" height="230" fill="url(#gf{p})"/>'
      '<path class="bkWave" d="M-260,-222 q32,-10 65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 L260,-200 L-260,-200Z" fill="#FFF1BF" opacity=".8"/>'
      + ''.join(f'<circle class="bkSpark" style="animation-delay:{k*.37:.2f}s" cx="{-70+k*20}" cy="-{30+(k*37)%150}" r="3" fill="#FFF8DC"/>' for k in range(8)) +
      '</g></g></g>' + coins +
      '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="none" stroke="#F2CC5A" stroke-width="7" stroke-linejoin="round"/>'
      '<text x="0" y="-104" text-anchor="middle" class="bkTxt">CDA</text></svg>')
CDA_BUCKET = cda_bucket('A', 300, 420)

slide('''
<div class="kick">What Mehar showed him</div>
<h2>Every dollar in John&rsquo;s corporation sits in one of <span class="gold">two buckets.</span></h2>
<div class="bkRow">
  <div class="bkC f"><svg viewBox="-160 -260 320 330" width="300" height="310"><path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(179,32,42,.18)" stroke="#E0303E" stroke-width="7" stroke-linejoin="round"/><text x="0" y="-92" text-anchor="middle" style="font:900 68px Georgia;fill:#FF7D78">%</text><g class="drip"><circle class="leak" style="animation-delay:0.0s" cx="-40" cy="20" r="11" fill="#E5B93C"/><circle class="leak" style="animation-delay:0.5s" cx="-20" cy="20" r="11" fill="#E5B93C"/><circle class="leak" style="animation-delay:1.0s" cx="0" cy="20" r="11" fill="#E5B93C"/><circle class="leak" style="animation-delay:1.5s" cx="20" cy="20" r="11" fill="#E5B93C"/><circle class="leak" style="animation-delay:2.0s" cx="40" cy="20" r="11" fill="#E5B93C"/></g></svg><b class="red">Taxable bucket</b><span>Salary, dividends, investment income: <strong>taxed on the way out</strong>, up to about half.</span></div>
  <div class="bkVs f">vs</div>
  <div class="bkC win f">'''+CDA_BUCKET+'''<b class="gold">Tax-free bucket</b><span>The Capital Dividend Account: <strong>every dollar comes out tax-free.</strong></span></div>
</div>
''', 'sBuckets', hud=H(40, NW(40)))

slide('''
<div class="kick">A question for the room</div>
<div class="askQ">What&rsquo;s sitting in <span class="red">your</span> corporation&rsquo;s <b>taxable bucket</b> right now?</div>
<p class="f mid">And how much of it could be in the <b class="gold">tax-free bucket</b> instead?</p>
''', 'sAsk')

BUBBLE = '<g class="f">' + bubble(46, -110, 260, ['Why didn&#8217;t anyone tell me', 'about this back then?'], 200, 118, size=20) + '</g>'
MBUB = '<g class="f">' + bubble(312, -196, 340, ['&#8220;We talked about this ten years', 'ago, my friend. The difference', 'today is that you&#8217;ve opened your', 'mind to learn. That&#8217;s okay. Let&#8217;s', 'learn from it, and focus on today', 'and your future.&#8221;'], 470, 132, size=18, bold_last=True) + '</g>'
SHOCK = scene(ground(700,420) + person('john',200,410,1.1,mood='shock') + person('mehar',470,410,1.05) + BUBBLE + MBUB, 470).replace('viewBox="0 0 1300 470" width="1300" height="470"','viewBox="0 -206 700 676" width="700" height="676"')
slide(f'''
<div class="split shockS">
  <div class="sp">{SHOCK}</div>
  <div class="sp2">
    <div class="kick" style="text-align:left">The moment</div>
    <h2 class="lft">This time, John was ready.</h2>
    <p class="lft big f">Mehar had shown him the tax-free bucket ten years earlier. <b>This time, John was ready to listen, and to learn.</b></p>
    <p class="lft big f"><b class="gold">&ldquo;How do I fill it?&rdquo;</b> he asked. <b>&ldquo;And how soon can we start?&rdquo;</b></p>
  </div>
</div>
''', 'sShock', hud=H(40, NW(40)))

# 15 CDA
slide(f'''
<div class="kick">The secret weapon</div>
<h2>The Capital Dividend Account (CDA)</h2>
<div class="split">
  <div class="sp cdaAuto cdaTF">{cda_bucket('B', 360, 490)}<div class="tfSeal"><b>TAX</b><b>FREE</b><span>&#10003;</span></div></div>
  <div class="cdaPts">
    <div class="f"><b>A notional account.</b> Not a bank account: a special tax account the corporation tracks, adding up the tax-free surpluses it has built.</div>
    <div class="f"><b>What fills it:</b> the non-taxable half of capital gains, capital dividends received from other corporations, and the big one: <b class="gold">life insurance paid to the corporation</b> (minus the policy&rsquo;s cost base).</div>
    <div class="f"><b>What it does:</b> the balance can be paid to Canadian-resident shareholders as <b class="green">capital dividends, completely tax-free</b>, once the corporation files an election with the CRA (Form T2054).</div>
    <div class="f"><b>Who can use it:</b> Canadian-controlled private corporations, like John&rsquo;s dental corporation.</div>
    <div class="f note3">David tracks the balance and files the election. Mehar fills it.</div>
  </div>
</div>
<div class="src">Source: Investopedia, &ldquo;Capital Dividend Account (CDA)&rdquo;, investopedia.com/terms/c/cda.asp; Canada Revenue Agency, capital dividend accounts.</div>
''', 'sCda', hud=H(40, NW(40)))

# 15b WHAT FILLS THE CDA
CF_IN = [(20, 'Capital gains', 'Non-taxable portion', 'The half of every capital gain that isn&rsquo;t taxed'),
         (128, '', 'Gains on goodwill', 'The non-taxable portion (formerly &ldquo;eligible capital property&rdquo;)'),
         (236, '', 'Capital dividends received', 'Tax-free dividends from other corporations'),
         (362, 'Biggest input', 'Corporate-owned life insurance', 'Death benefit minus the policy&rsquo;s cost base')]
def _cf_box(k, y, tag, t, d):
    big = k == 3; h = 104 if big else 88; cy = y + h/2
    path = f'M0,{h/2:.0f} C70,{h/2:.0f} 60,{262-y:.0f} 128,{262-y:.0f}'
    tg = f'<div class="cfTag{" g" if big else ""}">{"&#9733; " if big else ""}{tag}</div>' if tag else ''
    return (f'<div class="cfI paper f{" big" if big else ""}" style="top:{y}px;height:{h}px">{tg}<b>{t}</b><span>{d}</span>'
            f'<svg class="cfA" width="140" height="10" style="overflow:visible"><path d="{path}" class="cfP{" g" if big else ""}" marker-end="url(#cfArr{"G" if big else ""})"/></svg></div>')
CF_HTML = ''.join(_cf_box(k, *c) for k, c in enumerate(CF_IN))
slide(f'''
<div class="kick">How the tax-free bucket gets filled</div>
<h2>What fills the CDA</h2>
<svg width="0" height="0" style="position:absolute"><defs><marker id="cfArr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10Z" fill="#F2CC5A"/></marker><marker id="cfArrG" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10Z" fill="#7BE3AE"/></marker></defs></svg>
<div class="cfW">
  {CF_HTML}
  <div class="cfB cdaAuto">{cda_bucket('C', 250, 350)}<div class="cfBl">A running tally of tax-free dollars</div></div>
  <div class="cfO f"><svg class="cfA2" width="90" height="20" style="overflow:visible"><path d="M0,10 L78,10" class="cfP g" marker-end="url(#cfArrG)"/></svg>
    <div class="cfOut paper"><b>Paid out tax-free</b><span>As capital dividends to John,</span><span>and to his family through his estate</span></div></div>
</div>
<p class="f mid">Four inputs. One tax-free bucket. <b class="gold">For John, the policy is the big one.</b></p>
''', 'sCdaFill', hud=H(40, NW(40)))

# 10 3 HIDDEN PROBLEMS (with loonie)
slide(f'''
<div class="kick">What Mehar found</div>
<h2>Three hidden problems in John&rsquo;s business</h2>
<div class="probs">
  <div class="pb f"><div class="pbN">1</div><b>Double taxation</b><span>When John dies, his shares are taxed on his final return, and the same money is taxed again when the corporation pays it out to his family.</span></div>
  <div class="pb f"><div class="pbN">2</div>{SAFE}<b>Trapped money</b><span>Taking cash out of the corporation costs him about half. His dollar is worth 88&cent; inside, only 50&cent; outside.</span>
    <div class="loons"><div class="loon"><i style="--p:50%"></i></div><b class="red">50&cent;</b><div class="loon"><i style="--p:12%"></i></div><b class="green">88&cent;</b></div></div>
  <div class="pb f"><div class="pbN">3</div><b>Money not multiplying</b><span>His corporate savings sit in GICs, taxed every year. Nothing there is building on its own.</span></div>
</div>
''', 'sProbs', hud=H(40, NW(40)))

# 11 THE TEAM
slide(f'''
<div class="kick">The team</div>
<h2>John didn&rsquo;t replace his team. <span class="gold">He completed it.</span></h2>
{scene(ground(1300,400)+person('david',260,390,1.0)+person('john',520,390,1.05)+person('sarah',780,390,1.0)+person('mehar',1040,390,1.0)
       +label(260,430,'David, CPA',size=20)+label(520,430,'John',size=20)+label(780,430,'Sarah, lawyer',size=20)+label(1040,430,'Mehar, advisor',size=20), 440)}
<div class="roles">
  <div class="f"><b>David &middot; accountant</b><span>Tax returns, CDA tracking, capital dividend elections</span><q>&ldquo;I&rsquo;d watched his passive income get taxed every year. This finally fixed it.&rdquo;</q></div>
  <div class="f"><b>Sarah &middot; lawyer</b><span>Wills, holding company, shareholder agreement, estate freeze</span><q>&ldquo;Insurance with no agreements behind it is half a plan. We made every document match.&rdquo;</q></div>
  <div class="f"><b>Mehar &middot; advisor</b><span>The strategy: insurance, investments, and keeping everyone working together</span></div>
</div>
<p class="note2">John brought David and Sarah to the table himself.</p>
''', 'sTeam', hud=H(40, NW(40)))

# 12 CHAPTER 3
chap_full('Chapter Three', 'December 30, 2026 &middot; the same month', 'He Starts Now', ch3(), 'sChap', hud=H(40, NW(40), '0,4', '100'))

# 12b HOW IT'S STRUCTURED
slide('''
<div class="kick">How it&rsquo;s structured</div>
<h2>Who owns it, who pays, and who gets paid</h2>
<div class="stG">
  <div class="stC f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V6l8-3 8 3v14"/><path d="M3 20h18"/><path d="M8 9h2M14 9h2M8 13h2M14 13h2"/><path d="M10.5 20v-3h3v3"/></svg></i><span>Owner &amp; payer</span><b>John&rsquo;s corporation</b><em>Pays with 88&cent; corporate dollars, not 50&cent; personal ones</em></div>
  <div class="stC f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.9 3.1-6.5 7-6.5s7 2.6 7 6.5"/></svg></i><span>Life insured</span><b>John</b><em>The policy is on his life</em></div>
  <div class="stC f gold"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20v-8"/><path d="M12 12c0-3.5 2.5-6 6.5-6 0 3.5-2.5 6-6.5 6Z"/><path d="M12 14c0-3-2-5-5.5-5 0 3 2 5 5.5 5Z"/><path d="M7 20h10"/></svg></i><span>Inside the policy</span><b>Cash value grows</b><em>Tax-sheltered: guaranteed values plus dividends. He can borrow against it.</em></div>
  <div class="stC f"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9.5 12 4l9 5.5"/><path d="M4 20h16M5 17h14"/><path d="M6.5 10.5v6M10 10.5v6M14 10.5v6M17.5 10.5v6"/></svg></i><span>Beneficiary</span><b>John&rsquo;s corporation</b><em>Receives the tax-free death benefit</em></div>
  <div class="stC f gold"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7h14l-1.6 12.5H6.6Z"/><path d="M5 7c0-2 3.1-3.5 7-3.5S19 5 19 7"/><path d="M9.5 12.5h5"/></svg></i><span>The CDA</span><b>Gets credited</b><em>Death benefit minus the policy&rsquo;s cost base goes into the tax-free bucket</em></div>
  <div class="stC f green"><i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="7.5" r="2.5"/><circle cx="16" cy="7.5" r="2.5"/><circle cx="12" cy="13.2" r="1.8"/><path d="M3.5 19c0-3 2-5 4.5-5"/><path d="M20.5 19c0-3-2-5-4.5-5"/><path d="M9.5 20c0-2 1.1-3.3 2.5-3.3s2.5 1.3 2.5 3.3"/></svg></i><span>His family</span><b>Paid tax-free</b><em>As a capital dividend, out of the CDA</em></div>
</div>
<p class="f mid"><b>David</b> reviewed the tax. <b>Sarah</b> updated the corporate records and his will. <b>Mehar</b> designed the policy.</p>
''', 'sStruct', hud=H(40, NW(40), '0,4', '100'))

# 12c ALL IN ONE
slide('''
<div class="kick">The all-in-one strategy</div>
<h2 class="nwH">One policy. Six jobs.</h2>
<svg class="aoSvg" viewBox="0 0 1440 560" width="1440" height="560" aria-hidden="true">
 <g class="f"><rect x="540" y="10" width="360" height="64" rx="14" class="aoTop"/><text x="720" y="50" class="aoTt">John&rsquo;s Dental Corporation</text></g>
 <g class="f"><path class="aoL" d="M360,42 L540,42"/><rect x="180" y="16" width="180" height="52" rx="12" class="aoSide"/><text x="270" y="49" class="aoSt">Revenue in</text><path class="aoL red" d="M900,42 L1080,42"/><rect x="1080" y="16" width="180" height="52" rx="12" class="aoSide r"/><text x="1170" y="49" class="aoSt">Expenses out</text></g>
 <defs><marker id="aoArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10Z" fill="#F2CC5A"/></marker></defs><g class="f"><path class="aoL gold" d="M720,74 L720,196" marker-end="url(#aoArr)"/><rect x="330" y="112" width="364" height="42" rx="21" class="aoPill"/><text x="512" y="139" class="aoPt">Retained earnings: $100,000 a year</text></g>
 <g class="f"><rect x="520" y="200" width="400" height="130" rx="20" class="aoPol"/><text x="720" y="250" class="aoPolT">Permanent Policy</text><text x="720" y="280" class="aoPolS">(Whole Life)</text><text x="720" y="308" class="aoPolS">Cash value + tax-free death benefit</text></g>
 <g class="f aoB"><path class="aoL" d="M720,330 C720,380 170,380 170,430"/><rect x="68" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="170" y="468" class="aoBt">Tax-free growth</text><text x="170" y="494" class="aoBd">Cash value compounds sheltered</text></g><g class="f aoB"><path class="aoL" d="M720,330 C720,380 390,380 390,430"/><rect x="288" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="390" y="468" class="aoBt">Borrow anytime</text><text x="390" y="494" class="aoBd">Collateral for bank loans</text></g><g class="f aoB"><path class="aoL" d="M720,330 C720,380 610,380 610,430"/><rect x="508" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="610" y="468" class="aoBt">Debt protection</text><text x="610" y="494" class="aoBd">Pays off loans at death</text></g><g class="f aoB"><path class="aoL" d="M720,330 C720,380 830,380 830,430"/><rect x="728" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="830" y="468" class="aoBt">Key person</text><text x="830" y="494" class="aoBd">Protects the clinic</text></g><g class="f aoB"><path class="aoL" d="M720,330 C720,380 1050,380 1050,430"/><rect x="948" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="1050" y="468" class="aoBt">Buy-sell funding</text><text x="1050" y="494" class="aoBd">Partner buyout ready</text></g><g class="f aoB"><path class="aoL" d="M720,330 C720,380 1270,380 1270,430"/><rect x="1168" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="1270" y="468" class="aoBt">Tax-free estate</text><text x="1270" y="494" class="aoBd">Paid out through the CDA</text></g>
<g class="f"><path class="aoL gold aoBack" d="M920,262 C1070,262 1060,92 906,62" marker-end="url(#aoArr)"/><text x="1068" y="140" class="aoRt">Back to the business</text><text x="1068" y="166" class="aoRd">Borrow against the cash value</text><text x="1068" y="190" class="aoRd">to reinvest, or for personal use</text></g></svg>
''', 'sAio', hud=H(40, NW(40), '0,4', '100'))

# 13 THE POLICY
i41, i50, i65, i90 = ILL[41], ILL[50], ILL[65], ILL[90]
slide(f'''
<div class="kick">The plan</div>
<h2>A permanent (whole life) policy, owned by John&rsquo;s corporation</h2>
<div class="plan">
  <div class="pc f"><span>John&rsquo;s corporation pays</span><b>$100,000 a year</b><em>for 20 years (age 41 to 60). Then the dividends pay it.</em></div>
  <div class="pc f gold"><span>Protection from day one</span><b>{money(i41["totalDB"])}</b><em>tax-free death benefit, paid to the corporation</em></div>
  <div class="pc f green"><span>Cash value at 65</span><b>{money(i65["totalCV"])}</b><em>growing tax-sheltered, and he can borrow against it</em></div>
</div>
<p class="f mid">Funded from his corporate savings and profit. And he kept his TFSA <b>maxed every year</b>.</p>
<div class="src">Equitable Equimax Wealth Accumulator illustration, male 40, non-smoker, BC, $99,999.99/yr, premium offset from age 61, current dividend scale. Dividends are not guaranteed.</div>
''', 'sPlan', hud=H(41, NW(41), '0,4', '100'))

# 13b THE REAL ILLUSTRATION
import base64
SNAP = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'source', 'ill-snap.jpg'), 'rb').read()).decode()
slide(f'''
<div class="split snapS">
  <div class="snapP f"><img src="{SNAP}" alt="Page from John's real Equitable illustration"><i class="snapTag">The real illustration</i></div>
  <div class="sp2">
    <div class="kick" style="text-align:left">Not a made-up number</div>
    <h2 class="lft">This is the actual plan.</h2>
    <p class="lft big f">Mehar and John agreed this was <b>the best fit for his specific situation</b>: his age, his income, his debts and his goals.</p>
    <ul class="snapL">
      <li class="f"><b>$99,999.99 a year</b> for 20 years, then dividends pay the premium</li>
      <li class="f">Age 50: <b>{money(ILL[50]["totalCV"])}</b> cash value</li>
      <li class="f">Age 60: <b>{money(ILL[60]["totalCV"])}</b> cash value, premiums done</li>
      <li class="f">Age 65: <b class="gold">{money(ILL[65]["totalCV"])}</b> cash value, <b class="gold">{money(ILL[65]["totalDB"])}</b> death benefit</li>
    </ul>
  </div>
</div>
<div class="src">Equitable EquiMax Wealth Accumulator illustration: male 40, non-smoker, BC, paid-up additions, current dividend scale (not guaranteed). Every client&rsquo;s illustration is different.</div>
''', 'sSnap', hud=H(41, NW(41), '0,4', '100'))

# 14 GROWTH CHART (real data)
def _hover():
    pts = ''.join(f'<i data-a="{a}" data-x="{90 + (a - 41) * (1010 / 49):.1f}" data-ycv="{390 - ILL[a]["totalCV"] / 15e6 * 350:.1f}" data-ydb="{390 - ILL[a]["totalDB"] / 15e6 * 350:.1f}" data-cv="{money(ILL[a]["totalCV"])}" data-db="{money(ILL[a]["totalDB"])}" data-pr="{money(100000 * min(a - 40, 20))}"></i>' for a in range(41, 91))
    return ('<g class="hvG"><line class="hvL" x1="0" x2="0" y1="40" y2="390"/><circle class="hvC db" r="7"/><circle class="hvC cv" r="7"/>'
            '<g class="hvT"><rect width="230" height="104" rx="10"/><text class="t0" x="14" y="26"></text><text class="t1" x="14" y="50"></text><text class="t2" x="14" y="72"></text><text class="t3" x="14" y="94"></text></g></g>'
            f'<rect class="hvHit" x="90" y="30" width="1010" height="370"/><foreignObject width="0" height="0"><div class="hvD">{pts}</div></foreignObject>')
HOVER = _hover()
ages = list(range(41, 91))
def px(a): return 90 + (a - 41) * (1010 / 49)
def py(v): return 390 - v / 15e6 * 350
cv = ' '.join(f'{px(a):.1f},{py(ILL[a]["totalCV"]):.1f}' for a in ages)
db = ' '.join(f'{px(a):.1f},{py(ILL[a]["totalDB"]):.1f}' for a in ages)
grid = ''.join(f'<line x1="90" x2="1100" y1="{py(v):.0f}" y2="{py(v):.0f}" class="gl"/><text x="80" y="{py(v)+5:.0f}" text-anchor="end" class="ax">${v//1_000_000}M</text>' for v in range(0, 15_000_001, 3_000_000))
ticks = ''.join(f'<text x="{px(a):.0f}" y="418" text-anchor="middle" class="ax">{a}</text>' for a in (41, 50, 60, 65, 70, 80, 90))
marks = ''
for a, txt in ((50, 'Debt-free'), (65, 'Retires'), (90, 'Legacy')):
    marks += f'<g class="f"><circle cx="{px(a):.0f}" cy="{py(ILL[a]["totalDB"]):.0f}" r="8" fill="#E5B93C" stroke="#7A0F1A" stroke-width="3"/><text x="{px(a):.0f}" y="{py(ILL[a]["totalDB"])-18:.0f}" text-anchor="middle" class="mk">{txt} &middot; {money(ILL[a]["totalDB"])}</text></g>'
slide(f'''
<div class="kick">Watching it grow</div>
<h2>$2 million in premiums. Look what it becomes.</h2>
<svg class="chart hov" viewBox="0 0 1260 430" width="1260" height="430" data-x0="90" data-x1="1100">{grid}{ticks}
  <polyline class="ln db" points="{db}"/><polyline class="ln cv" points="{cv}"/>
  <text x="1108" y="{py(i90["totalDB"])+5:.0f}" class="lg gold">Death benefit</text><text x="1108" y="{py(i90["totalCV"])+5:.0f}" class="lg green">Cash value</text>{marks}{HOVER}</svg>
<p class="hint">Hover over the chart to see any year</p>
<div class="src">Same illustration. Total cash value and total death benefit, current dividend scale (not guaranteed). Age 90: cash value {money(i90["totalCV"])}, death benefit {money(i90["totalDB"])}.</div>
''', 'sChart', hud=H(41, NW(41), '0,4', '100'))

# 16 ROGERS
slide(f'''
<div class="kick">A real case &middot; proven in Tax Court</div>
<h2>The Rogers family did exactly this.</h2>
<div class="rog">
  <div class="f">{COURT}</div>
  <div class="rogBig f">{counter(102, '$', 'M')}<span>through the CDA, tax-free</span></div>
  <div class="rogTxt">
    <p class="f">Corporate-owned life insurance on Ted Rogers, held in the family&rsquo;s private companies.</p>
    <p class="f">On his passing, about $102 million was credited to the CDA and paid out as tax-free capital dividends.</p>
    <p class="f">The CRA challenged it. <b>The Tax Court ruled for the family.</b></p>
  </div>
</div>
<p class="f mid">John doesn&rsquo;t need $102 million. <b>He needs the same playbook.</b></p>
<div class="src">Rogers Enterprises (2015) Inc. v. The Queen, Tax Court of Canada.</div>
''', 'sRogers', hud=H(41, NW(41), '0,4', '101'))

# 17 RE vs S&P
slide(f'''
<div class="kick">Diversify, don&rsquo;t concentrate</div>
<h2>John was about to buy a second rental condo.</h2>
<p class="big">Then Mehar showed him this: <b>$180,000 invested in 1980.</b></p>
<div class="reRow">
  <div class="reC f">{scene(house(150,230,.8), 250).replace('viewBox="0 0 1300 250" width="1300"','viewBox="0 0 300 250" width="300"')}<span>Vancouver detached house</span>{counter(1880000)}<em>10x</em></div>
  <div class="vs f">vs</div>
  <div class="reC f win"><svg viewBox="0 0 300 250" width="300" height="250"><polyline points="20,230 80,215 130,190 180,150 230,90 280,20" fill="none" stroke="#2F6E4C" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg><span>S&amp;P 500, dividends reinvested</span>{counter(37300000)}<em>207x</em></div>
</div>
<p class="f mid">He kept his home. He put new money into <b>segregated funds</b> instead.</p>
<div class="src">House: Metro Vancouver detached benchmark, Dec 2025 (Greater Vancouver REALTORS&reg;). S&amp;P 500 total return (DQYDJ), 2024 rolled forward by 2025 (+17.4%). Past performance does not guarantee future results.</div>
''', 'sRe', hud=H(42, NW(42), '0,4', '101'))

# 18 SEG FUNDS
feat = [('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>', 'Market growth'), ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 19.5 6v5.5c0 4.6-3.2 8-7.5 9.5-4.3-1.5-7.5-4.9-7.5-9.5V6Z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>', '75&ndash;100% guarantee'), ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M19.5 8A8 8 0 0 0 5 9"/><path d="M19.5 3.5V8H15"/><path d="M4.5 16A8 8 0 0 0 19 15"/><path d="M4.5 20.5V16H9"/></svg>', 'Resets lock in gains'), ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/><circle cx="12" cy="15.2" r="1.2"/></svg>', 'Creditor protection'), ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3.5h7.5L19 8v12.5H7Z"/><path d="M14.5 3.5V8H19"/><path d="M10 12.5h6M10 16h6"/></svg>', 'Skips probate'), ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="9" r="5.5"/><path d="M9.2 13.8 7.5 21l4.5-2.5 4.5 2.5-1.7-7.2"/><path d="M10 9l1.5 1.5 3-3"/></svg>', 'Assuris protection')]
fh = ''.join(f'<div class="ft f"><i>{a}</i>{b}</div>' for a, b in feat)
slide(f'''
<div class="kick">Why segregated funds</div>
<h2>Growth <span class="gold">and</span> guarantees, in one place</h2>
<div class="feats">{fh}</div>
<div class="flexP f"><b>Mehar&rsquo;s flexible investment plan</b><span>John had only ever maxed his TFSA and RRSP. Now: <strong>both moved into seg funds</strong>, kept maxed every year, <strong>plus $15,000 a year</strong> in non-registered investments. Target: an average of <strong class="g12">12% a year</strong>.</span></div>
<p class="f mid"><b>Emma</b> liked the guarantee. <b>Sarah</b> liked that it skips probate. <b>John</b> liked sleeping at night.</p>
''', 'sSeg', hud=H(42, NW(42), '0,4', '101'))

# 19 CHAPTER 4: LOCATION #2 (full title page)
chap_full('Chapter Four', 'Christmas 2032 &middot; John is 46', 'Location #2', ch4(), 'sLoc2', hud=H(46, NW(46), '0,4,5', '101'),
  chips=chips(f'Funded by borrowing against his policy&rsquo;s cash value ({money(ILL[46]["totalCV"])})', 'The policy kept growing as if he&rsquo;d never touched it', 'Clinic #2 adds about $750K a year: revenue doubles to $1.5M'))

# 20 IFA EXPLAINED
def _ifa_chart():
    W, Hh, L, T, B = 640, 360, 70, 20, 300
    ages = list(range(46, 91)); mx = 13e6
    X = lambda a: L + (a - 46) / 44 * (W - L - 30)
    Y = lambda v: B - v / mx * (B - T)
    cv = ' '.join(f'{X(a):.0f},{Y(ILL[a]["totalCV"]):.0f}' for a in ages)
    db = ' '.join(f'{X(a):.0f},{Y(min(ILL[a]["totalDB"], mx)):.0f}' for a in ages if ILL[a]["totalDB"] <= mx)
    g = [f'<svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" class="ifaSvg">']
    for v in range(0, 14, 4):
        g.append(f'<line x1="{L}" x2="{W-30}" y1="{Y(v*1e6):.0f}" y2="{Y(v*1e6):.0f}" class="gl"/><text x="{L-10}" y="{Y(v*1e6)+5:.0f}" class="gt" text-anchor="end">${v}M</text>')
    for a in (46, 55, 65, 75, 90):
        g.append(f'<text x="{X(a):.0f}" y="{B+26}" class="gt" text-anchor="middle">{a}</text>')
    g.append(f'<path d="M{X(46):.0f},{Y(0):.0f} L{cv.replace(" "," L")} L{X(90):.0f},{Y(0):.0f}Z" class="ifaArea"/>')
    g.append(f'<polyline points="{cv}" class="ifaCv"/>')
    g.append(f'<line x1="{X(46):.0f}" x2="{X(90):.0f}" y1="{Y(5e5):.0f}" y2="{Y(5e5):.0f}" class="ifaLoan"/>')
    g.append(f'<text x="{X(60):.0f}" y="{Y(5e5)-10:.0f}" class="ifaLt">Bank loan: $500K, interest only</text>')
    g.append(f'<text x="{X(70):.0f}" y="{Y(ILL[70]["totalCV"])-16:.0f}" class="ifaCt" text-anchor="end">Policy cash value keeps growing</text>')
    g.append(f'<circle cx="{X(90):.0f}" cy="{Y(ILL[90]["totalCV"]):.0f}" r="7" class="ifaDot"/><text x="{X(90)-14:.0f}" y="{Y(ILL[90]["totalCV"])+6:.0f}" class="ifaCt" text-anchor="end">{money(ILL[90]["totalCV"])} at 90</text>')
    g.append(f'<text x="{L}" y="{Hh-6}" class="gt">John&rsquo;s age</text></svg>')
    return ''.join(g)
IFA_CHART = _ifa_chart()
slide(f'''
<div class="kick">How he borrowed</div>
<h2>The Immediate Financing Arrangement (IFA)</h2>
<div class="ifD">
  <div class="ifB paper f" style="left:0;top:178px;width:300px"><b>John&rsquo;s corporation</b><span>pays the <strong>$100K</strong> premium</span></div>
  <svg class="ifX f" style="left:300px;top:216px" width="130" height="60"><text x="65" y="18" class="ifLb">premium</text><path d="M8,38 L116,38" class="ifAr" marker-end="url(#ifM)"/></svg>
  <div class="ifB paper f big" style="left:430px;top:150px;width:440px"><b>Whole life policy</b><span class="g">Cash value keeps compounding, uninterrupted</span><span>and stands as collateral</span></div>
  <svg class="ifX f" style="left:870px;top:216px" width="130" height="60"><text x="65" y="18" class="ifLb">collateral</text><path d="M8,38 L116,38" class="ifAr" marker-end="url(#ifM)"/></svg>
  <div class="ifB paper f" style="left:1000px;top:178px;width:300px"><b>The bank</b><span>lends <strong>$500K</strong> against the policy</span></div>
  <svg class="ifX f" style="left:0;top:290px" width="1300" height="190"><path d="M1150,24 C1150,150 900,168 650,168 C400,168 150,150 150,30" class="ifAr g" marker-end="url(#ifMg)"/>
    <text x="650" y="156" class="ifLb g" text-anchor="middle">The loan flows back: $500K reinvested in clinic #2</text></svg>
  <svg class="ifX f" style="left:620px;top:96px" width="60" height="56"><path d="M30,52 L30,10" class="ifAr" marker-end="url(#ifM)"/></svg>
  <div class="ifB paper f" style="left:390px;top:0;width:520px;padding:12px 20px"><b>At death: Death benefit &minus; ACB = CDA</b><span>The loan is repaid; the rest exits <strong>tax-free</strong> to his family</span></div>
</div>
<svg width="0" height="0" style="position:absolute"><defs><marker id="ifM" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10Z" fill="#F2CC5A"/></marker><marker id="ifMg" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10Z" fill="#7BE3AE"/></marker></defs></svg>
<p class="f mid ifN2">Interest may be tax-deductible when the loan is used to earn business income. Walt Disney and Ray Kroc are widely reported to have used their policies this way. <b class="gold">One dollar, two jobs.</b></p>
<div class="src">IFA structures must be set up with your accountant and lender. Interest deductibility depends on how the loan is used. Not tax advice.</div>
''', 'sIfa', hud=H(46, NW(46), '0,4,5', '101'))

# 20a RAJ'S POLICY + BUY-SELL
RAJBS = scene(ground(520,420) + clinic(130,410,.62,2) + person('john',300,410,.9,'coat') + person('raj',420,410,.9,'coat')
  + label(300,448,'John') + label(420,448,'Dr. Raj'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')
slide(f'''
<div class="kick">Clinic #2 &middot; a new partner</div>
<h2>Raj, 44, buys in, and gets the same plan.</h2>
<div class="split rajB">
  <div class="sp">{RAJBS}</div>
  <div class="bsF">
    <div class="bfS f"><i>1</i><span><b>A policy on each partner.</b> Raj is 44. The clinic corporation pays <b>$100K a year for 20 years</b> into a whole life policy on him: <b class="gold">{money(RAJ[45]["totalDB"])} of coverage from day one.</b> It does the same for John.</span></div>
    <div class="bfS f"><i>2</i><span><b>Sarah writes the buy-sell agreement.</b> If a partner dies, the corporation must buy his shares from his family, at a fair price.</span></div>
    <div class="bfS f"><i>3</i><span><b>The policy pays for it.</b> The payout goes to the corporation, credits the CDA, and funds the buyout. <b class="gold">His family gets cash. The survivor keeps the clinic.</b></span></div>
    <div class="bfS f gold"><i>4</i><span><b>Raj gets the upside too.</b> His policy builds cash value he can borrow against, just like John&rsquo;s.</span></div>
  </div>
</div>
<div class="src">Illustrative. Buy-sell structures vary; ownership and beneficiary set-up should be designed with your lawyer and accountant.</div>
''', 'sRajBS', hud=H(46, NW(46), '0,3,4,5', '101'))

# 20b CHAPTER 5
chap_full('Chapter Five', '2034 &middot; John is 48', 'The Storm', ch5(), 'sChap sStorm', hud=H(48, NW(48), '0,3,4,5', '111'))

# 21 TWIST 1 crash
slide(f'''
<div class="kick red">Plot twist #1 &middot; 2034 &middot; John is 48</div>
<h2>The market crashes 25%.</h2>
{scene(ground(1300,380)+'<g transform="translate(0,60)">'+cloud(560,70,1.0)+cloud(800,90,.8)+'<line class="rain" style="animation-delay:-0.62s" x1="380" y1="167" x2="370" y2="201" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.80s" x1="402" y1="167" x2="392" y2="210" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.92s" x1="424" y1="121" x2="414" y2="204" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.78s" x1="446" y1="135" x2="436" y2="210" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.05s" x1="468" y1="130" x2="458" y2="193" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.37s" x1="490" y1="135" x2="480" y2="202" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.54s" x1="512" y1="156" x2="502" y2="197" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.01s" x1="534" y1="133" x2="524" y2="203" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.28s" x1="556" y1="169" x2="546" y2="202" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.16s" x1="578" y1="124" x2="568" y2="194" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.62s" x1="600" y1="148" x2="590" y2="194" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.13s" x1="622" y1="120" x2="612" y2="196" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.77s" x1="644" y1="130" x2="634" y2="195" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.29s" x1="666" y1="132" x2="656" y2="207" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.88s" x1="688" y1="160" x2="678" y2="196" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.18s" x1="710" y1="164" x2="700" y2="196" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.97s" x1="732" y1="144" x2="722" y2="199" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.02s" x1="754" y1="146" x2="744" y2="195" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.94s" x1="776" y1="136" x2="766" y2="192" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.33s" x1="798" y1="158" x2="788" y2="208" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.00s" x1="820" y1="163" x2="810" y2="212" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.34s" x1="842" y1="139" x2="832" y2="201" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.82s" x1="864" y1="150" x2="854" y2="212" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.32s" x1="886" y1="150" x2="876" y2="205" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.70s" x1="908" y1="123" x2="898" y2="198" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.98s" x1="930" y1="121" x2="920" y2="213" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.36s" x1="952" y1="145" x2="942" y2="190" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/><line class="rain" style="animation-delay:-0.55s" x1="974" y1="146" x2="964" y2="201" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".8"/></g><g transform="translate(980,90)"><rect x="0" y="0" width="240" height="160" rx="12" fill="rgba(20,4,8,.6)" stroke="rgba(255,111,107,.6)" stroke-width="2"/><polyline points="20,40 60,55 90,45 120,70 150,110 180,95 220,135" fill="none" stroke="#FF6F6B" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M210,122 L224,138 L204,140Z" fill="#FF6F6B"/><text x="120" y="28" text-anchor="middle" style="font:900 22px Georgia;fill:#FF8A86">&#8722;25%</text></g>'+umbrella(650,215,1.0)+person('john',610,370,.8,arm='hold')+person('emma',710,370,.76), 420)}
<div class="twist">
  <p class="f">John&rsquo;s seg funds had a <b>guaranteed floor</b>. When markets recovered, a <b>reset</b> locked in the new high.</p>
  <p class="f"><b>Mehar called John that same morning</b> and walked him through it, so nothing was sold in a panic.</p>
  <p class="f">His policy&rsquo;s cash value <b class="green">didn&rsquo;t drop at all</b> ({money(ILL[48]["totalCV"])} and climbing).</p>
</div>
''', 'sCrash', hud=H(48, NW(48), '0,3,4,5', '111'))

# 22 DEBT-FREE AT 50
slide(f'''
<div class="kick">Christmas 2036 &middot; John is 50</div>
<h2>Debt-free. <span class="green">Right on schedule: 10 years.</span></h2>
<div class="debtS f">{DEBT_SCENE}</div>
<div class="debt">
  <div class="dC f"><span>Practice loan</span><s>$500,000</s><b>$0</b></div>
  <div class="dC f"><span>Home mortgage</span><s>$1,000,000</s><b>$0</b></div>
  <div class="dC f gold"><span>Policy cash value</span><b>{money(i50["totalCV"])}</b></div>
</div>
<p class="f mid">Two clinics paid off his debts faster. <b>&#10003; Pay off every debt in 10 years.</b></p>
''', 'sDebt', hud=H(50, NW(50) - 0, '0,3,4,5', '111', cda=ILL[50]['totalDB']))

# 22c POLICY #2
J2SNAP = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'source', 'john2-snap.jpg'), 'rb').read()).decode()
slide(f'''
<div class="kick">Christmas 2036 &middot; John is 50 &middot; Policy #2</div>
<h2>No more debt payments. <span class="gold">Mehar puts that cash flow to work.</span></h2>
<div class="split p2S">
  <div class="snapP f p2Snap"><img src="{J2SNAP}" alt="John's second Equitable illustration, ages 51 to 66"><i class="snapTag">Policy #2: the real illustration</i></div>
  <div class="rpF">
    <div class="rpR paper f"><b>$150K a year, for 15 years</b><span>Paid by his corporation, with money that used to go to the bank.</span></div>
    <div class="rpR paper f gold"><b>{money(5758157)} of coverage from day one</b><span>A second corporate whole life policy on John.</span></div>
    <div class="rpR paper f green"><b>More fuel to grow the business</b><span>By 55, its cash value ({money(P2[55]["totalCV"])}) helps fund <strong>clinic #3</strong>, borrowed against just like the first policy.</span></div>
    <div class="rpR paper f green"><b>More tax-efficient money to access</b><span><strong>{money(P2[65]["totalCV"])}</strong> of cash value by 65, ready to borrow against.</span></div>
    <div class="rpR paper f gold"><b>A bigger tax-free legacy</b><span>{money(P2[90]["totalDB"])} more for the CDA by age 90.</span></div>
  </div>
</div>
<div class="src">Policy #2: Equitable EquiMax illustration, male 50, non-smoker, BC, $149,999.99/yr for 15 years, current dividend scale (not guaranteed).</div>
''', 'sPol2', hud=H(50, NW(50), '0,3,4,5', '111'))


RAJ_SCENE = scene(ground(560,420)
  + '<g class="rajGhost">' + person('raj',170,400,.82,'coat') + '</g>'
  + '<ellipse class="halo" cx="170" cy="182" rx="36" ry="10"/>'
  + '<g transform="translate(380,410)"><path d="M-95,0 L-95,-170 C-95,-235 95,-235 95,-170 L95,0Z" fill="#8E949C"/><path d="M-95,0 L-95,-170 C-95,-235 95,-235 95,-170 L95,0Z" fill="url(#gShade)"/>'
  + '<path d="M-80,0 L-80,-165 C-80,-220 80,-220 80,-165 L80,0" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="3"/>'
  + '<text y="-150" text-anchor="middle" style="font:900 52px Georgia;fill:#3A3F46">RIP</text><text y="-108" text-anchor="middle" style="font:700 22px Georgia;fill:#2E3238">Dr. Raj</text>'
  + '<text y="-82" text-anchor="middle" style="font:700 15px Georgia;fill:#2E3238">1988 &#8211; 2041</text><text y="-60" text-anchor="middle" style="font:italic 14px Georgia;fill:#2E3238">Partner. Father. Friend.</text>'
  + '<circle cx="-70" cy="-6" r="12" fill="#C62D3A"/><circle cx="-52" cy="-10" r="10" fill="#E5B93C"/><circle cx="-60" cy="-22" r="9" fill="#F4EBDD"/><circle cx="66" cy="-8" r="12" fill="#C62D3A"/><circle cx="50" cy="-16" r="9" fill="#F4EBDD"/></g>', 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 560 470" width="560"')

# 22b LIFE CAN HIT
slide('''
<div class="lifeHit">
  <svg viewBox="-60 -150 120 230" width="120" height="230" class="candle" aria-hidden="true"><ellipse cx="0" cy="-92" rx="34" ry="44" fill="rgba(255,190,90,.25)" class="cGlow"/><rect x="-22" y="-60" width="44" height="130" rx="6" fill="#F4EBDD"/><rect x="-22" y="-60" width="16" height="130" fill="rgba(0,0,0,.12)"/><path d="M0,-64 L0,-74" stroke="#333" stroke-width="3"/><path class="cFl" d="M0,-72 C-14,-90 -6,-110 0,-128 C6,-110 14,-90 0,-72Z" fill="#FFC85A"/></svg>
  <p class="lhA f">But life can change at any moment.</p>
  <p class="lhB f">Unfortunately, it often does when we least expect it.</p>
</div>
''', 'sLife', hud=H(55, NW(55), '0,3,4,5', '111'))

# 23 TWIST 2 partner dies
slide(f'''
<div class="kick red">Plot twist #2 &middot; 2041 &middot; John is 55</div>
<h2>Dr. Raj, John&rsquo;s partner, passed away suddenly. He was 53.</h2>
<div class="split">
  <div class="sp">{RAJ_SCENE}</div>
  <div class="twist2 paper rajP">
    <p class="f">A wife and two kids lost a husband and a father. John lost his partner and his friend.</p>
    <p class="f">Without a plan, this is where partnerships fall apart: the family needs cash, and the surviving partner can&rsquo;t afford to buy them out.</p>
    <p class="f">But nine years earlier, when Raj bought in, <b>Mehar, Sarah and David had planned for exactly this.</b></p>
    <p class="f mid2">No lawsuits. No fire sale. <b class="green">Here&rsquo;s what his policy did.</b></p>
  </div>
</div>
''', 'sRaj', hud=H(55, NW(55), '0,2,3,4,5', '111'))

# 23b WHAT RAJ'S POLICY DID
RSNAP = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'source', 'raj-snap.jpg'), 'rb').read()).decode()
r53 = RAJ[53]
slide(f'''
<div class="kick">What happened when Raj died</div>
<h2>$900K in. <span class="gold">{money(r53["totalDB"])} out</span>, exactly when it was needed.</h2>
<div class="split rpS">
  <div class="snapP f rpSnap"><img src="{RSNAP}" alt="Raj's real Equitable illustration, year 9 highlighted"><i class="snapTag">Raj&rsquo;s real illustration</i></div>
  <div class="rpF">
    <div class="rpR paper f"><b>9 years of premiums</b><span>The clinic corporation paid <strong>$900,000</strong> ($100K a year).</span></div>
    <div class="rpR paper f gold"><b>Death benefit: {money(r53["totalDB"])}</b><span>Paid to the corporation, <strong>tax-free</strong>, within weeks.</span></div>
    <div class="rpR paper f gold"><b>CDA credited</b><span>Almost all of it goes into the tax-free bucket (the payout minus the policy&rsquo;s cost base).</span></div>
    <div class="rpR paper f green"><b>Raj&rsquo;s family: paid in full</b><span>The corporation buys his shares at the agreed price, paid out through the CDA as a <strong>tax-free capital dividend</strong>.</span></div>
    <div class="rpR paper f green"><b>The clinic: protected</b><span>The rest carries the clinic while a new dentist is hired. John now owns 100%.</span></div>
  </div>
</div>
<div class="src">Raj: Equitable EquiMax illustration, male 44, $99,999.99/yr for 20 years, current dividend scale (not guaranteed); values at the end of year 9 (age 53). Buy-sell and capital dividend treatment must be set up with your lawyer and accountant.</div>
''', 'sRajPay', hud=H(55, NW(55), '0,2,3,4,5', '111'))

# 24 CHAPTER 6: RETIREMENT (full title page)
chap_full('Chapter Six', 'Christmas 2051 &middot; John is 65', 'Retirement, Right on Time', ch6(), 'sRetire', hud=H(65, NW(65), '0,2,3,4,5', '111'),
  chips=chips('Three clinics, about $1M a year each', '<b>Sarah:</b> holding company, estate freeze, updated will', '<b>David:</b> tax-free dividends and retirement income', '<b>Mehar:</b> policies and seg funds into tax-efficient income'))

# 5b JOHN'S SAVINGS PLAN
def _save_series():
    t, r, n = 109000, 150000, 0; rows = {40: (t, r, n, 0)}; wsum = 0
    for y in range(41, 91):
        if y <= 65: t = t*1.12 + TFSA_MAX; r = r*1.12 + RRSP_MAX; n = n*1.12 + NONREG; w = 0
        else:
            w = (t + r + n)*1.12*.1; wsum += w; t *= 1.12*.9; r *= 1.12*.9; n *= 1.12*.9
        rows[y] = (t, r, n, w)
    return rows, wsum
SAV, SAV_W = _save_series()
def _save_chart():
    W, Hh, L, T, B = 760, 390, 70, 56, 330; mx = 18e6
    X = lambda a: L + (a - 40)/50*(W - L - 20); Y = lambda v: B - v/mx*(B - T)
    g = [f'<svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" class="svSvg">']
    g.append(f'<rect x="{X(40):.0f}" y="{T}" width="{X(65)-X(40):.0f}" height="{B-T}" class="ph1"/><rect x="{X(65):.0f}" y="{T}" width="{X(90)-X(65):.0f}" height="{B-T}" class="ph2"/>')
    for v in range(0, 19, 6):
        g.append(f'<line x1="{L}" x2="{W-20}" y1="{Y(v*1e6):.0f}" y2="{Y(v*1e6):.0f}" class="gl"/><text x="{L-10}" y="{Y(v*1e6)+5:.0f}" class="gt" text-anchor="end">${v}M</text>')
    for a in (40, 50, 65, 80, 90):
        g.append(f'<text x="{X(a):.0f}" y="{B+24}" class="gt" text-anchor="middle">{a}</text>')
    layers = [(lambda r: r[0], 'svT'), (lambda r: r[0]+r[1], 'svR'), (lambda r: r[0]+r[1]+r[2], 'svN')]
    prev = None
    for fn, cls in layers:
        top = [(X(a), Y(fn(SAV[a]))) for a in range(40, 91)]
        base = [(X(a), Y(prev(SAV[a]) if prev else 0)) for a in range(90, 39, -1)]
        g.append('<path class="' + cls + '" d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in top + base) + 'Z"/>')
        prev = fn
    tot = lambda a: sum(SAV[a][:3])
    g.append(f'<circle cx="{X(65):.0f}" cy="{Y(tot(65)):.0f}" r="7" class="svDot"/><text x="{X(65)-12:.0f}" y="{Y(tot(65))-14:.0f}" class="svV" text-anchor="end">{money(tot(65))} at 65</text>')
    g.append(f'<circle cx="{X(90):.0f}" cy="{Y(tot(90)):.0f}" r="7" class="svDot"/><text x="{X(90)-6:.0f}" y="{Y(tot(90))-14:.0f}" class="svV" text-anchor="end">{money(tot(90))} at 90</text>')
    g.append(f'<text x="{(X(40)+X(65))/2:.0f}" y="22" class="phT" text-anchor="middle">BUILDING: adds $55,810 a year</text>')
    g.append(f'<text x="{(X(65)+X(90))/2:.0f}" y="22" class="phT b" text-anchor="middle">LIVING OFF IT: takes money out</text>')
    g.append(f'<text x="{L}" y="{Hh-6}" class="gt">John&rsquo;s age</text></svg>')
    return ''.join(g)
SAVE_CHART = _save_chart()
PUT_IN = (TFSA_MAX + RRSP_MAX + NONREG) * 25
slide(f'''
<div class="kick">From saving to spending</div>
<h2>At 65, John stops adding and <span class="gold">starts taking money out.</span></h2>
<div class="svW">
  <div class="svCh f">{SAVE_CHART}<div class="svKey"><span class="k t">TFSA (seg funds)</span><span class="k r">RRSP (seg funds)</span><span class="k n">Non-registered</span><span class="ret12">Average return: 12% a year</span></div></div>
  <div class="svC">
    <div class="svS paper f"><b>Ages 41 to 65: he puts money in</b><span>TFSA maxed <strong>$7,000</strong> &middot; RRSP maxed <strong>$33,810</strong> &middot; plus Mehar&rsquo;s flexible plan: <strong>$15,000</strong> non-registered. All averaging <strong>12% a year</strong>.</span></div>
    <div class="svS paper f gold"><b>At 65: {money(sum(SAV[65][:3]))}</b><span>He put in about {money(PUT_IN)}. Compounding at 12% did the rest.</span></div>
    <div class="svS paper f"><b>From 66: he takes money out</b><span>About 10% a year to live on: <strong>{money(SAV[66][3])}</strong> in the first year. It still earns 12%, so <strong>the balance keeps growing</strong> while he spends.</span></div>
    <div class="svS paper f green"><b>By 90: {money(SAV_W)} taken out</b><span>And <strong>{money(sum(SAV[90][:3]))}</strong> still invested.</span></div>
  </div>
</div>
<div class="cvInc paper f"><b>Plus: income from his policies&rsquo; cash value</b><span>In retirement John also draws from the cash value of his <strong>personal permanent policy</strong>. And over the years, he used some of the <strong>corporate policy&rsquo;s cash value</strong> for personal needs too, borrowing against it with David&rsquo;s help, while the policies kept growing.</span></div>
<div class="src">Illustrative: 2026 TFSA and RRSP limits held flat; an assumed 12% average annual return (not guaranteed), before tax. Withdrawals from 66 are about 10% of the balance each year.</div>
''', 'sSave', hud=H(65, NW(65), '0,2,3,4,5', '111'))

# 25 SUCCESSION
slide(f'''
<div class="kick">Passing the torch</div>
<h2>Lily takes over the clinics. Max is treated just as fairly.</h2>
{scene(ground(1300,380)+person('john',420,370,1.12,arm='hold')+person('lily',690,370,1.0)+person('max',960,370,1.0)
   +'<g class="torch"><ellipse cx="560" cy="150" rx="58" ry="58" fill="url(#gTorch)"/><path d="M478,252 L555,172" stroke="#8A5A2A" stroke-width="11" stroke-linecap="round"/><path d="M546,180 L566,160 L578,172 L558,192Z" fill="#E5B93C"/>'
   +'<path class="tFl" d="M572,166 C552,146 556,120 574,98 C576,118 592,120 590,140 C600,132 602,150 594,160 C588,170 578,172 572,166Z" fill="#FFB547"/><path class="tFl" d="M574,160 C566,148 570,134 578,124 C580,136 588,140 584,152 C582,158 578,162 574,160Z" fill="#FFF0B0"/></g>'
   +'<defs><radialGradient id="gTorch"><stop offset="0" stop-color="rgba(255,200,90,.7)"/><stop offset="1" stop-color="rgba(255,200,90,0)"/></radialGradient></defs>'
   +'<path d="M600,250 C620,228 640,236 646,252" stroke="#C62D3A" stroke-width="15" fill="none" stroke-linecap="round"/><circle cx="604" cy="250" r="9.5" fill="#F1C9A0"/>'
   +label(420,412,'John, 65',size=22)+label(690,412,'Lily, 31 &middot; now Dr. Lily',size=20)+label(960,412,'Max, 29',size=20), 420)}
<div class="succ">
  <p class="f"><b>Lily</b> inherits the business she runs.</p>
  <p class="f"><b>Max</b> receives equal value from the insurance, so nobody has to sell a clinic to be fair.</p>
</div>
''', 'sSucc', hud=H(65, NW(65), '0,1,2,3,4,5,6', '111'))

# 25b WHAT THE PLAN REALLY GAVE HIM: TIME
def _pol(inner, cap, rot):
    return (f'<div class="pol f" style="--r:{rot}deg"><svg viewBox="0 0 300 220" width="220" height="161">{inner}</svg><span>{cap}</span></div>')
def _ppl(spec):
    return ''.join(person(k, x, y, sc, **kw) for k, x, y, sc, kw in spec)
BEACH = ('<rect width="300" height="220" fill="#8FD0F0"/><circle cx="240" cy="50" r="26" fill="#FFE07A"/><rect y="120" width="300" height="40" fill="#3A8FC0"/>'
         '<path d="M0,128 Q40,122 80,128 T160,128 T240,128 T320,128" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/><rect y="155" width="300" height="65" fill="#F2DDA4"/>'
         '<path d="M262,205 C258,170 262,140 270,110" stroke="#7A5A2A" stroke-width="7" fill="none"/><path d="M270,110 C250,100 230,108 222,118 M270,110 C285,95 300,100 306,108 M270,110 C262,92 246,88 236,92 M270,110 C282,90 296,88 300,90" stroke="#2F6E4C" stroke-width="7" fill="none" stroke-linecap="round"/>'
         + _ppl([('john',80,212,.4,dict(arm='up')),('emma',122,212,.38,{}),('lily',158,212,.28,{}),('max',186,212,.24,{})]) + '<circle cx="214" cy="200" r="10" fill="#E8433A"/><path d="M204,200 H224" stroke="#fff" stroke-width="3"/>')
HOCKEY = ('<rect width="300" height="220" fill="#2A3A52"/><rect y="120" width="300" height="100" fill="#EEF4FA"/><rect y="120" width="300" height="10" fill="#C0202E"/><rect x="0" y="96" width="300" height="26" fill="#D8DEE6"/>'
          + _ppl([('john',70,120,.3,dict(arm='up')),('emma',100,120,.28,dict(arm='up'))]) + _ppl([('max',190,205,.42,{})])
          + '<path d="M206,170 L232,206 L246,206" stroke="#5A3A22" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="256" cy="207" rx="7" ry="3" fill="#111"/>')
RECITAL = ('<rect width="300" height="220" fill="#1A0A10"/><path d="M0,0 H60 C50,60 60,120 40,160 H0Z M300,0 H240 C250,60 240,120 260,160 H300Z" fill="#8E1B26"/>'
           '<path d="M150,0 L100,150 H200Z" fill="rgba(255,240,180,.25)"/><rect y="150" width="300" height="12" fill="#5A3A22"/>'
           + _ppl([('lily',150,152,.42,dict(arm='up'))]) + '<rect y="162" width="300" height="58" fill="#120608"/>'
           + ''.join(f'<circle cx="{x}" cy="190" r="13" fill="#3A2A2A"/>' for x in (30,70,190,230,270)) + '<circle cx="110" cy="188" r="14" fill="#5A3A22"/><circle cx="148" cy="190" r="14" fill="#A0522D"/>')
GRAD = ('<rect width="300" height="220" fill="#F4E9D4"/><rect x="20" y="20" width="260" height="34" rx="4" fill="#8E1B26"/><text x="150" y="44" text-anchor="middle" style="font:900 17px Georgia;fill:#FFE7A6">CONGRATULATIONS!</text>'
        + _ppl([('lily',100,212,.44,dict(arm='up')),('max',200,212,.44,dict(arm='up'))])
        + ''.join(f'<g transform="translate({x},{y})"><path d="M-16,0 L0,-7 L16,0 L0,7Z" fill="#1E1E24"/><rect x="-7" y="1" width="14" height="7" fill="#1E1E24"/></g>' for x, y in ((100,104),(200,104)))
        + '<g transform="translate(150,80) rotate(-20)"><path d="M-14,0 L0,-6 L14,0 L0,6Z" fill="#1E1E24"/></g><g transform="translate(250,70) rotate(25)"><path d="M-14,0 L0,-6 L14,0 L0,6Z" fill="#1E1E24"/></g>')
XMAS = ('<rect width="300" height="220" fill="#5A1A22"/><rect y="180" width="300" height="40" fill="#6B4226"/>' + tree(240,200,.42)
        + _ppl([('john',60,205,.36,{}),('emma',95,205,.34,{}),('lily',130,205,.3,{}),('max',160,205,.27,{})]) + gift(196,205,.22) + '<rect x="20" y="30" width="80" height="60" fill="#16213A" stroke="#E8D6B0" stroke-width="5"/>')
FAM = ''.join([_pol(BEACH, 'Family trips, a few times a year', -4), _pol(HOCKEY, 'Front row at every game', 3), _pol(RECITAL, 'Every recital and school concert', -2),
               _pol(GRAD, 'Every graduation', 4), _pol(XMAS, 'Home for every Christmas', -3)])
slide(f'''
<div class="kick">What the plan really gave him</div>
<h2>Time. <span class="gold">All the moments he used to miss.</span></h2>
<p class="big famP">Because his money was working, John didn&rsquo;t have to work every hour. From the first year, he took Emma and the kids away a few times a year. He never missed a game, a recital or a parent-teacher night. He was there for every first day of school, and he cheered at every graduation.</p>
<div class="polR">{FAM}</div>
<p class="famQ f">&ldquo;Remember the concert I missed when Lily was six? <b>I never missed another one.</b>&rdquo;</p>
''', 'sFamily')

# 26 CHAPTER 7: 90
def _roof_y(x):
    return 130 - (x - 40) * 90 / 610 if x <= 650 else 40 + (x - 650) * 90 / 610
HOUSE_P = 'M40,430 L40,130 L650,40 L1260,130 L1260,430'
HOME = ('<defs><pattern id="wp" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#5A1A22"/><rect width="20" height="40" fill="#621E27"/><circle cx="10" cy="20" r="2.4" fill="rgba(229,185,60,.35)"/></pattern>'
  '<clipPath id="hIn"><path d="M40,430 L40,130 L650,40 L1260,130 L1260,430Z"/></clipPath></defs>'
  '<g clip-path="url(#hIn)"><rect x="0" y="0" width="1300" height="430" fill="url(#wp)"/>'
  '<rect x="0" y="356" width="1300" height="74" fill="#6B4226"/>' + ''.join(f'<line x1="{x}" y1="356" x2="{x}" y2="430" stroke="rgba(0,0,0,.28)" stroke-width="2"/>' for x in range(40, 1300, 80)) +
  '<line x1="0" y1="393" x2="1300" y2="393" stroke="rgba(0,0,0,.2)" stroke-width="2"/>'
  '<rect x="0" y="346" width="1300" height="10" fill="#E8D6B0"/></g>'
  '<ellipse cx="650" cy="406" rx="400" ry="20" fill="#8E1B26" opacity=".85"/>'
  '<g><rect x="90" y="170" width="220" height="150" fill="#16213A"/>' + ''.join(f'<circle cx="{random.randint(100,300)}" cy="{random.randint(180,290)}" r="2.6" fill="#fff"/>' for _ in range(14)) +
  '<path d="M90,296 Q200,280 310,298 L310,320 L90,320Z" fill="#E8EEF6"/><rect x="196" y="170" width="8" height="150" fill="#E8D6B0"/><rect x="90" y="241" width="220" height="8" fill="#E8D6B0"/><rect x="85" y="165" width="230" height="160" fill="none" stroke="#E8D6B0" stroke-width="10"/>'
  '<path d="M74,160 C96,215 80,270 102,330 L74,330Z M326,160 C304,215 320,270 298,330 L326,330Z" fill="#9E1B26"/></g>'
  '<g fill="#3A1216" stroke="#C9A227" stroke-width="6"><rect x="480" y="160" width="80" height="62"/><rect x="600" y="148" width="100" height="78"/><rect x="740" y="160" width="80" height="62"/></g>'
  '<path d="M610,216 L630,190 L650,206 L668,182 L690,216Z" fill="#7A6A50"/><circle cx="520" cy="188" r="12" fill="#C9A9A0"/><circle cx="780" cy="188" r="12" fill="#C9A9A0"/>'
  f'<path d="{HOUSE_P}" fill="none" stroke="#8E1B26" stroke-width="22" stroke-linejoin="round"/>'
  f'<path d="{HOUSE_P}" fill="none" stroke="#E8D6B0" stroke-width="6" stroke-linejoin="round"/>'
  + ''.join(f'<line x1="{x}" y1="{_roof_y(x)+10:.1f}" x2="{x}" y2="{_roof_y(x)+20:.1f}" stroke="#1F4A30" stroke-width="2"/><circle cx="{x}" cy="{_roof_y(x)+25:.1f}" r="5.5" fill="{["#FF4D5E","#FFD27A","#7FE0A8","#FFFFFF"][k%4]}" class="hl{k%3}"/>'
            for k, x in enumerate([x for x in range(100, 1220, 55) if abs(x - 650) > 20])))
chap_full('Chapter Seven', 'Christmas 2076 &middot; John is 90', 'The Last Christmas', ch7(), 'sChap sHome', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))

# 26b CHRISTMAS MORNING REVEAL
slide(f'''
<div class="kick">Christmas morning, years later</div>
<h2>John&rsquo;s grandchildren open the last gift he left.</h2>
<div class="giftR">
  {scene(ground(1300,420)+person('lily',300,410,.62)+person('max',390,410,.56)+person('lily',910,410,.58)+person('max',1000,410,.5)
    +'<g class="gBox"><rect x="540" y="250" width="220" height="160" fill="#9E1B26"/><rect x="540" y="250" width="110" height="160" fill="rgba(255,255,255,.08)"/><rect x="636" y="250" width="28" height="160" fill="#E5B93C"/></g>'
    +'<g class="f gLid"><rect x="526" y="214" width="248" height="40" fill="#B32533"/><rect x="636" y="214" width="28" height="40" fill="#E5B93C"/><path d="M650,214 C600,150 570,200 650,214 C730,200 700,150 650,214Z" fill="#E5B93C"/></g>', 470)}
  <div class="f gVal"><span>Passed to his family, tax-free</span><b>{money(TOT90)}</b></div>
</div>
''', 'sGift', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))

# 27 LEGACY
slide(f'''
<div class="kick">The legacy</div>
<h2>When John passed, the tax bill was already planned for.</h2>
<div class="flow">
  <div class="fl f"><span>His two policies pay his corporation</span><b>{money(TOT90)}</b></div><div class="fa f">&#10140;</div>
  <div class="fl f gold"><span>Credited to the CDA</span><b>Tax-free bucket</b></div><div class="fa f">&#10140;</div>
  <div class="fl f green"><span>Paid to his family</span><b>Tax-free</b></div>
</div>
<div class="leg3">
  <div class="f">Seg funds paid his beneficiaries directly, <b>skipping probate</b>.</div>
  <div class="f">His TFSA passed to Emma <b>tax-free</b>.</div>
  <div class="f">The business stayed with Lily. <b>Nothing had to be sold.</b></div>
</div>
<div class="src">Death benefits at age 90 from both of John&rsquo;s illustrations: policy #1 {money(ILL[90]["totalDB"])} + policy #2 {money(P2[90]["totalDB"])} (current dividend scale, not guaranteed). The CDA is credited with the death benefit less the policy&rsquo;s adjusted cost basis.</div>
''', 'sLegacy', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))

# 28 JAKE
slide(f'''
<h2 class="mt">But remember Jake?</h2>
<p class="big">Same clinic. Same family. Same income. Same net worth at 40.</p>
{scene(ground(1300,420)+person('jake',650,410,1.2)+label(650,450,'Jake',"#5E6670",26), 470)}
<p class="once f">Jake decided to &ldquo;think about it.&rdquo;</p>
''', 'sJake')

# 29 SPLIT SCREEN
cmp = [('Investing', 'Seg funds + flexible plan, about 12% a year', 'Rental condos + bank mutual funds, low returns'),
       ('Age 46', 'Opened clinic #2', 'Cash stuck in the corporation'),
       ('Age 48: crash', 'Guaranteed floor, policy untouched', 'Panic-sold at the bottom, then a tax bill'),
       ('Protection', 'Seg fund guarantees, skips probate', 'No guarantees, probate fees'),
       ('Debt-free', 'At 50', 'At 58'),
       ('Age 55: partner dies', 'Buy-sell funded, business saved', 'No agreement: went into debt'),
       ('Locations', '3', '1'),
       ('Retired', 'At 65', 'At 70')]
lj = ''.join(f'<div class="spR f"><span>{a}</span><b>{b}</b></div>' for a, b, c in cmp)
rk = ''.join(f'<div class="spR f"><span>{a}</span><b>{c}</b></div>' for a, b, c in cmp)
slide(f'''
<div class="kick">Two lives, playing at once</div>
<div class="splitS">
  <div class="half john"><div class="hName">John</div>{scene(ground(600,300)+person('john',300,290,.95), 310).replace('viewBox="0 0 1300 310" width="1300"','viewBox="0 0 600 310" width="560"')}<div class="rows">{lj}</div></div>
  <div class="half jake"><div class="hName">Jake</div>{scene(ground(600,300)+person('jake',300,290,.95,mood='sad'), 310).replace('viewBox="0 0 1300 310" width="1300"','viewBox="0 0 600 310" width="560"')}<div class="rows">{rk}</div></div>
</div>
''', 'sSplit')

# 29b JAKE AT 90
JAKE90 = scene(ground(560,420) + tree(450,410,.55,lit=False) + cloud(190,40,.62)
  + ''.join(f'<line class="rain" style="animation-delay:-{k*.13:.2f}s" x1="{140+k*14}" y1="92" x2="{134+k*14}" y2="122" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>' for k in range(8))
  + person('jake',200,410,1.0,'old',mood='sad')
  + '<g transform="translate(330,330)"><rect x="0" y="0" width="70" height="80" fill="#5A4A3A"/><rect x="6" y="-18" width="58" height="20" fill="#EFE6D4" transform="rotate(-6)"/><rect x="8" y="-30" width="58" height="16" fill="#E2D7C2" transform="rotate(4)"/><text x="36" y="-16" text-anchor="middle" style="font:900 12px sans-serif;fill:#B3202A">TAX BILL</text></g>', 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 560 470" width="560"')
slide(f'''
<div class="split jake90">
  <div class="sp">{JAKE90}</div>
  <div class="sp2">
    <div class="kick red" style="text-align:left">Christmas 2076 &middot; Jake is 90</div>
    <h2 class="lft">Jake&rsquo;s last Christmas felt very different.</h2>
    <ul class="jkL">
      <li class="f"><b>Burnt out.</b> He worked until 70 and missed years of his kids growing up.</li>
      <li class="f"><b>Not enough wealth.</b> His savings were taxed every single year.</li>
      <li class="f"><b>No plan for the business.</b> When his partner died, he went into debt to buy out the family.</li>
      <li class="f"><b>No plan for his family.</b> A large tax bill, and nothing passing tax-free.</li>
    </ul>
    <p class="jkQ f">&ldquo;I always thought I&rsquo;d get to it next year.&rdquo;</p>
  </div>
</div>
<p class="f mid">Same start as John. Same income. Same family. <b class="gold">One simple decision apart.</b></p>
''', 'sJake90')

# 31 WEALTH GAP + TAX AT DEATH
def _jake_nw(a):
    home = 1.6e6*1.03**(a-40); mort = 1e6*max(0, (58-a)/18); loan = 5e5*max(0, (58-a)/18)
    bus = 9e5*1.04**(min(a, 70)-40)
    corp = 5e5*1.04**(a-40) + sum(100000*1.04**(min(a,90)-y) for y in range(41, min(a,60)+1))
    t, r, n = 109000, 150000, 0
    for y in range(41, a+1):
        if y <= 65: t = t*1.05 + 7000; r = r*1.05 + 33810; n = n*1.05 + 15000
        else: t *= 1.05*.9; r *= 1.05*.9; n *= 1.05*.9
        if y == 48: n *= .75
    return home - mort + bus - loan + corp + t + r + n, corp, r, n
J_NW, J_CORP, J_RRSP, J_NR = _jake_nw(90)
J_TAX = 0.5*J_CORP + 0.5*J_RRSP + 0.25*J_NR
J_FAM = J_NW - J_TAX
JN_NW = NW(90)
JN_TAX = 0.5*SAV[90][1] + 0.25*SAV[90][2]
JN_FAM = JN_NW - JN_TAX
def _bar(lbl, j, k, mx, cls=''):
    return (f'<div class="wgR f"><span class="wgL">{lbl}</span><div class="wgB"><i class="jk" style="width:{j/mx*100:.1f}%"><b>{money(j)}</b></i><em>Jake</em></div>'
            f'<div class="wgB"><i class="jn {cls}" style="width:{k/mx*100:.1f}%"><b>{money(k)}</b></i><em>John</em></div></div>')
MXW = max(JN_NW, J_NW)
slide(f'''
<div class="kick">At 90: two families, one difference</div>
<h2>The wealth gap, and the tax bill Jake never planned for</h2>
<div class="wg">
  {_bar('Net worth', J_NW, JN_NW, MXW)}
  {_bar('Paid out tax-free through the CDA', 0, TOT90, MXW, 'gold')}
  {_bar('Estimated tax at death', J_TAX, JN_TAX, MXW, 'red')}
  {_bar('What reached the family', J_FAM, JN_FAM, MXW, 'green')}
</div>
<p class="f mid">Jake never used his CDA, so his corporate savings were taxed again on the way out. <b class="green">{money(JN_FAM - J_FAM)} more</b> reached John&rsquo;s family.</p>
<p class="f mid wgTie">The difference wasn&rsquo;t luck. John was <b>open to learning</b>, and he <b>took action</b>, because he understood the value of time.</p>
<div class="src">Illustrative. Jake: same income and savings, 5% average return (real estate and bank mutual funds), panic-sold 25% lower in the 2034 crash, one clinic, debt-free at 58; tax at death about 50% on corporate assets and RRSP, 25% on non-registered gains. John: net worth from the story bar; both policies&rsquo; death benefits paid through the CDA. Not tax advice.</div>
''', 'sBars')

# 30 TWO DOCTORS
slide(f'''
<div class="stamp">Real case study</div>
<div class="kick">Stepping out of the story</div>
<h2>John and Jake are fictional. <span class="gold">This case study is real.</span></h2>
<p class="big">A real case study and comparison was done: same income, same savings, one difference.</p>
<div class="docs">
  <div class="dc f"><b>Dr. Brown</b><span>No whole life</span><div class="dv red">$2.7M</div><em>reached his family &middot; 72% lost to tax</em></div>
  <div class="dc f win"><b>Dr. Smith</b><span>Added whole life</span><div class="dv green">$7.8M</div><em>reached his family &middot; 42% to tax</em></div>
</div>
<p class="f mid">Same income. Same savings. <b>Nearly 3&times; more for the family.</b></p>
<div class="src">Levine Financial Group, A Tale of Two Physicians (Dec 2025): corporate assets at death, age 85.</div>
''', 'sDocs')

# 31c SCOREBOARD FINALE
slide('''
<h2 class="sr">The final scoreboard</h2>
''', 'sScore', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))
def _tile(lbl, a, b, cls=''):
    return f'<div class="sbT {cls}"><span>{lbl}</span><div class="sbV"><em>At 40</em><i>{a}</i></div><div class="sbV b"><em>At 90</em>{b}</div></div>'
SCORE = ('<div id="hudBig"><div class="sbHead"><em>Christmas 2076</em><b>John&rsquo;s Scoreboard</b><span>From the day he met Mehar at 40, to his last Christmas at 90</span></div><div class="sbG">'
  + _tile('Net worth', money(NW(40)), counter(int(NW(90))))
  + _tile('Tax-free to his family', '$0', counter(int(TOT90)), 'gold')
  + _tile('Taken out in retirement', '$0', counter(int(SAV_W)))
  + _tile('7 key needs covered', '0 of 7', '<b class="cnt" data-to="7" data-pre="" data-suf=" of 7">0 of 7</b>')
  + _tile('3 rules of money', 'Against him', '<b class="sbW">Working for him</b>', 'green')
  + _tile('Christmas list', '0 of 4', '<b class="cnt" data-to="4" data-pre="" data-suf=" of 4">0 of 4</b>', 'green')
  + '</div><div class="sbSig">With gratitude, from John&rsquo;s team: Mehar, David &amp; Sarah</div></div>')

# 32 EVERYTHING ACCOMPLISHED + TEAM
wl2 = ''.join(f'<li><i class="box on"></i>{w}</li>' for w in wl)
slide(f'''
<div class="split">
  <div class="scroll done"><div class="scT">John&rsquo;s Christmas List</div><ul class="wl">{wl2}</ul><div class="scSig">&mdash; J.</div></div>
  <div class="sp2">
    <h2 class="lft">John didn&rsquo;t get lucky.</h2>
    <p class="lft big">He had a team: <b>Mehar, David and Sarah.</b></p>
    <div class="allg f"><span>7 needs met</span><span>3 rules on his side</span><span>3 goals reached: protection, income, legacy</span></div>
    <p class="lft f ask">Who&rsquo;s on <b class="red">your</b> team?</p>
  </div>
</div>
''', 'sDone', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))

# 33 CTA
slide(f'''
<div class="kick">Your move</div>
<h2>Let&rsquo;s Write Your Story</h2>
<p class="ctaQ">&ldquo;Today is the second-best day to start. <b>The best day was yesterday.</b>&rdquo;</p>
<p class="big">No matter your age, your income, or your goals, this belongs in your plan.</p>
<div class="cta">
  <div class="f"><i>1</i><b>Book a One-on-One</b><span>A private, no-pressure conversation about your business and your goals.</span></div>
  <div class="f"><i>2</i><b>Your Personal Evaluation</b><span>We map your corporation&rsquo;s real numbers and build an illustration around <strong>you</strong>.</span></div>
  <div class="f gold"><i>3</i><b>Qualify &amp; Start</b><span>Confirm your coverage and put the plan to work, with your accountant and lawyer.</span></div>
</div>
''', 'sCta')

# 34 THANK YOU
slide(f'''
<div class="kick">Team All In</div>
<h1 class="ttl"><span class="hatL">H<svg class="hat" viewBox="0 0 120 110" aria-hidden="true"><path d="M8,92 C30,40 62,8 98,14 C108,16 112,30 104,44 C96,58 92,72 96,88Z" fill="#D11F2E"/><path d="M8,92 C30,40 62,8 98,14 C80,20 54,46 40,90Z" fill="#9E1424"/><rect x="0" y="84" width="104" height="22" rx="11" fill="#FFF"/><circle cx="104" cy="44" r="13" fill="#FFF"/></svg></span>appy Holidays</h1>
<p class="big">Thank you, and happy holidays. Scan to book your one-on-one and see if you qualify.</p>
<div class="qr"><img src="{QR}" alt="QR code"><span>Scan me</span></div>
{scene(ground(1300,200)+tree(170,200,.6)+tree(1130,200,.6)+gift(300,200,.6)+gift(1000,200,.6,'#2F6E4C'), 230)}
''', 'sThanks')

# service ribbons
SVC = {'sPol2': 7, 'sCdaFill': 3, 'sFund': 3, 'sRajPay': 7, 'sRajBS': 5, 'sNeeds': 2, 'sDollar': 3, 'sBuckets': 3, 'sShock': 3, 'sProbs': 3, 'sTeam': 4, 'sStruct': 5, 'sAio': 5, 'sPlan': 5, 'sSnap': 5,
       'sChart': 5, 'sCda': 3, 'sLoc2': 7, 'sIfa': 7, 'sCrash': 7, 'sRaj': 7, 'sRetire': 7, 'sSucc': 7}
for i, h in enumerate(SLIDES):
    cls = h.split('class="slide ', 1)[1].split('"', 1)[0].split()[0]
    if cls in SVC:
        k = SVC[cls]
        SLIDES[i] = h.replace('>', f'><div class="svc">&#9733; Mehar&rsquo;s process &middot; Step {k} of 7: <b>{STEPS[k-1][0]}</b></div>', 1)
    elif 'sChap' in h.split('>', 1)[0] and 'He Starts Now' in h:
        SLIDES[i] = h.replace('>', '><div class="svc">&#9733; Mehar&rsquo;s process &middot; Step 6 of 7: <b>Start</b></div>', 1)

# action banners: every time John acts with Mehar's help
TA, MS, PW = 'John takes action', 'Milestone', 'The plan at work'
ACT = {'sShock': (TA, 'Decides to start filling his tax-free bucket, as soon as possible'),
       'sTeam': (TA, 'Brings his accountant and his lawyer to the table with Mehar'),
       'sFund': (TA, 'Increases his personal protection to $2.5M of life insurance (permanent + term) and $250K critical illness'),
       'sPlan': (MS, 'Application approved: his corporate-owned whole life policy starts, $100K a year'),
       'sSeg': (TA, 'Moves his TFSA and RRSP into seg funds, and starts investing $15K a year'),
       'sLoc2': (TA, 'Opens clinic #2'),
       'sIfa': (TA, 'Sets up an IFA: borrows $500K against his policy to fund clinic #2'),
       'sPol2': (TA, 'Starts a second corporate policy: $150K a year for 15 years'),
       'sFamily': (PW, 'Time with his family: every trip, every game, every graduation'),
       'sRajBS': (TA, 'Sets up a funded buy-sell with his new partner, Raj'),
       'sCrash': (TA, 'Stays the course: Mehar calls him the morning of the crash'),
       'sDebt': (MS, 'Debt-free at 50: practice loan and mortgage paid off'),
       'sRajPay': (PW, 'Raj&rsquo;s family is paid in full, and the clinic is saved'),
       'sRetire': (TA, 'Retires at 65, with a holding company, estate freeze and income plan in place'),
       'sSave': (TA, 'Starts drawing retirement income: his investments, plus cash value from his personal and corporate policies'),
       'sSucc': (TA, 'Passes the clinics to Lily; the insurance gives Max equal value'),
       'sLegacy': (PW, f'His family receives {money(TOT90)}, tax-free')}
for i, h in enumerate(SLIDES):
    head = h.split('>', 1)[0]
    cls = head.split('class="slide ', 1)[1].split('"', 1)[0].split()[0]
    a = ACT.get(cls)
    if not a and 'He Starts Now' in h and 'sChap' in head:
        a = (TA, 'Applies for the plan, and goes through the application process with Mehar')
    if a:
        SLIDES[i] = h.replace('<section ', f'<section data-actl="{a[0]}" data-act="{a[1]}" ', 1)

# ------------------------------------------------------------------ page
flakes = ''.join(f'<i style="left:{random.uniform(-5,100):.1f}%;--d:-{random.uniform(0,22):.1f}s;--t:{random.uniform(14,26):.1f}s;--s:{random.uniform(.6,2.2):.2f};--x:{random.uniform(-60,60):.0f}px;--o:{random.uniform(.35,.95):.2f}"></i>' for _ in range(46))
flakes2 = ''.join(f'<i style="left:{random.uniform(-5,100):.1f}%;--d:-{random.uniform(0,30):.1f}s;--t:{random.uniform(24,40):.1f}s;--s:{random.uniform(.3,.8):.2f};--x:{random.uniform(-30,30):.0f}px;--o:{random.uniform(.25,.6):.2f}"></i>' for _ in range(40))
bokeh = ''.join(f'<i style="left:{random.uniform(0,100):.0f}%;top:{random.uniform(5,90):.0f}%;--sz:{random.randint(80,260)}px;--d:-{random.uniform(0,30):.0f}s;--c:{random.choice(["rgba(255,190,90,.16)","rgba(255,120,90,.12)","rgba(255,230,170,.12)"])}"></i>' for _ in range(12))
bulbs = ''.join(f'<i style="left:{2+k*3.2:.1f}%;top:{14+8*abs(((k%8)-4))/4:.0f}px;--c:{["#FF4D5E","#FFD27A","#7FE0A8","#FFFFFF"][k%4]};animation-delay:{(k%7)*.31:.2f}s"></i>' for k in range(31))
CLK_TICKS = ''.join(f'<line x1="0" y1="-84" x2="0" y2="{-74 if k % 3 else -66}" class="cTk" transform="rotate({k*30})"/>' for k in range(12))
orn_hud = ''.join(f'<i title="{n}"></i>' for n in NEEDS)

CSS = open(os.path.join(HERE, 'style.css')).read().replace('__TORN__', open(os.path.join(HERE,'torn.txt')).read())
CSS = CSS.replace('__CAVEAT__', 'data:font/woff2;base64,' + __import__('base64').b64encode(open(os.path.join(HERE, 'source', 'caveat-700.woff2'), 'rb').read()).decode())
JS = open(os.path.join(HERE, 'engine.js')).read()
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Gift That Keeps Giving: John&rsquo;s Story</title>
<style>{CSS}</style></head>
<body>
<div id="stage">
  {GDEFS}
  <div class="frame"></div>
  <div class="bokeh" aria-hidden="true">{bokeh}</div>
  <div class="snow far" aria-hidden="true">{flakes2}</div>
  <div class="snow" aria-hidden="true">{flakes}</div>
  <div class="vign" aria-hidden="true"></div>
  <div class="garland" aria-hidden="true"><svg viewBox="0 0 1440 40" preserveAspectRatio="none"><path d="M0,6 Q90,34 180,8 T360,8 T540,8 T720,8 T900,8 T1080,8 T1260,8 T1440,8" fill="none" stroke="#1F4A30" stroke-width="5"/></svg>{bulbs}</div>
  <div class="holly hl" aria-hidden="true"></div><div class="holly hr" aria-hidden="true"></div>
  <div class="brand">TEAM <b>ALL IN</b></div>
  <div id="ui"><button id="bToc" title="Slides (T)">&#9776;</button><button id="bEdit" title="Edit names (E)">&#9998;</button><button id="bSet" title="Settings (S)">&#9881;</button><button id="bFs" title="Full screen (F)">&#x26F6;</button></div>
  <div id="toc" class="panel"><div class="pH"><b>Slides</b><span>Click to jump &middot; eye to hide</span><button class="pX">&times;</button></div><div id="tocL"></div><div class="pF"><button id="tocAll">Show all</button></div></div>
  <div id="set" class="panel"><div class="pH"><b>Settings</b><span>Saved on this computer</span><button class="pX">&times;</button></div><div id="setL" style="overflow:auto"></div><div class="pF"><button id="setReset">Reset settings</button></div></div>
  <div id="timer" title="Click to restart the timer">0:00 / 40:00</div><div id="black"></div><div id="curt" aria-hidden="true"><i class="cL"></i><i class="cR"></i></div>
  <div id="edit" class="panel"><div class="pH"><b>Edit names &amp; title</b><button class="pX">&times;</button></div><div id="editL"></div><div class="pF"><button id="edReset">Reset</button><button id="edSave" class="pri">Save</button></div></div>
  <div class="deck">{"".join(SLIDES)}</div>
  <div id="tp" aria-hidden="true"><div class="tpC">
    <svg viewBox="-110 -110 220 220" width="300" height="300" class="clk"><circle r="102" class="cRim"/><circle r="92" class="cFace"/>{CLK_TICKS}<line x1="0" y1="8" x2="0" y2="-48" class="cH hr"/><line x1="0" y1="12" x2="0" y2="-76" class="cH mn"/><circle r="6" class="cPin"/></svg>
    <span class="tpF">Fast-forward &#9654;&#9654;</span><b id="tpY">2026</b><em id="tpA">John is 40</em></div></div>
  <div id="hud" class="paper">
    <div class="hTime"><span>Age</span><div class="hTrack"><i id="hDot"></i></div><b id="hAge">40</b></div>
    <div class="hNw"><span>Net worth</span><b id="hNw">$0</b></div>
    <div class="hCda"><div class="hB"><i id="hBf"></i></div><div><span>Future CDA credit</span><b id="hCda">$0</b></div></div>
    <div class="hNeeds"><span>7 needs</span><div id="hOrn">{orn_hud}</div></div>
    <div class="hRules"><span>3 rules</span><div id="hRu"><em>Compound</em><em>Risk</em><em>Tax</em></div></div>
    {SCORE}
  </div>
  <div id="act" aria-live="polite"><i>&#10003;</i><div><span id="actL">John takes action</span><b id="actT"></b><em>with Mehar&rsquo;s help</em></div></div>
  <div class="intl">FOR INTERNAL USE ONLY</div>
  <div class="foot">Illustrative story: John and Jake are fictional; net worth figures are illustrative. Policy values from a real Equitable illustration (current dividend scale, not guaranteed). We do not offer tax or legal advice; please consult a tax and/or legal professional.</div>
  <div class="prog"><i id="prog"></i></div>
</div>
<script>{JS}</script>
</body></html>'''
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)
print('slides', len(SLIDES), 'KB', len(html.encode()) // 1024)
