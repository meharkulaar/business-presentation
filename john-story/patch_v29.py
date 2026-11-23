f='build.py';s=open(f).read()
Q3 = "'" * 3
def R(a,b):
    global s; assert a in s,a[:90]; s=s.replace(a,b,1)

# ---------- shared helpers
R("# ---- v22 illustrations", r'''# ---- v29 helpers
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

# ---- v22 illustrations''')

# ---------- hook: illustration fills the left half
R("HOOK_SCENE = scene(", '''HOOK_HALF = half_svg('<rect width="720" height="810" fill="url(#hkSky)"/>' + ''.join(f'<circle cx="{(k*97)%700+10}" cy="{(k*53)%380+20}" r="{1.5 + (k%3)*.6}" fill="#fff" opacity=".55"/>' for k in range(40))
  + peace_tower(250, 690, 1.3) + snow_floor(680)
  + person('tax', 380, 712, 1.5, arm='hold') + money_bag(462, 538, 1.34) + tax_bill(244, 518, 1.42)
  + person('dau', 600, 712, 1.35, mood='sad') + '<circle cx="666" cy="592" r="14" fill="#E5B93C" stroke="#8A6510" stroke-width="3"/>',
  '<linearGradient id="hkSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A0810"/><stop offset="1" stop-color="#4A1520"/></linearGradient>')
HOOK_SCENE = scene(''')
a=s.index('<div class="kick red">A real case &middot; Ontario'); b=s.index(Q3+", 'sHook')")
s=s[:a]+'''{HOOK_HALF}
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
'''+s[b:]
R(Q3+", 'sHook')", Q3+", 'sHook sHalf')")

# ---------- Meet John: family fills the left half
a=s.index("MEET = scene("); b=s.index("\n", s.index("viewBox=\"0 0 560 470\" width=\"560\"')", a))+1
s=s[:a]+'''MEET = half_svg('<rect width="720" height="810" fill="url(#mtSky)"/>' + ''.join(f'<circle cx="{(k*89)%700+10}" cy="{(k*61)%300+20}" r="{1.4 + (k%3)*.6}" fill="#fff" opacity=".5"/>' for k in range(34))
  + house(150, 640, 1.05) + snow_floor(630)
  + person('john', 330, 650, 1.5) + person('emma', 462, 650, 1.4) + person('lily', 566, 650, .92) + person('max', 646, 650, .78)
  + label(330, 690, 'John, 40', size=22) + label(462, 690, 'Emma, 39', size=22) + label(566, 690, 'Lily, 6', size=20) + label(652, 690, 'Max, 4', size=20),
  '<linearGradient id="mtSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14101E"/><stop offset="1" stop-color="#3A1A28"/></linearGradient>')
'''+s[b:]
R('<div class="split meetS">\n  <div class="sp">{MEET}</div>\n  <div class="sp2">\n    <div class="kick" style="text-align:left">Meet John</div>',
  '{MEET}\n<div class="meetR">\n    <div class="kick" style="text-align:left">Meet John</div>')
R('<p class="meetQ f">&ldquo;I built a great practice. I just never had time to build a plan.&rdquo;</p>\n  </div>\n</div>\n<p class="f mid">Sound familiar?</p>',
  '<p class="meetQ f">&ldquo;I built a great practice. I just never had time to build a plan.&rdquo;</p>\n    <p class="f lft meetSF">Sound familiar?</p>\n</div>')
R(Q3+", 'sMeet',", Q3+", 'sMeet sHalf',")

# ---------- tug of war: obviously losing, centre line on the ground
R("    g.append('<rect x=\"745\" y=\"250\" width=\"14\" height=\"34\" rx=\"3\" fill=\"#B3202A\"/><path d=\"M650,300 L650,240\" stroke=\"#FFE7A6\" stroke-width=\"3\" stroke-dasharray=\"6 6\"/>')",
  "    g.append('<path d=\"M650,386 L650,446\" stroke=\"#B3202A\" stroke-width=\"5\" stroke-dasharray=\"10 8\"/><text x=\"650\" y=\"378\" text-anchor=\"middle\" style=\"font:800 13px sans-serif;fill:#7A0F1A;letter-spacing:.12em\">CENTRE</text>'\n             '<rect x=\"812\" y=\"252\" width=\"14\" height=\"36\" rx=\"3\" fill=\"#B3202A\"/><path d=\"M819,252 L819,226 L846,236 L819,246\" fill=\"#FFE7A6\" stroke=\"#B3202A\" stroke-width=\"2\"/>'\n             '<path d=\"M196,404 L276,402 M206,412 L270,410 M214,396 L262,395\" stroke=\"#B9C2CC\" stroke-width=\"4\" stroke-linecap=\"round\"/>' + ''.join(f'<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\" fill=\"#FFFFFF\" opacity=\".9\"/>' for x, y, r in ((268,392,7),(282,384,5),(256,386,4),(292,394,4)))\n             + '<path d=\"M420,200 L580,200\" stroke=\"#FF6F6B\" stroke-width=\"6\" stroke-linecap=\"round\"/><path d=\"M580,186 L604,200 L580,214Z\" fill=\"#FF6F6B\"/><text x=\"500\" y=\"186\" text-anchor=\"middle\" style=\"font:900 22px Georgia;fill:#FF8A86\">Losing ground</text>')")
R("    g.append('<g transform=\"rotate(-10 300 400)\">' + person('john',300,400,1.0,arm='hold',mood='shock') + '</g>')",
  "    g.append('<g transform=\"translate(24,0) rotate(12 300 400)\">' + person('john',300,400,1.0,arm='hold',mood='shock') + '</g>')")
R("        g.append(f'<g transform=\"rotate(9 {x} 400)\">' + person(kind, x, 400, .95, arm=None)",
  "        g.append(f'<g transform=\"rotate(13 {x} 400)\">' + person(kind, x, 400, .95, arm=None)")

# ---------- ten years earlier: split office, 2016 vs 2026, speech bubbles
a=s.index("FLASH = scene("); b=s.index("# 8b MEHAR'S PROCESS")
s=s[:a]+r'''def _office_half(x0, sep):
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
slide(f''' + Q3 + r'''
<div class="kick">But this wasn&rsquo;t their first meeting</div>
<h2>Ten years earlier, Mehar had shown John these same strategies.</h2>
{FLASH}
''' + Q3 + r''', 'sFlash')

'''+s[b:]

# ---------- fundamentals slide: flexible plan, remove "All of it"
R("He agreed to <b>$2.5M of personal life insurance, permanent plus term, and $250K of critical illness</b>.</li>",
  "He agreed to <b>$2.5M of personal life insurance, permanent plus term, and $250K of critical illness</b>. He also started a <b>flexible savings and investment plan</b> (more on that later).</li>")
R("    <li><b>All of it:</b> reviewed with Sarah and David: wills, powers of attorney and tax.</li>\n", "")

# ---------- bigger buckets and loonies
R("CDA_BUCKET = cda_bucket('A', 240, 336)", "CDA_BUCKET = cda_bucket('A', 300, 420)")
s=s.replace('viewBox="-160 -260 320 330" width="232" height="240"','viewBox="-160 -260 320 330" width="300" height="310"')
R('return (f\'<svg viewBox="-140 -140 280 280" width="250" height="250" class="lnS {cls}">', 'return (f\'<svg viewBox="-140 -140 280 280" width="300" height="300" class="lnS {cls}">')

# ---------- shock slide: bigger scene + Mehar's reply bubble
a=s.index("BUBBLE='<g transform="); b=s.index("slide(f'''\n<div class=\"split shockS\">")
s=s[:a]+r'''BUBBLE = '<g class="f">' + bubble(30, -110, 300, ['A tax-free bucket?', 'Nobody ever told me!'], 200, 118, size=22) + '</g>'
MBUB = '<g class="f">' + bubble(350, -124, 320, ['&#8220;We talked about this ten', 'years ago, my friend. You', 'weren&#8217;t ready then, and', 'that&#8217;s okay. You&#8217;re ready now.&#8221;'], 470, 132, size=19, bold_last=True) + '</g>'
SHOCK = scene(ground(700,420) + person('john',200,410,1.1,mood='shock') + person('mehar',470,410,1.05) + BUBBLE + MBUB, 470).replace('viewBox="0 0 1300 470" width="1300" height="470"','viewBox="0 -140 700 610" width="700" height="610"')
'''+s[b:]
open(f,'w').write(s); print('ok')
