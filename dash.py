import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_business_value(executions_per_day, value_per_execution, days=20):
    return executions_per_day * value_per_execution * days

# Page Configuration
st.set_page_config(layout="wide", page_title="AWP Executive Dashboard")

# Custom CSS for structured box layout
st.markdown("""
    <style>
        .black-box {
            border: 2px solid black;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
            background-color: white;
            text-align: center;
            width: 100%;
        }
        .container-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border: 2px solid black;
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            background-color: white;
            width: 100%;
        }
        .stMetric label { font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

# Header with Logo
st.image("awp_logo.jpg", width=100)

# Tabs for separating input values and dashboard
tab1, tab2 = st.tabs(["Dashboard", "Adjust Business Impact Values"])

with tab2:
    st.subheader("Modify Business Impact Values")
    col1, col2 = st.columns(2)
    
    with col1:
        scheduler_executions = st.number_input("Executions per Day (Scheduler)", min_value=0, value=10)
        scheduler_value_per_execution = st.number_input("Business Value per Execution ($) (Scheduler)", min_value=0.0, value=200.0)
        scheduler_total_value = calculate_business_value(scheduler_executions, scheduler_value_per_execution)
        
        mutcd_executions = st.number_input("Executions per Day (MUTCD Compliance)", min_value=0, value=3500)
        mutcd_value_per_execution = st.number_input("Business Value per Execution ($) (MUTCD Compliance)", min_value=0.0, value=1.0)
        mutcd_total_value = calculate_business_value(mutcd_executions, mutcd_value_per_execution)
    
    with col2:
        heatmap_monthly_value = st.number_input("Monthly Business Value from Heatmap ($)", min_value=0.0, value=20000.0)
        forecaster_monthly_value = st.number_input("Monthly Business Value from Forecaster ($)", min_value=0.0, value=20000.0)

# Total Business Value Calculation
total_value = scheduler_total_value + mutcd_total_value + heatmap_monthly_value + forecaster_monthly_value

with tab1:
    # Layout setup
    left_col, main_col = st.columns([1, 3])
    
    # Total Business Impact and KPI Summary
    with left_col:
        with st.container():
            st.markdown('<div class="container-box">', unsafe_allow_html=True)
            st.subheader("Total Business Impact")
            st.metric(label="Total Business Value for March ($)", value=f"${total_value:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("Impact by Application")
        for label, value, kpi, runs in zip(
            ["Scheduler", "MUTCD Compliance", "Heatmap", "Forecaster"],
            [scheduler_total_value, mutcd_total_value, heatmap_monthly_value, forecaster_monthly_value],
            ["Project Completion, Resource Utilization", "Regulatory Compliance, Audit Findings",
            "Incident Rate, Corrective Actions Taken", "Revenue Growth, Client Feedback Scores"],
            [scheduler_executions, mutcd_executions, "N/A", "N/A"]):
            
            with st.container():
                st.markdown('<div class="container-box">', unsafe_allow_html=True)
                st.subheader(label)
                st.metric(label="Business Value ($)", value=f"${value:,.2f}", help=f"{kpi}\nRuns per day: {runs}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Column - Application Visuals
    with main_col:
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.markdown('<div class="container-box">', unsafe_allow_html=True)
                st.image("heatmap_visual.png")
                st.caption("Heatmap - Safety Risk Distribution")
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            with st.container():
                st.markdown('<div class="container-box">', unsafe_allow_html=True)
                st.image("forecaster_visual.png")
                st.caption("AI-Based Forecasting - Workforce Demand")
                st.markdown('</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
            with st.container():
                st.markdown('<div class="container-box">', unsafe_allow_html=True)
                st.image("scheduler_visual.png")
                st.caption("Scheduler - Worker & Equipment Utilization")
                st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            with st.container():
                st.markdown('<div class="container-box">', unsafe_allow_html=True)
                days = [f"Day {i+1}" for i in range(20)]
                mutcd_values = [mutcd_executions for _ in range(20)]
                mutcd_df = pd.DataFrame({"Day": days, "MUTCD Checks": mutcd_values})
                fig = px.bar(mutcd_df, x="Day", y="MUTCD Checks")
                st.plotly_chart(fig)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Updated Total Business Value
    with st.container():
        st.markdown('<div class="container-box">', unsafe_allow_html=True)
        st.metric(label="Updated Total Business Value for March ($)", value=f"${total_value:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
