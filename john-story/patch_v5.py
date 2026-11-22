f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:60]; s=s.replace(a,b,1)

# 1) quotes from David and Sarah on the team slide
R('''  <div class="f"><b>David &middot; accountant</b><span>Tax returns, CDA tracking, capital dividend elections</span></div>
  <div class="f"><b>Sarah &middot; lawyer</b><span>Wills, holding company, shareholder agreement, estate freeze</span></div>''',
'''  <div class="f"><b>David &middot; accountant</b><span>Tax returns, CDA tracking, capital dividend elections</span><q>&ldquo;I&rsquo;d watched his passive income get taxed every year. This finally fixed it.&rdquo;</q></div>
  <div class="f"><b>Sarah &middot; lawyer</b><span>Wills, holding company, shareholder agreement, estate freeze</span><q>&ldquo;Insurance with no agreements behind it is half a plan. We made every document match.&rdquo;</q></div>''')

# 2) live audience moment after the buckets slide
R("BUBBLE=", '''slide(\'\'\'
<div class="kick">A question for the room</div>
<div class="askQ">What&rsquo;s sitting in <span class="red">your</span> corporation&rsquo;s <b>taxable bucket</b> right now?</div>
<p class="f mid">And how much of it could be in the <b class="gold">tax-free bucket</b> instead?</p>
\'\'\', 'sAsk')

BUBBLE=''')

# 3) Christmas-morning gift reveal before the legacy slide
R("# 27 LEGACY", '''# 26b CHRISTMAS MORNING REVEAL
slide(f\'\'\'
<div class="kick">Christmas morning, years later</div>
<h2>John&rsquo;s grandchildren open the last gift he left.</h2>
<div class="giftR">
  {scene(ground(1300,420)+person('lily',300,410,.62)+person('max',390,410,.56)+person('lily',910,410,.58)+person('max',1000,410,.5)
    +'<g class="gBox"><rect x="540" y="250" width="220" height="160" fill="#9E1B26"/><rect x="540" y="250" width="110" height="160" fill="rgba(255,255,255,.08)"/><rect x="636" y="250" width="28" height="160" fill="#E5B93C"/></g>'
    +'<g class="f gLid"><rect x="526" y="214" width="248" height="40" fill="#B32533"/><rect x="636" y="214" width="28" height="40" fill="#E5B93C"/><path d="M650,214 C600,150 570,200 650,214 C730,200 700,150 650,214Z" fill="#E5B93C"/></g>', 470)}
  <div class="f gVal"><span>Passed to his family, tax-free</span><b>{money(ILL[90]["totalDB"])}</b></div>
</div>
\'\'\', 'sGift', hud=H(90, 21500000, '0,1,2,3,4,5,6', '111'))

# 27 LEGACY''')

# 4) split-screen John vs Jake (replaces the table)
a=s.index("# 29 SIDE BY SIDE"); b=s.index("# 30 TWO DOCTORS")
s=s[:a]+'''# 29 SPLIT SCREEN
cmp = [('Age 46', 'Opened clinic #2', 'Cash stuck in the corporation'),
       ('Age 48: crash', 'Guaranteed floor, policy untouched', 'Lost 25% overnight'),
       ('Debt-free', 'At 50', 'At 58'),
       ('Age 55: partner dies', 'Buy-sell funded, business saved', 'No agreement: borrowed to buy out the family'),
       ('Locations', '3', '1'),
       ('Retired', 'At 65', 'At 70')]
lj = ''.join(f'<div class="spR f"><span>{a}</span><b>{b}</b></div>' for a, b, c in cmp)
rk = ''.join(f'<div class="spR f"><span>{a}</span><b>{c}</b></div>' for a, b, c in cmp)
slide(f\'\'\'
<div class="kick">Two lives, playing at once</div>
<div class="splitS">
  <div class="half john"><div class="hName">John</div>{scene(ground(600,300)+person('john',300,290,.95), 310).replace('viewBox="0 0 1300 310" width="1300"','viewBox="0 0 600 310" width="560"')}<div class="rows">{lj}</div></div>
  <div class="half jake"><div class="hName">Jake</div>{scene(ground(600,300)+person('jake',300,290,.95,mood='sad'), 310).replace('viewBox="0 0 1300 310" width="1300"','viewBox="0 0 600 310" width="560"')}<div class="rows">{rk}</div></div>
</div>
<div class="src">Illustrative story. John and Jake are fictional.</div>
\'\'\', 'sSplit')

'''+s[b:]
open(f,'w').write(s); print('ok')
