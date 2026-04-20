import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from supabase import create_client, Client

# ---------- Supabase setup ----------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="GlobalInternet.py – Python Software Company", page_icon="🌐", layout="wide")

# ---------- Functions for comments & likes (table "comments") ----------
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
        # Try to increment using RPC (requires a function in Supabase)
        supabase.rpc("increment_likes", {"row_id": comment_id}).execute()
    except:
        # Fallback: read and update
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
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP: {visitor_ip}\nUser Agent: {user_agent}"
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

if "notification_sent" not in st.session_state:
    send_visit_notification()
    st.session_state.notification_sent = True

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

# ---------- English dictionary (full) ----------
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
    # Project 1
    "project_haiti": "🇭🇹 Haiti Online Voting Software",
    "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
    "project_haiti_price": "$2,000 USD (one‑time fee)",
    "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
    "project_haiti_contact": "Contact owner for purchase",
    # Project 2
    "project_dashboard": "📊 Business Intelligence Dashboard",
    "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
    "project_dashboard_price": "$1,200 USD",
    "project_dashboard_status": "✅ Available now",
    "project_dashboard_contact": "Contact owner for purchase",
    # Project 3
    "project_chatbot": "🤖 AI Customer Support Chatbot",
    "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
    "project_chatbot_price": "$800 USD (basic) / $1,500 USD (advanced)",
    "project_chatbot_status": "✅ Available now",
    "project_chatbot_contact": "Contact owner for purchase",
    # Project 4
    "project_school": "🏫 School Management System",
    "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
    "project_school_price": "$1,500 USD",
    "project_school_status": "✅ Available now",
    "project_school_contact": "Contact owner for purchase",
    # Project 5
    "project_pos": "📦 Inventory & POS System",
    "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
    "project_pos_price": "$1,000 USD",
    "project_pos_status": "✅ Available now",
    "project_pos_contact": "Contact owner for purchase",
    # Project 6
    "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
    "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
    "project_scraper_price": "$500 – $2,000 (depends on complexity)",
    "project_scraper_status": "✅ Available now",
    "project_scraper_contact": "Contact owner for purchase",
    # Project 7
    "project_chess": "♟️ Play Chess Against the Machine",
    "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
    "project_chess_price": "$20 USD (one‑time fee)",
    "project_chess_status": "✅ Available now – lifetime access, free updates",
    "project_chess_contact": "Contact owner for purchase",
    # Project 8
    "project_accountant": "🧮 Accountant Excel Advanced AI",
    "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
    "project_accountant_price": "$199 USD (one‑time fee)",
    "project_accountant_status": "✅ Available now – lifetime access, free updates",
    "project_accountant_contact": "Contact owner for purchase",
    # Project 9
    "project_archives": "📜 Haiti Archives Nationales Database",
    "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
    "project_archives_price": "$1,500 USD (one‑time fee)",
    "project_archives_status": "✅ Available now – includes source code, setup, and support",
    "project_archives_contact": "Contact owner for purchase",
    # Project 10
    "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
    "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
    "project_dsm_price": "$299 USD (one‑time fee)",
    "project_dsm_status": "✅ Available now – lifetime license, free updates",
    "project_dsm_contact": "Contact owner for purchase",
    # Project 11
    "project_bi": "📊 Business Intelligence Dashboard",
    "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
    "project_bi_price": "$1,200 USD (one‑time fee)",
    "project_bi_status": "✅ Available now – lifetime access, free updates",
    "project_bi_contact": "Contact owner for purchase",
    # Project 12
    "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
    "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
    "project_ai_classifier_price": "$1,200 USD (one‑time fee)",
    "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
    "project_ai_classifier_contact": "Contact owner for purchase",
    # Project 13
    "project_task_manager": "🗂️ Task Manager Dashboard",
    "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
    "project_task_manager_price": "$1,200 USD (one‑time fee)",
    "project_task_manager_status": "✅ Available now – lifetime access, free updates",
    "project_task_manager_contact": "Contact owner for purchase",
    # Project 14
    "project_ray": "⚡ Ray Parallel Text Processor",
    "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
    "project_ray_price": "$1,200 USD (one‑time fee)",
    "project_ray_status": "✅ Available now – lifetime access, free updates",
    "project_ray_contact": "Contact owner for purchase",
    # Project 15
    "project_cassandra": "🗄️ Cassandra Data Dashboard",
    "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
    "project_cassandra_price": "$1,200 USD (one‑time fee)",
    "project_cassandra_status": "✅ Available now – lifetime access, free updates",
    "project_cassandra_contact": "Contact owner for purchase",
    # Project 16
    "project_spark": "🌊 Apache Spark Data Processor",
    "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
    "project_spark_price": "$1,200 USD (one‑time fee)",
    "project_spark_status": "✅ Available now – lifetime access, free updates",
    "project_spark_contact": "Contact owner for purchase",
    # Project 17
    "project_drone": "🚁 Haitian Drone Commander",
    "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
    "project_drone_price": "$2,000 USD (one‑time fee)",
    "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
    "project_drone_contact": "Contact owner for purchase",
    # Project 18
    "project_english": "🇬🇧 Let's Learn English with Gesner",
    "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
    "project_english_price": "$299 USD (one‑time fee)",
    "project_english_status": "✅ Available now – includes source code, setup, and support",
    "project_english_contact": "Contact owner for purchase",
    # Project 19
    "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
    "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
    "project_spanish_price": "$299 USD (one‑time fee)",
    "project_spanish_status": "✅ Available now – includes source code, setup, and support",
    "project_spanish_contact": "Contact owner for purchase",
    # Project 20
    "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
    "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
    "project_portuguese_price": "$299 USD (one‑time fee)",
    "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
    "project_portuguese_contact": "Contact owner for purchase",
    # Project 21
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
    "project_ai_career_contact": "Contact owner for purchase",
    # Project 22
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
    "project_ai_medical_contact": "Contact owner for purchase",
    # Project 23
    "project_music_studio": "🎧 Music Studio Pro – Complete Music Production Suite",
    "project_music_studio_desc": """
    **Professional music production software** – record, mix, and create beats. Includes:
    
    🎤 **Voice recording** with real‑time preview  
    🎛️ **Studio effects** – EQ, compressor, reverb, pitch correction  
    🥁 **Multi‑track beat maker** – 8 drum tracks with 16‑step sequencer  
    🎹 **Continuous loops** – deep bass and ethereal pad with volume control  
    🎵 **Sing over tracks** – record voice over any backing track  
    🔊 **Auto‑Tune Voice Recorder** – professional pitch correction and effects
    
    Perfect for musicians, producers, and content creators. Full source code included.
    """,
    "project_music_studio_price": "$299 USD (one‑time fee)",
    "project_music_studio_status": "✅ Available now – full source code included",
    "project_music_studio_contact": "Contact owner for purchase",
    # Project 24
    "project_ai_media": "🎭 AI Media Studio – Talking Photo & Video Editor",
    "project_ai_media_desc": """
    **Create professional videos from photos, audio, or video clips.**  
    Choose from four powerful modes:
    
    📷 **Photo + Speech** – upload a photo, type any text → male voice speaks  
    📷 **Photo + Uploaded Audio** – add your own voice or sound effect  
    📷 **Photo + Background Music** – select from 50 tracks or upload your own  
    🎥 **Video + Background Music** – add music to any video
    
    Features custom background (solid color or image), volume control, and instant preview.  
    Perfect for social media content, presentations, and personal projects.
    """,
    "project_ai_media_price": "$149 USD (one‑time fee)",
    "project_ai_media_status": "✅ Available now – full source code included",
    "project_ai_media_contact": "Contact owner for purchase",
    # Project 25
    "project_chinese": "🇨🇳 Let's Learn Chinese with Gesner – Book 1",
    "project_chinese_desc": """
    **Complete beginner course for Mandarin Chinese.**  
    20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes.
    
    📘 **What's inside:**
    - 20 lessons with real‑life dialogues
    - 100+ vocabulary words with native audio
    - 10 essential grammar rules with examples
    - Pronunciation practice with pinyin
    - Interactive quiz for each lesson
    - Cardinal and ordinal numbers (1-10)
    - Common Chinese idioms
    
    🎧 **Audio:** Natural Chinese voice (zh-CN-XiaoxiaoNeural) for all text.
    
    Perfect for students, teachers, and self‑learners. Full source code included.
    """,
    "project_chinese_price": "$299 USD (one‑time fee)",
    "project_chinese_status": "✅ Available now – full source code included",
    "project_chinese_contact": "Contact owner for purchase",
    # Project 26
    "project_french": "🇫🇷 Let's Learn French with Gesner – Book 1",
    "project_french_desc": """
    **Complete beginner course for French language.**  
    20 interactive lessons covering daily conversations, vocabulary, grammar, pronunciation, and quizzes.
    
    📘 **What's inside:**
    - 20 lessons with real‑life dialogues
    - 100+ vocabulary words with native audio
    - 10 essential grammar rules with examples
    - Pronunciation practice
    - Interactive quiz for each lesson
    - Cardinal and ordinal numbers (1-10)
    - Common French idioms
    
    🎧 **Audio:** Natural French voice (fr-FR-HenriNeural) for all text.
    
    Perfect for students, teachers, and self‑learners. Full source code included.
    """,
    "project_french_price": "$299 USD (one‑time fee)",
    "project_french_status": "✅ Available now – full source code included",
    "project_french_contact": "Contact owner for purchase",
    # Project 27
    "project_mathematics": "📐 Let's Learn Mathematics with Gesner – Book 1",
    "project_mathematics_desc": """
    **Complete mathematics course for beginners.**  
    20 lessons covering basic arithmetic, geometry, fractions, decimals, percentages, word problems, and more.
    
    📘 **What's inside:**
    - 20 lessons with progressive difficulty
    - Each lesson includes: symbols & tables, 3 demonstration exercises (with audio explanation), 3 interactive exercises
    - Audio support for all text (natural male voice)
    - Final quiz with questions from every lesson
    - Topics: addition, subtraction, multiplication, division, fractions, decimals, geometry (area, perimeter, volume), percentages, angles, mixed operations
    
    Perfect for students, teachers, and parents. Full source code included.
    """,
    "project_mathematics_price": "$299 USD (one‑time fee)",
    "project_mathematics_status": "✅ Available now – full source code included",
    "project_mathematics_contact": "Contact owner for purchase",
    # Project 28
    "project_ai_course": "🤖 AI Foundations & Certification Course",
    "project_ai_course_desc": """
    **28‑day AI mastery course – from beginner to certified expert.**  
    Learn ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, and more.
    
    📘 **What's inside:**
    - 28 lessons with audio (English, French, Spanish, Portuguese)
    - Week 1: AI Foundations & Personal Mentor
    - Week 2: Creativity & Skill‑Building (MidJourney, Runway, ElevenLabs)
    - Week 3: Building AI Bots & Automation (Make.com, chatbots)
    - Week 4: Certification & Career Application
    - Hands‑on projects & milestone achievements
    - Official AI Expert Certificate included
    
    Perfect for professionals, students, and anyone wanting to master AI. Full source code included.
    """,
    "project_ai_course_price": "$299 USD (one‑time fee)",
    "project_ai_course_status": "✅ Available now – full source code included",
    "project_ai_course_contact": "Contact owner for purchase",
    # Project 29
    "project_medical_term": "🩺 Medical Terminology Book for Translators",
    "project_medical_term_desc": """
    **Interactive medical terminology training for interpreters and healthcare professionals.**  
    20 lessons covering real doctor‑patient conversations, native voice audio, and translation practice.
    
    📘 **What's inside:**
    - 20 lessons with real medical scenarios
    - 50+ medical terms, acronyms & abbreviations per lesson
    - Native voice audio for English, Spanish, and other languages
    - Built‑in interpreter practice – doctor speaks English, patient speaks their native language, you translate both ways
    - Quizzes & progress tracking to certify your skills
    
    🏥 Perfect for medical interpreters, hospitals, clinics, and telemedicine providers.  
    Reduces errors, improves patient safety, and builds confidence for certification exams (CCHI, NBCMI).
    
    Full source code included. Delivered by email.
    """,
    "project_medical_term_price": "$299 USD (one‑time fee)",
    "project_medical_term_status": "✅ Available now – full source code included",
    "project_medical_term_contact": "Contact owner for purchase",
    # Project 30
    "project_python_course": "🐍 Let's Learn Coding through Python with Gesner",
    "project_python_course_desc": """
    **Complete Python programming course – from beginner to advanced.**  
    20 interactive lessons with demo code, 5 practice exercises per lesson, and audio support.
    
    📘 **What's inside:**
    - 20 lessons covering variables, loops, functions, OOP, NumPy, Matplotlib, and more
    - Each lesson includes: explanation with audio, demo code, 5 unique practice exercises with solutions
    - Audio support for all text (English, Spanish, French, Chinese, Portuguese)
    - Final project: build a mini calculator
    
    Perfect for students, professionals, and anyone wanting to learn Python. Full source code included.
    """,
    "project_python_course_price": "$299 USD (one‑time fee)",
    "project_python_course_status": "✅ Available now – full source code included",
    "project_python_course_contact": "Contact owner for purchase",
    # Project 31
    "project_hardware_course": "🔌 Let's Learn Software & Hardware with Gesner",
    "project_hardware_course_desc": """
    **Connect software with 20 hardware components – build IoT and robotics projects.**  
    20 lessons covering network cards, Wi‑Fi, Bluetooth, GPS, GPIO, sensors, motors, displays, and more.
    
    📘 **What's inside:**
    - 20 hardware components explained with text, audio, and images
    - Python code examples for each component
    - Practice exercises for real hardware interaction
    - Audio support in English, Spanish, French, Chinese, Portuguese
    
    Perfect for engineers, hobbyists, and students learning embedded systems and automation. Full source code included.
    """,
    "project_hardware_course_price": "$299 USD (one‑time fee)",
    "project_hardware_course_status": "✅ Available now – full source code included",
    "project_hardware_course_contact": "Contact owner for purchase",
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

# ---------- Sidebar (public, no login) ----------
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
st.sidebar.markdown("🌐 Language: English")
st.sidebar.markdown("---")
st.sidebar.markdown("**Founder & Developer:**")
st.sidebar.markdown("Gesner Deslandes")
st.sidebar.markdown("📞 WhatsApp: (509) 4738-5663")
st.sidebar.markdown("📧 Email: deslandes78@gmail.com")
st.sidebar.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Price")
st.sidebar.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
st.sidebar.markdown("---")
st.sidebar.markdown("### © 2025 GlobalInternet.py")
st.sidebar.markdown("All rights reserved")

# ---------- Display main content ----------
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
    
    🔗 [View the full demo on GitHub](https://github.com/Deslandes1/globalinternet_site.py/blob/main/Robotics.mp4)
    """)
st.caption("📽️ Demo: Python‑controlled humanoid robot in motion. Our software is evolving from screen to physical AI.")
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

# ---------- Projects (31 products) with comment system ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course"
]

projects = []
for key in project_keys:
    title_key = f"project_{key}"
    desc_key = f"project_{key}_desc"
    price_key = f"project_{key}_price"
    status_key = f"project_{key}_status"
    contact_key = f"project_{key}_contact"
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
        demo_url = "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/"
    elif key == "spanish":
        demo_url = "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/"
    elif key == "portuguese":
        demo_url = "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/"
    else:
        demo_url = None
    projects.append({
        "title": t.get(title_key, "Project"),
        "desc": t.get(desc_key, "Description not available"),
        "price": t.get(price_key, "Price"),
        "status": t.get(status_key, "Status"),
        "contact": t.get(contact_key, "Contact owner"),
        "key": key,
        "demo_url": demo_url
    })

for i in range(0, len(projects), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(projects):
            proj = projects[idx]
            with col:
                st.markdown(f"""
                <div class="card">
                    <h3>{proj['title']}</h3>
                    <p>{proj['desc']}</p>
                    <div class="price">{proj['price']}</div>
                    <p><em>{proj['status']}</em></p>
                </div>
                """, unsafe_allow_html=True)
                if proj.get("demo_url"):
                    st.markdown(f"<a href='{proj['demo_url']}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                else:
                    st.info("📹 Live demo available upon request. Contact us for a private walkthrough.")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    subject = f"Purchase: {proj['title']}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the software: {proj['title']} at {proj['price']}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; cursor:pointer;">💵 {t["buy_now"]}</button></a>', unsafe_allow_html=True)
                with col_btn2:
                    if st.button(f"{t['request_info']}", key=f"info_{proj['key']}"):
                        st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{proj['title']}'. Thank you!")

            # ---------- Comment section ----------
            st.markdown("#### 💬 Comments & Questions")
            comments = get_comments(proj['key'])
            for comment in comments:
                if comment["parent_id"] == 0:
                    st.markdown(f"""
                    <div class="comment-box">
                        <div class="comment-meta">
                            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]}
                        </div>
                        <div>{comment['comment']}</div>
                    """, unsafe_allow_html=True)
                    if st.button(f"❤️ {comment['likes']}", key=f"like_{proj['key']}_{comment['id']}"):
                        add_like(comment['id'])
                        st.rerun()
                    if st.button("💬 Reply", key=f"reply_{proj['key']}_{comment['id']}"):
                        st.session_state[f"reply_to_{comment['id']}"] = True
                    if st.session_state.get(f"reply_to_{comment['id']}", False):
                        with st.form(key=f"reply_form_{comment['id']}"):
                            reply_name = st.text_input("Your name", key=f"reply_name_{comment['id']}")
                            reply_text = st.text_area("Your reply", key=f"reply_text_{comment['id']}")
                            if st.form_submit_button("Post Reply"):
                                if reply_text.strip():
                                    add_comment(proj['key'], reply_name if reply_name.strip() else "Anonymous", reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
                                    st.session_state[f"reply_to_{comment['id']}"] = False
                                    st.rerun()
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
                        if st.button(f"❤️ {reply['likes']}", key=f"like_reply_{proj['key']}_{reply['id']}"):
                            add_like(reply['id'])
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            with st.form(key=f"comment_form_{proj['key']}"):
                st.markdown("**Leave a comment**")
                name = st.text_input("Your name (optional)", key=f"name_{proj['key']}")
                comment_text = st.text_area("Comment", key=f"comment_{proj['key']}")
                if st.form_submit_button("Post Comment"):
                    if comment_text.strip():
                        add_comment(proj['key'], name if name.strip() else "Anonymous", comment_text)
                        st.rerun()
                    else:
                        st.warning("Please enter a comment.")
            st.markdown("---")

# ---------- Donation section ----------
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

# ---------- Contact section ----------
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
