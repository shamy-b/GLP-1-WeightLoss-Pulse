# GLP-1 WeightLoss Pulse 💉

An interactive, premium Streamlit dashboard for analyzing the clinical, financial, and social impact of GLP-1 receptor agonists (Ozempic, Wegovy, Mounjaro, and more).

## 🌟 Features
- **Executive Summary**: High-level KPIs and drug spotlights.
- **Clinical Safety Profile**: Deep dive into FDA FAERS adverse event reports.
- **Market Pulse**: Correlation analysis between stock prices (LLY, NVO) and Google Search trends.
- **Research Pipeline**: Visualization of clinical trials from Phase 1 to Phase 4.
- **Global Filtering**: Dynamic drug-specific analysis across all modules.

## 🛠️ Tech Stack
- **Dashboard**: Streamlit, Streamlit-Option-Menu, Streamlit-Lottie
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS (Glassmorphism & Dark Mode)

## 📂 Project Structure
```text
GLP1-Analytics Weight Loss Drug Trends/
├── Dataset/                     # 8 CSV files (FAERS, Stocks, Trends, etc.)
├── eda.ipynb                    # Preliminary Exploratory Data Analysis
├── app.py                       # Main Streamlit Dashboard logic
├── style.css                    # Custom premium styling
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

## 🚀 How to Run Locally
1. **Clone the repository** (if applicable).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Data Sources
- **FDA FAERS**: Adverse event reporting system.
- **Google Trends**: Public interest search data.
- **Yahoo Finance**: Historical stock prices for Eli Lilly & Novo Nordisk.
- **ClinicalTrials.gov**: Global research registry.
- **Wikipedia**: Drug summaries and imagery.

---
Built with ❤️ for the GLP-1 Analytics Project.
