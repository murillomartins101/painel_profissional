# CV Dashboard – Streamlit (Responsivo)
# Author: Murillo Martins
# -------------------------------------------------
# Como usar:
# 1) Salve como app.py
# 2) (Opcional) venv: python -m venv .venv && .venv/Scripts/activate (Win) | source .venv/bin/activate (macOS/Linux)
# 3) Rode: streamlit run "C:\Users\muril\OneDrive\01 - Projetos\07 - Streamlit\Dashboard Painel Profissional\dashboard_painel_202510.py"
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
        "role": "Analista de Dados",
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
        "role": "Consultor Comercial",
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
        "role": "Consultor Comercial",
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
    "Comunicação": 100, "Marketing & Growth": 95, "Storytelling": 92,
    "Análise de Dados": 90, "Power BI": 88, "Python": 90,
    "SQL": 85, "Machine Learning": 60, "Estatística": 55,
}
SKILLS_TOOLS = {
    "Pandas": 90, "Scikit-learn": 82, "Plotly": 85, "Matplotlib": 80,
    "Excel": 95, "DAX": 78, "M (Power Query)": 72,
    "Google Analytics": 88, "YouTube Analytics": 80, "PowerPoint": 90,
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

def apply_grunge_theme(fig, title=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=GRAPHITE, plot_bgcolor=GRAPHITE,
        font=dict(family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial", size=13, color=SLATE),
        title=dict(
            text=title, x=0.5, xanchor="center",
            font=dict(family="Bebas Neue, Oswald, Impact, sans-serif", size=24, color=SLATE)
        ) if title else None,
        margin=dict(l=12, r=12, t=50, b=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.10)", borderwidth=0.5,
            orientation="h", yanchor="bottom", y=1.02, x=0,
            font=dict(size=12, color=SLATE), itemclick="toggleothers", itemdoubleclick="toggle"
        ),
        bargap=0.25,
        colorway=[ACCENT, "#60a5fa", "#f472b6", "#34d399", "#f59e0b", "#a78bfa", "#ef4444", "#22c55e"],
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", tickfont=dict(color=SLATE, size=11),
        title=dict(font=dict(color=MUTE, size=11))
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", tickfont=dict(color=SLATE, size=12),
        title=dict(font=dict(color=MUTE, size=11))
    )
    return fig

# -----------------------------
# CSS GLOBAL + PROJETOS + MÚSICA + PERFIL (Responsivo)
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
}}
div[role="tablist"] {{
  position: sticky; top: 62px; z-index: 5; padding: 6px 0 0 0;
  background: linear-gradient(180deg, rgba(11,13,17,.95), rgba(11,13,17,.80));
  backdrop-filter: blur(2px);
  border-bottom: 1px solid rgba(255,255,255,.08);
}}
section.main > div {{ padding-top: .4rem; }}

h1, h2, h3 {{
  font-family: "Bebas Neue", "Oswald", Impact, system-ui, sans-serif !important;
  font-weight: 900 !important; letter-spacing: .5px; text-transform: uppercase;
  color: {SLATE}; text-shadow: 0 0 6px rgba(34,211,238,.15);
}}
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
  font-size: 16px !important; font-weight: 800;
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
  padding: 14px 16px; display:flex; flex-direction:column; gap:8px; min-height: 200px;
}}
.proj-title {{ font-family: "Bebas Neue","Oswald",Impact,sans-serif; font-size:22px; letter-spacing:.5px; margin:0; color:{SLATE}; }}
.proj-desc {{ color:{SLATE}; opacity:.9; margin: 0 0 6px 0; }}
.proj-metrics {{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:12px; }}
@media (max-width: 900px) {{ .proj-metrics {{ grid-template-columns:1fr; }} }}
.proj-kpi {{ border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:10px 12px;
  background: radial-gradient(120% 100% at 0% 0%, rgba(34,211,238,0.08), rgba(34,211,238,0.02)); }}
.proj-kpi small {{ font-size:11px; color:{MUTE}; }}
.proj-kpi b {{ font-size:20px; color:{SLATE}; }}
.proj-footer {{ display:flex; align-items:center; justify-content:space-between; gap:10px; margin-top:6px; flex-wrap:wrap; }}
.proj-tags {{ color:{MUTE}; font-size:12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.proj-link a {{ color:var(--accent) !important; text-decoration:none; }}
.proj-link a:hover {{ text-decoration:underline; }}

/* Música */
.music-grid{{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:8px; }}
@media (max-width: 900px){{ .music-grid{{ grid-template-columns:1fr; }} }}
.music-card{{ border:1px solid rgba(255,255,255,.10); border-radius:16px;
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
  padding:12px 14px; display:flex; flex-direction:column; gap:10px;
}}
.music-title{{
  min-width:0;
  font-family:"Bebas Neue","Oswald",Impact,sans-serif; font-size:26px;
  letter-spacing:.4px; color:#cbd5e1; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.music-thumb{{ display:block; width:30%; aspect-ratio:16/9;
  border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,.10);
  background-position:center; background-size:cover; background-repeat:no-repeat;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.04);
}}
.music-thumb:hover{{ border-color: rgba(34,211,238,.35); }}

/* Sidebar • Perfil */
.profile-card{{ border:1px solid rgba(255,255,255,.10); border-radius:16px; padding:14px;
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.04); }}
.profile-photo{{ position:relative; border-radius:14px; overflow:hidden; border:1px solid rgba(255,255,255,.12); }}
.profile-photo::after{{ content:""; position:absolute; inset:-1px; border-radius:14px; pointer-events:none;
  box-shadow: 0 0 0 1px rgba(34,211,238,.20), 0 0 22px rgba(34,211,238,.08) inset; }}
.profile-name{{ font-family:"Bebas Neue","Oswald",Impact,sans-serif; font-size:26px; letter-spacing:.6px; margin:6px 0 0 0; color:{SLATE}; }}
.profile-headline{{ color:{SLATE}; opacity:.9; font-size:13px; line-height:1.35; margin-top:2px; }}
.profile-sep{{ height:1px; margin:10px 0; background: linear-gradient(90deg, rgba(255,255,255,0.0), rgba(255,255,255,0.22), rgba(255,255,255,0.0)); border-radius:999px; }}
.profile-section-title{{ display:flex; align-items:center; gap:8px; font-family:"Bebas Neue","Oswald",Impact,sans-serif; font-size:16px; letter-spacing:.5px; color:{SLATE}; margin:2px 0 2px 0; }}
.profile-section-title .emoji{{ width:22px; height:22px; display:inline-grid; place-items:center; border-radius:8px;
  background:rgba(34,211,238,.10); border:1px solid rgba(34,211,238,.25); box-shadow: inset 0 0 18px rgba(34,211,238,.06); }}
.profile-meta{{ display:grid; gap:6px; margin-top:6px; }}
.profile-meta div{{ font-size:13px; color:{SLATE}; opacity:.95; }}
.profile-links{{ display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }}
.profile-links a{{ font-size:12px; padding:6px 10px; border-radius:10px; border:1px solid rgba(255,255,255,.14);
  background: radial-gradient(120% 100% at 0% 0%, rgba(34,211,238,0.08), rgba(34,211,238,0.02)); color:{SLATE}!important; text-decoration:none; }}
.profile-links a:hover{{ border-color: rgba(34,211,238,.35); }}
.profile-bio{{ margin-top:8px; font-size:13px; color:{SLATE}; opacity:.9; }}
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

def timeline_chart(df: pd.DataFrame):
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
    fig.update_xaxes(tickformat="%Y", dtick="M12", title=None, showgrid=True)
    apply_grunge_theme(fig, "Linha do Tempo Profissional")
    fig.update_layout(height=420)
    return fig

def radar_chart(skills: dict, title: str):
    labels = list(skills.keys()) + [list(skills.keys())[0]]
    values = list(skills.values()) + [list(skills.values())[0]]
    fig = go.Figure([go.Scatterpolar(
        r=values, theta=labels, fill="toself", name=title,
        line=dict(color=ACCENT, width=3), marker=dict(size=6),
        fillcolor="rgba(34,211,238,0.18)"
    )])
    fig.update_layout(
        polar=dict(
            bgcolor=GRAPHITE,
            angularaxis=dict(tickfont=dict(size=12, color=SLATE), linecolor="rgba(255,255,255,0.15)", linewidth=1),
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=11, color=SLATE),
                            gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)", linewidth=1),
        ),
        showlegend=False,
    )
    apply_grunge_theme(fig, title)
    fig.update_layout(height=380)
    return fig

def bar_chart(skills: dict, title: str):
    df = pd.DataFrame({"Skill": list(skills.keys()), "Nível": list(skills.values())})
    fig = px.bar(df, x="Nível", y="Skill", orientation="h", title=None)
    fig.update_traces(marker=dict(line=dict(width=0.5, color="rgba(255,255,255,0.18)")),
                      hovertemplate="<b>%{y}</b><br>Nível: %{x}<extra></extra>")
    apply_grunge_theme(fig, title)
    fig.update_layout(height=380)
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
            return u.path.lstrip("/")
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
# SIDEBAR (perfil, sem duplicações)
# -----------------------------
with st.sidebar:
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)

    photo_path = Path(__file__).parent / "assets" / "profile.jpg"
    if photo_path.exists():
        st.image(Image.open(photo_path), use_container_width=True)
    else:
        st.markdown(
            "<div style='height:180px;display:flex;align-items:center;justify-content:center;"
            "border-radius:12px;background:rgba(255,255,255,.05);color:#aaa;font-size:14px;'>"
            "📸 Foto não encontrada</div>",
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
        first_start = ym_to_date(EXPERIENCES[-1]["start"])  # earliest na lista
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
<li><b>Análise de Dados + Marketing + Operações LATAM</b></li>
<li><b>Modelagem preditiva</b>, <b>dashboards executivos</b> e <b>crescimento data-driven</b></li>
<li>Criatividade aplicada em <b>música</b> e <b>conteúdo</b> (YouTube)</li>
</ul>
</div>
""", unsafe_allow_html=True)
    with right:
        st.markdown("### Idiomas")
        lang_df = pd.DataFrame({"Idioma": list(LANGUAGES.keys()), "Nível": list(LANGUAGES.values())})
        fig_lang = px.bar(lang_df, x="Idioma", y="Nível", title=None)
        fig_lang.update_traces(marker_line_width=0.6, marker_line_color="rgba(255,255,255,0.22)")
        apply_grunge_theme(fig_lang, "Proficiência de Idiomas")
        st.plotly_chart(fig_lang, use_container_width=True)

with aba_timeline:
    st.subheader("Experiência Profissional")
    df_exp = build_experience_df(EXPERIENCES)
    df_show = df_exp.copy()
    df_show["Início"] = df_show["Início"].dt.strftime("%Y-%m")
    df_show["Fim"] = df_show["Fim"].dt.strftime("%Y-%m")
    st.dataframe(df_show[["Empresa", "Cargo", "Cidade", "Início", "Fim"]], use_container_width=True, hide_index=True)
    st.plotly_chart(timeline_chart(df_exp), use_container_width=True)

with aba_skills:
    st.subheader("Habilidades Técnicas e de Negócio")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(radar_chart(SKILLS_CORE, "Competências Centrais"), use_container_width=True)
    with c2:
        st.plotly_chart(bar_chart(SKILLS_TOOLS, "Ferramentas & Bibliotecas"), use_container_width=True)

with aba_projects:
    st.subheader("Projetos em Destaque")
    grid_html = "<div class='proj-grid'>" + "".join(project_card_html(p) for p in PROJECTS) + "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

with aba_edu:
    st.subheader("Educação & Certificações")
    edu_df = pd.DataFrame(EDUCATION)
    st.dataframe(edu_df, use_container_width=True, hide_index=True)

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
    apply_grunge_theme(fig_edu_bar, "Formações por Ano")
    fig_edu_bar.update_layout(xaxis_title="Ano", yaxis_title="Quantidade", height=340)
    st.plotly_chart(fig_edu_bar, use_container_width=True)

    fig_edu_tl = px.timeline(df, x_start="start", x_end="end", y="title",
                             color="type", hover_data={"org": True, "year": True, "type": True})
    fig_edu_tl.update_yaxes(autorange="reversed", title=None)
    fig_edu_tl.update_xaxes(tickformat="%Y", title=None, dtick="M12")
    fig_edu_tl.update_traces(marker=dict(line=dict(color="rgba(255,255,255,0.14)", width=1)))
    apply_grunge_theme(fig_edu_tl, "Linha do Tempo – Educação & Certificações")
    fig_edu_tl.update_layout(height=460)
    st.plotly_chart(fig_edu_tl, use_container_width=True)

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
