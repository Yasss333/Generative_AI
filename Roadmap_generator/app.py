import streamlit as st
from dotenv import load_dotenv
import os
import re
import json
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

st.set_page_config(
  page_title="CareerHub Roadmap",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }
.stApp { background: #070b14; color: #e8eaf0; }
.main-title {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -2px;
    background: linear-gradient(135deg, #10b981 0%, #06b6d4 50%, #8b5cf6 100%);
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
.metric-value { font-size: 1.6rem; font-weight: 800; color: #10b981; }
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
    border-left: 3px solid #10b981; border-radius: 10px;
    padding: 1rem 1.2rem; margin-bottom: 0.8rem; transition: border-color 0.2s;
}
.ref-card:hover { border-left-color: #06b6d4; }
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
.badge-ok { background: #10b98115; color: #10b981; border: 1px solid #10b98130; }
.badge-warn { background: #f59e0b15; color: #f59e0b; border: 1px solid #f59e0b30; }
.badge-err { background: #ef444415; color: #ef4444; border: 1px solid #ef444430; }
.stSpinner > div { border-top-color: #10b981 !important; }
hr { border-color: #151d2e !important; }
.streamlit-expanderHeader {
    background: #0e1420 !important; border: 1px solid #1e2d40 !important;
    border-radius: 10px !important; color: #8892a4 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or os.getenv("SERAPI_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPEN_ROUTER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHAT_MEMORY_FILE = os.path.join(os.path.dirname(__file__), "chat_memory.json")

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

def _load_chat_history():
  try:
    with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception:
    return []

def _save_chat_history(hist):
  try:
    with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as f:
      json.dump(hist, f, ensure_ascii=False, indent=2)
  except Exception:
    pass

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

def generate_roadmap_json(goal, context, difficulty, timeline):
    prompt = f"""You are an expert learning roadmap generator.
Create a structured learning roadmap for:
Goal: {goal}
Difficulty: {difficulty}
Timeline: {timeline}
Context: {context[:2000]}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "title": "Goal Title",
  "totalDuration": "{timeline}",
  "difficulty": "{difficulty}",
  "phases": [
    {{
      "id": "phase1",
      "name": "Phase 1: Foundations",
      "duration": "4 weeks",
      "nodes": [
        {{
          "id": "n1",
          "label": "Topic Name",
          "duration": "1 week",
          "type": "core",
          "description": "Brief description",
          "resources": ["resource1", "resource2"],
          "dependencies": []
        }}
      ]
    }}
  ],
  "finalProjects": [
    {{"name": "Project", "description": "Build this"}}
  ]
}}

Rules: 3-4 phases, 3-5 nodes per phase
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Output only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)

def generate_summary(goal, context, difficulty, timeline):
    prompt = f"""You are a career advisor. Create a roadmap summary for: {goal}
Difficulty: {difficulty} | Timeline: {timeline}
Context: {context[:800]}

Use markdown:
- **Overview**: 2 sentences
- **Key Phases**: bullet list
- **Must-Learn Skills**: 5-6 skills
- **Build These**: 2-3 projects
- **Timeline**: job readiness estimate"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def render_interactive_roadmap(roadmap_data):
    data_json = json.dumps(roadmap_data)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Roadmap</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ 
  width: 100%; height: 100%; 
  background: #070b14; color: #e8eaf0; 
  font-family: 'Syne', sans-serif; 
  overflow: hidden;
}}
#root {{ width: 100%; height: 100%; display: flex; flex-direction: column; }}
svg {{ background: #070b14; display: block; }}
.controls {{ padding: 14px 20px; background: #0d1320; border-bottom: 1px solid #151d2e; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; font-family: 'DM Mono', monospace; }}
.label {{ font-size: 10px; color: #2a3548; letter-spacing: 0.08em; text-transform: uppercase; }}
.btn {{ 
  padding: 6px 14px; border-radius: 8px; border: 1px solid #1e2d40; 
  background: transparent; color: #3a4558; font-size: 11px; cursor: pointer; 
  font-family: 'DM Mono', monospace; transition: all 0.3s; text-transform: uppercase;
  letter-spacing: 0.05em; font-weight: 500;
}}
.btn.active {{ background: #10b98112; color: #10b981; border-color: #10b9814d; }}
.btn:hover {{ border-color: #10b981; color: #10b981; }}
.info {{ margin-left: auto; font-size: 10px; color: #1e2d40; font-family: 'DM Mono', monospace; }}
</style>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
</head>
<body>
<div id="root">
  <div class="controls">
    <span class="label">Filter:</span>
    <button class="btn active" onclick="filterType('all')">All</button>
    <button class="btn" onclick="filterType('core')">Core</button>
    <button class="btn" onclick="filterType('optional')">Optional</button>
    <button class="btn" onclick="filterType('project')">Projects</button>
    <span class="info">Scroll to zoom • Drag to pan</span>
  </div>
  <svg id="canvas" style="flex: 1;"></svg>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script>
const ROADMAP = {data_json};
let currentFilter = 'all';

const colors = ['#10b981', '#06b6d4', '#8b5cf6', '#ec4899'];
const typeColors = {{ core: '#10b981', optional: '#f59e0b', project: '#8b5cf6' }};

function filterType(t) {{
  currentFilter = t;
  document.querySelectorAll('.btn').forEach((btn, i) => {{
    btn.classList.toggle('active', i === (t === 'all' ? 0 : ['core', 'optional', 'project'].indexOf(t) + 1));
  }});
  render();
}}

function render() {{
  const svg = d3.select('#canvas');
  svg.selectAll('*').remove();
  
  const container = document.getElementById('canvas');
  const width = container.clientWidth || 1400;
  const height = container.clientHeight || 700;
  
  svg.attr('viewBox', `0 0 ${{width}} ${{height}}`).attr('width', width).attr('height', height);
  
  const g = svg.append('g');
  const defs = svg.append('defs');
  
  const nodes = [];
  const phaseWidth = 280;
  
  ROADMAP.phases.forEach((phase, pi) => {{
    const phaseX = 120 + pi * phaseWidth;
    const phaseColor = colors[pi % colors.length];
    const phaseNodes = phase.nodes.filter(n => currentFilter === 'all' || n.type === currentFilter);
    
    // Phase header
    g.append('text')
      .attr('x', phaseX + 80).attr('y', 50)
      .attr('text-anchor', 'middle')
      .attr('font-size', '13')
      .attr('font-weight', '700')
      .attr('fill', phaseColor)
      .attr('opacity', '0.9')
      .text(phase.name.replace(/Phase \\d+: /i, '').substring(0, 20));
    
    g.append('text')
      .attr('x', phaseX + 80).attr('y', 68)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10')
      .attr('fill', '#2a3548')
      .attr('font-family', "'DM Mono', monospace")
      .text(phase.duration || '');
    
    // Vertical timeline
    g.append('line')
      .attr('x1', phaseX + 80).attr('y1', 85)
      .attr('x2', phaseX + 80).attr('y2', 600)
      .attr('stroke', phaseColor).attr('stroke-opacity', '0.15')
      .attr('stroke-width', '2').attr('stroke-dasharray', '5,5');
    
    phaseNodes.forEach((node, ni) => {{
      const nodeY = 120 + ni * 90;
      const type = node.type;
      const color = typeColors[type] || phaseColor;
      
      nodes.push({{
        id: node.id,
        label: node.label,
        duration: node.duration,
        type: type,
        phaseColor: phaseColor,
        x: phaseX + 80,
        y: nodeY,
        color: color
      }});
    }});
  }});
  
  const glow = defs.append('filter').attr('id', 'glow');
  glow.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'coloredBlur');
  const feMerge = glow.append('feMerge');
  feMerge.append('feMergeNode').attr('in', 'coloredBlur');
  feMerge.append('feMergeNode').attr('in', 'SourceGraphic');
  
  const nodeGroups = g.selectAll('.node-group')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'node-group')
    .attr('transform', d => `translate(${{d.x}}, ${{d.y}})`)
    .style('cursor', 'pointer');
  
  nodeGroups.append('circle')
    .attr('r', 28)
    .attr('fill', d => d.color)
    .attr('opacity', '0.15')
    .attr('stroke', d => d.color)
    .attr('stroke-width', '2.5')
    .on('mouseenter', function(e, d) {{
      d3.select(this)
        .transition().duration(200)
        .attr('r', 34)
        .attr('opacity', '0.35')
        .attr('filter', 'url(#glow)');
      
      g.append('text')
        .attr('class', 'tooltip-text')
        .attr('x', d.x).attr('y', d.y - 50)
        .attr('text-anchor', 'middle')
        .attr('font-size', '11')
        .attr('font-weight', '600')
        .attr('fill', d.color)
        .text(d.label.substring(0, 22));
    }})
    .on('mouseleave', function(e, d) {{
      d3.select(this)
        .transition().duration(200)
        .attr('r', 28)
        .attr('opacity', '0.15')
        .attr('filter', 'none');
      
      g.selectAll('.tooltip-text').remove();
    }});
  
  nodeGroups.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '0.35em')
    .attr('font-size', '13')
    .attr('font-weight', '700')
    .attr('fill', d => d.color)
    .text(d => d.type === 'core' ? '●' : d.type === 'optional' ? '○' : '▲');
  
  nodeGroups.append('text')
    .attr('y', 50)
    .attr('text-anchor', 'middle')
    .attr('font-size', '10')
    .attr('font-weight', '600')
    .attr('fill', '#b0b8cc')
    .style('pointer-events', 'none')
    .each(function(d) {{
      const words = d.label.split(' ');
      const line = words.slice(0, 2).join(' ').substring(0, 16);
      d3.select(this).text(line);
    }});
  
  nodeGroups.append('text')
    .attr('y', 65)
    .attr('text-anchor', 'middle')
    .attr('font-size', '8')
    .attr('fill', '#2a3548')
    .attr('font-family', "'DM Mono', monospace")
    .style('pointer-events', 'none')
    .text(d => d.duration || '');
  
  const zoom = d3.zoom().scaleExtent([0.5, 2.5]).on('zoom', e => {{
    g.attr('transform', e.transform);
  }});
  svg.call(zoom);
}}

window.addEventListener('resize', render);
render();
</script>
</body>
</html>"""
    st.components.v1.html(html, height=750, scrolling=False)

st.markdown('<div class="main-title">🧭 CareerHub Roadmap</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">// enter a goal · get a visual learning path</div>', unsafe_allow_html=True)

chat_history = _load_chat_history()
for m in chat_history:
  if m.get("role") and m.get("content"):
    try:
      st.chat_message(m["role"]).write(m["content"])
    except Exception:
      pass

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
    st.caption("D3.js · GPT-4o-mini · SerpAPI")

user_input = st.chat_input("Enter your goal (e.g. Full Stack Developer, ML Engineer, iOS Dev...)")

if user_input:
  st.chat_message("user").write(user_input)
  try:
    chat_history.append({"role": "user", "content": user_input})
    _save_chat_history(chat_history)
  except Exception:
    pass

  with st.chat_message("assistant"):
    assistant_content = ""

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

      st.markdown('<div class="section-header"><h3>📊 Interactive Roadmap</h3></div>', unsafe_allow_html=True)
      render_interactive_roadmap(roadmap_data)

      try:
        assistant_content += f"Roadmap generated for: {user_input}\nPhases: {len(phases)}, Topics: {total_nodes}\n"
      except Exception:
        pass

      with st.expander("🗂 Raw Roadmap Data (JSON)"):
        st.json(roadmap_data)

    if show_summary:
      with st.spinner("📝 Writing summary..."):
        summary = generate_summary(user_input, context, difficulty, timeline)
      st.markdown('<div class="section-header"><h3>📋 Roadmap Summary</h3></div>', unsafe_allow_html=True)
      st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
      try:
        assistant_content += f"Summary:\n{summary}\n"
      except Exception:
        pass

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

    if show_refs and search_results:
      st.markdown('<div class="section-header"><h3>🔗 Reference Sources</h3></div>', unsafe_allow_html=True)
      for item in search_results:
        title = item.get("title", item["url"])
        snippet = item.get("snippet", "")
        url = item["url"]
        domain = url.split("/")[2] if len(url.split("/")) > 2 else url
        
        snippet_html = f'<div style="font-size:11px;color:#5a6478;margin-top:6px;line-height:1.5">{snippet[:180]}{"..." if len(snippet)>180 else ""}</div>' if snippet else ''
        
        st.markdown(f"""
        <div class="ref-card">
          <div class="ref-title">
            <a href="{url}" target="_blank" style="color:#e8eaf0;text-decoration:none;">
              {title[:90]}{'...' if len(title)>90 else ''}
            </a>
          </div>
          <div class="ref-url">🌐 {domain}</div>
          {snippet_html}
        </div>""", unsafe_allow_html=True)

    try:
      if assistant_content:
        chat_history.append({"role": "assistant", "content": assistant_content})
        _save_chat_history(chat_history)
    except Exception:
      pass