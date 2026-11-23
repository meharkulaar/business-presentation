import re
f='build.py';s=open(f).read()
def R(a,b):
    global s; assert a in s,a[:80]; s=s.replace(a,b,1)

# 1) remove the lamp entirely from the Rat Race
a=s.index("    L.append('<ellipse cx=\"470\" cy=\"560\" rx=\"200\" ry=\"70\" fill=\"url(#rLamp)\"/>')")
b=s.index("    L.append(person('john', 360, 690, 1.35")
s=s[:a]+s[b:]

# 2) generic full-screen chapter helpers + scenes
R("# 4 CHAPTER 1: THE RAT RACE (full-screen split)", r'''# ---- full-screen chapter title pages
def full_svg(inner, defs=''):
    return f'<svg class="ratSvg" viewBox="0 0 1440 810" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>{defs}</defs>{inner}</svg>'
def chap_full(num, when, title, svg, cls, hud=None, chips=''):
    ch = f'<div class="fChips">{chips}</div>' if chips else ''
    slide(f"""{svg}{ch}<div class="ratTop"><div class="chNum">{num}</div><div class="chWhen">{when}</div><h1>{title}</h1></div>""", cls + ' sFull', hud=hud)
def chips(*items):
    return ''.join(f'<div class="fChip f">{t}</div>' for t in items)
def wall_room(c1, c2, stripe='rgba(255,255,255,.04)'):
    return (f'<rect width="1440" height="810" fill="url(#wr)"/>' + ''.join(f'<path d="M{x},0 V640" stroke="{stripe}" stroke-width="20"/>' for x in range(30, 1440, 60))
            + '<rect y="640" width="1440" height="170" fill="#5A3A22"/>' + ''.join(f'<path d="M{x},640 V810" stroke="rgba(0,0,0,.25)" stroke-width="2"/>' for x in range(60, 1440, 100))
            + '<rect y="630" width="1440" height="12" fill="#E8D6B0"/>', f'<linearGradient id="wr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
def win(x, y, w, h, extra=''):
    import random as _r; _r.seed(x)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0E1A30"/>' + ''.join(f'<circle cx="{_r.randint(x+10,x+w-10)}" cy="{_r.randint(y+10,y+h-40)}" r="2.2" fill="#fff" opacity=".85"/>' for _ in range(int(w*h/2500)))
            + extra + f'<path d="M{x},{y+h-24} Q{x+w*.3},{y+h-36} {x+w*.55},{y+h-28} T{x+w},{y+h-30} V{y+h} H{x}Z" fill="#DCE6F0"/>'
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#E8D6B0" stroke-width="12"/><path d="M{x+w/2},{y} V{y+h} M{x},{y+h/2} H{x+w}" stroke="#E8D6B0" stroke-width="7"/>'
            + f'<rect x="{x-12}" y="{y+h-4}" width="{w+24}" height="14" fill="#C9B79C"/>')
def calendar(x, y, day):
    return (f'<g transform="translate({x},{y})"><rect x="-55" y="-60" width="110" height="120" rx="6" fill="#FBF6EA" stroke="#B9AE96" stroke-width="3"/><rect x="-55" y="-60" width="110" height="34" rx="6" fill="#B3202A"/>'
            f'<text y="-36" text-anchor="middle" style="font:900 18px Georgia;fill:#FFF4DC">DEC</text><text y="34" text-anchor="middle" style="font:900 54px Georgia;fill:#2E1E12">{day}</text></g>')
def office(extra_win=''):
    bg, d = wall_room('#1F3A3A', '#132626')
    shelf = '<g><rect x="1110" y="300" width="290" height="340" fill="#5A3A22"/>' + ''.join(f'<rect x="1110" y="{300+k*85}" width="290" height="10" fill="#3E2614"/>' for k in range(5))
    import random as _r; _r.seed(5)
    for k in range(4):
        x = 1122
        while x < 1386:
            w = _r.randint(14, 26); h = _r.randint(48, 70)
            shelf += f'<rect x="{x}" y="{385+k*85-h}" width="{w}" height="{h}" fill="{_r.choice(["#9E1B26","#2F6E4C","#C9962A","#3E5C76","#E8D6B0","#6B4A8A"])}"/>'
            x += w + 3
    shelf += '</g>'
    return bg + win(90, 300, 330, 240, extra_win) + shelf, d
def big_desk():
    return ('<rect x="480" y="560" width="560" height="26" rx="6" fill="#6B4226"/><rect x="500" y="586" width="520" height="230" fill="#5A3A22"/><rect x="500" y="586" width="520" height="230" fill="url(#gShade)" opacity=".45"/>'
            '<rect x="520" y="600" width="480" height="4" fill="rgba(255,255,255,.08)"/>')

# Chapter Two: The Meeting
def ch2():
    bg, d = office()
    paper = '<g transform="translate(700,552) rotate(-4)"><rect x="-70" y="-14" width="140" height="22" rx="2" fill="#F4E7C8" stroke="#C9A227" stroke-width="2"/><text y="2" text-anchor="middle" style="font:700 12px Georgia;fill:#7A0F1A">John&#8217;s wishlist</text></g>'
    return full_svg(bg + calendar(560, 380, '28') + person('john', 420, 690, 1.3, arm='hold') + person('mehar', 1020, 690, 1.3) + big_desk() + paper
                    + '<g transform="translate(900,556)"><rect x="-20" y="-18" width="40" height="22" rx="4" fill="#FFF"/><path d="M20,-12 c10,0 10,12 0,12" stroke="#FFF" stroke-width="4" fill="none"/></g>', d)

# Chapter Three: He Starts Now
def ch3():
    fw = ''.join(f'<g transform="translate({cx},{cy})" class="fw" style="animation-delay:{dl}s">' + ''.join(f'<path d="M0,0 L{24*__import__("math").cos(k*0.785):.1f},{24*__import__("math").sin(k*0.785):.1f}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for k in range(8)) + '</g>'
                 for cx, cy, c, dl in ((170, 360, '#FFD27A', 0), (320, 340, '#FF6F6B', .6), (250, 420, '#7BE3AE', 1.2)))
    bg, d = office(fw)
    form = '<g transform="translate(740,552) rotate(-3)"><rect x="-80" y="-16" width="160" height="26" rx="2" fill="#FBF6EA" stroke="#B9AE96" stroke-width="2"/><text y="2" text-anchor="middle" style="font:700 11px Georgia;fill:#2E1E12">APPLICATION</text></g>'
    pen = '<path d="M806,548 L842,520" stroke="#1E1E24" stroke-width="6" stroke-linecap="round"/><path d="M806,548 L800,554" stroke="#E5B93C" stroke-width="4"/>'
    return full_svg(bg + calendar(560, 380, '30') + tree(1290, 640, .9) + person('john', 800, 690, 1.3, arm='hold') + person('mehar', 1000, 690, 1.25, arm='up')
                    + big_desk() + gift(600, 560, 1.15, txt='THE PLAN') + form + pen, d)

# Chapter Four: Location #2
def street(sky1, sky2):
    d = f'<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky1}"/><stop offset="1" stop-color="{sky2}"/></linearGradient>'
    import random as _r; _r.seed(9)
    g = '<rect width="1440" height="810" fill="url(#sk)"/>' + ''.join(f'<circle cx="{_r.randint(0,1440)}" cy="{_r.randint(10,330)}" r="{_r.choice([1.2,1.8,2.4])}" fill="#fff" opacity=".7"/>' for _ in range(60))
    g += '<path d="M0,520 L120,470 L260,500 L420,450 L600,490 L780,440 L960,486 L1140,446 L1300,480 L1440,456 V640 H0Z" fill="rgba(20,20,40,.45)"/>'
    g += '<path d="M0,620 Q360,590 720,612 T1440,606 V810 H0Z" fill="#E8EEF6"/><path d="M0,640 Q360,616 720,634 T1440,630" stroke="rgba(160,170,190,.6)" stroke-width="3" fill="none"/>'
    return g, d
def ch4():
    g, d = street('#2A1E46', '#5A3A5E')
    banner = '<path d="M760,300 Q1000,340 1240,300" stroke="#E8D6B0" stroke-width="3" fill="none"/><g transform="translate(1000,330)"><rect x="-150" y="-26" width="300" height="52" rx="8" fill="#B3202A" stroke="#FFE7A6" stroke-width="3"/><text y="10" text-anchor="middle" style="font:900 28px Georgia;fill:#FFE7A6;letter-spacing:.08em">GRAND OPENING</text></g>'
    ribbon = '<path d="M820,600 C900,590 960,612 1000,598 C1060,612 1120,590 1180,600" stroke="#C62D3A" stroke-width="10" fill="none"/><path d="M990,590 l-24,30 M1010,590 l24,30" stroke="#C62D3A" stroke-width="8"/><circle cx="1000" cy="596" r="12" fill="#C62D3A"/>'
    sc = '<g transform="translate(1000,560) rotate(-20)"><path d="M0,0 L70,-14 M0,0 L70,14" stroke="#B9C2CC" stroke-width="8" stroke-linecap="round"/><circle cx="-14" cy="-10" r="12" fill="none" stroke="#E5B93C" stroke-width="6"/><circle cx="-14" cy="10" r="12" fill="none" stroke="#E5B93C" stroke-width="6"/></g>'
    return full_svg(g + clinic(330, 620, 1.35, 1) + clinic(1000, 620, 1.6, 2) + banner + person('emma', 560, 700, 1.0, arm='up') + person('lily', 640, 700, .66, arm='up') + person('max', 700, 700, .56)
                    + ribbon + person('john', 900, 710, 1.15, 'coat', arm='hold') + person('raj', 1100, 710, 1.15, 'coat', arm='hold') + sc, d)

# Chapter Five: The Storm
def ch5():
    d = '<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14141E"/><stop offset="1" stop-color="#3A3446"/></linearGradient>'
    import random as _r; _r.seed(4)
    rain = ''.join(f'<line class="rain" style="animation-delay:-{_r.uniform(0,1):.2f}s" x1="{x}" y1="{_r.randint(250,330)}" x2="{x-14}" y2="{_r.randint(360,420)}" stroke="#AFC3D6" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>' for x in range(20, 1440, 26))
    g = ('<rect width="1440" height="810" fill="url(#st)"/>' + cloud(260, 300, 1.3) + cloud(640, 270, 1.6) + cloud(1060, 300, 1.4) + cloud(1340, 320, 1.0) + rain
         + '<path d="M760,330 L720,430 L760,426 L726,520 L812,400 L770,404 L800,330Z" fill="#FFE08A" class="bolt"/>'
         + '<path d="M0,620 Q360,600 720,615 T1440,610 V810 H0Z" fill="#C9D2DC"/>'
         + clinic(250, 625, 1.25, 1) + clinic(1210, 625, 1.25, 2) + umbrella(720, 470, 1.25) + person('john', 670, 700, 1.15, arm='hold', mood='shock') + person('emma', 790, 700, 1.1))
    return full_svg(g, d)

# Chapter Six: Retirement
def ch6():
    g, d = street('#3A2050', '#E08A5A')
    keys = '<g transform="translate(724,560)"><circle r="12" fill="none" stroke="#E5B93C" stroke-width="5"/><path d="M8,8 L30,30 M22,22 L28,16 M26,26 L32,20" stroke="#E5B93C" stroke-width="5" stroke-linecap="round"/></g>'
    return full_svg(g + clinic(220, 610, 1.15, 1) + clinic(520, 610, 1.15, 2) + clinic(1260, 610, 1.15, 3)
                    + person('john', 680, 710, 1.2, arm='hold') + keys + person('lily', 820, 710, 1.12, arm='hold') + person('emma', 960, 710, 1.05) + person('max', 1070, 710, 1.1), d)

# Chapter Seven: The Last Christmas
def ch7():
    bg, d = wall_room('#6B2A22', '#3E1610', 'rgba(255,220,170,.05)')
    fire = ('<rect x="560" y="390" width="320" height="250" fill="#8A3A2A"/><rect x="540" y="372" width="360" height="24" rx="4" fill="#5A3A22"/><rect x="630" y="460" width="180" height="180" rx="90" fill="#1A0A06"/><rect x="630" y="550" width="180" height="90" fill="#1A0A06"/>'
            '<path class="tFl" d="M680,638 C660,600 676,566 700,540 C704,566 720,574 720,592 C732,576 740,552 732,530 C762,566 768,610 758,638Z" fill="#FF9A3A"/><path class="tFl" d="M700,638 C690,614 698,594 712,582 C714,600 726,604 728,618 C736,606 738,592 736,580 C750,602 752,624 744,638Z" fill="#FFD27A"/>'
            '<path d="M540,372 Q600,392 660,372 T780,372 T900,372" stroke="#2F6E4C" stroke-width="12" fill="none"/>' + ''.join(f'<circle cx="{560+k*44}" cy="{378 + (6 if k%2 else 0)}" r="6" fill="{["#FF4D5E","#FFD27A","#7BE3AE"][k%3]}"/>' for k in range(8)))
    return full_svg(bg + win(90, 300, 300, 240) + fire + tree(1270, 640, 1.1)
                    + person('john', 260, 700, 1.15, 'old') + person('emma', 380, 700, 1.08, 'old') + person('lily', 1000, 700, 1.05) + person('max', 1110, 700, 1.05)
                    + person('lily', 540, 710, .55) + person('max', 610, 710, .5) + person('lily', 830, 710, .52) + person('max', 900, 710, .46)
                    + label(260, 742, 'John, 90', size=20), d)

# 4 CHAPTER 1: THE RAT RACE (full-screen split)''')

def replace_call(start_marker, new_code):
    global s
    a = s.index(start_marker)
    b = s.index("'sChap", a); b = s.index("\n", b) + 1
    s = s[:a] + new_code + s[b:]
replace_call("slide(chapter('Chapter Two'", "chap_full('Chapter Two', 'December 28, 2026 &middot; John is 40', 'The Meeting', ch2(), 'sChap', hud=H(40, NW(40)))\n")
replace_call("slide(chapter('Chapter Three'", "chap_full('Chapter Three', 'December 30, 2026 &middot; the same month', 'He Starts Now', ch3(), 'sChap', hud=H(40, NW(40), '0,4', '100'))\n")
replace_call("slide(chapter('Chapter Five'", "chap_full('Chapter Five', '2034 &middot; John is 48', 'The Storm', ch5(), 'sChap sStorm', hud=H(48, NW(48), '0,3,4,5', '111'))\n")
a = s.index("HOME = (")
b = s.index("slide(chapter('Chapter Seven'")
s = s[:b] + s[b:]
replace_call("slide(chapter('Chapter Seven'", "chap_full('Chapter Seven', 'Christmas 2076 &middot; John is 90', 'The Last Christmas', ch7(), 'sChap sHome', hud=H(90, NW(90), '0,1,2,3,4,5,6', '111'))\n")

# Chapter Four: Location #2 slide -> full title page with chips
a = s.index("# 19 CHAPTER 4 + location 2 + famous names"); b = s.index("''', 'sLoc2'"); b = s.index("\n", b) + 1
hud_line = s[s.index("''', 'sLoc2'"):b]
hud = hud_line.split("hud=", 1)[1].rstrip()[:-1]
s = s[:a] + f'''# 19 CHAPTER 4: LOCATION #2 (full title page)
chap_full('Chapter Four', 'Christmas 2032 &middot; John is 46', 'Location #2', ch4(), 'sLoc2', hud={hud},
  chips=chips(f'Funded by borrowing against his policy&rsquo;s cash value ({{money(ILL[46]["totalCV"])}})', 'The policy kept growing as if he&rsquo;d never touched it', 'Clinic #2 adds about $750K a year: revenue doubles to $1.5M'))
''' + s[b:]

# Chapter Six: Retirement slide -> full title page with chips
a = s.index("# 24 CHAPTER 6: 65"); b = s.index("''', 'sRetire'"); b = s.index("\n", b) + 1
hud_line = s[s.index("''', 'sRetire'"):b]
hud = hud_line.split("hud=", 1)[1].rstrip()[:-1]
s = s[:a] + f'''# 24 CHAPTER 6: RETIREMENT (full title page)
chap_full('Chapter Six', 'Christmas 2051 &middot; John is 65', 'Retirement, Right on Time', ch6(), 'sRetire', hud={hud},
  chips=chips('Three clinics, about $1M a year each', '<b>Sarah:</b> holding company, estate freeze, updated will', '<b>David:</b> tax-free dividends and retirement income', '<b>Mehar:</b> policies and seg funds into tax-efficient income'))
''' + s[b:]
open(f,'w').write(s); print('ok')
