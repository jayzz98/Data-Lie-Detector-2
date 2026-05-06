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
try:
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
except ImportError as e:
    st.error(f"Missing utility files: {e}. Please ensure the 'utils' folder is present.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS (From Dashboard)
# ═══════════════════════════════════════════════════════════════════════
def get_score_color(score):
    if score >= 85: return "score-green"
    elif score >= 70: return "score-yellow"
    else: return "score-red"

def get_risk_class(risk_text):
    if "Low" in risk_text: return "risk-low"
    elif "Medium" in risk_text: return "risk-medium"
    else: return "risk-high"

def render_score_card(label, value, color_class=""):
    st.markdown(f"""
    <div class="score-card">
        <div class="label">{label}</div>
        <div class="value {color_class}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_section(icon, title):
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# LANDING PAGE RENDERER
# ═══════════════════════════════════════════════════════════════════════
def show_landing_page():
    """Renders the professional landing page."""
    
    # Read HTML and CSS
    try:
        with open("landing/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        with open("landing/style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
    except FileNotFoundError:
        st.error("Landing page files not found. Ensure 'landing/' directory is present.")
        return

    # Inject Logo Base64
    html_content = html_content.replace('src="logo.png"', f'src="data:image/png;base64,{logo_b64}"')
    
    # Update Links to work within Streamlit
    html_content = html_content.replace('href="/app"', 'href="?view=app"')
    html_content = html_content.replace('href="/app?plan=monthly"', 'href="?view=app&plan=monthly"')
    html_content = html_content.replace('href="/app?plan=semi_annual"', 'href="?view=app&plan=semi_annual"')
    html_content = html_content.replace('href="/app?plan=yearly"', 'href="?view=app&plan=yearly"')

    # Build the full component
    full_html = f"""
    <style>
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
    .hero-header h1 { font-size: 3.5rem; font-weight: 900; position:relative; color: #ffffff !important; margin-bottom: 0.2rem; letter-spacing:-0.02em; }
    .hero-header p { color: rgba(240,240,245,0.5); font-size: 0.85rem; font-weight: 400; position:relative; }

    /* ══ SCORE CARDS ══ */
    .score-card {
        background: rgba(13,13,26,0.8); backdrop-filter: blur(12px); border-radius: 18px; padding: 1.6rem 1.2rem; text-align: center;
        border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    }
    .score-card .label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,0.4); margin-bottom: 0.5rem; }
    .score-card .value { font-size: 2.4rem; font-weight: 900; letter-spacing:-0.02em; }
    .score-green { color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.3); }
    .score-yellow { color: #ffab00; text-shadow: 0 0 20px rgba(255,171,0,0.3); }
    .score-red { color: #ff1744; text-shadow: 0 0 20px rgba(255,23,68,0.3); }

    /* ══ SECTION HEADERS ══ */
    .section-header {
        background: linear-gradient(90deg, rgba(123,47,247,0.12), transparent);
        border-left: 3px solid #7b2ff7; padding: 0.7rem 1.2rem; border-radius: 0 10px 10px 0; margin: 2rem 0 1rem 0;
        font-weight: 700; font-size: 1.05rem; color: #e8e8f0;
    }

    /* ══ ALERT CARDS ══ */
    .alert-critical { background: rgba(255,23,68,0.06); border: 1px solid rgba(255,23,68,0.2); border-left: 3px solid #ff1744; padding: 0.9rem; margin: 0.5rem 0; color: #ff8a80; border-radius: 12px; }
    .alert-warning { background: rgba(255,171,0,0.06); border: 1px solid rgba(255,171,0,0.25); border-left: 3px solid #ffab00; padding: 0.9rem; margin: 0.5rem 0; color: #ffd54f; border-radius: 12px; }
    .alert-info { background: rgba(100,181,246,0.06); border: 1px solid rgba(100,181,246,0.2); border-left: 3px solid #64b5f6; padding: 0.9rem; margin: 0.5rem 0; color: #90caf9; border-radius: 12px; }

    /* ══ RISK BADGES ══ */
    .risk-badge { display:inline-block; padding:0.6rem 2rem; border-radius:50px; font-weight:800; font-size:1rem; }
    .risk-low { background:linear-gradient(135deg,#00e676,#00c853); color:#0a0a1a; }
    .risk-medium { background:linear-gradient(135deg,#ffab00,#ff8f00); color:#0a0a1a; }
    .risk-high { background:linear-gradient(135deg,#ff1744,#d50000); color:white; }

    /* ══ BUTTONS ══ */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #7b2ff7, #5a1fd6)!important; color:white!important;
        border:none!important; border-radius:12px!important; font-weight:700!important;
        padding:11px 24px!important; box-shadow:0 4px 20px rgba(123,47,247,0.35)!important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7b2ff7, #5a1fd6)!important;
        color: white!important; box-shadow: 0 4px 15px rgba(123,47,247,0.3);
    }
    .insight-box { background: rgba(13,13,26,0.9); border: 1px solid rgba(123,47,247,0.2); border-radius: 16px; padding: 1.8rem; color: #d0d0e0; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# ROUTING & SESSION
# ═══════════════════════════════════════════════════════════════════════
if "user_email" not in st.session_state: st.session_state.user_email = None
if "counted_files" not in st.session_state: st.session_state.counted_files = set()

params = st.query_params
view = params.get("view", "landing")

# Handle Plan Callback
if "plan" in params:
    st.session_state.pending_plan = params["plan"]
    st.query_params.update({"view": "app"})

# Handle OAuth Callback
if "code" in params and "state" in params:
    code, state = params["code"], params["state"]
    email = verify_google_code(code) if state == "google" else verify_microsoft_code(code)
    if email:
        user = login_user(email)
        st.session_state.user_email = user["email"]
        st.query_params.clear()
        st.query_params.update({"view": "app"})
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════
# EXECUTION
# ═══════════════════════════════════════════════════════════════════════
if st.session_state.user_email:
    # --- LOGGED IN: DASHBOARD ---
    apply_dashboard_styles()
    
    # Handle Pending Purchase
    if st.session_state.get("pending_plan"):
        plan = st.session_state.pending_plan
        st.markdown(f'<div class="insight-box" style="text-align:center;"><h2>Upgrading to {plan.upper()}</h2><p>Logged in as {st.session_state.user_email}</p></div>', unsafe_allow_html=True)
        if st.button("Confirm Purchase (Demo)"):
            upgrade_subscription(st.session_state.user_email, plan)
            del st.session_state["pending_plan"]
            st.success("Upgraded!")
            st.rerun()

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
        api_key = st.text_input("OpenAI API Key (optional)", type="password")
        st.divider()
        st.caption("Data Lie Detector v2.0")

    # HERO HEADER
    st.markdown(f"""
    <div class="hero-header">
        <h1>🕵️ Data Lie Detector</h1>
        <p>Dashboard — Upload your data to detect hidden issues</p>
    </div>
    """, unsafe_allow_html=True)

    # ───────── ANALYSIS ENGINE ─────────
    files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    if files:
        # Multi-file handling
        selected_file = files[0]
        if len(files) > 1:
            selected_file_name = st.selectbox("Select file", [f.name for f in files])
            selected_file = next(f for f in files if f.name == selected_file_name)
        
        df = load_file(selected_file)
        if df is not None:
            if selected_file.name not in st.session_state.counted_files:
                increment_dataset_usage(st.session_state.user_email)
                st.session_state.counted_files.add(selected_file.name)
            
            profile = profile_data(df)
            anomalies = detect_anomalies(df, profile["numeric_cols"])
            trust_score = calculate_trust(profile, anomalies, profile["rows"])
            risk_level = decision_risk(trust_score)
            explanation = generate_explanation(trust_score, profile, anomalies)

            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1: render_score_card("Trust Score", f"{trust_score}", get_score_color(trust_score))
            with m2: render_score_card("Rows", f"{profile['rows']:,}", "")
            with m3: render_score_card("Duplicates", f"{profile['duplicates']:,}", "score-red" if profile['duplicates']>0 else "score-green")
            with m4: st.markdown(f'<div class="score-card"><div class="label">Decision Risk</div><div style="margin-top:0.5rem"><span class="risk-badge {get_risk_class(risk_level)}">{risk_level}</span></div></div>', unsafe_allow_html=True)

            verdict_text, verdict_class = generate_decision_verdict(trust_score, any(v > 50 for v in profile["missing"].values()))
            st.markdown(f'<div class="insight-box" style="text-align:center; margin: 1rem 0; border-color: rgba(123,47,247,0.4);">{verdict_text}</div>', unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🕵️ Detection", "🧠 AI Insights", "🔄 Export"])
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)
                render_section("🧬", "Column Analysis")
                st.write(profile["missing"])
            with tab2:
                render_section("📉", "Anomalies Detected")
                st.write(anomalies)
            with tab3:
                if st.button("Get AI Analysis"):
                    from utils.ai_explain import ai_explain
                    st.write(ai_explain(profile, anomalies, trust_score, api_key=api_key))
            with tab4:
                if st.button("Download PDF Report"):
                    pdf = generate_report(trust_score, explanation, profile, anomalies, risk_level)
                    st.download_button("Download PDF", pdf, "report.pdf")

elif view == "app":
    # --- LOGIN ---
    apply_dashboard_styles()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><div style='text-align:center; background:rgba(255,255,255,0.03); padding:2.5rem; border-radius:20px; border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{logo_b64}' style='height:4rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:white;'>Welcome Back</h2><p style='color:gray;'>Log in to your dashboard</p>", unsafe_allow_html=True)
        
        google_url = get_google_login_url()
        if google_url: st.link_button("Continue with Google", google_url, type="primary", use_container_width=True)
        else: st.info("OAuth not configured. Use demo mode below.")
        
        if st.button("Continue as Guest (Demo)", use_container_width=True):
            st.session_state.user_email = f"guest_{int(time.time())}@demo.com"
            login_user(st.session_state.user_email)
            st.rerun()
        
        if st.button("← Back to Home"):
            st.query_params.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- LANDING PAGE ---
    show_landing_page()
