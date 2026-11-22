import math
f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:60]; s=s.replace(a,b,1)
R("<p class=\"lft f mid\">So in January, he made an appointment.</p>","<p class=\"lft f mid\">So that same week, between Christmas and New Year&rsquo;s, <b>he called Mehar.</b></p>")
R("slide(chapter('Chapter Two', 'January 2027 · John is 40', 'The Meeting',","slide(chapter('Chapter Two', 'December 28, 2026 · John is 40', 'The Meeting',")

# ---------- 7 needs full-screen web
a=s.index("# 9 7 NEEDS CHECK-UP"); b=s.index("# 10 3 HIDDEN PROBLEMS")
desc=['Corporate savings taxed every year','His family would face a huge tax bill','The clinic stops if John can&rsquo;t work','No funded plan if a partner dies','$1.5M of debt with no backstop','No cash when opportunity knocks','No fair split between Lily and Max']
cx,cy,rx,ry=720,330,520,220
P=[(cx+rx*math.cos(math.radians(-90+k*360/7)),cy+ry*math.sin(math.radians(-90+k*360/7))) for k in range(7)]
web=''.join(f'<line class="nwW" x1="{P[i][0]:.0f}" y1="{P[i][1]:.0f}" x2="{P[(i+j)%7][0]:.0f}" y2="{P[(i+j)%7][1]:.0f}"/>' for i in range(7) for j in (1,2))
NEEDS=['Delayed Taxes', 'Wealth Transfer', 'Key Person', 'Buy &amp; Sell', 'Debt', 'Liquidity', 'Estate Equalization']
nodes=''
for k,(x,y) in enumerate(P):
    right = x>cx+120; left = x<cx-120
    anc='start' if right else 'end' if left else 'middle'
    lx = x+58 if right else x-58 if left else x
    ly = (y-74 if y<cy else y+80) if (not right and not left) else y-6
    nodes+=(f'<g class="f nwN"><line class="nwB" x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/>'
            f'<g transform="translate({x:.0f},{y:.0f})"><circle r="46" class="nwG"/><rect x="-9" y="-48" width="18" height="12" rx="3" fill="#B0B7BF"/><circle r="34" class="nwO"/><path d="M-12,-12 L12,12 M12,-12 L-12,12" class="nwX"/></g>'
            f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anc}" class="nwT">{NEEDS[k]}</text>'
            f'<text x="{lx:.0f}" y="{ly+26:.0f}" text-anchor="{anc}" class="nwD">{desc[k]}</text></g>')
new=('# 9 7 NEEDS CHECK-UP (full-screen web)\nslide(\'\'\'\n<div class="kick">The check-up</div>\n<h2 class="nwH">The 7 key needs of John&rsquo;s corporation</h2>\n'
 f'<svg class="nwSvg" viewBox="0 0 1440 640" width="1440" height="640" aria-hidden="true"><g class="nwWeb">{web}</g>{nodes}'
 f'<g class="nwCore"><circle cx="{cx}" cy="{cy}" r="96" class="nwCg"/><circle cx="{cx}" cy="{cy}" r="78" class="nwC"/>'
 f'<text x="{cx}" y="{cy-6}" class="nwCt">JOHN&rsquo;S</text><text x="{cx}" y="{cy+22}" class="nwCt">CORPORATION</text></g>'
 f'<g class="f nwEnd"><rect x="{cx-170}" y="{cy+112}" width="340" height="52" rx="26" class="nwBadge"/><text x="{cx}" y="{cy+146}" class="nwBt">0 of 7 covered</text></g></svg>\n'
 "\'\'\', 'sNeeds')\n\n")
s=s[:a]+new+s[b:]

# ---------- buckets + shock
a=s.index("# 10 3 HIDDEN PROBLEMS")
coins=''.join(f'<circle class="leak" style="animation-delay:{k*.5:.1f}s" cx="{-40+k*20}" cy="20" r="11" fill="#E5B93C"/>' for k in range(5))
buck=('# 9b TWO BUCKETS\nslide(\'\'\'\n<div class="kick">What Mehar showed him</div>\n'
 '<h2>Every dollar in John&rsquo;s corporation sits in one of <span class="gold">two buckets.</span></h2>\n<div class="bkRow">\n'
 f'  <div class="bkC f"><svg viewBox="-160 -260 320 330" width="300" height="300"><path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(179,32,42,.18)" stroke="#E0303E" stroke-width="7" stroke-linejoin="round"/><text x="0" y="-92" text-anchor="middle" style="font:900 68px Georgia;fill:#FF7D78">%</text><g class="drip">{coins}</g></svg>'
 '<b class="red">Taxable bucket</b><span>Salary, dividends, investment income: <strong>taxed on the way out</strong>, up to about half.</span></div>\n'
 '  <div class="bkVs f">vs</div>\n'
 '  <div class="bkC win f"><svg viewBox="-160 -260 320 330" width="300" height="300"><path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(229,185,60,.22)" stroke="#F2CC5A" stroke-width="7" stroke-linejoin="round"/><rect class="bkLvl" x="-100" y="-60" width="200" height="60" fill="#E5B93C" opacity=".7"/><text x="0" y="-110" text-anchor="middle" style="font:900 60px Georgia;fill:#FFE08A">CDA</text></svg>'
 '<b class="gold">Tax-free bucket</b><span>The Capital Dividend Account: <strong>every dollar comes out tax-free.</strong></span></div>\n</div>\n'
 "\'\'\', 'sBuckets', hud=H(40, 1509000))\n\n"
 'BUBBLE=\'<g class="f"><path d="M150,92 L330,92 Q350,92 350,112 L350,160 Q350,180 330,180 L240,180 L210,214 L214,180 L150,180 Q130,180 130,160 L130,112 Q130,92 150,92Z" fill="#FBF3E2" stroke="#E5B93C" stroke-width="3"/><text x="240" y="128" text-anchor="middle" style="font:700 italic 20px Georgia;fill:#6B1218">A tax-free bucket?</text><text x="240" y="156" text-anchor="middle" style="font:700 italic 20px Georgia;fill:#6B1218">Nobody ever told me!</text></g>\'\n'
 "SHOCK=scene(ground(620,420)+person('john',200,410,1.1,mood='shock')+person('mehar',440,410,1.05)+BUBBLE, 470).replace('viewBox=\"0 0 1300 470\" width=\"1300\"','viewBox=\"0 0 620 470\" width=\"620\"')\n"
 "slide(f\'\'\'\n<div class=\"split shockS\">\n  <div class=\"sp\">{SHOCK}</div>\n  <div class=\"sp2\">\n"
 '    <div class="kick" style="text-align:left">The moment</div>\n    <h2 class="lft">John had never heard of it.</h2>\n'
 '    <p class="lft big f">Ten years in business. An accountant. A bank. <b>Nobody had ever shown him the tax-free bucket.</b></p>\n'
 '    <p class="lft big f"><b class="gold">&ldquo;How do I fill it?&rdquo;</b> he asked. <b>&ldquo;And how soon can we start?&rdquo;</b></p>\n  </div>\n</div>\n'
 "\'\'\', 'sShock', hud=H(40, 1509000))\n\n")
s=s[:a]+buck+s[a:]

# ---------- chapter 3: starts in December
R("slide(chapter('Chapter Three', 'Spring 2027 · John is 41', 'The Plan',","slide(chapter('Chapter Three', 'December 30, 2026 · the same month', 'He Starts Now',")
R("ground(1300,400)+gift(650,390,1.6,txt='THE PLAN')+person('john',400,400,.95)+person('mehar',900,400,.95)+tree(1130,400,.8)),\n    'sChap', hud=H(41, 1560000, '0,4', '100'))",
  "ground(1300,400)+gift(650,390,1.6,txt='THE PLAN')+person('john',400,400,.95,arm='up')+person('mehar',900,400,.95)+tree(1130,400,.8)\n    +'<text x=\"650\" y=\"60\" text-anchor=\"middle\" class=\"capt\">&ldquo;Why wait until next year? Time is the one thing I can&rsquo;t buy back.&rdquo;</text>'),\n    'sChap', hud=H(40, 1509000, '0,4', '100'))")

# ---------- structure + all-in-one
a=s.index("# 13 THE POLICY")
fan=[('Tax-free growth','Cash value compounds sheltered'),('Borrow anytime','Collateral for bank loans'),('Debt protection','Pays off loans at death'),('Key person','Protects the clinic'),('Buy-sell funding','Partner buyout ready'),('Tax-free estate','Paid out through the CDA')]
fx=[170,390,610,830,1050,1270]
fh=''.join(f'<g class="f aoB"><path class="aoL" d="M720,330 C720,380 {x},380 {x},430"/><rect x="{x-102}" y="430" width="204" height="92" rx="14" class="aoBox"/><text x="{x}" y="468" class="aoBt">{a1}</text><text x="{x}" y="494" class="aoBd">{b1}</text></g>' for x,(a1,b1) in zip(fx,fan))
struct=('# 12b HOW IT\'S STRUCTURED\nslide(\'\'\'\n<div class="kick">How it&rsquo;s structured</div>\n<h2>Who owns it, who pays, and who gets paid</h2>\n<div class="stG">\n'
 '  <div class="stC f"><i>&#127970;</i><span>Owner &amp; payer</span><b>John&rsquo;s corporation</b><em>Pays with 88&cent; corporate dollars, not 50&cent; personal ones</em></div>\n'
 '  <div class="stC f"><i>&#128100;</i><span>Life insured</span><b>John</b><em>The policy is on his life</em></div>\n'
 '  <div class="stC f gold"><i>&#128176;</i><span>Inside the policy</span><b>Cash value grows</b><em>Tax-sheltered: guaranteed values plus dividends. He can borrow against it.</em></div>\n'
 '  <div class="stC f"><i>&#127963;</i><span>Beneficiary</span><b>John&rsquo;s corporation</b><em>Receives the tax-free death benefit</em></div>\n'
 '  <div class="stC f gold"><i>&#129699;</i><span>The CDA</span><b>Gets credited</b><em>Death benefit minus the policy&rsquo;s cost base goes into the tax-free bucket</em></div>\n'
 '  <div class="stC f green"><i>&#128106;</i><span>His family</span><b>Paid tax-free</b><em>As a capital dividend, out of the CDA</em></div>\n</div>\n'
 '<p class="f mid"><b>David</b> reviewed the tax. <b>Sarah</b> updated the corporate records and his will. <b>Mehar</b> designed the policy.</p>\n'
 "\'\'\', 'sStruct', hud=H(40, 1509000, '0,4', '100'))\n\n"
 '# 12c ALL IN ONE\nslide(\'\'\'\n<div class="kick">The all-in-one strategy</div>\n<h2 class="nwH">One policy. Six jobs.</h2>\n'
 '<svg class="aoSvg" viewBox="0 0 1440 560" width="1440" height="560" aria-hidden="true">\n'
 ' <g class="f"><rect x="540" y="10" width="360" height="64" rx="14" class="aoTop"/><text x="720" y="50" class="aoTt">John&rsquo;s Dental Corporation</text></g>\n'
 ' <g class="f"><path class="aoL" d="M360,42 L540,42"/><rect x="180" y="16" width="180" height="52" rx="12" class="aoSide"/><text x="270" y="49" class="aoSt">Revenue in</text>'
 '<path class="aoL red" d="M900,42 L1080,42"/><rect x="1080" y="16" width="180" height="52" rx="12" class="aoSide r"/><text x="1170" y="49" class="aoSt">Expenses out</text></g>\n'
 ' <g class="f"><path class="aoL gold" d="M720,74 L720,200"/><rect x="490" y="112" width="460" height="42" rx="21" class="aoPill"/><text x="720" y="139" class="aoPt">Retained earnings &#8594; $100,000 a year</text></g>\n'
 ' <g class="f"><rect x="520" y="200" width="400" height="130" rx="20" class="aoPol"/><text x="720" y="250" class="aoPolT">Permanent Policy</text><text x="720" y="280" class="aoPolS">(Whole Life)</text><text x="720" y="308" class="aoPolS">Cash value + tax-free death benefit</text></g>\n'
 f' {fh}\n</svg>\n'
 "\'\'\', 'sAio', hud=H(40, 1509000, '0,4', '100'))\n\n")
s=s[:a]+struct+s[a:]
open(f,'w').write(s)
print('ok')
