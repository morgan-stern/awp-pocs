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

# Tabs for Executive Summary, Historical Analysis, Future Forecasting, US Heatmap, and Pennsylvania Breakdown
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Executive Summary", "📈 Historical Utilization", "🔮 AI Forecasting", "🗺️ US Workforce Heatmap", "📍 Pennsylvania Breakdown"])

with tab4:
    st.subheader("🗺️ US Workforce Utilization Map")
    
    # Generate utilization data for all 50 states
    us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    state_data = pd.DataFrame({
        "State": us_states,
        "Utilization (%)": np.clip(np.random.normal(85, 5, len(us_states)), 70, 100)  # Ensuring values between 70-100%
    })
    
    fig4 = px.choropleth(state_data, 
                          locations="State", 
                          locationmode="USA-states", 
                          color="Utilization (%)", 
                          color_continuous_scale=[(0, "red"), (0.5, "yellow"), (0.75, "green"), (1, "red")],
                          scope="usa", 
                          title="Workforce Utilization Across the US")
    st.plotly_chart(fig4, use_container_width=True)
    
    st.dataframe(state_data.style.background_gradient(cmap="coolwarm"))

with tab5:
    st.subheader("📍 Pennsylvania Workforce Utilization by County")
    
    # Simulated county-level workforce utilization for Pennsylvania
    pa_counties = ["Philadelphia", "Allegheny", "Montgomery", "Bucks", "Delaware", "Lancaster", "Chester", "York", "Berks", "Lehigh"]
    
    pa_data = pd.DataFrame({
        "County": pa_counties,
        "Utilization (%)": np.clip(np.random.normal(85, 5, len(pa_counties)), 70, 100)  # Ensuring values between 70-100%
    })
    
    fig5 = px.bar(pa_data, x="County", y="Utilization (%)", color="Utilization (%)",
                  title="Workforce Utilization by County in Pennsylvania",
                  color_continuous_scale=[(0, "red"), (0.5, "yellow"), (0.75, "green"), (1, "red")])
    st.plotly_chart(fig5, use_container_width=True)
    
    st.dataframe(pa_data.style.background_gradient(cmap="coolwarm"))