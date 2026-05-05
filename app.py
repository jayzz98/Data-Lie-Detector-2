# -*- coding: utf-8 -*-
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
# PAGE CONFIG & PREMIUM CSS
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Lie Detector",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)




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

    /* ══ HERO HEADER ══ */
    .hero-header {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1040 40%, #0d0d2a 100%);
        border-radius: 20px; padding: 3rem 2.5rem; margin-bottom: 2rem; text-align: center;
        border: 1px solid rgba(123,47,247,0.15);
        box-shadow: 0 8px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
        position: relative; overflow: hidden;
    }
    .hero-header::before {
        content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%;
        background: radial-gradient(circle at 30% 50%, rgba(123,47,247,0.08), transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(0,210,255,0.05), transparent 50%);
        pointer-events:none;
    }
    .hero-header h1 {
        font-size: 2.6rem; font-weight: 900; position:relative;
        background: linear-gradient(135deg, #00d2ff, #7b2ff7 50%, #ff6bcb);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem; letter-spacing:-0.02em;
    }
    .hero-header p { color: rgba(240,240,245,0.5); font-size: 0.95rem; font-weight: 400; position:relative; }

    /* ══ SCORE CARDS ══ */
    .score-card {
        background: rgba(13,13,26,0.8); backdrop-filter: blur(12px);
        border-radius: 18px; padding: 1.6rem 1.2rem; text-align: center;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    }
    .score-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.35);
        border-color: rgba(123,47,247,0.2);
    }
    .score-card .label {
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.5px; color: rgba(255,255,255,0.4); margin-bottom: 0.5rem;
    }
    .score-card .value { font-size: 2.4rem; font-weight: 900; letter-spacing:-0.02em; }
    .score-green { color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.3); }
    .score-yellow { color: #ffab00; text-shadow: 0 0 20px rgba(255,171,0,0.3); }
    .score-red { color: #ff1744; text-shadow: 0 0 20px rgba(255,23,68,0.3); }

    /* ══ SECTION HEADERS ══ */
    .section-header {
        background: linear-gradient(90deg, rgba(123,47,247,0.12), transparent);
        border-left: 3px solid #7b2ff7; padding: 0.7rem 1.2rem;
        border-radius: 0 10px 10px 0; margin: 2rem 0 1rem 0;
        font-weight: 700; font-size: 1.05rem; color: #e8e8f0;
        letter-spacing: 0.01em;
    }

    /* ══ ALERT CARDS ══ */
    .alert-critical {
        background: rgba(255,23,68,0.06); border: 1px solid rgba(255,23,68,0.2);
        border-radius: 12px; padding: 0.9rem 1.3rem; margin: 0.5rem 0;
        color: #ff8a80; font-weight: 500; backdrop-filter: blur(8px);
        border-left: 3px solid #ff1744;
    }
    .alert-warning {
        background: rgba(255,171,0,0.06); border: 1px solid rgba(255,171,0,0.2);
        border-radius: 12px; padding: 0.9rem 1.3rem; margin: 0.5rem 0;
        color: #ffd54f; font-weight: 500; backdrop-filter: blur(8px);
        border-left: 3px solid #ffab00;
    }
    .alert-success {
        background: rgba(0,230,118,0.06); border: 1px solid rgba(0,230,118,0.2);
        border-radius: 12px; padding: 0.9rem 1.3rem; margin: 0.5rem 0;
        color: #69f0ae; font-weight: 500; backdrop-filter: blur(8px);
        border-left: 3px solid #00e676;
    }
    .alert-info {
        background: rgba(100,181,246,0.06); border: 1px solid rgba(100,181,246,0.2);
        border-radius: 12px; padding: 0.9rem 1.3rem; margin: 0.5rem 0;
        color: #90caf9; font-weight: 500; backdrop-filter: blur(8px);
        border-left: 3px solid #64b5f6;
    }

    /* ══ SEVERITY BADGES ══ */
    .severity-badge {
        display: inline-block; padding: 0.2rem 0.7rem; border-radius: 6px;
        font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
        letter-spacing: 1px; margin-right: 0.6rem; vertical-align: middle;
    }
    .sev-critical { background: linear-gradient(135deg,#ff1744,#d50000); color: white; }
    .sev-moderate { background: linear-gradient(135deg,#ffab00,#ff8f00); color: #1a1a2e; }
    .sev-minor { background: linear-gradient(135deg,#64b5f6,#42a5f5); color: #1a1a2e; }

    /* ══ VERDICT BANNER ══ */
    .verdict-banner {
        border-radius: 14px; padding: 1.2rem 1.8rem; margin: 0.8rem 0 1.8rem 0;
        font-weight: 600; font-size: 1rem; text-align: center; letter-spacing: 0.3px;
        backdrop-filter: blur(8px);
    }
    .verdict-safe { background: rgba(0,230,118,0.08); border: 1px solid rgba(0,230,118,0.25); color: #69f0ae; }
    .verdict-caution { background: rgba(255,171,0,0.08); border: 1px solid rgba(255,171,0,0.25); color: #ffd54f; }
    .verdict-warning { background: rgba(255,23,68,0.08); border: 1px solid rgba(255,23,68,0.25); color: #ff8a80; }
    .verdict-danger { background: rgba(255,23,68,0.12); border: 1px solid rgba(255,23,68,0.35); color: #ff1744; }

    /* ══ TRUST DOTS ══ */
    .trust-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; vertical-align:middle; }
    .dot-red { background:#ff1744; box-shadow:0 0 6px rgba(255,23,68,0.5); }
    .dot-yellow { background:#ffab00; box-shadow:0 0 6px rgba(255,171,0,0.5); }
    .dot-green { background:#00e676; box-shadow:0 0 6px rgba(0,230,118,0.5); }

    /* ══ RISK BADGE ══ */
    .risk-badge {
        display:inline-block; padding:0.6rem 2rem; border-radius:50px;
        font-weight:800; font-size:1rem; letter-spacing:0.5px;
    }
    .risk-low { background:linear-gradient(135deg,#00e676,#00c853); color:#0a0a1a; box-shadow:0 4px 15px rgba(0,230,118,0.3); }
    .risk-medium { background:linear-gradient(135deg,#ffab00,#ff8f00); color:#0a0a1a; box-shadow:0 4px 15px rgba(255,171,0,0.3); }
    .risk-high { background:linear-gradient(135deg,#ff1744,#d50000); color:white; box-shadow:0 4px 15px rgba(255,23,68,0.3); }

    /* ══ INSIGHT BOX ══ */
    .insight-box {
        background: rgba(13,13,26,0.9); border: 1px solid rgba(123,47,247,0.2);
        border-radius: 16px; padding: 1.8rem; color: #d0d0e0; line-height: 1.8; font-size: 0.93rem;
        backdrop-filter: blur(12px); box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }

    /* ══ SIDEBAR ══ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08081a 0%, #0d0d24 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.04) !important;
    }
    section[data-testid="stSidebar"] * { color: #c0c0d8 !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #e8e8f0 !important; }
    section[data-testid="stSidebar"] .stButton>button {
        background: rgba(123,47,247,0.1)!important; border:1px solid rgba(123,47,247,0.25)!important;
        border-radius:10px!important; color:#c0b0f0!important; font-weight:600!important;
        transition:all .2s!important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background:rgba(123,47,247,0.2)!important; border-color:rgba(123,47,247,0.4)!important;
        transform:translateY(-1px)!important;
    }

    /* ══ TABS ══ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(13,13,26,0.6); border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px; padding: 4px; gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px; padding: 10px 20px; font-weight: 600;
        font-size: 0.88rem; color: rgba(255,255,255,0.5)!important;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7b2ff7, #5a1fd6)!important;
        color: white!important; box-shadow: 0 4px 15px rgba(123,47,247,0.3);
    }
    .stTabs [data-baseweb="tab"]:hover { color: #e0e0f0!important; }

    /* ══ INPUTS ══ */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(13,13,26,0.8)!important; border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important; color:#e8e8f0!important; padding:12px 16px!important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color:rgba(123,47,247,0.5)!important; box-shadow:0 0 0 3px rgba(123,47,247,0.1)!important;
    }
    .stSelectbox>div>div>div {
        background:rgba(13,13,26,0.8)!important; border:1px solid rgba(255,255,255,0.08)!important;
        border-radius:12px!important; color:#e8e8f0!important;
    }

    /* ══ BUTTONS ══ */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #7b2ff7, #5a1fd6)!important; color:white!important;
        border:none!important; border-radius:12px!important; font-weight:700!important;
        padding:11px 24px!important; box-shadow:0 4px 20px rgba(123,47,247,0.35)!important;
        transition:all .25s!important;
    }
    .stButton>button[kind="primary"]:hover {
        transform:translateY(-2px)!important; box-shadow:0 8px 30px rgba(123,47,247,0.45)!important;
    }
    .stButton>button[kind="secondary"] {
        background:rgba(255,255,255,0.04)!important; color:#c0c0d8!important;
        border:1px solid rgba(255,255,255,0.1)!important; border-radius:12px!important;
        font-weight:600!important; transition:all .2s!important;
    }
    .stButton>button[kind="secondary"]:hover {
        background:rgba(255,255,255,0.08)!important; border-color:rgba(255,255,255,0.18)!important;
    }

    /* ══ DATAFRAME ══ */
    [data-testid="stDataFrame"] { border-radius:14px!important; overflow:hidden!important; border:1px solid rgba(255,255,255,0.06)!important; }

    /* ══ METRICS ══ */
    [data-testid="stMetric"] {
        background:rgba(13,13,26,0.6)!important; border:1px solid rgba(255,255,255,0.06)!important;
        border-radius:16px!important; padding:18px!important;
    }

    /* ══ PROGRESS ══ */
    .stProgress>div>div { background:rgba(255,255,255,0.04)!important; border-radius:999px!important; }
    .stProgress>div>div>div { background:linear-gradient(90deg,#7b2ff7,#00d2ff)!important; border-radius:999px!important; }

    /* ══ FILE UPLOADER ══ */
    [data-testid="stFileUploader"]>section {
        background:rgba(13,13,26,0.6)!important; border:2px dashed rgba(123,47,247,0.2)!important;
        border-radius:16px!important; transition:all .3s!important;
    }
    [data-testid="stFileUploader"]>section:hover { border-color:rgba(123,47,247,0.4)!important; }

    /* ══ DIVIDER ══ */
    hr, [data-testid="stMarkdownDivider"] { border-color:rgba(255,255,255,0.06)!important; }

    /* ══ DOWNLOAD BUTTON ══ */
    .stDownloadButton>button {
        background:rgba(0,230,118,0.1)!important; border:1px solid rgba(0,230,118,0.25)!important;
        color:#69f0ae!important; border-radius:12px!important; font-weight:600!important;
    }
    .stDownloadButton>button:hover {
        background:rgba(0,230,118,0.18)!important; border-color:rgba(0,230,118,0.4)!important;
    }

    /* ══ EXPANDER ══ */
    .streamlit-expanderHeader {
        background:rgba(13,13,26,0.6)!important; border:1px solid rgba(255,255,255,0.06)!important;
        border-radius:12px!important; font-weight:600!important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════
def get_score_color(score):
    """Return CSS class based on score value."""
    if score >= 85:
        return "score-green"
    elif score >= 70:
        return "score-yellow"
    else:
        return "score-red"


def get_risk_class(risk_text):
    """Return CSS class based on risk level."""
    if "Low" in risk_text:
        return "risk-low"
    elif "Medium" in risk_text:
        return "risk-medium"
    else:
        return "risk-high"


def render_score_card(label, value, color_class=""):
    """Render a premium score card."""
    st.markdown(f"""
    <div class="score-card">
        <div class="label">{label}</div>
        <div class="value {color_class}">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section(icon, title):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)


if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "counted_files" not in st.session_state:
    st.session_state.counted_files = set()





# ═══════════════════════════════════════════════════════════════════════
# CAPTURE PLAN PARAMETER (from landing page "Buy Now" links)
# ═══════════════════════════════════════════════════════════════════════
if "plan" in st.query_params:
    st.session_state.pending_plan = st.query_params["plan"]
    st.query_params.clear()
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════
# MAIN APP / PAYWALL
# ═══════════════════════════════════════════════════════════════════════
if not st.session_state.user_email:
    # ── 1. Handle OAuth Callback (user is returning from Google/Microsoft) ──
    if "code" in st.query_params and "state" in st.query_params:
        code = st.query_params["code"]
        state = st.query_params["state"]
        email = None
        if state == "google":
            email = verify_google_code(code)
        elif state == "microsoft":
            email = verify_microsoft_code(code)

        st.query_params.clear()
        if email:
            user = login_user(email)
            st.session_state.user_email = user["email"]
            st.rerun()
        else:
            st.error("Authentication failed. Please try again.")

    # ── 2. Build OAuth URLs ──
    google_url = get_google_login_url()
    microsoft_url = get_microsoft_login_url()

    # If credentials are missing, fall back to a simulated form
    if "login" in st.query_params and not has_oauth_credentials():
        provider = st.query_params["login"].capitalize()
        st.query_params.clear()
        st.session_state.oauth_provider = provider
        st.rerun()

    # Show simulated OAuth form when no real credentials are configured
    if st.session_state.get("oauth_provider") and not has_oauth_credentials():
        provider = st.session_state.oauth_provider
        st.markdown(f"""
<style>
[data-testid="stSidebar"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}
[data-testid="stHeader"] {{ display: none; }}
.oauth-container {{
max-width: 420px; margin: 3rem auto 1rem auto; background: linear-gradient(145deg, #1a1a2e, #0f0c29);
border: 1px solid rgba(123,47,247,0.3); border-radius: 16px; padding: 2.5rem; text-align: center;
}}
</style>
<div class="oauth-container">
<h2 style="color:white; margin-bottom: 1rem;">Sign in with {provider}</h2>
<p style="color:gray; font-size: 0.9rem; margin-bottom: 1rem;">Enter your {provider} credentials to continue.</p>
</div>
""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            oauth_email = st.text_input(f"{provider} Email Address", placeholder="name@example.com")
            oauth_pass = st.text_input("Password", type="password")
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Cancel", use_container_width=True):
                    del st.session_state["oauth_provider"]
                    st.rerun()
            with col_b:
                if st.button("Secure Sign In", type="primary", use_container_width=True):
                    if "@" in oauth_email and len(oauth_pass) > 2:
                        user = login_user(oauth_email)
                        st.session_state.user_email = user["email"]
                        del st.session_state["oauth_provider"]
                        st.rerun()
                    else:
                        st.error("Please enter a valid email and password.")
        st.stop()

    # ── 3. Determine button hrefs ──
    google_href = google_url if google_url else "?login=google"
    microsoft_href = microsoft_url if microsoft_url else "?login=microsoft"

    # ── 4. Full-Page Login UI ──
    home_url = os.environ.get("HOME_URL", "http://localhost:8000/")
    
    css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
[data-testid="stHeader"] { display: none; }
.login-wrapper {
    display: flex; justify-content: center; align-items: center; min-height: 100vh;
    background: #06060f;
    font-family: 'Inter', sans-serif; position: relative; overflow: hidden;
}
.login-wrapper::before {
    content:''; position:absolute; width:100%; height:100%;
    background: radial-gradient(circle at top, rgba(123,47,247,0.1), transparent 70%);
    pointer-events:none;
}
.login-container {
    background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 32px;
    padding: 3.5rem; width: 100%; max-width: 480px; text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); position: relative; z-index: 10;
}
.login-title {
    color: white; font-size: 2.75rem; font-weight: 800; margin-bottom: 1rem;
    letter-spacing: -0.03em; line-height: 1;
}
.login-sub {
    color: rgba(255,255,255,0.5); font-size: 1.1rem; margin-bottom: 2.5rem;
    line-height: 1.6;
}
.oauth-btn {
    display: flex; align-items: center; justify-content: center; gap: 12px;
    width: 100%; padding: 1rem; border-radius: 16px; font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-decoration: none; margin-bottom: 1rem;
    font-size: 1.05rem;
}
.oauth-google {
    background: white; color: #1f2937;
}
.oauth-google:hover {
    background: #f9fafb; transform: translateY(-2px); box-shadow: 0 10px 20px -5px rgba(255,255,255,0.2);
}
.oauth-microsoft {
    background: rgba(255,255,255,0.05); color: #00a4ef; border: 1px solid rgba(255,255,255,0.1);
}
.oauth-microsoft:hover {
    background: rgba(255,255,255,0.08); transform: translateY(-2px); border-color: rgba(0,164,239,0.5);
}
.login-divider {
    display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0;
    color: rgba(255,255,255,0.2); font-size: 0.75rem; font-weight: 600; letter-spacing: 1px;
}
.login-divider::before, .login-divider::after {
    content:''; flex:1; height:1px; background: rgba(255,255,255,0.08);
}
</style>
"""
    
    login_html = """
<div class="login-wrapper">
<div class="login-container">
<a href=\"""" + home_url + """\" target="_top" style="position:absolute; top:20px; left:20px; color:rgba(255,255,255,0.4); text-decoration:none; font-size:0.85rem; font-weight:600; transition:color 0.2s;">← Back to Home</a>
<img src="data:image/png;base64,""" + logo_b64 + """\" style="height: 4.5rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 12px rgba(123,47,247,0.3)); border-radius: 12px;">
<div class="login-title">Welcome Back</div>
<div class="login-sub">Sign in or create an account to start your free trial.<br>No credit card required.</div>
<a href=\"""" + get_google_login_url() + """\" target="_self" class="oauth-btn oauth-google">
<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>
Continue with Google
</a>
<a href=\"""" + get_microsoft_login_url() + """\" target="_self" class="oauth-btn oauth-microsoft">
<svg width="18" height="18" viewBox="0 0 21 21"><rect x="1" y="1" width="9" height="9" fill="#f25022"/><rect x="11" y="1" width="9" height="9" fill="#7fba00"/><rect x="1" y="11" width="9" height="9" fill="#00a4ef"/><rect x="11" y="11" width="9" height="9" fill="#ffb900"/></svg>
Continue with Microsoft
</a>
</div>
</div>
"""
    
    st.markdown(css_code + login_html, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-divider">OR</div>', unsafe_allow_html=True)

        email_input = st.text_input("Email Address", placeholder="name@company.com", label_visibility="collapsed")
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Continue with Email →", type="primary", use_container_width=True):
                if "@" in email_input:
                    user = login_user(email_input)
                    st.session_state.user_email = user["email"]
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
        with c2:
            if st.button("Skip Login (Dev Mode) 🔓", use_container_width=True):
                user = login_user("guest@example.com")
                st.session_state.user_email = user["email"]
                st.rerun()

    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# PAYMENT PAGE (if user clicked "Buy Now" from landing page)
# ═══════════════════════════════════════════════════════════════════════
if st.session_state.get("pending_plan"):
    plan = st.session_state.pending_plan
    plan_names = {"monthly": "1 Month Pro", "semi_annual": "6 Months Pro", "yearly": "1 Year Pro"}
    plan_prices = {"monthly": "$5", "semi_annual": "$29", "yearly": "$49"}
    plan_label = plan_names.get(plan, plan.capitalize())
    plan_price = plan_prices.get(plan, "$0")

    st.markdown(f"""
<div style="max-width: 500px; margin: 2rem auto; background: linear-gradient(145deg, #1a1a2e, #0f0c29); border: 1px solid rgba(123,47,247,0.3); border-radius: 16px; padding: 2.5rem; text-align: center;">
<h2 style="color: white; margin-bottom: 0.5rem;">Complete Your Purchase</h2>
<p style="color: rgba(255,255,255,0.5); margin-bottom: 1.5rem;">You are upgrading to <strong style="color:#7b2ff7;">{plan_label}</strong></p>
<div style="font-size: 3rem; font-weight: 900; color: #00e676; margin-bottom: 0.5rem;">{plan_price}</div>
<p style="color: rgba(255,255,255,0.4); font-size: 0.85rem; margin-bottom: 2rem;">Logged in as: {st.session_state.user_email}</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("**Select Payment Method:**")
        p1, p2 = st.columns(2)
        with p1:
            if st.button("Pay with Card", type="primary", use_container_width=True):
                upgrade_subscription(st.session_state.user_email, plan)
                del st.session_state["pending_plan"]
                st.success(f"Payment successful! You are now on the **{plan_label}** plan.")
                st.balloons()
                import time; time.sleep(2)
                st.rerun()
        with p2:
            if st.button("Pay with UPI", use_container_width=True):
                upgrade_subscription(st.session_state.user_email, plan)
                del st.session_state["pending_plan"]
                st.success(f"Payment successful! You are now on the **{plan_label}** plan.")
                st.balloons()
                import time; time.sleep(2)
                st.rerun()

        if st.button("Cancel", use_container_width=True):
            del st.session_state["pending_plan"]
            st.rerun()

    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
with st.sidebar:
    if st.session_state.user_email:
        st.markdown("### 👤 Account")
        user = get_user(st.session_state.user_email)
        st.markdown(f"**{user['email']}**")
        st.caption(f"Plan: {user['subscription'].upper()}")
        if st.button("Logout"):
            st.session_state.user_email = None
            st.rerun()
        st.divider()

    st.markdown("### ⚙️ Settings")
    st.divider()

    # OpenAI API Key (optional)
    api_key = st.text_input("OpenAI API Key (optional)", type="password",
                            help="Enter your OpenAI API key for AI-powered insights")

    st.divider()
    st.markdown("### 📖 About")
    st.markdown("""
    **Data Lie Detector** analyzes your datasets
    for quality issues, suspicious patterns, and
    decision risks.

    *Upload → Detect → Trust → Decide*
    """)
    st.divider()
    st.caption("v2.0 — Decision Safety AI")


# ═══════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 1.2em; vertical-align: middle; margin-right: 12px;">' if logo_b64 else '🕵️'
st.markdown(f"""
<div class="hero-header">
    <h1>{logo_html} Data Lie Detector</h1>
    <p>Upload data → Detect issues → Score trust → Make safe decisions</p>
</div>
""", unsafe_allow_html=True)

has_access, reason, trial_status = check_access(st.session_state.user_email)

st.markdown(f"""
<div style="text-align:center; margin-bottom:1.5rem;">
    <span style="background:rgba(123,47,247,0.1); border:1px solid rgba(123,47,247,0.2); color:rgba(123,47,247,0.7); padding:0.3rem 1rem; border-radius:50px; font-size:0.75rem; font-weight:600; letter-spacing:0.5px;">{trial_status}</span>
</div>""", unsafe_allow_html=True)

if not has_access:
    # ── PAYWALL UI ──
    st.markdown(f'<div class="alert-critical" style="text-align:center; font-size:1.05rem; padding: 1.2rem; border-radius:14px;">🚨 {reason}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom: 2rem;">
        <div style="font-size:2rem; font-weight:900; color:#f0f0f5; letter-spacing:-0.02em;">Upgrade Your Plan</div>
        <div style="font-size:0.9rem; color:rgba(240,240,245,0.4); margin-top:0.4rem;">Unlock unlimited datasets, AI insights, and PDF reports</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:rgba(13,13,26,0.8); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:2rem 1.5rem; text-align:center; backdrop-filter:blur(12px);">
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:rgba(255,255,255,0.35); margin-bottom:0.8rem;">1 Month</div>
            <div style="font-size:3rem; font-weight:900; color:#f0f0f5; letter-spacing:-0.03em;">$5<span style="font-size:1rem; font-weight:400; color:rgba(255,255,255,0.3);">/mo</span></div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.3); margin-top:0.5rem;">Perfect for trying out</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Buy Monthly", use_container_width=True):
            st.session_state.selected_plan = "monthly"
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(145deg, rgba(123,47,247,0.12), rgba(13,13,26,0.9)); border:1px solid rgba(123,47,247,0.3); border-radius:20px; padding:2rem 1.5rem; text-align:center; backdrop-filter:blur(12px); position:relative; box-shadow:0 8px 40px rgba(123,47,247,0.1);">
            <div style="position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:linear-gradient(135deg,#7b2ff7,#ff6bcb); color:white; padding:3px 16px; border-radius:50px; font-size:0.65rem; font-weight:800; text-transform:uppercase; letter-spacing:1px;">Most Popular</div>
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:rgba(123,47,247,0.7); margin-bottom:0.8rem;">6 Months</div>
            <div style="font-size:3rem; font-weight:900; color:#f0f0f5; letter-spacing:-0.03em;">$29<span style="font-size:1rem; font-weight:400; color:rgba(255,255,255,0.3);">/6mo</span></div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:0.5rem;">Save 52% vs monthly</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Buy 6-Months", type="primary", use_container_width=True):
            st.session_state.selected_plan = "semi_annual"
    with col3:
        st.markdown("""
        <div style="background:rgba(13,13,26,0.8); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:2rem 1.5rem; text-align:center; backdrop-filter:blur(12px);">
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:rgba(255,255,255,0.35); margin-bottom:0.8rem;">1 Year</div>
            <div style="font-size:3rem; font-weight:900; color:#f0f0f5; letter-spacing:-0.03em;">$49<span style="font-size:1rem; font-weight:400; color:rgba(255,255,255,0.3);">/yr</span></div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.3); margin-top:0.5rem;">Best value — $4.08/mo</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Buy Yearly", use_container_width=True):
            st.session_state.selected_plan = "yearly"
            
    if "selected_plan" in st.session_state:
        st.divider()
        st.markdown(f"**Selected Plan:** {st.session_state.selected_plan.upper()}")
        st.markdown("Select Payment Method:")
        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("💳 Pay with Card", use_container_width=True):
                upgrade_subscription(st.session_state.user_email, st.session_state.selected_plan)
                del st.session_state.selected_plan
                st.success("Payment Successful! Upgrading account...")
                import time; time.sleep(1)
                st.rerun()
        with p2:
            if st.button("📱 Pay with UPI", use_container_width=True):
                upgrade_subscription(st.session_state.user_email, st.session_state.selected_plan)
                del st.session_state.selected_plan
                st.success("UPI Payment Successful! Upgrading account...")
                import time; time.sleep(1)
                st.rerun()
        with p3:
            if st.button("🅿️ Pay with PayPal", use_container_width=True):
                upgrade_subscription(st.session_state.user_email, st.session_state.selected_plan)
                del st.session_state.selected_plan
                st.success("PayPal Payment Successful! Upgrading account...")
                import time; time.sleep(1)
                st.rerun()
    st.stop()


# ═══════════════════════════════════════════════════════════════════════
# FILE UPLOAD (Multi-file support)
# ═══════════════════════════════════════════════════════════════════════
files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True,
    help="Upload one or more CSV files for analysis"
)

if files:
    # File selector for multi-file
    if len(files) > 1:
        render_section("📁", "Multi-File Mode")
        file_names = [f.name for f in files]
        selected_file_name = st.selectbox("Select file to analyze", file_names)
        selected_file = files[file_names.index(selected_file_name)]

        # Comparison overview
        with st.expander("📊 Quick Comparison — All Files"):
            comp_cols = st.columns(len(files))
            for i, f in enumerate(files):
                temp_df = load_file(f)
                f.seek(0)  # Reset file pointer
                if temp_df is not None:
                    with comp_cols[i]:
                        st.markdown(f"**{f.name}**")
                        st.caption(f"{temp_df.shape[0]} rows × {temp_df.shape[1]} cols")
                        temp_profile = profile_data(temp_df)
                        temp_anomalies = detect_anomalies(temp_df, temp_profile["numeric_cols"])
                        temp_score = calculate_trust(temp_profile, temp_anomalies, temp_profile["rows"])
                        color = get_score_color(temp_score)
                        st.markdown(f"<span class='{color}' style='font-size:1.4rem;font-weight:700'>{temp_score}</span>",
                                    unsafe_allow_html=True)

        selected_file.seek(0)  # Reset file pointer for main analysis
        
        # Track usage
        if selected_file.name not in st.session_state.counted_files:
            increment_dataset_usage(st.session_state.user_email)
            st.session_state.counted_files.add(selected_file.name)
    else:
        selected_file = files[0]
        if selected_file.name not in st.session_state.counted_files:
            increment_dataset_usage(st.session_state.user_email)
            st.session_state.counted_files.add(selected_file.name)

    df = load_file(selected_file)

    if df is None:
        st.error("❌ Error loading file. Please check the CSV format.")
    else:
        # ═══════════════════════════════════════════════════════════════
        # PHASE 1: DATA PROFILING & BASIC ANALYSIS
        # ═══════════════════════════════════════════════════════════════
        profile = profile_data(df)
        anomalies = detect_anomalies(df, profile["numeric_cols"])
        trust_score = calculate_trust(profile, anomalies, profile["rows"])
        risk_level = decision_risk(trust_score)
        explanation = generate_explanation(trust_score, profile, anomalies)

        # ── TOP METRICS DASHBOARD ──
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_score_card("Trust Score", f"{trust_score}", get_score_color(trust_score))
        with m2:
            render_score_card("Rows", f"{profile['rows']:,}", "")
        with m3:
            render_score_card("Duplicates", f"{profile['duplicates']:,}",
                              "score-red" if profile['duplicates'] > 0 else "score-green")
        with m4:
            risk_class = get_risk_class(risk_level)
            st.markdown(f"""
            <div class="score-card">
                <div class="label">Decision Risk</div>
                <div style="margin-top:0.5rem">
                    <span class="risk-badge {risk_class}">{risk_level}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── DECISION VERDICT (Killer line) ──
        has_severe = any(v > 50 for v in profile["missing"].values())
        verdict_text, verdict_class = generate_decision_verdict(trust_score, has_severe)
        st.markdown(f'<div class="verdict-banner {verdict_class}">{verdict_text}</div>',
                    unsafe_allow_html=True)

        # ── ALERTS (Top priority — severity-classified) ──
        alerts = generate_alerts(trust_score, anomalies, profile)
        if alerts:
            render_section("🔔", "Alerts")
            severity_map = {
                "critical": ("alert-critical", "sev-critical", "🚨"),
                "moderate": ("alert-warning", "sev-moderate", "⚠️"),
                "minor":    ("alert-info", "sev-minor", "ℹ️"),
            }
            for severity, msg in alerts:
                alert_cls, badge_cls, icon = severity_map.get(severity, ("alert-info", "sev-minor", "ℹ️"))
                badge = f'<span class="severity-badge {badge_cls}">{severity}</span>'
                st.markdown(f'<div class="{alert_cls}">{badge} {icon} {msg}</div>',
                            unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # ── TABBED ANALYSIS ──
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", "📉 Anomalies", "🕵️ Lie Detection",
            "🧠 AI Insight", "🔧 Fix & Export", "📡 API & Monitoring"
        ])

        # ─────────────────────────────────────────────────────────
        # TAB 1: OVERVIEW
        # ─────────────────────────────────────────────────────────
        with tab1:
            render_section("👀", "Data Preview")
            st.dataframe(df.head(20), use_container_width=True)

            col_left, col_right = st.columns(2)

            with col_left:
                render_section("🧬", "Column Types")
                st.markdown(f"**Numeric ({len(profile['numeric_cols'])}):** {', '.join(profile['numeric_cols']) or 'None'}")
                st.markdown(f"**Categorical ({len(profile['categorical_cols'])}):** {', '.join(profile['categorical_cols']) or 'None'}")

            with col_right:
                render_section("⚠️", "Missing Values (%)")
                missing_df = pd.DataFrame([
                    {"Column": k, "Missing %": round(v, 2)}
                    for k, v in profile["missing"].items() if v > 0
                ])
                if not missing_df.empty:
                    st.dataframe(missing_df, use_container_width=True, hide_index=True)
                else:
                    st.markdown('<div class="alert-success">✅ No missing values</div>', unsafe_allow_html=True)

            # Column-level trust scores with color indicators
            render_section("📊", "Column Trust Scores")
            col_scores = column_trust_score(df)

            def trust_indicator(score):
                if score >= 80:
                    return "🟢", "dot-green"
                elif score >= 60:
                    return "🟡", "dot-yellow"
                else:
                    return "🔴", "dot-red"

            # Build styled HTML table
            table_rows = ""
            for col, score in sorted(col_scores.items(), key=lambda x: x[1]):
                dot, dot_cls = trust_indicator(score)
                bar_width = max(score, 2)
                bar_color = "#ff1744" if score < 40 else "#ffab00" if score < 70 else "#00e676"
                text_color = '#1a1a2e' if score >= 60 else 'white'
                table_rows += f"""
                <tr>
                    <td style="padding:0.5rem 1rem; color:#e0e0e0; font-weight:500;">
                        <span class="trust-dot {dot_cls}"></span>{col}
                    </td>
                    <td style="padding:0.5rem 1rem; width:50%;">
                        <div style="background:rgba(255,255,255,0.06); border-radius:6px; overflow:hidden; height:22px;">
                            <div style="width:{bar_width}%; height:100%; background:{bar_color}; border-radius:6px; display:flex; align-items:center; padding-left:8px; font-size:0.75rem; font-weight:700; color:{text_color};">
                                {score}
                            </div>
                        </div>
                    </td>
                    <td style="padding:0.5rem; text-align:center; font-size:1.1rem;">{dot}</td>
                </tr>"""

            st.markdown(f"""
            <table style="width:100%; border-collapse:collapse; margin-top:0.5rem;">
                <thead>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
                        <th style="padding:0.6rem 1rem; text-align:left; color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Column</th>
                        <th style="padding:0.6rem 1rem; text-align:left; color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Trust Score</th>
                        <th style="padding:0.6rem; text-align:center; color:rgba(255,255,255,0.5); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Status</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

        # ─────────────────────────────────────────────────────────
        # TAB 2: ANOMALIES
        # ─────────────────────────────────────────────────────────
        with tab2:
            render_section("📉", "Statistical Anomalies (Z-Score)")
            anomaly_df = pd.DataFrame([
                {"Column": k, "Outlier Count": v} for k, v in anomalies.items()
            ])
            if not anomaly_df.empty:
                st.dataframe(anomaly_df, use_container_width=True, hide_index=True)
            else:
                st.markdown('<div class="alert-success">✅ No numeric columns to analyze</div>',
                            unsafe_allow_html=True)

            # Root Cause Analysis
            render_section("🔍", "Root Cause Analysis")
            causes = find_root_causes(df, anomalies)
            if causes:
                for c in causes:
                    st.markdown(f'<div class="alert-warning">{c}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-success">✅ No major root causes detected</div>',
                            unsafe_allow_html=True)

            # Time-Series Analysis
            render_section("📅", "Time Series Analysis")
            date_cols = df.select_dtypes(include=['object']).columns.tolist()

            if len(date_cols) > 0 and len(profile["numeric_cols"]) > 0:
                ts_col1, ts_col2 = st.columns(2)
                with ts_col1:
                    date_col = st.selectbox("Select Date Column", date_cols, key="ts_date")
                with ts_col2:
                    value_col = st.selectbox("Select Value Column", profile["numeric_cols"], key="ts_value")

                from utils.timeseries import detect_timeseries_anomalies

                ts_df = detect_timeseries_anomalies(df, date_col, value_col)
                st.line_chart(ts_df[[value_col]])

                ts_anomaly_count = ts_df["anomaly"].sum()
                if ts_anomaly_count > 0:
                    st.markdown(f'<div class="alert-warning">⚠️ {ts_anomaly_count} time-series anomalies detected</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-success">✅ No time-series anomalies</div>',
                                unsafe_allow_html=True)
            else:
                st.info("No date + numeric column pair available for time-series analysis.")

        # ─────────────────────────────────────────────────────────
        # TAB 3: LIE DETECTION (Suspicious Patterns)
        # ─────────────────────────────────────────────────────────
        with tab3:
            render_section("🕵️", "Suspicious Pattern Detection")
            suspicious = detect_suspicious_patterns(df, profile["numeric_cols"])

            if suspicious:
                for s in suspicious:
                    st.markdown(f'<div class="alert-critical">🚩 {s}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-success">✅ No obvious manipulation patterns detected</div>',
                            unsafe_allow_html=True)

            st.divider()

            render_section("🧠", "Rule-Based Explanation")
            st.markdown(f'<div class="insight-box">{explanation}</div>', unsafe_allow_html=True)

        # ─────────────────────────────────────────────────────────
        # TAB 4: AI INSIGHT
        # ─────────────────────────────────────────────────────────
        with tab4:
            render_section("🧠", "AI-Powered Insight")

            if st.button("🚀 Generate AI Insight", use_container_width=True):
                from utils.ai_explain import ai_explain
                with st.spinner("Analyzing with AI..."):
                    insight = ai_explain(profile, anomalies, trust_score, api_key=api_key or None)
                st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("Click the button above to generate an AI-powered analysis. Requires an OpenAI API key in the sidebar.")

        # ─────────────────────────────────────────────────────────
        # TAB 5: FIX & EXPORT
        # ─────────────────────────────────────────────────────────
        with tab5:
            render_section("🔄", "Suggested Fixes")
            fixes = suggest_fixes(profile, anomalies)

            if fixes:
                for f in fixes:
                    st.markdown(f'<div class="alert-warning">{f}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ Auto-Fix Data", use_container_width=True):
                    with st.spinner("Applying automated fixes..."):
                        fixed_df, fix_log = auto_fix_data(df, profile, anomalies)
                        
                        for log_entry in fix_log:
                            if "✅" in log_entry:
                                st.markdown(f'<div class="alert-success">{log_entry}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="alert-info">{log_entry}</div>', unsafe_allow_html=True)
                        
                        csv = fixed_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Download Cleaned Data (CSV)",
                            data=csv,
                            file_name=f"cleaned_{selected_file.name}",
                            mime="text/csv",
                            use_container_width=True
                        )
            else:
                st.markdown('<div class="alert-success">✅ No fixes needed — data looks good!</div>',
                            unsafe_allow_html=True)

            st.divider()

            render_section("📄", "Export Report")

            if st.button("📄 Generate PDF Report", use_container_width=True):
                pdf_bytes = generate_report(
                    trust_score, explanation,
                    profile=profile, anomalies=anomalies, risk_level=risk_level
                )
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download Report PDF",
                        data=pdf_bytes,
                        file_name="data_lie_detector_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("Report generated! Click download above.")
                else:
                    st.warning("ReportLab not installed. Run: `pip install reportlab`")

        # ─────────────────────────────────────────────────────────
        # TAB 6: API & MONITORING
        # ─────────────────────────────────────────────────────────
        with tab6:
            render_section("📡", "API Access")
            st.markdown("""
            Integrate Data Lie Detector directly into your pipelines using our REST API.
            
            **Start the server:**
            ```bash
            uvicorn utils.api_server:app --reload --port 8000
            ```
            
            **Example Request:**
            ```python
            import requests
            
            with open("data.csv", "rb") as f:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={"file": f}
                )
                
            print(response.json()["trust_score"])
            ```
            """)
            
            st.divider()
            
            render_section("📈", "Real-Time Monitoring")
            st.markdown("""
            <div class="insight-box" style="text-align: center;">
                <h3 style="margin-bottom: 1rem;">Coming Soon in Enterprise</h3>
                <p>Connect live data streams (Kafka, PostgreSQL, Snowflake) for continuous monitoring.</p>
                <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem;">
                    <div style="background: rgba(0,230,118,0.1); padding: 1rem; border-radius: 8px; border: 1px solid rgba(0,230,118,0.3);">
                        <div style="font-size: 2rem; color: #00e676; font-weight: 800;">1.2M</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">Rows Monitored Today</div>
                    </div>
                    <div style="background: rgba(255,23,68,0.1); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,23,68,0.3);">
                        <div style="font-size: 2rem; color: #ff1744; font-weight: 800;">43</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">Anomalies Caught</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ── EMPTY STATE ──
    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem; position:relative;">
        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:300px; height:300px; background:radial-gradient(circle, rgba(123,47,247,0.06), transparent 70%); pointer-events:none;"></div>
        <div style="font-size:4rem; margin-bottom:1rem; filter:drop-shadow(0 4px 12px rgba(123,47,247,0.2)); position:relative;">📁</div>
        <div style="font-size:1.3rem; font-weight:800; color:#e0e0f0; margin-bottom:0.6rem; position:relative;">Drop your CSV file above</div>
        <div style="font-size:0.88rem; color:rgba(240,240,245,0.35); max-width:400px; margin:0 auto; line-height:1.6; position:relative;">Your data stays 100% local — nothing is sent to any server unless you explicitly use AI Insight.</div>
    </div>
    """, unsafe_allow_html=True)
