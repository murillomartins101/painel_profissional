import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- MOBILE DETECTION
def is_mobile():
    """Detecta se o usuário está em dispositivo móvel"""
    try:
        user_agent = st.context.headers.get("User-Agent", "").lower()
        mobile_keywords = ["android", "iphone", "ipad", "mobile"]
        return any(keyword in user_agent for keyword in mobile_keywords)
    except:
        return False

IS_MOBILE = is_mobile()

# --- PAGE CONFIG
st.set_page_config(
    page_title="Murillo Martins | Analista de Dados",
    page_icon="📊",
    layout="centered" if IS_MOBILE else "wide",
    initial_sidebar_state="collapsed" if IS_MOBILE else "expanded",
)

# --- CORES E TEMAS
DARK_BG = "#0f1116"
CARD_BG = "#1e1e1e"
ACCENT_BG = "#262626"
PRIMARY = "#2e86de"
SECONDARY = "#10ac84"
ACCENT = "#ff9f43"
NEUTRAL = "#bdc3c7"
TEXT = "#ecf0f1"
TEXT_LIGHT = "#95a5a6"
BORDER = "#34495e"

# --- CSS CUSTOMIZADO
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

* {{
    font-family: 'Inter', 'Source Sans Pro', system-ui, sans-serif;
}}

[data-testid="stAppViewContainer"] {{
    background: {DARK_BG};
    color: {TEXT};
}}

[data-testid="stSidebar"] {{
    background: {ACCENT_BG};
}}

[data-testid="stSidebar"] > div:first-child {{
    background: {ACCENT_BG};
}}

/* Remove padding padrão do Streamlit no sidebar */
section[data-testid="stSidebar"] > div {{
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}}

.data-card {{
    background: {CARD_BG};
    border-radius: 12px;
    border: 1px solid {BORDER};
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}}

.data-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(0,0,0,0.4);
}}

.story-kpi {{
    background: {CARD_BG};
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid {PRIMARY};
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    margin-bottom: 1rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.story-kpi:hover {{
    transform: translateY(-2px);
}}

.story-kpi b {{
    font-size: 28px;
    color: {TEXT};
    font-weight: 700;
    display: block;
}}

.story-kpi small {{
    font-size: 12px;
    color: {TEXT_LIGHT};
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: block;
    margin-bottom: 0.5rem;
}}

.story-kpi .trend {{
    font-size: 12px;
    margin-top: 0.5rem;
    display: block;
}}

.story-kpi .trend.positive {{
    color: {SECONDARY};
}}

.story-kpi .trend.negative {{
    color: #e74c3c;
}}

.story-kpi.highlight {{
    border-left-color: {SECONDARY};
    background: linear-gradient(135deg, {CARD_BG}, {ACCENT_BG});
}}

.data-badge {{
    display: inline-block;
    padding: 6px 14px;
    background: rgba(46,134,222,0.15);
    color: {PRIMARY};
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px 5px;
    border: 1px solid rgba(46,134,222,0.3);
    backdrop-filter: blur(10px);
}}

.data-badge.secondary {{
    background: rgba(16,172,132,0.15);
    color: {SECONDARY};
    border-color: rgba(16,172,132,0.3);
}}

.data-badge.accent {{
    background: rgba(255,159,67,0.15);
    color: {ACCENT};
    border-color: rgba(255,159,67,0.3);
}}

.story-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}}

.main-header {{
    background: linear-gradient(135deg, {DARK_BG} 0%, {ACCENT_BG} 100%);
    border-bottom: 1px solid {BORDER};
    padding: 3rem 0 2rem 0;
    margin-bottom: 2rem;
    text-align: center;
}}

.stMetric {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}}

.stExpander {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-track {{
    background: {DARK_BG};
}}

::-webkit-scrollbar-thumb {{
    background: {PRIMARY};
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {SECONDARY};
}}

@media (max-width: 1024px) {{
    .story-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media (max-width: 640px) {{
    .story-grid {{
        grid-template-columns: 1fr;
    }}
    
    .data-card, .story-kpi {{
        padding: 1rem;
    }}
    
    .story-kpi b {{
        font-size: 22px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# --- DADOS BASE
PROFILE = {
    "name": "Murillo Martins",
    "headline": "Data Analyst | Data Science | Marketing | Analytics",
    "location": "São Paulo, Brasil",
    "email": "murilomartins09@gmail.com",
    "site": "https://www.murillomartins.com.br",
    "linkedin": "https://www.linkedin.com/in/murillomartins101",
    "github": "https://github.com/murillomartins101",
    "instagram": "https://www.instagram.com/murillomartins101",
    "bio": "Com mais de 15 anos de experiência em marketing, estratégias e desenvolvimento de negócios, atuei em empresas renomadas como Mercedes Benz Bank, Iveco, Case, New Holland e Honda. Essa vivência consolidou minha perspectiva global e expertise em conduzir operações em ambientes multiculturais, sempre buscando resultados estratégicos e sustentáveis."
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
            "Criação e Manutenção de Dashboards executivos em Power BI",
            "Estratégias orientadas a dados para crescimento",
            "Desenvolvimento de materiais e treinamento das áreas de negócio para adoção de cultura data-driven",
            "Automatização de relatórios e processos com Python e SQL",
            "Trabalho com equipes cross-functional para implementação de soluções analíticas"
        ],
        "skills": ["Python", "SQL", "Power BI", "ML"]
    },
    {
        "company": "Honda Brasil",
        "role": "Analista de Operações Internacionais",
        "start": "2023-04",
        "end": "2025-02",
        "city": "São Paulo / LATAM",
        "achievements": [
            "Gestão de distribuidores (Ecuador, Colômbia, Panamá, Suriname, Venezuela)",
            "Planejamento comercial, budget, marketing, vendas e expansão de portfólio",
            "Análise de performance e inteligência de mercado na região LATAM",
            "Coordenação de projetos cross-functional com equipes globais",
            "Liderança de iniciativas de pricing e estratégias de entrada em novos mercados"
        ],
        "skills": ["Comercial", "Planejamento", "Pricing", "LATAM"]
    },
    {
        "company": "Honda Brasil",
        "role": "Consultor Comercial",
        "start": "2019-06",
        "end": "2023-03",
        "city": "São Paulo",
        "achievements": [
            "Gestão de negócios em Concessionárias 4 rodas e 2 rodas (Brasil)",
            "Marketing, Produtos Financeiros, Vendas, Planejamento comercial",
            "Análise de performance e KPIs comerciais",
            "Desenvolvimento de campanhas de marketing e vendas orientadas a dados",
            "Liderança de projetos de melhoria contínua e otimização de processos"
        ],
        "skills": ["Serviços Financeiros", "Marketing", "Comercial", "Planejamento", "Pricing"]
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
            "Estratégias de crescimento e marketing digital",
            "Produção de conteúdo, SEO, Social Media e Paid Media",
            "Consultoria para startups e PMEs em marketing digital e growth",
            "Análise de dados para otimização de campanhas e estratégias"
        ],
        "skills": ["Marketing", "Digital Strategy", "Growth", "SEO", "Branding"]
    },
    {
        "company": "CNH Industrial Capital",
        "role": "Field Representative",
        "start": "2011-09",
        "end": "2015-06",
        "city": "São Paulo",
        "achievements": [
            "Forecast de vendas e inteligência de mercado",
            "Análise de performance e KPIs comerciais",
            "Financiamento de máquinas agrícolas e comerciais - Iveco, Case e New Holland",
            "Desenvolvimento de dashboards e relatórios gerenciais"
            ],
        "skills": ["Serviços Financeiros", "BNDES", "Forecast", "BI"]
    },
    {
        "company": "Banco Mercedes-Benz",
        "role": "Analista de F&I",
        "start": "2010-01",
        "end": "2011-09",
        "city": "São Paulo",
        "achievements": [
            "Forecast de vendas e inteligência de mercado",
            "Análise de performance e KPIs comerciais",
            "Financiamento de ônibus e caminhões - Mercedes-Benz",
            "Análise de empresas para crédito e financiamento"
            ],
        "skills": ["Serviços Financeiros", "BNDES", "Marketing", "Analytics", "CRM"]
    }
]

PROJECTS = [
    { 
    "title": "Análise de Turnover – Case RH (XGBoost com PyCaret)",
    "summary": "Estudo completo de EDA e Machine Learning aplicado à retenção de talentos. O projeto envolveu tratamento de dados, engenharia de variáveis e treinamento com XGBoost via PyCaret para prever risco de desligamento e apoiar decisões estratégicas do RH.",
    "metrics": {"Accuracy": 0.87, "AUC": 0.81, "Recall": 0.86, "Lift@10%": 2.8},
    "tags": ["Python", "PyCaret", "XGBoost", "EDA", "Feature Engineering", "SHAP", "Data Storytelling"],
    "link": "https://github.com/murillomartins101"
    },
    {
        "title": "Churn Prediction – Waze App",
        "summary": "Análise exploratória e pipeline de machine learning usando Random Forest e XGBoost para prever churn de usuários e identificar fatores de retenção no app Waze.",
        "metrics": {
        "Accuracy": 0.81,
        "Precision": 0.44,
        "Recall": 0.18,
        "F1": 0.24
    },
    "tags": ["Python", "Scikit-learn", "XGBoost", "EDA", "Machine Learning", "Classification"],
    "link": "https://github.com/murillomartins101"
    },
    {
        "title": "Murillo Martins – Carreira como Baterista Profissional",
        "summary": "Mais de 20 anos de trajetória como baterista, atuando em bandas de pop rock e metal. Performances no Brasil e exterior, incluindo apresentação no lendário The Cavern Club (Liverpool).",
        "metrics": {
            "Anos_experiência": 20,
            "Shows_realizados": "300+",
            "Países": "10+",
            "Views_Youtube": "125k+",
            "Watch_time": "4.1K+",
            "Projetos_ativos": 3
        },
    "tags": ["Baterista", "Performance", "Analytics", "Produção Artística", "Marketing Digital", "Educador"],
        "link": "https://www.murillomartins.com.br/"
    },
    {
        "title": "Machinage – Conteúdo, Growth & Produção Musical",
        "summary": "Retomada da banda após 8 anos de hiato. Atuação como baterista, produtor artístico e estrategista de marketing digital.",
        "metrics": {"Status": "Em andamento"},
        "tags": ["Baterista", "Estratégia Digital", "Marketing", "Growth", "Analytics", "YouTube"],
        "link": "https://www.instagram.com/machinageband/"
    },
    {
        "title": "RockBuzz – Calculadora de Cachê & Gerador de Contratos",
        "summary": "Sistema que substitui planilhas manuais por uma plataforma automatizada, reduzindo drasticamente o tempo de envio de propostas e aumentando a taxa de fechamento de contratos. Todos os integrantes podem acessar mobile e gerenciar orçamentos, contratos e históricos de forma rápida e eficiente.",
        "metrics": {
        "Taxa de Aceite": "100% (antes 20%)",
        "Tempo Médio de Geração": "03 min (antes ~05 horas)",
    },
    {
        "title": "RockBuzz – Conteúdo, Growth & Performance",
        "summary": "Criação e consolidação da banda como projeto de entretenimento ao vivo.",
        "metrics": {"Views": "250k+", "CTR": "6.5%"},
        "tags": ["Baterista", "Estratégia Digital", "Marketing", "Growth", "Analytics", "YouTube"],
        "link": "https://www.bandarockbuzz.com.br/"
    }
]

EDUCATION = [
    {"title": "Ciência da Computação (em andamento)", "org": "UniAnchieta", "year": "2025"},
    {"title": "Power BI Analyst Certificate", "org": "Microsoft", "year": "2024"},
    {"title": "Google Advanced Data Analytics Certificate", "org": "Google", "year": "2024"},
    {"title": "Google Data Analytics Certificate", "org": "Google", "year": "2023"},
    {"title": "Digital Marketing Specialization", "org": "University of Illinois", "year": "2020"},
    {"title": "MBA em Comércio Exterior", "org": "UniAnchieta", "year": "2012"},
    {"title": "B.Tech em Marketing", "org": "UniAnchieta", "year": "2010"}
]

SKILLS_CORE = {
    "Business Strategy & Growth": 94,
    "Data Storytelling & Comunicação": 92,
    "Python (Pandas, Scikit-learn, Plotly)": 87,
    "Power BI & Data Visualization": 85,
    "Estatística Aplicada": 70,
    "Machine Learning": 75,
    "SQL & Databricks": 70,
    "Project Management (Agile & Cross-functional)": 80,
    "Marketing Analytics": 88
}

SKILLS_TOOLS = {
    "Python": 85,
    "SQL": 75,
    "Power BI": 75,
    "Streamlit": 70,
    "AWS": 70,
    "Databricks": 65
}

LANGUAGES = {
    "Português": 100,
    "Inglês": 95,
    "Espanhol": 70,
    "Alemão": 30
}

# --- FUNÇÕES AUXILIARES
def apply_dark_theme(fig):
    """Aplica tema escuro consistente aos gráficos Plotly"""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family="Inter, sans-serif", size=12, color=TEXT),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor=CARD_BG,
            bordercolor=BORDER,
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        colorway=[PRIMARY, SECONDARY, ACCENT, "#8c564b", "#e377c2", "#7f7f7f"]
    )
    fig.update_xaxes(
        gridcolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(size=10, color=TEXT_LIGHT)
    )
    fig.update_yaxes(
        gridcolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(size=10, color=TEXT_LIGHT)
    )
    return fig

def ym_to_date(ym: str) -> datetime:
    """Converte string YYYY-MM para datetime"""
    return datetime.strptime(f"{ym}-01", "%Y-%m-%d")

def format_duration(rd: relativedelta) -> str:
    """Formata relativedelta em string legível"""
    years, months = rd.years, rd.months
    parts = []
    if years:
        parts.append(f"{years} ano{'s' if years > 1 else ''}")
    if months:
        parts.append(f"{months} mes{'es' if months > 1 else ''}")
    return " e ".join(parts) if parts else "0 meses"

def build_experience_df(experiences):
    """Constrói DataFrame de experiências profissionais"""
    rows = []
    today = datetime.today()
    
    for exp in experiences:
        start = ym_to_date(exp["start"])
        end = ym_to_date(exp["end"]) if exp["end"] else today
        duration = relativedelta(end, start)
        
        rows.append({
            "Empresa": exp["company"],
            "Cargo": exp["role"],
            "Início": start,
            "Fim": end,
            "Cidade": exp.get("city", ""),
            "Duração": duration,
            "Duracao_str": format_duration(duration),
            "Desc": " • ".join(exp.get("achievements", []))
        })
    
    return pd.DataFrame(rows).sort_values("Início", ascending=False)

def create_timeline_chart(df: pd.DataFrame):
    """Cria gráfico de timeline profissional"""
    role_colors = {
        "Cientista/Analista de Dados": PRIMARY,
        "Analista de Operações Internacionais": SECONDARY,
        "Consultor Comercial": ACCENT,
        "Founder | Head of Everything": "#8c564b",
        "Field Representative": "#e377c2",
        "Analista de F&I": TEXT_LIGHT
    }
    
    fig = px.timeline(
        df,
        x_start="Início",
        x_end="Fim",
        y="Empresa",
        color="Cargo",
        color_discrete_map=role_colors,
        custom_data=["Empresa", "Cargo", "Cidade", "Início", "Fim", "Duracao_str", "Desc"]
    )
    
    fig.update_traces(
        marker=dict(line=dict(color=CARD_BG, width=2)),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Cargo: %{customdata[1]}<br>"
            "Local: %{customdata[2]}<br>"
            "Período: %{customdata[3]|%b %Y} – %{customdata[4]|%b %Y}<br>"
            "Duração: %{customdata[5]}<br>"
            "<em>%{customdata[6]}</em><extra></extra>"
        )
    )
    
    fig.update_yaxes(autorange="reversed", title=None, showgrid=False)
    fig.update_xaxes(tickformat="%Y", dtick="M12", title=None)
    
    apply_dark_theme(fig)
    fig.update_layout(
        height=400,
        legend=dict(
            title="Evolução da Carreira",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_skill_radar(skills: dict):
    """Cria gráfico radar de competências"""
    labels = list(skills.keys())
    values = list(skills.values())
    avg_value = sum(values) / len(values)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        fillcolor=f'rgba(46, 134, 222, 0.2)',
        line=dict(color=PRIMARY, width=2),
        name="Competências Atuais"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[avg_value] * len(labels),
        theta=labels,
        line=dict(color=TEXT_LIGHT, width=1, dash='dash'),
        name="Média"
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor=CARD_BG,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=BORDER,
                linecolor=BORDER
            ),
            angularaxis=dict(
                gridcolor=BORDER,
                linecolor=BORDER
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    apply_dark_theme(fig)
    fig.update_layout(height=400)
    
    return fig

def create_progress_bars(skills: dict, title="Progresso"):
    """Cria gráfico de barras horizontais para habilidades"""
    df = pd.DataFrame({
        "Habilidade": list(skills.keys()),
        "Nível": list(skills.values())
    }).sort_values("Nível", ascending=True)
    
    fig = px.bar(
        df,
        x="Nível",
        y="Habilidade",
        orientation='h',
        title=title,
        text="Nível"
    )
    
    fig.update_traces(
        marker_color=PRIMARY,
        texttemplate='%{x}%',
        textposition='outside',
        marker_line_color=PRIMARY,
        marker_line_width=1
    )
    
    fig.update_layout(
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor=BORDER),
        yaxis=dict(showgrid=False),
        showlegend=False
    )
    
    apply_dark_theme(fig)
    
    return fig

def dark_kpi(label: str, value: str, trend=None, highlight=False):
    """Cria KPI card com tema escuro"""
    trend_html = ""
    if trend:
        trend_class = "positive" if trend > 0 else "negative"
        trend_symbol = "↗️" if trend > 0 else "↘️"
        trend_html = f'<span class="trend {trend_class}">{trend_symbol} {abs(trend)}%</span>'
    
    css_class = "story-kpi highlight" if highlight else "story-kpi"
    
    st.markdown(f'''
    <div class="{css_class}">
        <small>{label}</small>
        <b>{value}</b>
        {trend_html}
    </div>
    ''', unsafe_allow_html=True)

# --- SIDEBAR
with st.sidebar:
    # Foto de perfil
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <img src="https://raw.githubusercontent.com/murillomartins101/painel_profissional/main/profile.jpg"
             alt="Foto de Perfil"
             style="
                border-radius: 50%;
                width: 150px;
                height: 150px;
                object-fit: cover;
                border: 4px solid {PRIMARY};
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin: 0 auto;
                display: block;
             ">
    </div>
    """, unsafe_allow_html=True)
    
    # Nome e título
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="
            font-size: 1.5rem;
            font-weight: 700;
            color: {TEXT};
            margin-bottom: 0.5rem;
            line-height: 1.2;
        ">
            {PROFILE['name']}
        </h2>
        <p style="
            font-size: 0.9rem;
            color: {PRIMARY};
            font-weight: 600;
            margin-bottom: 1rem;
            line-height: 1.4;
        ">
            Data Analyst | Data Science<br>
            Marketing | Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informações de contato
    st.markdown(f"""
    <div style="
        background: {CARD_BG};
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid {BORDER};
    ">
        <p style="
            color: {TEXT_LIGHT};
            font-size: 0.85rem;
            margin: 0.5rem 0;
            line-height: 1.6;
        ">
            📍 {PROFILE['location']}
        </p>
        <p style="
            color: {TEXT_LIGHT};
            font-size: 0.85rem;
            margin: 0.5rem 0;
            line-height: 1.6;
        ">
            ✉️ <a href="mailto:{PROFILE['email']}" style="color: {TEXT}; text-decoration: none;">{PROFILE['email']}</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Links de redes sociais
    st.markdown("""
    <style>
    .sidebar-link {
        display: block;
        text-decoration: none;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    .sidebar-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Links individuais para evitar problemas de renderização
    st.markdown(f"""
        <a href="{PROFILE['linkedin']}" target="_blank" class="sidebar-link" style="
            background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
            color: #ffffff;
        ">
            🔗 LinkedIn
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <a href="{PROFILE['github']}" target="_blank" class="sidebar-link" style="
            background: linear-gradient(90deg, #333333, {PRIMARY});
            color: #ffffff;
        ">
            💻 GitHub
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <a href="{PROFILE['site']}" target="_blank" class="sidebar-link" style="
            background: linear-gradient(90deg, {ACCENT}, #e67e22);
            color: #ffffff;
        ">
            📁 Website
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <a href="{PROFILE['instagram']}" target="_blank" class="sidebar-link" style="
            background: linear-gradient(90deg, #c0392b, #8e44ad);
            color: #ffffff;
        ">
            🥁 Instagram
        </a>
    """, unsafe_allow_html=True)
    
    # Espaçamento após os links
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    
    # Footer do sidebar
    st.markdown(f"""
    <div style="
        text-align: center;
        padding-top: 1.5rem;
        border-top: 1px solid {BORDER};
        margin-top: 2rem;
    ">
        <p style="
            color: {TEXT_LIGHT};
            font-size: 0.75rem;
            line-height: 1.4;
        ">
            Desenvolvido por<br>
            <strong style="color: {TEXT};">{PROFILE['name']}</strong><br>
            © 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT

# Header
st.markdown(f"""
<div class="main-header">
    <h1 style="font-size: {'1.8rem' if IS_MOBILE else '2.5rem'}; margin-bottom: 1rem;">Dashboard Profissional</h1>
    <p style="font-size: {'0.9rem' if IS_MOBILE else '1.2rem'}; color: {TEXT_LIGHT}; font-weight: 400;">
        Um portfólio interativo focado em storytelling com dados
    </p>
</div>
""", unsafe_allow_html=True)

# KPIs
st.markdown("<div class='story-grid'>", unsafe_allow_html=True)

if IS_MOBILE:
    col1, col2 = st.columns(2)
    with col1:
        dark_kpi("Experiência", "15+ anos", trend=5, highlight=True)
    with col2:
        dark_kpi("Projetos Data", f"{len(PROJECTS)}+")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dark_kpi("Experiência", "15+ anos", trend=5, highlight=True)
    with col2:
        dark_kpi("Projetos Data", f"{len(PROJECTS)}+")
    with col3:
        dark_kpi("Certificações", "6", trend=25)
    with col4:
        dark_kpi("Idiomas", "4")

st.markdown("</div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Minha História",
    "📈 Trajetória",
    "🛠️ Competências",
    "🚀 Projetos",
    "🎓 Formação"
])

with tab1:
    col1, col2 = st.columns([2, 1] if not IS_MOBILE else [1, 1])
    
    with col1:
        st.markdown("### Da Estratégia à Análise de Dados")
        st.markdown(f"""
        <div class="data-card">
            <p style="font-size: 16px; line-height: 1.7; color: {TEXT};">{PROFILE['bio']}</p>
            <div style="margin-top: 1.5rem; padding: 1.5rem; background: {ACCENT_BG}; border-radius: 8px; border-left: 4px solid {PRIMARY};">
                <h4 style="color: {PRIMARY}; margin-bottom: 1rem;">🎯 Foco Atual</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    <span class="data-badge">Python</span>
                    <span class="data-badge secondary">Power BI</span>
                    <span class="data-badge">SQL</span>
                    <span class="data-badge accent">Machine Learning</span>
                    <span class="data-badge">Data Storytelling</span>
                    <span class="data-badge" style="background: rgba(155, 89, 182, 0.15); color: #9b59b6; border-color: rgba(155, 89, 182, 0.3);">Pensamento Analítico</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Marcos da Carreira")
        milestones = [
            {"ano": "2025-Presente", "evento": "Transição para Análise de Dados", "detalhe": "Honda Brasil - Data Analytics & Data Viz"},
            {"ano": "2023-2024", "evento": "Operações Internacionais", "detalhe": "Honda Brasil - Gestão LATAM"},
            {"ano": "2019-2023", "evento": "Consultor Comercial", "detalhe": "Honda Brasil"},
            {"ano": "2015-2019", "evento": "Fundador & Head of Everything", "detalhe": "Aditivo Media - Marketing Digital"},
            {"ano": "2011-2015", "evento": "Consultor Comercial", "detalhe": "CNH Industrial Capital"},
            {"ano": "2010-2011", "evento": "Analista de F&I", "detalhe": "Banco Mercedes-Benz"}
        ]
        
        for milestone in milestones:
            st.markdown(f"""
            <div class="data-card" style="padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; gap: 1rem;">
                    <div style="flex: 0 0 120px;">
                        <strong style="color: {PRIMARY}; font-size: 0.9rem;">{milestone['ano']}</strong>
                    </div>
                    <div style="flex: 1;">
                        <strong style="font-size: 1rem;">{milestone['evento']}</strong><br>
                        <small style="color: {TEXT_LIGHT}; font-size: 0.85rem;">{milestone['detalhe']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Idiomas")
        lang_data = pd.DataFrame({
            "Idioma": list(LANGUAGES.keys()),
            "Proficiência": list(LANGUAGES.values())
        })
        fig_lang = px.bar(lang_data, x="Proficiência", y="Idioma", orientation='h')
        fig_lang.update_traces(marker_color=PRIMARY, marker_line_color=PRIMARY, marker_line_width=1)
        apply_dark_theme(fig_lang)
        fig_lang.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_lang, use_container_width=True)
        
        st.markdown("### Especializações")
        st.markdown(f"""
        <div class="data-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 1rem;">
                    <span class="data-badge secondary" style="font-size: 14px; padding: 8px 16px;">Data Analytics</span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <span class="data-badge" style="font-size: 14px; padding: 8px 16px;">Business Intelligence</span>
                </div>
                <div>
                    <span class="data-badge accent" style="font-size: 14px; padding: 8px 16px;">Machine Learning</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### Evolução Profissional")
    df_exp = build_experience_df(EXPERIENCES)
    fig_timeline = create_timeline_chart(df_exp)
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {SECONDARY};">📈 Padrão de Crescimento</h4>
            <p style="font-size: 14px; color: {TEXT}; line-height: 1.6;">
                Transição consistente de funções operacionais para estratégicas, 
                com foco crescente em dados e analytics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {ACCENT};">🔄 Versatilidade</h4>
            <p style="font-size: 14px; color: {TEXT}; line-height: 1.6;">
                Experiência diversificada em setores: financeiro, automotivo, 
                marketing digital, tecnologia e music business
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Detalhamento das Experiências")
    
    for exp in EXPERIENCES:
        with st.expander(f"**{exp['company']}** - {exp['role']}", expanded=False):
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.markdown(f"**Período:** {exp['start']} - {exp['end'] if exp['end'] else 'Atual'}")
                st.markdown(f"**Localização:** {exp['city']}")
                st.markdown("**Principais Realizações:**")
                for achievement in exp['achievements']:
                    st.markdown(f"• {achievement}")
            
            with col_b:
                st.markdown("**Habilidades:**")
                for skill in exp['skills']:
                    st.markdown(f'<span class="data-badge" style="display: block; margin: 5px 0;">{skill}</span>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Competências Técnicas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Python", "87%", "+47% desde 2019")
    with col2:
        st.metric("Power BI", "85%", "+65% desde 2022")
    with col3:
        st.metric("Machine Learning", "70%", "Crescimento acelerado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Perfil de Competências")
        st.plotly_chart(create_skill_radar(SKILLS_CORE), use_container_width=True)
    
    with col2:
        st.markdown("#### Ferramentas & Tecnologias")
        st.plotly_chart(create_progress_bars(SKILLS_TOOLS, "Proficiência Técnica"), use_container_width=True)
    
    st.markdown("#### Evolução das Habilidades")
    
    evolution_data = {
        "Habilidade": ["Python", "Power BI", "SQL", "Machine Learning", "Storytelling"],
        "2019": [40, 20, 15, 20, 75],
        "2024": [87, 85, 60, 70, 90]
    }
    df_evo = pd.DataFrame(evolution_data)
    df_melted = df_evo.melt(id_vars=["Habilidade"], var_name="Ano", value_name="Nível")
    
    fig_evo = px.line(
        df_melted,
        x="Ano",
        y="Nível",
        color="Habilidade",
        markers=True,
        title="Crescimento das Principais Habilidades (2019-2024)"
    )
    apply_dark_theme(fig_evo)
    fig_evo.update_layout(height=400)
    st.plotly_chart(fig_evo, use_container_width=True)
    
    st.markdown("### Habilidades Comportamentais")
    
    soft_skills = {
        "Comunicação": 90,
        "Liderança": 80,
        "Trabalho em Equipe": 95,
        "Resolução de Problemas": 90,
        "Adaptabilidade": 92
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        for skill, level in soft_skills.items():
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 14px; color: {TEXT};">{skill}</span>
                    <span style="font-size: 14px; color: {PRIMARY}; font-weight: 600;">{level}%</span>
                </div>
                <div style="width: 100%; background: {BORDER}; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="width: {level}%; background: linear-gradient(90deg, {PRIMARY}, {SECONDARY}); height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {PRIMARY};">💡 Destaques</h4>
            <ul style="line-height: 1.8; color: {TEXT};">
                <li>Forte capacidade de <strong>comunicação técnica</strong> para públicos diversos</li>
                <li>Experiência em <strong>gestão de projetos complexos</strong> e multidisciplinares</li>
                <li>Habilidade comprovada em <strong>storytelling com dados</strong></li>
                <li>Adaptação rápida a novos <strong>desafios e tecnologias</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### Projetos com Impacto")
    
    for i, project in enumerate(PROJECTS):
        with st.expander(f"📊 {project['title']}", expanded=(i == 0)):
            col1, col2 = st.columns([3, 1] if not IS_MOBILE else [1, 1])
            
            with col1:
                st.write(f"**Descrição:** {project['summary']}")
                
                if project.get('metrics'):
                    st.write("**Resultados Mensuráveis:**")
                    metric_cols = st.columns(len(project['metrics']))
                    for idx, (metric, value) in enumerate(project['metrics'].items()):
                        with metric_cols[idx]:
                            st.metric(metric.replace("_", " "), str(value))
            
            with col2:
                st.write("**Tecnologias:**")
                for tag in project['tags']:
                    st.markdown(f'<span class="data-badge" style="display: block; margin: 5px 0;">{tag}</span>', unsafe_allow_html=True)
            
            if project.get('link'):
                st.markdown(f"[🔗 Ver projeto detalhado]({project['link']})")
    
    st.markdown("### Áreas de Atuação")
    
    areas = {
        "Análise de Dados": ["Python", "Databricks", "AWS", "SQL", "Power BI", "Estatística"],
        "Business Intelligence": ["Power BI", "Dashboards", "KPIs"],
        "Marketing Analytics": ["Growth", "SEO", "Paid Media", "CRM"],
        "Música & Performance": ["Baterista Profissional", "Produção Artística", "Estratégia de Marketing"]
    }
    
    cols = st.columns(2)
    
    for idx, (area, skills) in enumerate(areas.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {PRIMARY}; margin-bottom: 1rem;">{area}</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    {''.join([f'<span class="data-badge">{skill}</span>' for skill in skills])}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab5:
    st.markdown("### Formação Contínua")
    
    for edu in EDUCATION:
        year_color = SECONDARY if edu['year'] == '2025' else PRIMARY
        st.markdown(f"""
        <div class="data-card" style="transition: all 0.3s ease;">
            <div style="display: flex; justify-content: space-between; align-items: start; gap: 1rem;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 8px 0; color: {TEXT}; font-size: 1.1rem;">{edu['title']}</h4>
                    <p style="margin: 0; color: {PRIMARY}; font-weight: 600; font-size: 0.95rem;">{edu['org']}</p>
                </div>
                <div style="background: {year_color}; color: white; padding: 8px 16px; border-radius: 12px; font-size: 13px; font-weight: 600;">
                    {edu['year']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Certificações & Especializações")
    
    certifications = [
        {"name": "Power BI Analyst", "org": "Microsoft", "year": 2024, "icon": "📊"},
        {"name": "Google Advanced Data Analytics", "org": "Google", "year": 2024, "icon": "🎓"},
        {"name": "Google Data Analytics", "org": "Google", "year": 2023, "icon": "📈"},
        {"name": "Digital Marketing Specialization", "org": "Univ. Illinois", "year": 2020, "icon": "🎯"}
    ]
    
    cols = st.columns(2)
    
    for idx, cert in enumerate(certifications):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="data-card" style="padding: 1rem; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{cert['icon']}</div>
                <strong style="color: {TEXT}; font-size: 0.95rem;">{cert['name']}</strong><br>
                <small style="color: {TEXT_LIGHT}; font-size: 0.85rem;">{cert['org']} • {cert['year']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### Filosofia de Aprendizado")
    
    st.markdown(f"""
    <div class="data-card">
        <p style="font-size: 16px; line-height: 1.8; color: {TEXT}; text-align: center; font-style: italic;">
            “Vejo o lifelong learning como um modo de viver: 
            aprender continuamente é o que me move e sustenta meu propósito. 
            Busco evoluir como profissional e como pessoa, unindo curiosidade, conhecimento aplicado e impacto real em cada projeto que abraço.”
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {TEXT_LIGHT}; font-size: 14px; padding: 2rem 0;">
    <strong style="color: {TEXT}; font-size: 1.1rem;">{PROFILE['name']}</strong><br>
    <p style="margin: 1rem 0; font-size: 0.95rem;">Data Analyst | Data Science | Marketing | Analytics</p>  
    <p style="margin: 0.5rem 0;">📍 {PROFILE['location']} • ✉️ {PROFILE['email']}</p>
    <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
        <a href="{PROFILE['linkedin']}" style="color: {PRIMARY}; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
            LinkedIn
        </a>
        <a href="{PROFILE['github']}" style="color: {PRIMARY}; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
            GitHub
        </a>
        <a href="{PROFILE['site']}" style="color: {PRIMARY}; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
            Website
        </a>
        <a href="{PROFILE['instagram']}" style="color: {ACCENT}; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
            Instagram
        </a>
    </div>
    <p style="margin-top: 2rem; font-size: 0.85rem; color: {TEXT_LIGHT};">
        © 2025 {PROFILE['name']} • Desenvolvido com Streamlit & Python
    </p>
</div>
""", unsafe_allow_html=True)



