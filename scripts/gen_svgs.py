"""Generate the themed SVG panels used in the profile README.

Fonts are embedded as base64 so they render inside GitHub's <img> sandbox.
Usage: python scripts/gen_svgs.py <fonts_dir>
"""
import base64, os, sys
from html import escape

FONTS_DIR = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "hud")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#0F1B3D", "#14204A", "#34478A"
SILVER, STEEL, DIM, BLUE = "#FFFFFF", "#7DD3FC", "#A5B4FC", "#818CF8"
RARITY = {"LEGENDARY": "#C084FC", "EPIC": "#7C8CFF", "RARE": "#38BDF8", "COMMON": "#9CA3AF"}

def _font(fam, file):
    b = base64.b64encode(open(os.path.join(FONTS_DIR, file), "rb").read()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');}}"

FONTS = {
    "orb": _font("Orb", "bebas-neue-latin-400-normal.woff2"),
    "orb7": _font("Orb7", "exo-2-latin-800-normal.woff2"),
    "raj": _font("Raj", "exo-2-latin-600-normal.woff2"),
    "mono": _font("Mono", "jetbrains-mono-latin-500-normal.woff2"),
}

def svg(name, w, h, body, fonts=("orb", "raj", "mono"), css=""):
    style = "".join(FONTS[f] for f in fonts) + """
      .orb{font-family:'Orb',sans-serif}.orb7{font-family:'Orb7',sans-serif}
      .raj{font-family:'Raj',sans-serif}.mono{font-family:'Mono',monospace}
      @keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
      @keyframes fadeUp{from{opacity:0}to{opacity:1}}
      .blink{animation:blink 1.1s steps(1) infinite}
      .fade{opacity:0;animation:fadeUp .7s ease-out forwards}
    """ + css
    out = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{style}</style>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".05"/></pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity="0"/></pattern>
  <linearGradient id="panelg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1B2A63"/><stop offset="1" stop-color="#121C45"/></linearGradient>
  <linearGradient id="herog" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E1B4B"/><stop offset=".5" stop-color="#1E3A8A"/><stop offset="1" stop-color="#0E7490"/></linearGradient>
  <linearGradient id="steel" x1="0" x2="1"><stop offset="0" stop-color="{STEEL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E0E7FF"/></linearGradient>
</defs>
{body}
</svg>"""
    open(os.path.join(OUT, name), "w").write(out)

def frame(w, h, r=14):
    c = 18  # corner bracket length
    br = "".join(f'<path d="{d}" stroke="{STEEL}" stroke-width="2" fill="none"/>' for d in [
        f"M8 {8+c}V8H{8+c}", f"M{w-8-c} 8H{w-8}V{8+c}", f"M8 {h-8-c}V{h-8}H{8+c}", f"M{w-8-c} {h-8}H{w-8}V{h-8-c}"])
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#panelg)" stroke="{LINE}"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#grid)"/>' + br)

# ---------------------------------------------------------------- HERO
def hero():
    w, h = 1200, 360
    # abstract night skyline
    import random; random.seed(7)
    x, sky = 0, ""
    while x < w:
        bw, bh = random.randint(40, 90), random.randint(40, 110)
        sky += f'<rect x="{x}" y="{h-bh}" width="{bw}" height="{bh}" fill="#1A2A5E"/>'
        for wy in range(h - bh + 12, h - 10, 18):
            for wx in range(x + 8, x + bw - 8, 14):
                if random.random() < .12:
                    sky += f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="{STEEL}" opacity=".35"/>'
        x += bw + random.randint(2, 8)
    body = f"""
<rect width="{w}" height="{h}" rx="16" fill="url(#herog)"/>
<rect width="{w}" height="{h}" rx="16" fill="url(#grid)"/>
<g opacity=".55"><polygon points="600,{h} 380,0 820,0" fill="url(#beam)">
  <animateTransform attributeName="transform" type="rotate" values="-14 600 {h};14 600 {h};-14 600 {h}" dur="9s" repeatCount="indefinite"/></polygon></g>
<defs><linearGradient id="beam" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="#BAE6FD" stop-opacity=".45"/><stop offset="1" stop-color="#C9D1D9" stop-opacity="0"/></linearGradient></defs>
{sky}
<rect width="{w}" height="{h}" rx="16" fill="url(#scan)"/>
<text x="600" y="62" text-anchor="middle" class="mono fade" font-size="14" fill="{DIM}" letter-spacing="6" style="animation-delay:.1s">&gt; INCOMING SIGNAL · GOTHAM NETWORK</text>
<text x="600" y="150" text-anchor="middle" class="orb fade" font-size="94" fill="url(#chrome)" letter-spacing="8" style="animation-delay:.3s">YASHWANTH</text>
<text x="600" y="192" text-anchor="middle" class="raj fade" font-size="24" fill="{STEEL}" letter-spacing="10" style="animation-delay:.6s">AI DEVELOPER · AGENTIC SYSTEMS · RAG</text>
<g class="fade" style="animation-delay:.9s">
  <rect x="470" y="222" width="260" height="40" rx="4" fill="none" stroke="{STEEL}" stroke-opacity=".6"/>
  <text x="600" y="248" text-anchor="middle" class="orb7 blink" font-size="15" fill="{SILVER}" letter-spacing="6">▶ PRESS START</text>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none" stroke="{LINE}"/>"""
    svg("hero.svg", w, h, body, fonts=("orb", "orb7", "raj", "mono"))

# ---------------------------------------------------------------- HUD
def bar(x, y, wid, pct, label, val, delay, color="url(#steel)"):
    seg = ""
    n = 24
    sw = (wid - (n - 1) * 3) / n
    for i in range(n):
        on = i < round(n * pct)
        seg += (f'<rect x="{x + i*(sw+3):.1f}" y="{y}" width="{sw:.1f}" height="12" rx="1.5" '
                f'fill="{color if on else "#26346B"}" class="{"fade" if on else ""}" '
                f'style="animation-delay:{delay + i*0.035:.2f}s"/>')
    return (f'<text x="{x}" y="{y-8}" class="orb7" font-size="12" fill="{DIM}" letter-spacing="3">{label}</text>'
            f'<text x="{x+wid}" y="{y-8}" text-anchor="end" class="mono" font-size="13" fill="{SILVER}">{val}</text>' + seg)

def hud():
    w, h = 1200, 300
    stats = [("AGENTIC AI / RAG", .90, "90"), ("DOCUMENT INTEL", .85, "85"),
             ("BACKEND SYSTEMS", .80, "80"), ("FULL-STACK WEB", .70, "70")]
    right = "".join(bar(780, 70 + i * 56, 370, p, l, v, .4 + i * .2) for i, (l, p, v) in enumerate(stats))
    import math
    r, c = 62, 2 * math.pi * 62
    body = f"""{frame(w, h)}
<text x="40" y="44" class="mono" font-size="13" fill="{DIM}" letter-spacing="4">// PLAYER_01</text>
<g transform="translate(120,165)">
  <circle r="{r}" fill="none" stroke="#26346B" stroke-width="10"/>
  <circle r="{r}" fill="none" stroke="url(#steel)" stroke-width="10" stroke-linecap="round"
          stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" transform="rotate(-90)">
    <animate attributeName="stroke-dashoffset" from="{c:.1f}" to="{c*0.26:.1f}" dur="1.6s" fill="freeze"/></circle>
  <text y="-20" text-anchor="middle" class="orb7" font-size="12" fill="{DIM}" letter-spacing="3">LEVEL</text>
  <text y="34" text-anchor="middle" class="orb" font-size="54" fill="url(#chrome)">22</text>
</g>
<text x="215" y="110" class="orb" font-size="45" fill="url(#chrome)" letter-spacing="3">ATHOTA YASHWANTH</text>
<text x="217" y="142" class="raj" font-size="20" fill="{STEEL}" letter-spacing="4">CLASS · AI DEVELOPER</text>
<g class="raj" font-size="17" fill="{SILVER}">
  <text x="217" y="182"><tspan fill="{DIM}">GUILD   </tspan>OMICS International</text>
  <text x="217" y="208"><tspan fill="{DIM}">BASE    </tspan>Hyderabad, IN</text>
  <text x="217" y="234"><tspan fill="{DIM}">ORIGIN  </tspan>B.Tech CSE (AI &amp; ML) · 2026</text>
</g>
<g transform="translate(217,256)">
  <circle cx="6" cy="0" r="5" fill="#3FB950"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="20" y="5" class="mono" font-size="13" fill="{SILVER}" letter-spacing="2">ONLINE · ON PATROL</text>
</g>
<line x1="740" y1="40" x2="740" y2="260" stroke="{LINE}"/>
{right}
<text x="1150" y="276" text-anchor="end" class="mono" font-size="12" fill="{DIM}">XP 7,400 / 10,000 → SENIOR DEV</text>"""
    svg("hud.svg", w, h, body, fonts=("orb", "orb7", "raj", "mono"))

# ---------------------------------------------------------------- SECTION HEADERS
def header(slug, idx, title, sub):
    w, h = 1200, 84
    body = f"""
<rect width="{w}" height="{h}" fill="none"/>
<text x="4" y="30" class="mono" font-size="14" fill="{DIM}" letter-spacing="4">{idx} //</text>
<text x="4" y="66" class="orb" font-size="40" fill="url(#chrome)" letter-spacing="5">{escape(title)}</text>
<text x="{w-4}" y="66" text-anchor="end" class="raj" font-size="17" fill="{STEEL}" letter-spacing="4">{escape(sub)}</text>
<rect x="4" y="78" width="{w-8}" height="1" fill="{LINE}"/>
<rect x="4" y="77" width="120" height="3" fill="url(#steel)">
  <animate attributeName="x" values="4;{w-124};4" dur="7s" repeatCount="indefinite"/></rect>"""
    svg(f"h-{slug}.svg", w, h, body, fonts=("orb", "raj", "mono"))

# ---------------------------------------------------------------- PROJECT CARDS
def card(slug, rank, title, line1, line2, tags, rarity):
    w, h = 590, 210
    col = RARITY[rarity]
    tx, chips = 34, ""
    for t in tags:
        tw = len(t) * 8.4 + 22
        chips += (f'<rect x="{tx}" y="160" width="{tw}" height="26" rx="13" fill="#1C2A5C" stroke="{LINE}"/>'
                  f'<text x="{tx+tw/2}" y="178" text-anchor="middle" class="mono" font-size="13" fill="{SILVER}">{escape(t)}</text>')
        tx += tw + 8
    body = f"""{frame(w, h)}
<rect x="1" y="1" width="6" height="{h-2}" rx="3" fill="{col}"/>
<text x="34" y="44" class="mono" font-size="12" fill="{col}" letter-spacing="3">◆ {rarity}</text>
<g transform="translate({w-82},22)">
  <rect width="56" height="56" rx="8" fill="#1C2A5C" stroke="{col}" stroke-opacity=".7"/>
  <text x="28" y="40" text-anchor="middle" class="orb" font-size="40" fill="url(#chrome)">{rank}</text></g>
<text x="34" y="84" class="orb" font-size="37" fill="url(#chrome)" letter-spacing="2">{escape(title)}</text>
<text x="34" y="116" class="raj" font-size="18" fill="{SILVER}">{escape(line1)}</text>
<text x="34" y="140" class="raj" font-size="18" fill="{DIM}">{escape(line2)}</text>
{chips}"""
    svg(f"card-{slug}.svg", w, h, body, fonts=("orb", "raj", "mono"))

# ---------------------------------------------------------------- QUESTS
def quests():
    rows = [("ACTIVE", "Self-Corrective RAG", 0.8), ("ACTIVE", "Multi-Modal Chunking", 0.7),
            ("ACTIVE", "Voice-Driven Coding Agent", 0.6), ("LOCKED", "Graph RAG · Neo4j", 0.2),
            ("LOCKED", "Multi-Agent Orchestration", 0.15)]
    w, h = 1200, 60 + len(rows) * 52
    body = frame(w, h)
    for i, (st, name, p) in enumerate(rows):
        y = 50 + i * 52
        active = st == "ACTIVE"
        chip = "#1F6FEB" if active else "#30363D"
        body += f"""
<g class="fade" style="animation-delay:{.15*i:.2f}s">
  <rect x="34" y="{y}" width="96" height="28" rx="4" fill="{chip}" fill-opacity=".25" stroke="{chip}"/>
  <text x="82" y="{y+19}" text-anchor="middle" class="orb7" font-size="11" fill="{SILVER}" letter-spacing="2">{'▶ ' if active else '🔒 '}{st}</text>
  <text x="156" y="{y+21}" class="raj" font-size="21" fill="{SILVER if active else DIM}">{escape(name)}</text>
  <rect x="760" y="{y+9}" width="340" height="10" rx="5" fill="#26346B"/>
  <rect x="760" y="{y+9}" width="0" height="10" rx="5" fill="url(#steel)">
    <animate attributeName="width" from="0" to="{340*p:.0f}" begin="{.3+.15*i:.2f}s" dur="1.2s" fill="freeze"/></rect>
  <text x="1166" y="{y+19}" text-anchor="end" class="mono" font-size="14" fill="{SILVER}">{int(p*100)}%</text>
</g>"""
    svg("quests.svg", w, h, body, fonts=("orb7", "raj", "mono"))

# ---------------------------------------------------------------- GADGETS
def gadgets():
    items = [("GRAPNEL", "Hybrid Search", "LEGENDARY", "⟟"), ("SCANNER", "AST Extraction", "EPIC", "◎"),
             ("ARMOR", "CRAG Grader", "LEGENDARY", "⬢"), ("SPLITTER", "Multi-modal Chunker", "EPIC", "⧉"),
             ("COWL LOCK", "JWT + RBAC", "RARE", "⊠"), ("CONTAINMENT", "Docker", "RARE", "▣")]
    w, h = 1200, 250
    tw, gap = 176, 16
    body = frame(w, h)
    for i, (n, d, r, g) in enumerate(items):
        x, col = 34 + i * (tw + gap), RARITY[r]
        body += f"""
<g class="fade" style="animation-delay:{.12*i:.2f}s">
  <rect x="{x}" y="40" width="{tw}" height="172" rx="10" fill="#182557" stroke="{col}" stroke-opacity=".55"/>
  <rect x="{x}" y="40" width="{tw}" height="172" rx="10" fill="{col}" fill-opacity=".05"/>
  <text x="{x+14}" y="62" class="mono" font-size="12" fill="{DIM}">SLOT {i+1:02d}</text>
  <text x="{x+tw/2}" y="122" text-anchor="middle" font-size="46" fill="{col}" font-family="DejaVu Sans,Segoe UI Symbol,sans-serif">{g}</text>
  <text x="{x+tw/2}" y="160" text-anchor="middle" class="orb" font-size="18" fill="url(#chrome)" letter-spacing="2">{n}</text>
  <text x="{x+tw/2}" y="182" text-anchor="middle" class="raj" font-size="16" fill="{SILVER}">{escape(d)}</text>
  <rect x="{x+14}" y="194" width="{tw-28}" height="4" rx="2" fill="{col}"/>
</g>"""
    svg("gadgets.svg", w, h, body, fonts=("orb", "raj", "mono"))

# ---------------------------------------------------------------- FOOTER
def footer():
    w, h = 1200, 150
    body = f"""
<rect width="{w}" height="{h}" rx="16" fill="url(#herog)"/><rect width="{w}" height="{h}" rx="16" fill="url(#grid)"/>
<rect width="{w}" height="{h}" rx="16" fill="url(#scan)"/>
<text x="600" y="66" text-anchor="middle" class="orb" font-size="40" fill="url(#chrome)" letter-spacing="10">GAME SAVED</text>
<text x="600" y="104" text-anchor="middle" class="mono" font-size="16" fill="{STEEL}" letter-spacing="4">CONTINUE? <tspan fill="{SILVER}">[ Y ]</tspan> / N<tspan class="blink" fill="{SILVER}"> ▌</tspan></text>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none" stroke="{LINE}"/>"""
    svg("footer.svg", w, h, body, fonts=("orb", "mono"))

hero(); hud(); quests(); gadgets(); footer()
for a in [("profile", "01", "PLAYER PROFILE", "STATUS SCREEN"),
          ("quests", "02", "ACTIVE QUESTS", "MISSION BOARD"),
          ("cases", "03", "CASE FILES", "FEATURED PROJECTS"),
          ("gadgets", "04", "UTILITY BELT", "GADGETS & STACK"),
          ("trophies", "05", "TROPHY ROOM", "ACHIEVEMENTS"),
          ("telemetry", "06", "BATCOMPUTER", "LIVE TELEMETRY")]:
    header(*a)
card("halo", "S", "HALO", "Self-correcting PDF Q&A agent", "Citations · confidence scores · web fallback",
     ["Python", "LangGraph", "ChromaDB"], "LEGENDARY")
card("voxcode", "S", "VOXCODE", "Voice-driven AI coding agent", "AST search · planning loop · live diffs",
     ["Python", "Hybrid RAG", "STT/TTS"], "LEGENDARY")
card("omnichunk", "A", "OMNICHUNK", "Multi-modal chunking engine", "Structure-aware · zero information loss",
     ["Python", "Multi-modal"], "EPIC")
card("pulsus", "A", "PULSUS-REGAIN", "Cinematic 3D portfolio + outreach", "Real-time spatial visualisation",
     ["JavaScript", "Three.js"], "EPIC")
card("omniscout", "A", "OMNISCOUT", "Biomedical literature intelligence", "55 sources · PDF extraction · Excel export",
     ["FastAPI", "Data"], "EPIC")
card("booking", "B", "BOOKING-API", "Concurrency-safe REST API", "RBAC · JWT · pessimistic locking",
     ["Spring Boot", "Java"], "RARE")
print("ok", sorted(os.listdir(OUT)))
