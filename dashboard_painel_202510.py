# CV Dashboard – Streamlit (Responsivo + Auto-Compact + Título Externo)
# Author: Murillo Martins
# -------------------------------------------------
# Como usar:
# 1) Salve como app.py
# 2) (Opcional) venv: python -m venv .venv && .venv/Scripts/activate (Win) | source .venv/bin/activate (macOS/Linux)
# 3) Rode: streamlit run app.py
# -------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from PIL import Image
import json
import io
import streamlit.components.v1 as components

# -----------------------------
# CONFIG GERAL
# -----------------------------
st.set_page_config(
    page_title="Murillo Martins | Painel Profissional",
    page_icon="🤘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- FONTES (Google Fonts) ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue:wght@400..700&family=Oswald:wght@300;400;500;600;700&family=Inter:wght@400;600;700&display=swap');
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DADOS (edite aqui)
# -----------------------------
PROFILE = {
    "name": "Murillo Martins",
    "headline": "Data Analyst | Data Science | Marketing | Analytics",
    "location": "São Paulo, Brasil",
    "email": "murilomartins09@gmail.com",
    "site": "https://www.murillomartins.com.br",
    "linkedin": "https://www.linkedin.com/in/murillomartins101",
    "github": "https://github.com/murillomartins101",
    "bio": ("Analista de Dados, com mais de 15 anos de experiência em marketing, "
            "inteligência comercial e estratégia.")
}

EXPERIENCES = [
    {
        "company": "Honda Brasil",
        "role": "Cientista/Analista de Dados",
        "start": "2025-03",
        "end": None,
        "city": "São Paulo",
        "achievements": [
            "Dataviz para análise de produtividade e performance",
            "Dashboards executivos de carteira e inadimplência",
            "Estratégias orientadas a dados para crescimento",
        ],
        "skills": ["Python", "SQL", "Power BI", "ML"],
    },
    {
        "company": "Honda Brasil",
        "role": "Analista de Operações Internacionais",
        "start": "2023-04",
        "end": "2025-02",
        "city": "São Paulo / LATAM",
        "achievements": [
            "Gestão de distribuidores (Ecuador, Colômbia, Panamá, Suriname, Venezuela)",
            "Planejamento comercial, pricing e expansão de portfólio",
        ],
        "skills": ["Comercial", "Planejamento", "Pricing", "LATAM"],
    },
    {
        "company": "Honda Brasil",
        "role": "Consultor Comercial",
        "start": "2019-06",
        "end": "2023-03",
        "city": "São Paulo",
        "achievements": [
            "Gestão de Concessionárias 4 rodas e 2 rodas (Brasil)",
            "Marketing, Produtos Financeiros, Vendas, Planejamento comercial, pricing e expansão de portfólio",
        ],
        "skills": ["Marketing", "Comercial", "Planejamento", "Pricing", "LATAM"],
    },
    {
        "company": "Aditivo Media",
        "role": "Founder | Head of Everything",
        "start": "2015-06",
        "end": "2019-06",
        "city": "São Paulo",
        "achievements": [
            "Mais de 100k visitas orgânicas em projetos de clientes",
            "Campanhas de performance e conteúdos data-driven",
        ],
        "skills": ["Marketing", "Growth", "SEO", "Paid Media", "Branding"],
    },
    {
        "company": "CNH Industrial Capital",
        "role": "Field Representative",
        "start": "2011-09",
        "end": "2015-06",
        "city": "São Paulo",
        "achievements": ["Forecast de vendas e inteligência de mercado"],
        "skills": [
            "Serviços Financeiros", "BNDES",
            "Financiamento de Caminhões, Máquinas Agrícolas e Máquinas de Construção",
            "Forecast", "BI"
        ],
    },
    {
        "company": "Banco Mercedes-Benz",
        "role": "Analista de F&I",
        "start": "2010-01",
        "end": "2011-09",
        "city": "São Paulo",
        "achievements": ["Campanhas de aquisição e retenção"],
        "skills": ["Marketing", "Analytics", "CRM", "Serviços Financeiros", "BNDES", "Financiamento de Caminhões e Ônibus", "Forecast", "BI"],
    },
]

PROJECTS = [
    {
        "title": "Churn Prediction – Waze App (case educacional)",
        "summary": "Pipeline de ML para prever evasão e priorizar retenção.",
        "metrics": {"AUC": 0.87, "Lift@10%": 3.2},
        "tags": ["Python", "Scikit-learn", "EDA", "Feature Eng."],
        "link": "https://github.com/seuusuario/churn-waze",
    },
    {
        "title": "Credit Risk Dashboard – Banco Honda",
        "summary": "Visualização executiva de KPIs de carteira e inadimplência.",
        "metrics": {"Tempo de análise": "-35%"},
        "tags": ["Power BI", "SQL", "DAX"],
        "link": "https://seusite.com/credit-risk",
    },
    {
        "title": "RockBuzz – Conteúdo & Growth (YouTube)",
        "summary": "Estratégia de conteúdo para covers e shows ao vivo.",
        "metrics": {"Views": "250k+", "CTR": "6.5%"},
        "tags": ["YouTube", "SEO", "Analytics"],
        "link": "https://www.youtube.com/@bandarockbuzz",
    },
]

EDUCATION = [
    {"title": "Ciência da Computação (em andamento)", "org": "UniAnchieta", "year": "2025"},
    {"title": "Power BI Analyst Certificate", "org": "Microsoft", "year": "2024"},
    {"title": "Google Advanced Data Analytics Certificate", "org": "Google", "year": "2024"},
    {"title": "Google Data Analytics Certificate", "org": "Google", "year": "2023"},
    {"title": "Digital Marketing Specialization", "org": "University of Illinois Urbana-Champaign", "year": "2020"},
    {"title": "MBA em Comércio Exterior", "org": "UniAnchieta", "year": "2012"},
    {"title": "B.Tech em Marketing", "org": "UniAnchieta", "year": "2010"},
]

# Habilidades (0–100)
SKILLS_CORE = {
    # Estratégia e Comunicação
    "Comunicação": 92,
    "Storytelling": 90,
    "Marketing & Growth": 88,
    "Gestão de Projetos": 80,

    # Dados e Análise
    "Análise de Dados": 90,
    "Power BI": 88,
    "Python": 85,
    "SQL": 75,

    # Estatística e Modelagem
    "Estatística": 70,
    "Machine Learning": 68,
}

SKILLS_TOOLS = {
    # Bibliotecas Python
    "Pandas": 90,
    "Scikit-learn": 82,
    "Plotly": 85,
    "Matplotlib": 80,
    "Streamlit": 75,

    # Ecossistema Microsoft
    "Excel": 95,
    "DAX": 82,
    "M (Power Query)": 78,
    "PowerPoint": 88,
}

LANGUAGES = {"Português": 100, "Inglês": 85, "Espanhol": 70, "Alemão": 30}

MUSIC = [
    {"title": "Rolling Stones – Jumpin’ Jack Flash | Performance by Murillo Martins at The Cavern Club, Liverpool", "url": "https://www.youtube.com/watch?v=v8o4fG5cF0Y"},
    {"title": "Iron Maiden – Wasted Years | Drum Cover by Murillo Martins", "url": "https://www.youtube.com/watch?v=9eR7HhZlBok"},
]

# -----------------------------
# THEME HELPERS (PLOTLY + CSS)
# -----------------------------
PRIMARY = "#22d3ee"
INK = "#0a0a0a"
GRAPHITE = "#111317"
SLATE = "#cbd5e1"
MUTE = "#94a3b8"
ACCENT = PRIMARY

def apply_grunge_theme(fig, title=None, compact=False):
    """
    Título interno não é usado. Os títulos serão externos (chart_heading).
    No mobile (compact=True) a legenda desce para baixo e margens são ajustadas.
    """
    tick_size = 9 if compact else 11
    legend_size = 9 if compact else 12

    legend_cfg = dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.10)",
        borderwidth=0.5,
        font=dict(size=legend_size, color=SLATE),
        itemclick="toggleothers",
        itemdoubleclick="toggle",
    )
    if compact:
        legend_cfg.update(dict(orientation="h", x=0, y=-0.2, yanchor="top"))  # legenda embaixo
        top_margin = 8
        bottom_margin = 40
    else:
        legend_cfg.update(dict(orientation="h", x=0, y=1.02, yanchor="bottom"))  # legenda em cima
        top_margin = 12
        bottom_margin = 12

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=GRAPHITE, plot_bgcolor=GRAPHITE,
        font=dict(family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial",
                  size=(11 if compact else 13), color=SLATE),
        margin=dict(l=8 if compact else 12, r=8 if compact else 12,
                    t=top_margin, b=bottom_margin),
        legend=legend_cfg,
        bargap=0.25,
        colorway=[ACCENT, "#60a5fa", "#f472b6", "#34d399", "#f59e0b", "#a78bfa", "#ef4444", "#22c55e"],
    )
    fig.update_xaxes(
        automargin=True,
        gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", tickfont=dict(color=SLATE, size=tick_size),
        title=dict(font=dict(color=MUTE, size=tick_size)),
    )
    fig.update_yaxes(
        automargin=True,
        gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", tickfont=dict(color=SLATE, size=tick_size),
        title=dict(font=dict(color=MUTE, size=tick_size)),
    )
    return fig

# -----------------------------
# CSS GLOBAL (responsivo)
# -----------------------------
st.markdown(f"""
<style>
:root {{
  --ink: {INK}; --graphite: {GRAPHITE}; --slate: {SLATE}; --mute: {MUTE}; --accent: {ACCENT};
  --radius: 14px;
  --card-bg: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  --texture: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
             radial-gradient(rgba(255,255,255,0.02) 1px, transparent 1px);
}}
html, body, [data-testid="stAppViewContainer"] {{
  background: linear-gradient(180deg, #0b0d11 0%, #0b0d11 40%, #0a0c10 100%), var(--texture);
  background-size: 3px 3px, 5px 5px;
  overflow-x: hidden;
}}
/* Tabs pegajosas só em telas maiores */
div[role="tablist"] {{
  position: sticky; top: 62px; z-index: 5; padding: 6px 0 0 0;
  background: linear-gradient(180deg, rgba(11,13,17,.95), rgba(11,13,17,.80));
  backdrop-filter: blur(2px);
  border-bottom: 1px solid rgba(255,255,255,.08);
}}
@media (max-width: 640px) {{
  div[role="tablist"] {{ position: static; top: auto; }}
}}

section.main > div {{ padding-top: .4rem; }}

/* Títulos do app (não dos gráficos) com clamp */
h1, h2, h3 {{
  font-family: "Bebas Neue", "Oswald", Impact, system-ui, sans-serif !important;
  font-weight: 900 !important; letter-spacing: .5px; text-transform: uppercase;
  color: {SLATE}; text-shadow: 0 0 6px rgba(34,211,238,.15);
}}
h1 {{ font-size: clamp(22px, 6vw, 40px); }}
h2 {{ font-size: clamp(18px, 4.8vw, 32px); }}
h3 {{ font-size: clamp(16px, 4.2vw, 26px); }}
h1::after {{
  content:""; display:block; height:3px; margin-top:8px;
  background: linear-gradient(90deg, var(--accent), rgba(34,211,238,0));
  filter: drop-shadow(0 0 6px rgba(34,211,238,.35));
}}

/* KPIs */
.kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 8px 0 6px 0; }}
@media (max-width: 1200px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 640px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}
.kpi {{
  padding: 12px 14px; border-radius: var(--radius);
  border: 1px solid rgba(255,255,255,.12);
  background: radial-gradient(120% 100% at 0% 0%, rgba(34,211,238,0.08), rgba(34,211,238,0.02)), var(--card-bg);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03);
}}
.kpi small {{ font-size:12px; color: {MUTE}; letter-spacing:.6px }}
.kpi b {{ font-size:22px; color: {SLATE} }}

/* Cards base */
.card {{
  border-radius: 16px; border: 1px solid rgba(255,255,255,0.10);
  background: var(--card-bg), var(--texture);
  background-size: 100% 100%, 4px 4px, 5px 5px;
  padding: 14px 16px; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
}}

/* Tabs */
div[role="tab"] {{
  font-size: 15px !important; font-weight: 800;
  color: #93a3b8 !important; padding: 8px 8px 12px 8px; position: relative;
  text-transform: uppercase; letter-spacing:.6px;
}}
div[role="tab"][aria-selected="true"] {{
  color: var(--accent) !important; filter: drop-shadow(0 0 4px rgba(34,211,238,.35));
}}
div[role="tab"][aria-selected="true"]::after {{
  content: ""; position: absolute; left: 6px; right: 6px; bottom: -6px; height: 3px;
  background: linear-gradient(90deg, var(--accent), rgba(34,211,238,0)); border-radius: 2px;
}}

/* Projetos */
.proj-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
@media (max-width: 1200px) {{ .proj-grid {{ grid-template-columns: 1fr; }} }}
.proj-card {{
  border-radius: 16px; border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
  padding: 14px 16px; display:flex; flex-direction:column; gap:8px;
}}
.proj-title {{ font-family: "Bebas Neue","Oswald",Impact,sans-serif; font-size: clamp(18px, 4.4vw, 22px); letter-spacing:.5px; margin:0; color:{SLATE}; }}
.proj-desc {{ color:{SLATE}; opacity:.9; margin: 0 0 6px 0; }}
.proj-metrics {{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:12px; }}
@media (max-width: 900px) {{ .proj-metrics {{ grid-template-columns:1fr; }} }}
.proj-kpi {{ border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:10px 12px;
  background: radial-gradient(120% 100% at 0% 0%, rgba(34,211,238,0.08), rgba(34,211,238,0.02)); }}
.proj-footer {{ display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; }}

/* Música */
.music-grid{{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:8px; }}
@media (max-width: 900px){{ .music-grid{{ grid-template-columns:1fr; }} }}
.music-card{{ border:1px solid rgba(255,255,255,.10); border-radius:16px;
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
  padding:12px 14px; display:flex; flex-direction:column; gap:10px;
}}
.music-title{{ min-width:0; font-family:"Bebas Neue","Oswald",Impact,sans-serif;
  font-size: clamp(18px, 5.2vw, 28px); letter-spacing:.4px; color:#cbd5e1; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.music-thumb{{ display:block; width:100%; aspect-ratio:16/9;
  border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,.10);
  background-position:center; background-size:cover; background-repeat:no-repeat;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def ym_to_date(ym: str) -> datetime:
    return datetime.strptime(ym + "-01", "%Y-%m-%d")

def build_experience_df(items):
    rows, today = [], datetime.today()
    for i in items:
        start = ym_to_date(i["start"]) if isinstance(i["start"], str) else i["start"]
        end = ym_to_date(i["end"]) if i["end"] else today
        rows.append({
            "Empresa": i["company"], "Cargo": i["role"], "Início": start, "Fim": end,
            "Cidade": i.get("city", ""), "Duração": relativedelta(end, start),
            "Desc": " • ".join(i.get("achievements", [])),
        })
    return pd.DataFrame(rows).sort_values("Início", ascending=False)

def _fmt_duration(rd: relativedelta) -> str:
    y, m = rd.years, rd.months
    parts = ([] if not y else [f"{y}a"]) + ([] if not m else [f"{m}m"])
    return " ".join(parts) if parts else "0m"

def timeline_chart(df: pd.DataFrame, compact=False):
    df = df.copy()
    df["Duracao_str"] = df["Duração"].apply(_fmt_duration)
    df["Label"] = df["Cargo"] + " • " + df["Duracao_str"]

    role_palette = {
        "Cientista/Analista de Dados": "#1fbad6",
        "Analista de Operações Internacionais": "#2563eb",
        "Consultor Comercial": "#fda4af",
        "Founder | Head of Everything": "#ef4444",
        "Field Representative": "#34d399",
        "Analista de F&I": "#86efac",
    }

    y_order = list(df["Empresa"].unique())

    fig = px.timeline(
        df,
        x_start="Início", x_end="Fim", y="Empresa",
        color="Cargo", color_discrete_map=role_palette,
        category_orders={"Empresa": y_order},
        custom_data=df[["Empresa","Cargo","Cidade","Início","Fim","Duracao_str","Desc"]],
        title=None,
    )
    fig.update_traces(
        marker=dict(line=dict(color="rgba(255,255,255,0.14)", width=1)),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Cargo: %{customdata[1]}<br>"
            "Cidade: %{customdata[2]}<br>"
            "Período: %{customdata[3]|%b %Y} – %{customdata[4]|%b %Y}<br>"
            "Duração: %{customdata[5]}<br><br>%{customdata[6]}<extra></extra>"
        ),
    )
    fig.update_yaxes(autorange="reversed", title=None)
    fig.update_xaxes(tickformat="%Y", dtick="M12", title=None, showgrid=True, automargin=True)
    apply_grunge_theme(fig, compact=compact)
    fig.update_layout(height=(320 if compact else 420), autosize=True)
    return fig

def radar_chart(skills: dict, compact=False):
    labels = list(skills.keys()) + [list(skills.keys())[0]]
    values = list(skills.values()) + [list(skills.values())[0]]
    fig = go.Figure([go.Scatterpolar(
        r=values, theta=labels, fill="toself",
        line=dict(color=ACCENT, width=3), marker=dict(size=6),
        fillcolor="rgba(34,211,238,0.18)"
    )])
    fig.update_layout(
        polar=dict(
            bgcolor=GRAPHITE,
            angularaxis=dict(tickfont=dict(size=(10 if compact else 12), color=SLATE),
                             linecolor="rgba(255,255,255,0.15)", linewidth=1),
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=(9 if compact else 11), color=SLATE),
                            gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)", linewidth=1),
        ),
        showlegend=False,
    )
    apply_grunge_theme(fig, compact=compact)
    fig.update_layout(height=(300 if compact else 380))
    return fig

def bar_chart(skills: dict, compact=False):
    df = pd.DataFrame({"Skill": list(skills.keys()), "Nível": list(skills.values())})
    fig = px.bar(df, x="Nível", y="Skill", orientation="h", title=None)
    fig.update_traces(marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.18)")),
                      hovertemplate="<b>%{y}</b><br>Nível: %{x}<extra></extra>")
    apply_grunge_theme(fig, compact=compact)
    fig.update_layout(height=(300 if compact else 380))
    return fig

def kpi_badge(label: str, value: str):
    st.markdown(f"<div class='kpi'><small>{label}</small><br><b>{value}</b></div>", unsafe_allow_html=True)

def project_card_html(p: dict) -> str:
    parts = []
    parts.append("<div class='proj-card'>")
    parts.append(f"<h4 class='proj-title'>{p['title']}</h4>")
    if p.get("summary"):
        parts.append(f"<p class='proj-desc'>{p['summary']}</p>")
    metrics = p.get("metrics") or {}
    if metrics:
        parts.append("<div class='proj-metrics'>")
        for k, v in metrics.items():
            parts.append(f"<div class='proj-kpi'><small>{k}</small><br><b>{v}</b></div>")
        parts.append("</div>")
    tags = ", ".join(p.get("tags", [])) or "-"
    link_html = f"<a href='{p.get('link')}' target='_blank' rel='noopener'>Abrir projeto</a>" if p.get("link") else ""
    parts.append("<div class='proj-footer'>")
    parts.append(f"<div class='proj-tags'>Tags: {tags}</div>")
    parts.append(f"<div class='proj-link'>{link_html}</div>")
    parts.append("</div>")
    parts.append("</div>")
    return "".join(parts)

def youtube_id_from_url(url: str):
    try:
        u = urlparse(url)
        if u.netloc in ("youtu.be", "www.youtu.be"):
            return u.path.strip("/")
        if "youtube.com" in u.netloc:
            qs = parse_qs(u.query)
            if "v" in qs: return qs["v"][0]
            parts = u.path.split("/")
            if "embed" in parts and len(parts) >= 3:
                return parts[parts.index("embed")+1]
    except Exception:
        pass
    return None

def render_music_card(item: dict, inline_play_default=False):
    title, url = item.get("title",""), item.get("url","")
    vid = youtube_id_from_url(url)

    st.markdown("<div class='music-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='music-title'>{title}</div>", unsafe_allow_html=True)

    if vid:
        thumb_url = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        st.markdown(
            f"<a href='{url}' target='_blank' rel='noopener' class='music-thumb' "
            f"aria-label='Abrir no YouTube' style='background-image:url({thumb_url});'></a>",
            unsafe_allow_html=True
        )
        with st.expander("▶️ Tocar aqui", expanded=inline_play_default):
            st.video(url)
    else:
        st.info("Vídeo não reconhecido — verifique a URL.")

    st.markdown(
        f"<div class='music-actions'><span></span>"
        f"<a href='{url}' target='_blank' rel='noopener'>Assistir no YouTube</a></div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# COMPONENTE DE TÍTULO EXTERNO PARA GRÁFICOS
# -----------------------------
def chart_heading(text: str):
    st.markdown(f"""
    <div style="
      font-family:'Bebas Neue','Oswald',Impact,system-ui,sans-serif;
      font-weight:900; letter-spacing:.5px; text-transform:uppercase;
      color:#cbd5e1; text-shadow:0 0 6px rgba(34,211,238,.15);
      margin: 4px 0 8px 0;
      font-size: clamp(18px, 5.5vw, 28px);
    ">{text}</div>
    """, unsafe_allow_html=True)

# -----------------------------
# AUTO-DETECÇÃO DO MODO COMPACTO (via viewport)
# Se a tela < 768px: ativa ?compact=1; se > 992px: remove.
# Usa sessionStorage para não entrar em loop.
# -----------------------------
components.html("""
<script>
(function() {
  try {
    const w = window.innerWidth || document.documentElement.clientWidth;
    const url = new URL(window.location.href);
    const qsHas = url.searchParams.has('compact');
    const qsVal = url.searchParams.get('compact');
    const key = 'compactApplied';

    const shouldCompact = (w < 768);
    const shouldDesktop = (w > 992);

    if (shouldCompact && (!qsHas || (qsVal !== '1'))) {
      if (!sessionStorage.getItem(key)) {
        url.searchParams.set('compact','1');
        sessionStorage.setItem(key, '1');
        window.location.replace(url.toString());
      }
    } else if (shouldDesktop && qsHas && (qsVal === '1')) {
      if (!sessionStorage.getItem(key)) {
        url.searchParams.delete('compact');
        sessionStorage.setItem(key, '1');
        window.location.replace(url.toString());
      }
    } else {
      sessionStorage.removeItem(key);
    }
  } catch(e) { /* silencioso */ }
})();
</script>
""", height=0)

# -----------------------------
# MODO COMPACTO (query string + toggle)
# -----------------------------
try:
    compact_qs = st.query_params.get("compact", None)
    IS_COMPACT = str(compact_qs).lower() in ("1", "true", "yes")
except Exception:
    IS_COMPACT = "compact" in st.experimental_get_query_params()

with st.sidebar:
    IS_COMPACT = st.toggle("📱 Modo compacto (mobile)", value=IS_COMPACT,
                           help="Reduz alturas/ fontes para telas pequenas")

# -----------------------------
# SIDEBAR (perfil)
# -----------------------------
with st.sidebar:
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)

    # --- Caminhos possíveis + fallback para GitHub RAW ---
    GITHUB_RAW_URL = (
        "https://raw.githubusercontent.com/murillomartins101/painel_profissional/main/"
        "painel_profissional/profile.jpg"
    )

    PHOTO_CANDIDATES = [
        Path(__file__).parent / "assets" / "profile.jpg",
        Path(__file__).parent / "painel_profissional" / "profile.jpg",
        Path(__file__).parent / "profile.jpg",
    ]

    @st.cache_data(show_spinner=False)
    def resolve_profile_photo() -> str:
        """Retorna caminho local se existir; senão, URL RAW do GitHub."""
        for p in PHOTO_CANDIDATES:
            if p.exists():
                return str(p)
        return GITHUB_RAW_URL

    # --- Usa a função para definir o caminho ---
    photo_src = resolve_profile_photo()

    # --- Exibe a imagem ou mensagem de erro ---
    try:
        if photo_src.startswith("http"):
            st.image(photo_src, use_container_width=True)
        else:
            st.image(Image.open(photo_src), use_container_width=True)
    except Exception as e:
        st.markdown(
            "<div style='height:180px;display:flex;align-items:center;justify-content:center;"
            "border-radius:12px;background:rgba(255,255,255,.05);color:#aaa;font-size:14px;'>"
            f"📸 Erro ao carregar imagem ({e})</div>",
            unsafe_allow_html=True
        )

    st.markdown(f"<div class='profile-name'>{PROFILE['name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='profile-headline'>{PROFILE['headline']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='profile-sep'></div>", unsafe_allow_html=True)

    st.markdown("<div class='profile-meta'>", unsafe_allow_html=True)
    st.markdown(f"<div>📍 {PROFILE['location']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div>✉️ <a href='mailto:{PROFILE['email']}'>{PROFILE['email']}</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='profile-links'>", unsafe_allow_html=True)
    st.markdown(f"<a href='{PROFILE['linkedin']}' target='_blank' rel='noopener'>LinkedIn</a>", unsafe_allow_html=True)
    st.markdown(f"<a href='{PROFILE['github']}' target='_blank' rel='noopener'>GitHub</a>", unsafe_allow_html=True)
    st.markdown(f"<a href='{PROFILE['site']}' target='_blank' rel='noopener'>Site</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='profile-bio'>{PROFILE['bio']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# HEADER + KPIs
# -----------------------------
st.title("Painel Profissional")
st.write(PROFILE["headline"])

st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if EXPERIENCES:
        first_start = datetime.strptime(EXPERIENCES[-1]["start"] + "-01", "%Y-%m-%d")
        total_years = relativedelta(datetime.today(), first_start)
        kpi_badge("Experiência total", f"{total_years.years}a {total_years.months}m")
with c2:
    kpi_badge("Projetos Destaque", str(len(PROJECTS)))
with c3:
    kpi_badge("Certificações", str(len([e for e in EDUCATION if "Google" in e["title"] or "Cert" in e["title"]])))
with c4:
    kpi_badge("Idiomas", ", ".join(LANGUAGES.keys()))
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# ABAS
# -----------------------------
aba_overview, aba_timeline, aba_skills, aba_projects, aba_edu, aba_music, aba_export = st.tabs(
    ["Visão Geral", "Linha do Tempo", "Habilidades", "Projetos", "Edu & Certs", "Música", "Exportar"]
)

with aba_overview:
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("### Resumo")
        st.markdown(f"<div class='card'>{PROFILE['bio']}</div>", unsafe_allow_html=True)
        st.markdown("### Pontos-chave")
        st.markdown("""
<div class="card">
<ul>
<li><b>Análise de Dados e Estratégia Comercial</b></li>
<li><b>Modelagem preditiva</b>, <b>dashboards executivos</b> e <b>crescimento data-driven</b></li>
<li>Criatividade aplicada em <b>música</b> e <b>conteúdo</b></li>
</ul>
</div>
""", unsafe_allow_html=True)
    with right:
        chart_heading("Proficiência de Idiomas")
        lang_df = pd.DataFrame({"Idioma": list(LANGUAGES.keys()), "Nível": list(LANGUAGES.values())})
        fig_lang = px.bar(lang_df, x="Idioma", y="Nível", title=None)
        fig_lang.update_traces(marker_line_width=0.6, marker_line_color="rgba(255,255,255,0.22)")
        apply_grunge_theme(fig_lang, compact=IS_COMPACT)
        st.plotly_chart(fig_lang, use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_timeline:
    st.subheader("Experiência Profissional")
    df_exp = build_experience_df(EXPERIENCES)
    df_show = df_exp.copy()
    df_show["Início"] = df_show["Início"].dt.strftime("%Y-%m")
    df_show["Fim"] = df_show["Fim"].dt.strftime("%Y-%m")
    st.dataframe(df_show[["Empresa", "Cargo", "Cidade", "Início", "Fim"]],
                 use_container_width=True, hide_index=True, height=(260 if IS_COMPACT else 360))
    chart_heading("Linha do Tempo Profissional")
    st.plotly_chart(timeline_chart(df_exp, compact=IS_COMPACT), use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_skills:
    st.subheader("Habilidades Técnicas e de Negócio")
    c1, c2 = st.columns(2)
    with c1:
        chart_heading("Competências Centrais")
        st.plotly_chart(radar_chart(SKILLS_CORE, compact=IS_COMPACT),
                        use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})
    with c2:
        chart_heading("Ferramentas & Bibliotecas")
        st.plotly_chart(bar_chart(SKILLS_TOOLS, compact=IS_COMPACT),
                        use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_projects:
    st.subheader("Projetos em Destaque")
    grid_html = "<div class='proj-grid'>" + "".join(project_card_html(p) for p in PROJECTS) + "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

with aba_edu:
    st.subheader("Educação & Certificações")
    edu_df = pd.DataFrame(EDUCATION)
    st.dataframe(edu_df, use_container_width=True, hide_index=True, height=(240 if IS_COMPACT else 320))

    df = edu_df.copy()

    def infer_type(title, org):
        t = (title or "").lower()
        if "cert" in t or "certificate" in t or org in ("Google", "Microsoft"):
            return "Certificação"
        return "Graduação/Pós"

    df["type"] = df.apply(lambda r: infer_type(r.get("title",""), r.get("org","")), axis=1)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"]).sort_values("year")
    df["start"] = pd.to_datetime(df["year"].astype(int).astype(str) + "-01-01")
    df["end"] = df["start"] + pd.to_timedelta(180, unit="D")

    counts = df.groupby(["year", "type"]).size().reset_index(name="qtde")
    fig_edu_bar = px.bar(counts, x="year", y="qtde", color="type",
                         barmode="stack", category_orders={"type": ["Graduação/Pós", "Certificação"]})
    fig_edu_bar.update_traces(marker_line_width=0.6, marker_line_color="rgba(255,255,255,0.18)")
    chart_heading("Formações por Ano")
    apply_grunge_theme(fig_edu_bar, compact=IS_COMPACT)
    fig_edu_bar.update_layout(xaxis_title="Ano", yaxis_title="Quantidade", height=(300 if IS_COMPACT else 340))
    fig_edu_bar.update_xaxes(tickangle=0)
    st.plotly_chart(fig_edu_bar, use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False, "responsive": True})

    fig_edu_tl = px.timeline(df, x_start="start", x_end="end", y="title",
                             color="type", hover_data={"org": True, "year": True, "type": True})
    fig_edu_tl.update_yaxes(autorange="reversed", title=None)
    fig_edu_tl.update_xaxes(tickformat="%Y", title=None, dtick="M12", tickangle=0)
    fig_edu_tl.update_traces(marker=dict(line=dict(color="rgba(255,255,255,0.14)", width=1)))
    chart_heading("Linha do Tempo – Educação & Certificações")
    apply_grunge_theme(fig_edu_tl, compact=IS_COMPACT)
    fig_edu_tl.update_layout(height=(360 if IS_COMPACT else 460))
    st.plotly_chart(fig_edu_tl, use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_music:
    st.subheader("Música & Vídeos")
    st.write("Seleção de vídeos e registros de shows.")
    st.markdown("<div class='music-grid'>", unsafe_allow_html=True)
    for m in MUSIC:
        with st.container():
            render_music_card(m, inline_play_default=False)
    st.markdown("</div>", unsafe_allow_html=True)

with aba_export:
    st.subheader("Exportar & Instruções de Publicação")
    st.markdown("""
- Publique no **Streamlit Community Cloud** e incorpore no Wix via **iframe**.
- Caso precise controle corporativo, recrie versão em **Power BI** para embed interno.
    """)
    export_payload = {
        "profile": PROFILE,
        "experiences": EXPERIENCES,
        "projects": PROJECTS,
        "education": EDUCATION,
        "skills_core": SKILLS_CORE,
        "skills_tools": SKILLS_TOOLS,
        "languages": LANGUAGES,
        "music": MUSIC,
    }
    buffer = io.BytesIO()
    buffer.write(json.dumps(export_payload, ensure_ascii=False, indent=2).encode("utf-8"))
    st.download_button("Baixar dados (JSON)", buffer.getvalue(), "cv_dashboard_data.json", "application/json")

st.caption("Aditivo Media © 2025.")
