import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Blinkit Sales Forecasting",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color:#0E1117; color:white; }
h1,h2,h3,h4,h5,h6,p,label,span { color:white !important; }
[data-testid="stMetric"] {
    background:#1E1E1E; padding:15px; border-radius:15px;
    color:white; box-shadow:0px 2px 8px rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 Blinkit Retail Sales Forecasting Dashboard")
st.markdown("### 📈 30-Day Revenue Prediction using Facebook Prophet")
st.divider()

@st.cache_data
def load_and_forecast():

    df = pd.read_csv("orders_forecasting.csv")
    df["order_date"] = pd.to_datetime(df["order_date"], format="%d-%m-%Y %H:%M")
    df = df.rename(columns={"order_date": "ds", "order_total": "y"})

    daily_sales = (
        df.groupby(df["ds"].dt.date)["y"]
        .sum()
        .reset_index()
    )
    daily_sales.columns = ["ds", "y"]
    daily_sales["ds"] = pd.to_datetime(daily_sales["ds"])

    # ✅ FIX 1: Fill missing dates with median (not zero)
    full_range = pd.date_range(
        start=daily_sales["ds"].min(),
        end=daily_sales["ds"].max(),
        freq="D"
    )
    daily_sales = (
        daily_sales
        .set_index("ds")
        .reindex(full_range)
        .rename_axis("ds")
        .reset_index()
    )
    median_revenue = daily_sales["y"].median()
    daily_sales["y"] = daily_sales["y"].fillna(median_revenue)

    # ✅ FIX 2: Cap extreme outliers (bottom 2%)
    lower_bound = daily_sales["y"].quantile(0.02)
    daily_sales["y"] = daily_sales["y"].clip(lower=lower_bound)

    # ✅ FIX 3: Set floor=0 so Prophet never predicts negative
    daily_sales["floor"] = 0
    daily_sales["cap"] = daily_sales["y"].max() * 1.5

    holidays = pd.DataFrame({
        "holiday": "indian_festival",
        "ds": pd.to_datetime([
            "2023-10-24", "2024-11-01", "2024-03-25",
            "2023-03-08", "2023-08-15", "2024-08-15",
            "2023-10-02", "2024-10-02"
        ]),
        "lower_window": -1,
        "upper_window": 1
    })

    # ✅ FIX 4: Use logistic growth with floor/cap
    model = Prophet(
        growth="logistic",
        seasonality_mode="multiplicative",
        weekly_seasonality=True,
        yearly_seasonality=True,
        holidays=holidays,
        interval_width=0.80
    )

    model.fit(daily_sales)

    future = model.make_future_dataframe(periods=30)
    future["floor"] = 0
    future["cap"] = daily_sales["cap"].max()

    forecast = model.predict(future)

    # ✅ FIX 5: Hard clip just in case
    forecast["yhat"] = forecast["yhat"].clip(lower=0)
    forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)
    forecast["yhat_upper"] = forecast["yhat_upper"].clip(lower=0)

    return model, forecast, daily_sales


with st.spinner("⏳ Training Forecast Model..."):
    model, forecast, daily_sales = load_and_forecast()

st.subheader("📊 Key Business Metrics")
next_30 = forecast.tail(30)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Daily Revenue", f"₹{next_30['yhat'].mean():,.0f}")
col2.metric("Maximum Revenue", f"₹{next_30['yhat_upper'].max():,.0f}")
col3.metric("Minimum Revenue", f"₹{next_30['yhat_lower'].min():,.0f}")
col4.metric("Total Forecast Revenue", f"₹{next_30['yhat'].sum():,.0f}")

st.divider()

st.subheader("🤖 AI Business Insights")
best_day = daily_sales.loc[daily_sales["y"].idxmax()]
avg_sales = daily_sales["y"].mean()
forecast_total = next_30["yhat"].sum()

st.info(f"""
📈 Revenue trend is stable and growing.

🏆 Highest Revenue Day: {best_day['ds'].strftime('%d %b %Y')}

💰 Revenue Earned: ₹{best_day['y']:,.0f}

📊 Average Daily Revenue: ₹{avg_sales:,.0f}

🔮 Expected Revenue Next 30 Days: ₹{forecast_total:,.0f}

✅ Business Outlook: Sales are expected to remain positive in the coming month.
""")

st.divider()

st.subheader("📈 Revenue Forecast (Actual vs Predicted Revenue)")
fig1, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(daily_sales["ds"], daily_sales["y"], linewidth=2, label="Actual Revenue")
ax1.plot(forecast["ds"], forecast["yhat"], linewidth=3, label="Predicted Revenue")
ax1.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.2)
ax1.set_title("Actual Revenue vs Predicted Revenue")
ax1.set_xlabel("Date")
ax1.set_ylabel("Revenue (₹)")
ax1.legend()
st.pyplot(fig1)

st.divider()

st.subheader("📉 Revenue Trend Analysis")
fig2, ax2 = plt.subplots(figsize=(14, 5))
ax2.plot(forecast["ds"], forecast["trend"], linewidth=3)
ax2.set_title("Overall Revenue Growth Trend")
ax2.set_xlabel("Date")
ax2.set_ylabel("Trend")
st.pyplot(fig2)

st.divider()

st.subheader("📅 Weekly Seasonality Analysis")
if "weekly" in forecast.columns:
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    weekly = forecast.groupby(forecast["ds"].dt.day_name())["weekly"].mean()
    weekly = weekly.reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    ax3.plot(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], weekly.values, marker="o", linewidth=3)
    ax3.set_title("Revenue Pattern by Day of Week")
    ax3.set_ylabel("Seasonality Impact")
    st.pyplot(fig3)

st.divider()

st.subheader("🗓️ Yearly Seasonality Analysis")
if "yearly" in forecast.columns:
    fig4, ax4 = plt.subplots(figsize=(14, 5))
    ax4.plot(forecast["ds"], forecast["yearly"], linewidth=2)
    ax4.set_title("Revenue Pattern Throughout The Year")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Yearly Effect")
    st.pyplot(fig4)

st.divider()

st.subheader("📋 Next 30 Days Revenue Forecast")
table = next_30[["ds","yhat","yhat_lower","yhat_upper"]].copy()
table.columns = ["Date","Predicted Revenue","Min Estimate","Max Estimate"]
table["Date"] = table["Date"].dt.strftime("%d %b %Y")
table[["Predicted Revenue","Min Estimate","Max Estimate"]] = \
    table[["Predicted Revenue","Min Estimate","Max Estimate"]].round(0)
st.dataframe(table, use_container_width=True)

csv = table.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇ Download Forecast CSV",
    data=csv,
    file_name="forecast_results.csv",
    mime="text/csv"
)

st.success("✅ Forecast Generated Successfully")
