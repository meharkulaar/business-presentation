f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:70]; s=s.replace(a,b,1)

# 1) 7 needs: smaller centre label so it sits inside the circle
R('<text x="720" y="344" class="nwCt">JOHN&rsquo;S</text><text x="720" y="372" class="nwCt">CORPORATION</text>',
  '<text x="720" y="343" class="nwCt">JOHN&rsquo;S</text><text x="720" y="367" class="nwCt">CORPORATION</text>')

# 2) Two buckets: coins fall INTO the tax-free bucket, which fills and glows
a=s.index('<div class="bkC win f">'); b=s.index('</div>\n</div>\n\'\'\', \'sBuckets\'')
s=s[:a]+'''<div class="bkC win f">'''+"'''+CDA_BUCKET+'''"+'''<b class="gold">Tax-free bucket</b><span>The Capital Dividend Account: <strong>every dollar comes out tax-free.</strong></span>'''+s[b:]
R("# 9b TWO BUCKETS\nslide('''", '''# 9b TWO BUCKETS
_coins = ''.join(f'<g transform="translate({x},0)"><g class="coinF" style="animation-delay:{d}s"><ellipse rx="17" ry="17" fill="#F2CC5A" stroke="#A87A12" stroke-width="3"/><ellipse rx="10" ry="10" fill="none" stroke="#C99A2A" stroke-width="2"/><text y="6" text-anchor="middle" style="font:900 16px Georgia;fill:#8A6510">$</text></g></g>'
                 for x, d in [(-60,0),(30,.45),(-15,.9),(55,1.35),(-45,1.8),(10,2.25),(40,2.7),(-30,3.15)])
CDA_BUCKET = ('<svg viewBox="-160 -380 320 450" width="300" height="420" style="overflow:visible">'
  '<defs><clipPath id="cdaClip"><path d="M-117,-217 L117,-217 L92,-3 L-92,-3Z"/></clipPath>'
  '<linearGradient id="gFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A0"/><stop offset=".35" stop-color="#F2CC5A"/><stop offset="1" stop-color="#B8860B"/></linearGradient></defs>'
  '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(229,185,60,.10)"/>'
  '<g class="bkGlow"><g clip-path="url(#cdaClip)"><g class="bkFill"><rect x="-130" y="-225" width="260" height="230" fill="url(#gFill)"/>'
  '<path class="bkWave" d="M-260,-222 q32,-10 65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 L260,-200 L-260,-200Z" fill="#FFF1BF" opacity=".8"/>'
  + ''.join(f'<circle class="bkSpark" style="animation-delay:{k*.37:.2f}s" cx="{-70+k*20}" cy="-{30+(k*37)%150}" r="3" fill="#FFF8DC"/>' for k in range(8)) +
  '</g></g></g>' + _coins +
  '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="none" stroke="#F2CC5A" stroke-width="7" stroke-linejoin="round"/>'
  '<text x="0" y="-104" text-anchor="middle" class="bkTxt">CDA</text></svg>')

slide(\'\'\'''')

# 3) Shock: bubble higher, clear of John's head
R("BUBBLE='<g class=\"f\">", "BUBBLE='<g class=\"f\" transform=\"translate(-6,-104)\">")
R(""".replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 620 470" width="620"')
slide(f'''
<div class="split shockS">""", """.replace('viewBox="0 0 1300 470" width="1300" height="470"','viewBox="0 -40 620 510" width="620" height="510"')
slide(f'''
<div class="split shockS">""")

# 4) Corporate dollar vs personal dollar (before the two buckets)
def hend(r):
    import math
    return ' '.join(f'{r*math.cos(-math.pi/2+k*2*math.pi/11):.1f},{r*math.sin(-math.pi/2+k*2*math.pi/11):.1f}' for k in range(11))
H11 = hend(120); H11i = hend(104)
R("# 9b TWO BUCKETS", f'''# 9a CORPORATE DOLLAR VS PERSONAL DOLLAR
def LOON(tax, cls):
    d = tax * 6.283 * 120
    return (f'<svg viewBox="-140 -140 280 280" width="250" height="250" class="lnS {{cls}}"><defs><clipPath id="lc{{cls}}"><polygon points="{H11}"/></clipPath></defs>'
            f'<polygon points="{H11}" fill="url(#gLoon)" stroke="#8A6510" stroke-width="5"/><polygon points="{H11i}" fill="none" stroke="rgba(120,80,10,.55)" stroke-width="3"/>'
            f'<text y="22" text-anchor="middle" style="font:900 64px Georgia;fill:#7A5A10">$1</text>'
            f'<g clip-path="url(#lc{{cls}})"><circle r="120" fill="none" class="tW" stroke-width="240" style="--d:{{d:.0f}}px" transform="rotate(-90)"/></g></svg>')
slide(f\'\'\'
<div class="kick">First, Mehar explained one simple idea</div>
<h2>Which dollar pays: <span class="red">personal</span> or <span class="gold">corporate</span>?</h2>
<svg width="0" height="0" style="position:absolute"><defs><radialGradient id="gLoon" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#FFF0B0"/><stop offset=".5" stop-color="#E5B93C"/><stop offset="1" stop-color="#A87A12"/></radialGradient></defs></svg>
<div class="dlR">
  <div class="dlC f"><div class="dlT red">Personal dollar</div>{{LOON(.5,'p')}}<div class="dlV"><b class="red">50&cent;</b><span>left after personal tax (about half)</span></div>
    <p>To pay a <b>$100,000</b> premium personally, John must earn about <b class="red">$200,000</b>.</p></div>
  <div class="dlVs f">vs</div>
  <div class="dlC win f"><div class="dlT gold">Corporate dollar</div>{{LOON(.12,'c')}}<div class="dlV"><b class="green">88&cent;</b><span>left after small business tax</span></div>
    <p>Paid by his corporation, the same premium takes about <b class="green">$113,600</b> of earnings.</p></div>
</div>
<p class="f mid">Same $100,000 premium. <b class="gold">About $86,000 a year less income needed</b>, just by using the right dollar.</p>
<div class="src">Approximate BC rates: small business about 11%, top personal rate about 53.5%. Rounded for illustration. Not tax advice; confirm with your accountant.</div>
\'\'\', 'sDollar', hud=H(40, 1509000))

# 9b TWO BUCKETS''')

# 5) All-in-one: $100K label to the side, plus a return arrow back to the business
R('<g class="f"><path class="aoL gold" d="M720,74 L720,200"/><rect x="490" y="112" width="460" height="42" rx="21" class="aoPill"/><text x="720" y="139" class="aoPt">Retained earnings &#8594; $100,000 a year</text></g>',
  '<defs><marker id="aoArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10Z" fill="#F2CC5A"/></marker></defs>'
  '<g class="f"><path class="aoL gold" d="M720,74 L720,196" marker-end="url(#aoArr)"/><rect x="330" y="112" width="364" height="42" rx="21" class="aoPill"/><text x="512" y="139" class="aoPt">Retained earnings: $100,000 a year</text></g>')
R('</svg>\n\'\'\', \'sAio\'',
  '<g class="f"><path class="aoL gold aoBack" d="M920,262 C1070,262 1060,92 906,62" marker-end="url(#aoArr)"/>'
  '<text x="1068" y="140" class="aoRt">Back to the business</text><text x="1068" y="166" class="aoRd">Borrow against the cash value</text><text x="1068" y="190" class="aoRd">to reinvest, or for personal use</text></g>'
  '</svg>\n\'\'\', \'sAio\'')

# 6) Snapshot of the real illustration (after the policy slide)
R("# 14 GROWTH CHART (real data)", '''# 13b THE REAL ILLUSTRATION
import base64
SNAP = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'source', 'ill-snap.jpg'), 'rb').read()).decode()
slide(f\'\'\'
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
\'\'\', 'sSnap', hud=H(41, 1560000, '0,4', '100'))

# 14 GROWTH CHART (real data)''')

# 7) IFA: steps on the left, chart on the right
a=s.index('<div class="ifa">'); b=s.index("<div class=\"src\">IFA structures")
s=s[:a]+'''<div class="ifaW">
<div class="ifa v">
  <div class="ifC f"><div class="ifN">1</div><b>Pay the premium</b><span>His corporation pays $100K into the policy.</span></div>
  <div class="ifC f"><div class="ifN">2</div><b>Pledge the policy</b><span>The bank lends against the cash value.</span></div>
  <div class="ifC f"><div class="ifN">3</div><b>Reinvest the cash</b><span>The $500K loan funds clinic #2.</span></div>
  <div class="ifC f gold"><div class="ifN">4</div><b>Policy keeps growing</b><span>The death benefit repays the loan one day.</span></div>
</div>
<div class="ifaCh f">{IFA_CHART}<p>Walt Disney and Ray Kroc are widely reported to have used their policies the same way. <b class="gold">One dollar, two jobs.</b></p></div>
</div>
'''+s[b:]
R("# 20 IFA EXPLAINED", '''# 20 IFA EXPLAINED
def _ifa_chart():
    W, Hh, L, T, B = 640, 360, 70, 20, 300
    ages = list(range(46, 91)); mx = 9e6
    X = lambda a: L + (a - 46) / 44 * (W - L - 30)
    Y = lambda v: B - v / mx * (B - T)
    cv = ' '.join(f'{X(a):.0f},{Y(ILL[a]["totalCV"]):.0f}' for a in ages)
    db = ' '.join(f'{X(a):.0f},{Y(min(ILL[a]["totalDB"], mx)):.0f}' for a in ages if ILL[a]["totalDB"] <= mx)
    g = [f'<svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" class="ifaSvg">']
    for v in range(0, 10, 3):
        g.append(f'<line x1="{L}" x2="{W-30}" y1="{Y(v*1e6):.0f}" y2="{Y(v*1e6):.0f}" class="gl"/><text x="{L-10}" y="{Y(v*1e6)+5:.0f}" class="gt" text-anchor="end">${v}M</text>')
    for a in (46, 55, 65, 75, 90):
        g.append(f'<text x="{X(a):.0f}" y="{B+26}" class="gt" text-anchor="middle">{a}</text>')
    g.append(f'<path d="M{X(46):.0f},{Y(0):.0f} L{cv.replace(" "," L")} L{X(90):.0f},{Y(0):.0f}Z" class="ifaArea"/>')
    g.append(f'<polyline points="{cv}" class="ifaCv"/>')
    g.append(f'<line x1="{X(46):.0f}" x2="{X(90):.0f}" y1="{Y(5e5):.0f}" y2="{Y(5e5):.0f}" class="ifaLoan"/>')
    g.append(f'<text x="{X(60):.0f}" y="{Y(5e5)-10:.0f}" class="ifaLt">Bank loan: $500K, interest only</text>')
    g.append(f'<text x="{X(70):.0f}" y="{Y(ILL[70]["totalCV"])-16:.0f}" class="ifaCt" text-anchor="end">Policy cash value keeps growing</text>')
    g.append(f'<circle cx="{X(90):.0f}" cy="{Y(ILL[90]["totalCV"]):.0f}" r="7" class="ifaDot"/><text x="{X(90)-10:.0f}" y="{Y(ILL[90]["totalCV"])+30:.0f}" class="ifaCt" text-anchor="end">{money(ILL[90]["totalCV"])} at 90</text>')
    g.append(f'<text x="{L}" y="{Hh-6}" class="gt">John&rsquo;s age</text></svg>')
    return ''.join(g)
IFA_CHART = _ifa_chart()''')

# 8) "Life can hit" slide before Raj, and a new Raj memorial visual
R("# 23 TWIST 2 partner dies", '''# 22b LIFE CAN HIT
slide(\'\'\'
<div class="lifeHit">
  <svg viewBox="-60 -150 120 230" width="120" height="230" class="candle" aria-hidden="true"><ellipse cx="0" cy="-92" rx="34" ry="44" fill="rgba(255,190,90,.25)" class="cGlow"/><rect x="-22" y="-60" width="44" height="130" rx="6" fill="#F4EBDD"/><rect x="-22" y="-60" width="16" height="130" fill="rgba(0,0,0,.12)"/><path d="M0,-64 L0,-74" stroke="#333" stroke-width="3"/><path class="cFl" d="M0,-72 C-14,-90 -6,-110 0,-128 C6,-110 14,-90 0,-72Z" fill="#FFC85A"/></svg>
  <p class="lhA f">But life can change at any moment.</p>
  <p class="lhB f">Unfortunately, it often does when we least expect it.</p>
</div>
\'\'\', 'sLife', hud=H(55, 6400000, '0,4,5', '111'))

# 23 TWIST 2 partner dies''')
a=s.index('<div class="sp">{scene(ground(520,420)+\'<rect x="150" y="190"'); b=s.index('<div class="twist2">')
s=s[:a]+'<div class="sp">{RAJ_SCENE}</div>\n  '+s[b:]
R("# 22b LIFE CAN HIT", '''RAJ_SCENE = scene(ground(560,420)
  + '<g class="rajGhost">' + person('raj',170,400,.82,'coat') + '</g>'
  + '<ellipse class="halo" cx="170" cy="182" rx="36" ry="10"/>'
  + '<g transform="translate(380,410)"><path d="M-95,0 L-95,-170 C-95,-235 95,-235 95,-170 L95,0Z" fill="#8E949C"/><path d="M-95,0 L-95,-170 C-95,-235 95,-235 95,-170 L95,0Z" fill="url(#gShade)"/>'
  + '<path d="M-80,0 L-80,-165 C-80,-220 80,-220 80,-165 L80,0" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="3"/>'
  + '<text y="-150" text-anchor="middle" style="font:900 52px Georgia;fill:#3A3F46">RIP</text><text y="-108" text-anchor="middle" style="font:700 22px Georgia;fill:#2E3238">Dr. Raj</text>'
  + '<text y="-80" text-anchor="middle" style="font:italic 15px Georgia;fill:#2E3238">Partner. Father. Friend.</text>'
  + '<circle cx="-70" cy="-6" r="12" fill="#C62D3A"/><circle cx="-52" cy="-10" r="10" fill="#E5B93C"/><circle cx="-60" cy="-22" r="9" fill="#F4EBDD"/><circle cx="66" cy="-8" r="12" fill="#C62D3A"/><circle cx="50" cy="-16" r="9" fill="#F4EBDD"/></g>', 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 560 470" width="560"')

# 22b LIFE CAN HIT''')
R("<h2>Dr. Raj, John&rsquo;s partner, passes away suddenly.</h2>", "<h2>Dr. Raj, John&rsquo;s partner, passed away suddenly.</h2>")

# 9) Last Christmas: inside a home, with walls and a roofline
a=s.index("slide(chapter('Chapter Seven'"); b=s.index("# 26b CHRISTMAS MORNING REVEAL")
s=s[:a]+'''HOME = ('<defs><pattern id="wp" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#5A1A22"/><rect width="20" height="40" fill="#621E27"/><circle cx="10" cy="20" r="2.4" fill="rgba(229,185,60,.35)"/></pattern></defs>'
  '<path d="M30,430 L30,110 L650,14 L1270,110 L1270,430Z" fill="url(#wp)"/>'
  '<rect x="30" y="352" width="1240" height="78" fill="#6B4226"/>' + ''.join(f'<line x1="{x}" y1="352" x2="{x-30}" y2="430" stroke="rgba(0,0,0,.25)" stroke-width="2"/>' for x in range(110, 1270, 90)) +
  '<rect x="30" y="344" width="1240" height="10" fill="#E8D6B0"/><ellipse cx="640" cy="404" rx="420" ry="22" fill="#8E1B26" opacity=".8"/>'
  '<g><rect x="80" y="150" width="230" height="160" fill="#16213A"/>' + ''.join(f'<circle cx="{random.randint(92,298)}" cy="{random.randint(160,300)}" r="2.6" fill="#fff"/>' for _ in range(16)) +
  '<path d="M80,280 Q195,262 310,282 L310,310 L80,310Z" fill="#E8EEF6"/><rect x="190" y="150" width="8" height="160" fill="#E8D6B0"/><rect x="80" y="226" width="230" height="8" fill="#E8D6B0"/><rect x="72" y="142" width="246" height="176" fill="none" stroke="#E8D6B0" stroke-width="10"/>'
  '<path d="M64,138 C90,200 70,260 96,320 L64,320Z M326,138 C300,200 320,260 294,320 L326,320Z" fill="#9E1B26"/></g>'
  '<rect x="470" y="140" width="80" height="62" fill="#3A1216" stroke="#C9A227" stroke-width="6"/><rect x="600" y="128" width="100" height="78" fill="#3A1216" stroke="#C9A227" stroke-width="6"/><rect x="750" y="140" width="80" height="62" fill="#3A1216" stroke="#C9A227" stroke-width="6"/>'
  '<path d="M610,196 L630,170 L650,186 L668,162 L690,196Z" fill="#7A6A50"/><circle cx="510" cy="168" r="12" fill="#C9A9A0"/><circle cx="790" cy="168" r="12" fill="#C9A9A0"/>'
  '<path d="M30,110 L650,14 L1270,110" fill="none" stroke="#E8D6B0" stroke-width="16" stroke-linejoin="round"/>'
  '<path d="M30,110 L30,430 M1270,110 L1270,430" stroke="#E8D6B0" stroke-width="16"/>'
  '<path d="M0,116 L650,0 L1300,116" fill="none" stroke="#8E1B26" stroke-width="12" stroke-linejoin="round"/>'
  + ''.join(f'<circle cx="{120+k*58}" cy="{111-((120+k*58) if (120+k*58)<650 else 1300-(120+k*58))*0.155+14:.0f}" r="5" fill="{["#FF4D5E","#FFD27A","#7FE0A8","#FFFFFF"][k%4]}" class="hl{k%3}"/>' for k in range(19)))
slide(chapter('Chapter Seven', 'Christmas 2076 · John is 90', 'The Last Christmas',
    HOME + tree(1120,410,1.0)+person('john',300,410,.9,'old')+person('emma',400,410,.86)
    + person('lily',540,410,.9)+person('max',660,410,.9)+person('lily',760,410,.5)+person('max',820,410,.45)+person('lily',880,410,.42)+person('max',940,410,.38)
    + label(300,428,'John, 90',size=18)),
    'sChap sHome', hud=H(90, 21500000, '0,1,2,3,4,5,6', '111'))

'''+s[b:]

# 10) Jake at 90, after the split screen
R("# 30 TWO DOCTORS", '''# 29b JAKE AT 90
JAKE90 = scene(ground(560,420) + tree(450,410,.55,lit=False) + cloud(190,40,.62)
  + ''.join(f'<line class="rain" style="animation-delay:-{k*.13:.2f}s" x1="{140+k*14}" y1="92" x2="{134+k*14}" y2="122" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>' for k in range(8))
  + person('jake',200,410,1.0,'old',mood='sad')
  + '<g transform="translate(330,330)"><rect x="0" y="0" width="70" height="80" fill="#5A4A3A"/><rect x="6" y="-18" width="58" height="20" fill="#EFE6D4" transform="rotate(-6)"/><rect x="8" y="-30" width="58" height="16" fill="#E2D7C2" transform="rotate(4)"/><text x="36" y="-16" text-anchor="middle" style="font:900 12px sans-serif;fill:#B3202A">TAX BILL</text></g>', 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 560 470" width="560"')
slide(f\'\'\'
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
\'\'\', 'sJake90')

# 30 TWO DOCTORS''')

# 11) Two doctors: move after the $100K bars and mark clearly as a real case study
a=s.index("# 30 TWO DOCTORS"); b=s.index("# 31 THE $100K DECISION")
docs=s[a:b]; s=s[:a]+s[b:]
docs=docs.replace('<div class="kick">This isn&rsquo;t just a story</div>\n<h2>Real numbers: two doctors, one difference</h2>',
  '<div class="stamp">Real case study</div>\n<div class="kick">Stepping out of the story</div>\n<h2>John and Jake are fictional. <span class="gold">This case is real.</span></h2>\n<p class="big">A published study compared two real physicians with the same income and savings.</p>')
c=s.index("# 32 EVERYTHING ACCOMPLISHED")
s=s[:c]+docs+s[c:]

# 12) Happy Holidays
R('<span class="hatL">M<svg', '<span class="hatL">H<svg')
R('</svg></span>erry Christmas</h1>', '</svg></span>appy Holidays</h1>')
R("<p class=\"big\">Thank you. Scan to book", "<p class=\"big\">Thank you, and happy holidays. Scan to book")

open(f,'w').write(s); print('ok')
