# GLP-1 WeightLoss Pulse: Analytics & AI Risk Predictor

## 🚀 Project Overview
**GLP-1 WeightLoss Pulse** is a comprehensive data science and machine learning project designed to analyze the impact, safety, and market trends of GLP-1 weight loss medications (such as Ozempic, Wegovy, Mounjaro, and Zepbound). 

The project combines **advanced data analytics** (Streamlit Dashboard) with **predictive AI** (Risk Assessment Model) to provide a 360-degree view of the GLP-1 landscape—from clinical adverse events to stock market performance.

---

## 🛠️ Features

### 1. Interactive Analytics Dashboard (`app.py`)
*   **Executive Summary:** High-level KPIs including total adverse reports and active clinical trials.
*   **Clinical Safety Profile:** Deep dive into patient demographics and reaction outcomes.
*   **Market Pulse:** Multi-axis visualization comparing Google Search interest with stock prices (Eli Lilly & Novo Nordisk).
*   **Research Pipeline:** Tracking the progression of GLP-1 drugs through clinical trial phases.

### 2. AI Patient Risk Predictor (`modelapp.py`)
*   **Machine Learning Model:** A highly optimized **HistGradientBoosting** classifier.
*   **Functionality:** Predicts the probability of a "Serious" adverse event based on a patient's Age, Weight, Sex, and specific Drug type.
*   **Performance Metrics:**
    *   **ROC AUC Score:** ~0.85 (High predictive power)
    *   **Recall (Serious Events):** 77% (Optimized for patient safety)
    *   **Stability:** Validated using 5-Fold Stratified Cross-Validation.

---

## 📊 Dataset Details
The project utilizes 8 interconnected datasets stored in the `Dataset/` directory:
1.  **`adverse_events.csv`**: Raw FDA adverse event reports.
2.  **`clinical_trials.csv`**: Data on active and completed GLP-1 trials.
3.  **`stock_prices.csv`**: Historical prices for LLY and NVO.
4.  **`search_trends.csv`**: Google Trends data for weight loss drug hype.
5.  **`drugs_overview.csv`**: Mechanism of action and manufacturer info.
6.  *Plus summary and reference datasets.*

---

## ⚙️ Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Setup Environment
```bash
# Clone the repository
git clone https://github.com/shamy-b/GLP-1-WeightLoss-Pulse.git
cd GLP-1-WeightLoss-Pulse

# Install dependencies
pip install -r requirements.txt
```

### 3. Training the Model
If you wish to re-train the AI model or view the training metrics:
1.  Open `model_training.ipynb` in Jupyter.
2.  Run all cells. This will generate the required `.joblib` files.

### 4. Running the Applications
*   **To view the Analytics Dashboard:**
    ```bash
    streamlit run app.py
    ```
*   **To use the AI Risk Predictor:**
    ```bash
    streamlit run modelapp.py
    ```

---

## 🧠 Machine Learning Pipeline
Our "Top Model" was developed through a rigorous 4-phase pipeline:
1.  **Preprocessing:** Handling missing values via grouped medians and standardizing patient age units.
2.  **Feature Engineering:** Converting unstructured "Reaction" text into binary features for top symptoms.
3.  **Optimization:** Using **GridSearchCV** to tune hyperparameters (learning rate, depth, etc.).
4.  **Serialization:** Saving the final model and scalers for real-time inference in the Streamlit app.

---

## 📜 Credits & License
Developed for portfolio purposes as a demonstration of **End-to-End Data Science**—from raw data cleaning to AI deployment.
