import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
import os

# Set Page Config
st.set_page_config(
    page_title="GLP-1 WeightLoss Pulse",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Lottie Animation Loader
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_pulse = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6cuL6.json") # Medical pulse

# Data Loading with Caching
@st.cache_data
def load_data():
    dataset_dir = 'Dataset'
    data = {
        'adverse': pd.read_csv(os.path.join(dataset_dir, 'adverse_events.csv')),
        'summary': pd.read_csv(os.path.join(dataset_dir, 'adverse_events_summary.csv')),
        'trials': pd.read_csv(os.path.join(dataset_dir, 'clinical_trials.csv')),
        'overview': pd.read_csv(os.path.join(dataset_dir, 'drugs_overview.csv')),
        'trends': pd.read_csv(os.path.join(dataset_dir, 'search_trends.csv')),
        'stocks': pd.read_csv(os.path.join(dataset_dir, 'stock_prices.csv')),
        'wiki': pd.read_csv(os.path.join(dataset_dir, 'wikipedia_summaries.csv')),
        'dictionary': pd.read_csv(os.path.join(dataset_dir, 'data_dictionary.csv'))
    }
    
    # Basic cleaning
    data['adverse']['receive_date'] = pd.to_datetime(data['adverse']['receive_date'])
    data['trends']['date'] = pd.to_datetime(data['trends']['date'])
    data['stocks']['date'] = pd.to_datetime(data['stocks']['date'])
    data['trials']['start_date'] = pd.to_datetime(data['trials']['start_date'])
    
    return data

# Load Data
with st.spinner("Initializing Dashboard..."):
    data = load_data()

# Sidebar Navigation
with st.sidebar:
    if lottie_pulse:
        st_lottie(lottie_pulse, height=100, key="pulse")
    else:
        st.image("https://www.svgrepo.com/show/475470/pulse.svg", width=80)
        
    st.markdown("<h2 style='text-align: center;'>GLP-1 Pulse</h2>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Executive Summary", "Clinical Safety", "Market Pulse", "Research Pipeline"],
        icons=["house", "activity", "graph-up", "flask"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00D2D3", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(108, 92, 231, 0.2)"},
            "nav-link-selected": {"background-color": "#6C5CE7"},
        }
    )
    
    st.markdown("---")
    st.markdown("#### 🛠️ Controls")
    all_drugs = sorted(data['overview']['generic_name'].unique().tolist())
    selected_drug = st.selectbox("Global Drug Filter", ["All Drugs"] + all_drugs, 
                               help="Filter clinical and research data across the entire dashboard.")
    
    with st.expander("📖 Data Dictionary"):
        st.dataframe(data['dictionary'], hide_index=True)

# --- PAGES ---

if selected == "Executive Summary":
    st.markdown("<h1 style='margin-bottom: 0;'>🚀 GLP-1 Weight Loss Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem; opacity: 0.8;'>A comprehensive analysis of clinical safety, market trends, and research pipelines.</p>", unsafe_allow_html=True)
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Adverse Reports", f"{len(data['adverse']):,}", help="Total number of reports logged in the FDA FAERS database for these drugs.")
    with col2:
        recruiting = len(data['trials'][data['trials']['overall_status'] == 'RECRUITING'])
        st.metric("Active Trials", recruiting, help="Number of clinical trials currently in the 'Recruiting' phase.")
    with col3:
        latest_lly = data['stocks'][data['stocks']['ticker'] == 'LLY']['close'].iloc[-1]
        prev_lly = data['stocks'][data['stocks']['ticker'] == 'LLY']['close'].iloc[-2]
        delta_lly = ((latest_lly - prev_lly) / prev_lly) * 100
        st.metric("Eli Lilly (LLY)", f"${latest_lly:.2f}", f"{delta_lly:.2f}%")
    with col4:
        latest_nvo = data['stocks'][data['stocks']['ticker'] == 'NVO']['close'].iloc[-1]
        prev_nvo = data['stocks'][data['stocks']['ticker'] == 'NVO']['close'].iloc[-2]
        delta_nvo = ((latest_nvo - prev_nvo) / prev_nvo) * 100
        st.metric("Novo Nordisk (NVO)", f"${latest_nvo:.2f}", f"{delta_nvo:.2f}%")

    st.markdown("---")
    
    # Drug Overview Cards
    st.header("💊 Spotlight on GLP-1 Medications")
    cols = st.columns(3)
    display_drugs = all_drugs if selected_drug == "All Drugs" else [selected_drug]
    
    for i, drug in enumerate(display_drugs[:6]): # Limit to top 6 for layout
        with cols[i % 3]:
            wiki_info = data['wiki'][data['wiki']['generic_name'] == drug]
            drug_meta = data['overview'][data['overview']['generic_name'] == drug]
            
            summary = wiki_info['summary'].values[0] if not wiki_info.empty else "No summary available."
            img_url = wiki_info['image_url'].values[0] if not wiki_info.empty and pd.notna(wiki_info['image_url'].values[0]) else "https://via.placeholder.com/150"
            brand = drug_meta['brand_names'].values[0] if not drug_meta.empty else "N/A"
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; height: 100%;">
                <img src="{img_url}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 15px; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #A29BFE;">{drug.capitalize()}</h3>
                <p style="color: #00D2D3; font-weight: bold; margin-bottom: 10px;">Brand: {brand}</p>
                <p style="font-size: 14px; line-height: 1.6; opacity: 0.9;">{summary[:250]}...</p>
            </div>
            """, unsafe_allow_html=True)

elif selected == "Clinical Safety":
    st.title("🏥 Clinical Safety Profile")
    st.info("Interactive visualization of FDA adverse event reports. Use the sidebar to filter by drug.")
    
    # Filter data
    df_safety = data['adverse'] if selected_drug == "All Drugs" else data['adverse'][data['adverse']['generic_name'] == selected_drug]
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Top 10 Reactions
        top_reactions = df_safety['reaction'].value_counts().head(10).reset_index()
        top_reactions.columns = ['Reaction', 'Count']
        fig_reactions = px.bar(top_reactions, x='Count', y='Reaction', orientation='h', 
                             title="Most Frequent Adverse Reactions",
                             color='Count', color_continuous_scale='Purples')
        fig_reactions.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_reactions, use_container_width=True)
        
    with col_b:
        # Seriousness Donut
        seriousness = df_safety['serious'].value_counts().reset_index()
        seriousness.columns = ['Status', 'Count']
        seriousness['Status'] = seriousness['Status'].map({1: 'Serious', 2: 'Non-Serious'})
        fig_serious = px.pie(seriousness, values='Count', names='Status', hole=0.6,
                            title="Report Severity Distribution",
                            color_discrete_sequence=['#6C5CE7', '#00D2D3'])
        fig_serious.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_serious, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        # Age Distribution
        fig_age = px.histogram(df_safety, x='patient_age', nbins=30, 
                              title="Patient Age Distribution",
                              color_discrete_sequence=['#A29BFE'],
                              labels={'patient_age': 'Age (Years)'})
        fig_age.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col_d:
        # Sex Distribution
        sex_dist = df_safety['patient_sex'].value_counts().reset_index()
        sex_dist.columns = ['Sex', 'Count']
        sex_dist['Sex'] = sex_dist['Sex'].map({1: 'Male', 2: 'Female', 0: 'Unknown'})
        fig_sex = px.bar(sex_dist, x='Sex', y='Count', title="Patient Sex Distribution",
                        color='Sex', color_discrete_map={'Male': '#6C5CE7', 'Female': '#00D2D3', 'Unknown': '#A29BFE'})
        fig_sex.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sex, use_container_width=True)

elif selected == "Market Pulse":
    st.title("📈 Market & Interest Dynamics")
    
    # Stock Ticker Selection
    ticker = st.radio("Select Company to View", ["Eli Lilly (LLY)", "Novo Nordisk (NVO)"], horizontal=True)
    target_ticker = "LLY" if "Lilly" in ticker else "NVO"
    
    # Combined Chart
    fig = go.Figure()
    
    stock_df = data['stocks'][data['stocks']['ticker'] == target_ticker]
    
    # Primary Y-Axis: Stock Price
    fig.add_trace(go.Scatter(x=stock_df['date'], y=stock_df['close'], name=f"{target_ticker} Price", 
                            line=dict(color='#6C5CE7', width=3),
                            fill='tozeroy', fillcolor='rgba(108, 92, 231, 0.1)'))
    
    # Secondary Y-Axis: Search Interest
    # We use 'Ozempic' for NVO and 'Mounjaro' for LLY as representative terms
    term = "Ozempic" if target_ticker == "NVO" else "Mounjaro"
    trend_df = data['trends'][data['trends']['term'] == term]
    
    fig.add_trace(go.Scatter(x=trend_df['date'], y=trend_df['search_interest'], name=f"{term} Interest", 
                            line=dict(color='#00D2D3', width=2, dash='dot'), yaxis="y2"))
    
    fig.update_layout(
        title=f"{target_ticker} Stock Performance vs {term} Search Trends",
        xaxis=dict(title="Timeline"),
        yaxis=dict(title="Stock Price (USD)", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Google Search Interest (0-100)", overlaying="y", side="right", showgrid=False),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Market Sentiment Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    avg_vol = stock_df['volume'].mean()
    m_col1.metric("Avg Daily Volume", f"{avg_vol/1e6:.1f}M")
    
    peak_interest = trend_df['search_interest'].max()
    m_col2.metric(f"Peak {term} Interest", peak_interest)
    
    yearly_return = ((stock_df['close'].iloc[-1] - stock_df['close'].iloc[0]) / stock_df['close'].iloc[0]) * 100
    m_col3.metric("Stock Return (Period)", f"{yearly_return:.1f}%")

elif selected == "Research Pipeline":
    st.title("🔬 Research & Innovation Pipeline")
    
    # Filter trials
    df_trials = data['trials'] if selected_drug == "All Drugs" else data['trials'][data['trials']['drug_query'].str.contains(selected_drug, case=False, na=False)]
    
    col_f, col_g = st.columns([1, 2])
    
    with col_f:
        # Phase distribution
        phase_dist = df_trials['phase'].value_counts().reset_index()
        phase_dist.columns = ['Phase', 'Count']
        # Sort phases correctly
        phase_order = ['PHASE1', 'PHASE2', 'PHASE3', 'PHASE4', 'EARLY_PHASE1', 'NOT_APPLICABLE']
        phase_dist['Phase'] = pd.Categorical(phase_dist['Phase'], categories=phase_order, ordered=True)
        phase_dist = phase_dist.sort_values('Phase')
        
        fig_phase = px.funnel(phase_dist, x='Count', y='Phase', title="Clinical Trial Attrition Funnel",
                             color_discrete_sequence=['#6C5CE7'])
        fig_phase.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_phase, use_container_width=True)
    
    with col_g:
        # Trial Status Pie
        status_dist = df_trials['overall_status'].value_counts().head(5).reset_index()
        status_dist.columns = ['Status', 'Count']
        fig_status = px.pie(status_dist, values='Count', names='Status', title="Trial Status Distribution",
                           color_discrete_sequence=px.colors.sequential.Purples_r)
        fig_status.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_status, use_container_width=True)

    st.markdown("### 📋 Exploration Registry")
    st.write("Browse current and historical clinical studies for the selected GLP-1 focus.")
    st.dataframe(df_trials[['brief_title', 'overall_status', 'phase', 'enrollment', 'lead_sponsor']].sort_values('enrollment', ascending=False), 
                 use_container_width=True, hide_index=True)

# Footer
st.markdown("<br><hr><center style='opacity: 0.5;'>GLP-1 Pulse Analytics Dashboard | Data Source: FDA FAERS, Google Trends, ClinicalTrials.gov | © 2024</center>", unsafe_allow_html=True)
