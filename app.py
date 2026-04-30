import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import re
import json
from typing import Any, Dict, Optional, Tuple
from supabase import create_client, Client

# ============================================================
# GLOBAL SECURITY SHIELD (EMBEDDED)
# ============================================================
DEFAULT_PATTERNS = {
    "sql_injection": [r"(\%27)|(\')|(\-\-)|(\%23)|(#)", r"(union.*select)", r"(or\s+1\s*=\s*1)"],
    "xss": [r"<script", r"javascript:", r"onload=", r"onerror="],
    "path_traversal": [r"\.\./", r"\.\.\\"],
    "command_injection": [r"(\|)|(\&)|(;)", r"(ping)|(nslookup)|(wget)"]
}

class SecurityException(Exception): pass

class WebAppShield:
    def __init__(self, app_name: str, api_key: str, dashboard_url: str):
        self.app_name = app_name
        self.api_key = api_key
        self.dashboard_url = dashboard_url
        self.patterns = DEFAULT_PATTERNS.copy()

    def sanitize_input(self, value: Any) -> Any:
        if isinstance(value, str):
            for attack_type, patterns in self.patterns.items():
                for pat in patterns:
                    if re.search(pat, value, re.IGNORECASE):
                        raise SecurityException(f"Blocked: potential {attack_type}")
            return value
        return value

    def log_threat(self, request_data: Dict):
        try:
            payload = {"app_name": self.app_name, "api_key": self.api_key, "timestamp": datetime.utcnow().isoformat(), "data": request_data}
            requests.get(f"{self.dashboard_url}{json.dumps(payload)}", timeout=1)
        except: pass

    def protect_streamlit(self):
        if hasattr(st, 'query_params'):
            for key, value in st.query_params.items():
                try: self.sanitize_input(value)
                except SecurityException:
                    st.error("🚨 Security alert: Malicious input blocked.")
                    st.stop()

shield = WebAppShield(
    app_name="GlobalInternet.py Main Website",
    api_key="b-yXubx0KlFJ_uOxnlH3OhbCKigNqiXbL-LVaUQlNoU",
    dashboard_url="https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
)

# ============================================================
# APP CONFIG & BACKGROUND
# ============================================================
st.set_page_config(page_title="GlobalInternet.py", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0f2a 0%, #0f1a3a 50%, #0a0f2a 100%) !important;
    }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 60% 70%, white, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 80% 10%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 10% 80%, white, rgba(0,0,0,0));
        background-size: 200px 200px; opacity: 0.8; z-index: -1;
        animation: twinkle 4s infinite alternate;
    }
    @keyframes twinkle { 0% { opacity: 0.3; } 100% { opacity: 1; } }
    
    /* Content styling */
    .hero, .card, .team-card, .comment-box {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem; color: #111;
    }
    .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important; color: white !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Google AdSense Meta Tag (Direct Markdown)
st.markdown('<meta name="google-adsense-account" content="ca-pub-YOUR_ADSENSE_ID">', unsafe_allow_html=True)

# ============================================================
# CORE LOGIC
# ============================================================
shield.protect_streamlit()

# --- Dictionaries (Condensed for brevity) ---
lang_choice = st.sidebar.selectbox("🌐 Language / Langue", ["English", "Français", "Español", "Kreyòl"])

# --- Main UI ---
st.markdown(f"""
<div class="hero">
    <h1>GlobalInternet.py</h1>
    <p>Build with Python. Deliver with Speed. Innovate with AI.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card"><h3>👨‍💻 About GlobalInternet.py</h3><p>We build high-end Python software for a global market. From AI solutions to national voting systems, our team delivers the complete source code to your inbox.</p></div>', unsafe_allow_html=True)
    
    # Video Embed via Markdown
    st.markdown("""
    <div style="border-radius:15px; overflow:hidden;">
        <iframe width="100%" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>💳 Payments</h3><p>We accept <b>Sendwave</b> and <b>Western Union</b> for international software contracts.</p></div>', unsafe_allow_html=True)
    
    st.info("Founder: Gesner Deslandes")
    st.write("Technology Coordinator")

# --- Projects Section ---
st.header("🏆 Premium Projects")
p_col1, p_col2 = st.columns(2)

with p_col1:
    st.markdown("""
    <div class="card">
        <h3>🇭🇹 Haiti Online Voting Software</h3>
        <p>Complete multi-language presidential election system.</p>
        <p style="color:#ff6b35; font-weight:bold;">$15,000 USD</p>
    </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.markdown("""
    <div class="card">
        <h3>🚁 Drone Commander</h3>
        <p>Simulation and real-time MAVLink control system.</p>
        <p style="color:#ff6b35; font-weight:bold;">$12,000 USD</p>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align:center; color:white; padding:2rem;">
    <p>© 2026 GlobalInternet.py - Built by Gesner Deslandes</p>
</div>
""", unsafe_allow_html=True)
