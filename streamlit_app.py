# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import base64
import os
import time
import urllib.parse

# ═══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════
# ASSET HELPERS
# ═══════════════════════════════════════════════════════════════════════
@st.cache_data
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

logo_b64 = get_base64_image("assets/logo.png")

# ═══════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════
from utils.loader import load_file
from utils.profiler import profile_data
from utils.anomaly import detect_anomalies
from utils.trust import calculate_trust
from utils.explain import generate_explanation, generate_decision_verdict
from utils.suspicious import detect_suspicious_patterns
from utils.column_trust import column_trust_score
from utils.root_cause import find_root_causes
from utils.risk import decision_risk
from utils.fixer import suggest_fixes
from utils.alerts import generate_alerts
from utils.report import generate_report
from utils.auto_fix import auto_fix_data
from utils.auth import (
    login_user, check_access, increment_dataset_usage, upgrade_subscription, get_user,
    get_google_login_url, get_microsoft_login_url,
    verify_google_code, verify_microsoft_code, has_oauth_credentials,
)

# ═══════════════════════════════════════════════════════════════════════
# LANDING PAGE RENDERER
# ═══════════════════════════════════════════════════════════════════════
def show_landing_page():
    """Renders the professional landing page."""
    
    # Read HTML and CSS
    with open("landing/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    with open("landing/style.css", "r", encoding="utf-8") as f:
        css_content = f.read()

    # Inject Logo Base64
    html_content = html_content.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')
    
    # Update Links to work within Streamlit
    # Streamlit query params can be used to trigger the app
    html_content = html_content.replace('href="/app"', 'href="?view=app"')
    html_content = html_content.replace('href="/app?plan=monthly"', 'href="?view=app&plan=monthly"')
    html_content = html_content.replace('href="/app?plan=semi_annual"', 'href="?view=app&plan=semi_annual"')
    html_content = html_content.replace('href="/app?plan=yearly"', 'href="?view=app&plan=yearly"')

    # Build the full component
    full_html = f"""
    <style>
    /* Hide Streamlit elements on landing page */
    #MainMenu, footer, header, [data-testid="stToolbar"] {{ visibility:hidden!important; height:0!important; }}
    .stDeployButton {{ display:none!important; }}
    [data-testid="stSidebar"] {{ display:none!important; }}
    [data-testid="stHeader"] {{ background:transparent!important; }}
    .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    
    {css_content}
    </style>
    {html_content}
    """
    
    st.markdown(full_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# DASHBOARD STYLES
# ═══════════════════════════════════════════════════════════════════════
def apply_dashboard_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ══ GLOBAL ══ */
    .stApp { font-family: 'Inter', -apple-system, sans-serif; }
    html, body, .stApp { background: #06060f !important; }
    #MainMenu, footer, header, [data-testid="stToolbar"] { visibility:hidden!important; height:0!important; }
    .stDeployButton { display:none!important; }
    [data-testid="stHeader"] { background:transparent!important; }
    ::-webkit-scrollbar { width:5px; }
    ::-webkit-scrollbar-track { background:transparent; }
    ::-webkit-scrollbar-thumb { background:rgba(123,47,247,0.3); border-radius:10px; }
    .main .block-container { padding-top: 0.5rem !important; }

    /* ══ HERO HEADER ══ */
    .hero-header {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1040 40%, #0d0d2a 100%);
        border-radius: 20px; padding: 0.2rem 1.5rem; margin-bottom: 0.5rem; text-align: center;
        border: 1px solid rgba(123,47,247,0.15); margin-top: -4rem !important;
        box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
        position: relative; overflow: hidden;
    }
    .hero-header h1 {
        font-size: 3.5rem; font-weight: 900; position:relative;
        color: #ffffff !important;
        margin-bottom: 0.2rem; letter-spacing:-0.02em;
    }
    .hero-header p { color: rgba(240,240,245,0.5); font-size: 0.85rem; font-weight: 400; position:relative; }

    /* ══ SCORE CARDS ══ */
    .score-card {
        background: rgba(13,13,26,0.8); backdrop-filter: blur(12px);
        border-radius: 18px; padding: 1.6rem 1.2rem; text-align: center;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    }
    .score-card .value { font-size: 2.4rem; font-weight: 900; letter-spacing:-0.02em; }
    .score-green { color: #00e676; }
    .score-yellow { color: #ffab00; }
    .score-red { color: #ff1744; }

    /* ══ SECTION HEADERS ══ */
    .section-header {
        background: linear-gradient(90deg, rgba(123,47,247,0.12), transparent);
        border-left: 3px solid #7b2ff7; padding: 0.7rem 1.2rem;
        border-radius: 0 10px 10px 0; margin: 2rem 0 1rem 0;
        font-weight: 700; font-size: 1.05rem; color: #e8e8f0;
    }

    /* ══ ALERT CARDS ══ */
    .alert-critical { background: rgba(255,23,68,0.06); border: 1px solid rgba(255,23,68,0.2); border-left: 3px solid #ff1744; padding: 0.9rem; margin: 0.5rem 0; color: #ff8a80; border-radius: 12px; }
    .alert-warning { background: rgba(255,171,0,0.06); border: 1px solid rgba(255,171,0,0.25); border-left: 3px solid #ffab00; padding: 0.9rem; margin: 0.5rem 0; color: #ffd54f; border-radius: 12px; }
    .alert-info { background: rgba(100,181,246,0.06); border: 1px solid rgba(100,181,246,0.2); border-left: 3px solid #64b5f6; padding: 0.9rem; margin: 0.5rem 0; color: #90caf9; border-radius: 12px; }

    /* ══ BUTTONS ══ */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #7b2ff7, #5a1fd6)!important; color:white!important;
        border:none!important; border-radius:12px!important; font-weight:700!important;
        padding:11px 24px!important; box-shadow:0 4px 20px rgba(123,47,247,0.35)!important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# MAIN LOGIC
# ═══════════════════════════════════════════════════════════════════════

# Initializing Session States
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# 1. Handle Navigation and Query Params
params = st.query_params
view = params.get("view", "landing")

# Handle Plan Selection
if "plan" in params:
    st.session_state.pending_plan = params["plan"]
    # Clear the plan param to prevent loops but keep view=app if needed
    st.query_params.update({"view": "app"})

# 2. Handle OAuth Callback
if "code" in params and "state" in params:
    code = params["code"]
    state = params["state"]
    email = None
    if state == "google":
        email = verify_google_code(code)
    elif state == "microsoft":
        email = verify_microsoft_code(code)
    
    if email:
        user = login_user(email)
        st.session_state.user_email = user["email"]
        st.query_params.clear()
        st.query_params.update({"view": "app"})
        st.rerun()

# 3. ROUTING
if st.session_state.user_email:
    # --- LOGGED IN: DASHBOARD ---
    apply_dashboard_styles()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Account")
        user = get_user(st.session_state.user_email)
        st.markdown(f"**{user['email']}**")
        st.caption(f"Plan: {user['subscription'].upper()}")
        if st.button("Logout"):
            st.session_state.user_email = None
            st.query_params.clear()
            st.rerun()
        st.divider()
        st.markdown("### 📖 About")
        st.caption("Data Lie Detector v2.0")

    # Main Dashboard Logic (Simplified for brevity, but you can paste the rest of app.py here)
    # [Rest of app.py logic starting from File Upload goes here]
    
    # HERO HEADER
    st.markdown(f"""
    <div class="hero-header">
        <h1>🕵️ Data Lie Detector</h1>
        <p>Dashboard — Analyzing {st.session_state.user_email}</p>
    </div>
    """, unsafe_allow_html=True)

    # File Uploader
    files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    if files:
        st.success(f"Loaded {len(files)} files. Analysis engine starting...")
        # ... rest of your analysis logic ...

elif view == "app":
    # --- NOT LOGGED IN: LOGIN SCREEN ---
    apply_dashboard_styles()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
            <img src="data:image/png;base64,{logo_b64}" style="height: 4rem; margin-bottom: 1rem;">
            <h2 style="color: white;">Welcome Back</h2>
            <p style="color: gray;">Sign in to analyze your data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        google_url = get_google_login_url()
        if google_url:
            st.link_button("Continue with Google", google_url, type="primary", use_container_width=True)
        
        # Guest Login for testing
        if st.button("Continue as Guest (Demo)", use_container_width=True):
            user = login_user(f"guest_{int(time.time())}@demo.com")
            st.session_state.user_email = user["email"]
            st.rerun()
        
        if st.button("← Back to Home"):
            st.query_params.clear()
            st.rerun()

else:
    # --- DEFAULT: LANDING PAGE ---
    show_landing_page()
