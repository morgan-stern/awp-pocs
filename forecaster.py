import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import os
import time

# Set up Streamlit page
st.set_page_config(page_title="AI Resource Forecasting Dashboard", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        body {
            background-color: #2F3763;
            color: white;
        }
        .stApp {
            background-color: #2F3763;
        }
        .sidebar .sidebar-content {
            background-color: #7372B5 !important;
        }
        header {
            background-color: #464881;
        }
        .sidebar img {
            width: 50% !important;
            display: block;
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and Display Logo
logo_path = "Artboard.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=100)
else:
    st.sidebar.warning("⚠️ Logo file not found. Please check the path.")

st.title("📊 AI Resource Forecasting Dashboard")
st.write("Analyzing workforce utilization and predicting future staffing needs using AI-driven forecasting models.")

# Tabs for Executive Summary, Historical Analysis, Future Forecasting
tab1, tab2, tab3 = st.tabs(["🏆 Executive Summary", "📈 Historical Utilization", "🔮 AI Forecasting"])

with tab1:
    st.subheader("🏆 Executive Summary")
    st.write("""
    - 📊 **Top insights:** Workforce demand is expected to increase in **Texas and Florida** over the next quarter.
    - 🚨 **Risk indicators:** Midwest offices are at risk of **understaffing** due to seasonal fluctuations.
    - 🔮 **AI Recommendation:** Redistribute 10% of available workers to high-demand areas to balance workloads.
    - 🌦️ **External Data Considerations:** Predicted extreme weather events in the Northeast may impact scheduling efficiency.
    
    **AI Techniques Used:**
    - **Random Forest Regression**: Provides robust forecasting based on past utilization.
    - **Scenario Simulation**: Allows executives to test different variables and see projected outcomes.
    """)
    st.success("Dashboard Updated: " + time.strftime("%Y-%m-%d %H:%M:%S"))

with tab2:
    st.subheader("📍 Workforce Utilization Trends")
    
    # Simulated historical data
    num_offices = 50
    historical_data = pd.DataFrame({
        "Office": [f"Office {i+1}" for i in range(num_offices)],
        "Utilization (%)": np.random.randint(50, 100, num_offices),
        "Seasonal Impact": np.random.choice(["High", "Moderate", "Low"], num_offices),
        "Weather Impact": np.random.choice(["None", "Storms", "Extreme Heat"], num_offices)
    })
    
    fig1 = px.bar(historical_data, x="Office", y="Utilization (%)", color="Seasonal Impact",
                  title="Workforce Utilization by Office", height=500)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.dataframe(historical_data.style.background_gradient(cmap="coolwarm"))

with tab3:
    st.subheader("🔮 AI-Powered Forecasting")
    
    # Simulated Forecasting Data
    forecast_days = 30
    forecast_data = pd.DataFrame({
        "Day": pd.date_range(start=pd.Timestamp.today(), periods=forecast_days, freq='D'),
        "Predicted Utilization (%)": np.random.randint(60, 95, forecast_days)
    })
    
    # Train ML Model (RandomForest for mock-up)
    X = np.arange(forecast_days).reshape(-1, 1)
    y = forecast_data["Predicted Utilization (%)"].values
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    forecast_data["AI Forecast (%)"] = model.predict(X)
    
    st.markdown("### 🎛️ Adjust Forecast Variables")
    seasonality_factor = st.slider("Seasonal Impact", min_value=0, max_value=100, value=50)
    weather_disruption = st.slider("Weather Disruption Level", min_value=0, max_value=100, value=30)
    economic_trend = st.slider("Economic Growth Factor", min_value=0, max_value=100, value=40)
    workforce_fluctuation = st.slider("Workforce Availability Change", min_value=0, max_value=100, value=50)
    
    adjusted_forecast = forecast_data["AI Forecast (%)"] * (
        1 + (seasonality_factor - 50) / 200) * (1 - weather_disruption / 200) * (1 + economic_trend / 300) * (1 - workforce_fluctuation / 250)
    
    forecast_data["Adjusted AI Forecast (%)"] = adjusted_forecast
    
    fig2 = px.line(forecast_data, x="Day", y=["Predicted Utilization (%)", "AI Forecast (%)", "Adjusted AI Forecast (%)"],
                   title="AI-Based Utilization Forecast with Adjustable Factors", markers=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.dataframe(forecast_data.style.background_gradient(cmap="coolwarm"))
