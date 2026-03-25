import streamlit as st
from dotenv import load_dotenv
import os
import re
import json
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="RoadmapAI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Custom CSS — Premium Dark UI
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }

.stApp { background: #070b14; color: #e8eaf0; }

.main-title {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -2px;
    background: linear-gradient(135deg, #00f5a0 0%, #00d9f5 50%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.1; margin-bottom: 0.2rem;
}
.sub-title {
    font-size: 1rem; color: #5a6478; letter-spacing: 0.05em;
    font-family: 'DM Mono', monospace !important; margin-bottom: 2rem;
}

.stChatInput > div {
    background: #0e1420 !important;
    border: 1px solid #1e2d40 !important;
    border-radius: 16px !important;
}

section[data-testid="stSidebar"] {
    background: #080c16 !important;
    border-right: 1px solid #151d2e;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #8892a4 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

.stSelectbox > div > div {
    background: #0e1420 !important;
    border: 1px solid #1e2d40 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}

.metric-card {
    background: linear-gradient(135deg, #0e1420, #111827);
    border: 1px solid #1e2d40; border-radius: 14px;
    padding: 1.2rem 1.5rem; text-align: center;
}
.metric-label { font-size: 0.7rem; color: #5a6478; font-family: 'DM Mono', monospace; letter-spacing: 0.1em; text-transform: uppercase; }
.metric-value { font-size: 1.6rem; font-weight: 800; color: #00f5a0; }

.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
    border-bottom: 1px solid #151d2e;
}
.section-header h3 {
    font-size: 1rem; font-weight: 700; color: #e8eaf0;
    margin: 0; letter-spacing: 0.05em; text-transform: uppercase;
}

.ref-card {
    background: #0e1420; border: 1px solid #1e2d40;
    border-left: 3px solid #00f5a0; border-radius: 10px;
    padding: 1rem 1.2rem; margin-bottom: 0.8rem; transition: border-color 0.2s;
}
.ref-card:hover { border-left-color: #00d9f5; }
.ref-title { font-weight: 700; color: #e8eaf0; font-size: 0.9rem; margin-bottom: 0.2rem; }
.ref-url { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #5a6478; word-break: break-all; }

.video-card {
    background: #0e1420; border: 1px solid #1e2d40;
    border-radius: 14px; overflow: hidden; margin-bottom: 1rem;
}
.video-info { padding: 0.8rem 1rem; }
.video-title { font-size: 0.85rem; font-weight: 700; color: #e8eaf0; margin-bottom: 0.2rem; line-height: 1.3; }
.video-channel { font-size: 0.72rem; color: #5a6478; font-family: 'DM Mono', monospace; }

.summary-box {
    background: linear-gradient(135deg, #0a1628, #0e1a2e);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 1.5rem; font-size: 0.9rem; line-height: 1.8; color: #c8d0e0;
}

.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-family: 'DM Mono', monospace; font-weight: 500; }
.badge-ok { background: #00f5a015; color: #00f5a0; border: 1px solid #00f5a030; }
.badge-warn { background: #f59e0b15; color: #f59e0b; border: 1px solid #f59e0b30; }
.badge-err { background: #ef444415; color: #ef4444; border: 1px solid #ef444430; }

.stSpinner > div { border-top-color: #00f5a0 !important; }
hr { border-color: #151d2e !important; }

.streamlit-expanderHeader {
    background: #0e1420 !important; border: 1px solid #1e2d40 !important;
    border-radius: 10px !important; color: #8892a4 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Load ENV
# -----------------------
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

# -----------------------
# Google Search
# -----------------------
def search_google(query):
    try:
        url = "https://serpapi.com/search"
        params = {"q": query, "api_key": SERPAPI_KEY, "engine": "google", "num": 5}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        results = []
        for item in data.get("organic_results", [])[:5]:
            link = item.get("link")
            title = item.get("title", link)
            snippet = item.get("snippet", "")
            if link:
                results.append({"url": link, "title": title, "snippet": snippet})
        return results
    except Exception:
        return []

# -----------------------
# Scraper
# -----------------------
def scrape(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:1500]
    except Exception:
        return ""

# -----------------------
# YouTube Search
# -----------------------
def search_youtube(query):
    if not YOUTUBE_API_KEY:
        return []
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet", "q": f"{query} tutorial roadmap",
            "type": "video", "maxResults": 4, "key": YOUTUBE_API_KEY,
            "relevanceLanguage": "en", "videoDuration": "medium"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        videos = []
        for item in data.get("items", []):
            vid_id = item["id"].get("videoId")
            if vid_id:
                videos.append({
                    "id": vid_id,
                    "title": item["snippet"]["title"],
                    "channel": item["snippet"]["channelTitle"],
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                })
        return videos
    except Exception:
        return []

# -----------------------
# Generate Roadmap JSON (for D3)
# -----------------------
def generate_roadmap_json(goal, context, difficulty, timeline):
    prompt = f"""
You are an expert learning roadmap generator.

Create a structured learning roadmap for:
Goal: {goal}
Difficulty: {difficulty}
Timeline: {timeline}

Context: {context[:2000]}

Return ONLY a valid JSON object (no markdown, no explanation) with this exact structure:
{{
  "title": "Goal Title",
  "totalDuration": "{timeline}",
  "difficulty": "{difficulty}",
  "phases": [
    {{
      "id": "phase1",
      "name": "Phase 1: Foundations",
      "duration": "4 weeks",
      "color": "#00f5a0",
      "nodes": [
        {{
          "id": "n1",
          "label": "Topic Name",
          "duration": "1 week",
          "type": "core",
          "description": "Brief description of what to learn",
          "resources": ["resource1", "resource2"],
          "dependencies": []
        }}
      ]
    }}
  ],
  "finalProjects": [
    {{"name": "Project name", "description": "What to build"}}
  ]
}}

Rules:
- 3-4 phases total, each with a distinct color from: #00f5a0, #00d9f5, #a78bfa, #f472b6
- 3-5 nodes per phase
- type must be one of: "core", "optional", "project"
- dependencies list node IDs from same or previous phases
- Keep descriptions to 1-2 sentences
- finalProjects should have 2-3 items
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You output ONLY valid JSON. No markdown fences, no extra text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)

# -----------------------
# Generate Summary
# -----------------------
def generate_summary(goal, context, difficulty, timeline):
    prompt = f"""
You are a career advisor. Create a concise roadmap summary for: {goal}
Difficulty: {difficulty} | Timeline: {timeline}
Context: {context[:800]}

Provide (use markdown):
- **Overview**: 2 sentences
- **Key Phases**: bullet list of phase names + durations
- **Must-Learn Skills**: top 5-6 tools/skills
- **Build These Projects**: 2-3 project ideas
- **Job Readiness**: estimated timeline

Be specific and encouraging.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

# -----------------------
# React + D3.js Interactive Roadmap
# -----------------------
def render_interactive_roadmap(roadmap_data):
    data_json = json.dumps(roadmap_data)

    html = fr"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    background: #070b14;
    font-family: 'Syne', 'Segoe UI', sans-serif;
    color: #e8eaf0;
    overflow-x: hidden;
}}
#root {{ width:100%; min-height:640px; }}

.tooltip {{
    position: fixed;
    background: #0e1420;
    border: 1px solid #1e2d40;
    border-left: 3px solid #00f5a0;
    border-radius: 12px;
    padding: 14px 18px;
    pointer-events: none;
    z-index: 9999;
    max-width: 280px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    opacity: 0;
    transition: opacity 0.15s;
}}
.tooltip.visible {{ opacity: 1; }}
.tooltip-title {{ font-weight: 700; font-size: 14px; color: #e8eaf0; margin-bottom:4px; }}
.tooltip-dur {{ font-size: 11px; color: #00f5a0; font-family: 'DM Mono', monospace; margin-bottom:8px; letter-spacing:0.05em; }}
.tooltip-desc {{ font-size: 12px; color: #8892a4; line-height:1.6; }}
.tooltip-res {{ font-size:10px; color:#5a6478; margin-top:8px; font-family:monospace; }}
.t-badge {{
    display:inline-block; margin-top:8px; padding:2px 10px;
    border-radius:20px; font-size:10px; font-family:monospace;
}}
.b-core {{ background:#00f5a015; color:#00f5a0; border:1px solid #00f5a030; }}
.b-optional {{ background:#f59e0b15; color:#f59e0b; border:1px solid #f59e0b30; }}
.b-project {{ background:#a78bfa15; color:#a78bfa; border:1px solid #a78bfa30; }}
.hint {{ font-size:9px; color:#2a3548; margin-top:6px; font-family:monospace; }}
</style>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
</head>
<body>
<div id="root"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>

<script type="text/babel">
const {{ useState, useEffect, useRef, useCallback }} = React;
const ROADMAP = {data_json};

const phaseColors = ROADMAP.phases.map((p,i) => {{
  const fallback = ["#00f5a0","#00d9f5","#a78bfa","#f472b6"];
  return p.color || fallback[i % fallback.length];
}});

const typeColor = t => ({{optional:"#f59e0b", project:"#a78bfa"}})[t] || null;

function buildGraph() {{
  const nodes=[], links=[], nodeMap={{}};
  let gx = 100;
  const colGap = 68, nodeR = 32;

  ROADMAP.phases.forEach((phase, pi) => {{
    const pColor = phaseColors[pi];
    const count = phase.nodes.length;
    const rowH = 110;
    const startY = 140;

    phase.nodes.forEach((node, ni) => {{
      const col = ni % 3;
      const row = Math.floor(ni / 3);
      const x = gx + col * (nodeR*2 + colGap);
      const y = startY + row * rowH;
      const n = {{ ...node, x, y, phaseIdx:pi, phaseColor:pColor, phaseName:phase.name, phaseId:phase.id }};
      nodes.push(n);
      nodeMap[node.id] = n;
    }});

    const cols = Math.min(count, 3);
    gx += cols * (nodeR*2 + colGap) + 80;
  }});

  nodes.forEach(n => {{
    (n.dependencies||[]).forEach(depId => {{
      if(nodeMap[depId]) links.push({{source:nodeMap[depId], target:n}});
    }});
  }});

  return {{ nodes, links, nodeMap, totalWidth: gx + 60 }};
}}

function App() {{
  const svgRef = useRef(null);
  const ttRef = useRef(null);
  const [filter, setFilter] = useState("all");
  const [completed, setCompleted] = useState(new Set());
  const [hovered, setHovered] = useState(null);
  const [activePhase, setActivePhase] = useState(null);

  const {{ nodes, links, totalWidth }} = buildGraph();
  const H = 460;

  const toggle = useCallback(id => {{
    setCompleted(prev => {{
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    }});
  }}, []);

  const progress = Math.round(completed.size / nodes.length * 100) || 0;

  const visNodes = filter === "all"
    ? (activePhase ? nodes.filter(n=>n.phaseId===activePhase) : nodes)
    : nodes.filter(n => n.type === filter);

  useEffect(() => {{
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    const W = totalWidth;

    const zoom = d3.zoom().scaleExtent([0.3,2.2]).on("zoom", e => g.attr("transform", e.transform));
    svg.call(zoom);

    const g = svg.append("g");
    const defs = svg.append("defs");

    // Animated gradient background line
    const bgGrad = defs.append("linearGradient").attr("id","bgLine").attr("x1","0%").attr("x2","100%");
    bgGrad.append("stop").attr("offset","0%").attr("stop-color","#00f5a0").attr("stop-opacity","0.15");
    bgGrad.append("stop").attr("offset","50%").attr("stop-color","#00d9f5").attr("stop-opacity","0.1");
    bgGrad.append("stop").attr("offset","100%").attr("stop-color","#a78bfa").attr("stop-opacity","0.15");

    g.append("line").attr("x1",60).attr("y1",140).attr("x2",W-60).attr("y2",140)
      .attr("stroke","url(#bgLine)").attr("stroke-width","1").attr("stroke-dasharray","6 4");

    // Glow filter
    const glow = defs.append("filter").attr("id","glow");
    glow.append("feGaussianBlur").attr("stdDeviation","4").attr("result","blur");
    const fm = glow.append("feMerge");
    fm.append("feMergeNode").attr("in","blur");
    fm.append("feMergeNode").attr("in","SourceGraphic");

    // Phase backgrounds
    ROADMAP.phases.forEach((phase, pi) => {{
      const pNodes = nodes.filter(n => n.phaseIdx===pi);
      if(!pNodes.length) return;
      const xs=pNodes.map(n=>n.x), ys=pNodes.map(n=>n.y);
      const x1=Math.min(...xs)-52, x2=Math.max(...xs)+52;
      const y1=Math.min(...ys)-52, y2=Math.max(...ys)+52;
      const pColor = phaseColors[pi];
      const isActive = activePhase === phase.id;

      const phGrad = defs.append("linearGradient").attr("id",`pg${{pi}}`).attr("x1","0%").attr("y1","0%").attr("x2","0%").attr("y2","100%");
      phGrad.append("stop").attr("offset","0%").attr("stop-color",pColor).attr("stop-opacity", isActive?"0.14":"0.06");
      phGrad.append("stop").attr("offset","100%").attr("stop-color",pColor).attr("stop-opacity","0.02");

      g.append("rect")
        .attr("x",x1).attr("y",y1).attr("width",x2-x1).attr("height",y2-y1)
        .attr("rx",18).attr("fill",`url(#pg${{pi}})`)
        .attr("stroke",pColor).attr("stroke-opacity", isActive?"0.4":"0.12")
        .attr("stroke-width", isActive?"1.5":"1")
        .style("cursor","pointer")
        .on("click", () => setActivePhase(prev => prev===phase.id ? null : phase.id));

      g.append("text").attr("x",(x1+x2)/2).attr("y",y1+20)
        .attr("text-anchor","middle").attr("font-size","10").attr("font-weight","700")
        .attr("fill",pColor).attr("opacity","0.9").attr("letter-spacing","1.5")
        .text(phase.name.toUpperCase().substring(0,30));

      g.append("text").attr("x",(x1+x2)/2).attr("y",y1+35)
        .attr("text-anchor","middle").attr("font-size","9").attr("fill","#3a4558")
        .attr("font-family","'DM Mono',monospace").text(phase.duration||"");
    }});

    // Arrow marker
    defs.append("marker").attr("id","arr").attr("viewBox","0 0 10 10")
      .attr("refX","9").attr("refY","5").attr("markerWidth","5").attr("markerHeight","5").attr("orient","auto")
      .append("path").attr("d","M0 0 L10 5 L0 10z").attr("fill","#1e3a5f");

    // Links
    const visible = new Set(visNodes.map(n=>n.id));
    g.selectAll(".lnk")
      .data(links.filter(l => visible.has(l.source.id) && visible.has(l.target.id)))
      .enter().append("path").attr("class","lnk")
      .attr("d", d => {{
        const dx = d.target.x - d.source.x, dy = d.target.y - d.source.y;
        return `M${{d.source.x}} ${{d.source.y}} C${{d.source.x+dx*0.55}} ${{d.source.y}},${{d.target.x-dx*0.55}} ${{d.target.y}},${{d.target.x}} ${{d.target.y}}`;
      }})
      .attr("fill","none")
      .attr("stroke", d => phaseColors[d.source.phaseIdx])
      .attr("stroke-opacity","0.2").attr("stroke-width","1.5")
      .attr("stroke-dasharray","5 3").attr("marker-end","url(#arr)");

    // Nodes
    const ng = g.selectAll(".nd")
      .data(visNodes).enter().append("g").attr("class","nd")
      .attr("transform", d=>`translate(${{d.x}},${{d.y}})`)
      .style("cursor","pointer")
      .on("click", (_,d) => toggle(d.id))
      .on("mouseenter", (event,d) => {{
        setHovered(d);
        const tt = ttRef.current;
        if(tt) {{ tt.classList.add("visible"); tt.style.left=(event.clientX+16)+"px"; tt.style.top=(event.clientY-12)+"px"; }}
        d3.select(event.currentTarget).select(".mc")
          .transition().duration(180).attr("r",38);
        d3.select(event.currentTarget).select(".ring")
          .transition().duration(180).attr("stroke-opacity","0.5");
      }})
      .on("mousemove", event => {{
        const tt=ttRef.current;
        if(tt) {{ tt.style.left=(event.clientX+16)+"px"; tt.style.top=(event.clientY-12)+"px"; }}
      }})
      .on("mouseleave", (event,d) => {{
        setHovered(null);
        const tt=ttRef.current;
        if(tt) tt.classList.remove("visible");
        d3.select(event.currentTarget).select(".mc")
          .transition().duration(180).attr("r",32);
        d3.select(event.currentTarget).select(".ring")
          .transition().duration(180).attr("stroke-opacity","0.2");
      }});

    // Pulse ring
    ng.append("circle").attr("class","ring").attr("r",40)
      .attr("fill","none")
      .attr("stroke", d => typeColor(d.type)||phaseColors[d.phaseIdx])
      .attr("stroke-width","1").attr("stroke-opacity","0.2")
      .attr("stroke-dasharray","6 4");

    // Build node gradient per node
    ng.each(function(d) {{
      const nc = typeColor(d.type)||phaseColors[d.phaseIdx];
      const done = completed.has(d.id);
      const gid = `ng_${{d.id}}`;
      const rg = d3.select(svgRef.current).select("defs").append("radialGradient").attr("id",gid);
      rg.append("stop").attr("offset","0%").attr("stop-color", done ? nc : "#1e2840");
      rg.append("stop").attr("offset","100%").attr("stop-color", done ? nc+"55" : "#0a0f1a");

      d3.select(this).append("circle").attr("class","mc").attr("r",32)
        .attr("fill",`url(#${{gid}})`)
        .attr("stroke",nc).attr("stroke-width", done?2.5:1.5)
        .attr("filter", done?"url(#glow)":"none");
    }});

    // Label inside
    ng.append("text").attr("text-anchor","middle").attr("y",-3)
      .attr("font-size","9.5").attr("font-weight","700")
      .attr("fill", d => typeColor(d.type)||phaseColors[d.phaseIdx])
      .attr("letter-spacing","0.3")
      .text(d => d.label.split(" ").slice(0,2).map(w=>w.substring(0,5)).join(" "));

    ng.append("text").attr("text-anchor","middle").attr("y",11)
      .attr("font-size","8").attr("fill","#3a4558")
      .attr("font-family","'DM Mono',monospace")
      .text(d => d.duration||"");

    // Checkmark
    ng.filter(d => completed.has(d.id))
      .append("text").attr("x",22).attr("y",-22)
      .attr("font-size","15").attr("fill","#00f5a0").text("✓");

    // Label below
    ng.append("foreignObject").attr("x",-54).attr("y",38).attr("width",108).attr("height",52)
      .append("xhtml:div")
      .style("text-align","center").style("font-size","10px")
      .style("font-weight","600").style("color","#b0b8cc")
      .style("line-height","1.35").style("padding","0 4px")
      .text(d => d.label);

  }}, [visNodes, completed, totalWidth, activePhase]);

  return (
    <div style={{background:'#07090f', borderRadius:'18px', border:'1px solid #1e2d40', overflow:'hidden', fontFamily:"'Syne',sans-serif"}}>

      {{/* Top Header */}}
      <div style={{padding:'20px 26px 16px', borderBottom:'1px solid #111827'}}>
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start', flexWrap:'wrap', gap:'12px'}}>
          <div>
            <div style={{fontSize:'20px', fontWeight:'800', color:'#e8eaf0', letterSpacing:'-0.5px'}}>
              {{ROADMAP.title}}
            </div>
            <div style={{fontSize:'11px', color:'#3a4558', fontFamily:"'DM Mono',monospace", marginTop:'4px', letterSpacing:'0.05em'}}>
              {{ROADMAP.difficulty}} &nbsp;·&nbsp; {{ROADMAP.totalDuration}} &nbsp;·&nbsp; {{nodes.length}} topics &nbsp;·&nbsp; {{ROADMAP.phases.length}} phases
            </div>
          </div>
          <div style={{display:'flex', gap:'8px', alignItems:'center', flexWrap:'wrap'}}>
            {{ROADMAP.phases.map((phase,pi) => (
              <button key={{phase.id}}
                onClick={{() => setActivePhase(prev => prev===phase.id ? null : phase.id)}}
                style={{
                  background: activePhase===phase.id ? phaseColors[pi]+'20' : '#0e1420',
                  border: `1px solid ${{activePhase===phase.id ? phaseColors[pi]+'60' : '#1e2d40'}}`,
                  color: activePhase===phase.id ? phaseColors[pi] : '#5a6478',
                  padding:'4px 12px', borderRadius:'20px', fontSize:'10px',
                  cursor:'pointer', fontFamily:"'DM Mono',monospace",
                  transition:'all 0.2s', letterSpacing:'0.03em'
                }}>
                {{phase.name.replace(/Phase r"\d"+: /i,'').substring(0,16)}}
              </button>
            ))}}
          </div>
        </div>

        {{/* Progress */}}
        <div style={{marginTop:'14px'}}>
          <div style={{display:'flex', justifyContent:'space-between', marginBottom:'5px'}}>
            <span style={{fontSize:'10px', color:'#3a4558', fontFamily:"'DM Mono',monospace", letterSpacing:'0.08em'}}>
              PROGRESS
            </span>
            <span style={{fontSize:'10px', color:'#00f5a0', fontFamily:"'DM Mono',monospace"}}>
              {{completed.size}} / {{nodes.length}} &nbsp; {{progress}}%
            </span>
          </div>
          <div style={{height:'4px', background:'#111827', borderRadius:'4px'}}>
            <div style={{
              height:'100%', borderRadius:'4px', width:`${{progress}}%`,
              background:'linear-gradient(90deg,#00f5a0,#00d9f5,#a78bfa)',
              transition:'width 0.8s ease', boxShadow: progress>0 ? '0 0 8px #00f5a060' : 'none'
            }}/>
          </div>
        </div>
      </div>

      {{/* Controls */}}
      <div style={{display:'flex', gap:'8px', padding:'12px 22px', flexWrap:'wrap', alignItems:'center', borderBottom:'1px solid #0d1320'}}>
        <span style={{fontSize:'10px', color:'#2a3548', fontFamily:"'DM Mono',monospace", letterSpacing:'0.08em'}}>FILTER TYPE:</span>
        {{["all","core","optional","project"].map(f => (
          <button key={{f}}
            onClick={{() => setFilter(f)}}
            style={{
              background: filter===f ? '#00f5a012' : 'transparent',
              border: filter===f ? '1px solid #00f5a040' : '1px solid #151d2e',
              color: filter===f ? '#00f5a0' : '#3a4558',
              padding:'3px 12px', borderRadius:'20px', fontSize:'10px',
              cursor:'pointer', fontFamily:"'DM Mono',monospace",
              transition:'all 0.2s', textTransform:'uppercase', letterSpacing:'0.06em'
            }}>
            {{f}}
          </button>
        ))}}
        <div style={{marginLeft:'auto', display:'flex', gap:'16px'}}>
          {{[
            {{c:'#00f5a0', l:'Core'}},
            {{c:'#f59e0b', l:'Optional'}},
            {{c:'#a78bfa', l:'Project'}},
          ].map(l => (
            <div key={{l.l}} style={{display:'flex', alignItems:'center', gap:'5px'}}>
              <div style={{width:'7px', height:'7px', borderRadius:'50%', background:l.c}}/>
              <span style={{fontSize:'9px', color:'#3a4558', fontFamily:"'DM Mono',monospace"}}>{{l.l}}</span>
            </div>
          ))}}
        </div>
      </div>

      {{/* D3 Canvas */}}
      <div style={{overflowX:'auto', overflowY:'hidden', background:'#070b14'}}>
        <svg ref={{svgRef}} width={{totalWidth}} height={{H}} style={{display:'block', minWidth:'100%'}}/>
      </div>

      {{/* Hint bar */}}
      <div style={{padding:'8px 22px', background:'#050810', borderTop:'1px solid #0d1320',
        fontSize:'9px', color:'#1e2d40', fontFamily:"'DM Mono',monospace", letterSpacing:'0.06em',
        display:'flex', gap:'20px'}}>
        <span>↕ scroll to zoom</span>
        <span>← → drag to pan</span>
        <span>◉ click node to complete</span>
        <span>▣ click phase label to filter</span>
      </div>

      {{/* Final Projects */}}
      {{ROADMAP.finalProjects && ROADMAP.finalProjects.length > 0 && (
        <div style={{padding:'18px 22px', borderTop:'1px solid #111827', background:'#06080f'}}>
          <div style={{fontSize:'10px', fontWeight:'700', color:'#a78bfa',
            letterSpacing:'0.12em', textTransform:'uppercase', marginBottom:'12px',
            fontFamily:"'DM Mono',monospace"}}>
            🚀 Capstone Projects
          </div>
          <div style={{display:'flex', gap:'12px', flexWrap:'wrap'}}>
            {{ROADMAP.finalProjects.map((p,i) => (
              <div key={{i}} style={{
                background:'linear-gradient(135deg,#0d0f1f,#100d20)',
                border:'1px solid #2d1f6e', borderRadius:'12px',
                padding:'12px 16px', flex:'1', minWidth:'160px'
              }}>
                <div style={{fontSize:'12px', fontWeight:'700', color:'#a78bfa', marginBottom:'5px'}}>{{p.name}}</div>
                <div style={{fontSize:'11px', color:'#5a6478', lineHeight:'1.5'}}>{{p.description}}</div>
              </div>
            ))}}
          </div>
        </div>
      )}}
    </div>
  );
}}

// Tooltip wrapper
function WithTooltip() {{
  const ttRef = useRef(null);
  const [hovered, setHovered] = useState(null);
  return (
    <>
      <App ttRef={{ttRef}} setHovered={{setHovered}} hovered={{hovered}}/>
      <div ref={{ttRef}} className="tooltip">
        {{hovered && <>
          <div className="tooltip-title">{{hovered.label}}</div>
          <div className="tooltip-dur">⏱ {{hovered.duration}}</div>
          <div className="tooltip-desc">{{hovered.description}}</div>
          {{hovered.resources?.length > 0 && (
            <div className="tooltip-res">📚 {{hovered.resources.join(", ")}}</div>
          )}}
          <div className={{`t-badge b-${{hovered.type}}`}}>{{hovered.type}}</div>
          <div className="hint">click to mark {{hovered.type === 'complete' ? 'incomplete' : 'complete'}}</div>
        </>}}
      </div>
    </>
  );
}}

// Pass ttRef and setHovered into App via a different approach
function AppWithTooltip() {{
  const ttRef = useRef(null);
  const svgRef = useRef(null);
  const [filter, setFilter] = useState("all");
  const [completed, setCompleted] = useState(new Set());
  const [hovered, setHovered] = useState(null);
  const [activePhase, setActivePhase] = useState(null);

  const {{ nodes, links, totalWidth }} = buildGraph();
  const H = 460;

  const toggle = useCallback(id => {{
    setCompleted(prev => {{
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    }});
  }}, []);

  const progress = Math.round(completed.size / nodes.length * 100) || 0;

  const visNodes = filter === "all"
    ? (activePhase ? nodes.filter(n=>n.phaseId===activePhase) : nodes)
    : nodes.filter(n => n.type === filter);

  useEffect(() => {{
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    const W = totalWidth;

    const zoomB = d3.zoom().scaleExtent([0.3,2.2]).on("zoom", e => g.attr("transform", e.transform));
    svg.call(zoomB);
    const g = svg.append("g");
    const defs = svg.append("defs");

    const bgGrad = defs.append("linearGradient").attr("id","bgLine2").attr("x1","0%").attr("x2","100%");
    bgGrad.append("stop").attr("offset","0%").attr("stop-color","#00f5a0").attr("stop-opacity","0.12");
    bgGrad.append("stop").attr("offset","50%").attr("stop-color","#00d9f5").attr("stop-opacity","0.08");
    bgGrad.append("stop").attr("offset","100%").attr("stop-color","#a78bfa").attr("stop-opacity","0.12");
    g.append("line").attr("x1",80).attr("y1",140).attr("x2",W-80).attr("y2",140)
      .attr("stroke","url(#bgLine2)").attr("stroke-width","1").attr("stroke-dasharray","6 4");

    const glow = defs.append("filter").attr("id","glow2");
    glow.append("feGaussianBlur").attr("stdDeviation","4").attr("result","blur");
    const fm = glow.append("feMerge");
    fm.append("feMergeNode").attr("in","blur");
    fm.append("feMergeNode").attr("in","SourceGraphic");

    ROADMAP.phases.forEach((phase,pi) => {{
      const pNodes = nodes.filter(n=>n.phaseIdx===pi);
      if(!pNodes.length) return;
      const xs=pNodes.map(n=>n.x), ys=pNodes.map(n=>n.y);
      const x1=Math.min(...xs)-56, x2=Math.max(...xs)+56;
      const y1=Math.min(...ys)-58, y2=Math.max(...ys)+58;
      const pc = phaseColors[pi];
      const isActive = activePhase===phase.id;

      const phG = defs.append("linearGradient").attr("id",`pg2_${{pi}}`).attr("x1","0%").attr("y1","0%").attr("x2","0%").attr("y2","100%");
      phG.append("stop").attr("offset","0%").attr("stop-color",pc).attr("stop-opacity",isActive?"0.15":"0.05");
      phG.append("stop").attr("offset","100%").attr("stop-color",pc).attr("stop-opacity","0.01");

      g.append("rect").attr("x",x1).attr("y",y1).attr("width",x2-x1).attr("height",y2-y1)
        .attr("rx",18).attr("fill",`url(#pg2_${{pi}})`)
        .attr("stroke",pc).attr("stroke-opacity",isActive?"0.45":"0.12")
        .attr("stroke-width",isActive?"1.5":"1")
        .style("cursor","pointer")
        .on("click",() => setActivePhase(prev => prev===phase.id ? null : phase.id));

      g.append("text").attr("x",(x1+x2)/2).attr("y",y1+20)
        .attr("text-anchor","middle").attr("font-size","10").attr("font-weight","700")
        .attr("fill",pc).attr("opacity","0.85").attr("letter-spacing","1.5")
        .text(phase.name.toUpperCase().substring(0,28));
      g.append("text").attr("x",(x1+x2)/2).attr("y",y1+34)
        .attr("text-anchor","middle").attr("font-size","9").attr("fill","#2a3548")
        .attr("font-family","'DM Mono',monospace").text(phase.duration||"");
    }});

    defs.append("marker").attr("id","arr2").attr("viewBox","0 0 10 10")
      .attr("refX","9").attr("refY","5").attr("markerWidth","5").attr("markerHeight","5").attr("orient","auto")
      .append("path").attr("d","M0 0 L10 5 L0 10z").attr("fill","#1e3a5f");

    const visible = new Set(visNodes.map(n=>n.id));
    g.selectAll(".lnk2")
      .data(links.filter(l=>visible.has(l.source.id)&&visible.has(l.target.id)))
      .enter().append("path").attr("class","lnk2")
      .attr("d",d=>{{
        const dx=d.target.x-d.source.x, dy=d.target.y-d.source.y;
        return `M${{d.source.x}} ${{d.source.y}} C${{d.source.x+dx*0.55}} ${{d.source.y}},${{d.target.x-dx*0.55}} ${{d.target.y}},${{d.target.x}} ${{d.target.y}}`;
      }})
      .attr("fill","none").attr("stroke",d=>phaseColors[d.source.phaseIdx])
      .attr("stroke-opacity","0.2").attr("stroke-width","1.5")
      .attr("stroke-dasharray","5 3").attr("marker-end","url(#arr2)");

    const ng = g.selectAll(".nd2")
      .data(visNodes).enter().append("g").attr("class","nd2")
      .attr("transform",d=>`translate(${{d.x}},${{d.y}})`).style("cursor","pointer")
      .on("click",(_,d)=>toggle(d.id))
      .on("mouseenter",(event,d)=>{{
        setHovered(d);
        const tt=ttRef.current;
        if(tt){{tt.classList.add("visible");tt.style.left=(event.clientX+16)+"px";tt.style.top=(event.clientY-12)+"px";}}
        d3.select(event.currentTarget).select(".mc2").transition().duration(180).attr("r",38);
        d3.select(event.currentTarget).select(".ring2").transition().duration(180).attr("stroke-opacity","0.5");
      }})
      .on("mousemove",event=>{{
        const tt=ttRef.current;
        if(tt){{tt.style.left=(event.clientX+16)+"px";tt.style.top=(event.clientY-12)+"px";}}
      }})
      .on("mouseleave",(event)=>{{
        setHovered(null);
        const tt=ttRef.current;
        if(tt) tt.classList.remove("visible");
        d3.select(event.currentTarget).select(".mc2").transition().duration(180).attr("r",32);
        d3.select(event.currentTarget).select(".ring2").transition().duration(180).attr("stroke-opacity","0.18");
      }});

    ng.append("circle").attr("class","ring2").attr("r",42)
      .attr("fill","none").attr("stroke",d=>typeColor(d.type)||phaseColors[d.phaseIdx])
      .attr("stroke-width","1").attr("stroke-opacity","0.18").attr("stroke-dasharray","6 4");

    ng.each(function(d){{
      const nc=typeColor(d.type)||phaseColors[d.phaseIdx];
      const done=completed.has(d.id);
      const gid=`ng2_${{d.id}}`;
      const rg=d3.select(svgRef.current).select("defs").append("radialGradient").attr("id",gid);
      rg.append("stop").attr("offset","0%").attr("stop-color",done?nc:"#1a2535");
      rg.append("stop").attr("offset","100%").attr("stop-color",done?nc+"44":"#070b14");
      d3.select(this).append("circle").attr("class","mc2").attr("r",32)
        .attr("fill",`url(#${{gid}})`).attr("stroke",nc)
        .attr("stroke-width",done?2.5:1.5).attr("filter",done?"url(#glow2)":"none");
    }});

    ng.append("text").attr("text-anchor","middle").attr("y",-3)
      .attr("font-size","9.5").attr("font-weight","700")
      .attr("fill",d=>typeColor(d.type)||phaseColors[d.phaseIdx]).attr("letter-spacing","0.3")
      .text(d=>d.label.split(" ").slice(0,2).map(w=>w.substring(0,5)).join(" "));

    ng.append("text").attr("text-anchor","middle").attr("y",11)
      .attr("font-size","8").attr("fill","#2a3548").attr("font-family","'DM Mono',monospace")
      .text(d=>d.duration||"");

    ng.filter(d=>completed.has(d.id))
      .append("text").attr("x",22).attr("y",-22).attr("font-size","15").attr("fill","#00f5a0").text("✓");

    ng.append("foreignObject").attr("x",-54).attr("y",38).attr("width",108).attr("height",54)
      .append("xhtml:div")
      .style("text-align","center").style("font-size","10px")
      .style("font-weight","600").style("color","#9aa3b8")
      .style("line-height","1.35").style("padding","0 4px")
      .text(d=>d.label);

  }}, [visNodes, completed, totalWidth, activePhase]);

  return (
    <div style={{background:'#07090f', borderRadius:'18px', border:'1px solid #1a2535', overflow:'hidden', fontFamily:"'Syne',sans-serif"}}>

      <div style={{padding:'20px 26px 16px', borderBottom:'1px solid #0d1525'}}>
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start', flexWrap:'wrap', gap:'12px'}}>
          <div>
            <div style={{fontSize:'20px', fontWeight:'800', color:'#e8eaf0', letterSpacing:'-0.5px'}}>
              {{ROADMAP.title}}
            </div>
            <div style={{fontSize:'11px', color:'#2a3548', fontFamily:"'DM Mono',monospace", marginTop:'4px', letterSpacing:'0.05em'}}>
              {{ROADMAP.difficulty}} · {{ROADMAP.totalDuration}} · {{nodes.length}} topics · {{ROADMAP.phases.length}} phases
            </div>
          </div>
          <div style={{display:'flex', gap:'8px', flexWrap:'wrap'}}>
            {{ROADMAP.phases.map((phase,pi) => (
              <button key={{phase.id}} onClick={{()=>setActivePhase(prev=>prev===phase.id?null:phase.id)}}
                style={{
                  background: activePhase===phase.id ? phaseColors[pi]+'18' : 'transparent',
                  border: `1px solid ${{activePhase===phase.id ? phaseColors[pi]+'55' : '#151d2e'}}`,
                  color: activePhase===phase.id ? phaseColors[pi] : '#3a4558',
                  padding:'3px 11px', borderRadius:'20px', fontSize:'10px',
                  cursor:'pointer', fontFamily:"'DM Mono',monospace", transition:'all 0.2s', letterSpacing:'0.03em'
                }}>
                {{phase.name.replace(/Phase r"\d"+:?\s*/i,'').substring(0,18)}}
              </button>
            ))}}
          </div>
        </div>

        <div style={{marginTop:'14px'}}>
          <div style={{display:'flex', justifyContent:'space-between', marginBottom:'5px'}}>
            <span style={{fontSize:'10px', color:'#2a3548', fontFamily:"'DM Mono',monospace", letterSpacing:'0.1em'}}>PROGRESS</span>
            <span style={{fontSize:'10px', color:'#00f5a0', fontFamily:"'DM Mono',monospace"}}>{{completed.size}} / {{nodes.length}} completed · {{progress}}%</span>
          </div>
          <div style={{height:'3px', background:'#0d1320', borderRadius:'3px'}}>
            <div style={{height:'100%', borderRadius:'3px', width:`${{progress}}%`,
              background:'linear-gradient(90deg,#00f5a0,#00d9f5,#a78bfa)',
              transition:'width 0.8s ease', boxShadow:progress>0?'0 0 10px #00f5a050':'none'}}/>
          </div>
        </div>
      </div>

      <div style={{display:'flex', gap:'8px', padding:'11px 22px', flexWrap:'wrap', alignItems:'center', borderBottom:'1px solid #0a0f1a'}}>
        <span style={{fontSize:'9px', color:'#1e2d40', fontFamily:"'DM Mono',monospace", letterSpacing:'0.1em'}}>TYPE:</span>
        {{["all","core","optional","project"].map(f => (
          <button key={{f}} onClick={{()=>setFilter(f)}}
            style={{
              background:filter===f?'#00f5a010':'transparent',
              border:filter===f?'1px solid #00f5a035':'1px solid #0d1525',
              color:filter===f?'#00f5a0':'#2a3548',
              padding:'3px 11px', borderRadius:'20px', fontSize:'9px',
              cursor:'pointer', fontFamily:"'DM Mono',monospace",
              transition:'all 0.2s', textTransform:'uppercase', letterSpacing:'0.08em'
            }}>{{f}}</button>
        ))}}
        <div style={{marginLeft:'auto', display:'flex', gap:'14px'}}>
          {{[['#00f5a0','Core'],['#f59e0b','Optional'],['#a78bfa','Project']].map(([c,l])=>(
            <div key={{l}} style={{display:'flex', alignItems:'center', gap:'5px'}}>
              <div style={{width:'6px', height:'6px', borderRadius:'50%', background:c}}/>
              <span style={{fontSize:'9px', color:'#2a3548', fontFamily:"'DM Mono',monospace"}}>{{l}}</span>
            </div>
          ))}}
        </div>
      </div>

      <div style={{overflowX:'auto', background:'#070b14'}}>
        <svg ref={{svgRef}} width={{totalWidth}} height={{H}} style={{display:'block', minWidth:'100%'}}/>
      </div>

      <div style={{padding:'7px 22px', background:'#040609', borderTop:'1px solid #0a0f1a',
        fontSize:'9px', color:'#151d2e', fontFamily:"'DM Mono',monospace", letterSpacing:'0.08em',
        display:'flex', gap:'18px', flexWrap:'wrap'}}>
        <span>⟳ scroll = zoom</span>
        <span>← drag = pan</span>
        <span>● click node = complete</span>
        <span>▣ click phase = filter</span>
      </div>

      {{ROADMAP.finalProjects?.length > 0 && (
        <div style={{padding:'16px 22px', borderTop:'1px solid #0d1525', background:'#050810'}}>
          <div style={{fontSize:'9px', fontWeight:'700', color:'#a78bfa', letterSpacing:'0.12em',
            textTransform:'uppercase', marginBottom:'10px', fontFamily:"'DM Mono',monospace"}}>
            🚀 Capstone Projects
          </div>
          <div style={{display:'flex', gap:'10px', flexWrap:'wrap'}}>
            {{ROADMAP.finalProjects.map((p,i)=>(
              <div key={{i}} style={{background:'linear-gradient(135deg,#0a0d1c,#0d0a1e)',
                border:'1px solid #1e1650', borderRadius:'10px', padding:'11px 15px', flex:'1', minWidth:'150px'}}>
                <div style={{fontSize:'12px', fontWeight:'700', color:'#a78bfa', marginBottom:'4px'}}>{{p.name}}</div>
                <div style={{fontSize:'11px', color:'#3a4558', lineHeight:'1.5'}}>{{p.description}}</div>
              </div>
            ))}}
          </div>
        </div>
      )}}

      <div ref={{ttRef}} className="tooltip">
        {{hovered && <>
          <div className="tooltip-title">{{hovered.label}}</div>
          <div className="tooltip-dur">⏱ {{hovered.duration}}</div>
          <div className="tooltip-desc">{{hovered.description}}</div>
          {{hovered.resources?.length > 0 &&
            <div className="tooltip-res">📚 {{hovered.resources.slice(0,3).join(" · ")}}</div>
          }}
          <div className={{`t-badge b-${{hovered.type}}`}}>{{hovered.type}}</div>
          <div className="hint">click to mark {{completed.has(hovered.id)?'incomplete':'complete'}}</div>
        </>}}
      </div>
    </div>
  );
}}

ReactDOM.render(<AppWithTooltip/>, document.getElementById('root'));
</script>
</body>
</html>"""
    st.components.v1.html(html, height=720, scrolling=False)


# ======================
# UI LAYOUT
# ======================
st.markdown('<div class="main-title">🧭 RoadmapAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">// enter any learning goal · get an interactive visual roadmap with d3.js</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.divider()
    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"], index=0)
    timeline = st.selectbox("Target Timeline", ["1 month", "3 months", "6 months", "1 year"], index=1)
    st.divider()
    st.markdown("### 🔧 Sections")
    show_summary = st.toggle("Roadmap Summary", value=True)
    show_youtube = st.toggle("YouTube Resources", value=True)
    show_refs = st.toggle("Reference Sources", value=True)
    st.divider()
    st.markdown("### 🔑 API Status")

    def badge_html(ok, warn=False):
        if ok: return '<span class="badge badge-ok">● CONNECTED</span>'
        if warn: return '<span class="badge badge-warn">● OPTIONAL</span>'
        return '<span class="badge badge-err">● MISSING</span>'

    st.markdown(f"**SerpAPI** {badge_html(bool(SERPAPI_KEY))}", unsafe_allow_html=True)
    st.markdown(f"**OpenRouter** {badge_html(bool(OPENROUTER_API_KEY))}", unsafe_allow_html=True)
    st.markdown(f"**YouTube** {badge_html(bool(YOUTUBE_API_KEY), warn=True)}", unsafe_allow_html=True)
    st.divider()
    st.caption("React · D3.js · GPT-4o-mini · SerpAPI")

# Chat
user_input = st.chat_input("Enter your goal (e.g. Full Stack Developer, ML Engineer, iOS Dev, DevOps...)")

if user_input:
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Researching..."):
            search_results = search_google(f"{user_input} learning roadmap {difficulty.lower()}")
            context = ""
            for item in search_results:
                context += scrape(item["url"]) + "\n"

        roadmap_data = None
        with st.spinner("🧠 Building interactive roadmap..."):
            try:
                roadmap_data = generate_roadmap_json(user_input, context, difficulty, timeline)
            except Exception as e:
                st.error(f"Roadmap generation failed: {e}")
                st.info("Try rephrasing your goal or check your API key.")

        if roadmap_data:
            phases = roadmap_data.get("phases", [])
            total_nodes = sum(len(p["nodes"]) for p in phases)
            projects = roadmap_data.get("finalProjects", [])

            # Metrics
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Phases</div><div class="metric-value">{len(phases)}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Topics</div><div class="metric-value">{total_nodes}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Projects</div><div class="metric-value">{len(projects)}</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Timeline</div><div class="metric-value" style="font-size:1rem">{timeline}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Interactive roadmap
            st.markdown('<div class="section-header"><h3>📊 Interactive Roadmap</h3></div>', unsafe_allow_html=True)
            render_interactive_roadmap(roadmap_data)

            # Raw JSON expander
            with st.expander("🗂 Raw Roadmap Data (JSON)"):
                st.json(roadmap_data)

        # Summary
        if show_summary:
            with st.spinner("📝 Writing summary..."):
                summary = generate_summary(user_input, context, difficulty, timeline)
            st.markdown('<div class="section-header"><h3>📋 Roadmap Summary</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

        # YouTube
        if show_youtube:
            if YOUTUBE_API_KEY:
                with st.spinner("📺 Finding video resources..."):
                    videos = search_youtube(user_input)
                if videos:
                    st.markdown('<div class="section-header"><h3>🎥 YouTube Resources</h3></div>', unsafe_allow_html=True)
                    vcols = st.columns(2)
                    for i, video in enumerate(videos):
                        with vcols[i % 2]:
                            st.markdown(f"""
                            <div class="video-card">
                                <a href="{video['url']}" target="_blank">
                                    <img src="{video['thumbnail']}" style="width:100%;display:block;">
                                </a>
                                <div class="video-info">
                                    <div class="video-title">
                                        <a href="{video['url']}" target="_blank" style="color:#e8eaf0;text-decoration:none;">
                                            {video['title'][:65]}{'...' if len(video['title'])>65 else ''}
                                        </a>
                                    </div>
                                    <div class="video-channel">📺 {video['channel']}</div>
                                </div>
                            </div>""", unsafe_allow_html=True)
            else:
                st.info("💡 Add `YOUTUBE_API_KEY` to `.env` to enable video recommendations.")

        # References
        if show_refs and search_results:
            st.markdown('<div class="section-header"><h3>🔗 Reference Sources</h3></div>', unsafe_allow_html=True)
            for item in search_results:
                title = item.get("title", item["url"])
                snippet = item.get("snippet", "")
                url = item["url"]
                domain = url.split("/")[2] if len(url.split("/")) > 2 else url
                st.markdown(f"""
                <div class="ref-card">
                    <div class="ref-title">
                        <a href="{url}" target="_blank" style="color:#e8eaf0;text-decoration:none;">
                            {title[:90]}{'...' if len(title)>90 else ''}
                        </a>
                    </div>
                    <div class="ref-url">🌐 {domain}</div>
                    {f'<div style="font-size:11px;color:#5a6478;margin-top:6px;line-height:1.5">{snippet[:180]}{"..." if len(snippet)>180 else ""}</div>' if snippet else ''}
                </div>""", unsafe_allow_html=True)