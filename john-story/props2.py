# ---- upgraded characters & props (shading, faces, hands, snow detail) ----
GDEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="gShade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
<radialGradient id="gFace" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></radialGradient>
<linearGradient id="gSnow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9D4E6"/></linearGradient>
<linearGradient id="gTree" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2E7D4F"/><stop offset=".5" stop-color="#1F5E3A"/><stop offset="1" stop-color="#123D25"/></linearGradient>
<linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7F2EA"/><stop offset="1" stop-color="#DCD3C4"/></linearGradient>
<linearGradient id="gGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE7A8"/><stop offset="1" stop-color="#F2B95A"/></linearGradient>
<linearGradient id="gCloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A808A"/><stop offset="1" stop-color="#3E434C"/></linearGradient>
<linearGradient id="gUmb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D72B3A"/><stop offset="1" stop-color="#8E1220"/></linearGradient>
</defs></svg>'''

def person(kind, x, y, s=1.0, outfit=None, extra='', mood='smile', arm=None):
    P = {
        'john':  dict(hair=('side', '#5A3A22'), top='#B3202A', bottom='#2E3440'),
        'jake':  dict(hair=('side', '#5A3A22'), top='#8C939C', bottom='#3B4048'),
        'emma':  dict(hair=('long', '#A0522D'), top='#E8E4DA', bottom='#5B2A3A'),
        'lily':  dict(hair=('pony', '#7A4A26'), top='#C62D3A', bottom='#3E5C76'),
        'max':   dict(hair=('short', '#7A4A26'), top='#2F6E4C', bottom='#2E3440'),
        'mehar': dict(hair=('turban', '#1E3F7A'), top='#1F2A44', bottom='#1F2A44', acc=['tie','beard']),
        'david': dict(hair=('short', '#9A8F86'), top='#5E6B78', bottom='#2E3440', acc=['glasses', 'tie']),
        'sarah': dict(hair=('bun', '#2A1A12'), top='#6B1F2A', bottom='#2B2B33'),
        'raj':   dict(hair=('short', '#1E1A18'), top='#FAFAFA', bottom='#2E3440', acc=['coat']),
    }[kind].copy()
    P['acc'] = list(P.get('acc', []))
    if outfit == 'coat': P['acc'].append('coat')
    if outfit == 'old': P['hair'] = ('grey', '#D9D9D9'); P['acc'].append('cane')
    sk = SKIN[kind]; hs, hc = P['hair']; top, bot = P['top'], P['bottom']
    g = ['<ellipse cx="0" cy="3" rx="50" ry="8" fill="rgba(0,0,0,.28)"/>']
    # legs + shoes
    g.append(f'<path d="M-25,-84 L-6,-84 L-7,-6 L-23,-6Z" fill="{bot}"/><path d="M6,-84 L25,-84 L23,-6 L7,-6Z" fill="{bot}"/>')
    g.append('<path d="M-25,-84 L-6,-84 L-7,-6 L-23,-6Z M6,-84 L25,-84 L23,-6 L7,-6Z" fill="url(#gShade)"/>')
    g.append('<path d="M-30,0 C-30,-10 -6,-12 -5,-4 L-5,0Z" fill="#231C18"/><path d="M30,0 C30,-10 6,-12 5,-4 L5,0Z" fill="#231C18"/>')
    g.append('<path d="M-28,-6 C-22,-9 -12,-9 -8,-7" stroke="rgba(255,255,255,.25)" stroke-width="2" fill="none"/>')
    # arms
    la = '<path d="M-38,-158 C-52,-150 -56,-118 -54,-86" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/>'
    ra = '<path d="M38,-158 C52,-150 56,-118 54,-86" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/>'
    if arm == 'up':   ra = '<path d="M38,-158 C56,-170 64,-200 60,-232" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/>'
    if arm == 'hold': ra = '<path d="M38,-158 C56,-150 62,-128 50,-118" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round"/>'
    g.append(la.format(c=top) + ra.format(c=top))
    hands = [(-54, -82)] + ([(60, -238)] if arm == 'up' else [(48, -116)] if arm == 'hold' else [(54, -82)])
    for hx, hy in hands: g.append(f'<circle cx="{hx}" cy="{hy}" r="9.5" fill="{sk}"/>')
    # torso
    g.append(f'<path d="M-40,-150 C-40,-166 -26,-170 0,-170 C26,-170 40,-166 40,-150 L38,-78 C20,-72 -20,-72 -38,-78Z" fill="{top}"/>')
    g.append('<path d="M-40,-150 C-40,-166 -26,-170 0,-170 C26,-170 40,-166 40,-150 L38,-78 C20,-72 -20,-72 -38,-78Z" fill="url(#gShade)"/>')
    g.append(f'<path d="M-38,-82 C-20,-76 20,-76 38,-82 L38,-76 C20,-70 -20,-70 -38,-76Z" fill="rgba(0,0,0,.22)"/>')
    if 'coat' in P['acc']:
        g.append('<path d="M-42,-152 C-42,-166 -28,-171 -10,-171 L0,-132 L10,-171 C28,-171 42,-166 42,-152 L43,-66 L-43,-66Z" fill="#FBFBFB"/>'
                 '<path d="M-42,-152 C-42,-166 -28,-171 -10,-171 L0,-132 L10,-171 C28,-171 42,-166 42,-152 L43,-66 L-43,-66Z" fill="url(#gShade)"/>'
                 '<path d="M0,-132 L0,-66" stroke="#D8D8D8" stroke-width="2"/><rect x="18" y="-140" width="14" height="10" rx="2" fill="#CFE3F0"/>'
                 '<path d="M-14,-152 C-26,-118 -6,-102 6,-110" fill="none" stroke="#3E4B5B" stroke-width="3"/><circle cx="7" cy="-109" r="5" fill="#9AA6B2"/>')
    if 'tie' in P['acc']:
        g.append('<path d="M-13,-170 L0,-150 L13,-170Z" fill="#FAFAFA"/><path d="M-4,-154 L4,-154 L7,-112 L0,-102 L-7,-112Z" fill="#C9A227"/>'
                 '<path d="M-24,-168 L-8,-150 L-14,-120Z M24,-168 L8,-150 L14,-120Z" fill="rgba(0,0,0,.18)"/>')
    else:
        g.append(f'<path d="M-12,-170 Q0,-158 12,-170" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3"/>')
    # neck, ears, head
    g.append(f'<rect x="-9" y="-182" width="18" height="16" fill="{sk}"/><rect x="-9" y="-176" width="18" height="6" fill="rgba(0,0,0,.12)"/>')
    g.append(f'<ellipse cx="-33" cy="-198" rx="6" ry="9" fill="{sk}"/><ellipse cx="33" cy="-198" rx="6" ry="9" fill="{sk}"/>')
    g.append(f'<ellipse cx="0" cy="-200" rx="33" ry="36" fill="{sk}"/><ellipse cx="0" cy="-200" rx="33" ry="36" fill="url(#gFace)"/>')
    g.append(hair(hs, hc))
    # face
    brow = '#3A2A20' if hs != 'grey' else '#BDBDBD'
    by = -214 if mood != 'shock' else -220
    g.append(f'<path d="M-19,{by} Q-12,{by-4} -5,{by}" stroke="{brow}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M5,{by} Q12,{by-4} 19,{by}" stroke="{brow}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    er = 5.5 if mood == 'shock' else 4.4
    g.append(f'<ellipse cx="-12" cy="-202" rx="{er+1.6}" ry="{er+2}" fill="#fff"/><ellipse cx="12" cy="-202" rx="{er+1.6}" ry="{er+2}" fill="#fff"/>')
    g.append(f'<circle cx="-11" cy="-201" r="{er-.6}" fill="#2b2420"/><circle cx="13" cy="-201" r="{er-.6}" fill="#2b2420"/><circle cx="-9.5" cy="-203" r="1.3" fill="#fff"/><circle cx="14.5" cy="-203" r="1.3" fill="#fff"/>')
    g.append('<path d="M0,-198 Q-4,-188 1,-186" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="2.4" stroke-linecap="round"/>')
    g.append('<ellipse cx="-21" cy="-186" rx="6" ry="4" fill="#E8838A" opacity=".45"/><ellipse cx="21" cy="-186" rx="6" ry="4" fill="#E8838A" opacity=".45"/>')
    if mood == 'shock':
        g.append('<ellipse cx="0" cy="-178" rx="7" ry="9" fill="#5A2018"/><ellipse cx="0" cy="-175" rx="4" ry="3" fill="#C85A5A"/>')
    elif mood == 'sad':
        g.append('<path d="M-9,-176 Q0,-183 9,-176" fill="none" stroke="#7A3B2E" stroke-width="2.6" stroke-linecap="round"/>')
    else:
        g.append('<path d="M-11,-182 Q0,-171 11,-182 Q0,-177 -11,-182Z" fill="#7A3B2E"/><path d="M-7,-180 Q0,-176 7,-180" fill="#fff"/>')
    if 'beard' in P['acc']:
        g.append('<path d="M-33,-204 C-34,-178 -22,-160 0,-156 C22,-160 34,-178 33,-204 C29,-190 20,-182 0,-180 C-20,-182 -29,-190 -33,-204Z" fill="#141210"/>'
                 '<path d="M-20,-186 C-12,-192 -4,-190 0,-186 C4,-190 12,-192 20,-186 C14,-180 6,-182 0,-184 C-6,-182 -14,-180 -20,-186Z" fill="#141210"/>')
    if 'glasses' in P['acc']:
        g.append('<circle cx="-12" cy="-202" r="10" fill="rgba(255,255,255,.1)" stroke="#333" stroke-width="2.4"/><circle cx="12" cy="-202" r="10" fill="rgba(255,255,255,.1)" stroke="#333" stroke-width="2.4"/><path d="M-2,-202 L2,-202" stroke="#333" stroke-width="2.4"/>')
    if 'cane' in P['acc']:
        g.append('<path d="M62,0 L62,-80 Q62,-94 50,-94" fill="none" stroke="#6B4A2E" stroke-width="6" stroke-linecap="round"/>')
    g.append(extra)
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'

def tree(x, y, s=1.0, lit=True):
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         '<ellipse cx="0" cy="2" rx="120" ry="12" fill="rgba(0,0,0,.25)"/>',
         '<rect x="-14" y="-34" width="28" height="34" fill="#5A3A22"/><rect x="0" y="-34" width="14" height="34" fill="rgba(0,0,0,.25)"/>']
    for k, (w, yb, yt) in enumerate([(120, -26, -110), (96, -88, -168), (72, -150, -222), (46, -204, -268)]):
        o.append(f'<path d="M0,{yt} C{w*.3},{yt+30} {w*.7},{yb-20} {w},{yb} Q{w*.5},{yb-10} 0,{yb-4} Q{-w*.5},{yb-10} {-w},{yb} C{-w*.7},{yb-20} {-w*.3},{yt+30} 0,{yt}Z" fill="url(#gTree)"/>')
        o.append(f'<path d="M{-w},{yb} Q{-w*.5},{yb-10} 0,{yb-4} Q{w*.5},{yb-10} {w},{yb} Q{w*.5},{yb-20} 0,{yb-14} Q{-w*.5},{yb-20} {-w},{yb}Z" fill="#F4F2F8" opacity=".85"/>')
    o.append('<path d="M0,-296 L8,-278 L27,-277 L12,-265 L17,-246 L0,-257 L-17,-246 L-12,-265 L-27,-277 L-8,-278Z" fill="#F2CC5A" style="filter:drop-shadow(0 0 8px #F2CC5A)"/>')
    if lit:
        pts = [(-34,-186),(30,-176),(-60,-126),(56,-118),(0,-140),(-86,-60),(84,-54),(-24,-70),(34,-64),(0,-210),(-14,-110),(18,-238)]
        for i, (ox, oy) in enumerate(pts):
            c = ['#FF4D5E', '#FFD27A', '#E9EEF6', '#7FE0A8'][i % 4]
            o.append(f'<circle class="tw" style="animation-delay:{i*0.31:.2f}s;filter:drop-shadow(0 0 5px {c})" cx="{ox}" cy="{oy}" r="7" fill="{c}"/>')
    o.append('</g>')
    return ''.join(o)

def house(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="70" y="-250" width="30" height="70" fill="#7A2A22"/><path d="M66,-252 L104,-252 L104,-244 L66,-244Z" fill="#F4F2F8"/>'
            '<rect x="-120" y="-150" width="240" height="150" fill="url(#gWall)"/>'
            '<path d="M-150,-148 L0,-262 L150,-148 L138,-140 L0,-246 L-138,-140Z" fill="#8E1A24"/>'
            '<path d="M-152,-150 L0,-266 L152,-150 L140,-150 L0,-254 L-140,-150Z" fill="#F4F2F8"/>'
            '<rect x="-92" y="-122" width="72" height="62" fill="url(#gGlass)" stroke="#5A3A22" stroke-width="5"/><path d="M-56,-122 L-56,-60 M-92,-91 L-20,-91" stroke="#5A3A22" stroke-width="4"/>'
            '<rect x="22" y="-122" width="72" height="62" fill="url(#gGlass)" stroke="#5A3A22" stroke-width="5"/><path d="M58,-122 L58,-60 M22,-91 L94,-91" stroke="#5A3A22" stroke-width="4"/>'
            '<rect x="-18" y="-76" width="36" height="76" fill="#7A0F1A"/><circle cx="10" cy="-38" r="3" fill="#F2CC5A"/>'
            '<circle cx="0" cy="-100" r="15" fill="none" stroke="#2F6E4C" stroke-width="7"/><circle cx="0" cy="-86" r="4" fill="#D11F2E"/>'
            + ''.join(f'<circle class="tw" style="animation-delay:{k*.2:.1f}s" cx="{-140+k*28}" cy="{-147+abs(k-5)*0}" r="4" fill="{["#FF4D5E","#FFD27A","#7FE0A8"][k%3]}"/>' for k in range(11))
            + '<path d="M-120,0 L120,0 L130,8 L-130,8Z" fill="#F4F2F8"/></g>')

def clinic(x, y, s=1.0, n=1):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<ellipse cx="0" cy="4" rx="130" ry="10" fill="rgba(0,0,0,.25)"/>'
            '<rect x="-112" y="-176" width="224" height="176" fill="url(#gWall)"/><rect x="40" y="-176" width="72" height="176" fill="rgba(0,0,0,.08)"/>'
            '<rect x="-122" y="-196" width="244" height="24" fill="#F4F2F8"/><rect x="-122" y="-176" width="244" height="6" fill="rgba(0,0,0,.12)"/>'
            '<rect x="-80" y="-168" width="160" height="28" rx="4" fill="#7A0F1A"/>'
            f'<text x="0" y="-148" text-anchor="middle" style="fill:#F7E7C6;font:700 14px Georgia,serif;letter-spacing:.1em">SMILE DENTAL{" #"+str(n) if n>1 else ""}</text>'
            '<rect x="-92" y="-126" width="62" height="52" fill="url(#gGlass)" stroke="#5E6B78" stroke-width="5"/><path d="M-61,-126 L-61,-74" stroke="#5E6B78" stroke-width="3"/>'
            '<rect x="30" y="-126" width="62" height="52" fill="url(#gGlass)" stroke="#5E6B78" stroke-width="5"/><path d="M61,-126 L61,-74" stroke="#5E6B78" stroke-width="3"/>'
            '<path d="M-96,-130 L-26,-130 L-30,-120 L-92,-120Z M26,-130 L96,-130 L92,-120 L30,-120Z" fill="#9E1B26"/>'
            '<rect x="-22" y="-84" width="44" height="84" fill="#3E4B5B"/><rect x="-16" y="-78" width="32" height="42" fill="url(#gGlass)" opacity=".8"/>'
            '<path d="M-24,-104 C-24,-116 -10,-120 0,-110 C10,-120 24,-116 24,-104 C24,-94 14,-90 10,-86 L6,-92 L0,-88 L-6,-92 L-10,-86 C-14,-90 -24,-94 -24,-104Z" fill="#FFFFFF" stroke="#9AA6B2" stroke-width="2" transform="translate(0,-4) scale(.62)"/>'
            '<path d="M-112,0 L112,0 L122,8 L-122,8Z" fill="#F4F2F8"/></g>')

def ground(w=1300, y=470):
    return (f'<path d="M0,{y} Q{w*.25},{y-26} {w*.5},{y-6} T{w},{y-14} L{w},{y+80} L0,{y+80}Z" fill="url(#gSnow)"/>'
            f'<path d="M0,{y+12} Q{w*.3},{y-6} {w*.6},{y+8} T{w},{y+2}" fill="none" stroke="rgba(150,140,180,.35)" stroke-width="3"/>')

def umbrella(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M-150,0 C-140,-90 -60,-130 0,-130 C60,-130 140,-90 150,0 C130,-14 110,-14 90,0 C70,-14 50,-14 30,0 C10,-14 -10,-14 -30,0 C-50,-14 -70,-14 -90,0 C-110,-14 -130,-14 -150,0Z" fill="url(#gUmb)"/>'
            '<path d="M0,-130 C-30,-90 -50,-50 -90,0 M0,-130 C30,-90 50,-50 90,0 M0,-130 L-30,0 M0,-130 L30,0" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3"/>'
            '<path d="M-150,0 C-140,-90 -60,-130 0,-130" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="4"/>'
            '<circle cx="0" cy="-134" r="6" fill="#3A2A20"/><path d="M0,0 L0,150 Q0,168 -16,168 Q-28,168 -28,156" fill="none" stroke="#3A2A20" stroke-width="7" stroke-linecap="round"/></g>')

def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<circle cx="-90" cy="10" r="58" fill="url(#gCloud)"/><circle cx="-20" cy="-26" r="78" fill="url(#gCloud)"/><circle cx="66" cy="-6" r="66" fill="url(#gCloud)"/><circle cx="130" cy="20" r="46" fill="url(#gCloud)"/>'
            '<rect x="-148" y="10" width="324" height="58" rx="29" fill="#3E434C"/>'
            '<circle cx="-30" cy="-50" r="40" fill="rgba(255,255,255,.08)"/></g>')
