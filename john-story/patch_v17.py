f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:80]; s=s.replace(a,b,1)

# ---- 1) 7 key needs: Santa's handwritten checklist
a=s.index("# 9 7 NEEDS CHECK-UP"); b=s.index("# 9a CORPORATE DOLLAR")
s=s[:a]+'''# 9 7 NEEDS: SANTA'S CHECKLIST
NEED_NOTES = [('Delayed taxes', 'corporate savings taxed every year'), ('Wealth transfer', 'family faces a huge tax bill'),
              ('Key person', 'clinic stops if John can&rsquo;t work'), ('Buy &amp; sell', 'no funded plan if a partner dies'),
              ('Debt', '$1.5M owing, no backstop'), ('Liquidity', 'no cash when opportunity knocks'),
              ('Estate equalization', 'no fair split for Lily &amp; Max')]
def _need(k, t, d):
    box = '<svg class="hbx" viewBox="0 0 40 40" width="34" height="34"><path d="M5,6 C14,4 26,5 35,5 C36,15 35,26 36,35 C26,36 14,35 5,36 C4,26 5,15 5,6Z" fill="none" stroke="#3A2A1A" stroke-width="2.6" stroke-linecap="round"/><path class="hx" d="M9,10 L31,31 M31,9 L10,31" fill="none" stroke="#C0202E" stroke-width="4" stroke-linecap="round"/></svg>'
    return f'<li class="f">{box}<span class="hn">{t}</span><span class="hd">&mdash; {d}</span></li>'
slide(\'\'\'
<div class="kick">The check-up</div>
<div class="santa paper">
  <div class="snH"><span class="snHat">&#127877;</span>Santa&rsquo;s Checklist<small>John&rsquo;s corporation &middot; the 7 key needs</small></div>
  <ul class="snL">\'\'\' + ''.join(_need(k, t, d) for k, (t, d) in enumerate(NEED_NOTES)) + \'\'\'</ul>
  <div class="snT f">0 of 7 covered!</div>
</div>
\'\'\', 'sNeeds')

'''+s[b:]

# ---- 2) THE PLAN gift: outlined so it reads from afar
R("""def gift(x, y, s=1.0, col='#9E1B26', txt=''):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-60" y="-100" width="120" height="100" fill="{col}"/>'
            '<rect x="-68" y="-118" width="136" height="24" fill="#B32533"/>'
            '<rect x="-9" y="-118" width="18" height="118" fill="#E5B93C"/>'
            '<path d="M0,-118 C-40,-160 -60,-120 0,-118 C60,-120 40,-160 0,-118Z" fill="#E5B93C"/>'
            f'<text x="0" y="-40" text-anchor="middle" style="fill:#fff;font:700 14px Georgia,serif">{txt}</text></g>')""",
"""def gift(x, y, s=1.0, col='#9E1B26', txt=''):
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
            '<path d="M0,-118 C-40,-160 -60,-120 0,-118 C60,-120 40,-160 0,-118Z" fill="#E5B93C"/></g>')""")

# ---- 3) interactive growth chart
R("""<svg class="chart" viewBox="0 0 1260 430" width="1260" height="430">{grid}{ticks}""",
  """<svg class="chart hov" viewBox="0 0 1260 430" width="1260" height="430" data-x0="90" data-x1="1100">{grid}{ticks}""")
R("""<text x="1108" y="{py(i90["totalCV"])+5:.0f}" class="lg green">Cash value</text>{marks}</svg>""",
  """<text x="1108" y="{py(i90["totalCV"])+5:.0f}" class="lg green">Cash value</text>{marks}{HOVER}</svg>
<p class="hint">Hover over the chart to see any year</p>""")
R("# 14 GROWTH CHART (real data)", '''# 14 GROWTH CHART (real data)
def _hover():
    pts = ''.join(f'<i data-a="{a}" data-x="{90 + (a - 41) * (1010 / 49):.1f}" data-ycv="{390 - ILL[a]["totalCV"] / 15e6 * 350:.1f}" data-ydb="{390 - ILL[a]["totalDB"] / 15e6 * 350:.1f}" data-cv="{money(ILL[a]["totalCV"])}" data-db="{money(ILL[a]["totalDB"])}" data-pr="{money(100000 * min(a - 40, 20))}"></i>' for a in range(41, 91))
    return ('<g class="hvG"><line class="hvL" x1="0" x2="0" y1="40" y2="390"/><circle class="hvC db" r="7"/><circle class="hvC cv" r="7"/>'
            '<g class="hvT"><rect width="230" height="104" rx="10"/><text class="t0" x="14" y="26"></text><text class="t1" x="14" y="50"></text><text class="t2" x="14" y="72"></text><text class="t3" x="14" y="94"></text></g></g>'
            f'<rect class="hvHit" x="90" y="30" width="1010" height="370"/><foreignObject width="0" height="0"><div class="hvD">{pts}</div></foreignObject>')
HOVER = _hover()''')

# ---- 4) RIP Raj: text on paper
R('''  <div class="twist2">
    <p class="f">A wife and two kids''', '''  <div class="twist2 paper rajP">
    <p class="f">A wife and two kids''')

# ---- 5) passing the torch
R("""{scene(ground(1300,380)+person('lily',420,370,1.0,'coat'.replace('coat',''))+person('john',650,370,.95)+person('max',880,370,1.0)+label(420,410,'Lily, 31 &middot; now Dr. Lily',size=20)+label(880,410,'Max, 29',size=20), 420)}""",
"""{scene(ground(1300,380)+person('john',420,370,1.12,arm='hold')+person('lily',690,370,1.0)+person('max',960,370,1.0)
   +'<g class="torch"><ellipse cx="560" cy="150" rx="58" ry="58" fill="url(#gTorch)"/><path d="M478,252 L555,172" stroke="#8A5A2A" stroke-width="11" stroke-linecap="round"/><path d="M546,180 L566,160 L578,172 L558,192Z" fill="#E5B93C"/>'
   +'<path class="tFl" d="M572,166 C552,146 556,120 574,98 C576,118 592,120 590,140 C600,132 602,150 594,160 C588,170 578,172 572,166Z" fill="#FFB547"/><path class="tFl" d="M574,160 C566,148 570,134 578,124 C580,136 588,140 584,152 C582,158 578,162 574,160Z" fill="#FFF0B0"/></g>'
   +'<defs><radialGradient id="gTorch"><stop offset="0" stop-color="rgba(255,200,90,.7)"/><stop offset="1" stop-color="rgba(255,200,90,0)"/></radialGradient></defs>'
   +'<path d="M600,250 C620,228 640,236 646,252" stroke="#C62D3A" stroke-width="15" fill="none" stroke-linecap="round"/><circle cx="604" cy="250" r="9.5" fill="#F1C9A0"/>'
   +label(420,412,'John, 65',size=22)+label(690,412,'Lily, 31 &middot; now Dr. Lily',size=20)+label(960,412,'Max, 29',size=20), 420)}""")

# ---- 6) John & Raj: remove the handshake arc
R("""  + '<path d="M344,300 C356,292 374,292 386,300" stroke="#F1C9A0" stroke-width="12" fill="none" stroke-linecap="round"/>'\n""", "")

# ---- 7) IFA: diagram inspired by the uploaded chart
a=s.index('<div class="ifaW">'); b=s.index("<div class=\"src\">IFA structures")
s=s[:a]+'''<div class="ifD">
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
'''+s[b:]

# ---- 8) clock overlay markup replaces the snow globe
R('''<div id="tp" aria-hidden="true"><div class="tpG"><div class="tpSnow"></div><span>Years pass&hellip;</span><b id="tpY">2026</b><em id="tpA">John is 40</em></div></div>''',
  '''<div id="tp" aria-hidden="true"><div class="tpC">
    <svg viewBox="-110 -110 220 220" width="300" height="300" class="clk"><circle r="102" class="cRim"/><circle r="92" class="cFace"/>{CLK_TICKS}<line x1="0" y1="8" x2="0" y2="-48" class="cH hr"/><line x1="0" y1="12" x2="0" y2="-76" class="cH mn"/><circle r="6" class="cPin"/></svg>
    <span class="tpF">Fast-forward &#9654;&#9654;</span><b id="tpY">2026</b><em id="tpA">John is 40</em></div></div>''')

R("orn_hud = ''.join(", "CLK_TICKS = ''.join(f'<line x1=\"0\" y1=\"-84\" x2=\"0\" y2=\"{-74 if k % 3 else -66}\" class=\"cTk\" transform=\"rotate({k*30})\"/>' for k in range(12))\norn_hud = ''.join(")
open(f,'w').write(s); print('ok')
