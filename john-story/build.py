#!/usr/bin/env python3
"""Builds john-story/index.html  ("The Gift That Keeps Giving: John's Story").
Run:  python3 john-story/build.py
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ILL = {r['age']: r for r in json.load(open(os.path.join(HERE, 'illustration.json')))['rows']}
QR = open(os.path.join(HERE, 'source', 'qr.txt')).read().strip()

def money(v, short=True):
    if short and v >= 1_000_000:
        return f"${v/1e6:.2f}M".replace('.00M', 'M')
    if short and v >= 1000:
        return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"

# ------------------------------------------------------------------ characters
SKIN = {'john': '#F2C9A5', 'emma': '#EDBE98', 'lily': '#F4CFAE', 'max': '#F4CFAE',
        'mehar': '#C48A5C', 'david': '#EBC39C', 'sarah': '#8E5B3C', 'raj': '#B57B52', 'jake': '#F2C9A5'}

def hair(style, col):
    s = {
        'short': f'<path d="M-36,-196 C-38,-242 38,-242 36,-196 C31,-222 -31,-222 -36,-196Z" fill="{col}"/>',
        'side':  f'<path d="M-36,-194 C-40,-244 40,-244 36,-194 C30,-226 -8,-230 -36,-194Z" fill="{col}"/>',
        'long':  f'<path d="M-37,-196 C-40,-244 40,-244 37,-196 L40,-150 L26,-150 L28,-200 C20,-222 -20,-222 -28,-200 L-26,-150 L-40,-150Z" fill="{col}"/>',
        'bun':   f'<circle cx="0" cy="-238" r="14" fill="{col}"/><path d="M-36,-196 C-38,-242 38,-242 36,-196 C31,-222 -31,-222 -36,-196Z" fill="{col}"/>',
        'pony':  f'<path d="M30,-214 C58,-206 58,-168 44,-160 C48,-184 40,-200 30,-206Z" fill="{col}"/><path d="M-36,-196 C-38,-242 38,-242 36,-196 C31,-222 -31,-222 -36,-196Z" fill="{col}"/>',
        'curly': ''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="{col}"/>' for x, y in [(-28,-214),(-14,-228),(2,-232),(18,-228),(30,-214),(-34,-198),(34,-198)]),
        'grey':  f'<path d="M-36,-196 C-38,-236 38,-236 36,-196 C31,-216 -31,-216 -36,-196Z" fill="#D9D9D9"/>',
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
        'mehar': dict(hair=('side', '#1E1A18'), top='#1F2A44', bottom='#1F2A44', acc=['tie']),
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
            o.append(f'<circle cx="{ox}" cy="{oy}" r="8" fill="{c}"/>')
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
    return f'<path d="M0,{y} Q{w*.25},{y-26} {w*.5},{y-6} T{w},{y-14} L{w},{y+80} L0,{y+80}Z" fill="#FFFFFF" stroke="#E4E8EE" stroke-width="2"/>'

def gift(x, y, s=1.0, col='#9E1B26', txt=''):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-60" y="-100" width="120" height="100" fill="{col}"/>'
            '<rect x="-68" y="-118" width="136" height="24" fill="#B32533"/>'
            '<rect x="-9" y="-118" width="18" height="118" fill="#E5B93C"/>'
            '<path d="M0,-118 C-40,-160 -60,-120 0,-118 C60,-120 40,-160 0,-118Z" fill="#E5B93C"/>'
            f'<text x="0" y="-40" text-anchor="middle" style="fill:#fff;font:700 14px Georgia,serif">{txt}</text></g>')

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
        cda = ILL[age]['totalDB'] if age in ILL else 0
    return dict(age=age, nw=nw, needs=needs, rules=rules, cda=cda)

def counter(to, pre='$', suf='', cls=''):
    return f'<b class="cnt {cls}" data-to="{to}" data-pre="{pre}" data-suf="{suf}">{pre}0{suf}</b>'

# ================================================================== SLIDES
random.seed(3)

# 1 COVER
slide(f'''
<div class="cover">
  <div class="kick">Team All In presents</div>
  <h1 class="ttl">The Gift That<br>Keeps Giving</h1>
  <div class="rule"></div>
  <p class="subt">A Christmas story about John, his business,<br>and the legacy he left behind.</p>
</div>
{scene(ground(1300,440)+house(360,440,1.0)+tree(980,440,1.25)+person('john',640,440,.8)+person('emma',740,440,.76)+person('lily',830,440,.5)+person('max',890,440,.42), 470)}
''', 'sCover')

# 2 HOOK
slide(f'''
<div class="kick red">A true story · Ontario, 2024</div>
<h2>Every year, Canadian families give the biggest gift of their lives&hellip;</h2>
<p class="big f">&hellip;to the taxman. <span class="red">Most never meant to.</span></p>
<div class="hookRow f">
  <div class="hookCard"><span>Their parents&rsquo; RRSP</span><b>$715,000</b></div>
  <div class="arrow">&#10140;</div>
  <div class="hookCard tax"><span>Tax due in one year</span><b>&asymp; $659,000</b></div>
  <div class="arrow">&#10140;</div>
  <div class="hookCard left"><span>Left for two children</span>{counter(56000)}</div>
</div>
<p class="f mid">Two parents, gone eleven months apart. A will, a cottage, and <b>no plan for the tax.</b></p>
<div class="src">Source: SooToday / Village Media (2025); MoneySense, Ask a Planner (Oct 2025). Tax figures are a CFP&rsquo;s estimate.</div>
''', 'sHook')

# 3 TWO OWNERS
slide(f'''
<h2 class="mt">This is a story about two business owners.</h2>
<p class="big">Same life. Same income. Same chances. <b class="gold">One decision apart.</b></p>
{scene(ground(1300,430)+person('john',520,420,1.15)+person('jake',780,420,1.15)+label(520,460,'John',size=24)+'<g class="f">'+label(780,460,'Jake','#5E6670',24)+'</g>', 470)}
<p class="once f">Once upon a time&hellip;</p>
''', 'sTwo')

# 4 CHAPTER 1
slide(chapter('Chapter One', 'Christmas Eve, 2026 · John is 40', 'The Rat Race',
    ground(1300,400)+clinic(330,400,1.0)+person('john',520,400,.95,'coat')+
    '<g><rect x="760" y="140" width="380" height="260" fill="#F4EBDD" stroke="#C9B79C" stroke-width="2"/><rect x="800" y="180" width="300" height="180" fill="#F7C96B"/>'
    + person('emma',880,360,.62)+person('lily',960,360,.42)+person('max',1020,360,.36)+tree(1070,360,.4)+'</g>'
    +'<text x="520" y="120" text-anchor="middle" class="nm" style="fill:#5E6670;font-size:22px">9:47 p.m. &mdash; still at the clinic</text>'),
    'sChap', hud=H(40, 1509000))

# 5 JOHN'S NUMBERS
rows = [('Clinic revenue', '$500K&ndash;$750K a year', ''), ('Practice loan', '$1M &middot; <b class="red">$500K still owing</b>', ''),
        ('Home', '$1.6M &middot; <b class="red">$1M mortgage</b>', ''), ('Clinic value', '$900K', ''),
        ('Corporate savings', '$250K', ''), ('RRSP', '$150K', ''), ('TFSA', '$109K &middot; <b class="green">maxed out</b>', '')]
rhtml = ''.join(f'<div class="bsR f"><span>{a}</span><b>{b}</b></div>' for a, b, _ in rows)
slide(f'''
<div class="kick">Meet John</div>
<h2>Dentist. 10 years in business. A good income.</h2>
<div class="split">
  <div class="bs">{rhtml}<div class="bsR tot f"><span>Net worth</span>{counter(1509000)}</div></div>
  <div class="sp">{scene(ground(520,420)+person('john',160,410,1.0,'coat')+person('emma',290,410,.92)+person('lily',380,410,.6)+person('max',450,410,.5)+label(160,452,'John')+label(290,452,'Emma')+label(380,452,'Lily, 6')+label(450,452,'Max, 4'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')}</div>
</div>
''', 'sNums', hud=H(40, 1509000))

# 6 RAT RACE: 3 RULES RED
slide(f'''
<div class="kick">The problem</div>
<h2>John works harder every year. His net worth barely moves.</h2>
<div class="rules3">
  <div class="rc f"><div class="rI">&#8635;</div><b>The Compound Effect</b><span>His savings sit in the corporation, earning almost nothing.</span><em>Against him</em></div>
  <div class="rc f"><div class="rI">&#9888;</div><b>The Risk Effect</b><span>Everything he owns is tied to one clinic and one house.</span><em>Against him</em></div>
  <div class="rc f"><div class="rI">%</div><b>The Tax Effect</b><span>Investment income in his corporation is taxed at about 50% in BC, every year.</span><em>Against him</em></div>
</div>
<p class="f mid">All three rules of money were working <b class="red">against</b> John.</p>
''', 'sRules', hud=H(40, 1509000))

# 7 WISH LIST
wl = ['Pay off every debt in 10 years', 'Open more locations', 'Retire by 65', 'Take care of Emma and the kids, forever']
wlh = ''.join(f'<li class="f"><i class="box"></i>{w}</li>' for w in wl)
slide(f'''
<div class="split">
  <div class="scroll"><div class="scT">John&rsquo;s Christmas List</div><ul class="wl">{wlh}</ul><div class="scSig">&mdash; J.</div></div>
  <div class="sp2"><h2 class="lft">He wasn&rsquo;t asking for a sports car.</h2><p class="lft big">He wanted his <b>time</b> back, and a future his family could count on.</p><p class="lft f mid">So in January, he made an appointment.</p></div>
</div>
''', 'sList', hud=H(40, 1509000))

# 8 CHAPTER 2
slide(chapter('Chapter Two', 'January 2027 · John is 40', 'The Meeting',
    '<rect x="0" y="0" width="1300" height="430" fill="#F7F1E3"/><rect x="980" y="60" width="200" height="140" fill="#E4E8EE" stroke="#C9CED6" stroke-width="3"/>'
    '<text x="1080" y="140" text-anchor="middle" style="font:700 22px Georgia;fill:#7A0F1A">TEAM ALL IN</text>'
    + person('john',470,410,1.0)+person('mehar',830,410,1.0)+desk(650,410,1.0)+label(470,150,'John',size=22)+label(830,150,'Mehar, his advisor',size=22)),
    'sChap', hud=H(40, 1509000))

# 9 7 NEEDS CHECK-UP
orn = ''.join(f'<div class="orn f"><i></i><span>{n}</span></div>' for n in NEEDS)
slide(f'''
<div class="kick">The check-up</div>
<h2>Every corporation has 7 key needs. John had covered <span class="red">none</span> of them.</h2>
<div class="ornRow">{orn}</div>
<p class="f mid">Mehar didn&rsquo;t sell John anything that day. <b>He showed him the gaps.</b></p>
''', 'sNeeds', hud=H(40, 1509000))

# 10 3 HIDDEN PROBLEMS (with loonie)
slide(f'''
<div class="kick">What Mehar found</div>
<h2>Three hidden problems in John&rsquo;s business</h2>
<div class="probs">
  <div class="pb f"><div class="pbN">1</div><b>The estate tax trap</b><span>If John died, his corporation would face tax on his shares and again when the money is paid out to Emma.</span></div>
  <div class="pb f"><div class="pbN">2</div><b>Trapped money</b><span>Taking cash out of the corporation costs him about half. His dollar is worth 88&cent; inside, only 50&cent; outside.</span>
    <div class="loons"><div class="loon"><i style="--p:50%"></i></div><b class="red">50&cent;</b><div class="loon"><i style="--p:12%"></i></div><b class="green">88&cent;</b></div></div>
  <div class="pb f"><div class="pbN">3</div><b>Money not multiplying</b><span>His savings sit in GICs, taxed every year. Nothing is building on its own.</span></div>
</div>
''', 'sProbs', hud=H(40, 1509000))

# 11 THE TEAM
slide(f'''
<div class="kick">The team</div>
<h2>John didn&rsquo;t replace his team. <span class="gold">He completed it.</span></h2>
{scene(ground(1300,400)+person('david',260,390,1.0)+person('john',520,390,1.05)+person('sarah',780,390,1.0)+person('mehar',1040,390,1.0)
       +label(260,430,'David, CPA',size=20)+label(520,430,'John',size=20)+label(780,430,'Sarah, lawyer',size=20)+label(1040,430,'Mehar, advisor',size=20), 440)}
<div class="roles">
  <div class="f"><b>David &middot; accountant</b><span>Tax returns, CDA tracking, capital dividend elections</span></div>
  <div class="f"><b>Sarah &middot; lawyer</b><span>Wills, holding company, shareholder agreement, estate freeze</span></div>
  <div class="f"><b>Mehar &middot; advisor</b><span>The strategy: insurance, investments, and keeping everyone working together</span></div>
</div>
<p class="note2">John brought David and Sarah to the table himself.</p>
''', 'sTeam', hud=H(40, 1509000))

# 12 CHAPTER 3
slide(chapter('Chapter Three', 'Spring 2027 · John is 41', 'The Plan',
    ground(1300,400)+gift(650,390,1.6,txt='THE PLAN')+person('john',400,400,.95)+person('mehar',900,400,.95)+tree(1130,400,.8)),
    'sChap', hud=H(41, 1560000, '0,4', '100'))

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
''', 'sPlan', hud=H(41, 1560000, '0,4', '100'))

# 14 GROWTH CHART (real data)
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
<svg class="chart" viewBox="0 0 1260 430" width="1260" height="430">{grid}{ticks}
  <polyline class="ln db" points="{db}"/><polyline class="ln cv" points="{cv}"/>
  <text x="1108" y="{py(i90["totalDB"])+5:.0f}" class="lg gold">Death benefit</text><text x="1108" y="{py(i90["totalCV"])+5:.0f}" class="lg green">Cash value</text>{marks}</svg>
<div class="src">Same illustration. Total cash value and total death benefit, current dividend scale (not guaranteed). Age 90: cash value {money(i90["totalCV"])}, death benefit {money(i90["totalDB"])}.</div>
''', 'sChart', hud=H(41, 1560000, '0,4', '100'))

# 15 CDA
slide(f'''
<div class="kick">The secret weapon</div>
<h2>The Capital Dividend Account (CDA)</h2>
<div class="split">
  <div class="sp">{scene(bucket(260,400,1.25,.18,'bkA'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')}</div>
  <div class="cdaPts">
    <div class="f"><b>A notional account.</b> Not a bank account: a running tally of tax-free dollars in John&rsquo;s corporation.</div>
    <div class="f"><b>What fills it:</b> the tax-free half of capital gains, capital dividends received, and the big one: <b class="gold">life insurance paid to the corporation.</b></div>
    <div class="f"><b>What it does:</b> every dollar in it can be paid to John&rsquo;s family as a <b class="green">tax-free capital dividend.</b></div>
    <div class="f note3">David tracks the balance and files the election. Mehar fills it.</div>
  </div>
</div>
''', 'sCda', hud=H(41, 1560000, '0,4', '101'))

# 16 ROGERS
slide(f'''
<div class="kick">A real case &middot; proven in Tax Court</div>
<h2>The Rogers family did exactly this.</h2>
<div class="rog">
  <div class="rogBig f">{counter(102, '$', 'M')}<span>through the CDA, tax-free</span></div>
  <div class="rogTxt">
    <p class="f">Corporate-owned life insurance on Ted Rogers, held in the family&rsquo;s private companies.</p>
    <p class="f">On his passing, about $102 million was credited to the CDA and paid out as tax-free capital dividends.</p>
    <p class="f">The CRA challenged it. <b>The Tax Court ruled for the family.</b></p>
  </div>
</div>
<p class="f mid">John doesn&rsquo;t need $102 million. <b>He needs the same playbook.</b></p>
<div class="src">Rogers Enterprises (2015) Inc. v. The Queen, Tax Court of Canada.</div>
''', 'sRogers', hud=H(41, 1560000, '0,4', '101'))

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
''', 'sRe', hud=H(42, 1640000, '0,4', '101'))

# 18 SEG FUNDS
feat = [('&#128200;', 'Market growth'), ('&#128737;', '75&ndash;100% guarantee'), ('&#8635;', 'Resets lock in gains'), ('&#128274;', 'Creditor protection'), ('&#9993;', 'Skips probate'), ('&#127963;', 'Assuris protection')]
fh = ''.join(f'<div class="ft f"><i>{a}</i>{b}</div>' for a, b in feat)
slide(f'''
<div class="kick">Why segregated funds</div>
<h2>Growth <span class="gold">and</span> guarantees, in one place</h2>
<div class="feats">{fh}</div>
<p class="f mid"><b>Emma</b> liked the guarantee. <b>Sarah</b> liked that it skips probate. <b>John</b> liked sleeping at night.</p>
''', 'sSeg', hud=H(42, 1640000, '0,4', '101'))

# 19 CHAPTER 4 + location 2 + famous names
slide(f'''
<div class="kick">Chapter Four &middot; Christmas 2032 &middot; John is 46</div>
<h2>Location #2 opens.</h2>
{scene(ground(1300,380)+clinic(300,370,.85,1)+clinic(640,370,.85,2)+person('john',920,370,.85,'coat')+person('raj',1060,370,.85,'coat')+label(1060,405,'Dr. Raj, his new partner',size=18), 420)}
<div class="loan">
  <p class="f">John <b>borrowed against his policy&rsquo;s cash value</b> ({money(ILL[46]["totalCV"])}) to fund it.</p>
  <p class="f">The policy kept growing as if he had never touched it. <b class="gold">His corporate dollar worked twice.</b></p>
</div>
''', 'sLoc2', hud=H(46, 2600000, '0,4,5', '101'))

# 20 FAMOUS NAMES
slide(f'''
<div class="kick">He wasn&rsquo;t the first</div>
<h2>Same playbook, famous names</h2>
<div class="fam">
  <div class="f"><b>Walt Disney</b><span>is widely reported to have borrowed against his life insurance to help fund Disneyland.</span></div>
  <div class="f"><b>Ray Kroc</b><span>is widely reported to have used his policies&rsquo; cash value to help cover salaries in McDonald&rsquo;s early years.</span></div>
  <div class="f"><b>John</b><span>borrowed against his to open clinic #2.</span></div>
</div>
<p class="f mid">The policy wasn&rsquo;t just protection. <b>It was the engine.</b></p>
''', 'sFam', hud=H(46, 2600000, '0,4,5', '101'))

# 21 TWIST 1 crash
slide(f'''
<div class="kick red">Plot twist #1 &middot; 2034 &middot; John is 48</div>
<h2>The market crashes 25%.</h2>
{scene(ground(1300,380)+'<g class="storm"><ellipse cx="650" cy="90" rx="220" ry="60" fill="#5E6670"/><ellipse cx="520" cy="110" rx="120" ry="50" fill="#6E7680"/><ellipse cx="790" cy="110" rx="130" ry="50" fill="#6E7680"/>'
  + ''.join(f'<line x1="{x}" y1="150" x2="{x-14}" y2="200" stroke="#9AA6B2" stroke-width="3"/>' for x in range(470,840,40))+'</g>'
  + '<path d="M480,250 Q650,150 820,250Z" fill="#9E1B26"/><path d="M650,170 L650,360" stroke="#5E3820" stroke-width="6"/>'
  + person('john',600,370,.8)+person('emma',700,370,.76), 420)}
<div class="twist">
  <p class="f">John&rsquo;s seg funds had a <b>guaranteed floor</b>. When markets recovered, a <b>reset</b> locked in the new high.</p>
  <p class="f">His policy&rsquo;s cash value <b class="green">didn&rsquo;t drop at all</b> ({money(ILL[48]["totalCV"])} and climbing).</p>
</div>
''', 'sCrash', hud=H(48, 2750000, '0,4,5', '111'))

# 22 DEBT-FREE AT 50
slide(f'''
<div class="kick">Christmas 2036 &middot; John is 50</div>
<h2>Debt-free. <span class="green">Right on schedule: 10 years.</span></h2>
<div class="debt">
  <div class="dC f"><span>Practice loan</span><s>$500,000</s><b>$0</b></div>
  <div class="dC f"><span>Home mortgage</span><s>$1,000,000</s><b>$0</b></div>
  <div class="dC f gold"><span>Policy cash value</span><b>{money(i50["totalCV"])}</b></div>
</div>
<p class="f mid">Two clinics paid off his debts faster. <b>&#10003; Pay off every debt in 10 years.</b></p>
''', 'sDebt', hud=H(50, 4100000, '0,4,5', '111'))

# 23 TWIST 2 partner dies
slide(f'''
<div class="kick red">Plot twist #2 &middot; 2041 &middot; John is 55</div>
<h2>Dr. Raj, John&rsquo;s partner, passes away suddenly.</h2>
<div class="split">
  <div class="sp">{scene(ground(520,420)+'<rect x="150" y="190" width="220" height="220" rx="10" fill="#F4EBDD" stroke="#C9A227" stroke-width="6"/>'+person('raj',260,380,.75,'coat')+'<rect x="240" y="410" width="40" height="0"/><path d="M420,400 L420,330" stroke="#E5B93C" stroke-width="12"/><path d="M420,318 C410,300 430,296 420,282 C432,296 432,312 420,318Z" fill="#F2A33A"/>', 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')}</div>
  <div class="twist2">
    <p class="f"><b>Sarah</b> had drafted a buy-sell agreement. <b>Mehar</b> had funded it with insurance on both partners.</p>
    <p class="f">The corporation received the payout and bought Raj&rsquo;s shares at a fair price. <b>Raj&rsquo;s family got cash within weeks.</b></p>
    <p class="f">Key person coverage carried the clinic while a new dentist was hired.</p>
    <p class="f mid2">No lawsuits. No fire sale. <b class="green">The business survived.</b></p>
  </div>
</div>
''', 'sRaj', hud=H(55, 6400000, '0,2,3,4,5', '111'))

# 24 CHAPTER 6: 65
slide(f'''
<div class="kick">Chapter Six &middot; Christmas 2051 &middot; John is 65</div>
<h2>Three clinics. And John retires, right on time.</h2>
{scene(ground(1300,360)+clinic(230,350,.7,1)+clinic(520,350,.7,2)+clinic(810,350,.7,3)+person('john',1070,350,.8)+person('emma',1150,350,.76), 390)}
<div class="three">
  <div class="f"><b>Sarah</b><span>set up his holding company, an estate freeze and an updated will.</span></div>
  <div class="f"><b>David</b><span>timed tax-free capital dividends and his retirement income.</span></div>
  <div class="f"><b>Mehar</b><span>turned the policy and seg funds into tax-efficient income.</span></div>
</div>
<p class="f mid">&#10003; Open more locations &nbsp; &#10003; Retire by 65</p>
''', 'sRetire', hud=H(65, 11200000, '0,2,3,4,5', '111'))

# 25 SUCCESSION
slide(f'''
<div class="kick">Passing the torch</div>
<h2>Lily takes over the clinics. Max is treated just as fairly.</h2>
{scene(ground(1300,380)+person('lily',420,370,1.0,'coat'.replace('coat',''))+person('john',650,370,.95)+person('max',880,370,1.0)+label(420,410,'Lily, 31 &middot; now Dr. Lily',size=20)+label(880,410,'Max, 29',size=20), 420)}
<div class="succ">
  <p class="f"><b>Lily</b> inherits the business she runs.</p>
  <p class="f"><b>Max</b> receives equal value from the insurance, so nobody has to sell a clinic to be fair.</p>
</div>
''', 'sSucc', hud=H(65, 11200000, '0,1,2,3,4,5,6', '111'))

# 26 CHAPTER 7: 90
slide(chapter('Chapter Seven', 'Christmas 2076 · John is 90', 'The Last Christmas',
    '<rect x="0" y="0" width="1300" height="430" fill="#F7F1E3"/><rect x="60" y="40" width="300" height="220" fill="#1F2A44"/>'
    + ''.join(f'<circle cx="{random.randint(80,340)}" cy="{random.randint(60,240)}" r="3" fill="#fff"/>' for _ in range(18))
    + tree(1100,410,1.2)+person('john',300,410,.9,'old')+person('emma',400,410,.86,'old'.replace('old',''))
    + person('lily',540,410,.9)+person('max',660,410,.9)+person('lily',760,410,.5)+person('max',820,410,.45)+person('lily',880,410,.42)+person('max',940,410,.38)
    + label(300,428,'John, 90',size=18)),
    'sChap', hud=H(90, 21500000, '0,1,2,3,4,5,6', '111'))

# 27 LEGACY
slide(f'''
<div class="kick">The legacy</div>
<h2>When John passed, the tax bill was already planned for.</h2>
<div class="flow">
  <div class="fl f"><span>Policy pays his corporation</span><b>{money(i90["totalDB"])}</b></div><div class="fa f">&#10140;</div>
  <div class="fl f gold"><span>Credited to the CDA</span><b>Tax-free bucket</b></div><div class="fa f">&#10140;</div>
  <div class="fl f green"><span>Paid to his family</span><b>Tax-free</b></div>
</div>
<div class="leg3">
  <div class="f">Seg funds paid his beneficiaries directly, <b>skipping probate</b>.</div>
  <div class="f">His TFSA passed to Emma <b>tax-free</b>.</div>
  <div class="f">The business stayed with Lily. <b>Nothing had to be sold.</b></div>
</div>
<div class="src">Death benefit from the illustration at age 90 (current dividend scale, not guaranteed). The CDA is credited with the death benefit less the policy&rsquo;s adjusted cost basis.</div>
''', 'sLegacy', hud=H(90, 21500000, '0,1,2,3,4,5,6', '111'))

# 28 JAKE
slide(f'''
<h2 class="mt">But remember Jake?</h2>
<p class="big">Same clinic. Same family. Same income. Same net worth at 40.</p>
{scene(ground(1300,420)+person('jake',650,410,1.2)+label(650,450,'Jake',"#5E6670",26), 470)}
<p class="once f">Jake decided to &ldquo;think about it.&rdquo;</p>
''', 'sJake')

# 29 SIDE BY SIDE
cmp = [('Age 46', 'Opened clinic #2', 'Cash stuck in the corporation'),
       ('Age 48: crash', 'Guaranteed floor, policy untouched', 'Lost 25% overnight'),
       ('Debt-free', 'Age 50', 'Age 58'),
       ('Age 55: partner dies', 'Buy-sell funded, business saved', 'No agreement, borrowed to buy out the family'),
       ('Locations', '3', '1'),
       ('Retired', 'At 65', 'At 70')]
ch = ''.join(f'<div class="cR f"><span>{a}</span><b class="cj">{b}</b><b class="ck">{c}</b></div>' for a, b, c in cmp)
slide(f'''
<div class="kick">Two lives, side by side</div>
<div class="cmp"><div class="cR cH"><span></span><b class="cj">John</b><b class="ck">Jake</b></div>{ch}</div>
<div class="src">Illustrative story. John and Jake are fictional.</div>
''', 'sCmp')

# 30 TWO DOCTORS
slide(f'''
<div class="kick">This isn&rsquo;t just a story</div>
<h2>Real numbers: two doctors, one difference</h2>
<div class="docs">
  <div class="dc f"><b>Dr. Brown</b><span>No whole life</span><div class="dv red">$2.7M</div><em>reached his family &middot; 72% lost to tax</em></div>
  <div class="dc f win"><b>Dr. Smith</b><span>Added whole life</span><div class="dv green">$7.8M</div><em>reached his family &middot; 42% to tax</em></div>
</div>
<p class="f mid">Same income. Same savings. <b>Nearly 3&times; more for the family.</b></p>
<div class="src">Levine Financial Group, A Tale of Two Physicians (Dec 2025): corporate assets at death, age 85.</div>
''', 'sDocs')

# 31 THE $100K DECISION
fv60 = sum(100000 * 1.04 ** (60 - y) for y in range(41, 61))
jake90 = fv60 * 1.04 ** 30
jake_fam = jake90 * 0.5
john_fam = i90['totalDB']
slide(f'''
<div class="kick">What the same $100,000 a year became</div>
<h2>At age 90, for each family</h2>
<div class="bars">
  <div class="bc f"><div class="bb" style="height:{jake_fam/john_fam*310:.0f}px"><b>{money(jake_fam)}</b></div><span>Jake&rsquo;s family</span><em>Taxable investments, about half lost to tax at death</em></div>
  <div class="bc f win"><div class="bb" style="height:310px"><b>{money(john_fam)}</b></div><span>John&rsquo;s family</span><em>Death benefit through the CDA, tax-free</em></div>
</div>
<p class="f mid">Same $2 million saved. <b class="green">{money(john_fam-jake_fam)} more</b> for John&rsquo;s family.</p>
<div class="src">Jake: $100K/yr ages 41&ndash;60 in taxable corporate investments at an assumed 4% after-tax growth, held to 90 ({money(jake90)}), about 50% combined tax at death. Illustrative only. John: illustration death benefit at 90.</div>
''', 'sBars')

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
''', 'sDone', hud=H(90, 21500000, '0,1,2,3,4,5,6', '111'))

# 33 CTA
slide(f'''
<div class="kick">Your move</div>
<h2>Let&rsquo;s Write Your Story</h2>
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
<h1 class="ttl">Merry Christmas</h1>
<p class="big">Thank you. Scan to book your one-on-one and see if you qualify.</p>
<div class="qr"><img src="{QR}" alt="QR code"><span>Scan me</span></div>
{scene(ground(1300,200)+tree(170,200,.6)+tree(1130,200,.6)+gift(300,200,.6)+gift(1000,200,.6,'#2F6E4C'), 230)}
''', 'sThanks')

# ------------------------------------------------------------------ page
flakes = ''.join(f'<i style="left:{random.randint(0,100)}%;--d:{random.uniform(0,14):.1f}s;--t:{random.uniform(10,18):.1f}s;--s:{random.uniform(.5,1.2):.2f}"></i>' for _ in range(34))
orn_hud = ''.join(f'<i title="{n}"></i>' for n in NEEDS)

CSS = open(os.path.join(HERE, 'style.css')).read()
JS = open(os.path.join(HERE, 'engine.js')).read()
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Gift That Keeps Giving: John&rsquo;s Story</title>
<style>{CSS}</style></head>
<body>
<div id="stage">
  <div class="frame"></div>
  <div class="snow" aria-hidden="true">{flakes}</div>
  <div class="brand">TEAM <b>ALL IN</b></div>
  <div class="deck">{"".join(SLIDES)}</div>
  <div id="hud">
    <div class="hTime"><span>Age</span><div class="hTrack"><i id="hDot"></i></div><b id="hAge">40</b></div>
    <div class="hNw"><span>Net worth</span><b id="hNw">$0</b></div>
    <div class="hCda"><div class="hB"><i id="hBf"></i></div><div><span>Future CDA credit</span><b id="hCda">$0</b></div></div>
    <div class="hNeeds"><span>7 needs</span><div id="hOrn">{orn_hud}</div></div>
    <div class="hRules"><span>3 rules</span><div id="hRu"><em>Compound</em><em>Risk</em><em>Tax</em></div></div>
  </div>
  <div class="foot">Illustrative story: John and Jake are fictional; net worth figures are illustrative. Policy values from a real Equitable illustration (current dividend scale, not guaranteed). We do not offer tax or legal advice; please consult a tax and/or legal professional.</div>
  <div class="prog"><i id="prog"></i></div>
</div>
<script>{JS}</script>
</body></html>'''
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)
print('slides', len(SLIDES), 'KB', len(html.encode()) // 1024)
