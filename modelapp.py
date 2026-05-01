import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(
    page_title="GLP-1 AI Risk Predictor",
    page_icon="🔮",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_assets():
    # Check if files exist
    required_files = ['glp1_risk_model.joblib', 'scaler.joblib', 'le_sex.joblib', 'feature_names.joblib']
    for f in required_files:
        if not os.path.exists(f):
            return None, None, None, None
            
    model = joblib.load('glp1_risk_model.joblib')
    scaler = joblib.load('scaler.joblib')
    le_sex = joblib.load('le_sex.joblib')
    features = joblib.load('feature_names.joblib')
    return model, scaler, le_sex, features

model, scaler, le_sex, features = load_model_assets()

if model is None:
    st.error("🚨 **Model Files Missing**")
    st.info("Please run the **`model_training.ipynb`** notebook completely to generate the required model and feature files (`glp1_risk_model.joblib`, `feature_names.joblib`, etc.).")
else:
    st.title("🔮 GLP-1 Patient Risk Predictor")
    st.markdown("### AI-Powered Adverse Event Probability Assessment")
    st.write("Enter patient details below to estimate the probability of a 'Serious' adverse reaction based on FDA data.")

    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Patient Age", 18, 100, 45)
            weight = st.number_input("Patient Weight (kg)", 40, 200, 85)
        
        with col2:
            sex = st.selectbox("Patient Sex", ["Male", "Female", "Unknown"])
            
            # Extract drug names from features
            drug_list = sorted([f.replace("drug_", "") for f in features if f.startswith("drug_")])
            drug = st.selectbox("Select GLP-1 Drug", drug_list if drug_list else ["SEMAGLUTIDE", "TIRZEPATIDE", "LIRAGLUTIDE"])

        st.markdown("---")
        submitted = st.form_submit_button("CALCULATE RISK PROBABILITY")

    if submitted:
        try:
            # Prepare Input Data
            input_df = pd.DataFrame(columns=features)
            input_df.loc[0] = 0 # Initialize with zeros
            
            # Fill Basic Info
            input_df['patient_age_years'] = age
            input_df['patient_weight_kg'] = weight
            
            # Handle sex encoding safely
            try:
                input_df['patient_sex_encoded'] = le_sex.transform([sex])[0]
            except:
                input_df['patient_sex_encoded'] = 0 # Fallback
            
            # Fill Drug OHE
            drug_col = f"drug_{drug}"
            if drug_col in input_df.columns:
                input_df[drug_col] = 1
                
            # Scale
            input_scaled = scaler.transform(input_df)
            
            # Predict
            prob = model.predict_proba(input_scaled)[0][1]
            risk_pct = prob * 100

            # Visual Results
            st.markdown("### Prediction Results")
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_pct,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score", 'font': {'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#ff4b4b" if risk_pct > 50 else "#ffa500" if risk_pct > 25 else "#00cc96"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 25], 'color': 'rgba(0, 204, 150, 0.2)'},
                        {'range': [25, 50], 'color': 'rgba(255, 165, 0, 0.2)'},
                        {'range': [50, 100], 'color': 'rgba(255, 75, 75, 0.2)'}],
                }
            ))
            fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)

            if risk_pct > 50:
                st.error(f"**High Risk Warning**: There is a {risk_pct:.1f}% probability of a serious event.")
            elif risk_pct > 25:
                st.warning(f"**Moderate Risk**: Probability of a serious event is {risk_pct:.1f}%.")
            else:
                st.success(f"**Low Risk**: Probability of a serious event is {risk_pct:.1f}%.")
        except Exception as e:
            st.error(f"Prediction Error: {e}")
