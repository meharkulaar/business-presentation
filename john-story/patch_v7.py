f='build.py';s=open(f).read()
def R(a,b,cnt=1):
    global s; assert a in s,a[:80]; s=s.replace(a,b,cnt)

# 1) CDA bucket becomes a reusable function with unique ids
a=s.index("CDA_BUCKET = ("); b=s.index("slide('''", a)
s=s[:a]+'''def cda_bucket(p, w=300, h=420, cls=''):
    coins = ''.join(f'<g transform="translate({x},0)"><g class="coinF" style="animation-delay:{d}s"><ellipse rx="17" ry="17" fill="#F2CC5A" stroke="#A87A12" stroke-width="3"/><ellipse rx="10" ry="10" fill="none" stroke="#C99A2A" stroke-width="2"/><text y="6" text-anchor="middle" style="font:900 16px Georgia;fill:#8A6510">$</text></g></g>'
                    for x, d in [(-60,0),(30,.45),(-15,.9),(55,1.35),(-45,1.8),(10,2.25),(40,2.7),(-30,3.15)])
    return (f'<svg viewBox="-160 -380 320 450" width="{w}" height="{h}" class="cdaB {cls}" style="overflow:visible">'
      f'<defs><clipPath id="cc{p}"><path d="M-117,-217 L117,-217 L92,-3 L-92,-3Z"/></clipPath>'
      f'<linearGradient id="gf{p}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A0"/><stop offset=".35" stop-color="#F2CC5A"/><stop offset="1" stop-color="#B8860B"/></linearGradient></defs>'
      '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="rgba(229,185,60,.10)"/>'
      f'<g class="bkGlow"><g clip-path="url(#cc{p})"><g class="bkFill"><rect x="-130" y="-225" width="260" height="230" fill="url(#gf{p})"/>'
      '<path class="bkWave" d="M-260,-222 q32,-10 65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 t65,0 L260,-200 L-260,-200Z" fill="#FFF1BF" opacity=".8"/>'
      + ''.join(f'<circle class="bkSpark" style="animation-delay:{k*.37:.2f}s" cx="{-70+k*20}" cy="-{30+(k*37)%150}" r="3" fill="#FFF8DC"/>' for k in range(8)) +
      '</g></g></g>' + coins +
      '<path d="M-120,-220 L120,-220 L94,0 L-94,0Z" fill="none" stroke="#F2CC5A" stroke-width="7" stroke-linejoin="round"/>'
      '<text x="0" y="-104" text-anchor="middle" class="bkTxt">CDA</text></svg>')
CDA_BUCKET = cda_bucket('A')

'''+s[b:]
R("""<div class="sp">{scene(bucket(260,400,1.25,.18,'bkA'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')}</div>""",
  """<div class="sp cdaAuto">{cda_bucket('B', 380, 520)}</div>""")

# 2) Shock bubble: centred over John's head, well clear
R("BUBBLE='<g class=\"f\" transform=\"translate(-6,-104)\">", "BUBBLE='<g class=\"f\" transform=\"translate(-40,-168)\">")
R("""'viewBox="0 -40 620 510" width="620" height="510"'""", """'viewBox="0 -100 620 570" width="620" height="570"'""")

# 3) Dollar slide: no premium talk, Mehar asks which dollar John would use
a=s.index('<div class="dlR">'); b=s.index('<div class="src">Approximate BC rates')
s=s[:a]+'''<div class="dlR">
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
'''+s[b:]
R("<div class=\"src\">Approximate BC rates: small business about 11%, top personal rate about 53.5%. Rounded for illustration. Not tax advice; confirm with your accountant.</div>",
  "<div class=\"src\">Approximate BC rates: small business about 11%, top personal rate about 53.5%. Rounded for illustration. Not tax advice; confirm with your accountant.</div>")
R("slide(f\'\'\'\n<div class=\"kick\">First, Mehar explained one simple idea</div>",
  """DL_MEHAR = scene(ground(220,400)+person('mehar',110,390,.95), 420).replace('viewBox="0 0 1300 420" width="1300" height="420"','viewBox="0 0 220 420" width="150" height="286"')
DL_JOHN = scene(ground(220,400)+person('john',110,390,.95), 420).replace('viewBox="0 0 1300 420" width="1300" height="420"','viewBox="0 0 220 420" width="150" height="286"')
slide(f\'\'\'
<div class="kick">First, Mehar explained one simple idea</div>""")
R("<h2>Which dollar pays: <span class=\"red\">personal</span> or <span class=\"gold\">corporate</span>?</h2>",
  "<h2>A <span class=\"red\">personal</span> dollar vs a <span class=\"gold\">corporate</span> dollar</h2>")

# 4) Meeting chapter: no sign; John brings his wishlist, Mehar promises step by step
a=s.index("slide(chapter('Chapter Two'"); b=s.index("# 9 7 NEEDS CHECK-UP")
wish = ("'<g transform=\"translate(70,96) rotate(-3)\"><rect x=\"0\" y=\"0\" width=\"270\" height=\"280\" rx=\"10\" fill=\"#F4E7C8\" stroke=\"#C9A227\" stroke-width=\"4\"/>"
        "<text x=\"135\" y=\"44\" text-anchor=\"middle\" style=\"font:900 24px Georgia;fill:#7A0F1A\">John&#8217;s wishlist</text><line x1=\"24\" y1=\"60\" x2=\"246\" y2=\"60\" stroke=\"#C9A227\" stroke-width=\"2\"/>'"
        "+''.join(f'<rect x=\"24\" y=\"{88+k*48}\" width=\"22\" height=\"22\" rx=\"4\" fill=\"#fff\" stroke=\"#7A0F1A\" stroke-width=\"3\"/><text x=\"58\" y=\"{106+k*48}\" style=\"font:700 17px Georgia;fill:#3A2A1A\">{t}</text>' for k,t in enumerate(['Debt-free in 10 years','More locations','Retire by 65','Take care of my family']))"
        "+'</g>'")
s=s[:a]+f'''slide(chapter('Chapter Two', 'December 28, 2026 · John is 40', 'The Meeting',
    {wish}
    + desk(760,410,1.0)+person('john',560,410,1.0,arm='hold')+'<g transform="translate(598,292) rotate(-8)"><rect width="46" height="60" rx="4" fill="#F4E7C8" stroke="#C9A227" stroke-width="2"/><rect x="8" y="12" width="9" height="9" fill="none" stroke="#7A0F1A" stroke-width="2"/><rect x="8" y="28" width="9" height="9" fill="none" stroke="#7A0F1A" stroke-width="2"/><rect x="8" y="44" width="9" height="9" fill="none" stroke="#7A0F1A" stroke-width="2"/></g>'
    + person('mehar',960,410,1.0)+tree(1180,410,.62)
    + '<text x="760" y="60" text-anchor="middle" class="capt">&ldquo;Let&rsquo;s go through your list together, step by step.&rdquo;</text>'
    + label(560,150,'John',size=22)+label(960,150,'Mehar',size=22)),
    'sChap', hud=H(40, 1509000))

# 8b MEHAR'S PROCESS
STEPS = [('Listen', 'Your wishlist, your goals, your worries'),
         ('Check-up', 'The 7 key needs of your corporation'),
         ('Educate', 'The right dollar and the two buckets, explained simply'),
         ('Team up', 'Your accountant and lawyer at the same table'),
         ('Design', 'A plan built for you, with a real illustration'),
         ('Start', 'Put it in place right away, not someday'),
         ('Review', 'Every year, and whenever life changes')]
slide(\'\'\'
<div class="kick">The Team All In service</div>
<h2>Mehar walked John through it, <span class="gold">step by step.</span></h2>
<p class="big">In ten years of business, nobody had ever done this for John.</p>
<div class="road">\'\'\' + ''.join(f'<div class="rdS f"><i>{{k+1}}</i><b>{{t}}</b><span>{{d}}</span></div>' for k, (t, d) in enumerate(STEPS)) + \'\'\'</div>
\'\'\', 'sRoad', hud=H(40, 1509000))

'''+s[b:]

# 5) Service ribbon on the slides where each step happens
R("# ------------------------------------------------------------------ page", '''# service ribbons
SVC = {'sNeeds': 2, 'sDollar': 3, 'sBuckets': 3, 'sShock': 3, 'sProbs': 3, 'sTeam': 4, 'sStruct': 5, 'sAio': 5, 'sPlan': 5, 'sSnap': 5,
       'sChart': 5, 'sCda': 5, 'sLoc2': 7, 'sIfa': 7, 'sCrash': 7, 'sRaj': 7, 'sRetire': 7, 'sSucc': 7}
for i, h in enumerate(SLIDES):
    cls = h.split('class="slide ', 1)[1].split('"', 1)[0].split()[0]
    if cls in SVC:
        k = SVC[cls]
        SLIDES[i] = h.replace('>', f'><div class="svc">&#9733; Mehar&rsquo;s process &middot; Step {k} of 7: <b>{STEPS[k-1][0]}</b></div>', 1)
    elif 'sChap' in h.split('>', 1)[0] and 'He Starts Now' in h:
        SLIDES[i] = h.replace('>', '><div class="svc">&#9733; Mehar&rsquo;s process &middot; Step 6 of 7: <b>Start</b></div>', 1)

# ------------------------------------------------------------------ page''')

# 6) Crash: clouds fully visible, plus Mehar's call; and a Chapter Five title before it
a=s.index("{scene(ground(1300,380)+cloud(560,70,1.15)+cloud(800,90,.9)+");
R("{scene(ground(1300,380)+cloud(560,70,1.15)+cloud(800,90,.9)+'<line", "{scene(ground(1300,380)+'<g transform=\"translate(0,60)\">'+cloud(560,70,1.0)+cloud(800,90,.8)+'<line")
R("""stroke-linecap="round" opacity=".8"/><g transform="translate(980,90)">""", """stroke-linecap="round" opacity=".8"/></g><g transform="translate(980,90)">""")
R("""  <p class="f">His policy&rsquo;s cash value <b class="green">didn&rsquo;t drop at all</b>""", """  <p class="f"><b>Mehar called John that same morning</b> and walked him through it, so nothing was sold in a panic.</p>
  <p class="f">His policy&rsquo;s cash value <b class="green">didn&rsquo;t drop at all</b>""")
R("# 21 TWIST 1 crash", '''# 20b CHAPTER 5
slide(chapter('Chapter Five', '2034 · John is 48', 'The Storm',
    ground(1300,400)+cloud(420,150,.95)+cloud(700,120,1.1)+cloud(960,160,.85)
    + '<path d="M700,215 L670,285 L700,282 L676,350 L740,262 L708,266 L730,215Z" fill="#FFE08A" class="bolt"/>'
    + clinic(300,390,.7,1)+clinic(1000,390,.7,2)+person('john',600,390,.85)+person('emma',690,390,.8)),
    'sChap sStorm', hud=H(48, 2750000, '0,4,5', '111'))

# 21 TWIST 1 crash''')

# 7) Last Christmas home: clean symmetric frame, fully inside the scene
a=s.index("HOME = ("); b=s.index("slide(chapter('Chapter Seven'")
s=s[:a]+'''def _roof_y(x):
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
'''+s[b:]

open(f,'w').write(s); print('ok')
