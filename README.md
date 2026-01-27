# ✈️ Flight Delay Analysis & Prediction (Nov 2024 to Oct 2025 – US DOT BTS)

## 📌 Project Overview

This project is an end-to-end Data Analytics and Data Science case study based on flight data from the U.S. Department of Transportation (DOT) Bureau of Transportation Statistics (BTS), covering **from November 2024 to October 2025**.

The goal is twofold:

1. **Data Analytics**: Perform exploratory data analysis (EDA) and build meaningful KPIs and visualizations to understand flight delays and cancellations.
2. **Machine Learning**: Build predictive models to classify whether a flight will be delayed (≥15 minutes), comparing multiple algorithms.

The project follows a complete pipeline:
- Data cleaning & preprocessing  
- Feature engineering  
- Exploratory Data Analysis (EDA)  
- Visualization  
- Machine Learning modeling & evaluation  

---

## 🧰 Tech Stack

- **Python**
  - pandas, numpy
  - matplotlib, seaborn
  - scikit-learn
  - imbalanced-learn
  - xgboost
- **Visualization**
  - matplotlib / seaborn (EDA)
  - Tableau (dashboarding)
- **Machine Learning Models**
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - XGBoost

---

## 📂 Dataset

Source: U.S. DOT – Bureau of Transportation Statistics (BTS)

Scope:
- Domestic US flights
- From November 2024 to October 2025 

Key variables include:
- Flight date components (year, month, day, day of week)
- Origin & destination airports
- Departure and arrival times
- Departure and arrival delays
- Delay indicators (15+ minutes)
- Cancellation flags and cancellation codes
- Delay causes (carrier, weather, NAS, security)

---

## 🧹 Data Cleaning & Feature Engineering

Main preprocessing steps:

- Handled missing values while preserving cancellation information
- Converted time columns into datetime format
- Created categorical bins for departure time (`dep_bin`)
- Added engineered features:
  - `season` (Winter, Spring, Summer, Autumn)
  - `delay_category` (On Time, Minor Delay, Moderate Delay, Severe Delay, Cancelled)
- Encoded categorical variables using OneHotEncoder
- Scaled numerical variables using StandardScaler
- Built a unified preprocessing pipeline using `ColumnTransformer`

Special care was taken to avoid **data leakage** by embedding preprocessing directly inside ML pipelines.

---

## 📊 Exploratory Data Analysis (EDA)

The EDA focuses on operational and business-relevant KPIs, including:

- Distribution of delay categories
- Average delays by:
  - Day of week
  - Time of day (bins)
  - Season
- Cancellation rate by season and cancellation code
- Delay categories by season
- Calendar-style heatmap of average daily delays
- Identification of the most problematic routes

Visualizations include:
- Bar charts
- Pie charts
- Stacked bars
- Heatmaps
- Route maps
- Calendar heatmaps

These analyses highlight temporal patterns, seasonal effects, and operational bottlenecks.

---

## 🤖 Machine Learning

### 🎯 Objective

Binary classification:
- **0** → On-time flight  
- **1** → Delayed flight (≥15 minutes)

Primary business goal:
> Maximize recall for delayed flights in order to proactively detect operational disruptions.

---

### ⚙️ Preprocessing Pipeline

A unified pipeline was used for all models:

- Numerical features → StandardScaler
- Categorical features → OneHotEncoder
- Models trained on top of the same preprocessing logic

Class imbalance was addressed using:
- Oversampling
- Undersampling
- SMOTE (where applicable)

---

### 🧠 Models Trained

Four supervised models were implemented and compared:

1. Logistic Regression (baseline linear model)
2. Decision Tree (non-linear baseline)
3. Random Forest (ensemble model)
4. XGBoost (gradient boosting)

Each model was evaluated using:

- Precision (delay class)
- Recall (delay class)
- F1-score
- Confusion Matrix

---

## 📈 Model Comparison

Models were compared on the same test set using consistent metrics.

Key findings:
- Logistic Regression provides a strong baseline but struggles with non-linear relationships.
- Decision Trees improve recall by capturing feature interactions.
- Random Forest further stabilizes performance through ensembling.
- XGBoost delivers the best overall performance, achieving the strongest balance between recall and precision for delayed flights.


XGBoost was selected as the final model due to superior performance in detecting delayed flights.

---

## ✅ Key Conclusions

- Flight delays show strong dependency on seasonality, time of day, and specific routes.
- The dataset is significantly imbalanced, making recall a critical metric.
- Tree-based and boosting models outperform linear models for this task.
- XGBoost provides the best operational value for proactive delay detection.

---

## 🚀 Future Improvements

Potential next steps:

- Hyperparameter tuning via cross-validation
- Threshold optimization for business-specific tradeoffs
- SHAP values for model explainability
- Incorporation of weather data
- Time-series modeling
- Deployment as an API or dashboard integration


