f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:80]; s=s.replace(a,b,1)

# ---- 1) precedent slide after the hook
R("# 3 TWO OWNERS", '''# 2b HOW TONIGHT WORKS
slide(\'\'\'
<div class="kick">Tonight</div>
<h2>That family didn&rsquo;t do anything wrong. <span class="gold">They just didn&rsquo;t have a plan.</span></h2>
<p class="big">So instead of slides full of rules, I&rsquo;m going to show you what a plan looks like, through one story.</p>
<div class="prec">
  <div class="pcC f"><i>&#128214;</i><b>The family is fictional</b><span>John, his wife and his kids are made up, so we can follow a whole lifetime in 40 minutes.</span></div>
  <div class="pcC f gold"><i>&#128202;</i><b>The numbers are real</b><span>A real Equitable policy illustration, and real Canadian cases along the way.</span></div>
  <div class="pcC f"><i>&#129693;</i><b>Ask yourself one question</b><span>As you watch, ask: <strong>&ldquo;Is this me?&rdquo;</strong></span></div>
</div>
\'\'\', 'sPrec')

# 3 TWO OWNERS''')

# ---- 2) Meet John (personal) after Chapter One
R("# 5 JOHN'S NUMBERS", '''# 4b MEET JOHN
MEET = scene(ground(560,420) + house(150,410,.62) + person('john',300,410,1.0) + person('emma',400,410,.93) + person('lily',476,410,.6) + person('max',530,410,.5)
  + label(300,452,'John, 40') + label(400,452,'Emma') + label(476,452,'Lily, 6') + label(534,452,'Max, 4'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 560 470" width="560"')
slide(f\'\'\'
<div class="split meetS">
  <div class="sp">{MEET}</div>
  <div class="sp2">
    <div class="kick" style="text-align:left">Meet John</div>
    <h2 class="lft">A dentist in BC who gives everything to his patients.</h2>
    <ul class="meetL">
      <li class="f"><i>&#129463;</i><span><b>40 years old</b>, ten years into running his own clinic</span></li>
      <li class="f"><i>&#10084;&#65039;</i><span>Married to <b>Emma</b>. <b>Lily</b> (6) wants to be a dentist like Dad. <b>Max</b> (4) wants to be a hockey player.</span></li>
      <li class="f"><i>&#9200;</i><span>Works <b>55 hours a week</b>. This year he missed Lily&rsquo;s school concert.</span></li>
      <li class="f"><i>&#128176;</i><span>A great income, a disciplined saver, and <b>no real plan</b> tying it all together</span></li>
    </ul>
    <p class="meetQ f">&ldquo;I built a great practice. I just never had time to build a plan.&rdquo;</p>
  </div>
</div>
<p class="f mid">Sound familiar?</p>
\'\'\', 'sMeet', hud=H(40, NW(40)))

# 5 JOHN'S NUMBERS''')
R("<div class=\"kick\">Meet John</div>\n<h2>Dentist. 10 years in business. A good income.</h2>",
  "<div class=\"kick\">John&rsquo;s finances</div>\n<h2>On paper, John is doing great.</h2>")
R("""<div class="src">From here on, John maxes out his TFSA ($7,000) and RRSP ($33,810) every year and invests another $25,000 a year in non-registered investments, all assumed to earn an average of 12% a year. Illustrative, not guaranteed.</div>
""", "")

# ---- 3) Savings plan chart after the numbers
R("# 6 RAT RACE: 3 RULES RED", '''# 5b JOHN'S SAVINGS PLAN
def _save_series():
    t, r, n = 109000, 150000, 0; rows = {40: (t, r, n, 0)}; wsum = 0
    for y in range(41, 91):
        if y <= 65: t = t*1.12 + 7000; r = r*1.12 + 33810; n = n*1.12 + 25000; w = 0
        else:
            w = (t + r + n)*1.12*.1; wsum += w; t *= 1.12*.9; r *= 1.12*.9; n *= 1.12*.9
        rows[y] = (t, r, n, w)
    return rows, wsum
SAV, SAV_W = _save_series()
def _save_chart():
    W, Hh, L, T, B = 760, 380, 70, 30, 320; mx = 18e6
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
    g.append(f'<text x="{(X(40)+X(65))/2:.0f}" y="{T+26}" class="phT" text-anchor="middle">BUILDING: adds $65,810 a year</text>')
    g.append(f'<text x="{(X(65)+X(90))/2:.0f}" y="{T+26}" class="phT b" text-anchor="middle">LIVING OFF IT: takes money out</text>')
    g.append(f'<text x="{L}" y="{Hh-6}" class="gt">John&rsquo;s age</text></svg>')
    return ''.join(g)
SAVE_CHART = _save_chart()
slide(f\'\'\'
<div class="kick">What John already does right</div>
<h2>He saves. <span class="gold">Every single year, until 65.</span></h2>
<div class="svW">
  <div class="svCh f">{SAVE_CHART}<div class="svKey"><span class="k t">TFSA</span><span class="k r">RRSP</span><span class="k n">Non-registered</span></div></div>
  <div class="svC">
    <div class="svS f"><b>Ages 41 to 65: he puts money in</b><span>TFSA maxed: <strong>$7,000</strong> &middot; RRSP maxed: <strong>$33,810</strong> &middot; plus <strong>$25,000</strong> invested. All earning an average of <strong>12%</strong>.</span></div>
    <div class="svS f gold"><b>At 65: {money(sum(SAV[65][:3]))}</b><span>He put in about $1.65M. Compounding did the rest.</span></div>
    <div class="svS f"><b>From 66: he takes money out</b><span>About 10% a year to live on: <strong>{money(SAV[66][3])}</strong> in the first year. His money still earns 12%, so <strong>the balance keeps growing</strong> while he spends.</span></div>
    <div class="svS f green"><b>By 90: {money(SAV_W)} taken out</b><span>And <strong>{money(sum(SAV[90][:3]))}</strong> still invested.</span></div>
  </div>
</div>
<div class="src">Illustrative: 2026 TFSA and RRSP limits held flat, an assumed 12% average annual return (not guaranteed), before tax. Withdrawals from 66 are about 10% of the balance each year.</div>
\'\'\', 'sSave', hud=H(40, NW(40)))

# 6 RAT RACE: 3 RULES RED''')

# keep the "problem" about the corporation, not his personal savings
R("<h2>John works harder every year. His net worth barely moves.</h2>", "<h2>But inside his corporation, John&rsquo;s money is stuck.</h2>")
R("His savings sit in the corporation, earning almost nothing.", "$250K of corporate savings sits in GICs, earning almost nothing.")
R("His savings sit in GICs, taxed every year. Nothing is building on its own.", "His corporate savings sit in GICs, taxed every year. Nothing there is building on its own.")

# ---- 4) Retirement: explain the switch to withdrawals
R("""<p class="f mid">&#10003; Open more locations &nbsp; &#10003; Retire by 65 &nbsp;&middot;&nbsp; His TFSA, RRSP and investments: <b class="gold">{money(sum(ACCTS(65)))}</b></p>""",
  """<p class="f mid">&#10003; Open more locations &nbsp; &#10003; Retire by 65 &nbsp;&middot;&nbsp; He stops adding to his investments (<b class="gold">{money(sum(ACCTS(65)))}</b>) and starts taking money out, about <b class="gold">{money(SAV[66][3])}</b> in year one, while the rest keeps growing.</p>""")

# ---- 5) Raj's policy and the buy-sell, after the IFA slide
R("# 21 TWIST 1 crash", '''# 20a RAJ'S POLICY + BUY-SELL
RAJBS = scene(ground(520,420) + clinic(130,410,.62,2) + person('john',300,410,.9,'coat') + person('raj',420,410,.9,'coat')
  + '<path d="M344,300 C356,292 374,292 386,300" stroke="#F1C9A0" stroke-width="12" fill="none" stroke-linecap="round"/>'
  + label(300,448,'John') + label(420,448,'Dr. Raj'), 470).replace('viewBox="0 0 1300 470" width="1300"','viewBox="0 0 520 470" width="520"')
slide(f\'\'\'
<div class="kick">Clinic #2 &middot; a new partner</div>
<h2>Raj buys in, and gets the same plan.</h2>
<div class="split rajB">
  <div class="sp">{RAJBS}</div>
  <div class="bsF">
    <div class="bfS f"><i>1</i><span><b>A policy on each partner.</b> The clinic corporation owns a whole life policy on John <em>and</em> one on Raj, sized to each partner&rsquo;s share.</span></div>
    <div class="bfS f"><i>2</i><span><b>Sarah writes the buy-sell agreement.</b> If a partner dies, the corporation must buy his shares from his family, at a fair price.</span></div>
    <div class="bfS f"><i>3</i><span><b>The policy pays for it.</b> The payout goes to the corporation, credits the CDA, and funds the buyout. <b class="gold">His family gets cash. The survivor keeps the clinic.</b></span></div>
    <div class="bfS f gold"><i>4</i><span><b>Raj gets the upside too.</b> His policy builds cash value he can borrow against, just like John&rsquo;s.</span></div>
  </div>
</div>
<div class="src">Illustrative. Buy-sell structures vary; ownership and beneficiary set-up should be designed with your lawyer and accountant.</div>
\'\'\', 'sRajBS', hud=H(46, NW(46), '0,3,4,5', '101'))

# 21 TWIST 1 crash''')
R("SVC = {'sNeeds': 2,", "SVC = {'sRajBS': 5, 'sNeeds': 2,")

open(f,'w').write(s); print('ok')
