import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# Set up Streamlit page
st.set_page_config(page_title="AI Workforce Scheduler", layout="wide")

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
    st.sidebar.image(logo_path, width=100)  # Explicitly set width to avoid use_container_width issue
else:
    st.sidebar.warning("⚠️ Logo file not found. Please check the path.")

st.title("AI-Powered Workforce Scheduling Tool")
st.write("Optimizing workforce scheduling with machine learning for better efficiency and resource allocation.")

# Simulated scheduling data
data = {
    'experience_level': np.random.choice(['Beginner', 'Intermediate', 'Advanced'], 100),
    'weather_conditions': np.random.choice(['Clear', 'Rain', 'Fog', 'Snow'], 100),
    'job_complexity': np.random.choice(['Low', 'Medium', 'High'], 100),
    'historical_availability': np.random.randint(0, 2, 100),
    'assigned_shift': np.random.choice(['Morning', 'Afternoon', 'Night'], 100)
}

# Encode categorical data
df = pd.DataFrame(data)
df_encoded = pd.get_dummies(df, columns=['experience_level', 'weather_conditions', 'job_complexity'])
X = df_encoded.drop(columns=['assigned_shift'])
y = df['assigned_shift']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Display workforce distribution
st.markdown("### 📊 Workforce Distribution")
fig = px.histogram(df, x='assigned_shift', color='experience_level', 
                   title="Shift Distribution by Experience Level", 
                   barmode='group')
st.plotly_chart(fig, use_container_width=True)

# Streamlit UI Controls
st.markdown("### 🛠 Workforce Scheduling Assistant")
experience_level = st.selectbox("Experience Level", ['Beginner', 'Intermediate', 'Advanced'])
weather_conditions = st.selectbox("Weather Conditions", ['Clear', 'Rain', 'Fog', 'Snow'])
job_complexity = st.selectbox("Job Complexity", ['Low', 'Medium', 'High'])
historical_availability = st.checkbox("Historically Available for This Time Slot?")

# Prepare input for prediction
input_data = pd.DataFrame([[experience_level, weather_conditions, job_complexity, int(historical_availability)]], 
                           columns=['experience_level', 'weather_conditions', 'job_complexity', 'historical_availability'])
input_encoded = pd.get_dummies(input_data)
input_encoded = input_encoded.reindex(columns=X.columns, fill_value=0)

# Predict shift assignment
if st.button("Recommend Shift"):
    predicted_shift = model.predict(input_encoded)[0]
    st.success(f"✅ Recommended Shift: {predicted_shift}")

st.markdown("---")
st.markdown("### 📌 AI & Business Benefits")
st.write("""
- ✅ **Optimized workforce allocation** using AI-based scheduling.
- ⚙️ **Minimizes scheduling conflicts**, reducing inefficiencies.
- 📊 **Predictive insights** for better labor cost management.
- 📈 **Real-time visualization of workforce data** to support decisions.

**AI Techniques Used:**
- **Machine Learning (Random Forest)**: Predicts the best shift based on historical trends.
- **Data Encoding & Feature Engineering**: Converts qualitative data into a format suitable for ML models.
- **Visualization & Analytics**: Provides interactive insights into scheduling efficiency.
""")

st.write(f"Model Accuracy: {accuracy:.2f}")