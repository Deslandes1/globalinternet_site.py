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

# ========== SECURITY: AUTOMATED THREAT DETECTION (NO IPs PRE-BLOCKED) ==========
# NO IPs are pre-blocked. Only malicious behavior triggers auto-block.

# Store blocked IPs (starts empty - only malicious IPs get added)
BLOCKED_IPS = set([])  # ← EMPTY! Your IP is NOT blocked

# Track suspicious activity per IP
suspicious_ips = defaultdict(list)

# Malicious patterns to detect
MALICIOUS_PATHS = [
    "/wp-admin", "/wp-login.php", "/wordpress",           # WordPress attacks
    "/admin", "/administrator", "/admin.php",             # Admin panel scans
    ".env", ".git", ".aws", ".config",                    # Secret file scans
    "/phpmyadmin", "/mysql", "/pma",                      # Database scans
    "/api/v1", "/swagger", "/docs",                       # API endpoint scans
    "/backup", "/dump", "/sql",                           # Backup scans
    "/shell", "/cmd", "/exec",                            # Command execution
    "../", "..%2f", "..%252f",                           # Path traversal
    "' OR '1'='1", "' UNION SELECT",                      # SQL injection patterns
    "<script", "javascript:", "onerror=",                 # XSS patterns
]

SUSPICIOUS_USER_AGENTS = [
    "python-requests", "curl", "wget", "go-http-client",
    "nikto", "nmap", "sqlmap", "burp", "masscan", "zgrab",
]

def detect_malicious_activity(ip, path, user_agent):
    """Detect if a request is malicious"""
    reasons = []
    
    # Check for malicious paths
    for malicious in MALICIOUS_PATHS:
        if malicious.lower() in path.lower():
            reasons.append(f"Suspicious path: {malicious}")
            break
    
    # Check for suspicious user agents (NOT including "unknown" - that could be you)
    for suspicious in SUSPICIOUS_USER_AGENTS:
        if suspicious.lower() in user_agent.lower():
            reasons.append(f"Suspicious User-Agent: {user_agent}")
            break
    
    # Check for rapid requests (rate limiting breach attempt)
    now = datetime.now()
    suspicious_ips[ip] = [ts for ts in suspicious_ips[ip] if now - ts < timedelta(seconds=60)]
    suspicious_ips[ip].append(now)
    
    if len(suspicious_ips[ip]) > 50:  # More than 50 requests in 60 seconds
        reasons.append(f"Rapid requests: {len(suspicious_ips[ip])} in 60 seconds")
    
    return reasons

def auto_block_ip(ip, reasons):
    """Automatically block an IP and log the reason"""
    if ip not in BLOCKED_IPS:
        BLOCKED_IPS.add(ip)
        
        # Log the block (you can also email yourself)
        block_log = f"{datetime.now()} - BLOCKED IP: {ip} - Reasons: {', '.join(reasons)}\n"
        try:
            with open("blocked_ips.log", "a") as f:
                f.write(block_log)
        except:
            pass
        
        # Optional: Send email alert
        try:
            sender = st.secrets.get("email", {}).get("sender", "")
            password = st.secrets.get("email", {}).get("password", "")
            receiver = st.secrets.get("email", {}).get("receiver", "")
            if sender and password and receiver:
                msg = MIMEMultipart()
                msg["From"] = sender
                msg["To"] = receiver
                msg["Subject"] = f"🚨 SECURITY ALERT: IP {ip} BLOCKED"
                body = f"Time: {datetime.now()}\nIP: {ip}\nReasons: {', '.join(reasons)}"
                msg.attach(MIMEText(body, "plain"))
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender, password)
                    server.sendmail(sender, receiver, msg.as_string())
        except:
            pass
        
        return True
    return False

def security_check():
    """Main security function - runs on every request"""
    try:
        # Get visitor IP
        visitor_ip = requests.get("https://api.ipify.org", timeout=5).text
        
        # Check if already blocked
        if visitor_ip in BLOCKED_IPS:
            st.error("🚫 ACCESS DENIED: Your IP has been blocked due to suspicious activity.")
            st.stop()
        
        # Get request path and user agent
        path = st.context.headers.get("X-Forwarded-Path", "/") if hasattr(st, 'context') else "/"
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        
        # Detect malicious activity
        reasons = detect_malicious_activity(visitor_ip, path, user_agent)
        
        if reasons:
            # Auto-block the IP
            auto_block_ip(visitor_ip, reasons)
            st.error("🚫 ACCESS DENIED: Suspicious activity detected.")
            st.stop()
            
    except Exception as e:
        # If security check fails, allow access (don't block everyone)
        pass

# Run security check FIRST
security_check()
# ========== END SECURITY ==========

# ========== SECURITY: SESSION-BASED RATE LIMITING ==========
def check_rate_limit(max_requests=200, window_seconds=60):
    """Prevents bot attacks by limiting requests per session (higher limit for normal users)"""
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

# ---------- Supabase setup with error handling ----------
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.warning("⚠️ Supabase connection not configured. Comments and likes will be disabled.")
    supabase = None

st.set_page_config(page_title="GlobalInternet.py – Python Software Company", page_icon="🌐", layout="wide")

# ---------- Functions for comments & likes (table "comments") ----------
def get_comments(project_key):
    if not supabase:
        return []
    try:
        response = supabase.table("comments").select("*").eq("project_key", project_key).order("timestamp", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Error loading comments: {e}")
        return []

def add_comment(project_key, username, comment, parent_id=0, reply_to_username=""):
    if not supabase:
        st.warning("Comments are currently disabled.")
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
    except Exception as e:
        st.error(f"Error adding comment: {e}")
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

def delete_comment(comment_id, admin_password):
    if not supabase:
        return False
    if admin_password == "20082010":
        try:
            supabase.table("comments").delete().eq("id", comment_id).execute()
            return True
        except:
            return False
    return False

# ---------- Email notification with error handling ----------
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

# Call rate limiter after initial setup
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
    .like-button { background: none; border: none; cursor: pointer; font-size: 1rem; padding: 0; margin-right: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ---------- English dictionary (COMPLETE - all keys present) ----------
t = {
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
    "view_demo": "🎬 View Demo",
    "demo_screenshot": "Screenshot preview (replace with actual image)",
    "live_demo": "🔗 Live Demo",
    "demo_password_hint": "🔐 Demo password: 20082010",
    "request_info": "Request Info",
    "buy_now": "💵 Buy Now",
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
    "footer_pride": "🇭🇹 Proudly Haitian – serving the world with Python and AI 🇭🇹"
}

# Add all project dictionary entries
project_titles = {
    "haiti": "🇭🇹 Haiti Online Voting Software",
    "dashboard": "📊 Business Intelligence Dashboard",
    "chatbot": "🤖 AI Customer Support Chatbot",
    "school": "🏫 School Management System",
    "pos": "📦 Inventory & POS System",
    "scraper": "📈 Custom Web Scraper & Data Pipeline",
    "chess": "♟️ Play Chess Against the Machine",
    "accountant": "🧮 Accountant Excel Advanced AI",
    "archives": "📜 Haiti Archives Nationales Database",
    "dsm": "🛡️ DSM-2026: SYSTEM SECURED",
    "bi": "📊 Business Intelligence Dashboard",
    "ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
    "task_manager": "🗂️ Task Manager Dashboard",
    "ray": "⚡ Ray Parallel Text Processor",
    "cassandra": "🗄️ Cassandra Data Dashboard",
    "spark": "🌊 Apache Spark Data Processor",
    "drone": "🚁 Haitian Drone Commander",
    "english": "🇬🇧 Let's Learn English with Gesner",
    "spanish": "🇪🇸 Let's Learn Spanish with Gesner",
    "portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
    "ai_career": "🚀 AI Career Coach – Resume Optimizer",
    "ai_medical": "🧪 AI Medical & Scientific Literature Assistant",
    "music_studio": "🎧 Music Studio Pro – Complete Music Production Suite",
    "ai_media": "🎭 AI Media Studio – Talking Photo & Video Editor",
    "chinese": "🇨🇳 Let's Learn Chinese with Gesner – Book 1",
    "french": "🇫🇷 Let's Learn French with Gesner – Book 1",
    "mathematics": "📐 Let's Learn Mathematics with Gesner – Book 1",
    "ai_course": "🤖 AI Foundations & Certification Course",
    "medical_term": "🩺 Medical Terminology Book for Translators",
    "python_course": "🐍 Let's Learn Coding through Python with Gesner",
    "hardware_course": "🔌 Let's Learn Software & Hardware with Gesner"
}

project_descs = {
    "haiti": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard, secret ballot.",
    "dashboard": "Real‑time analytics dashboard. Connect to any database and visualize KPIs, sales trends, inventory.",
    "chatbot": "Intelligent chatbot trained on your business data. Answer customer questions 24/7.",
    "school": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal.",
    "pos": "Web‑based inventory management with point‑of‑sale. Barcode scanning, stock alerts, sales reports.",
    "scraper": "Automated data extraction from any website. Schedule daily, weekly, or monthly runs.",
    "chess": "Educational chess game with AI opponent. Learn tactics like forks, pins, and discovered checks.",
    "accountant": "Professional accounting and loan management suite. Track income/expenses, manage loans.",
    "archives": "National archives database for Haitian citizens. Store NIF, CIN, Passport, Driver's License.",
    "dsm": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time.",
    "bi": "Real‑time analytics dashboard. Connect SQL, Excel, CSV – visualize KPIs and sales trends.",
    "ai_classifier": "Upload an image and AI identifies it from 1000 categories using TensorFlow MobileNetV2.",
    "task_manager": "Manage tasks, track progress, and analyze productivity with real‑time charts.",
    "ray": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution.",
    "cassandra": "Distributed NoSQL database demo. Add orders, search by customer, real‑time analytics.",
    "spark": "Upload CSV and run SQL‑like aggregations using Spark. Real‑time results and charts.",
    "drone": "Control Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink).",
    "english": "Interactive English language learning app. Vocabulary, grammar, pronunciation, quizzes.",
    "spanish": "Complete Spanish learning platform. Vocabulary, verb conjugations, listening comprehension.",
    "portuguese": "Brazilian and European Portuguese learning app. Essential phrases, grammar, dialogues.",
    "ai_career": "Upload your CV and job description – AI analyzes both and provides optimization suggestions.",
    "ai_medical": "Ask medical questions – get answers backed by real research from PubMed with citations.",
    "music_studio": "Professional music production software. Record, mix, create beats with studio effects.",
    "ai_media": "Create videos from photos, audio, or video clips. Four powerful modes including text-to-speech.",
    "chinese": "Complete beginner course for Mandarin Chinese. 20 interactive lessons with native audio.",
    "french": "Complete beginner course for French language. 20 interactive lessons with native audio.",
    "mathematics": "Complete mathematics course for beginners. 20 lessons covering arithmetic to geometry.",
    "ai_course": "28‑day AI mastery course – from beginner to certified expert. Learn ChatGPT, Gemini, MidJourney.",
    "medical_term": "Interactive medical terminology training for interpreters and healthcare professionals.",
    "python_course": "Complete Python programming course – from beginner to advanced. 20 lessons with exercises.",
    "hardware_course": "Connect software with 20 hardware components. Build IoT and robotics projects."
}

project_prices = {
    "haiti": "$2,000 USD", "dashboard": "$1,200 USD", "chatbot": "$800 USD", "school": "$1,500 USD",
    "pos": "$1,000 USD", "scraper": "$500 – $2,000", "chess": "$20 USD", "accountant": "$199 USD",
    "archives": "$1,500 USD", "dsm": "$299 USD", "bi": "$1,200 USD", "ai_classifier": "$1,200 USD",
    "task_manager": "$1,200 USD", "ray": "$1,200 USD", "cassandra": "$1,200 USD", "spark": "$1,200 USD",
    "drone": "$2,000 USD", "english": "$299 USD", "spanish": "$299 USD", "portuguese": "$299 USD",
    "ai_career": "$149 USD", "ai_medical": "$149 USD", "music_studio": "$299 USD", "ai_media": "$149 USD",
    "chinese": "$299 USD", "french": "$299 USD", "mathematics": "$299 USD", "ai_course": "$299 USD",
    "medical_term": "$299 USD", "python_course": "$299 USD", "hardware_course": "$299 USD"
}

project_status = "✅ Available now – includes source code, setup, and support"

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
st.markdown("*From Python scripts to embodied AI – the next frontier.*")

col_video, col_caption = st.columns([2, 1])
with col_video:
    st.video("https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Robotics.mp4")
with col_caption:
    st.markdown("""
    **🧠 Where we are taking our software:**
    - 🤖 **Humanoid Robotics Integration** – Controlling humanoid robots with Python
    - 🧬 **Physical AI (VLA Models)** – Bridging code and real‑world movement
    - 🏭 **Industrial Automation** – Deploying humanoids in factories and logistics
    - 🏠 **Service & Companion Robots** – AI that walks, talks, and assists
    
    👉 Watch how our Python‑powered control systems are bringing humanoid robots to life.
    """)
st.caption("📽️ Demo: Python‑controlled humanoid robot in motion. Our software is evolving from screen to physical AI.")
st.markdown("---")

# ---------- Projects in Perspective (Roadmap) ----------
st.markdown("## 🚀 Projects in Perspective")
st.markdown("*What we are building next – innovations on the horizon.*")

future_projects = [
    {"icon": "🧠", "title": "Humanoid Robot Control Suite", "description": "Python SDK for controlling humanoid robots. Integration with ROS2 and real‑time AI.", "status": "In Development – Q3 2026", "highlight": "VLA models + Python"},
    {"icon": "🏭", "title": "Industrial Automation OS", "description": "Complete operating system for factories – orchestrating humanoid robots and conveyor belts.", "status": "Planning – Q4 2026", "highlight": "Industry 4.0 ready"},
    {"icon": "🏠", "title": "Service Robot Companion", "description": "AI‑powered home assistant that can clean, organize, and interact naturally.", "status": "Research Phase – 2027", "highlight": "Natural language + vision"},
    {"icon": "📦", "title": "Logistics & Warehouse AI", "description": "Autonomous mobile robots for sorting, picking, and delivering packages.", "status": "Prototype – Q1 2027", "highlight": "Real‑time path planning"},
    {"icon": "🌾", "title": "Agricultural Humanoid", "description": "Robots for precision farming – planting, monitoring crops, and harvesting.", "status": "Concept – 2027", "highlight": "Sustainable agriculture"},
    {"icon": "🏥", "title": "Medical Assistant Robot", "description": "Humanoid robot for hospitals – delivering supplies and assisting nurses.", "status": "Early Research – 2027", "highlight": "Healthcare automation"}
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
st.markdown("📢 *These projects represent our vision for the future. Interested in collaborating or investing? Contact us.*")
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

# ---------- Projects Section ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course"
]

demo_urls = {
    "haiti": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/",
    "chess": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/",
    "accountant": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/",
    "dsm": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/",
    "bi": "https://9enktzu34sxzyvtsymghxd.streamlit.app/",
    "ai_classifier": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/",
    "task_manager": "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/",
    "ray": "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/",
    "cassandra": "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/",
    "spark": "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/",
    "drone": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/",
    "english": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/",
    "spanish": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/",
    "portuguese": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/"
}

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
                    st.info("📹 Live demo available upon request. Contact us for a private walkthrough.")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the software: {title} at {price}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; cursor:pointer;">💵 {t["buy_now"]}</button></a>', unsafe_allow_html=True)
                with col_btn2:
                    if st.button(f"{t['request_info']}", key=f"info_{key}"):
                        st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{title}'. Thank you!")

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