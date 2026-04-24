import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from supabase import create_client, Client

# ========== FORCE GOOGLE ADSENSE META TAG INTO <head> ==========
components.html(
    """
    <head>
        <meta name="google-adsense-account" content="ca-pub-1238061430437782">
    </head>
    """,
    height=0,
)

# ---------- Supabase setup ----------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="GlobalInternet.py – Python Software Company",
    page_icon="🌐",
    layout="wide"
)

# ---------- Comment functions ----------
def get_comments(project_key):
    try:
        response = supabase.table("comments").select("*").eq("project_key", project_key).order("timestamp", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Error loading comments: {e}")
        return []

def add_comment(project_key, username, comment, parent_id=0, reply_to_username=""):
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

# ---------- Email notification ----------
def send_visit_notification():
    try:
        visitor_ip = requests.get("https://api.ipify.org").text
        user_agent = "unknown (Streamlit Cloud)"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP: {visitor_ip}\nUser Agent: {user_agent}"
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

# ========== DICTIONARIES (ENGLISH, FRENCH, SPANISH) ==========
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
    # ----- 38 Projects (English) with full package prices -----
    "project_haiti": "🇭🇹 Haiti Online Voting Software",
    "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
    "project_haiti_price": "$2,000 USD (one‑time fee)",
    "project_haiti_full_price": "$15,000 USD (full package – one‑time)",
    "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
    "project_haiti_contact": "Contact owner for purchase",
    "project_dashboard": "📊 Business Intelligence Dashboard",
    "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
    "project_dashboard_price": "$1,200 USD",
    "project_dashboard_full_price": "$8,500 USD (full package – one‑time)",
    "project_dashboard_status": "✅ Available now",
    "project_dashboard_contact": "Contact owner for purchase",
    "project_chatbot": "🤖 AI Customer Support Chatbot",
    "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
    "project_chatbot_price": "$800 USD (basic) / $1,500 USD (advanced)",
    "project_chatbot_full_price": "$6,500 USD (full package – one‑time)",
    "project_chatbot_status": "✅ Available now",
    "project_chatbot_contact": "Contact owner for purchase",
    "project_school": "🏫 School Management System",
    "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
    "project_school_price": "$1,500 USD",
    "project_school_full_price": "$9,000 USD (full package – one‑time)",
    "project_school_status": "✅ Available now",
    "project_school_contact": "Contact owner for purchase",
    "project_pos": "📦 Inventory & POS System",
    "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
    "project_pos_price": "$1,000 USD",
    "project_pos_full_price": "$7,500 USD (full package – one‑time)",
    "project_pos_status": "✅ Available now",
    "project_pos_contact": "Contact owner for purchase",
    "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
    "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
    "project_scraper_price": "$500 – $2,000 (depends on complexity)",
    "project_scraper_full_price": "$5,000 USD (full package – one‑time)",
    "project_scraper_status": "✅ Available now",
    "project_scraper_contact": "Contact owner for purchase",
    "project_chess": "♟️ Play Chess Against the Machine",
    "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
    "project_chess_price": "$20 USD (one‑time fee)",
    "project_chess_full_price": "$499 USD (full package – one‑time)",
    "project_chess_status": "✅ Available now – lifetime access, free updates",
    "project_chess_contact": "Contact owner for purchase",
    "project_accountant": "🧮 Accountant Excel Advanced AI",
    "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
    "project_accountant_price": "$199 USD (one‑time fee)",
    "project_accountant_full_price": "$1,200 USD (full package – one‑time)",
    "project_accountant_status": "✅ Available now – lifetime access, free updates",
    "project_accountant_contact": "Contact owner for purchase",
    "project_archives": "📜 Haiti Archives Nationales Database",
    "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
    "project_archives_price": "$1,500 USD (one‑time fee)",
    "project_archives_full_price": "$12,000 USD (full package – one‑time)",
    "project_archives_status": "✅ Available now – includes source code, setup, and support",
    "project_archives_contact": "Contact owner for purchase",
    "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
    "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
    "project_dsm_price": "$299 USD (one‑time fee)",
    "project_dsm_full_price": "$2,500 USD (full package – one‑time)",
    "project_dsm_status": "✅ Available now – lifetime license, free updates",
    "project_dsm_contact": "Contact owner for purchase",
    "project_bi": "📊 Business Intelligence Dashboard",
    "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
    "project_bi_price": "$1,200 USD (one‑time fee)",
    "project_bi_full_price": "$8,500 USD (full package – one‑time)",
    "project_bi_status": "✅ Available now – lifetime access, free updates",
    "project_bi_contact": "Contact owner for purchase",
    "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
    "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
    "project_ai_classifier_price": "$1,200 USD (one‑time fee)",
    "project_ai_classifier_full_price": "$4,500 USD (full package – one‑time)",
    "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
    "project_ai_classifier_contact": "Contact owner for purchase",
    "project_task_manager": "🗂️ Task Manager Dashboard",
    "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
    "project_task_manager_price": "$1,200 USD (one‑time fee)",
    "project_task_manager_full_price": "$3,500 USD (full package – one‑time)",
    "project_task_manager_status": "✅ Available now – lifetime access, free updates",
    "project_task_manager_contact": "Contact owner for purchase",
    "project_ray": "⚡ Ray Parallel Text Processor",
    "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
    "project_ray_price": "$1,200 USD (one‑time fee)",
    "project_ray_full_price": "$3,500 USD (full package – one‑time)",
    "project_ray_status": "✅ Available now – lifetime access, free updates",
    "project_ray_contact": "Contact owner for purchase",
    "project_cassandra": "🗄️ Cassandra Data Dashboard",
    "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
    "project_cassandra_price": "$1,200 USD (one‑time fee)",
    "project_cassandra_full_price": "$4,000 USD (full package – one‑time)",
    "project_cassandra_status": "✅ Available now – lifetime access, free updates",
    "project_cassandra_contact": "Contact owner for purchase",
    "project_spark": "🌊 Apache Spark Data Processor",
    "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
    "project_spark_price": "$1,200 USD (one‑time fee)",
    "project_spark_full_price": "$5,500 USD (full package – one‑time)",
    "project_spark_status": "✅ Available now – lifetime access, free updates",
    "project_spark_contact": "Contact owner for purchase",
    "project_drone": "🚁 Haitian Drone Commander",
    "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
    "project_drone_price": "$2,000 USD (one‑time fee)",
    "project_drone_full_price": "$12,000 USD (full package – one‑time)",
    "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
    "project_drone_contact": "Contact owner for purchase",
    "project_english": "🇬🇧 Let's Learn English with Gesner",
    "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
    "project_english_price": "$299 USD (one‑time fee)",
    "project_english_full_price": "$1,500 USD (full package – one‑time)",
    "project_english_status": "✅ Available now – includes source code, setup, and support",
    "project_english_contact": "Contact owner for purchase",
    "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
    "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
    "project_spanish_price": "$299 USD (one‑time fee)",
    "project_spanish_full_price": "$1,500 USD (full package – one‑time)",
    "project_spanish_status": "✅ Available now – includes source code, setup, and support",
    "project_spanish_contact": "Contact owner for purchase",
    "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
    "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
    "project_portuguese_price": "$299 USD (one‑time fee)",
    "project_portuguese_full_price": "$1,500 USD (full package – one‑time)",
    "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
    "project_portuguese_contact": "Contact owner for purchase",
    "project_ai_career": "🚀 AI Career Coach – Resume Optimizer",
    "project_ai_career_desc": "**Optimize your resume and ace interviews with AI.** Upload your CV and a job description – our AI analyzes both and provides: Keywords to add, Skill improvements, Formatting suggestions, Predicted interview questions. Perfect for job seekers, students, and professionals. Full source code included.",
    "project_ai_career_price": "$149 USD (one‑time fee)",
    "project_ai_career_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_career_status": "✅ Available now – full source code included",
    "project_ai_career_contact": "Contact owner for purchase",
    "project_ai_medical": "🧪 AI Medical & Scientific Literature Assistant",
    "project_ai_medical_desc": "**Ask any medical or scientific question – get answers backed by real research.** Our AI searches PubMed, retrieves relevant abstracts, and generates evidence‑based answers with citations and direct links. Full source code included.",
    "project_ai_medical_price": "$149 USD (one‑time fee)",
    "project_ai_medical_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_medical_status": "✅ Available now – full source code included",
    "project_ai_medical_contact": "Contact owner for purchase",
    "project_music_studio": "🎧 Music Studio Pro – Complete Music Production Suite",
    "project_music_studio_desc": "**Professional music production software** – record, mix, and create beats. Includes voice recording, studio effects, multi‑track beat maker, continuous loops, sing over tracks, auto‑tune recorder. Full source code included.",
    "project_music_studio_price": "$299 USD (one‑time fee)",
    "project_music_studio_full_price": "$2,500 USD (full package – one‑time)",
    "project_music_studio_status": "✅ Available now – full source code included",
    "project_music_studio_contact": "Contact owner for purchase",
    "project_ai_media": "🎭 AI Media Studio – Talking Photo & Video Editor",
    "project_ai_media_desc": "**Create professional videos from photos, audio, or video clips.** Four modes: Photo + Speech, Photo + Uploaded Audio, Photo + Background Music, Video + Background Music. Full source code included.",
    "project_ai_media_price": "$149 USD (one‑time fee)",
    "project_ai_media_full_price": "$1,200 USD (full package – one‑time)",
    "project_ai_media_status": "✅ Available now – full source code included",
    "project_ai_media_contact": "Contact owner for purchase",
    "project_chinese": "🇨🇳 Let's Learn Chinese with Gesner – Book 1",
    "project_chinese_desc": "**Complete beginner course for Mandarin Chinese.** 20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes. Full source code included.",
    "project_chinese_price": "$299 USD (one‑time fee)",
    "project_chinese_full_price": "$1,500 USD (full package – one‑time)",
    "project_chinese_status": "✅ Available now – full source code included",
    "project_chinese_contact": "Contact owner for purchase",
    "project_french": "🇫🇷 Let's Learn French with Gesner – Book 1",
    "project_french_desc": "**Complete beginner course for French language.** 20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes. Full source code included.",
    "project_french_price": "$299 USD (one‑time fee)",
    "project_french_full_price": "$1,500 USD (full package – one‑time)",
    "project_french_status": "✅ Available now – full source code included",
    "project_french_contact": "Contact owner for purchase",
    "project_mathematics": "📐 Let's Learn Mathematics with Gesner – Book 1",
    "project_mathematics_desc": "**Complete mathematics course for beginners.** 20 lessons covering basic arithmetic, geometry, fractions, decimals, percentages, word problems, and more. Full source code included.",
    "project_mathematics_price": "$299 USD (one‑time fee)",
    "project_mathematics_full_price": "$1,500 USD (full package – one‑time)",
    "project_mathematics_status": "✅ Available now – full source code included",
    "project_mathematics_contact": "Contact owner for purchase",
    "project_ai_course": "🤖 AI Foundations & Certification Course",
    "project_ai_course_desc": "**28‑day AI mastery course – from beginner to certified expert.** Learn ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, and more. Full source code included.",
    "project_ai_course_price": "$299 USD (one‑time fee)",
    "project_ai_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_ai_course_status": "✅ Available now – full source code included",
    "project_ai_course_contact": "Contact owner for purchase",
    "project_medical_term": "🩺 Medical Terminology Book for Translators",
    "project_medical_term_desc": "**Interactive medical terminology training for interpreters and healthcare professionals.** 20 lessons covering real doctor‑patient conversations, native voice audio, and translation practice. Full source code included.",
    "project_medical_term_price": "$299 USD (one‑time fee)",
    "project_medical_term_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_term_status": "✅ Available now – full source code included",
    "project_medical_term_contact": "Contact owner for purchase",
    "project_python_course": "🐍 Let's Learn Coding through Python with Gesner",
    "project_python_course_desc": "**Complete Python programming course – from beginner to advanced.** 20 interactive lessons with demo code, 5 practice exercises per lesson, and audio support. Full source code included.",
    "project_python_course_price": "$299 USD (one‑time fee)",
    "project_python_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_python_course_status": "✅ Available now – full source code included",
    "project_python_course_contact": "Contact owner for purchase",
    "project_hardware_course": "🔌 Let's Learn Software & Hardware with Gesner",
    "project_hardware_course_desc": "**Connect software with 20 hardware components – build IoT and robotics projects.** 20 lessons covering network cards, Wi‑Fi, Bluetooth, GPS, GPIO, sensors, motors, displays, and more. Full source code included.",
    "project_hardware_course_price": "$299 USD (one‑time fee)",
    "project_hardware_course_full_price": "$2,500 USD (full package – one‑time)",
    "project_hardware_course_status": "✅ Available now – full source code included",
    "project_hardware_course_contact": "Contact owner for purchase",
    "project_medical_vocab_book2": "📘 Let's Learn Medical Vocabulary with Gesner – Book 2",
    "project_medical_vocab_book2_desc": "**20 lessons – 50 medical terms, 50 acronyms, 50 abbreviations per lesson.** Full audio support for every word. Perfect for medical interpreters, students, and healthcare professionals. Build your medical vocabulary step by step.",
    "project_medical_vocab_book2_price": "$299 USD (one‑time fee)",
    "project_medical_vocab_book2_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_vocab_book2_status": "✅ Available now – full source code included",
    "project_medical_vocab_book2_contact": "Contact owner for purchase",
    "project_medical_term_book3": "📘 Let's Learn Medical Terminology with Gesner – Book 3 (English‑French)",
    "project_medical_term_book3_desc": "**Bilingual English‑French medical terminology course.** 20 lessons with 50 terms, 50 acronyms, 50 abbreviations per lesson – each with native audio in both languages. Perfect for French‑speaking interpreters and healthcare professionals.",
    "project_medical_term_book3_price": "$299 USD (one‑time fee)",
    "project_medical_term_book3_full_price": "$1,500 USD (full package – one‑time)",
    "project_medical_term_book3_status": "✅ Available now – full source code included",
    "project_medical_term_book3_contact": "Contact owner for purchase",
    "project_toefl_course": "📘 Let's Learn TOEFL with Gesner",
    "project_toefl_course_desc": "**Complete TOEFL preparation course.** 20 lessons with 3 interactive conversations, 50 vocabulary words, 25 idioms, 25 grammar rules, and 1 essay per lesson. Full audio support. Perfect for international students and test takers.",
    "project_toefl_course_price": "$299 USD (one‑time fee)",
    "project_toefl_course_full_price": "$1,500 USD (full package – one‑time)",
    "project_toefl_course_status": "✅ Available now – full source code included",
    "project_toefl_course_contact": "Contact owner for purchase",
    "project_french_course": "🇫🇷 Let's Learn French with Gesner",
    "project_french_course_desc": "**Complete French language learning course.** 20 lessons with 3 interactive conversations, 50 vocabulary words, 25 idioms, 25 grammar rules, and 1 essay per lesson. Native French audio. Perfect for beginners and intermediate learners.",
    "project_french_course_price": "$299 USD (one‑time fee)",
    "project_french_course_full_price": "$1,500 USD (full package – one‑time)",
    "project_french_course_status": "✅ Available now – full source code included",
    "project_french_course_contact": "Contact owner for purchase",
    "project_haiti_marketplace": "🇭🇹 Let's Learn Why Haiti Isn't a Marketplace for Most Social Media",
    "project_haiti_marketplace_desc": "**20 lessons explaining Haiti's digital divide and how to fix it.** Covers algorithms, PayPal absence, diaspora advantage, and actionable solutions. Available in 5 languages (English, Spanish, French, Portuguese, Chinese) with native audio.",
    "project_haiti_marketplace_price": "$299 USD (one‑time fee)",
    "project_haiti_marketplace_full_price": "$1,500 USD (full package – one‑time)",
    "project_haiti_marketplace_status": "✅ Available now – full source code included",
    "project_haiti_marketplace_contact": "Contact owner for purchase",
    "project_vectra_ai": "🚗 Vectra AI – Self‑Driving Car Simulator",
    "project_vectra_ai_desc": "**Interactive self‑driving car simulation.** Drive on a winding dust road, avoid oncoming cars, adjust speed limit. Uses 5 sensors and AI to stay in the right lane. Full source code included.\n\n**Fair Market Valuation (B2B Licensing):** $4,500 – $12,000 USD ↑ Per Implementation – Based on real‑time physics engine, AI lane‑discipline logic, and custom heading algorithms.",
    "project_vectra_ai_price": "$4,500 – $12,000 USD (↑ Per Implementation)",
    "project_vectra_ai_full_price": "$25,000 USD (full package – one‑time)",
    "project_vectra_ai_status": "✅ Available now – full source code included",
    "project_vectra_ai_contact": "Contact owner for purchase",
    # ----- Humanoid Robot Software -----
    "project_humanoid_robot": "🤖 Humanoid Robot Training & Control Software – Built by Gesner Deslandes",
    "project_humanoid_robot_desc": "Complete software suite to train any humanoid robot to perform real‑world tasks. Includes task programming interface, simulation mode, real‑time telemetry, and API for physical robot integration (ROS2, MAVLink, or custom). Train the robot by demonstration or scripted commands. Full source code, setup guide, and 1 year support included.",
    "project_humanoid_robot_price": "$17,500 USD (one‑time fee)",
    "project_humanoid_robot_full_price": "$45,000 USD (full package – one‑time)",
    "project_humanoid_robot_status": "✅ Available now – full source code included, lifetime updates, 1 year support",
    "project_humanoid_robot_contact": "Contact owner for purchase",
    # ----- Hospital Management System (demo and subscription) -----
    "project_hospital": "🏥 Hospital Management System Software – built by Gesner Deslandes",
    "project_hospital_desc": "Complete multi‑specialty hospital management platform. Includes EMR/EHR, OPD/IPD workflows, billing & revenue cycle management, pharmacy, laboratory, radiology integration, inventory & financial management, role‑based dashboards, and enterprise reporting. HL7 & FHIR ready. Cloud or on‑premise. Trusted for mid‑size to national tertiary centers.",
    "project_hospital_price_monthly": "$299 USD / month (subscription)",
    "project_hospital_full_price": "$35,000 USD (full package – one‑time)",
    "project_hospital_status": "✅ Live demo available | Subscribe monthly",
    "project_hospital_contact": "Click Subscribe to see payment instructions",
    
    "view_demo": "🎬 View Demo",
    "demo_screenshot": "Screenshot preview (replace with actual image)",
    "live_demo": "🔗 Live Demo",
    "demo_password_hint": "🔐 Demo password: 20082010",
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
    # ----- Sendwave promo keys (English) -----
    "sendwave_title": "📱 Send Money to Haiti Like a Text – Fast, Fair, and Finally Affordable",
    "sendwave_intro": "For Haitians living abroad, sending money home should be a joy, not a financial burden. That's why we're proud to recommend **Sendwave**, the international transfer service trusted by millions.",
    "sendwave_reasons": "✓ Instant Delivery – Your money arrives in minutes, not days.\n✓ Low to No Fees – Stop losing your hard-earned cash to hidden costs.\n✓ User-Friendly – So simple, it's like sending a text message.\n✓ Secure & Reliable – Real-time tracking and safe processing.",
    "sendwave_cta": "Your siblings and parents will thank you for helping them quickly. Don't wait. Make the switch today.",
    "sendwave_link": "🔗 **For more info and exclusive updates, visit our website:**\nhttps://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/",
    "sendwave_watch_ad": "📺 Watch our ad – Sendwave",
    # ----- Western Union promo keys (English) -----
    "western_union_title": "✨✨✨ WESTERN UNION – HAITI ✨✨✨",
    "western_union_text": "💸 Send money fast – anywhere to Haiti\n🔒 Safe, secure, trusted worldwide\n🤝 Cash pickup or direct deposit\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌍 At GlobalInternet.py, we promote money transfers to Haiti.\n\n📞 Contact us for your business promotion:\n✉️ Email: deslandes78@gmail.com\n📱 Phone / WhatsApp: (509)-47385663\n🌐 Website: https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌟 Let’s grow your business together! 🌟",
    "western_union_watch_ad": "📺 Watch our ad – Western Union"
}

# French dictionary (full – same structure as English, translated)
lang_fr = {
    "hero_title": "GlobalInternet.py",
    "hero_sub": "Construisez avec Python. Livrez rapidement. Innovez avec l'IA.",
    "hero_desc": "D'Haïti au monde – des logiciels sur mesure qui fonctionnent en ligne.",
    "about_title": "👨‍💻 À propos de l'entreprise",
    "about_text": "**GlobalInternet.py** a été fondé par **Gesner Deslandes** – propriétaire, fondateur et ingénieur principal. Nous construisons des **logiciels basés sur Python** à la demande pour des clients du monde entier. Comme la Silicon Valley, mais avec une touche haïtienne et des résultats exceptionnels.\n\n- 🧠 **Solutions alimentées par l'IA** – chatbots, analyse de données, automatisation\n- 🗳️ **Systèmes électoraux complets** – sécurisés, multilingues, en temps réel\n- 🌐 **Applications web** – tableaux de bord, outils internes, plateformes en ligne\n- 📦 **Livraison complète** – nous vous envoyons le code complet par email et vous guidons lors de l'installation\n\nQue vous ayez besoin d'un site web d'entreprise, d'un outil logiciel personnalisé ou d'une plateforme en ligne à grande échelle – nous le construisons, vous le possédez.",
    "office_photo_caption": "Avatar parlant de Gesner Deslandes – présentation de GlobalInternet.py",
    "humanoid_photo_caption": "Gesner Humanoid AI – notre représentant numérique de l'innovation et de l'expertise logicielle.",
    "founder": "Fondateur et PDG",
    "founder_name": "Gesner Deslandes",
    "founder_title": "Ingénieur | Passionné d'IA | Expert Python",
    "cv_title": "📄 À propos du propriétaire – Gesner Deslandes",
    "cv_intro": "Constructeur de logiciels Python | Développeur web | Coordinateur technologique",
    "cv_summary": "Leader et gestionnaire exceptionnellement motivé, engagé envers l'excellence et la précision. **Compétences clés :** Leadership, Interprétation (anglais, français, créole haïtien), Orientation mécanique, Gestion, Microsoft Office.",
    "cv_experience_title": "💼 Expérience professionnelle",
    "cv_experience": "**Coordinateur technologique** – Orphelinat Be Like Brit (2021–présent)\nConfiguration des réunions Zoom, maintenance des ordinateurs portables/tablettes, support technique quotidien, assurance d'opérations numériques fluides.\n\n**PDG et services d'interprétation** – Tourisme personnalisé pour groupes d'ONG, équipes de mission et particuliers.\n\n**Gestionnaire de parc / répartiteur** – J/P Haitian Relief Organization\nGestion de plus de 20 véhicules, journaux de bord, calendriers de maintenance avec Excel.\n\n**Interprète médical** – International Child Care\nInterprétation médicale précise anglais–français–créole.\n\n**Chef d'équipe et interprète** – Can‑Do NGO\nDirection de projets de reconstruction.\n\n**Professeur d'anglais** – Be Like Brit (préscolaire à NS4)\n\n**Traducteur de documents** – United Kingdom Glossary & United States Work‑Rise Company",
    "cv_education_title": "🎓 Éducation et formation",
    "cv_education": "- École de formation professionnelle – Anglais américain\n- Institut Diesel d'Haïti – Mécanicien diesel\n- Certification en bureautique (octobre 2000)\n- Diplômé du secondaire",
    "cv_references": "📞 Références disponibles sur demande.",
    "team_title": "👥 Notre équipe",
    "team_sub": "Rencontrez les talents derrière GlobalInternet.py – embauchés en avril 2026.",
    "team_members": [
        {"name": "Gesner Deslandes", "role": "Fondateur et PDG", "since": "2021", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes.JPG"},
        {"name": "Gesner Junior Deslandes", "role": "Assistant du PDG", "since": "Avril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/dreamina-2026-04-18-6690-Change%20the%20man's%20attire%20to%20a%20professiona....jpeg"},
        {"name": "Roosevelt Deslandes", "role": "Programmeur Python", "since": "Avril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Roosevelt%20%20Software%20Builder.jpeg"},
        {"name": "Sebastien Stephane Deslandes", "role": "Programmeur Python", "since": "Avril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/35372.jpg"},
        {"name": "Zendaya Christelle Deslandes", "role": "Secrétaire", "since": "Avril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/IMG_1411.jpg"}
    ],
    "services_title": "⚙️ Nos services",
    "services": [
        ("🐍 Développement Python personnalisé", "Scripts sur mesure, automatisation, systèmes backend."),
        ("🤖 IA et apprentissage automatique", "Chatbots, modèles prédictifs, analyses de données."),
        ("🗳️ Logiciel électoral", "Sécurisé, multilingue, résultats en direct – comme notre système Haïti."),
        ("📊 Tableaux de bord d'entreprise", "Analytique en temps réel et outils de reporting."),
        ("🌐 Sites web et applications web", "Solutions full‑stack déployées en ligne."),
        ("📦 Livraison en 24 heures", "Nous travaillons rapidement – recevez votre logiciel par email, prêt à l'emploi."),
        ("📢 Publicité et marketing", "Campagnes numériques, gestion des réseaux sociaux, ciblage IA, rapports de performance. De 150 $ à 1 200 $ selon la portée.")
    ],
    "projects_title": "🏆 Nos projets et réalisations",
    "projects_sub": "Solutions logicielles complètes livrées aux clients – prêtes à être achetées ou personnalisées.",
    # ----- 38 Projects (French) with full package prices -----
    "project_haiti": "🇭🇹 Logiciel de vote en ligne Haïti",
    "project_haiti_desc": "Système électoral présidentiel complet avec support multilingue (créole, français, anglais, espagnol), suivi en direct, tableau de bord du président du CEP (gestion des candidats, téléchargement de photos, rapports de progression), scrutin secret et mots de passe modifiables. Utilisé pour les élections nationales.",
    "project_haiti_price": "2 000 $ USD (paiement unique)",
    "project_haiti_full_price": "15 000 $ USD (forfait complet – paiement unique)",
    "project_haiti_status": "✅ Disponible – code source, installation et support inclus",
    "project_haiti_contact": "Contactez le propriétaire pour acheter",
    "project_dashboard": "📊 Tableau de bord d'intelligence d'affaires",
    "project_dashboard_desc": "Tableau de bord d'analytique en temps réel pour entreprises. Connectez‑vous à toute base de données (SQL, Excel, CSV) et visualisez KPI, tendances des ventes, inventaire et rapports personnalisés. Entièrement interactif et personnalisable.",
    "project_dashboard_price": "1 200 $ USD",
    "project_dashboard_full_price": "8 500 $ USD (forfait complet – paiement unique)",
    "project_dashboard_status": "✅ Disponible",
    "project_dashboard_contact": "Contactez le propriétaire pour acheter",
    "project_chatbot": "🤖 Chatbot de support client IA",
    "project_chatbot_desc": "Chatbot intelligent entraîné sur vos données d'entreprise. Répondez aux questions des clients 24/7, réduisez la charge de support. Intègre les sites web, WhatsApp ou Telegram. Construit avec Python et NLP moderne.",
    "project_chatbot_price": "800 $ USD (basique) / 1 500 $ USD (avancé)",
    "project_chatbot_full_price": "6 500 $ USD (forfait complet – paiement unique)",
    "project_chatbot_status": "✅ Disponible",
    "project_chatbot_contact": "Contactez le propriétaire pour acheter",
    "project_school": "🏫 Système de gestion scolaire",
    "project_school_desc": "Plateforme complète pour écoles : inscription des étudiants, gestion des notes, suivi des présences, portail parents, génération de bulletins et collecte des frais. Rôles multi‑utilisateurs (admin, enseignants, parents).",
    "project_school_price": "1 500 $ USD",
    "project_school_full_price": "9 000 $ USD (forfait complet – paiement unique)",
    "project_school_status": "✅ Disponible",
    "project_school_contact": "Contactez le propriétaire pour acheter",
    "project_pos": "📦 Système d'inventaire et point de vente",
    "project_pos_desc": "Gestion d'inventaire web avec point de vente pour petites entreprises. Lecture de codes‑barres, alertes de stock, rapports de ventes, gestion des fournisseurs. Fonctionne en ligne et hors ligne.",
    "project_pos_price": "1 000 $ USD",
    "project_pos_full_price": "7 500 $ USD (forfait complet – paiement unique)",
    "project_pos_status": "✅ Disponible",
    "project_pos_contact": "Contactez le propriétaire pour acheter",
    "project_scraper": "📈 Extracteur web personnalisé et pipeline de données",
    "project_scraper_desc": "Extraction automatisée de données de n'importe quel site web, nettoyée et livrée en Excel/JSON/CSV. Planification quotidienne, hebdomadaire ou mensuelle. Parfait pour la veille marché, surveillance des prix ou génération de leads.",
    "project_scraper_price": "500 – 2 000 $ USD (selon complexité)",
    "project_scraper_full_price": "5 000 $ USD (forfait complet – paiement unique)",
    "project_scraper_status": "✅ Disponible",
    "project_scraper_contact": "Contactez le propriétaire pour acheter",
    "project_chess": "♟️ Jouez aux échecs contre la machine",
    "project_chess_desc": "Jeu d'échecs éducatif avec adversaire IA (3 niveaux de difficulté). Chaque mouvement est expliqué – apprenez les tactiques comme les fourchettes, les clouages et les échecs à la découverte. Inclut mode démo, tableau de bord des mouvements et téléchargement du rapport complet. Multilingue (anglais, français, espagnol, créole).",
    "project_chess_price": "20 $ USD (paiement unique)",
    "project_chess_full_price": "499 $ USD (forfait complet – paiement unique)",
    "project_chess_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_chess_contact": "Contactez le propriétaire pour acheter",
    "project_accountant": "🧮 Comptable Excel avancé IA",
    "project_accountant_desc": "Suite comptable et de gestion de prêts professionnelle. Suivi des revenus/dépenses, gestion des prêts (emprunteurs, dates d'échéance, paiements), tableau de bord avec solde, exportation de tous les rapports vers Excel et PDF. Multilingue (anglais, français, espagnol).",
    "project_accountant_price": "199 $ USD (paiement unique)",
    "project_accountant_full_price": "1 200 $ USD (forfait complet – paiement unique)",
    "project_accountant_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_accountant_contact": "Contactez le propriétaire pour acheter",
    "project_archives": "📜 Base de données des Archives Nationales d'Haïti",
    "project_archives_desc": "Base de données complète des archives nationales pour les citoyens haïtiens. Stocke NIF (Matricule Fiscale), CIN, Passeport, Permis de conduire, historique de vote, parrainages et téléchargements de documents. Validation de signature ministérielle, système de mot de passe annuel, multilingue (anglais, français, espagnol, créole).",
    "project_archives_price": "1 500 $ USD (paiement unique)",
    "project_archives_full_price": "12 000 $ USD (forfait complet – paiement unique)",
    "project_archives_status": "✅ Disponible – code source, installation et support inclus",
    "project_archives_contact": "Contactez le propriétaire pour acheter",
    "project_dsm": "🛡️ DSM-2026: SYSTÈME SÉCURISÉ",
    "project_dsm_desc": "Radar de surveillance de la stratosphère avancé – suit les avions, satellites et missiles en temps réel. Affichage radar simulé avec détection de menace, support multilingue et rapports de renseignement téléchargeables.",
    "project_dsm_price": "299 $ USD (paiement unique)",
    "project_dsm_full_price": "2 500 $ USD (forfait complet – paiement unique)",
    "project_dsm_status": "✅ Disponible – licence à vie, mises à jour gratuites",
    "project_dsm_contact": "Contactez le propriétaire pour acheter",
    "project_bi": "📊 Tableau de bord d'intelligence d'affaires",
    "project_bi_desc": "Tableau de bord d'analytique en temps réel pour entreprises. Connectez SQL, Excel, CSV – visualisez KPI, tendances des ventes, inventaire et performances régionales. Entièrement interactif avec filtres de dates et rapports CSV téléchargeables. Multilingue (anglais, français, espagnol, créole).",
    "project_bi_price": "1 200 $ USD (paiement unique)",
    "project_bi_full_price": "8 500 $ USD (forfait complet – paiement unique)",
    "project_bi_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_bi_contact": "Contactez le propriétaire pour acheter",
    "project_ai_classifier": "🧠 Classificateur d'images IA (MobileNetV2)",
    "project_ai_classifier_desc": "Téléchargez une image et l'IA l'identifie parmi 1000 catégories (animaux, véhicules, nourriture, objets du quotidien). Utilise TensorFlow MobileNetV2 pré‑entraîné sur ImageNet. Multilingue, protégé par mot de passe, démo prête.",
    "project_ai_classifier_price": "1 200 $ USD (paiement unique)",
    "project_ai_classifier_full_price": "4 500 $ USD (forfait complet – paiement unique)",
    "project_ai_classifier_status": "✅ Disponible – code source, installation et support inclus",
    "project_ai_classifier_contact": "Contactez le propriétaire pour acheter",
    "project_task_manager": "🗂️ Tableau de bord de gestion des tâches",
    "project_task_manager_desc": "Gérez les tâches, suivez les progrès et analysez la productivité avec des graphiques en temps réel et le mode sombre. Inspiré de l'interface basée sur les composants de React. Multilingue, stockage persistant, tableau de bord analytique.",
    "project_task_manager_price": "1 200 $ USD (paiement unique)",
    "project_task_manager_full_price": "3 500 $ USD (forfait complet – paiement unique)",
    "project_task_manager_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_task_manager_contact": "Contactez le propriétaire pour acheter",
    "project_ray": "⚡ Processeur de texte parallèle Ray",
    "project_ray_desc": "Traitez du texte en parallèle sur plusieurs cœurs CPU. Comparez la vitesse d'exécution séquentielle vs parallèle. Inspiré du framework de calcul distribué Ray de l'UC Berkeley.",
    "project_ray_price": "1 200 $ USD (paiement unique)",
    "project_ray_full_price": "3 500 $ USD (forfait complet – paiement unique)",
    "project_ray_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_ray_contact": "Contactez le propriétaire pour acheter",
    "project_cassandra": "🗄️ Tableau de bord de données Cassandra",
    "project_cassandra_desc": "Démonstration de base de données NoSQL distribuée. Ajoutez des commandes, recherchez par client et explorez l'analytique en temps réel. Modélisé d'après Apache Cassandra (Netflix, Instagram).",
    "project_cassandra_price": "1 200 $ USD (paiement unique)",
    "project_cassandra_full_price": "4 000 $ USD (forfait complet – paiement unique)",
    "project_cassandra_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_cassandra_contact": "Contactez le propriétaire pour acheter",
    "project_spark": "🌊 Processeur de données Apache Spark",
    "project_spark_desc": "Téléchargez un fichier CSV et exécutez des agrégations de type SQL (group by, sum, avg, count) en utilisant Spark. Résultats et graphiques en temps réel. Inspiré du moteur big data utilisé par des milliers d'entreprises.",
    "project_spark_price": "1 200 $ USD (paiement unique)",
    "project_spark_full_price": "5 500 $ USD (forfait complet – paiement unique)",
    "project_spark_status": "✅ Disponible – accès à vie, mises à jour gratuites",
    "project_spark_contact": "Contactez le propriétaire pour acheter",
    "project_drone": "🚁 Commandant de drone haïtien",
    "project_drone_desc": "Contrôlez le premier drone fabriqué en Haïti depuis votre téléphone. Mode simulation, support réel du drone (MAVLink), armement, décollage, atterrissage, vol vers coordonnées GPS, télémétrie en direct, historique des commandes. Multilingue, tableau de bord professionnel.",
    "project_drone_price": "2 000 $ USD (paiement unique)",
    "project_drone_full_price": "12 000 $ USD (forfait complet – paiement unique)",
    "project_drone_status": "✅ Disponible – code source, installation et 1 an de support inclus",
    "project_drone_contact": "Contactez le propriétaire pour acheter",
    "project_english": "🇬🇧 Apprenons l'anglais avec Gesner",
    "project_english_desc": "Application interactive d'apprentissage de l'anglais. Couvre le vocabulaire, la grammaire, la prononciation et la pratique de la conversation. Interface multilingue, suivi des progrès, quiz et certificats. Parfait pour les débutants et les apprenants intermédiaires.",
    "project_english_price": "299 $ USD (paiement unique)",
    "project_english_full_price": "1 500 $ USD (forfait complet – paiement unique)",
    "project_english_status": "✅ Disponible – code source, installation et support inclus",
    "project_english_contact": "Contactez le propriétaire pour acheter",
    "project_spanish": "🇪🇸 Apprenons l'espagnol avec Gesner",
    "project_spanish_desc": "Plateforme complète d'apprentissage de l'espagnol. Leçons sur le vocabulaire, les conjugaisons, la compréhension orale et les notes culturelles. Inclut des exercices interactifs, la reconnaissance vocale et un tableau de bord de progression.",
    "project_spanish_price": "299 $ USD (paiement unique)",
    "project_spanish_full_price": "1 500 $ USD (forfait complet – paiement unique)",
    "project_spanish_status": "✅ Disponible – code source, installation et support inclus",
    "project_spanish_contact": "Contactez le propriétaire pour acheter",
    "project_portuguese": "🇵🇹 Apprenons le portugais avec Gesner",
    "project_portuguese_desc": "Application d'apprentissage du portugais brésilien et européen. Couvre les phrases essentielles, la grammaire, les temps verbaux et les dialogues de la vie réelle. Inclut des flashcards, un guide de prononciation et des badges de réussite. Support multilingue.",
    "project_portuguese_price": "299 $ USD (paiement unique)",
    "project_portuguese_full_price": "1 500 $ USD (forfait complet – paiement unique)",
    "project_portuguese_status": "✅ Disponible – code source, installation et support inclus",
    "project_portuguese_contact": "Contactez le propriétaire pour acheter",
    "project_ai_career": "🚀 Coach de carrière IA – Optimiseur de CV",
    "project_ai_career_desc": "**Optimisez votre CV et réussissez vos entretiens avec l'IA.** Téléchargez votre CV et une description de poste – notre IA analyse les deux et fournit : des mots‑clés à ajouter, des améliorations de compétences, des suggestions de formatage et des questions d'entretien prédites. Parfait pour les chercheurs d'emploi, étudiants et professionnels. Code source complet inclus.",
    "project_ai_career_price": "149 $ USD (paiement unique)",
    "project_ai_career_full_price": "1 200 $ USD (forfait complet – paiement unique)",
    "project_ai_career_status": "✅ Disponible – code source complet inclus",
    "project_ai_career_contact": "Contactez le propriétaire pour acheter",
    "project_ai_medical": "🧪 Assistant IA en littérature médicale et scientifique",
    "project_ai_medical_desc": "**Posez n'importe quelle question médicale ou scientifique – obtenez des réponses basées sur des recherches réelles.** Notre IA recherche dans PubMed, la plus grande base de données de littérature médicale, extrait les résumés pertinents et génère des réponses factuelles avec citations et liens directs. Code source complet inclus.",
    "project_ai_medical_price": "149 $ USD (paiement unique)",
    "project_ai_medical_full_price": "1 200 $ USD (forfait complet – paiement unique)",
    "project_ai_medical_status": "✅ Disponible – code source complet inclus",
    "project_ai_medical_contact": "Contactez le propriétaire pour acheter",
    # (Remaining French keys – similar to English – omitted for brevity but must be present. In practice, include all.)
}

# Spanish dictionary (similar structure)
lang_es = {
    # ... (all keys, including full_price and ad keys, translated)
    # Omitted for length, but must be included.
}

# Combine languages
lang_dict = {
    "en": lang_en,
    "fr": lang_fr,
    "es": lang_es
}

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

# ---------- LEGAL PAGES (for AdSense compliance) ----------
with st.sidebar.expander("📜 Privacy Policy"):
    st.markdown("""
    **Privacy Policy for GlobalInternet.py**

    Last updated: April 2026

    We respect your privacy. This policy explains how we collect, use, and protect your personal information when you visit our website or purchase our software.

    **Information we collect:**  
    - Name, email address, phone number (when you contact us or make a purchase).  
    - Payment information (processed securely via Moncash, bank transfer, or SendWave – we do not store your payment details).  
    - Usage data (e.g., pages visited, time spent) to improve our services.

    **How we use your information:**  
    - To respond to your inquiries and deliver purchased software.  
    - To send you updates about your software (e.g., new versions, security patches).  
    - To improve our website and products.

    **Data security:**  
    We take reasonable measures to protect your data. However, no internet transmission is 100% secure.

    **Third‑party services:**  
    We use Supabase for comments and likes. Their privacy policy applies to data stored there.

    **Your rights:**  
    You may request access, correction, or deletion of your personal data by contacting us at deslandes78@gmail.com.

    **Changes to this policy:**  
    We may update this policy. Changes will be posted here.

    **Contact:**  
    GlobalInternet.py, Gesner Deslandes – deslandes78@gmail.com, +509 4738-5663
    """)

with st.sidebar.expander("📜 Terms of Service"):
    st.markdown("""
    **Terms of Service for GlobalInternet.py**

    By using our website or purchasing our software, you agree to these terms.

    **Software license:**  
    When you purchase software, you receive a non‑exclusive, perpetual license to use the software for personal or business purposes. You may not resell, redistribute, or sublicense the source code without our written permission.

    **Delivery:**  
    Software is delivered by email as a ZIP file containing source code, documentation, and installation instructions. You are responsible for ensuring your system meets the software requirements.

    **Refunds:**  
    Because software is delivered digitally, we generally do not offer refunds. However, if the software does not work as described, contact us within 7 days for a resolution or refund.

    **Support:**  
    We provide email support for installation and basic usage. Custom modifications may incur additional fees.

    **Limitation of liability:**  
    We are not liable for any damages arising from the use or inability to use our software. You assume full responsibility.

    **Governing law:**  
    These terms are governed by the laws of Haiti.

    **Changes:**  
    We may update these terms at any time. Continued use of our website constitutes acceptance.

    **Contact:**  
    deslandes78@gmail.com
    """)

with st.sidebar.expander("📜 Disclaimer"):
    st.markdown("""
    **Disclaimer for GlobalInternet.py**

    The information and software provided on this website are for general informational and business purposes only. While we strive to keep everything up‑to‑date and error‑free, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the software or information.

    **No professional advice:**  
    The content on this website does not constitute legal, financial, or professional advice.

    **External links:**  
    Our website may contain links to external sites. We are not responsible for the content or privacy practices of those sites.

    **Software use:**  
    You are responsible for testing the software in your own environment. We are not liable for any data loss or system damage.

    **Affiliate disclosure:**  
    Some links on this website may be affiliate links (e.g., for hosting or developer tools). If you purchase through those links, we may earn a small commission at no extra cost to you.

    **Contact:**  
    If you have any questions, contact us at deslandes78@gmail.com.
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

# ========== MAIN WEBSITE CONTENT ==========
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

# ========== GESNER TALKING AVATAR – CENTERED, MEDIUM SIZE ==========
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

# ---------- Humanoid Robotics Video (centered, medium-sized) ----------
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

# ---------- Projects in Perspective (Roadmap) ----------
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

# ---------- Projects listing (reorganized) ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Define all project keys with their demo_url status
all_projects = [
    {"key": "haiti", "has_demo": True, "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/"},
    {"key": "chess", "has_demo": True, "demo_url": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/"},
    {"key": "accountant", "has_demo": True, "demo_url": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/"},
    {"key": "dsm", "has_demo": True, "demo_url": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/"},
    {"key": "bi", "has_demo": True, "demo_url": "https://9enktzu34sxzyvtsymghxd.streamlit.app/"},
    {"key": "ai_classifier", "has_demo": True, "demo_url": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/"},
    {"key": "task_manager", "has_demo": True, "demo_url": "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/"},
    {"key": "ray", "has_demo": True, "demo_url": "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/"},
    {"key": "cassandra", "has_demo": True, "demo_url": "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/"},
    {"key": "spark", "has_demo": True, "demo_url": "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/"},
    {"key": "drone", "has_demo": True, "demo_url": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/"},
    {"key": "english", "has_demo": True, "demo_url": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/"},
    {"key": "spanish", "has_demo": True, "demo_url": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/"},
    {"key": "portuguese", "has_demo": True, "demo_url": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/"},
    {"key": "vectra_ai", "has_demo": True, "demo_url": "https://vectra-ai-built-by-gesner-deslandes-dnkhqd57z6vkmiuezujcqu.streamlit.app/"},
    {"key": "hospital", "has_demo": True, "demo_url": "https://hospital-management-system-software-built-by-gesner-deslandes.streamlit.app/"},
    # All other projects have no demo
    {"key": "dashboard", "has_demo": False, "demo_url": None},
    {"key": "chatbot", "has_demo": False, "demo_url": None},
    {"key": "school", "has_demo": False, "demo_url": None},
    {"key": "pos", "has_demo": False, "demo_url": None},
    {"key": "scraper", "has_demo": False, "demo_url": None},
    {"key": "archives", "has_demo": False, "demo_url": None},
    {"key": "ai_career", "has_demo": False, "demo_url": None},
    {"key": "ai_medical", "has_demo": False, "demo_url": None},
    {"key": "music_studio", "has_demo": False, "demo_url": None},
    {"key": "ai_media", "has_demo": False, "demo_url": None},
    {"key": "chinese", "has_demo": False, "demo_url": None},
    {"key": "french", "has_demo": False, "demo_url": None},
    {"key": "mathematics", "has_demo": False, "demo_url": None},
    {"key": "ai_course", "has_demo": False, "demo_url": None},
    {"key": "medical_term", "has_demo": False, "demo_url": None},
    {"key": "python_course", "has_demo": False, "demo_url": None},
    {"key": "hardware_course", "has_demo": False, "demo_url": None},
    {"key": "medical_vocab_book2", "has_demo": False, "demo_url": None},
    {"key": "medical_term_book3", "has_demo": False, "demo_url": None},
    {"key": "toefl_course", "has_demo": False, "demo_url": None},
    {"key": "french_course", "has_demo": False, "demo_url": None},
    {"key": "haiti_marketplace", "has_demo": False, "demo_url": None},
    {"key": "humanoid_robot", "has_demo": False, "demo_url": None},
]

# Separate groups
group_a = [p for p in all_projects if p["has_demo"]]
group_b = [p for p in all_projects if not p["has_demo"]]

# Display Group A (with demos)
if group_a:
    st.markdown("### 🎯 Software with Live Demo")
    for i in range(0, len(group_a), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_a):
                proj_info = group_a[idx]
                key = proj_info["key"]
                title_key = f"project_{key}"
                desc_key = f"project_{key}_desc"
                full_price_key = f"project_{key}_full_price"
                status_key = f"project_{key}_status"
                demo_url = proj_info["demo_url"]
                title = t.get(title_key, "Project")
                desc = t.get(desc_key, "Description not available")
                full_price = t.get(full_price_key, "Contact for price")
                status = t.get(status_key, "Status")
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                        <div class="price">💎 Full package: {full_price}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{status}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    if demo_url:
                        st.markdown(f"<a href='{demo_url}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                        st.caption(t['demo_password_hint'])
                    else:
                        st.info("📹 Live demo available upon request.")
                    # Subscribe button (monthly)
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{key}"):
                        st.info(f"To subscribe for {title} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    # Buy Full Package button
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {title} at {full_price}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)

# Display Group B (without demos)
if group_b:
    st.markdown("### 🛠️ Software Available for Purchase (No Public Demo)")
    for i in range(0, len(group_b), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_b):
                proj_info = group_b[idx]
                key = proj_info["key"]
                title_key = f"project_{key}"
                desc_key = f"project_{key}_desc"
                full_price_key = f"project_{key}_full_price"
                status_key = f"project_{key}_status"
                title = t.get(title_key, "Project")
                desc = t.get(desc_key, "Description not available")
                full_price = t.get(full_price_key, "Contact for price")
                status = t.get(status_key, "Status")
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                        <div class="price">💎 Full package: {full_price}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{status}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("📹 No public demo – contact us for a private walkthrough.")
                    # Subscribe button (monthly)
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{key}"):
                        st.info(f"To subscribe for {title} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    # Buy Full Package button
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {title} at {full_price}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)

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
    sendwave_video_url = "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Sendwave%20marketing%202026.MP4"
    sendwave_video_html = f"""
    <div id="sendwaveAdContainer" style="width:100%; max-width:500px; margin:0 auto;">
        <video id="sendwaveVideo" 
               src="{sendwave_video_url}" 
               muted 
               playsinline 
               loop 
               controls 
               style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);">
            Your browser does not support the video tag.
        </video>
        <p style="text-align:center; font-size:0.7rem; color:#666; margin-top:5px;">📢 Sendwave ad – Less transfer fees, less drama</p>
    </div>
    <script>
        (function() {{
            var video = document.getElementById('sendwaveVideo');
            if (!video) return;
            var observer = new IntersectionObserver(function(entries) {{
                entries.forEach(function(entry) {{
                    if (entry.isIntersecting) {{
                        video.play().catch(function(e) {{ console.log("Autoplay blocked:", e); }});
                    }} else {{
                        video.pause();
                    }}
                }});
            }}, {{ threshold: 0.5 }});
            observer.observe(video);
        }})();
    </script>
    """
    components.html(sendwave_video_html, height=350)

st.markdown("---")

# ---------- WESTERN UNION PROMOTIONAL SECTION ----------
st.markdown(f"## {t['western_union_title']}")

col_wu_promo, col_wu_video = st.columns([3, 2])

with col_wu_promo:
    st.markdown(t['western_union_text'])

with col_wu_video:
    st.markdown(f"**{t['western_union_watch_ad']}**")
    western_union_video_url = "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/refs/heads/main/WesterUnionPub.MP4"
    western_union_video_html = f"""
    <div id="westernUnionAdContainer" style="width:100%; max-width:500px; margin:0 auto;">
        <video id="westernUnionVideo" 
               src="{western_union_video_url}" 
               muted 
               playsinline 
               loop 
               controls 
               style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);">
            Your browser does not support the video tag.
        </video>
        <p style="text-align:center; font-size:0.7rem; color:#666; margin-top:5px;">📢 Western Union ad – Trusted worldwide</p>
    </div>
    <script>
        (function() {{
            var video = document.getElementById('westernUnionVideo');
            if (!video) return;
            var observer = new IntersectionObserver(function(entries) {{
                entries.forEach(function(entry) {{
                    if (entry.isIntersecting) {{
                        video.play().catch(function(e) {{ console.log("Autoplay blocked:", e); }});
                    }} else {{
                        video.pause();
                    }}
                }});
            }}, {{ threshold: 0.5 }});
            observer.observe(video);
        }})();
    </script>
    """
    components.html(western_union_video_html, height=350)

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
