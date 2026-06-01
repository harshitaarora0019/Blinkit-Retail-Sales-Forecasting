import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Blinkit Sales Forecasting",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# DARK THEME
# ==========================================
st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
    color:white;
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

[data-testid="stMetric"]{
    background:#1E1E1E;
    padding:15px;
    border-radius:15px;
    color:white;
    box-shadow:0px 2px 8px rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================
st.title("🛒 Blinkit Retail Sales Forecasting Dashboard")
st.markdown("### 📈 30-Day Revenue Prediction using Facebook Prophet")

st.divider()

# ==========================================
# LOAD DATA & FORECAST
# ==========================================
@st.cache_data
def load_and_forecast():

    df = pd.read_csv("orders_forecasting.csv")

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%d-%m-%Y %H:%M"
    )

    df = df.rename(
        columns={
            "order_date": "ds",
            "order_total": "y"
        }
    )

    # Daily Revenue
    daily_sales = (
        df.groupby(df["ds"].dt.date)["y"]
        .sum()
        .reset_index()
    )

    daily_sales.columns = ["ds", "y"]
    daily_sales["ds"] = pd.to_datetime(
        daily_sales["ds"]
    )

    # Indian Holidays
    holidays = pd.DataFrame({
        "holiday": "indian_festival",
        "ds": pd.to_datetime([
            "2023-10-24",
            "2024-11-01",
            "2024-03-25",
            "2023-03-08",
            "2023-08-15",
            "2024-08-15",
            "2023-10-02",
            "2024-10-02"
        ]),
        "lower_window": -1,
        "upper_window": 1
    })

    # Prophet Model
    model = Prophet(
        seasonality_mode="multiplicative",
        weekly_seasonality=True,
        yearly_seasonality=True,
        holidays=holidays
    )

    model.fit(daily_sales)

    future = model.make_future_dataframe(
        periods=30
    )

    forecast = model.predict(future)

    return model, forecast, daily_sales


with st.spinner("⏳ Training Forecast Model..."):
    model, forecast, daily_sales = load_and_forecast()

# ==========================================
# KPI METRICS
# ==========================================
st.subheader("📊 Key Business Metrics")

next_30 = forecast.tail(30)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Daily Revenue",
    f"₹{next_30['yhat'].mean():,.0f}"
)

col2.metric(
    "Maximum Revenue",
    f"₹{next_30['yhat_upper'].max():,.0f}"
)

col3.metric(
    "Minimum Revenue",
    f"₹{next_30['yhat_lower'].min():,.0f}"
)

col4.metric(
    "Total Forecast Revenue",
    f"₹{next_30['yhat'].sum():,.0f}"
)

st.divider()

# ==========================================
# AI BUSINESS INSIGHTS
# ==========================================
st.subheader("🤖 AI Business Insights")

best_day = daily_sales.loc[
    daily_sales["y"].idxmax()
]

avg_sales = daily_sales["y"].mean()

forecast_total = next_30["yhat"].sum()

st.info(
    f"""
📈 Revenue trend is stable and growing.

🏆 Highest Revenue Day:
{best_day['ds'].strftime('%d %b %Y')}

💰 Revenue Earned:
₹{best_day['y']:,.0f}

📊 Average Daily Revenue:
₹{avg_sales:,.0f}

🔮 Expected Revenue Next 30 Days:
₹{forecast_total:,.0f}

✅ Business Outlook:
Sales are expected to remain positive in the coming month.
"""
)

st.divider()

# ==========================================
# REVENUE FORECAST GRAPH
# ==========================================
st.subheader("📈 Revenue Forecast (Actual vs Predicted Revenue)")

fig1, ax1 = plt.subplots(figsize=(14,6))

ax1.plot(
    daily_sales["ds"],
    daily_sales["y"],
    linewidth=2,
    label="Actual Revenue"
)

ax1.plot(
    forecast["ds"],
    forecast["yhat"],
    linewidth=3,
    label="Predicted Revenue"
)

ax1.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.2
)

ax1.set_title("Actual Revenue vs Predicted Revenue")
ax1.set_xlabel("Date")
ax1.set_ylabel("Revenue (₹)")
ax1.legend()

st.pyplot(fig1)

st.divider()

# ==========================================
# REVENUE TREND GRAPH
# ==========================================
st.subheader("📉 Revenue Trend Analysis")

fig2, ax2 = plt.subplots(figsize=(14,5))

ax2.plot(
    forecast["ds"],
    forecast["trend"],
    linewidth=3
)

ax2.set_title("Overall Revenue Growth Trend")
ax2.set_xlabel("Date")
ax2.set_ylabel("Trend")

st.pyplot(fig2)

st.divider()

# ==========================================
# WEEKLY SEASONALITY GRAPH
# ==========================================
st.subheader("📅 Weekly Seasonality Analysis")

if "weekly" in forecast.columns:

    fig3, ax3 = plt.subplots(figsize=(10,4))

    weekly = forecast.groupby(
        forecast["ds"].dt.day_name()
    )["weekly"].mean()

    weekly = weekly.reindex([
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ])

    ax3.plot(
        ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        weekly.values,
        marker="o",
        linewidth=3
    )

    ax3.set_title(
        "Revenue Pattern by Day of Week"
    )

    ax3.set_ylabel(
        "Seasonality Impact"
    )

    st.pyplot(fig3)

st.divider()

# ==========================================
# YEARLY SEASONALITY GRAPH
# ==========================================
st.subheader("🗓️ Yearly Seasonality Analysis")

if "yearly" in forecast.columns:

    fig4, ax4 = plt.subplots(figsize=(14,5))

    ax4.plot(
        forecast["ds"],
        forecast["yearly"],
        linewidth=2
    )

    ax4.set_title(
        "Revenue Pattern Throughout The Year"
    )

    ax4.set_xlabel("Date")
    ax4.set_ylabel("Yearly Effect")

    st.pyplot(fig4)

st.divider()

# ==========================================
# FORECAST TABLE
# ==========================================
st.subheader("📋 Next 30 Days Revenue Forecast")

table = next_30[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].copy()

table.columns = [
    "Date",
    "Predicted Revenue",
    "Min Estimate",
    "Max Estimate"
]

table["Date"] = table["Date"].dt.strftime(
    "%d %b %Y"
)

table[
    [
        "Predicted Revenue",
        "Min Estimate",
        "Max Estimate"
    ]
] = table[
    [
        "Predicted Revenue",
        "Min Estimate",
        "Max Estimate"
    ]
].round(0)

st.dataframe(
    table,
    use_container_width=True
)

# ==========================================
# DOWNLOAD FORECAST
# ==========================================
csv = table.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Forecast CSV",
    data=csv,
    file_name="forecast_results.csv",
    mime="text/csv"
)

st.success("✅ Forecast Generated Successfully")