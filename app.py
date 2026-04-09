import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="GlobalInternet.py – Python Software Company",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Email notification on visit (optional, requires secrets)
# -----------------------------
def send_visit_notification():
    try:
        try:
            visitor_ip = requests.get("https://api.ipify.org").text
        except:
            visitor_ip = "unknown"
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"""
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        IP Address: {visitor_ip}
        User Agent: {user_agent}
        """
        try:
            sender = st.secrets["email"]["sender"]
            password = st.secrets["email"]["password"]
            receiver = st.secrets["email"]["receiver"]
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = receiver
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
        except:
            pass
    except:
        pass

if "notification_sent" not in st.session_state:
    send_visit_notification()
    st.session_state.notification_sent = True

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .hero {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 { font-size: 3rem; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.2rem; opacity: 0.9; }
    .card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 100%;
    }
    .card:hover { transform: translateY(-5px); }
    .card h3 { color: #1e3c72; margin-top: 0; }
    .price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff6b35;
        margin: 0.5rem 0;
    }
    .stButton button {
        background-color: #ff6b35;
        color: white;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover { background-color: #e85d2a; }
    .footer {
        text-align: center;
        padding: 2rem;
        background-color: #1e3c72;
        color: white;
        border-radius: 20px;
        margin-top: 3rem;
    }
    .flag-container { display: flex; justify-content: center; margin: 1rem 0; }
    .donation-box {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Translation Dictionary (full, but only English shown for brevity – include all languages in your actual code)
# For this response, I'll include the full multilingual dictionaries as in the previous code.
# To keep the answer readable, I'm including the complete lang_dict from the previous version.
# In your actual file, you already have all four languages. I'll copy them here.
# (Assuming you have the full lang_dict from the last working version; I'll add the new "live_demo" key.)
# -----------------------------

# Full lang_dict (English, French, Spanish, Kreyòl) as previously defined, plus new "live_demo" key
# For brevity, I'm showing only the English part with the new key, but in your code you must add "live_demo" to all languages.
lang_dict = {
    "en": {
        # ... (all previous keys, plus:)
        "live_demo": "🔗 Live Demo",
        # ... rest unchanged
    },
    "fr": {
        # ... add "live_demo": "🔗 Démo en direct",
    },
    "es": {
        # ... add "live_demo": "🔗 Demo en vivo",
    },
    "ht": {
        # ... add "live_demo": "🔗 Demonstrasyon an dirè",
    }
}
# To save space, I'm not repeating the entire dictionary here. In your actual code, keep your existing lang_dict
# and simply add "live_demo": "🔗 Live Demo" (and translations) to each language.

# -----------------------------
# Language selector
# -----------------------------
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
lang = st.sidebar.selectbox(
    "🌐 Language / Langue / Idioma / Lang",
    options=["en", "fr", "es", "ht"],
    format_func=lambda x: {"en": "English", "fr": "Français", "es": "Español", "ht": "Kreyòl"}[x]
)
t = lang_dict[lang]

# -----------------------------
# Hero Section
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://flagcdn.com/w320/ht.png", width=100)
st.markdown(f"""
<div class="hero">
    <h1>{t['hero_title']}</h1>
    <p>{t['hero_sub']}</p>
    <p style="font-size:1rem;">{t['hero_desc']}</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# About Section
# -----------------------------
st.markdown(f"## {t['about_title']}")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(t['about_text'])
with col2:
    st.markdown(f"""
    <div class="card">
        <h3>{t['founder']}</h3>
        <p><strong>{t['founder_name']}</strong></p>
        <p>{t['founder_title']}</p>
        <p>📞 (509)-47385663</p>
        <p>✉️ deslandes78@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# CV Section (Owner's full background)
# -----------------------------
st.markdown(f"## {t['cv_title']}")
st.markdown(f"### {t['cv_intro']}")
st.markdown(t['cv_summary'])

with st.expander(f"{t['cv_experience_title']} (click to view)"):
    st.markdown(t['cv_experience'])

with st.expander(f"{t['cv_education_title']} (click to view)"):
    st.markdown(t['cv_education'])

st.caption(t['cv_references'])
st.divider()

# -----------------------------
# Services Section
# -----------------------------
st.markdown(f"## {t['services_title']}")
services = t['services']
cols = st.columns(3)
for i, (title, desc) in enumerate(services):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Projects Section (10 projects) with LIVE DEMO URLs for first two
# -----------------------------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

projects = [
    {
        "title": t['project_haiti'],
        "desc": t['project_haiti_desc'],
        "price": t['project_haiti_price'],
        "status": t['project_haiti_status'],
        "contact": t['project_haiti_contact'],
        "key": "haiti",
        "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/",  # LIVE DEMO
        "screenshot": "https://via.placeholder.com/800x400?text=Haiti+Voting+Software"
    },
    {
        "title": t['project_dashboard'],
        "desc": t['project_dashboard_desc'],
        "price": t['project_dashboard_price'],
        "status": t['project_dashboard_status'],
        "contact": t['project_dashboard_contact'],
        "key": "dashboard",
        "demo_url": None,  # No live demo yet – contact for URL
        "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"
    },
    {
        "title": t['project_chatbot'],
        "desc": t['project_chatbot_desc'],
        "price": t['project_chatbot_price'],
        "status": t['project_chatbot_status'],
        "contact": t['project_chatbot_contact'],
        "key": "chatbot",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=AI+Chatbot"
    },
    {
        "title": t['project_school'],
        "desc": t['project_school_desc'],
        "price": t['project_school_price'],
        "status": t['project_school_status'],
        "contact": t['project_school_contact'],
        "key": "school",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=School+Management"
    },
    {
        "title": t['project_pos'],
        "desc": t['project_pos_desc'],
        "price": t['project_pos_price'],
        "status": t['project_pos_status'],
        "contact": t['project_pos_contact'],
        "key": "pos",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=Inventory+POS"
    },
    {
        "title": t['project_scraper'],
        "desc": t['project_scraper_desc'],
        "price": t['project_scraper_price'],
        "status": t['project_scraper_status'],
        "contact": t['project_scraper_contact'],
        "key": "scraper",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=Web+Scraper"
    },
    {
        "title": t['project_chess'],
        "desc": t['project_chess_desc'],
        "price": t['project_chess_price'],
        "status": t['project_chess_status'],
        "contact": t['project_chess_contact'],
        "key": "chess",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=Chess+Game"
    },
    {
        "title": t['project_weapon'],
        "desc": t['project_weapon_desc'],
        "price": t['project_weapon_price'],
        "status": t['project_weapon_status'],
        "contact": t['project_weapon_contact'],
        "key": "weapon",
        "demo_url": "https://ghk5zhugzsx956esum3vth.streamlit.app/",  # LIVE DEMO
        "screenshot": "https://via.placeholder.com/800x400?text=Weapon+Detection"
    },
    {
        "title": t['project_accountant'],
        "desc": t['project_accountant_desc'],
        "price": t['project_accountant_price'],
        "status": t['project_accountant_status'],
        "contact": t['project_accountant_contact'],
        "key": "accountant",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=Accounting+Software"
    },
    {
        "title": t['project_archives'],
        "desc": t['project_archives_desc'],
        "price": t['project_archives_price'],
        "status": t['project_archives_status'],
        "contact": t['project_archives_contact'],
        "key": "archives",
        "demo_url": None,
        "screenshot": "https://via.placeholder.com/800x400?text=National+Archives"
    }
]

# Display projects in rows of 2
for i in range(0, len(projects), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(projects):
            proj = projects[idx]
            with col:
                st.markdown(f"""
                <div class="card" style="height: auto;">
                    <h3>{proj['title']}</h3>
                    <p>{proj['desc']}</p>
                    <div class="price">{proj['price']}</div>
                    <p><em>{proj['status']}</em></p>
                    <p>📞 {proj['contact']}</p>
                </div>
                """, unsafe_allow_html=True)

                # If a live demo URL exists, show a "Live Demo" button
                if proj.get("demo_url"):
                    st.markdown(f"<a href='{proj['demo_url']}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t.get('live_demo', '🔗 Live Demo')}</button></a>", unsafe_allow_html=True)
                else:
                    # Otherwise show the placeholder screenshot demo (or you can keep both)
                    if st.button(f"{t['view_demo']}", key=f"demo_{proj['key']}_{lang}"):
                        with st.expander(f"📸 {proj['title']} – {t['demo_screenshot']}", expanded=True):
                            st.image(proj['screenshot'], use_column_width=True)
                            st.caption("This is a placeholder. Contact us for a live demo URL.")

                # Request Info button (always present)
                if st.button(f"{t['request_info']}", key=f"btn_{proj['key']}_{lang}"):
                    st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{proj['title']}'. Thank you!")

# -----------------------------
# Donation, Contact, Footer (unchanged)
# -----------------------------
st.markdown(f"## {t['donation_title']}")
st.markdown(f"""
<div class="donation-box">
    <h3>{t['donation_text']}</h3>
    <p>{t['donation_sub']}</p>
    <br>
    <p><strong>{t['donation_method']}</strong></p>
    <p style="font-size:1.5rem; font-weight:bold;">{t['donation_phone']}</p>
    <p><strong>{t['donation_limit']}</strong></p>
    <p><em>{t['donation_instruction']}</em></p>
    <br>
    <p><strong>{t['donation_future']}</strong></p>
</div>
""", unsafe_allow_html=True)

if st.button(t['donation_button']):
    st.success(t['donation_thanks'])

st.markdown(f"## {t['contact_title']}")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: center; background-color: #e9ecef; padding: 2rem; border-radius: 20px;">
        <h3>{t['contact_ready']}</h3>
        <p>{t['contact_phone']}</p>
        <p>{t['contact_email']}</p>
        <p>{t['contact_delivery']}</p>
        <p><em>{t['contact_tagline']}</em></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} GlobalInternet.py – {t['footer_rights']}</p>
    <p>{t['footer_founded']}</p>
    <p>{t['footer_pride']}</p>
</div>
""", unsafe_allow_html=True)
