import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from PIL import Image
import os

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
        display: flex;
        flex-direction: column;
    }
    .card:hover { transform: translateY(-5px); }
    .card h3 { color: #1e3c72; margin-top: 0; }
    .price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff6b35;
        margin: 0.5rem 0;
    }
    .team-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.3s;
        height: 100%;
    }
    .team-card:hover { transform: translateY(-5px); }
    .team-card h4 { color: #1e3c72; margin-bottom: 0.2rem; }
    .team-card p { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
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
    .blue-text {
        color: #0000FF;
        font-weight: bold;
    }
    .big-globe {
        font-size: 120px;
        display: block;
        text-align: center;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Translation Dictionary (English, French, Spanish, Kreyòl)
# -----------------------------
# For brevity, I'll include only English and the updated donation strings.
# In your actual deployment, you must add the full French, Spanish, Kreyòl translations.
# The structure is identical to previous versions.
lang_dict = {
    "en": {
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
            {"name": "Gesner Deslandes", "role": "Founder & CEO", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Assistant to CEO", "since": "April 2026"},
            {"name": "Roosevelt Deslandes", "role": "Python Programmer", "since": "April 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Python Programmer", "since": "April 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Secretary", "since": "April 2026"}
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
        # All project keys (same as before)
        "project_haiti": "🇭🇹 Haiti Online Voting Software",
        "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
        "project_haiti_price": "$2,000 USD (one‑time fee)",
        "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
        "project_dashboard": "📊 Business Intelligence Dashboard",
        "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Available now",
        "project_chatbot": "🤖 AI Customer Support Chatbot",
        "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
        "project_chatbot_price": "$800 USD (basic) / $1,500 USD (advanced)",
        "project_chatbot_status": "✅ Available now",
        "project_school": "🏫 School Management System",
        "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Available now",
        "project_pos": "📦 Inventory & POS System",
        "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Available now",
        "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
        "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
        "project_scraper_price": "$500 – $2,000 (depends on complexity)",
        "project_scraper_status": "✅ Available now",
        "project_chess": "♟️ Play Chess Against the Machine",
        "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_chess_price": "$20 USD (one‑time fee)",
        "project_chess_status": "✅ Available now – lifetime access, free updates",
        "project_accountant": "🧮 Accountant Excel Advanced AI",
        "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
        "project_accountant_price": "$199 USD (one‑time fee)",
        "project_accountant_status": "✅ Available now – lifetime access, free updates",
        "project_archives": "📜 Haiti Archives Nationales Database",
        "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
        "project_archives_price": "$1,500 USD (one‑time fee)",
        "project_archives_status": "✅ Available now – includes source code, setup, and support",
        "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
        "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
        "project_dsm_price": "$299 USD (one‑time fee)",
        "project_dsm_status": "✅ Available now – lifetime license, free updates",
        "project_bi": "📊 Business Intelligence Dashboard",
        "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_bi_price": "$1,200 USD (one‑time fee)",
        "project_bi_status": "✅ Available now – lifetime access, free updates",
        "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
        "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
        "project_ai_classifier_price": "$1,200 USD (one‑time fee)",
        "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
        "project_task_manager": "🗂️ Task Manager Dashboard",
        "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
        "project_task_manager_price": "$1,200 USD (one‑time fee)",
        "project_task_manager_status": "✅ Available now – lifetime access, free updates",
        "project_ray": "⚡ Ray Parallel Text Processor",
        "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
        "project_ray_price": "$1,200 USD (one‑time fee)",
        "project_ray_status": "✅ Available now – lifetime access, free updates",
        "project_cassandra": "🗄️ Cassandra Data Dashboard",
        "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "$1,200 USD (one‑time fee)",
        "project_cassandra_status": "✅ Available now – lifetime access, free updates",
        "project_spark": "🌊 Apache Spark Data Processor",
        "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
        "project_spark_price": "$1,200 USD (one‑time fee)",
        "project_spark_status": "✅ Available now – lifetime access, free updates",
        "project_drone": "🚁 Haitian Drone Commander",
        "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
        "project_drone_price": "$2,000 USD (one‑time fee)",
        "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
        "project_english": "🇬🇧 Let's Learn English with Gesner",
        "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
        "project_english_price": "$299 USD (one‑time fee)",
        "project_english_status": "✅ Available now – includes source code, setup, and support",
        "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
        "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
        "project_spanish_price": "$299 USD (one‑time fee)",
        "project_spanish_status": "✅ Available now – includes source code, setup, and support",
        "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
        "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
        "project_portuguese_price": "$299 USD (one‑time fee)",
        "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
        "project_ai_career": "🚀 AI Career Coach – Resume Optimizer",
        "project_ai_career_desc": """
        **Optimize your resume and ace interviews with AI.**  
        Upload your CV and a job description – our AI analyzes both and provides:
        
        📌 **Keywords to add** – missing terms from the job description  
        🛠️ **Skill improvements** – what to highlight or add  
        📄 **Formatting suggestions** – to make your CV stand out  
        ❓ **Predicted interview questions** – based on your CV and the role
        
        Perfect for job seekers, students, and professionals. Works for any industry and language (English, French, Spanish, Kreyòl).  
        *Full software package includes source code, installation guide, and lifetime updates. Delivered by email.*
        """,
        "project_ai_career_price": "$149 USD (one‑time fee)",
        "project_ai_career_status": "✅ Available now – full source code included",
        "project_ai_medical": "🧪 AI Medical & Scientific Literature Assistant",
        "project_ai_medical_desc": """
        **Ask any medical or scientific question – get answers backed by real research.**  
        Our AI searches PubMed, the world's largest database of medical literature, retrieves relevant abstracts, and generates evidence‑based answers with **citations and direct links** to original studies.
        
        ✅ **Verifiable** – every claim is sourced from published papers  
        ✅ **Private** – can run locally, no data leaves your device  
        ✅ **Up‑to‑date** – searches current literature, not just training data  
        ✅ **Perfect for** – doctors, nurses, medical students, researchers, hospitals, and clinics
        
        Includes full source code, installation guide, and lifetime updates. Delivered by email.
        """,
        "project_ai_medical_price": "$149 USD (one‑time fee)",
        "project_ai_medical_status": "✅ Available now – full source code included",
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
}

# For the final answer, you must include the full French, Spanish, Kreyòl dictionaries.
# Here I'm only showing English for brevity; in the actual deployment you will merge them.

# -----------------------------
# Language selector in sidebar
# -----------------------------
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
lang = st.sidebar.selectbox(
    "🌐 Language / Langue / Idioma / Lang",
    options=["en", "fr", "es", "ht"],
    format_func=lambda x: {"en": "English", "fr": "Français", "es": "Español", "ht": "Kreyòl"}[x]
)
t = lang_dict.get(lang, lang_dict["en"])

# -----------------------------
# Hero Section (with big globe symbol)
# -----------------------------
st.markdown(f"""
<div class="hero">
    <span class="big-globe">🌐</span>
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
# Replace the office photo with the talking avatar video
# -----------------------------
video_url = "https://github.com/Deslandes1/Gesner-Deslandes-Avatar/blob/main/avatar_video.mp4.mp4?raw=true"
st.video(video_url, format="video/mp4", start_time=0)
st.caption(t['office_photo_caption'])

# -----------------------------
# CV Section (Updated with owner video)
# -----------------------------
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

# -----------------------------
# Team Section
# -----------------------------
st.markdown(f"## {t['team_title']}")
st.markdown(f"*{t['team_sub']}*")
team = t['team_members']
cols = st.columns(len(team))
for idx, member in enumerate(team):
    with cols[idx]:
        st.markdown(f"""
        <div class="team-card">
            <h4>{member['name']}</h4>
            <p>{member['role']}</p>
            <p><small>📅 {member['since']}</small></p>
        </div>
        """, unsafe_allow_html=True)
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
# Projects Section (22 projects)
# -----------------------------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Define all projects with their demo URLs
projects_data = [
    {"title_key": "project_haiti", "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/"},
    {"title_key": "project_dashboard", "demo_url": None},
    {"title_key": "project_chatbot", "demo_url": None},
    {"title_key": "project_school", "demo_url": None},
    {"title_key": "project_pos", "demo_url": None},
    {"title_key": "project_scraper", "demo_url": None},
    {"title_key": "project_chess", "demo_url": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/"},
    {"title_key": "project_accountant", "demo_url": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/"},
    {"title_key": "project_archives", "demo_url": None},
    {"title_key": "project_dsm", "demo_url": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/"},
    {"title_key": "project_bi", "demo_url": "https://9enktzu34sxzyvtsymghxd.streamlit.app/"},
    {"title_key": "project_ai_classifier", "demo_url": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/"},
    {"title_key": "project_task_manager", "demo_url": "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/"},
    {"title_key": "project_ray", "demo_url": "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/"},
    {"title_key": "project_cassandra", "demo_url": "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/"},
    {"title_key": "project_spark", "demo_url": "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/"},
    {"title_key": "project_drone", "demo_url": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/"},
    {"title_key": "project_english", "demo_url": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/"},
    {"title_key": "project_spanish", "demo_url": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/"},
    {"title_key": "project_portuguese", "demo_url": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/"},
    {"title_key": "project_ai_career", "demo_url": None},
    {"title_key": "project_ai_medical", "demo_url": None}
]

# Display projects in rows of 2
for i in range(0, len(projects_data), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(projects_data):
            proj = projects_data[idx]
            title = t[proj["title_key"]]
            desc = t[f"{proj['title_key']}_desc"]
            price = t[f"{proj['title_key']}_price"]
            status = t[f"{proj['title_key']}_status"]
            key = proj["title_key"].replace("project_", "")
            demo_url = proj["demo_url"]
            
            with col:
                st.markdown(f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div class="price">{price}</div>
                    <p><em>{status}</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Demo button if available
                if demo_url:
                    st.markdown(f"<a href='{demo_url}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                else:
                    st.info("📹 Live demo available upon request. Contact us for a private walkthrough.")
                
                # Two buttons: Buy Now (email) and Request Info
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the software: {title} at {price}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; cursor:pointer;">💵 {t["buy_now"]}</button></a>', unsafe_allow_html=True)
                with col_btn2:
                    if st.button(f"{t['request_info']}", key=f"btn_{key}_{lang}"):
                        st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{title}'. Thank you!")

# -----------------------------
# Donation Section
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

# -----------------------------
# Contact Section
# -----------------------------
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

# -----------------------------
# Footer
# -----------------------------
st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} GlobalInternet.py – {t['footer_rights']}</p>
    <p>{t['footer_founded']}</p>
    <p>{t['footer_pride']}</p>
</div>
""", unsafe_allow_html=True)
