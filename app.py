import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from supabase import create_client, Client
from datetime import timedelta
from collections import defaultdict

# ========== SECURITY: AUTOMATED THREAT DETECTION ==========
# NO IPs are pre-blocked - your IP 35.185.209.55 is NOT blocked

# Store blocked IPs (starts empty - only malicious IPs get added)
BLOCKED_IPS = set([])

# Track suspicious activity per IP
suspicious_ips = defaultdict(list)

# Malicious patterns to detect
MALICIOUS_PATHS = [
    "/wp-admin", "/wp-login.php", "/wordpress",
    "/admin", "/administrator", "/admin.php",
    ".env", ".git", ".aws", ".config",
    "/phpmyadmin", "/mysql", "/pma",
    "/backup", "/dump", "/sql",
    "/shell", "/cmd", "/exec",
    "../", "..%2f", "..%252f",
    "' OR '1'='1", "' UNION SELECT",
    "<script", "javascript:", "onerror=",
]

SUSPICIOUS_USER_AGENTS = [
    "python-requests", "curl", "wget", "go-http-client",
    "nikto", "nmap", "sqlmap", "burp", "masscan", "zgrab",
]

def detect_malicious_activity(ip, path, user_agent):
    reasons = []
    for malicious in MALICIOUS_PATHS:
        if malicious.lower() in path.lower():
            reasons.append(f"Suspicious path: {malicious}")
            break
    for suspicious in SUSPICIOUS_USER_AGENTS:
        if suspicious.lower() in user_agent.lower():
            reasons.append(f"Suspicious User-Agent: {user_agent}")
            break
    now = datetime.now()
    suspicious_ips[ip] = [ts for ts in suspicious_ips[ip] if now - ts < timedelta(seconds=60)]
    suspicious_ips[ip].append(now)
    if len(suspicious_ips[ip]) > 50:
        reasons.append(f"Rapid requests: {len(suspicious_ips[ip])} in 60 seconds")
    return reasons

def auto_block_ip(ip, reasons):
    if ip not in BLOCKED_IPS:
        BLOCKED_IPS.add(ip)
        try:
            with open("blocked_ips.log", "a") as f:
                f.write(f"{datetime.now()} - BLOCKED IP: {ip} - Reasons: {', '.join(reasons)}\n")
        except:
            pass

def security_check():
    try:
        visitor_ip = requests.get("https://api.ipify.org", timeout=5).text
        if visitor_ip in BLOCKED_IPS:
            st.error("🚫 ACCESS DENIED: Your IP has been blocked due to suspicious activity.")
            st.stop()
        path = st.context.headers.get("X-Forwarded-Path", "/") if hasattr(st, 'context') else "/"
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        reasons = detect_malicious_activity(visitor_ip, path, user_agent)
        if reasons:
            auto_block_ip(visitor_ip, reasons)
            st.error("🚫 ACCESS DENIED: Suspicious activity detected.")
            st.stop()
    except:
        pass

security_check()
# ========== END SECURITY ==========

# ========== RATE LIMITING ==========
def check_rate_limit(max_requests=200, window_seconds=60):
    if "request_history" not in st.session_state:
        st.session_state.request_history = []
    now = datetime.now()
    st.session_state.request_history = [
        ts for ts in st.session_state.request_history 
        if now - ts < timedelta(seconds=window_seconds)
    ]
    if len(st.session_state.request_history) >= max_requests:
        st.error("🚫 Security: Too many requests. Please wait 60 seconds.")
        st.stop()
    st.session_state.request_history.append(now)
# ========== END RATE LIMITING ==========

# ---------- Supabase setup ----------
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None
    st.warning("⚠️ Comments disabled. Supabase not configured.")

st.set_page_config(page_title="GlobalInternet.py – Python Software Company", page_icon="🌐", layout="wide")

# ---------- Functions for comments & likes ----------
def get_comments(project_key):
    if not supabase:
        return []
    try:
        response = supabase.table("comments").select("*").eq("project_key", project_key).order("timestamp", desc=False).execute()
        return response.data
    except:
        return []

def add_comment(project_key, username, comment, parent_id=0, reply_to_username=""):
    if not supabase:
        return False
    try:
        supabase.table("comments").insert({
            "project_key": project_key,
            "username": username.strip() if username else "Anonymous",
            "comment": comment.strip(),
            "timestamp": datetime.now().isoformat(),
            "likes": 0,
            "parent_id": parent_id,
            "reply_to_username": reply_to_username
        }).execute()
        return True
    except:
        return False

def add_like(comment_id):
    if not supabase:
        return
    try:
        supabase.rpc("increment_likes", {"row_id": comment_id}).execute()
    except:
        try:
            current = supabase.table("comments").select("likes").eq("id", comment_id).execute()
            if current.data:
                new_likes = current.data[0]["likes"] + 1
                supabase.table("comments").update({"likes": new_likes}).eq("id", comment_id).execute()
        except:
            pass

# ---------- Email notification ----------
def send_visit_notification():
    try:
        visitor_ip = requests.get("https://api.ipify.org", timeout=5).text
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP: {visitor_ip}\nUser Agent: {user_agent}"
        sender = st.secrets.get("email", {}).get("sender", "")
        password = st.secrets.get("email", {}).get("password", "")
        receiver = st.secrets.get("email", {}).get("receiver", "")
        if sender and password and receiver:
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

if "notification_sent" not in st.session_state:
    send_visit_notification()
    st.session_state.notification_sent = True

check_rate_limit()

# ---------- CSS ----------
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
        display: flex;
        flex-direction: column;
    }
    .card:hover { transform: translateY(-5px); }
    .card h3 { color: #1e3c72; margin-top: 0; }
    .price { font-size: 1.5rem; font-weight: bold; color: #ff6b35; margin: 0.5rem 0; }
    .team-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .team-card:hover { transform: translateY(-5px); }
    .team-card h4 { color: #1e3c72; margin-bottom: 0.2rem; }
    .team-card p { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
    .team-card img {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 0.5rem;
        border: 2px solid #1e3c72;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        background-color: #1e3c72;
        color: white;
        border-radius: 20px;
        margin-top: 3rem;
    }
    .donation-box {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    .blue-text { color: #0000FF; font-weight: bold; }
    .big-globe { font-size: 120px; display: block; text-align: center; margin-bottom: 0.5rem; }
    .future-project-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .future-project-card:hover { transform: translateY(-5px); }
    .future-project-card h3 { color: #1e3c72; margin: 0.5rem 0; }
    .future-project-card p { color: #333; flex-grow: 1; }
    .status-badge { color: #ff6b35; font-weight: bold; }
    .tech-badge { color: #00c9a7; font-weight: bold; }
    .comment-box {
        background-color: #f1f3f5;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .comment-meta { font-size: 0.8rem; color: #555; margin-bottom: 0.3rem; }
    .reply-box { margin-left: 2rem; border-left: 2px solid #ccc; padding-left: 1rem; }
</style>
""", unsafe_allow_html=True)

# ---------- English dictionary ----------
t = {
    "hero_title": "GlobalInternet.py",
    "hero_sub": "Build with Python. Deliver with Speed. Innovate with AI.",
    "hero_desc": "From Haiti to the world – custom software that works online.",
    "about_title": "👨‍💻 About the Company",
    "about_text": "**GlobalInternet.py** was founded by **Gesner Deslandes** – owner, founder, and lead engineer. We build **Python‑based software** on demand for clients worldwide.",
    "office_photo_caption": "Gesner Deslandes talking avatar – introducing GlobalInternet.py",
    "founder": "Founder & CEO",
    "founder_name": "Gesner Deslandes",
    "founder_title": "Engineer | AI Enthusiast | Python Expert",
    "cv_title": "📄 About the Owner – Gesner Deslandes",
    "cv_intro": "Python Software Builder | Web Developer | Technology Coordinator",
    "cv_summary": "Exceptionally driven leader and manager with a commitment to excellence.",
    "cv_experience_title": "💼 Professional Experience",
    "cv_experience": "Technology Coordinator at Be Like Brit Orphanage (2021–Present)",
    "cv_education_title": "🎓 Education & Training",
    "cv_education": "Vocational Training School – American English",
    "cv_references": "📞 References available upon request.",
    "team_title": "👥 Our Team",
    "team_sub": "Meet the talented people behind GlobalInternet.py",
    "team_members": [
        {"name": "Gesner Deslandes", "role": "Founder & CEO", "since": "2021", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes.JPG"},
        {"name": "Gesner Junior Deslandes", "role": "Assistant to CEO", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/dreamina-2026-04-18-6690-Change%20the%20man's%20attire%20to%20a%20professiona....jpeg"},
        {"name": "Roosevelt Deslandes", "role": "Python Programmer", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Roosevelt%20%20Software%20Builder.jpeg"},
        {"name": "Sebastien Stephane Deslandes", "role": "Python Programmer", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/35372.jpg"},
        {"name": "Zendaya Christelle Deslandes", "role": "Secretary", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/IMG_1411.jpg"}
    ],
    "services_title": "⚙️ Our Services",
    "services": [
        ("🐍 Custom Python Development", "Tailored scripts, automation, backend systems."),
        ("🤖 AI & Machine Learning", "Chatbots, predictive models, data insights."),
        ("🗳️ Election & Voting Software", "Secure, multi‑language, live results."),
        ("📊 Business Dashboards", "Real‑time analytics and reporting tools."),
        ("🌐 Website & Web Apps", "Full‑stack solutions deployed online."),
        ("📦 24‑Hour Delivery", "We work fast – get your software by email."),
    ],
    "projects_title": "🏆 Our Projects & Accomplishments",
    "projects_sub": "Completed software solutions delivered to clients.",
    "view_demo": "🎬 View Demo",
    "live_demo": "🔗 Live Demo",
    "demo_password_hint": "🔐 Demo password: 20082010",
    "request_info": "Request Info",
    "buy_now": "💵 Buy Now",
    "donation_title": "💖 Support GlobalInternet.py",
    "donation_text": "Help us grow and continue building innovative software.",
    "donation_sub": "Your donation supports hosting and development.",
    "donation_method": "🇭🇹 Prisme transfer to Moncash (Digicel)",
    "donation_phone": "📱 (509)-47385663",
    "donation_limit": "Amount limit: Up to 100,000 HTG per transaction",
    "donation_instruction": "Use 'Prisme transfer' in your Moncash app.",
    "donation_sendwave_title": "🌍 SendWave",
    "donation_sendwave_instruction": "Send money via SendWave app.",
    "donation_sendwave_phone": "(509) 4738-5663",
    "donation_bank_title": "🏦 Bank Transfer (UNIBANK)",
    "donation_bank_account": "105-2016-16594727",
    "donation_bank_note": "SWIFT: UNIBANKUS",
    "donation_future": "🔜 Coming soon: Bank transfers.",
    "donation_button": "💸 I've sent my donation",
    "donation_thanks": "Thank you! We will confirm within 24 hours.",
    "contact_title": "📞 Let's Build Something Great",
    "contact_ready": "Ready to start your project?",
    "contact_phone": "📞 (509)-47385663",
    "contact_email": "✉️ deslandes78@gmail.com",
    "contact_delivery": "We deliver full software packages by email.",
    "contact_tagline": "GlobalInternet.py – Your Python partner.",
    "footer_rights": "All rights reserved.",
    "footer_founded": "Founded by Gesner Deslandes | Built with Streamlit",
    "footer_pride": "🇭🇹 Proudly Haitian – serving the world 🇭🇹"
}

# Project data
project_titles = {
    "haiti": "🇭🇹 Haiti Online Voting Software",
    "chess": "♟️ Play Chess Against the Machine",
    "accountant": "🧮 Accountant Excel Advanced AI",
    "dsm": "🛡️ DSM-2026: SYSTEM SECURED",
    "bi": "📊 Business Intelligence Dashboard",
    "ai_classifier": "🧠 AI Image Classifier",
    "drone": "🚁 Haitian Drone Commander",
    "english": "🇬🇧 Learn English with Gesner",
    "spanish": "🇪🇸 Learn Spanish with Gesner",
    "portuguese": "🇵🇹 Learn Portuguese with Gesner",
}

project_descs = {
    "haiti": "Complete presidential election system with multi‑language support.",
    "chess": "Educational chess game with AI opponent. Learn tactics and improve.",
    "accountant": "Professional accounting and loan management suite.",
    "dsm": "Advanced stratosphere monitoring radar system.",
    "bi": "Real‑time analytics dashboard for businesses.",
    "ai_classifier": "Upload an image and AI identifies it from 1000 categories.",
    "drone": "Control Haitian‑made drone from your phone.",
    "english": "Interactive English language learning app.",
    "spanish": "Complete Spanish learning platform.",
    "portuguese": "Brazilian and European Portuguese learning app.",
}

project_prices = {
    "haiti": "$2,000 USD", "chess": "$20 USD", "accountant": "$199 USD",
    "dsm": "$299 USD", "bi": "$1,200 USD", "ai_classifier": "$1,200 USD",
    "drone": "$2,000 USD", "english": "$299 USD", "spanish": "$299 USD", "portuguese": "$299 USD",
}

project_status = "✅ Available now – includes source code, setup, and support"

demo_urls = {
    "haiti": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/",
    "chess": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/",
    "accountant": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/",
    "dsm": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/",
    "bi": "https://9enktzu34sxzyvtsymghxd.streamlit.app/",
    "ai_classifier": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/",
    "drone": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/",
    "english": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/",
    "spanish": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/",
    "portuguese": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/",
}

project_keys = ["haiti", "chess", "accountant", "dsm", "bi", "ai_classifier", "drone", "english", "spanish", "portuguese"]

# ---------- Sidebar ----------
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
st.sidebar.markdown("🌐 Language: English")
st.sidebar.markdown("---")
st.sidebar.markdown("**Founder & Developer:**")
st.sidebar.markdown("Gesner Deslandes")
st.sidebar.markdown("📞 WhatsApp: (509) 4738-5663")
st.sidebar.markdown("📧 Email: deslandes78@gmail.com")
st.sidebar.markdown("---")
st.sidebar.markdown("### © 2026 GlobalInternet.py")
st.sidebar.markdown("All rights reserved")

# ---------- Hero Section ----------
st.markdown(f"""
<div class="hero">
    <span class="big-globe">🌐</span>
    <h1>{t['hero_title']}</h1>
    <p>{t['hero_sub']}</p>
    <p style="font-size:1rem;">{t['hero_desc']}</p>
</div>
""", unsafe_allow_html=True)

# ---------- About Section ----------
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

# ---------- Avatar Video ----------
video_url = "https://github.com/Deslandes1/Gesner-Deslandes-Avatar/blob/main/avatar_video.mp4.mp4?raw=true"
st.video(video_url, format="video/mp4", start_time=0)
st.caption(t['office_photo_caption'])

# ---------- CV Section ----------
st.markdown(f"## {t['cv_title']}")
col_photo, col_info = st.columns([1, 2])
with col_photo:
    owner_video_url = "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes%20The%20Owner%20(1).mp4"
    st.video(owner_video_url)
    st.caption("Gesner Deslandes - Owner & Founder")
with col_info:
    st.markdown(f"### {t['cv_intro']}")
    st.markdown(t['cv_summary'])
with st.expander(f"{t['cv_experience_title']} (click to view)"):
    st.markdown(t['cv_experience'])
with st.expander(f"{t['cv_education_title']} (click to view)"):
    st.markdown(t['cv_education'])
st.caption(t['cv_references'])
st.divider()

# ---------- Team Section ----------
st.markdown(f"## {t['team_title']}")
st.markdown(f"*{t['team_sub']}*")
team = t['team_members']
cols = st.columns(len(team))
for idx, member in enumerate(team):
    with cols[idx]:
        st.markdown(f"""
        <div class="team-card">
            {f'<img src="{member["img"]}" alt="{member["name"]}">' if member["img"] else ''}
            <h4>{member['name']}</h4>
            <p>{member['role']}</p>
            <p><small>📅 {member['since']}</small></p>
        </div>
        """, unsafe_allow_html=True)
st.divider()

# ---------- Humanoid Robotics Video ----------
st.markdown("---")
st.markdown("## 🤖 Leveling Up Our Software: Humanoid Robotics")
col_video, col_caption = st.columns([2, 1])
with col_video:
    st.video("https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Robotics.mp4")
with col_caption:
    st.markdown("""
    **🧠 Where we are taking our software:**
    - 🤖 **Humanoid Robotics Integration**
    - 🧬 **Physical AI (VLA Models)**
    - 🏭 **Industrial Automation**
    - 🏠 **Service & Companion Robots**
    """)
st.markdown("---")

# ---------- Projects in Perspective ----------
st.markdown("## 🚀 Projects in Perspective")
future_projects = [
    {"icon": "🧠", "title": "Humanoid Robot Control Suite", "status": "In Development – Q3 2026"},
    {"icon": "🏭", "title": "Industrial Automation OS", "status": "Planning – Q4 2026"},
    {"icon": "🏠", "title": "Service Robot Companion", "status": "Research Phase – 2027"},
]
cols = st.columns(3)
for idx, project in enumerate(future_projects):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="future-project-card">
            <div style="font-size: 2.5rem;">{project['icon']}</div>
            <h3>{project['title']}</h3>
            <p><span class="status-badge">Status:</span> {project['status']}</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown("---")

# ---------- Services ----------
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

# ---------- Projects Section WITH COMMENTS ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

for i in range(0, len(project_keys), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(project_keys):
            key = project_keys[idx]
            title = project_titles.get(key, "Project")
            desc = project_descs.get(key, "Description not available")
            price = project_prices.get(key, "Contact for price")
            
            with col:
                st.markdown(f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div class="price">{price}</div>
                    <p><em>{project_status}</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                if key in demo_urls:
                    st.markdown(f"<a href='{demo_urls[key]}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                else:
                    st.info("📹 Live demo available upon request.")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner, I am interested in purchasing {title} at {price}."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; cursor:pointer;">💵 {t["buy_now"]}</button></a>', unsafe_allow_html=True)
                with col_btn2:
                    if st.button(f"{t['request_info']}", key=f"info_{key}"):
                        st.info(f"Contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{title}'.")

            # ========== COMMENT SECTION (RESTORED) ==========
            st.markdown("#### 💬 Comments & Questions")
            comments = get_comments(key)
            
            # Display existing comments
            for comment in comments:
                if comment["parent_id"] == 0:
                    st.markdown(f"""
                    <div class="comment-box">
                        <div class="comment-meta">
                            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]}
                        </div>
                        <div>{comment['comment']}</div>
                    """, unsafe_allow_html=True)
                    
                    # Like button
                    if st.button(f"❤️ {comment['likes']}", key=f"like_{key}_{comment['id']}"):
                        add_like(comment['id'])
                        st.rerun()
                    
                    # Reply button
                    if st.button("💬 Reply", key=f"reply_{key}_{comment['id']}"):
                        st.session_state[f"reply_to_{comment['id']}"] = True
                    
                    # Reply form
                    if st.session_state.get(f"reply_to_{comment['id']}", False):
                        with st.form(key=f"reply_form_{comment['id']}"):
                            reply_name = st.text_input("Your name", key=f"reply_name_{comment['id']}")
                            reply_text = st.text_area("Your reply", key=f"reply_text_{comment['id']}")
                            if st.form_submit_button("Post Reply"):
                                if reply_text.strip():
                                    add_comment(key, reply_name if reply_name.strip() else "Anonymous", reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
                                    st.session_state[f"reply_to_{comment['id']}"] = False
                                    st.rerun()
                    
                    # Display replies
                    replies = [c for c in comments if c["parent_id"] == comment["id"]]
                    for reply in replies:
                        st.markdown(f"""
                        <div class="reply-box">
                            <div class="comment-meta">
                                <strong>{reply['username']}</strong> (replied to {reply['reply_to_username']}) · {reply['timestamp'][:16]}
                            </div>
                            <div>{reply['comment']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"❤️ {reply['likes']}", key=f"like_reply_{key}_{reply['id']}"):
                            add_like(reply['id'])
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # New comment form
            with st.form(key=f"comment_form_{key}"):
                st.markdown("**Leave a comment**")
                name = st.text_input("Your name (optional)", key=f"name_{key}")
                comment_text = st.text_area("Comment", key=f"comment_{key}")
                if st.form_submit_button("Post Comment"):
                    if comment_text.strip():
                        add_comment(key, name if name.strip() else "Anonymous", comment_text)
                        st.rerun()
                    else:
                        st.warning("Please enter a comment.")
            st.markdown("---")
            # ========== END COMMENT SECTION ==========

# ---------- Donation Section ----------
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
    <p><strong>{t['donation_sendwave_title']}</strong></p>
    <p>{t['donation_sendwave_instruction']}</p>
    <p style="font-size:1.2rem; font-weight:bold;">{t['donation_sendwave_phone']}</p>
    <br>
    <p><strong>{t['donation_bank_title']}</strong></p>
    <p style="font-size:1.2rem; font-weight:bold;">{t['donation_bank_account']}</p>
    <p><em>{t['donation_bank_note']}</em></p>
    <br>
    <p><strong>{t['donation_future']}</strong></p>
</div>
""", unsafe_allow_html=True)

if st.button(t['donation_button']):
    st.success(t['donation_thanks'])

# ---------- Contact Section ----------
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

# ---------- Footer ----------
st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} GlobalInternet.py – {t['footer_rights']}</p>
    <p>{t['footer_founded']}</p>
    <p>{t['footer_pride']}</p>
</div>
""", unsafe_allow_html=True)