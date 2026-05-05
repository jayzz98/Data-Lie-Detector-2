import streamlit as st
import pandas as pd

import base64
import os

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

logo_b64 = get_base64_image("assets/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 1.2em; vertical-align: middle; margin-right: 12px;">' if logo_b64 else '🕵️'

st.markdown(f"<h1>{logo_html} Data Lie Detector</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='latin1')
        
        st.write("### 👀 Data Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")