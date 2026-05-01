# GLP-1 WeightLoss Pulse: Advanced Analytics & AI Risk Forecasting

## 🚀 Project Overview
**GLP-1 WeightLoss Pulse** is an end-to-end data science and machine learning ecosystem designed to analyze the clinical safety, financial impact, and public interest surrounding GLP-1 medications (Ozempic, Wegovy, Mounjaro, and Zepbound). 

This project bridges the gap between **unstructured healthcare data** and **actionable AI insights**, providing a dual-layered approach:
1.  **Macro-Analytics**: A multi-page Streamlit dashboard tracking global market trends and FDA safety reports.
2.  **Micro-Forecasting**: A specialized AI engine that predicts individual patient risk probabilities for serious adverse reactions.

---

## 🛠️ Feature Deep-Dive

### 1. The Analytics Dashboard (`app.py`)
A comprehensive visual suite designed for healthcare analysts and market researchers:
*   **🏠 Executive Summary**: Real-time KPIs tracking total adverse reports, active clinical trials, and stock performance of Novo Nordisk (NVO) and Eli Lilly (LLY).
*   **🏥 Clinical Safety Profile**: 
    *   Interactive demographic analysis (Age & Sex distribution).
    *   Dynamic "Outcome Donut Charts" (Hospitalization vs. Life-Threatening vs. Non-Serious).
    *   Top 10 Adverse Reaction tracking per medication.
*   **📈 Market Pulse**: Dual-axis time-series visualization overlaying Google Search Interest (public hype) against historical stock price volatility.
*   **🔬 Research Pipeline**: A funnel visualization of clinical trials moving from Phase 1 to Phase 4.

### 2. AI Patient Risk Predictor (`modelapp.py`)
An interactive AI tool for predictive safety assessment:
*   **Core Engine**: Uses an optimized **HistGradientBoostingClassifier** (Scikit-Learn's state-of-the-art gradient boosting implementation).
*   **Predictive Logic**: Analyzes patient age, weight, biological sex, and specific GLP-1 drug type to output a real-time risk probability score.
*   **Safety Thresholds**: Implements colored visual alerts (Green/Orange/Red) to provide immediate feedback on predicted risk levels.

---

## 🧠 Machine Learning Methodology
The "Top Model" was developed through a rigorous scientific pipeline:

*   **Data Preprocessing**: 
    *   **Unit Standardization**: Automated conversion of patient ages from Months/Days/Weeks into uniform Year decimals.
    *   **Grouped Imputation**: Missing weight and age data were filled using medians grouped by specific medication types to maintain demographic accuracy.
*   **Feature Engineering**:
    *   Extracted the top 20 most frequent adverse reactions from ~100k reports.
    *   Engineered binary flag features to transform unstructured reaction text into structured input for the model.
*   **Imbalance Handling**: Utilized **SMOTE (Synthetic Minority Over-sampling Technique)** to address the heavy class imbalance (serious vs. non-serious events) in medical reporting.
*   **Optimization**: Applied **GridSearchCV** with 3-fold cross-validation to tune hyperparameters:
    *   `learning_rate`: 0.2
    *   `max_depth`: 20
    *   `max_iter`: 200
*   **Model Validation**: Achieving a stable **ROC-AUC of 0.85** and a **Recall of 77%** for high-risk cases.

---

## 📊 Dataset Architecture
The project utilizes 8 interconnected datasets (`Dataset/` folder):
*   `adverse_events.csv`: Primary source of patient-level clinical reports (FDA FAERS data).
*   `clinical_trials.csv`: Detailed records of global clinical study progressions.
*   `stock_prices.csv`: Daily historical pricing for key pharmaceutical players (LLY, NVO).
*   `search_trends.csv`: Aggregated search volume data for GLP-1 related keywords.
*   `wikipedia_summaries.csv`: Contextual information on drug mechanisms and history.

---

## ⚙️ Technical Stack
*   **Frontend**: Streamlit (Dashboarding), Plotly (Interactive Visuals).
*   **Data Handling**: Pandas, NumPy.
*   **Machine Learning**: Scikit-Learn, XGBoost, Imbalanced-Learn (SMOTE).
*   **Serialization**: Joblib.

---

## 🚀 Installation & Getting Started

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/shamy-b/GLP-1-WeightLoss-Pulse.git
cd GLP-1-WeightLoss-Pulse

# Install all required libraries
pip install -r requirements.txt
```

### 2. Training & Replication
To replicate the AI model or inspect the tuning results, open `model_training.ipynb` and run all cells. This generates the following artifacts:
*   `glp1_risk_model.joblib`: The trained model binary.
*   `scaler.joblib`: Numerical feature scaler.
*   `le_sex.joblib`: Label encoder for demographics.
*   `feature_names.joblib`: Column definitions for model inference.

### 3. Execution
**Analytics Dashboard:**
```bash
streamlit run app.py
```
**AI Risk Predictor:**
```bash
streamlit run modelapp.py
```

---

## 🛠️ Roadmap & Future Enhancements
- [ ] **NLP Integration**: Implement TF-IDF or BERT embeddings for more nuanced analysis of adverse reaction text descriptions.
- [ ] **Time-Series Forecasting**: Add an LSTM-based predictor for future stock price movements based on clinical trial success rates.
- [ ] **Multi-Drug Comparison**: Expand the AI predictor to compare risk profiles across multiple GLP-1 drugs simultaneously.
