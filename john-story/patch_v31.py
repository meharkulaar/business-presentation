f='build.py';s=open(f).read()
Q3="'"*3
def R(a,b):
    global s; assert a in s,a[:90]; s=s.replace(a,b,1)

# ---- Christmas list: John calling Mehar
R('<div class="sp2"><h2 class="lft">He wasn&rsquo;t asking for a sports car.</h2><p class="lft big">He wanted his <b>time</b> back, and a future his family could count on.</p><p class="lft f mid">So that same week, between Christmas and New Year&rsquo;s, <b>he called Mehar again.</b></p></div>',
  '<div class="sp2"><h2 class="lft">He wasn&rsquo;t asking for a sports car.</h2><p class="lft big">He wanted his <b>time</b> back, and a future his family could count on.</p><p class="lft f mid">So that same week, between Christmas and New Year&rsquo;s, <b>he called Mehar again.</b></p><div class="f callS">{CALL}</div></div>')
R("# 7 WISH LIST", r'''# 7 WISH LIST
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
''')

# ---- complete family plan: checklist style
a=s.index('<div class="fdC paper f"><h3>A complete plan for the family</h3><ul>'); b=s.index('</ul></div>', a)+len('</ul></div>')
CK='<i class="ck">&#10003;</i>'
s=s[:a]+f'''<div class="fdC paper f famCk"><h3>A complete plan for the family</h3><ul>
    <li>{CK}<span><b>John&rsquo;s protection:</b> from $500K term + $50K critical illness up to <b>$2.5M life (permanent + term) + $250K critical illness</b></span></li>
    <li>{CK}<span><b>John&rsquo;s flexible plan:</b> savings and investments, <em>more on that later</em></span></li>
    <li>{CK}<span><b>Emma:</b> her own protection, savings and retirement plan</span></li>
    <li>{CK}<span><b>Lily &amp; Max:</b> education savings and coverage, locked in young</span></li>
  </ul></div>'''+s[b:]

# ---- shock slide: John's line, Mehar's reply, heading
R("BUBBLE = '<g class=\"f\">' + bubble(30, -110, 300, ['A tax-free bucket?', 'Nobody ever told me!'], 200, 118, size=22) + '</g>'",
  "BUBBLE = '<g class=\"f\">' + bubble(20, -110, 310, ['Why didn&#8217;t anyone tell me', 'about this back then?'], 200, 118, size=20) + '</g>'")
a=s.index("MBUB = "); b=s.index("\n",a)
s=s[:a]+"MBUB = '<g class=\"f\">' + bubble(345, -196, 345, ['&#8220;We talked about this ten years', 'ago, my friend. The difference', 'today is that you&#8217;ve opened your', 'mind to learn. That&#8217;s okay. Let&#8217;s', 'learn from it, and focus on today', 'and your future.&#8221;'], 470, 132, size=18, bold_last=True) + '</g>'"+s[b:]
s=s.replace("""'viewBox="0 -140 700 610" width="700" height="610"'""","""'viewBox="0 -206 700 676" width="700" height="676"'""")
R('<h2 class="lft">John had never heard of it.</h2>', '<h2 class="lft">This time, John was ready.</h2>')
R('<p class="lft big f">Ten years in business. An accountant. A bank. <b>Nobody had ever shown him the tax-free bucket.</b></p>',
  '<p class="lft big f">Mehar had shown him the tax-free bucket ten years earlier. <b>This time, John was ready to listen, and to learn.</b></p>')

# ---- CDA explanation (Investopedia), tax-free visual, source
a=s.index('<div class="cdaPts">', s.index("# 15 CDA")); b=s.index("''', 'sCda'")
s=s[:a]+'''<div class="cdaPts">
    <div class="f"><b>A notional account.</b> Not a bank account: a special tax account the corporation tracks, adding up the tax-free surpluses it has built.</div>
    <div class="f"><b>What fills it:</b> the non-taxable half of capital gains, capital dividends received from other corporations, and the big one: <b class="gold">life insurance paid to the corporation</b> (minus the policy&rsquo;s cost base).</div>
    <div class="f"><b>What it does:</b> the balance can be paid to Canadian-resident shareholders as <b class="green">capital dividends, completely tax-free</b>, once the corporation files an election with the CRA (Form T2054).</div>
    <div class="f"><b>Who can use it:</b> Canadian-controlled private corporations, like John&rsquo;s dental corporation.</div>
    <div class="f note3">David tracks the balance and files the election. Mehar fills it.</div>
  </div>
</div>
<div class="src">Source: Investopedia, &ldquo;Capital Dividend Account (CDA)&rdquo;, investopedia.com/terms/c/cda.asp; Canada Revenue Agency, capital dividend accounts.</div>
'''+s[b:]
R('<div class="sp cdaAuto">{cda_bucket(\'B\', 380, 520)}</div>', '<div class="sp cdaAuto cdaTF">{cda_bucket(\'B\', 360, 490)}<div class="tfSeal"><b>TAX</b><b>FREE</b><span>&#10003;</span></div></div>')

# ---- split screen: Jake's investing
R("""cmp = [('Age 46', 'Opened clinic #2', 'Cash stuck in the corporation'),
       ('Age 48: crash', 'Guaranteed floor, policy untouched', 'Lost 25% overnight'),""",
  """cmp = [('Investing', 'Seg funds + flexible plan, about 12% a year', 'Rental condos + bank mutual funds, low returns'),
       ('Age 46', 'Opened clinic #2', 'Cash stuck in the corporation'),
       ('Age 48: crash', 'Guaranteed floor, policy untouched', 'Panic-sold at the bottom, then a tax bill'),
       ('Protection', 'Seg fund guarantees, skips probate', 'No guarantees, probate fees'),""")

# ---- bars slide: wealth gap + tax consequences
a=s.index("# 31 THE $100K DECISION"); b=s.index("''', 'sBars')")+len("''', 'sBars')")
s=s[:a]+r'''# 31 WEALTH GAP + TAX AT DEATH
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
slide(f\'\'\'
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
\'\'\', 'sBars')'''+s[b:]

# ---- CTA quote
R('<p class="big">No matter your age, your income, or your goals, this belongs in your plan.</p>',
  '<p class="ctaQ">&ldquo;Today is the second-best day to start. <b>The best day was yesterday.</b>&rdquo;</p>\n<p class="big">No matter your age, your income, or your goals, this belongs in your plan.</p>')
open(f,'w').write(s); print('ok')
