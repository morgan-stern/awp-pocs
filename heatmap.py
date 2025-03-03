import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Set up Streamlit page
st.set_page_config(page_title="Workforce & Asset Heatmap Dashboard", layout="wide")

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

st.title("🗺️ Workforce & Asset Utilization Heatmaps")
st.write("Visualizing workforce and asset distribution across the US and Pennsylvania for better resource planning.")

# Role selection
role_options = ["All Roles", "Field Supervisor", "Driver", "Flagger", "Qualified Observer"]
selected_role = st.sidebar.selectbox("Select Workforce Role", role_options)

# Asset selection
asset_options = ["All Assets", "Trucks", "AFAD Units"]
selected_asset = st.sidebar.selectbox("Select Asset Type", asset_options)

# Adjustable Threshold Slider
utilization_threshold = st.sidebar.slider("Set Utilization Threshold (%)", min_value=50, max_value=100, value=85)

# AI-Powered Relocation Strategies Button
if st.sidebar.button("Generate AI-Based Relocation Plan"):
    st.sidebar.success("🚚 AI recommends moving 5 AFAD Units from PA to TX and redistributing 10 Trucks from NY to FL.")

# Tabs for US Heatmap and Pennsylvania Breakdown
tab1, tab2 = st.tabs(["🗺️ US Workforce & Asset Heatmap", "📍 Pennsylvania Breakdown"])

with tab1:
    st.subheader("🗺️ US Workforce & Asset Utilization Map")
    
    # Generate utilization data for all 50 states
    us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    state_data = pd.DataFrame({
        "State": us_states,
        "Utilization (%)": np.clip(np.random.normal(utilization_threshold, 5, len(us_states)), 50, 100)  # Ensuring values between 50-100%
    })
    
    fig1 = px.choropleth(state_data, 
                          locations="State", 
                          locationmode="USA-states", 
                          color="Utilization (%)", 
                          color_continuous_scale=[(0, "red"), (0.5, "yellow"), (0.75, "green"), (1, "red")],
                          scope="usa", 
                          title=f"{selected_role} & {selected_asset} Utilization Across the US")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.dataframe(state_data.style.background_gradient(cmap="coolwarm"))

with tab2:
    st.subheader("📍 Pennsylvania Workforce & Asset Utilization by City")
    
    # Simulated city-level workforce utilization for Pennsylvania
    pa_cities = ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Scranton", "Bethlehem", "Lancaster", "Harrisburg", "Altoona", "York", "Wilkes-Barre", "Chester", "Williamsport", "Easton", "Lebanon", "Hazleton", "New Castle", "Johnstown", "McKeesport", "Hermitage", "Butler", "Sharon", "Greensburg", "Pottsville", "Washington", "Meadville", "Oil City", "DuBois", "Sunbury"]
    
    pa_data = pd.DataFrame({
        "City": pa_cities,
        "Utilization (%)": np.clip(np.random.normal(utilization_threshold, 5, len(pa_cities)), 50, 100)  # Ensuring values between 50-100%
    })
    
    fig2 = px.bar(pa_data, x="City", y="Utilization (%)", color="Utilization (%)",
                  title=f"{selected_role} & {selected_asset} Utilization by City in Pennsylvania",
                  color_continuous_scale=[(0, "red"), (0.5, "yellow"), (0.75, "green"), (1, "red")])
    st.plotly_chart(fig2, use_container_width=True)
    
    st.dataframe(pa_data.style.background_gradient(cmap="coolwarm"))
