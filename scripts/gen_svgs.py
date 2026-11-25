"""Generate the cinematic SVG panels used in the profile README.

Fonts are embedded as base64 so they render inside GitHub's <img> sandbox.
Usage: python scripts/gen_svgs.py <fonts_dir>
"""
import base64, os, sys, shutil
from html import escape

FONTS_DIR = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "hud")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

INK, LINE = "#0A0A0B", "#2A2A2E"
WHITE, SOFT, DIM, RED = "#F5F5F4", "#D4D4D8", "#8A8A93", "#E11D2E"

def _font(fam, file):
    b = base64.b64encode(open(os.path.join(FONTS_DIR, file), "rb").read()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');}}"

FONTS = {
    "anton": _font("Anton", "anton-latin-400-normal.woff2"),
    "inter": _font("Inter", "inter-latin-500-normal.woff2"),
    "interb": _font("InterB", "inter-latin-700-normal.woff2"),
}

def svg(name, w, h, body, fonts=("anton", "inter", "interb")):
    style = "".join(FONTS[f] for f in fonts) + """
      .t{font-family:'Anton',Impact,sans-serif}.b{font-family:'Inter',sans-serif}.bb{font-family:'InterB',sans-serif}
      @keyframes in{from{opacity:0}to{opacity:1}}
      @keyframes rise{from{opacity:0;letter-spacing:40px}to{opacity:1}}
      .in{opacity:0;animation:in 1.2s ease-out forwards}
    """
    open(os.path.join(OUT, name), "w").write(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{style}</style>
<defs>
  <radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset="0" stop-color="#1C1C20"/><stop offset="1" stop-color="{INK}"/></radialGradient>
  <radialGradient id="glow" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="{RED}" stop-opacity=".28"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
  <linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18181B"/><stop offset="1" stop-color="#101012"/></linearGradient>
  <linearGradient id="titleg" x1="0" x2="1" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#F5F5F4"/>
    <stop offset="0" stop-color="#F5F5F4"><animate attributeName="offset" values="-.3;1.1" dur="5s" repeatCount="indefinite"/></stop>
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"><animate attributeName="offset" values="-.2;1.2" dur="5s" repeatCount="indefinite"/></stop>
    <stop offset="0" stop-color="#C7C7CC"><animate attributeName="offset" values="-.15;1.25" dur="5s" repeatCount="indefinite"/></stop>
    <stop offset="0" stop-color="#F5F5F4"><animate attributeName="offset" values="-.1;1.3" dur="5s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="#F5F5F4"/></linearGradient>
  <radialGradient id="cglow" cx="1" cy="0" r=".8"><stop offset="0" stop-color="{RED}" stop-opacity=".22"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}" stop-opacity=".12"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <linearGradient id="redbar" x1="0" x2="1"><stop offset="0" stop-color="#9F1239"/><stop offset="1" stop-color="{RED}"/></linearGradient>
</defs>
{body}
</svg>""")

import random
def rain(w, h, n=70, seed=3):
    random.seed(seed); out = '<g stroke="#FFFFFF" stroke-linecap="round">'
    for _ in range(n):
        x, y0, L = random.uniform(0, w + 200), random.uniform(-h, 0), random.uniform(14, 34)
        d, o = random.uniform(.7, 1.4), random.uniform(.06, .22)
        out += (f'<line x1="{x:.0f}" y1="{y0:.0f}" x2="{x-L*.35:.0f}" y2="{y0+L:.0f}" stroke-opacity="{o:.2f}" stroke-width="1.2">'
                f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-h*.35:.0f} {h*1.6:.0f}" '
                f'dur="{d:.2f}s" begin="-{random.uniform(0, d):.2f}s" repeatCount="indefinite"/></line>')
    return out + '</g>'

def skyline(w, h, seed=11):
    random.seed(seed); x, out = 0, ''
    while x < w:
        bw, bh = random.randint(30, 80), random.randint(16, 52)
        out += f'<rect x="{x}" y="{h-bh}" width="{bw}" height="{bh}" fill="#060607"/>'
        if random.random() < .25:
            out += f'<rect x="{x+bw/2-1}" y="{h-bh-18}" width="2" height="18" fill="#060607"/>'
        for wy in range(h - bh + 8, h - 6, 12):
            for wx in range(x + 6, x + bw - 6, 10):
                if random.random() < .06:
                    out += f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="#E11D2E" opacity=".55"/>'
        x += bw + random.randint(0, 4)
    return out

BAT = "M0 0 C-6 -8 -14 -8 -22 -2 C-17 -2 -15 1 -14 4 C-11 1 -7 2 -5 5 C-3 2 -1 1 0 3 C1 1 3 2 5 5 C7 2 11 1 14 4 C15 1 17 -2 22 -2 C14 -8 6 -8 0 0Z"
def bats(w, h, n=7, seed=5):
    random.seed(seed); out = ""
    for i in range(n):
        y, sc, d = random.uniform(60, 220), random.uniform(1.1, 2.0), random.uniform(10, 18)
        dy = random.uniform(-40, 40)
        out += (f'<g opacity=".9"><g>'
                f'<animateTransform attributeName="transform" type="translate" values="-60 {y:.0f};{w/2:.0f} {y+dy:.0f};{w+60} {y:.0f}" '
                f'dur="{d:.1f}s" begin="-{random.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
                f'<g transform="scale({sc:.2f})"><path d="{BAT}" fill="#000000" stroke="#E11D2E" stroke-opacity=".35" stroke-width=".6">'
                f'<animateTransform attributeName="transform" type="scale" values="1 1;1 .45;1 1" dur="{random.uniform(.25,.4):.2f}s" repeatCount="indefinite"/>'
                f'</path></g></g></g>')
    return out

def hero():
    w, h = 1200, 420
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#vig)"/>
<rect width="{w}" height="{h}" fill="url(#glow)"/>
<g opacity=".16" stroke="{WHITE}">
  <line x1="600" y1="{h}" x2="140" y2="0"><animate attributeName="opacity" values=".2;1;.2" dur="6s" repeatCount="indefinite"/></line>
  <line x1="600" y1="{h}" x2="1060" y2="0"><animate attributeName="opacity" values="1;.2;1" dur="6s" repeatCount="indefinite"/></line>
</g>
{rain(w, h)}
<rect width="{w}" height="{h}" fill="#DDE3FF" opacity="0">
  <animate attributeName="opacity" values="0;0;.16;0;.09;0;0" keyTimes="0;.86;.87;.885;.9;.92;1" dur="9s" repeatCount="indefinite"/></rect>
{bats(w, h)}
<g transform="translate(0,0)">{skyline(w, h)}</g>
<rect width="{w}" height="26" fill="#000"/><rect y="{h-26}" width="{w}" height="26" fill="#000"/>
<text x="600" y="98" text-anchor="middle" class="bb in" font-size="15" fill="{DIM}" letter-spacing="9">A NITRO BUILDS PRODUCTION</text>
<text x="600" y="236" text-anchor="middle" class="t" font-size="150" fill="url(#titleg)" letter-spacing="14"
      style="opacity:0;animation:rise 1.6s cubic-bezier(.2,.7,.2,1) .2s forwards">YASHWANTH</text>
<rect x="520" y="262" width="160" height="4" fill="url(#redbar)" class="in" style="animation-delay:1s">
  <animate attributeName="width" values="160;220;160" dur="4s" begin="1.2s" repeatCount="indefinite"/>
  <animate attributeName="x" values="520;490;520" dur="4s" begin="1.2s" repeatCount="indefinite"/></rect>
<text x="600" y="304" text-anchor="middle" class="bb in" font-size="20" fill="{SOFT}" letter-spacing="7" style="animation-delay:1.2s">AI DEVELOPER  ·  AGENTIC SYSTEMS  ·  RAG ENGINEERING</text>
<text x="600" y="340" text-anchor="middle" class="b in" font-size="13" fill="{DIM}" letter-spacing="5" style="animation-delay:1.6s">OMICS INTERNATIONAL   ·   HYDERABAD   ·   NOW SHOWING</text>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>"""
    svg("hero.svg", w, h, body)

def xp():
    w, h = 1200, 96
    pct = .74
    body = f"""
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#card)" stroke="{LINE}"/>
<text x="36" y="62" class="t" font-size="34" fill="{WHITE}" letter-spacing="2">LVL 22</text>
<text x="170" y="42" class="bb" font-size="12" fill="{DIM}" letter-spacing="3">CLASS</text>
<text x="170" y="64" class="bb" font-size="17" fill="{SOFT}">AI Developer</text>
<rect x="340" y="38" width="640" height="12" rx="6" fill="#232327"/>
<rect x="340" y="38" width="0" height="12" rx="6" fill="url(#redbar)">
  <animate attributeName="width" from="0" to="{640*pct:.0f}" begin=".3s" dur="1.6s" fill="freeze"/></rect>
<g fill="{INK}">{"".join(f'<rect x="{340+640*k/10-1:.0f}" y="38" width="2" height="12"/>' for k in range(1,10))}</g>
<text x="340" y="74" class="b" font-size="13" fill="{DIM}">7,400 / 10,000 XP</text>
<text x="1164" y="42" text-anchor="end" class="bb" font-size="12" fill="{DIM}" letter-spacing="3">NEXT RANK</text>
<text x="1164" y="64" text-anchor="end" class="bb" font-size="17" fill="{SOFT}">Senior Developer</text>"""
    svg("xp.svg", w, h, body)

def header(slug, num, title):
    w, h = 1200, 74
    body = f"""
<text x="0" y="56" class="t" font-size="40" fill="{WHITE}" letter-spacing="4">{escape(title)}</text>
<text x="{w}" y="56" text-anchor="end" class="bb" font-size="14" fill="{RED}" letter-spacing="4">{num}</text>
<rect x="0" y="68" width="{w}" height="1" fill="{LINE}"/>
<rect x="0" y="67" width="64" height="3" fill="url(#redbar)"/>"""
    svg(f"h-{slug}.svg", w, h, body, fonts=("anton", "interb"))

def card(slug, tag, title, desc, stack, idx="01"):
    w, h = 590, 190
    body = f"""
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#card)" stroke="{LINE}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#cglow)"/>
<text x="{w-28}" y="{h-18}" text-anchor="end" class="t" font-size="120" fill="#FFFFFF" fill-opacity=".04">{idx}</text>
<rect x="24" y="0" width="{w-48}" height="3" fill="url(#redbar)"/>
<text x="32" y="46" class="bb" font-size="12" fill="{RED}" letter-spacing="3">{escape(tag)}</text>
<text x="32" y="96" class="t" font-size="42" fill="{WHITE}" letter-spacing="2">{escape(title)}</text>
<text x="32" y="130" class="b" font-size="16" fill="{SOFT}">{escape(desc)}</text>
<text x="32" y="164" class="b" font-size="13" fill="{DIM}" letter-spacing="1">{escape(stack)}</text>
<g transform="translate({w-62},26)"><circle cx="14" cy="14" r="16" fill="none" stroke="{LINE}"/>
<text x="14" y="21" text-anchor="middle" class="b" font-size="18" fill="{SOFT}">→</text></g>"""
    svg(f"card-{slug}.svg", w, h, body)

def footer():
    w, h = 1200, 150
    body = f"""
<clipPath id="fc"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<g clip-path="url(#fc)"><rect width="{w}" height="{h}" fill="url(#vig)"/><rect width="{w}" height="{h}" fill="url(#glow)"/>{rain(w, h, 30, 9)}</g>
<text x="600" y="76" text-anchor="middle" class="t" font-size="38" fill="{WHITE}" letter-spacing="10">TO BE CONTINUED</text>
<rect x="560" y="94" width="80" height="3" fill="url(#redbar)"/>
<text x="600" y="126" text-anchor="middle" class="b" font-size="13" fill="{DIM}" letter-spacing="4">NEXT EPISODE: YOUR PROJECT</text>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>"""
    svg("footer.svg", w, h, body)

def credits():
    w, h = 1200, 300
    rows = [("STARRING", "Python  ·  Rust  ·  Go  ·  TypeScript  ·  Java"),
            ("AI DIRECTION", "PyTorch  ·  TensorFlow  ·  LangChain  ·  LangGraph"),
            ("BACKEND CREW", "FastAPI  ·  Flask  ·  Spring Boot"),
            ("DATA & EFFECTS", "PostgreSQL  ·  MongoDB  ·  Redis  ·  ChromaDB"),
            ("PRODUCTION", "Docker  ·  Git  ·  Postman")]
    body = f"""<clipPath id="cc"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<g clip-path="url(#cc)"><rect width="{w}" height="{h}" fill="url(#vig)"/><rect width="{w}" height="{h}" fill="url(#glow)"/></g>"""
    for i, (role, names) in enumerate(rows):
        y = 64 + i * 50
        body += (f'<g class="in" style="animation-delay:{.25*i:.2f}s">'
                 f'<text x="380" y="{y}" text-anchor="end" class="bb" font-size="13" fill="{RED}" letter-spacing="4">{escape(role)}</text>'
                 f'<text x="420" y="{y+1}" class="t" font-size="24" fill="{WHITE}" letter-spacing="2">{escape(names)}</text></g>')
    body += f'''<rect x="0" y="0" width="220" height="{h}" fill="url(#sweep)" clip-path="url(#cc)">
  <animate attributeName="x" values="-260;{w+40}" dur="5s" repeatCount="indefinite"/></rect>'''
    body += f'<rect x="400" y="40" width="1" height="{h-80}" fill="{LINE}"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>'
    svg("credits.svg", w, h, body)

hero(); xp(); footer(); credits()
for a in [("about", "01", "THE ORIGIN"), ("quests", "02", "CURRENT QUESTS"),
          ("cases", "03", "FEATURED WORK"), ("stack", "04", "ARSENAL"), ("stats", "05", "BY THE NUMBERS")]:
    header(*a)
card("halo", "FLAGSHIP · RAG", "HALO", "Self-correcting PDF Q&A with citations & confidence", "Python · LangGraph · ChromaDB", "01")
card("voxcode", "FLAGSHIP · AGENTS", "VOXCODE", "Voice-driven AI coding agent with live diffs", "Python · Hybrid search · STT/TTS", "02")
card("omnichunk", "DOCUMENT AI", "OMNICHUNK", "Multi-modal chunking with zero information loss", "Python · Multi-modal", "03")
print(sorted(os.listdir(OUT)))
