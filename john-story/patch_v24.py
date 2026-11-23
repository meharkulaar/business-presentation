f='build.py';s=open(f).read()
def R(a,b,n=1):
    global s; assert a in s,a[:80]; s=s.replace(a,b,n)

# second policy data
R("RAJ = {r['age']: r for r in json.load(open(os.path.join(HERE, 'raj.json')))['rows']}",
  "RAJ = {r['age']: r for r in json.load(open(os.path.join(HERE, 'raj.json')))['rows']}\nP2 = {r['age']: r for r in json.load(open(os.path.join(HERE, 'john2.json')))['rows']}\ndef P2DB(a): return P2[a]['totalDB'] if a >= 51 else (P2[51]['totalDB'] if a == 50 else 0)\ndef P2CV(a): return P2[a]['totalCV'] if a >= 51 else 0\nTOT90 = ILL[90]['totalDB'] + P2[90]['totalDB']")
R("        cda = ILL[age]['totalDB'] if age in ILL else 0", "        cda = (ILL[age]['totalDB'] if age in ILL else 0) + P2DB(age)")
R("corp = 5e5*1.05**(a-40); cv = ILL[a]['totalCV'] if a >= 41 else 0;", "corp = 5e5*1.05**(a-40); cv = (ILL[a]['totalCV'] if a >= 41 else 0) + P2CV(a);")

# double taxation
R("<b>The estate tax trap</b><span>If John died, his corporation would face tax on his shares and again when the money is paid out to Emma.</span>",
  "<b>Double taxation</b><span>When John dies, his shares are taxed on his final return, and the same money is taxed again when the corporation pays it out to his family.</span>")

# debt slide: CDA before policy 2
R("''', 'sDebt', hud=H(50, NW(50), '0,3,4,5', '111'))", "''', 'sDebt', hud=H(50, NW(50) - 0, '0,3,4,5', '111', cda=ILL[50]['totalDB']))")

# policy #2 slide after debt-free
R("# 23 TWIST 2 partner dies", '''# 22c POLICY #2
J2SNAP = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(HERE, 'source', 'john2-snap.jpg'), 'rb').read()).decode()
slide(f\'\'\'
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
\'\'\', 'sPol2', hud=H(50, NW(50), '0,3,4,5', '111'))

# 23 TWIST 2 partner dies''')

# legacy totals: both policies
R('<div class="f gVal"><span>Passed to his family, tax-free</span><b>{money(ILL[90]["totalDB"])}</b></div>',
  '<div class="f gVal"><span>Passed to his family, tax-free</span><b>{money(TOT90)}</b></div>')
R('<div class="fl f"><span>Policy pays his corporation</span><b>{money(i90["totalDB"])}</b></div>',
  '<div class="fl f"><span>His two policies pay his corporation</span><b>{money(TOT90)}</b></div>')
R("_tile('Tax-free to his family', '$0', counter(int(ILL[90]['totalDB'])), 'gold')", "_tile('Tax-free to his family', '$0', counter(int(TOT90)), 'gold')")
R("'sLegacy': (PW, 'His family receives $14.18M, tax-free')}", "'sLegacy': (PW, f'His family receives {money(TOT90)}, tax-free')}")
R("'sRajBS': (TA,", "'sPol2': (TA, 'Starts a second corporate policy: $150K a year for 15 years'),\n       'sFamily': (PW, 'Time with his family: every trip, every game, every graduation'),\n       'sRajBS': (TA,")
R("SVC = {'sCdaFill': 3,", "SVC = {'sPol2': 7, 'sCdaFill': 3,")

# family time montage before Chapter Seven
R("# 26 CHAPTER 7: 90", '''# 25b WHAT THE PLAN REALLY GAVE HIM: TIME
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
slide(f\'\'\'
<div class="kick">What the plan really gave him</div>
<h2>Time. <span class="gold">All the moments he used to miss.</span></h2>
<p class="big famP">Because his money was working, John didn&rsquo;t have to work every hour. From the first year, he took Emma and the kids away a few times a year. He never missed a game, a recital or a parent-teacher night. He was there for every first day of school, and he cheered at every graduation.</p>
<div class="polR">{FAM}</div>
<p class="famQ f">&ldquo;Remember the concert I missed when Lily was six? <b>I never missed another one.</b>&rdquo;</p>
\'\'\', 'sFamily')

# 26 CHAPTER 7: 90''')
open(f,'w').write(s); print('ok')
