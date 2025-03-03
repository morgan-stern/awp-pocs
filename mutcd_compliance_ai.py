import base64
import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import os
import requests

# Set up Streamlit page
st.set_page_config(page_title="MUTCD Compliance Checker", layout="wide")

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

# Add API key inputs to the sidebar
st.sidebar.header("API Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
telegram_bot_token = st.sidebar.text_input("Telegram Bot Token", type="password")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID")

# Save API keys to session state
if openai_api_key:
    st.session_state['openai_api_key'] = openai_api_key
if telegram_bot_token:
    st.session_state['telegram_bot_token'] = telegram_bot_token
if telegram_chat_id:
    st.session_state['telegram_chat_id'] = telegram_chat_id

st.title("AI-Enhanced MUTCD Compliance Checker")
st.write("""
### Overview
This tool uses **AI-powered image analysis** to determine compliance with **MUTCD safety regulations** for flaggers.

**AI Techniques Used:**
- **GPT-4 Vision AI**: Identifies helmets, safety vests, and stop paddles in uploaded images.
- **Natural Language Processing (NLP)**: Interprets compliance status and extracts missing PPE elements.

**Business Impact:**
- **Enhances workplace safety** by automating PPE checks.
- **Ensures regulatory compliance** to reduce legal risks.
- **Speeds up safety audits**, reducing manual inspections.
""")

# Function to encode image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to send image to OpenAI GPT-4 Vision API
def process_image(image, api_key):
    base64_image = encode_image(image)
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Does this person have a helmet, safety vest, and a stop paddle? Answer with either 'Yes' or 'No' and list any missing items if applicable."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ],
        )
        return response.dict()  # Ensure the response is returned as a dictionary
    except Exception as e:
        return {"error": str(e)}

# Function to send message to Telegram
def send_to_telegram(bot_token, chat_id, message, image=None):
    try:
        if image:
            # Send image with caption
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            files = {'photo': ('image.jpg', image, 'image/jpeg')}
            data = {'chat_id': chat_id, 'caption': message}
            response = requests.post(url, files=files, data=data)
        else:
            # Send text message only
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message}
            response = requests.post(url, json=data)
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# File uploader to allow users to submit images
uploaded_file = st.file_uploader("Upload an image of the flagger", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Check if OpenAI API key is provided
    if not openai_api_key:
        st.error("❌ Please enter your OpenAI API key in the sidebar.")
        st.stop()
    
    # Load the uploaded image and ensure it's in RGB mode
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)
    
    # Process the image through GPT-4 Vision API
    result = process_image(img, openai_api_key)
    
    # Extract response and display it
    if "choices" in result:
        compliance_status = result["choices"][0]["message"]["content"]
        st.write(f"Detected Compliance Status: {compliance_status}")
        
        # Determine compliance based on the response
        is_compliant = "yes" in compliance_status.lower()
        
        # Identify missing items
        missing_items = []
        for item in ["helmet", "safety vest", "stop paddle"]:
            if item in compliance_status.lower() and "no" in compliance_status.lower():
                missing_items.append(item.title())
        
        # Display compliance status
        if is_compliant:
            st.success("✅ Compliance Met! PPE detected.")
            compliance_message = "✅ Compliance Met! All required PPE detected."
        else:
            if missing_items:
                st.warning(f"⚠️ Compliance Violation Detected! Missing: {', '.join(missing_items)}")
                compliance_message = f"⚠️ Compliance Violation Detected! Missing: {', '.join(missing_items)}"
            else:
                st.warning("⚠️ Compliance Violation Detected! No PPE detected.")
                compliance_message = "⚠️ Compliance Violation Detected! No PPE detected."
        
        # Add button to send to Telegram
        if telegram_bot_token and telegram_chat_id:
            if st.button("Send Compliance Report to Telegram"):
                # Prepare image for sending
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                image_bytes = buffered.getvalue()
                
                # Send to Telegram
                telegram_response = send_to_telegram(
                    telegram_bot_token, 
                    telegram_chat_id, 
                    f"MUTCD Compliance Report:\n{compliance_message}\n\nFull Analysis: {compliance_status}",
                    image_bytes
                )
                
                if telegram_response.get("ok"):
                    st.success("✅ Report sent to Telegram successfully!")
                else:
                    st.error(f"❌ Failed to send to Telegram: {telegram_response.get('description', 'Unknown error')}")
        else:
            st.info("ℹ️ To send reports to Telegram, please enter your Telegram Bot Token and Chat ID in the sidebar.")
    else:
        st.error("❌ Error: Unable to process image. Check API response.")
        st.write(result.get("error", "No error details available."))
