import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="StellarMart Sales Dashboard",
    layout="wide"
)

# ===== LOAD DATA =====
@st.cache_data
def load_daily_sales():
    daily = pd.read_csv("data/daily_sales.csv")
    daily["transaction_date"] = pd.to_datetime(daily["transaction_date"])
    return daily

# Load data
daily = load_daily_sales()

# ===== KPIs =====
total_sales = daily["daily_sales"].sum()
avg_sales = daily["daily_sales"].mean()
peak_day = daily.loc[daily["daily_sales"].idxmax(), "transaction_date"]

# Convert peak day to safe string format for Streamlit
try:
    peak_day_str = peak_day.strftime("%Y-%m-%d")
except:
    peak_day_str = str(peak_day)

# ===== TITLE =====
st.title("📊 StellarMart Sales Forecasting Dashboard")

# Convert peak day to safe string format for Streamlit
try:
    peak_day_str = peak_day.strftime("%Y-%m-%d")
except Exception:
    peak_day_str = str(peak_day)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Avg Daily Sales", f"${avg_sales:,.0f}")
col3.metric("Peak Sales Day", peak_day_str)


st.markdown("---")

# ===== DAILY SALES CHART =====
fig1 = px.line(
    daily,
    x="transaction_date",
    y="daily_sales",
    title="📈 Daily Sales Over Time"
)
st.plotly_chart(fig1, use_container_width=True)

# ===== LOAD MODEL =====
try:
    model = joblib.load("models/sales_model.pkl")
    st.success("Model Loaded Successfully")
except:
    st.error("⚠️ Model file not found. Please train the model first.")
    st.stop()

# ===== FORECAST SECTION =====
st.header("🔮 14-Day Sales Forecast")

if st.button("Generate Forecast"):
    last_day_number = len(daily)
    future_days = pd.DataFrame({"day_number": range(last_day_number, last_day_number + 14)})

    forecast = model.predict(future_days)

    forecast_df = pd.DataFrame({
        "day": range(1, 15),
        "forecasted_sales": forecast
    })

    fig2 = px.bar(
        forecast_df,
        x="day",
        y="forecasted_sales",
        title="📅 14-Day Forecasted Sales"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.write("### 📄 Forecast Data")
    st.dataframe(forecast_df)

else:
    st.info("⬆️ Click the button above to generate the forecast.")
