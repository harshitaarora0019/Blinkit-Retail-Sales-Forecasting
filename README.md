# 🛒 Blinkit Retail Sales Forecasting

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-purple?style=for-the-badge&logo=pandas">
  <img src="https://img.shields.io/badge/Prophet-Time%20Series-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/SQL-Data%20Extraction-orange?style=for-the-badge">
</p>

---

## 🌐 Live Demo

**Streamlit App:**
https://blinkit-retail-sales-forecasting-et3mnehh3up4nghxogyxgy.streamlit.app/

---

## 📌 Project Overview

Blinkit Retail Sales Forecasting is an AI-powered analytics dashboard that predicts future sales revenue using historical retail order data.

The project combines SQL-based data extraction, data preprocessing using Pandas, time-series forecasting using Facebook Prophet, and interactive business visualization through Streamlit.

The dashboard enables businesses to forecast future revenue, identify sales trends, analyze seasonal demand patterns, and make data-driven decisions.

### Key Objectives

✅ Forecast future revenue

✅ Analyze business growth trends

✅ Identify seasonal sales patterns

✅ Generate AI-powered business insights

✅ Monitor key performance indicators (KPIs)

---

## 🎯 Problem Statement

Retail businesses often face challenges in accurately predicting future demand and revenue.

Without proper forecasting:

* Inventory planning becomes inefficient
* Revenue expectations remain uncertain
* Seasonal opportunities may be missed
* Strategic decisions become reactive instead of proactive

This project addresses these challenges by using Machine Learning-based forecasting techniques to predict future sales revenue.

---

## 🚀 Features

### 📊 Business KPI Dashboard

* Average Daily Revenue
* Maximum Revenue
* Minimum Revenue
* Total Forecast Revenue

### 📈 Revenue Forecasting

Predicts future revenue for the next 30 days using Facebook Prophet.

### 📉 Trend Analysis

Visualizes long-term business growth and revenue trends.

### 📅 Weekly Seasonality Analysis

Identifies the best-performing weekdays based on revenue.

### 🗓️ Yearly Seasonality Analysis

Analyzes revenue fluctuations throughout the year.

### 🤖 AI Business Insights

Automatically generates:

* Highest Revenue Day
* Average Revenue
* Revenue Trends
* Future Revenue Expectations

### 📥 Export Forecast Results

Download forecast results as CSV files.

---

## 🛠️ Tech Stack

<table>
<tr>
<th>Category</th>
<th>Technology</th>
</tr>

<tr>
<td>Programming Language</td>
<td>Python</td>
</tr>

<tr>
<td>Database Querying</td>
<td>SQL</td>
</tr>

<tr>
<td>Dashboard Framework</td>
<td>Streamlit</td>
</tr>

<tr>
<td>Data Processing</td>
<td>Pandas</td>
</tr>

<tr>
<td>Forecasting Model</td>
<td>Facebook Prophet</td>
</tr>

<tr>
<td>Data Visualization</td>
<td>Matplotlib</td>
</tr>

<tr>
<td>Dataset Format</td>
<td>CSV</td>
</tr>

</table>

---

## 🧠 Forecasting Workflow

```text
SQL Database
      │
      ▼
Data Extraction
      │
      ▼
CSV Dataset
      │
      ▼
Data Cleaning (Pandas)
      │
      ▼
Feature Engineering
      │
      ▼
Facebook Prophet Model
      │
      ▼
Revenue Prediction
      │
      ▼
Streamlit Dashboard
```

---

📂 Project Structure
Blinkit-Retail-Sales-Forecasting/
│
├── sql/
│   └── blinkit_analysis.sql
│
├── Screenshot/
│   ├── Blinkit Retail Sales Forecasting Dashboard.png
│   ├── Key Business Metrics.png
│   ├── Revenue Forecast.png
│   ├── AI Business Insights.png
│   └── Next 30 Days Revenue Forecast.png
│
├── notebooks/
│   └── Blinkit_Forecasting.ipynb
│
├── main.py
├── orders_forecasting.csv
├── requirements.txt
└── README.md

📁 Folder Description
Folder/File	Description
sql/	Contains SQL queries used for retail analytics, joins, KPI calculations, and forecasting dataset preparation
Screenshot/	Dashboard screenshots and project outputs
notebooks/	Jupyter Notebook used for forecasting model development and analysis
main.py	Streamlit application source code
orders_forecasting.csv	Forecasting dataset generated from SQL analysis
requirements.txt	Project dependencies
README.md	Project documentation

## 📈 Dashboard Modules

### Revenue Forecast

Displays actual revenue and predicted revenue with confidence intervals.

### Revenue Trend Analysis

Visualizes long-term revenue growth patterns.

### Weekly Seasonality Analysis

Identifies the most profitable weekdays.

### Yearly Seasonality Analysis

Shows annual revenue patterns and seasonal demand.

### AI Business Insights

Generates actionable business insights from forecast results.

---

## 💡 Business Benefits

* Better inventory planning
* Revenue estimation
* Seasonal demand forecasting
* Strategic decision-making
* Business growth monitoring
* Improved operational efficiency

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/harshitaarora0019/Blinkit-Retail-Sales-Forecasting.git
```

### Navigate to Project Directory

```bash
cd Blinkit-Retail-Sales-Forecasting
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit Application

```bash
streamlit run main.py
```

---

## 📸 Dashboard Screenshots

### 🏠 Main Dashboard

<img src="Screenshot/Blinkit Retail Sales Forecasting Dashboard.png" width="100%">

<br><br>

### 📊 Key Business Metrics

<img src="Screenshot/Key Business Metrics.png" width="100%">

<br><br>

### 📈 Revenue Forecast

<img src="Screenshot/Revenue Forecast.png" width="100%">

<br><br>

### 🤖 AI Business Insights

<img src="Screenshot/AI Business Insights.png" width="100%">

<br><br>

### 📅 Next 30 Days Revenue Forecast

<img src="Screenshot/Next 30 Days Revenue Forecast.png" width="100%">

---

## 📊 Future Enhancements

* Product-wise Sales Forecasting
* Category-wise Revenue Analysis
* Real-Time Data Integration
* AI Chat Assistant
* Interactive Plotly Dashboards
* Cloud Deployment
* Automated Reporting System

---

## 👩‍💻 Developer

**Harshita Arora**
Passionate about Data Analytics, Machine Learning, Forecasting, Business Intelligence, and Dashboard Development.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

<p align="center">
<b>Built with ❤️ by Harshita Arora</b>
</p>
