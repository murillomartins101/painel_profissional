# CV Dashboard – Streamlit (Responsivo + Auto-Compact + Dados Dinâmicos)
# Author: Murillo Martins
# -------------------------------------------------
# Como usar:
# 1) Salve como app.py
# 2) Rode: streamlit run app.py
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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
import io
import streamlit.components.v1 as components
import requests
import time
from typing import Dict, List, Optional

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
# DADOS BASE (fallback)
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

# Habilidades atualizadas com base na trajetória real
SKILLS_CORE = {
    # Estratégia e Comunicação (base forte desde início)
    "Comunicação": 92,
    "Storytelling": 90, 
    "Marketing & Growth": 88,
    "Gestão de Projetos": 80,

    # Dados e Análise (evolução real 2019-2024)
    "Análise de Dados": 88,
    "Power BI": 85,
    "Python": 87,
    "SQL": 60,
    "R": 45,  # Uso até 2023, depois descontinuado

    # Estatística e Modelagem (base sólida + crescimento)
    "Estatística": 82,
    "Machine Learning": 70,
}

SKILLS_TOOLS = {
    # Bibliotecas Python (crescimento com Python)
    "Pandas": 85,
    "Scikit-learn": 75,
    "Plotly": 82,
    "Matplotlib": 80,
    "Streamlit": 75,

    # Ferramentas de Análise
    "Excel": 95,
    "DAX": 80,
    "M (Power Query)": 78,
    "PowerPoint": 88,
}

LANGUAGES = {"Português": 100, "Inglês": 85, "Espanhol": 70, "Alemão": 30}

MUSIC = [
    {"title": "Rolling Stones – Jumpin' Jack Flash | Performance by Murillo Martins at The Cavern Club, Liverpool", "url": "https://www.youtube.com/watch?v=v8o4fG5cF0Y"},
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
        legend_cfg.update(dict(orientation="h", x=0, y=-0.2, yanchor="top"))
        top_margin = 8
        bottom_margin = 40
    else:
        legend_cfg.update(dict(orientation="h", x=0, y=1.02, yanchor="bottom"))
        top_margin = 12
        bottom_margin = 12

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=GRAPHITE, 
        plot_bgcolor=GRAPHITE,
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
        gridcolor="rgba(255,255,255,0.06)", 
        linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", 
        tickfont=dict(color=SLATE, size=tick_size),
        title=dict(font=dict(color=MUTE, size=tick_size)),
    )
    
    fig.update_yaxes(
        automargin=True,
        gridcolor="rgba(255,255,255,0.06)", 
        linecolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.10)", 
        tickfont=dict(color=SLATE, size=tick_size),
        title=dict(font=dict(color=MUTE, size=tick_size)),
    )
    
    return fig

# -----------------------------
# CSS GLOBAL MODERNO
# -----------------------------
st.markdown(f"""
<style>
:root {{
  --ink: {INK}; --graphite: {GRAPHITE}; --slate: {SLATE}; --mute: {MUTE}; --accent: {ACCENT};
  --radius: 16px;
  --card-bg: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  --shadow: 0 8px 32px rgba(0,0,0,0.3);
  --glow: 0 0 20px rgba(34, 211, 238, 0.15);
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: linear-gradient(135deg, #0b0d11 0%, #0a0c10 50%, #090b0f 100%);
  overflow-x: hidden;
}}

/* Header moderno */
.main-header {{
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(8, 12, 23, 0.9));
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding: 2rem 0;
  margin-bottom: 2rem;
  position: relative;
}}
.main-header::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}}

/* Tabs modernas */
div[role="tablist"] {{
  position: sticky; 
  top: 0px; 
  z-index: 100; 
  padding: 1rem 0 0 0;
  background: linear-gradient(135deg, rgba(11,13,17,0.98), rgba(11,13,17,0.95));
  backdrop-filter: blur(15px);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 2rem;
}}

div[role="tab"] {{
  font-size: 15px !important; 
  font-weight: 700;
  color: #94a3b8 !important; 
  padding: 12px 24px; 
  position: relative;
  text-transform: uppercase; 
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  border-radius: var(--radius) var(--radius) 0 0;
  margin: 0 4px;
}}
div[role="tab"]:hover {{
  color: var(--accent) !important;
  background: rgba(34, 211, 238, 0.05);
}}
div[role="tab"][aria-selected="true"] {{
  color: var(--accent) !important; 
  background: rgba(34, 211, 238, 0.1);
  box-shadow: var(--glow);
}}
div[role="tab"][aria-selected="true"]::after {{
  content: ""; 
  position: absolute; 
  left: 0;
  right: 0;
  bottom: -1px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), #60a5fa);
  border-radius: 2px;
}}

@media (max-width: 768px) {{
  div[role="tablist"] {{ 
    position: static; 
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 1rem;
  }}
  div[role="tab"] {{
    display: inline-block;
    font-size: 14px !important;
    padding: 10px 20px !important;
  }}
}}

/* Tipografia moderna */
h1, h2, h3 {{
  font-family: "Bebas Neue", "Oswald", Impact, system-ui, sans-serif !important;
  font-weight: 900 !important; 
  letter-spacing: 0.5px; 
  text-transform: uppercase;
  color: {SLATE}; 
  text-shadow: 0 0 10px rgba(34,211,238,.2);
  line-height: 1.1;
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
h1 {{ 
  font-size: clamp(28px, 7vw, 48px); 
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(34,211,238,.3);
}}
h2 {{ 
  font-size: clamp(22px, 5.5vw, 38px); 
  margin-bottom: 0.75rem;
}}
h3 {{ 
  font-size: clamp(20px, 5vw, 32px); 
  margin-bottom: 0.5rem;
}}

/* KPIs modernos */
.kpi-grid {{ 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); 
  gap: 1.5rem; 
  margin: 2rem 0;
}}
@media (max-width: 1024px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 640px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}
.kpi {{
  padding: 1.5rem; 
  border-radius: var(--radius);
  border: 1px solid rgba(255,255,255,.15);
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}}
.kpi::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}}
.kpi:hover {{
  transform: translateY(-5px);
  box-shadow: var(--shadow), var(--glow);
  border-color: rgba(34, 211, 238, 0.3);
}}
.kpi small {{ 
  font-size: 13px; 
  color: {MUTE}; 
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}}
.kpi b {{ 
  font-size: 28px; 
  color: {SLATE};
  display: block;
  font-weight: 800;
}}

/* Cards modernos */
.card {{
  border-radius: var(--radius); 
  border: 1px solid rgba(255,255,255,0.12);
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  padding: 2rem; 
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}}
.card::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}}
.card:hover {{
  box-shadow: var(--shadow), var(--glow);
  border-color: rgba(34, 211, 238, 0.2);
}}

/* Sidebar moderna */
.profile-card {{
  text-align: center;
  padding: 2rem 0;
}}
.profile-name {{
  font-family: "Bebas Neue", "Oswald", Impact, sans-serif;
  font-size: clamp(26px, 5vw, 36px);
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 1rem 0 0.5rem 0;
  letter-spacing: 0.5px;
}}
.profile-headline {{
  color: {MUTE};
  font-size: 15px;
  margin-bottom: 1rem;
  font-weight: 500;
}}
.profile-sep {{
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  margin: 1.5rem 0;
}}
.profile-meta div {{
  margin: 0.75rem 0;
  color: {SLATE};
  font-size: 14px;
  font-weight: 500;
}}
.profile-links {{
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin: 1.5rem 0;
}}
.profile-links a {{
  color: var(--accent) !important;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(34, 211, 238, 0.1);
  border: 1px solid rgba(34, 211, 238, 0.2);
}}
.profile-links a:hover {{
  background: rgba(34, 211, 238, 0.2);
  box-shadow: var(--glow);
}}
.profile-bio {{
  color: {SLATE};
  font-size: 14px;
  line-height: 1.6;
  margin-top: 1.5rem;
}}

/* Badges modernas */
.skill-badge {{
  display: inline-block;
  padding: 6px 12px;
  background: rgba(34, 211, 238, 0.1);
  border: 1px solid rgba(34, 211, 238, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  margin: 2px 4px;
  transition: all 0.3s ease;
}}
.skill-badge:hover {{
  background: rgba(34, 211, 238, 0.2);
  box-shadow: var(--glow);
}}

/* Animações suaves */
.fade-in {{
  animation: fadeIn 0.8s ease-in;
}}
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* Scrollbar personalizada */
::-webkit-scrollbar {{
  width: 8px;
}}
::-webkit-scrollbar-track {{
  background: rgba(255,255,255,0.05);
}}
::-webkit-scrollbar-thumb {{
  background: var(--accent);
  border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
  background: #06b6d4;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS EXISTENTES (mantidos)
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

def kpi_badge(label: str, value: str, tooltip: str = ""):
    tooltip_attr = f'title="{tooltip}"' if tooltip else ""
    st.markdown(f'<div class="kpi fade-in" {tooltip_attr}><small>{label}</small><b>{value}</b></div>', unsafe_allow_html=True)

def chart_heading(text: str):
    st.markdown(f"""
    <div style="
      font-family:'Bebas Neue','Oswald',Impact,system-ui,sans-serif;
      font-weight:900; letter-spacing:0.5px; text-transform:uppercase;
      color:#cbd5e1; text-shadow:0 0 10px rgba(34,211,238,.2);
      margin: 2rem 0 1rem 0;
      font-size: clamp(22px, 5.5vw, 36px);
      background: linear-gradient(135deg, #cbd5e1, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    ">{text}</div>
    """, unsafe_allow_html=True)

# -----------------------------
# NOVAS VISUALIZAÇÕES MODERNAS
# -----------------------------
def create_skills_evolution_heatmap():
    """
    Mapa de calor moderno mostrando evolução temporal REAL das habilidades
    """
    skills_evolution = {
        "Python": {"2019": 40, "2020": 55, "2021": 65, "2022": 75, "2023": 82, "2024": 87},
        "R": {"2019": 50, "2020": 60, "2021": 65, "2022": 68, "2023": 70, "2024": 45},
        "Power BI": {"2019": 20, "2020": 25, "2021": 30, "2022": 50, "2023": 70, "2024": 85},
        "SQL": {"2019": 15, "2020": 20, "2021": 25, "2022": 30, "2023": 45, "2024": 60},
        "Machine Learning": {"2019": 20, "2020": 25, "2021": 30, "2022": 35, "2023": 50, "2024": 70},
        "Estatística": {"2019": 60, "2020": 65, "2021": 70, "2022": 75, "2023": 78, "2024": 82},
        "Storytelling": {"2019": 75, "2020": 78, "2021": 82, "2022": 85, "2023": 87, "2024": 90},
        "Análise de Dados": {"2019": 65, "2020": 70, "2021": 75, "2022": 80, "2023": 85, "2024": 88}
    }
    
    df = pd.DataFrame(skills_evolution).T
    
    fig = px.imshow(
        df,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="",
        labels=dict(x="Ano", y="Habilidade", color="Nível")
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Ano",
        yaxis_title="Habilidade",
        coloraxis_colorbar=dict(title="Nível"),
        font=dict(family="Inter, sans-serif")
    )
    
    return fig

def create_project_showcase():
    """
    Showcase moderno de projetos
    """
    projects_data = []
    for project in PROJECTS:
        projects_data.append({
            "Projeto": project["title"],
            "Descrição": project["summary"],
            "Tecnologias": ", ".join(project["tags"]),
            "Dificuldade": 7 if "ML" in project["tags"] else 5,
            "Impacto": 9 if "Dashboard" in project["title"] else 7,
            "Duração": 4
        })
    
    df = pd.DataFrame(projects_data)
    fig = px.scatter(df, x="Dificuldade", y="Impacto", size="Duração",
                    hover_name="Projeto", hover_data=["Descrição", "Tecnologias"],
                    size_max=20, color="Impacto",
                    color_continuous_scale="Viridis")
    
    fig.update_layout(
        height=400,
        title="",
        xaxis_title="Complexidade Técnica",
        yaxis_title="Impacto no Negócio"
    )
    
    return fig

# -----------------------------
# AUTO-DETECÇÃO DO MODO COMPACTO
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
# MODO COMPACTO
# -----------------------------
try:
    compact_qs = st.query_params.get("compact", None)
    IS_COMPACT = str(compact_qs).lower() in ("1", "true", "yes")
except Exception:
    IS_COMPACT = "compact" in st.experimental_get_query_params()

# -----------------------------
# SIDEBAR MODERNA
# -----------------------------
with st.sidebar:
    st.markdown("<div class='profile-card'>", unsafe_allow_html=True)

    # Foto de perfil
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/murillomartins101/painel_profissional/main/painel_profissional/profile.jpg"
    PHOTO_CANDIDATES = [
        Path(__file__).parent / "assets" / "profile.jpg",
        Path(__file__).parent / "painel_profissional" / "profile.jpg",
        Path(__file__).parent / "profile.jpg",
    ]

    @st.cache_data(show_spinner=False)
    def resolve_profile_photo() -> str:
        for p in PHOTO_CANDIDATES:
            if p.exists():
                return str(p)
        return GITHUB_RAW_URL

    photo_src = resolve_profile_photo()

    try:
        if photo_src.startswith("http"):
            st.image(photo_src, use_container_width=True)
        else:
            st.image(Image.open(photo_src), use_container_width=True)
    except Exception as e:
        st.markdown(
            "<div style='height:200px;display:flex;align-items:center;justify-content:center;"
            "border-radius:16px;background:rgba(255,255,255,.05);color:#aaa;font-size:14px;'>"
            f"📸 Imagem do perfil</div>",
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
    
    st.markdown("---")
    IS_COMPACT = st.toggle("📱 Modo compacto", value=IS_COMPACT,
                           help="Otimizar para dispositivos móveis")

# -----------------------------
# HEADER MODERNO
# -----------------------------
st.markdown("""
<div class="main-header">
    <div style="text-align: center;">
        <h1>Murillo Martins</h1>
        <div style="font-size: 1.2rem; color: #94a3b8; margin-top: 0.5rem;">
            Data Analyst | Data Science | Marketing | Analytics
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KPIs modernos
st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if EXPERIENCES:
        first_start = datetime.strptime(EXPERIENCES[-1]["start"] + "-01", "%Y-%m-%d")
        total_years = relativedelta(datetime.today(), first_start)
        kpi_badge("Experiência Profissional", f"{total_years.years} anos", "Trajetória consolidada no mercado")
with c2:
    kpi_badge("Projetos em Destaque", str(len(PROJECTS)), "Portfólio diversificado")
with c3:
    kpi_badge("Certificações", "4", "Google, Microsoft e especializações")
with c4:
    kpi_badge("Idiomas", "4", "Português, Inglês, Espanhol, Alemão")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# ABAS MODERNAS
# -----------------------------
aba_overview, aba_timeline, aba_skills, aba_projects, aba_edu, aba_music = st.tabs(
    ["🎯 Visão Geral", "📈 Linha do Tempo", "🚀 Habilidades", "💼 Projetos", "🎓 Educação", "🎵 Música"]
)

with aba_overview:
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### Sobre Mim")
        st.markdown(f"""
        <div class="card">
            <p style="font-size: 16px; line-height: 1.6; color: #cbd5e1;">{PROFILE['bio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Destaques")
        st.markdown("""
        <div class="card">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="text-align: center; padding: 1rem; background: rgba(34, 211, 238, 0.05); border-radius: 12px;">
                    <div style="font-size: 14px; color: #94a3b8;">💼 Carreira</div>
                    <div style="font-size: 18px; font-weight: bold; color: #22d3ee;">15+ anos</div>
                    <div style="font-size: 12px; color: #cbd5e1;">Experiência</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: rgba(34, 211, 238, 0.05); border-radius: 12px;">
                    <div style="font-size: 14px; color: #94a3b8;">🎯 Especialização</div>
                    <div style="font-size: 18px; font-weight: bold; color: #22d3ee;">Data</div>
                    <div style="font-size: 12px; color: #cbd5e1;">Analytics & Science</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: rgba(34, 211, 238, 0.05); border-radius: 12px;">
                    <div style="font-size: 14px; color: #94a3b8;">🚀 Metodologia</div>
                    <div style="font-size: 18px; font-weight: bold; color: #22d3ee;">Data-Driven</div>
                    <div style="font-size: 12px; color: #cbd5e1;">Decision Making</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: rgba(34, 211, 238, 0.05); border-radius: 12px;">
                    <div style="font-size: 14px; color: #94a3b8;">🎨 Criatividade</div>
                    <div style="font-size: 18px; font-weight: bold; color: #22d3ee;">Storytelling</div>
                    <div style="font-size: 12px; color: #cbd5e1;">& Visualização</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        chart_heading("Idiomas")
        lang_df = pd.DataFrame({"Idioma": list(LANGUAGES.keys()), "Nível": list(LANGUAGES.values())})
        fig_lang = px.bar(lang_df, x="Idioma", y="Nível", title=None)
        fig_lang.update_traces(marker_line_width=0.6, marker_line_color="rgba(255,255,255,0.22)",
                              marker_color=PRIMARY)
        apply_grunge_theme(fig_lang, compact=IS_COMPACT)
        st.plotly_chart(fig_lang, use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})
        
        st.markdown("""
        <div class="card">
            <h4>🎯 Foco Atual</h4>
            <div style="margin-top: 1rem;">
                <span class="skill-badge">Python Avançado</span>
                <span class="skill-badge">Power BI Expert</span>
                <span class="skill-badge">SQL</span>
                <span class="skill-badge">Machine Learning</span>
                <span class="skill-badge">Data Storytelling</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with aba_timeline:
    st.markdown("### Experiência Profissional")
    df_exp = build_experience_df(EXPERIENCES)
    df_show = df_exp.copy()
    df_show["Início"] = df_show["Início"].dt.strftime("%Y-%m")
    df_show["Fim"] = df_show["Fim"].dt.strftime("%Y-%m")
    
    # Dataframe estilizado
    st.dataframe(df_show[["Empresa", "Cargo", "Cidade", "Início", "Fim"]],
                 use_container_width=True, hide_index=True, height=(280 if IS_COMPACT else 380))
    
    chart_heading("Linha do Tempo Profissional")
    st.plotly_chart(timeline_chart(df_exp, compact=IS_COMPACT), use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_skills:
    st.markdown("### Habilidades Técnicas")
    
    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Python", "87%", "↗️ +47% desde 2019")
    with col2:
        st.metric("Power BI", "85%", "🚀 +65% desde 2022")
    with col3:
        st.metric("SQL", "60%", "📈 +45% desde 2023")
    
    col1, col2 = st.columns(2)
    with col1:
        chart_heading("Competências Principais")
        st.plotly_chart(radar_chart(SKILLS_CORE, compact=IS_COMPACT),
                        use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})
    with col2:
        chart_heading("Ferramentas & Tecnologias")
        st.plotly_chart(bar_chart(SKILLS_TOOLS, compact=IS_COMPACT),
                        use_container_width=True,
                        config={"displayModeBar": False, "displaylogo": False, "responsive": True})
    
    # Evolução temporal
    chart_heading("Evolução das Habilidades")
    st.plotly_chart(create_skills_evolution_heatmap(), use_container_width=True)

with aba_projects:
    st.markdown("### Portfólio de Projetos")
    
    # Métricas dos projetos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projetos Concluídos", len(PROJECTS))
    with col2:
        st.metric("Tecnologias Utilizadas", "8+")
    with col3:
        st.metric("Áreas de Atuação", "4")
    
    # Showcase visual
    chart_heading("Análise de Projetos")
    st.plotly_chart(create_project_showcase(), use_container_width=True)
    
    # Detalhes dos projetos
    for i, project in enumerate(PROJECTS):
        with st.expander(f"🚀 {project['title']}", expanded=i == 0):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Descrição:** {project['summary']}")
                if project.get('metrics'):
                    st.write("**Resultados:**")
                    for metric, value in project['metrics'].items():
                        st.write(f"- {metric}: `{value}`")
            with col2:
                st.write("**Tecnologias:**")
                for tag in project['tags']:
                    st.markdown(f'<span class="skill-badge">{tag}</span>', unsafe_allow_html=True)
            
            if project.get('link'):
                st.markdown(f"[🔗 Acessar Projeto]({project['link']})")

with aba_edu:
    st.markdown("### Formação Acadêmica & Certificações")
    edu_df = pd.DataFrame(EDUCATION)
    
    # Dataframe estilizado
    st.dataframe(edu_df, use_container_width=True, hide_index=True, height=(260 if IS_COMPACT else 360))
    
    # Análise temporal
    df = edu_df.copy()
    def infer_type(title, org):
        t = (title or "").lower()
        if "cert" in t or "certificate" in t or org in ("Google", "Microsoft"):
            return "Certificação"
        return "Graduação/Pós"

    df["type"] = df.apply(lambda r: infer_type(r.get("title",""), r.get("org","")), axis=1)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"]).sort_values("year")
    
    counts = df.groupby(["year", "type"]).size().reset_index(name="qtde")
    fig_edu_bar = px.bar(counts, x="year", y="qtde", color="type",
                         barmode="stack", category_orders={"type": ["Graduação/Pós", "Certificação"]})
    fig_edu_bar.update_traces(marker_line_width=0.6, marker_line_color="rgba(255,255,255,0.18)")
    chart_heading("Evolução da Formação")
    apply_grunge_theme(fig_edu_bar, compact=IS_COMPACT)
    fig_edu_bar.update_layout(xaxis_title="Ano", yaxis_title="Quantidade", height=(320 if IS_COMPACT else 400))
    fig_edu_bar.update_xaxes(tickangle=0)
    st.plotly_chart(fig_edu_bar, use_container_width=True,
                    config={"displayModeBar": False, "displaylogo": False, "responsive": True})

with aba_music:
    st.markdown("### Expressão Musical")
    st.write("Integração entre análise de dados e criatividade musical.")
    
    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Performances", "2", "Liverpool & Covers")
    with col2:
        st.metric("Plataforma", "YouTube", "Conteúdo musical")
    
    for i, m in enumerate(MUSIC):
        with st.expander(f"🎵 {m['title']}", expanded=i == 0):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.video(m['url'])
            with col2:
                st.markdown(f"""
                <div class="card">
                    <h4>Detalhes</h4>
                    <p style="font-size: 14px; color: #cbd5e1;">
                    {'Performance ao vivo no palco histórico' if 'Cavern Club' in m['title'] else 'Cover instrumental gravado em estúdio'}
                    </p>
                    <a href="{m['url']}" target="_blank" style="display: inline-block; margin-top: 1rem; padding: 8px 16px; background: rgba(239, 68, 68, 0.2); color: #ef4444; text-decoration: none; border-radius: 20px; font-weight: 600; border: 1px solid rgba(239, 68, 68, 0.3);">
                        ▶️ Assistir no YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)