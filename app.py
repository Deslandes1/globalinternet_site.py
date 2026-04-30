import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import re
from supabase import create_client, Client

# ============================================================
# GLOBAL SECURITY SHIELD (EMBEDDED – NO EXTERNAL IMPORT)
# ============================================================
import json
from typing import Any, Dict, Optional, Tuple

DEFAULT_PATTERNS = {
    "sql_injection": [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(union.*select)",
        r"(insert.*into)",
        r"(delete.*from)",
        r"(drop.*table)",
        r"(select.*from.*where)",
        r"(or\s+1\s*=\s*1)"
    ],
    "xss": [
        r"<script",
        r"javascript:",
        r"onload=",
        r"onerror=",
        r"onclick=",
        r"alert\(",
        r"prompt\("
    ],
    "path_traversal": [
        r"\.\./",
        r"\.\.\\",
        r"\.\.%2f"
    ],
    "command_injection": [
        r"(\|)|(\&)|(;)",
        r"(ping)|(nslookup)|(wget)"
    ],
    "malicious_user_agents": [
        r"sqlmap",
        r"nikto",
        r"nmap"
    ]
}

class SecurityException(Exception):
    pass

class WebAppShield:
    def __init__(self, app_name: str, api_key: str, dashboard_url: Optional[str] = None):
        self.app_name = app_name
        self.api_key = api_key
        self.dashboard_url = dashboard_url or "https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
        self.patterns = DEFAULT_PATTERNS.copy()
        self.custom_patterns = {}

    def add_custom_pattern(self, attack_type: str, pattern: str):
        if attack_type not in self.custom_patterns:
            self.custom_patterns[attack_type] = []
        self.custom_patterns[attack_type].append(pattern)

    def is_malicious(self, text: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(text, str):
            return False, None
        for attack_type, patterns in self.patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        for attack_type, patterns in self.custom_patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        return False, None

    def sanitize_input(self, value: Any) -> Any:
        if isinstance(value, str):
            malicious, attack_type = self.is_malicious(value)
            if malicious:
                raise SecurityException(f"Blocked: potential {attack_type} attack")
            return value
        elif isinstance(value, dict):
            return {k: self.sanitize_input(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.sanitize_input(i) for i in value]
        else:
            return value

    def log_threat(self, request_data: Dict):
        try:
            payload = {
                "app_name": self.app_name,
                "api_key": self.api_key,
                "timestamp": datetime.utcnow().isoformat(),
                "data": request_data
            }
            log_url = f"{self.dashboard_url}{json.dumps(payload)}"
            requests.get(log_url, timeout=2)
        except Exception:
            pass

    def protect_streamlit(self):
        if hasattr(st, 'query_params') and st.query_params:
            for key, value in st.query_params.items():
                try:
                    self.sanitize_input(value)
                except SecurityException as e:
                    st.error("🚨 Security alert: Malicious input detected and blocked.")
                    self.log_threat({
                        "type": "query_param",
                        "key": key,
                        "value": value,
                        "error": str(e)
                    })
                    st.stop()
        st.sidebar.markdown("🛡️ **Global Security Shield active**")

# Initialise the shield with your API key
shield = WebAppShield(
    app_name="GlobalInternet.py Main Website",
    api_key="b-yXubx0KlFJ_uOxnlH3OhbCKigNqiXbL-LVaUQlNoU",
    dashboard_url="https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
)
# ============================================================

# ---------- Supabase setup ----------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="GlobalInternet.py – Python Software Company",
    page_icon="🌐",
    layout="wide"
)

# ---------- Comment functions (with shield sanitisation) ----------
def get_comments(project_key):
    try:
        response = supabase.table("comments").select("*").eq("project_key", project_key).order("timestamp", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Error loading comments: {e}")
        return []

def add_comment(project_key, username, comment, parent_id=0, reply_to_username=""):
    try:
        safe_comment = shield.sanitize_input(comment.strip())
        safe_username = shield.sanitize_input(username.strip() if username else "Anonymous")
    except SecurityException as e:
        st.error("Security alert: Your comment was blocked because it contains suspicious content.")
        shield.log_threat({
            "type": "comment_blocked",
            "project_key": project_key,
            "username": username,
            "comment": comment,
            "error": str(e)
        })
        return False

    try:
        supabase.table("comments").insert({
            "project_key": project_key,
            "username": safe_username,
            "comment": safe_comment,
            "timestamp": datetime.now().isoformat(),
            "likes": 0,
            "parent_id": parent_id,
            "reply_to_username": reply_to_username
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error adding comment: {e}")
        return False

def add_like(comment_id):
    try:
        supabase.rpc("increment_likes", {"row_id": comment_id}).execute()
    except:
        current = supabase.table("comments").select("likes").eq("id", comment_id).execute()
        if current.data:
            new_likes = current.data[0]["likes"] + 1
            supabase.table("comments").update({"likes": new_likes}).eq("id", comment_id).execute()

def delete_comment(comment_id, admin_password):
    if admin_password == "20082010":
        try:
            supabase.table("comments").delete().eq("id", comment_id).execute()
            return True
        except:
            return False
    return False

# ---------- IP Geolocation ----------
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon,query", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon")
                }
    except Exception:
        pass
    return None

def is_private_ip(ip):
    private_patterns = [
        re.compile(r'^10\.'),
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
        re.compile(r'^192\.168\.'),
        re.compile(r'^127\.'),
        re.compile(r'^169\.254\.'),
        re.compile(r'^fc00:'),
        re.compile(r'^fd00:'),
        re.compile(r'^::1$')
    ]
    return any(pattern.match(ip) for pattern in private_patterns)

def get_real_ip():
    try:
        headers = st.context.headers
        forwarded = headers.get("X-Forwarded-For")
        if forwarded:
            for candidate in forwarded.split(","):
                candidate = candidate.strip()
                if candidate and not is_private_ip(candidate):
                    return candidate
            return forwarded.split(",")[0].strip()
    except Exception:
        pass

    if "real_ip" not in st.session_state:
        query_params = st.query_params
        if "real_ip" in query_params:
            st.session_state.real_ip = query_params["real_ip"]
        else:
            ip_fetcher_script = """
            <script>
                fetch('https://api.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => {
                        var ip = data.ip;
                        var url = new URL(window.location.href);
                        url.searchParams.set('real_ip', ip);
                        window.location.href = url.toString();
                    });
            </script>
            """
            st.markdown(ip_fetcher_script, unsafe_allow_html=True)
            st.stop()
        return st.session_state.real_ip
    else:
        return st.session_state.real_ip

    return "Unable to retrieve"

def send_visit_notification():
    try:
        visitor_ip = get_real_ip()
        location = get_location(visitor_ip) if visitor_ip != "Unable to retrieve" else None
        user_agent = "unknown (Streamlit Cloud)"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP: {visitor_ip}\n"
        if location:
            body += f"📍 Country: {location['country']}\n📍 Region: {location['region']}\n📍 City: {location['city']}\n🛜 ISP: {location['isp']}\n"
        else:
            body += "📍 Location: Could not determine\n"
        body += f"User Agent: {user_agent}\n"
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

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Activate shield protection (checks URL parameters)
shield.protect_streamlit()

# ============================================================
# BEAUTIFUL STARRY BLUE BACKGROUND (ADDED)
# ============================================================
st.markdown("""
<style>
    /* Starry background for the whole app */
    .stApp {
        background: linear-gradient(135deg, #0a0f2a 0%, #0f1a3a 50%, #0a0f2a 100%) !important;
        position: relative;
        overflow-x: hidden;
    }
    /* Fixed starfield covering all empty areas */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 60% 70%, white, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 80% 10%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 40% 90%, white, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 95% 45%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 5% 85%, white, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 75% 55%, white, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 30% 15%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 50% 50%, white, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 88% 92%, white, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 12% 22%, white, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 45% 78%, white, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 67% 33%, white, rgba(0,0,0,0));
        background-size: 200px 200px, 250px 250px, 300px 300px, 150px 150px, 220px 220px, 180px 180px, 260px 260px, 280px 280px, 200px 200px, 240px 240px, 190px 190px, 210px 210px, 270px 270px;
        background-repeat: no-repeat;
        opacity: 0.8;
        pointer-events: none;
        z-index: -1;
        animation: twinkle 3s infinite alternate;
    }
    /* Twinkling animation */
    @keyframes twinkle {
        0% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    /* Additional floating stars using multiple box shadows */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        box-shadow: 
            0px 0px 2px 1px white, 100px 300px 3px 1px white, 250px 50px 2px 0px white,
            400px 600px 3px 1px white, 550px 150px 2px 0px white, 700px 450px 3px 1px white,
            850px 200px 2px 0px white, 1000px 700px 4px 1px white, 1200px 350px 2px 0px white,
            150px 800px 3px 1px white, 350px 950px 2px 0px white, 650px 1100px 4px 1px white;
        opacity: 0.7;
        pointer-events: none;
        z-index: -1;
        animation: shine 5s infinite ease-in-out;
    }
    @keyframes shine {
        0% { opacity: 0.3; filter: brightness(1); }
        50% { opacity: 1; filter: brightness(1.2); }
        100% { opacity: 0.3; filter: brightness(1); }
    }
    /* Make content cards slightly transparent to let stars shine through */
    .hero, .card, .team-card, .future-project-card, .donation-box, .footer, .comment-box {
        background-color: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(0px);
    }
    /* Sidebar semi-transparent to see stars */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 42, 0.9) !important;
        color: white;
    }
    .stApp .main .block-container {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ---------- CSS (existing, unchanged) ----------
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
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1e3c72;
    }
    .comment-meta { font-size: 0.75rem; color: #555; margin-bottom: 0.2rem; }
    .reply-box { margin-left: 1.5rem; border-left: 2px solid #ccc; padding-left: 1rem; margin-top: 0.5rem; }
    .like-button { background: none; border: none; cursor: pointer; font-size: 0.8rem; padding: 0; margin-right: 0.5rem; color: #1e3c72; }
    .delete-button { background: none; border: none; cursor: pointer; font-size: 0.7rem; color: red; padding: 0; margin-left: 0.5rem; }
    .stApp {
        margin: 0;
        padding: 0;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FULL DICTIONARIES (ENGLISH, FRENCH, SPANISH)
# ============================================================

# ---------- ENGLISH ----------
lang_en = {
    "hero_title": "GlobalInternet.py",
    "hero_sub": "Build with Python. Deliver with Speed. Innovate with AI.",
    "hero_desc": "From Haiti to the world – custom software that works online.",
    "about_title": "👨‍💻 About the Company",
    "about_text": """
    **GlobalInternet.py** was founded by **Gesner Deslandes** – owner, founder, and lead engineer.  
    We build **Python‑based software** on demand for clients worldwide. Like Silicon Valley, but with a Haitian touch and outstanding outcomes.
    
    - 🧠 **AI‑powered solutions** – chatbots, data analysis, automation  
    - 🗳️ **Complete election & voting systems** – secure, multi‑language, real‑time  
    - 🌐 **Web applications** – dashboards, internal tools, online platforms  
    - 📦 **Full package delivery** – we email you the complete code and guide you through installation
    
    Whether you need a company website, a custom software tool, or a full‑scale online platform – we build it, you own it.
    """,
    "office_photo_caption": "Gesner Deslandes talking avatar – introducing GlobalInternet.py",
    "humanoid_photo_caption": "Gesner Humanoid AI – our digital representative of innovation and software expertise.",
    "founder": "Founder & CEO",
    "founder_name": "Gesner Deslandes",
    "founder_title": "Engineer | AI Enthusiast | Python Expert",
    "cv_title": "📄 About the Owner – Gesner Deslandes",
    "cv_intro": "Python Software Builder | Web Developer | Technology Coordinator",
    "cv_summary": """
    Exceptionally driven leader and manager with a commitment to excellence and precision.  
    **Core competencies:** Leadership, Interpreting (English, French, Haitian Creole), Mechanical orientation, Management, Microsoft Office.
    """,
    "cv_experience_title": "💼 Professional Experience",
    "cv_experience": """
    **Technology Coordinator** – Be Like Brit Orphanage (2021–Present)  
    Set up Zoom meetings, maintain laptops/tablets, provide daily technical support, ensure smooth digital operations.

    **CEO & Interpreting Services** – Personalized tourism for NGO groups, mission teams, and individuals.

    **Fleet Manager / Dispatcher** – J/P Haitian Relief Organization  
    Managed 20+ vehicles, driver logs, maintenance schedules using Excel.

    **Medical Interpreter** – International Child Care  
    Accurate English–French–Creole medical interpretation.

    **Team Leader & Interpreter** – Can‑Do NGO  
    Led reconstruction projects.

    **English Teacher** – Be Like Brit (Preschool to NS4)

    **Document Translator** – United Kingdom Glossary & United States Work‑Rise Company
    """,
    "cv_education_title": "🎓 Education & Training",
    "cv_education": """
    - Vocational Training School – American English  
    - Diesel Institute of Haiti – Diesel Mechanic  
    - Office Computing Certification (October 2000)  
    - High School Graduate
    """,
    "cv_references": "📞 References available upon request.",
    "team_title": "👥 Our Team",
    "team_sub": "Meet the talented people behind GlobalInternet.py – hired April 2026.",
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
        ("🗳️ Election & Voting Software", "Secure, multi‑language, live results – like our Haiti system."),
        ("📊 Business Dashboards", "Real‑time analytics and reporting tools."),
        ("🌐 Website & Web Apps", "Full‑stack solutions deployed online."),
        ("📦 24‑Hour Delivery", "We work fast – get your software by email, ready to use."),
        ("📢 Advertising & Marketing", "Digital campaigns, social media management, AI‑driven targeting, performance reports. From $150 to $1,200 depending on scope.")
    ],
    "projects_title": "🏆 Our Projects & Accomplishments",
    "projects_sub": "Completed software solutions delivered to clients – ready for you to purchase or customize.",
    # ----- ALL PROJECTS (ENGLISH) -----
    "project_haiti": "🇭🇹 Haiti Online Voting Software",
    "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords.",
    "project_haiti_full_price": "$15,000 USD (full package – one‑time)",
    "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
    "project_dashboard": "📊 Business Intelligence Dashboard",
    "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
    "project_dashboard_full_price": "$8,500 USD (full package – one‑time)",
    "project_dashboard_status": "✅ Available now",
    "project_chatbot": "🤖 AI Customer Support Chatbot",
    "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram.",
    "project_chatbot_full_price": "$6,500 USD (full package – one‑time)",
    "project_chatbot_status": "✅ Available now",
    "project_school": "🏫 School Management System",
    "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles.",
    "project_school_full_price": "$9,000 USD (full package – one‑time)",
    "project_school_status": "✅ Available now",
    "project_pos": "📦 Inventory & POS System",
    "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
    "project_pos_full_price": "$7,500 USD (full package – one‑time)",
    "project_pos_status": "✅ Available now",
    "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
    "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs.",
    "project_scraper_full_price": "$5,000 USD (full package – one‑time)",
    "project_scraper_status": "✅ Available now",
    "project_chess": "♟️ Play Chess Against the Machine",
    "project_chess_desc": "Educational chess game with AI opponent (3 levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Multi‑language.",
    "project_chess_full_price": "$499 USD (full package – one‑time)",
    "project_chess_status": "✅ Available now – lifetime access, free updates",
    "project_accountant": "🧮 Accountant Excel Advanced AI",
    "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
    "project_accountant_full_price": "$1,200 USD (full package – one‑time)",
    "project_accountant_status": "✅ Available now – lifetime access, free updates",
    "project_archives": "📜 Haiti Archives Nationales Database",
    "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF, CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
    "project_archives_full_price": "$12,000 USD (full package – one‑time)",
    "project_archives_status": "✅ Available now – includes source code, setup, and support",
    "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
    "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
    "project_dsm_full_price": "$2,500 USD (full package – one‑time)",
    "project_dsm_status": "✅ Available now – lifetime license, free updates",
    "project_bi": "📊 Business Intelligence Dashboard",
    "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
    "project_bi_full_price": "$8,500 USD (full package – one‑time)",
    "project_bi_status": "✅ Available now – lifetime access, free updates",
    "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
    "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
    "project_ai_classifier_full_price": "$4,500 USD (full package – one‑time)",
    "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
    "project_task_manager": "🗂️ Task Manager Dashboard",
    "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
    "project_task_manager_full_price": "$3,500 USD (full package – one‑time)",
    "project_task_manager_status": "✅ Available now – lifetime access, free updates",
    "project_ray": "⚡ Ray Parallel Text Processor",
    "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
    "project_ray_full_price": "$3,500 USD (full package – one‑time)",
    "project_ray_status": "✅ Available now – lifetime access, free updates",
    "project_cassandra": "🗄️ Cassandra Data Dashboard",
    "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
    "project_cassandra_full_price": "$4,000 USD (full package – one‑time)",
    "project_cassandra_status": "✅ Available now – lifetime access, free updates",
    "project_spark": "🌊 Apache Spark Data Processor",
    "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
    "project_spark_full_price": "$5,500 USD (full package – one‑time)",
    "project_spark_status": "✅ Available now – lifetime access, free updates",
    "project_drone": "🚁 Haitian Drone Commander",
    "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
    "project_drone_full_price": "$12,000 USD (full package – one‑time)",
    "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
    "project_english": "🇬🇧 Let's Learn English with Gesner",
    "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
    "project_english_full_price": "$1,500 USD (full package – one‑time)",
    "project_english_status": "✅ Available now – includes source code, setup, and support",
    "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
    "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
    "project_spanish_full_price": "$1,500 USD (full package – one‑time)",
    "project_spanish_status": "✅ Available now – includes source code, setup, and support",
    "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
    "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
    "project_portuguese_full_price": "$1,500 USD (full package – one‑time)",
    "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
    "project_ai_career": "🚀 AI Career Coach – Resume Optimizer",
    "project_ai_career_desc": "**Optimize your resume and ace interviews with AI.** Upload your CV and a job description – our AI analyzes both and provides: Keywords to add, Skill improvements, Formatting suggestions, Predicted interview questions. Perfect for job seekers, students, and professionals. Full source code included.",
    "project_ai_career_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_career_status": "✅ Available now – full source code included",
    "project_ai_medical": "🧪 AI Medical & Scientific Literature Assistant",
    "project_ai_medical_desc": "**Ask any medical or scientific question – get answers backed by real research.** Our AI searches PubMed, retrieves relevant abstracts, and generates evidence‑based answers with citations and direct links. Full source code included.",
    "project_ai_medical_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_medical_status": "✅ Available now – full source code included",
    "project_music_studio": "🎧 Music Studio Pro – Complete Music Production Suite",
    "project_music_studio_desc": "**Professional music production software** – record, mix, and create beats. Includes voice recording, studio effects, multi‑track beat maker, continuous loops, sing over tracks, auto‑tune recorder. Full source code included.",
    "project_music_studio_full_price": "$2,500 USD (full package – one‑time)",
    "project_music_studio_status": "✅ Available now – full source code included",
    "project_ai_media": "🎭 AI Media Studio – Talking Photo & Video Editor",
    "project_ai_media_desc": "**Create professional videos from photos, audio, or video clips.** Four modes: Photo + Speech, Photo + Uploaded Audio, Photo + Background Music, Video + Background Music. Full source code included.",
    "project_ai_media_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_media_status": "✅ Available now – full source code included",
    "project_chinese": "🇨🇳 Let's Learn Chinese with Gesner – Book 1",
    "project_chinese_desc": "**Complete beginner course for Mandarin Chinese.** 20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes. Full source code included.",
    "project_chinese_full_price": "$1,500 USD (full package – one‑time)",
    "project_chinese_status": "✅ Available now – full source code included",
    "project_french": "🇫🇷 Let's Learn French with Gesner – Book 1",
    "project_french_desc": "**Complete beginner course for French language.** 20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes. Full source code included.",
    "project_french_full_price": "$1,500 USD (full package – one‑time)",
    "project_french_status": "✅ Available now – full source code included",
    "project_mathematics": "📐 Let's Learn Mathematics with Gesner – Book 1",
    "project_mathematics_desc": "**Complete mathematics course for beginners.** 20 lessons covering basic arithmetic, geometry, fractions, decimals, percentages, word problems, and more. Full source code included.",
    "project_mathematics_full_price": "$1,500 USD (full package – one‑time)",
    "project_mathematics_status": "✅ Available now – full source code included",
    "project_ai_course": "🤖 AI Foundations & Certification Course",
    "project_ai_course_desc": "**28‑day AI mastery course – from beginner to certified expert.** Learn ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, and more. Full source code included.",
    "project_ai_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_ai_course_status": "✅ Available now – full source code included",
    "project_medical_term": "🩺 Medical Terminology Book for Translators",
    "project_medical_term_desc": "**Interactive medical terminology training for interpreters and healthcare professionals.** 20 lessons covering real doctor‑patient conversations, native voice audio, and translation practice. Full source code included.",
    "project_medical_term_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_term_status": "✅ Available now – full source code included",
    "project_python_course": "🐍 Let's Learn Coding through Python with Gesner",
    "project_python_course_desc": "**Complete Python programming course – from beginner to advanced.** 20 interactive lessons with demo code, 5 practice exercises per lesson, and audio support. Full source code included.",
    "project_python_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_python_course_status": "✅ Available now – full source code included",
    "project_hardware_course": "🔌 Let's Learn Software & Hardware with Gesner",
    "project_hardware_course_desc": "**Connect software with 20 hardware components – build IoT and robotics projects.** 20 lessons covering network cards, Wi‑Fi, Bluetooth, GPS, GPIO, sensors, motors, displays, and more. Full source code included.",
    "project_hardware_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_hardware_course_status": "✅ Available now – full source code included",
    "project_medical_vocab_book2": "📘 Let's Learn Medical Vocabulary with Gesner – Book 2",
    "project_medical_vocab_book2_desc": "**20 lessons – 50 medical terms, 50 acronyms, 50 abbreviations per lesson.** Full audio support for every word. Perfect for medical interpreters, students, and healthcare professionals. Build your medical vocabulary step by step.",
    "project_medical_vocab_book2_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_vocab_book2_status": "✅ Available now – full source code included",
    "project_medical_term_book3": "📘 Let's Learn Medical Terminology with Gesner – Book 3 (English‑French)",
    "project_medical_term_book3_desc": "**Bilingual English‑French medical terminology course.** 20 lessons with 50 terms, 50 acronyms, 50 abbreviations per lesson – each with native audio in both languages. Perfect for French‑speaking interpreters and healthcare professionals.",
    "project_medical_term_book3_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_term_book3_status": "✅ Available now – full source code included",
    "project_toefl_course": "📘 Let's Learn TOEFL with Gesner",
    "project_toefl_course_desc": "**Complete TOEFL preparation course.** 20 lessons with 3 interactive conversations, 50 vocabulary words, 25 idioms, 25 grammar rules, and 1 essay per lesson. Full audio support. Perfect for international students and test takers.",
    "project_toefl_course_full_price": "$1,500 USD (full package – one‑time)",
    "project_toefl_course_status": "✅ Available now – full source code included",
    "project_french_course": "🇫🇷 Let's Learn French with Gesner",
    "project_french_course_desc": "**Complete French language learning course.** 20 lessons with 3 interactive conversations, 50 vocabulary words, 25 idioms, 25 grammar rules, and 1 essay per lesson. Native French audio. Perfect for beginners and intermediate learners.",
    "project_french_course_full_price": "$1,500 USD (full package – one‑time)",
    "project_french_course_status": "✅ Available now – full source code included",
    "project_haiti_marketplace": "🇭🇹 Let's Learn Why Haiti Isn't a Marketplace for Most Social Media",
    "project_haiti_marketplace_desc": "**20 lessons explaining Haiti's digital divide and how to fix it.** Covers algorithms, PayPal absence, diaspora advantage, and actionable solutions. Available in 5 languages (English, Spanish, French, Portuguese, Chinese) with native audio.",
    "project_haiti_marketplace_full_price": "$1,500 USD (full package – one‑time)",
    "project_haiti_marketplace_status": "✅ Available now – full source code included",
    "project_vectra_ai": "🚗 Vectra AI – Self‑Driving Car Simulator",
    "project_vectra_ai_desc": "**Interactive self‑driving car simulation.** Drive on a winding dust road, avoid oncoming cars, adjust speed limit. Uses 5 sensors and AI to stay in the right lane. Full source code included.\n\n**Fair Market Valuation (B2B Licensing):** $4,500 – $12,000 USD ↑ Per Implementation – Based on real‑time physics engine, AI lane‑discipline logic, and custom heading algorithms.",
    "project_vectra_ai_full_price": "$25,000 USD (full package – one‑time)",
    "project_vectra_ai_status": "✅ Available now – full source code included",
    "project_humanoid_robot": "🤖 Humanoid Robot Training & Control Software – Built by Gesner Deslandes",
    "project_humanoid_robot_desc": "Complete software suite to train any humanoid robot to perform real‑world tasks. Includes task programming interface, simulation mode, real‑time telemetry, and API for physical robot integration (ROS2, MAVLink, or custom). Train the robot by demonstration or scripted commands. Full source code, setup guide, and 1 year support included.",
    "project_humanoid_robot_full_price": "$45,000 USD (full package – one‑time)",
    "project_humanoid_robot_status": "✅ Available now – full source code included, lifetime updates, 1 year support",
    "project_hospital": "🏥 Hospital Management System Software – built by Gesner Deslandes",
    "project_hospital_desc": "Complete multi‑specialty hospital management platform. Includes EMR/EHR, OPD/IPD workflows, billing & revenue cycle management, pharmacy, laboratory, radiology integration, inventory & financial management, role‑based dashboards, and enterprise reporting. HL7 & FHIR ready. Cloud or on‑premise. Trusted for mid‑size to national tertiary centers.",
    "project_hospital_full_price": "$35,000 USD (full package – one‑time)",
    "project_hospital_status": "✅ Live demo available | Subscribe monthly",
    "project_arbitration": "⚖️ Develop your arbitration skills With Gesner",
    "project_arbitration_desc": "Executive course – 20 lessons, guest practitioners, interactive learning, audio support, and illustrative images. Covers international arbitration from agreements to enforcement, ethics, and future trends.",
    "project_arbitration_full_price": "$1,200 USD (full package – one‑time)",
    "project_arbitration_status": "✅ Live demo available | Subscribe monthly",
    "project_programming_book": "📘 Let's Learn Basic Syntaxes & Symbols with Gesner",
    "project_programming_book_desc": "Your first step into coding – 20 lessons, 3 examples, 3 exercises per lesson, audio support, and a summary in each chapter. Perfect for beginners.",
    "project_programming_book_full_price": "$499 USD (full package – one‑time)",
    "project_programming_book_status": "✅ Live demo available | Subscribe monthly",
    "project_employee_mgmt": "👥 Employee Management Software – built by Gesner Deslandes",
    "project_employee_mgmt_desc": "Complete workforce management platform with AI scheduling, time tracking, geofencing, payroll integration, team chat, and advanced reports. Perfect for remote, deskless, and multi‑location teams.",
    "project_employee_mgmt_full_price": "$12,500 USD (full package – one‑time)",
    "project_employee_mgmt_status": "✅ Live demo available | Subscribe monthly",
    "project_miroir": "🇭🇹 Miroir Revelation Entreprise de Grand Goave",
    "project_miroir_desc": "Business management app for sales, haircut cards (250 HTG), Moncash & Natcash transactions, and daily CSV reports. Perfect for small business owners.",
    "project_miroir_full_price": "$1,500 USD (full package – one‑time)",
    "project_miroir_status": "✅ Live demo available | Subscribe monthly",
    "project_wordpress": "📝 WordPress Development Suite – built by Gesner Deslandes",
    "project_wordpress_desc": "A fully interactive portfolio tool that proves custom theme/plugin development, performance optimization, SEO best practices, responsive design, project management, and troubleshooting.",
    "project_wordpress_full_price": "$2,500 USD (full package – one‑time)",
    "project_wordpress_status": "✅ Live demo (any username/password) | Subscribe monthly",
    "project_building_systems": "🏢 Building Systems Architect Dashboard – built by Gesner Deslandes",
    "project_building_systems_desc": "A professional MEP & BMS control suite demonstrating real‑time BMS monitoring, thermal networks (CHW/LTHW), electrical infrastructure, BIM‑ready asset register, decarbonisation tracking, and commissioning reports.",
    "project_building_systems_full_price": "$4,500 USD (full package – one‑time)",
    "project_building_systems_status": "✅ Live demo (any username/password) | Subscribe monthly",
    "project_kubernetes_dashboard": "☸️ Kubernetes Dashboard Simulator – built by Gesner Deslandes",
    "project_kubernetes_dashboard_desc": "Interactive simulator of a Kubernetes dashboard. Visualize pods, nodes, deployments, and services. Monitor cluster health, resource usage, and manage workloads via a user‑friendly interface. Perfect for learning K8s or demonstrating cluster management.",
    "project_kubernetes_dashboard_full_price": "$3,500 USD (full package – one‑time)",
    "project_kubernetes_dashboard_status": "✅ Live demo (any username/password) | Subscribe monthly",
    "project_haiti_radar2_tracker": "📡 Haiti Radar 2 Tracker – built by Gesner Deslandes",
    "project_haiti_radar2_tracker_desc": "Advanced radar tracking system for monitoring aircraft, weather, and maritime activity around Haiti. Real‑time simulation with historical data replay, alert zones, and multi‑language support.",
    "project_haiti_radar2_tracker_full_price": "$2,500 USD (full package – one‑time)",
    "project_haiti_radar2_tracker_status": "✅ Live demo (any username/password) | Subscribe monthly",
    # NEW: Let's Learn AI with Gesner
    "project_learn_ai": "🤖 Let's Learn AI with Gesner",
    "project_learn_ai_desc": "Complete 20‑lesson AI learning platform with full English/French/Spanish translations, read‑aloud feature (reads full lesson text), sidebar lesson picker, pricing (monthly and one‑time), and password protection. Master ChatGPT, Gemini, DeepSeek, Grok, Claude, Midjourney, and more.",
    "project_learn_ai_full_price": "$249 USD (full package – one‑time) or $29/month subscription",
    "project_learn_ai_status": "✅ Available now – includes source code, setup, and support",
    # UI common keys
    "view_demo": "🎬 View Demo",
    "live_demo": "🔗 Live Demo",
    "demo_password_hint": "🔐 Demo password: 20082010 (or any username/password on new demos)",
    "request_info": "Request Info",
    "buy_now": "💵 Buy Full Package",
    "subscribe_monthly": "📅 Subscribe Monthly ($299/mo)",
    "contact_note": "📞 To purchase or subscribe, contact us directly: Phone (509)-47385663 | Email deslandes78@gmail.com",
    "donation_title": "💖 Support GlobalInternet.py",
    "donation_text": "Help us grow and continue building innovative software for Haiti and the world.",
    "donation_sub": "Your donation supports hosting, development tools, and free resources for local developers.",
    "donation_method": "🇭🇹 Easy & fast – Prisme transfer to Moncash (Digicel)",
    "donation_phone": "📱 (509)-47385663",
    "donation_limit": "Amount limit: Up to 100,000 HTG per transaction",
    "donation_instruction": "Just use the 'Prisme transfer' feature in your Moncash app to send your contribution to Gesner Deslandes.",
    "donation_sendwave_title": "🌍 International transfer via <span class='blue-text'>SendWave</span>",
    "donation_sendwave_instruction": "Send money directly to our phone number using the SendWave app (available worldwide).",
    "donation_sendwave_phone": "Recipient phone: (509) 4738-5663 (Gesner Deslandes)",
    "donation_bank_title": "🏦 Bank Transfer (UNIBANK US Account)",
    "donation_bank_account": "Account number: 105-2016-16594727",
    "donation_bank_note": "For international transfers, please use SWIFT code UNIBANKUS (or contact us for details).",
    "donation_future": "🔜 Coming soon: Bank‑to‑bank transfers in USD and HTG (international and local).",
    "donation_button": "💸 I've sent my donation – notify me",
    "donation_thanks": "Thank you so much! We will confirm receipt within 24 hours. Your donation via Prisme Transfer, Sendwave, or Moncash (Digicel) goes directly to Gesner Deslandes at (509)-47385663. Your support means the world to us! 🇭🇹",
    "contact_title": "📞 Let’s Build Something Great",
    "contact_ready": "Ready to start your project?",
    "contact_phone": "📞 Phone / WhatsApp: (509)-47385663",
    "contact_email": "✉️ Email: deslandes78@gmail.com",
    "contact_delivery": "We deliver full software packages by email – fast, reliable, and tailored to you.",
    "contact_tagline": "GlobalInternet.py – Your Python partner, from Haiti to the world.",
    "footer_rights": "All rights reserved.",
    "footer_founded": "Founded by Gesner Deslandes | Built with Streamlit | Hosted on GitHub + Streamlit Cloud",
    "footer_pride": "🇭🇹 Proudly Haitian – serving the world with Python and AI 🇭🇹",
    "sendwave_title": "📱 Send Money to Haiti Like a Text – Fast, Fair, and Finally Affordable",
    "sendwave_intro": "For Haitians living abroad, sending money home should be a joy, not a financial burden. That's why we're proud to recommend **Sendwave**, the international transfer service trusted by millions.",
    "sendwave_reasons": "✓ Instant Delivery – Your money arrives in minutes, not days.\n✓ Low to No Fees – Stop losing your hard-earned cash to hidden costs.\n✓ User-Friendly – So simple, it's like sending a text message.\n✓ Secure & Reliable – Real-time tracking and safe processing.",
    "sendwave_cta": "Your siblings and parents will thank you for helping them quickly. Don't wait. Make the switch today.",
    "sendwave_link": "🔗 **For more info and exclusive updates, visit our website:**\nhttps://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/",
    "sendwave_watch_ad": "📺 Watch our ad – Sendwave",
    "western_union_title": "✨✨✨ WESTERN UNION – HAITI ✨✨✨",
    "western_union_text": "💸 Send money fast – anywhere to Haiti\n🔒 Safe, secure, trusted worldwide\n🤝 Cash pickup or direct deposit\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌍 At GlobalInternet.py, we promote money transfers to Haiti.\n\n📞 Contact us for your business promotion:\n✉️ Email: deslandes78@gmail.com\n📱 Phone / WhatsApp: (509)-47385663\n🌐 Website: https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌟 Let’s grow your business together! 🌟",
    "western_union_watch_ad": "📺 Watch our ad – Western Union"
}

# ---------- FRENCH (copy English then override specific keys) ----------
lang_fr = lang_en.copy()
lang_fr.update({
    "hero_sub": "Construisez avec Python. Livrez rapidement. Innovez avec l'IA.",
    "hero_desc": "D'Haïti au monde – des logiciels sur mesure qui fonctionnent en ligne.",
    "about_title": "👨‍💻 À propos de l'entreprise",
    "founder": "Fondateur et PDG",
    "founder_title": "Ingénieur | Passionné d'IA | Expert Python",
    "cv_title": "📄 À propos du propriétaire – Gesner Deslandes",
    "cv_intro": "Constructeur de logiciels Python | Développeur web | Coordinateur technologique",
    "team_title": "👥 Notre équipe",
    "team_sub": "Rencontrez les talents derrière GlobalInternet.py – embauchés en avril 2026.",
    "services_title": "⚙️ Nos services",
    "projects_title": "🏆 Nos projets et réalisations",
    "projects_sub": "Solutions logicielles complètes livrées aux clients – prêtes à être achetées ou personnalisées.",
    "view_demo": "🎬 Voir la démo",
    "live_demo": "🔗 Démo en direct",
    "demo_password_hint": "🔐 Mot de passe démo : 20082010 (ou n'importe quel identifiant/mot de passe sur les nouvelles démos)",
    "request_info": "Demander des informations",
    "buy_now": "💵 Acheter le forfait complet",
    "subscribe_monthly": "📅 S'abonner mensuellement (299 $/mois)",
    "contact_note": "📞 Pour acheter ou vous abonner, contactez‑nous directement : Téléphone (509)-47385663 | Email deslandes78@gmail.com",
    "donation_title": "💖 Soutenez GlobalInternet.py",
    "donation_text": "Aidez-nous à grandir et à continuer de développer des logiciels innovants pour Haïti et le monde.",
    "donation_sub": "Votre don soutient l'hébergement, les outils de développement et les ressources gratuites pour les développeurs locaux.",
    "donation_method": "🇭🇹 Facile et rapide – Transfert Prisme vers Moncash (Digicel)",
    "donation_phone": "📱 (509)-47385663",
    "donation_limit": "Limite de montant : jusqu'à 100 000 HTG par transaction",
    "donation_instruction": "Utilisez simplement la fonction 'Transfert Prisme' dans votre application Moncash pour envoyer votre contribution à Gesner Deslandes.",
    "donation_sendwave_title": "🌍 Transfert international via <span class='blue-text'>SendWave</span>",
    "donation_sendwave_instruction": "Envoyez de l'argent directement à notre numéro de téléphone en utilisant l'application SendWave (disponible dans le monde entier).",
    "donation_sendwave_phone": "Téléphone du bénéficiaire : (509) 4738-5663 (Gesner Deslandes)",
    "donation_bank_title": "🏦 Virement bancaire (Compte UNIBANK US)",
    "donation_bank_account": "Numéro de compte : 105-2016-16594727",
    "donation_bank_note": "Pour les transferts internationaux, veuillez utiliser le code SWIFT UNIBANKUS (ou contactez‑nous pour plus de détails).",
    "donation_future": "🔜 À venir : virements bancaires en USD et HTG (internationaux et locaux).",
    "donation_button": "💸 J'ai envoyé mon don – prévenez‑moi",
    "donation_thanks": "Merci infiniment ! Nous confirmerons la réception dans les 24 heures. Votre don via Prisme Transfer, Sendwave ou Moncash (Digicel) va directement à Gesner Deslandes au (509)-47385663. Votre soutien signifie tout pour nous ! 🇭🇹",
    "contact_title": "📞 Construisons quelque chose de grand",
    "contact_ready": "Prêt à démarrer votre projet ?",
    "contact_phone": "📞 Téléphone / WhatsApp : (509)-47385663",
    "contact_email": "✉️ Email : deslandes78@gmail.com",
    "contact_delivery": "Nous livrons des logiciels complets par email – rapides, fiables et adaptés à vous.",
    "contact_tagline": "GlobalInternet.py – Votre partenaire Python, d'Haïti au monde.",
    "footer_rights": "Tous droits réservés.",
    "footer_founded": "Fondé par Gesner Deslandes | Construit avec Streamlit | Hébergé sur GitHub + Streamlit Cloud",
    "footer_pride": "🇭🇹 Fier d'être Haïtien – servant le monde avec Python et l'IA 🇭🇹",
    "sendwave_title": "📱 Envoyer de l'argent en Haïti comme un texto – Rapide, juste et enfin abordable",
    "sendwave_intro": "Pour les Haïtiens vivant à l'étranger, envoyer de l'argent à la maison devrait être une joie, pas un fardeau financier. C'est pourquoi nous sommes fiers de recommander **Sendwave**, le service de transfert international approuvé par des millions de personnes.",
    "sendwave_reasons": "✓ Livraison instantanée – Votre argent arrive en minutes, pas en jours.\n✓ Frais faibles ou nuls – Ne perdez plus votre argent durement gagné en frais cachés.\n✓ Facile à utiliser – Aussi simple qu'un texto.\n✓ Sécurisé et fiable – Suivi en temps réel et traitement sécurisé.",
    "sendwave_cta": "Vos frères, sœurs et parents vous remercieront de les aider rapidement. N'attendez plus. Passez à Sendwave dès aujourd'hui.",
    "sendwave_link": "🔗 **Pour plus d'informations et des offres exclusives, visitez notre site Web :**\nhttps://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/",
    "sendwave_watch_ad": "📺 Regardez notre publicité – Sendwave",
    "western_union_title": "✨✨✨ WESTERN UNION – HAÏTI ✨✨✨",
    "western_union_text": "💸 Envoyez de l'argent rapidement – n'importe où en Haïti\n🔒 Sûr, sécurisé, approuvé dans le monde entier\n🤝 Retrait en espèces ou dépôt direct\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌍 Chez GlobalInternet.py, nous faisons la promotion des transferts d'argent vers Haïti.\n\n📞 Contactez-nous pour la promotion de votre entreprise :\n✉️ Email : deslandes78@gmail.com\n📱 Téléphone / WhatsApp : (509)-47385663\n🌐 Site Web : https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌟 Développons votre entreprise ensemble ! 🌟",
    "western_union_watch_ad": "📺 Regardez notre publicité – Western Union",
    "project_learn_ai": "🤖 Apprenons l'IA avec Gesner",
    "project_learn_ai_desc": "Plateforme complète d'apprentissage de l'IA en 20 leçons avec traductions complètes en anglais, français, espagnol, fonction de lecture à voix haute (lit tout le texte), sélecteur de leçon dans la barre latérale, tarifs (mensuel ou unique) et protection par mot de passe. Maîtrisez ChatGPT, Gemini, DeepSeek, Grok, Claude, Midjourney et plus encore.",
    "project_learn_ai_full_price": "249 $US (forfait complet – paiement unique) ou abonnement mensuel 29 $US/mois",
    "project_learn_ai_status": "✅ Disponible maintenant – comprend le code source, l'installation et le support",
})

# ---------- SPANISH (copy English then override) ----------
lang_es = lang_en.copy()
lang_es.update({
    "hero_sub": "Construye con Python. Entrega con velocidad. Innova con IA.",
    "hero_desc": "De Haití al mundo – software personalizado que funciona en línea.",
    "about_title": "👨‍💻 Sobre la empresa",
    "founder": "Fundador y CEO",
    "founder_title": "Ingeniero | Entusiasta de IA | Experto en Python",
    "cv_title": "📄 Sobre el propietario – Gesner Deslandes",
    "cv_intro": "Constructor de software Python | Desarrollador web | Coordinador de tecnología",
    "team_title": "👥 Nuestro equipo",
    "team_sub": "Conozca a los talentos detrás de GlobalInternet.py – contratados en abril de 2026.",
    "services_title": "⚙️ Nuestros servicios",
    "projects_title": "🏆 Nuestros proyectos y logros",
    "projects_sub": "Soluciones de software completas entregadas a los clientes – listas para comprar o personalizar.",
    "view_demo": "🎬 Ver demostración",
    "live_demo": "🔗 Demostración en vivo",
    "demo_password_hint": "🔐 Contraseña de demostración: 20082010 (o cualquier nombre de usuario/contraseña en las nuevas demos)",
    "request_info": "Solicitar información",
    "buy_now": "💵 Comprar paquete completo",
    "subscribe_monthly": "📅 Suscribirse mensualmente ($299/mes)",
    "contact_note": "📞 Para comprar o suscribirse, contáctenos directamente: Teléfono (509)-47385663 | Correo electrónico deslandes78@gmail.com",
    "donation_title": "💖 Apoya GlobalInternet.py",
    "donation_text": "Ayúdanos a crecer y a seguir desarrollando software innovador para Haití y el mundo.",
    "donation_sub": "Tu donación apoya el alojamiento, las herramientas de desarrollo y los recursos gratuitos para desarrolladores locales.",
    "donation_method": "🇭🇹 Fácil y rápido – Transferencia Prisme a Moncash (Digicel)",
    "donation_phone": "📱 (509)-47385663",
    "donation_limit": "Límite de monto: hasta 100,000 HTG por transacción",
    "donation_instruction": "Simplemente use la función 'Transferencia Prisme' en su aplicación Moncash para enviar su contribución a Gesner Deslandes.",
    "donation_sendwave_title": "🌍 Transferencia internacional vía <span class='blue-text'>SendWave</span>",
    "donation_sendwave_instruction": "Envíe dinero directamente a nuestro número de teléfono usando la aplicación SendWave (disponible en todo el mundo).",
    "donation_sendwave_phone": "Teléfono del destinatario: (509) 4738-5663 (Gesner Deslandes)",
    "donation_bank_title": "🏦 Transferencia bancaria (Cuenta UNIBANK US)",
    "donation_bank_account": "Número de cuenta: 105-2016-16594727",
    "donation_bank_note": "Para transferencias internacionales, utilice el código SWIFT UNIBANKUS (o contáctenos para más detalles).",
    "donation_future": "🔜 Próximamente: transferencias bancarias en USD y HTG (internacionales y locales).",
    "donation_button": "💸 He enviado mi donación – notifíqueme",
    "donation_thanks": "¡Muchas gracias! Confirmaremos la recepción en 24 horas. Su donación a través de Prisme Transfer, Sendwave o Moncash (Digicel) va directamente a Gesner Deslandes al (509)-47385663. ¡Su apoyo significa todo para nosotros! 🇭🇹",
    "contact_title": "📞 Construyamos algo grandioso",
    "contact_ready": "¿Listo para comenzar su proyecto?",
    "contact_phone": "📞 Teléfono / WhatsApp: (509)-47385663",
    "contact_email": "✉️ Correo electrónico: deslandes78@gmail.com",
    "contact_delivery": "Entregamos paquetes de software completos por correo electrónico – rápidos, confiables y adaptados a usted.",
    "contact_tagline": "GlobalInternet.py – Su socio Python, desde Haití hacia el mundo.",
    "footer_rights": "Todos los derechos reservados.",
    "footer_founded": "Fundado por Gesner Deslandes | Construido con Streamlit | Alojado en GitHub + Streamlit Cloud",
    "footer_pride": "🇭🇹 Orgullosamente haitiano – sirviendo al mundo con Python e IA 🇭🇹",
    "sendwave_title": "📱 Envía dinero a Haití como un texto – Rápido, justo y finalmente asequible",
    "sendwave_intro": "Para los haitianos que viven en el extranjero, enviar dinero a casa debería ser una alegría, no una carga financiera. Por eso nos enorgullece recomendar **Sendwave**, el servicio de transferencia internacional confiable por millones.",
    "sendwave_reasons": "✓ Entrega instantánea – Tu dinero llega en minutos, no en días.\n✓ Comisiones bajas o nulas – Deja de perder tu dinero en costos ocultos.\n✓ Fácil de usar – Tan simple como enviar un mensaje de texto.\n✓ Seguro y confiable – Seguimiento en tiempo real y procesamiento seguro.",
    "sendwave_cta": "Tus hermanos y padres te agradecerán por ayudarlos rápidamente. No esperes más. Cambia a Sendwave hoy.",
    "sendwave_link": "🔗 **Para más información y ofertas exclusivas, visita nuestro sitio web:**\nhttps://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/",
    "sendwave_watch_ad": "📺 Mira nuestro anuncio – Sendwave",
    "western_union_title": "✨✨✨ WESTERN UNION – HAITÍ ✨✨✨",
    "western_union_text": "💸 Envía dinero rápido – a cualquier lugar de Haití\n🔒 Seguro, protegido, confiable en todo el mundo\n🤝 Retiro en efectivo o depósito directo\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌍 En GlobalInternet.py, promovemos las transferencias de dinero a Haití.\n\n📞 Contáctanos para la promoción de tu negocio:\n✉️ Correo electrónico: deslandes78@gmail.com\n📱 Teléfono / WhatsApp: (509)-47385663\n🌐 Sitio web: https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌟 ¡Hagamos crecer tu negocio juntos! 🌟",
    "western_union_watch_ad": "📺 Mira nuestro anuncio – Western Union",
    "project_learn_ai": "🤖 Aprendamos IA con Gesner",
    "project_learn_ai_desc": "Plataforma completa de aprendizaje de IA con 20 lecciones, traducciones completas al inglés, francés y español, función de lectura en voz alta (lee todo el texto), selector de lección en la barra lateral, precios (único o mensual) y protección con contraseña. Domina ChatGPT, Gemini, DeepSeek, Grok, Claude, Midjourney y más.",
    "project_learn_ai_full_price": "$249 USD (paquete completo – pago único) o suscripción mensual $29 USD/mes",
    "project_learn_ai_status": "✅ Disponible ahora – incluye código fuente, instalación y soporte",
})

lang_dict = {"en": lang_en, "fr": lang_fr, "es": lang_es}

# Language selector
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
lang = st.sidebar.selectbox(
    "🌐 Language / Langue / Idioma",
    options=["en", "fr", "es"],
    format_func=lambda x: {"en": "English", "fr": "Français", "es": "Español"}[x]
)
t = lang_dict[lang]

st.sidebar.markdown("---")
st.sidebar.markdown("**Founder & Developer:**")
st.sidebar.markdown("Gesner Deslandes")
st.sidebar.markdown("📞 WhatsApp: (509) 4738-5663")
st.sidebar.markdown("📧 Email: deslandes78@gmail.com")
st.sidebar.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 My CV")
st.sidebar.markdown("[📥 Download / View my CV (Python Developer 2026)](https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes%20CV%20Python%202026.docx)")
st.sidebar.markdown("---")

# ---------- LEGAL PAGES (full content) ----------
with st.sidebar.expander("📜 Privacy Policy"):
    st.markdown("""
    **Privacy Policy for GlobalInternet.py**

    **1. Information we collect**  
    - When you visit our website, we automatically collect your IP address, browser type, and referring page (via standard web logs and services like ip-api.com).  
    - If you post a comment, we store your username, comment text, timestamp, and the project you commented on.  
    - We also collect your email address when you contact us via the contact form or email.

    **2. How we use your information**  
    - To send you notifications about new visitors (only to the site owner).  
    - To respond to your inquiries and process software purchases.  
    - To improve our website and services.  
    - Comments are displayed publicly on the relevant project page.

    **3. Cookies**  
    We use cookies to remember your language preference and login session. Third‑party services (Supabase, Streamlit Cloud) may also use cookies. Google AdSense may place cookies for personalized ads – see Google’s privacy policy.

    **4. Data sharing**  
    We do not sell your personal data. We share only with essential service providers:  
    - Supabase (database for comments)  
    - Streamlit Cloud (hosting)  
    - ip-api.com (IP geolocation)  
    - Google AdSense (advertising, if enabled)

    **5. Your rights**  
    You can request deletion of your comments by emailing deslandes78@gmail.com with the comment ID.

    **6. Contact**  
    For any privacy questions, contact Gesner Deslandes at deslandes78@gmail.com.
    """)

with st.sidebar.expander("📜 Terms of Service"):
    st.markdown("""
    **Terms of Service for GlobalInternet.py**

    **1. Acceptance**  
    By using this website and purchasing software, you agree to these Terms.

    **2. Software purchases**  
    - All software is delivered as source code via email.  
    - You receive a non‑exclusive, perpetual license to use, modify, and deploy the software for your own business or personal use.  
    - You may not resell the source code as‑is without significant modification.  
    - Monthly subscriptions grant access to updates and support for the duration of the subscription.

    **3. Refunds**  
    Because software is delivered digitally, all sales are final. No refunds will be issued after the source code has been sent. However, we offer a live demo before purchase – test thoroughly.

    **4. Demo access**  
    Demos are provided “as is” and may be reset or changed without notice.

    **5. Limitation of liability**  
    We are not liable for any damages arising from the use of our software or website. You assume all responsibility for proper implementation and backup.

    **6. Governing law**  
    These terms are governed by the laws of Haiti.

    **7. Changes**  
    We may update these terms at any time. Continued use of the website constitutes acceptance.
    """)

with st.sidebar.expander("📜 Disclaimer"):
    st.markdown("""
    **Disclaimer for GlobalInternet.py**

    **General**  
    The information and software provided on this website are for general informational purposes only. While we strive to keep the information correct and the software free of bugs, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the software, products, services, or related graphics.

    **No professional advice**  
    The software solutions presented are tools; they do not constitute legal, financial, or medical advice. You should consult a qualified professional for your specific situation.

    **External links**  
    Our website may contain links to external sites (e.g., Sendwave, Western Union, live demos). We have no control over the content or practices of those sites and accept no responsibility for them.

    **“As is” and “as available”**  
    Your use of any software or information on this website is solely at your own risk. We will not be liable for any loss or damage arising from the use of this website or any software purchased from us.

    **Google AdSense**  
    Third‑party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Users may opt out of personalized advertising by visiting Google Ad Settings.

    **Contact**  
    If you have any questions, please contact us at deslandes78@gmail.com.
    """)

st.sidebar.markdown("### 💰 Price")
st.sidebar.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
st.sidebar.markdown("---")
st.sidebar.markdown("### © 2025 GlobalInternet.py")
st.sidebar.markdown("All rights reserved")
st.sidebar.markdown("---")
if st.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# ----------------------------------------------------------------------
# MAIN WEBSITE CONTENT (hero, about, avatar, cv, team, robotics, etc.)
# ----------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <span class="big-globe">🌐</span>
    <h1>{t['hero_title']}</h1>
    <p>{t['hero_sub']}</p>
    <p style="font-size:1rem;">{t['hero_desc']}</p>
</div>
""", unsafe_allow_html=True)

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

col_left, col_center, col_right = st.columns([1,2,1])
with col_center:
    video_url = "https://github.com/Deslandes1/Gesner-Deslandes-Avatar/blob/main/avatar_video.mp4.mp4?raw=true"
    st.video(video_url, format="video/mp4", start_time=0)
    st.caption(t['office_photo_caption'])

st.markdown(f"## {t['cv_title']}")
col_photo, col_info = st.columns([1, 2])
with col_photo:
    owner_video_url = "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes%20The%20Owner%20(1).mp4"
    st.video(owner_video_url)
    st.caption("Gesner Deslandes - Owner & Founder")
with col_info:
    st.markdown(f"### {t['cv_intro']}")
    st.markdown(t['cv_summary'])
    st.markdown("📄 [**Download my CV (Python Developer 2026)**](https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes%20CV%20Python%202026.docx)")
    with st.expander(f"{t['cv_experience_title']} (click to view)"):
        st.markdown(t['cv_experience'])
    with st.expander(f"{t['cv_education_title']} (click to view)"):
        st.markdown(t['cv_education'])
st.caption(t['cv_references'])
st.divider()

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

# Humanoid Robotics Video
st.markdown("---")
st.markdown("## 🤖 Leveling Up Our Software: Humanoid Robotics")
st.markdown("*From Python scripts to embodied AI – the next frontier.*")
col_vid1, col_vid2, col_vid3 = st.columns([1,2,1])
with col_vid2:
    st.video("https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Robotics.mp4")
col_desc1, col_desc2 = st.columns([1,1])
with col_desc1:
    st.caption("📽️ Demo: Python‑controlled humanoid robot in motion. Our software is evolving from screen to physical AI.")
with col_desc2:
    st.markdown("""
    **🧠 Where we are taking our software:**
    - 🤖 **Humanoid Robotics Integration** – Controlling humanoid robots with Python
    - 🧬 **Physical AI (VLA Models)** – Bridging code and real‑world movement
    - 🏭 **Industrial Automation** – Deploying humanoids in factories and logistics
    - 🏠 **Service & Companion Robots** – AI that walks, talks, and assists
    👉 Watch how our Python‑powered control systems are bringing humanoid robots to life.
    🔗 [View the full demo on GitHub](https://github.com/Deslandes1/globalinternet_site.py/blob/main/Robotics.mp4)
    """)
st.markdown("---")

# Projects in Perspective
st.markdown("## 🚀 Projects in Perspective")
st.markdown("*What we are building next – innovations on the horizon.*")
future_projects = [
    {"icon": "🧠", "title": "Humanoid Robot Control Suite", "description": "Python SDK for controlling humanoid robots (walking, grasping, navigation). Integration with ROS2 and real‑time AI.", "status": "In Development – Q3 2026", "highlight": "VLA models + Python"},
    {"icon": "🏭", "title": "Industrial Automation OS", "description": "Complete operating system for factories – orchestrating humanoid robots, conveyor belts, and quality inspection AI.", "status": "Planning – Q4 2026", "highlight": "Industry 4.0 ready"},
    {"icon": "🏠", "title": "Service Robot Companion", "description": "AI‑powered home assistant that can clean, organize, and interact naturally using Python and multimodal models.", "status": "Research Phase – 2027", "highlight": "Natural language + vision"},
    {"icon": "📦", "title": "Logistics & Warehouse AI", "description": "Autonomous mobile robots (AMRs) for sorting, picking, and delivering packages in warehouses and hospitals.", "status": "Prototype – Q1 2027", "highlight": "Real‑time path planning"},
    {"icon": "🌾", "title": "Agricultural Humanoid", "description": "Robots for precision farming – planting, monitoring crops, and harvesting using computer vision and AI.", "status": "Concept – 2027", "highlight": "Sustainable agriculture"},
    {"icon": "🏥", "title": "Medical Assistant Robot", "description": "Humanoid robot for hospitals – delivering supplies, assisting nurses, and patient interaction.", "status": "Early Research – 2027", "highlight": "Healthcare automation"}
]
cols = st.columns(3)
for idx, project in enumerate(future_projects):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="future-project-card">
            <div style="font-size: 2.5rem;">{project['icon']}</div>
            <h3>{project['title']}</h3>
            <p>{project['description']}</p>
            <p><span class="status-badge">Status:</span> {project['status']}</p>
            <p><span class="tech-badge">Key technology:</span> {project['highlight']}</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown("---")
st.markdown("📢 *These projects represent our vision for the future. Each will be built with Python, AI, and human‑centered design. Interested in collaborating or investing? Contact us.*")
st.markdown("---")

# Services
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

# ---------- Projects listing with compact comment section ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

def display_comment(comment, level=0, project_key=None):
    st.markdown(f"""
    <div class="comment-box" style="margin-left: {level*20}px;">
        <div class="comment-meta">
            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]} · 👍 {comment['likes']}
        </div>
        <p style="margin: 0 0 0.2rem 0;">{comment['comment']}</p>
    </div>
    """, unsafe_allow_html=True)
    col_like, col_reply = st.columns([1,4])
    with col_like:
        if st.button(f"❤️ {comment['likes']}", key=f"like_{comment['id']}"):
            add_like(comment['id'])
            st.rerun()
    with st.expander("💬 Reply", expanded=False):
        with st.form(key=f"reply_form_{comment['id']}"):
            reply_name = st.text_input("Your name", key=f"reply_name_{comment['id']}", placeholder="Anonymous")
            reply_text = st.text_area("Reply", key=f"reply_text_{comment['id']}", height=68)
            if st.form_submit_button("Post Reply"):
                if reply_text.strip():
                    add_comment(project_key, reply_name, reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
                    st.rerun()
                else:
                    st.warning("Please enter a reply.")
    replies = [c for c in st.session_state.get(f"comments_{project_key}", []) if c.get("parent_id") == comment['id']]
    for reply in replies:
        display_comment(reply, level+1, project_key)

def show_comment_section(project_key):
    if f"comments_{project_key}" not in st.session_state:
        st.session_state[f"comments_{project_key}"] = get_comments(project_key)
    comments = st.session_state[f"comments_{project_key}"]
    comment_count = len([c for c in comments if c.get("parent_id") == 0])
    with st.expander(f"💬 Comments ({comment_count})", expanded=False):
        top_comments = [c for c in comments if c.get("parent_id") == 0]
        for comment in top_comments:
            display_comment(comment, 0, project_key)
        st.markdown("---")
        with st.form(key=f"new_comment_{project_key}"):
            username = st.text_input("Your name (optional)", key=f"username_{project_key}", placeholder="Anonymous")
            new_comment = st.text_area("Your comment", key=f"comment_{project_key}", height=100)
            if st.form_submit_button("Post Comment"):
                if new_comment.strip():
                    add_comment(project_key, username, new_comment)
                    st.session_state[f"comments_{project_key}"] = get_comments(project_key)
                    st.rerun()
                else:
                    st.warning("Please write a comment.")

project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course",
    "medical_vocab_book2", "medical_term_book3", "toefl_course", "french_course", "haiti_marketplace", "vectra_ai",
    "humanoid_robot", "hospital", "arbitration", "programming_book", "employee_mgmt", "miroir",
    "wordpress", "building_systems", "kubernetes_dashboard", "haiti_radar2_tracker",
    "learn_ai"
]

projects = []
for key in project_keys:
    demo_url = None
    if key == "haiti":
        demo_url = "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/"
    elif key == "chess":
        demo_url = "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/"
    elif key == "accountant":
        demo_url = "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/"
    elif key == "dsm":
        demo_url = "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/"
    elif key == "bi":
        demo_url = "https://9enktzu34sxzyvtsymghxd.streamlit.app/"
    elif key == "ai_classifier":
        demo_url = "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/"
    elif key == "task_manager":
        demo_url = "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/"
    elif key == "ray":
        demo_url = "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/"
    elif key == "cassandra":
        demo_url = "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/"
    elif key == "spark":
        demo_url = "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/"
    elif key == "drone":
        demo_url = "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/"
    elif key == "english":
        demo_url = "https://learn-english-with-gesner-preschoolers-book-app-vpajde8odmsq8x.streamlit.app/"
    elif key == "spanish":
        demo_url = "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/"
    elif key == "portuguese":
        demo_url = "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/"
    elif key == "vectra_ai":
        demo_url = "https://vectra-ai-built-by-gesner-deslandes-dnkhqd57z6vkmiuezujcqu.streamlit.app/"
    elif key == "hospital":
        demo_url = "https://hospital-management-system-software-built-by-gesner-deslandes.streamlit.app/"
    elif key == "arbitration":
        demo_url = "https://develop-your-arbitration-skills-with-gesner-sskvqnmurdk4cuwpr7.streamlit.app/"
    elif key == "programming_book":
        demo_url = "https://let-s-learn-basic-syntaxes-symbols-with-gesner-in-coding-bdupj.streamlit.app/"
    elif key == "employee_mgmt":
        demo_url = "https://employee-management-software-by-gesner-deslandes-nbg7cuewryjif.streamlit.app/"
    elif key == "miroir":
        demo_url = "https://miroir-revelation-entreprise-de-grand-groave-built-by-gesner-d.streamlit.app/"
    elif key == "wordpress":
        demo_url = "https://aczydtm6hucjpvgpdcqomp.streamlit.app/"
    elif key == "building_systems":
        demo_url = "https://building-systems-architect-dashboard-software-built-by-gesner.streamlit.app/"
    elif key == "ai_medical":
        demo_url = "https://ai-scientific-medical-literature-assistant-app-jekssesjyf6ompu.streamlit.app/"
    elif key == "ai_course":
        demo_url = "https://ai-foundations-certification-course-app-lppx7mfpyfwhkokkrxjqtd.streamlit.app/"
    elif key == "music_studio":
        demo_url = "https://7tsm7edg27r5bgbsau7tjk.streamlit.app/"
    elif key == "medical_term":
        demo_url = "https://medtnwvxbgz76wc2jkn3dy.streamlit.app/"
    elif key == "chinese":
        demo_url = "https://fknxadp8mtgntwuqdyuu2v.streamlit.app/"
    elif key == "archives":
        demo_url = "https://haiti-archives-database-367hd3cptqyxdxvezwrzdj.streamlit.app/"
    elif key == "kubernetes_dashboard":
        demo_url = "https://kubernetes-dashboard-simulator-qtkvrzw9twbrqcbhg5yx3z.streamlit.app/"
    elif key == "haiti_radar2_tracker":
        demo_url = "https://haitiradar2-tracker-z9c46uryq5fnp8933wvzjb.streamlit.app/"
    elif key == "learn_ai":
        demo_url = "https://let-s-learn-ai-with-gesner-wodbaf3gydrkif6gshczq5.streamlit.app/"
    projects.append({
        "title": t.get(f"project_{key}", "Project"),
        "desc": t.get(f"project_{key}_desc", "Description not available"),
        "full_price": t.get(f"project_{key}_full_price", "Contact for price"),
        "status": t.get(f"project_{key}_status", "Status"),
        "key": key,
        "demo_url": demo_url
    })

group_a = [p for p in projects if p["demo_url"]]
group_b = [p for p in projects if not p["demo_url"]]

if group_a:
    st.markdown("### 🎯 Software with Live Demo")
    for i in range(0, len(group_a), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_a):
                proj = group_a[idx]
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{proj['title']}</h3>
                        <p>{proj['desc']}</p>
                        <div class="price">💎 Full package: {proj['full_price']}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{proj['status']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<a href='{proj['demo_url']}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{proj['key']}"):
                        st.info(f"To subscribe for {proj['title']} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    subject = f"Purchase: {proj['title']}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {proj['title']} at {proj['full_price']}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)
                    show_comment_section(proj['key'])

if group_b:
    st.markdown("### 🛠️ Software Available for Purchase (No Public Demo)")
    for i in range(0, len(group_b), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_b):
                proj = group_b[idx]
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{proj['title']}</h3>
                        <p>{proj['desc']}</p>
                        <div class="price">💎 Full package: {proj['full_price']}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{proj['status']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("📹 No public demo – contact us for a private walkthrough.")
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{proj['key']}"):
                        st.info(f"To subscribe for {proj['title']} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    subject = f"Purchase: {proj['title']}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {proj['title']} at {proj['full_price']}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)
                    show_comment_section(proj['key'])

# ---------- SENDWAVE PROMOTIONAL SECTION ----------
st.markdown("---")
st.markdown(f"## {t['sendwave_title']}")
col_promo, col_video_ad = st.columns([3, 2])
with col_promo:
    st.markdown(t['sendwave_intro'])
    st.markdown(t['sendwave_reasons'])
    st.markdown(t['sendwave_cta'])
    st.markdown(t['sendwave_link'])
with col_video_ad:
    st.markdown(f"**{t['sendwave_watch_ad']}**")
    sendwave_video_html = """
    <div style="width:100%; max-width:500px; margin:0 auto;">
        <video src="https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Sendwave%20marketing%202026.MP4" muted playsinline loop controls style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"></video>
        <p style="text-align:center; font-size:0.7rem; color:#666; margin-top:5px;">📢 Sendwave ad – Less transfer fees, less drama</p>
    </div>
    """
    st.markdown(sendwave_video_html, unsafe_allow_html=True)

st.markdown("---")

# ---------- WESTERN UNION PROMOTIONAL SECTION ----------
st.markdown(f"## {t['western_union_title']}")
col_wu_promo, col_wu_video = st.columns([3, 2])
with col_wu_promo:
    st.markdown(t['western_union_text'])
with col_wu_video:
    st.markdown(f"**{t['western_union_watch_ad']}**")
    western_union_video_html = """
    <div style="width:100%; max-width:500px; margin:0 auto;">
        <video src="https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/refs/heads/main/WesterUnionPub.MP4" muted playsinline loop controls style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"></video>
        <p style="text-align:center; font-size:0.7rem; color:#666; margin-top:5px;">📢 Western Union ad – Trusted worldwide</p>
    </div>
    """
    st.markdown(western_union_video_html, unsafe_allow_html=True)

st.markdown("---")

# ---------- Donation ----------
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

# ---------- Contact ----------
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
