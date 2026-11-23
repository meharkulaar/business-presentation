import re
# ---- new characters
f='props2.py';p=open(f).read()
a="        'raj':   dict(hair=('short', '#1E1A18'), top='#FAFAFA', bottom='#2E3440', acc=['coat']),"
assert a in p
p=p.replace(a, a+"""
        'tax':   dict(hair=('short', '#2A2A2A'), top='#3A3F48', bottom='#2A2D33', acc=['tie', 'glasses']),
        'dau':   dict(hair=('long', '#4A2E1E'), top='#5E7FA3', bottom='#2E3440'),
        'rc':    dict(hair=('short', '#3A2A20'), top='#9E1B26', bottom='#3B2228'),
        'rr':    dict(hair=('short', '#2A2A2A'), top='#7A6A5A', bottom='#33302C'),
        'rt':    dict(hair=('short', '#1E1A18'), top='#4A3A5A', bottom='#2A2530'),""")
open(f,'w').write(p)

f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:80]; s=s.replace(a,b,1)
R("'raj': '#B57B52', 'jake': '#F2C9A5'}","'raj': '#B57B52', 'jake': '#F2C9A5', 'tax': '#E8BE98', 'dau': '#F0C8A4', 'rc': '#D9A57E', 'rr': '#E8BE98', 'rt': '#C48A5C'}")

# ---- insurance: $2.5M total
R("He agreed to raise it to <b>$1.5M life and $250K critical illness</b>.",
  "He agreed to <b>$2.5M of personal life insurance, permanent plus term, and $250K of critical illness</b>.")
R("'Increases his personal protection to $1.5M life and $250K critical illness'",
  "'Increases his personal protection to $2.5M of life insurance (permanent + term) and $250K critical illness'")

# ---- scenes
R("# 2 HOOK", '''# ---- v22 illustrations
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
HOOK_SCENE = scene(ground(620,420) + peace_tower(330,410,.78)
  + person('tax',300,410,.95,arm='hold') + money_bag(352,300,.85) + tax_bill(214,286,.9)
  + person('dau',530,410,.9,mood='sad') + '<circle cx="574" cy="330" r="10" fill="#E5B93C" stroke="#8A6510" stroke-width="2"/>'
  + label(300,448,'The taxman',size=17) + label(530,448,'Their daughter',size=17), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 620 470" width="560"')

def tug():
    g = []
    g.append('<path d="M330,262 C560,272 760,272 1000,262" stroke="#C9A47A" stroke-width="9" fill="none" stroke-linecap="round"/>')
    g.append('<path d="M330,262 C560,272 760,272 1000,262" stroke="#8A6A3A" stroke-width="2" fill="none" stroke-dasharray="6 8"/>')
    g.append('<rect x="745" y="250" width="14" height="34" rx="3" fill="#B3202A"/><path d="M650,300 L650,240" stroke="#FFE7A6" stroke-width="3" stroke-dasharray="6 6"/>')
    g.append('<g transform="rotate(-10 300 400)">' + person('john',300,400,1.0,arm='hold',mood='shock') + '</g>')
    for k, (kind, nm) in enumerate([('rc','Compound'), ('rr','Risk'), ('rt','Tax')]):
        x = 860 + k*125
        g.append(f'<g transform="rotate(9 {x} 400)">' + person(kind, x, 400, .95, arm=None) + f'<rect x="{x-48}" y="{290}" width="96" height="26" rx="6" fill="#FBF6EA" stroke="#B3202A" stroke-width="2"/><text x="{x}" y="{308}" text-anchor="middle" style="font:900 15px Georgia;fill:#B3202A">{nm}</text></g>')
    g.append('<path d="M640,350 L560,350" stroke="#FF6F6B" stroke-width="5" marker-end="url(#tgArr)" opacity=".0"/>')
    g.append(label(300,442,'John',size=20))
    return scene(ground(1300,400) + ''.join(g), 450)
TUG_SCENE = tug()

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

# 2 HOOK''')

# hook layout with the scene
a=s.index('<div class="hookRow f">'); b=s.index('<p class="f mid">Both parents died')
s=s[:a]+'''<div class="split hookS">
  <div class="sp f">{HOOK_SCENE}</div>
  <div class="hookCol">
    <div class="hookCard f"><span>Their parents&rsquo; RRSPs</span><b>&asymp; $715,000</b></div>
    <div class="hookCard tax f"><span>Tax bill</span><b>$660,000+</b></div>
    <div class="hookCard left f"><span>What was left</span><b>Almost nothing</b></div>
  </div>
</div>
'''+s[b:]

# rules slide: tug of war above the cards
R('<div class="rules3">', '<div class="tugW f">{TUG_SCENE}</div>\n<div class="rules3">')
# hidden problems: safe on card 2
R('<div class="pb f"><div class="pbN">2</div><b>Trapped money</b>', '<div class="pb f"><div class="pbN">2</div>{SAFE}<b>Trapped money</b>')
# debt-free scene
R('<div class="debt">', '<div class="debtS f">{DEBT_SCENE}</div>\n<div class="debt">')
# Rogers court visual
R('<div class="rog">\n  <div class="rogBig f">', '<div class="rog">\n  <div class="f">{COURT}</div>\n  <div class="rogBig f">')
open(f,'w').write(s); print('ok')
