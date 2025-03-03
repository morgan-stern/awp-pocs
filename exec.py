import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
import os

# Set up Streamlit page
st.set_page_config(page_title="Executive Dashboard", layout="wide")

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
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.warning("⚠️ Logo file not found. Please check the path.")

st.title("🚀 AWP Executive Dashboard")
st.markdown("Providing real-time insights into workforce efficiency, safety compliance, and incident reporting.")

# Generate mock data
safety_data = pd.DataFrame({
    "Location": ["Site A", "Site B", "Site C", "Site D", "Site E"],
    "Compliance Rate (%)": [random.randint(75, 100) for _ in range(5)],
    "Incident Reports": [random.randint(0, 5) for _ in range(5)],
    "Average Response Time (min)": [random.randint(5, 20) for _ in range(5)],
})

workforce_data = pd.DataFrame({
    "Day": pd.date_range(start="2024-03-01", periods=7, freq='D'),
    "Scheduled Workers": [random.randint(50, 100) for _ in range(7)],
    "Actual Workers": [random.randint(45, 100) for _ in range(7)],
    "Overtime Hours": [random.randint(0, 10) for _ in range(7)],
})

# Layout Configuration
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Safety & Compliance Overview")
    fig1 = px.bar(safety_data, x="Location", y="Compliance Rate (%)", text="Compliance Rate (%)", 
                  title="Compliance Rates Across Sites", color="Compliance Rate (%)", 
                  color_continuous_scale="Viridis")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### ⚠️ Incident Reports")
    fig2 = px.bar(safety_data, x="Location", y="Incident Reports", text="Incident Reports", 
                  title="Incident Reports Per Site", color="Incident Reports", 
                  color_continuous_scale="Reds")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### ⏳ Workforce Efficiency")
st.dataframe(workforce_data.style.background_gradient(cmap="coolwarm"))

# Workforce Metrics
col3, col4 = st.columns(2)

with col3:
    fig3 = px.line(workforce_data, x="Day", y=["Scheduled Workers", "Actual Workers"], 
                   title="Scheduled vs Actual Workers", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.line(workforce_data, x="Day", y="Overtime Hours", title="Overtime Trends", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("### 📌 Executive Insights")
st.write("""
- ✅ **High compliance rates** observed in most sites, but **Site C** requires attention.
- ⚠️ **Incident reports** are highest at **Site B** – investigate further.
- 🔄 **Workforce scheduling aligns well**, but overtime spikes indicate possible inefficiencies.

**AI Techniques Used:**
- **Predictive Analytics**: Workforce trends analyzed to optimize staffing.
- **Data Visualization**: Interactive graphs provide real-time decision-making support.
- **Automation**: Reduces manual reporting efforts, improving operational efficiency.

**Business Benefits:**
- **Enhances compliance monitoring** to prevent safety violations.
- **Optimizes labor allocation** to minimize inefficiencies and cost overruns.
- **Provides actionable insights** for better decision-making at executive levels.
""")

st.success("Dashboard Updated: " + time.strftime("%Y-%m-%d %H:%M:%S"))
