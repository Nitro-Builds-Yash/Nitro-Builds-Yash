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
  <linearGradient id="redbar" x1="0" x2="1"><stop offset="0" stop-color="#9F1239"/><stop offset="1" stop-color="{RED}"/></linearGradient>
</defs>
{body}
</svg>""")

def hero():
    w, h = 1200, 420
    body = f"""
<rect width="{w}" height="{h}" rx="14" fill="url(#vig)"/>
<rect width="{w}" height="{h}" rx="14" fill="url(#glow)"/>
<g opacity=".18" stroke="{WHITE}">
  <line x1="600" y1="{h}" x2="140" y2="0"><animate attributeName="opacity" values=".2;1;.2" dur="6s" repeatCount="indefinite"/></line>
  <line x1="600" y1="{h}" x2="1060" y2="0"><animate attributeName="opacity" values="1;.2;1" dur="6s" repeatCount="indefinite"/></line>
</g>
<text x="600" y="92" text-anchor="middle" class="bb in" font-size="15" fill="{DIM}" letter-spacing="9">A NITRO BUILDS PRODUCTION</text>
<text x="600" y="232" text-anchor="middle" class="t" font-size="150" fill="{WHITE}" letter-spacing="14"
      style="opacity:0;animation:rise 1.6s cubic-bezier(.2,.7,.2,1) .2s forwards">YASHWANTH</text>
<rect x="520" y="262" width="160" height="4" fill="url(#redbar)" class="in" style="animation-delay:1s"/>
<text x="600" y="306" text-anchor="middle" class="bb in" font-size="20" fill="{SOFT}" letter-spacing="7" style="animation-delay:1.2s">AI DEVELOPER  ·  AGENTIC SYSTEMS  ·  RAG ENGINEERING</text>
<text x="600" y="372" text-anchor="middle" class="b in" font-size="14" fill="{DIM}" letter-spacing="4" style="animation-delay:1.6s">OMICS INTERNATIONAL   ·   HYDERABAD   ·   NOW SHOWING</text>
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

def card(slug, tag, title, desc, stack):
    w, h = 590, 190
    body = f"""
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#card)" stroke="{LINE}"/>
<rect x="24" y="0" width="{w-48}" height="3" fill="url(#redbar)"/>
<text x="32" y="46" class="bb" font-size="12" fill="{RED}" letter-spacing="3">{escape(tag)}</text>
<text x="32" y="96" class="t" font-size="42" fill="{WHITE}" letter-spacing="2">{escape(title)}</text>
<text x="32" y="130" class="b" font-size="16" fill="{SOFT}">{escape(desc)}</text>
<text x="32" y="164" class="b" font-size="13" fill="{DIM}" letter-spacing="1">{escape(stack)}</text>
<text x="{w-32}" y="96" text-anchor="end" class="b" font-size="22" fill="{DIM}">→</text>"""
    svg(f"card-{slug}.svg", w, h, body)

def footer():
    w, h = 1200, 150
    body = f"""
<rect width="{w}" height="{h}" rx="14" fill="url(#vig)"/>
<text x="600" y="76" text-anchor="middle" class="t" font-size="38" fill="{WHITE}" letter-spacing="10">TO BE CONTINUED</text>
<rect x="560" y="94" width="80" height="3" fill="url(#redbar)"/>
<text x="600" y="126" text-anchor="middle" class="b" font-size="13" fill="{DIM}" letter-spacing="4">NEXT EPISODE: YOUR PROJECT</text>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>"""
    svg("footer.svg", w, h, body)

hero(); xp(); footer()
for a in [("about", "01", "THE ORIGIN"), ("quests", "02", "CURRENT QUESTS"),
          ("cases", "03", "FEATURED WORK"), ("stack", "04", "ARSENAL"), ("stats", "05", "BY THE NUMBERS")]:
    header(*a)
card("halo", "FLAGSHIP · RAG", "HALO", "Self-correcting PDF Q&A with citations & confidence", "Python · LangGraph · ChromaDB")
card("voxcode", "FLAGSHIP · AGENTS", "VOXCODE", "Voice-driven AI coding agent with live diffs", "Python · Hybrid search · STT/TTS")
card("omnichunk", "DOCUMENT AI", "OMNICHUNK", "Multi-modal chunking with zero information loss", "Python · Multi-modal")
card("pulsus", "WEB · 3D", "PULSUS-REGAIN", "Cinematic 3D portfolio and research outreach", "JavaScript · Three.js")
card("omniscout", "DATA · PRIVATE", "OMNISCOUT", "Biomedical literature & author intelligence", "FastAPI · PDF extraction · Excel")
card("booking", "BACKEND", "BOOKING API", "Concurrency-safe bookings with RBAC & JWT", "Java · Spring Boot")
print(sorted(os.listdir(OUT)))
