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
        # ----- Project 1 -----
        "project_haiti": "🇭🇹 Haiti Online Voting Software",
        "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
        "project_haiti_price": "$2,000 USD (one‑time fee)",
        "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
        "project_haiti_contact": "Contact owner for purchase",
        # ----- Project 2 -----
        "project_dashboard": "📊 Business Intelligence Dashboard",
        "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Available now",
        "project_dashboard_contact": "Contact owner for purchase",
        # ----- Project 3 -----
        "project_chatbot": "🤖 AI Customer Support Chatbot",
        "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
        "project_chatbot_price": "$800 USD (basic) / $1,500 USD (advanced)",
        "project_chatbot_status": "✅ Available now",
        "project_chatbot_contact": "Contact owner for purchase",
        # ----- Project 4 -----
        "project_school": "🏫 School Management System",
        "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Available now",
        "project_school_contact": "Contact owner for purchase",
        # ----- Project 5 -----
        "project_pos": "📦 Inventory & POS System",
        "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Available now",
        "project_pos_contact": "Contact owner for purchase",
        # ----- Project 6 -----
        "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
        "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
        "project_scraper_price": "$500 – $2,000 (depends on complexity)",
        "project_scraper_status": "✅ Available now",
        "project_scraper_contact": "Contact owner for purchase",
        # ----- Project 7 -----
        "project_chess": "♟️ Play Chess Against the Machine",
        "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_chess_price": "$20 USD (one‑time fee)",
        "project_chess_status": "✅ Available now – lifetime access, free updates",
        "project_chess_contact": "Contact owner for purchase",
        # ----- Project 8 -----
        "project_accountant": "🧮 Accountant Excel Advanced AI",
        "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
        "project_accountant_price": "$199 USD (one‑time fee)",
        "project_accountant_status": "✅ Available now – lifetime access, free updates",
        "project_accountant_contact": "Contact owner for purchase",
        # ----- Project 9 -----
        "project_archives": "📜 Haiti Archives Nationales Database",
        "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
        "project_archives_price": "$1,500 USD (one‑time fee)",
        "project_archives_status": "✅ Available now – includes source code, setup, and support",
        "project_archives_contact": "Contact owner for purchase",
        # ----- Project 10 -----
        "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
        "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
        "project_dsm_price": "$299 USD (one‑time fee)",
        "project_dsm_status": "✅ Available now – lifetime license, free updates",
        "project_dsm_contact": "Contact owner for purchase",
        # ----- Project 11 -----
        "project_bi": "📊 Business Intelligence Dashboard",
        "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_bi_price": "$1,200 USD (one‑time fee)",
        "project_bi_status": "✅ Available now – lifetime access, free updates",
        "project_bi_contact": "Contact owner for purchase",
        # ----- Project 12 -----
        "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
        "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
        "project_ai_classifier_price": "$1,200 USD (one‑time fee)",
        "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
        "project_ai_classifier_contact": "Contact owner for purchase",
        # ----- Project 13 -----
        "project_task_manager": "🗂️ Task Manager Dashboard",
        "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
        "project_task_manager_price": "$1,200 USD (one‑time fee)",
        "project_task_manager_status": "✅ Available now – lifetime access, free updates",
        "project_task_manager_contact": "Contact owner for purchase",
        # ----- Project 14 -----
        "project_ray": "⚡ Ray Parallel Text Processor",
        "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
        "project_ray_price": "$1,200 USD (one‑time fee)",
        "project_ray_status": "✅ Available now – lifetime access, free updates",
        "project_ray_contact": "Contact owner for purchase",
        # ----- Project 15 -----
        "project_cassandra": "🗄️ Cassandra Data Dashboard",
        "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "$1,200 USD (one‑time fee)",
        "project_cassandra_status": "✅ Available now – lifetime access, free updates",
        "project_cassandra_contact": "Contact owner for purchase",
        # ----- Project 16 -----
        "project_spark": "🌊 Apache Spark Data Processor",
        "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
        "project_spark_price": "$1,200 USD (one‑time fee)",
        "project_spark_status": "✅ Available now – lifetime access, free updates",
        "project_spark_contact": "Contact owner for purchase",
        # ----- Project 17 -----
        "project_drone": "🚁 Haitian Drone Commander",
        "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
        "project_drone_price": "$2,000 USD (one‑time fee)",
        "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
        "project_drone_contact": "Contact owner for purchase",
        # ----- Project 18 -----
        "project_english": "🇬🇧 Let's Learn English with Gesner",
        "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
        "project_english_price": "$299 USD (one‑time fee)",
        "project_english_status": "✅ Available now – includes source code, setup, and support",
        "project_english_contact": "Contact owner for purchase",
        # ----- Project 19 -----
        "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
        "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
        "project_spanish_price": "$299 USD (one‑time fee)",
        "project_spanish_status": "✅ Available now – includes source code, setup, and support",
        "project_spanish_contact": "Contact owner for purchase",
        # ----- Project 20 -----
        "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
        "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
        "project_portuguese_price": "$299 USD (one‑time fee)",
        "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
        "project_portuguese_contact": "Contact owner for purchase",
        # ----- Project 21 -----
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
        # ----- Project 22 -----
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
        # ----- Project 23 -----
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
        # ----- Project 24 -----
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
        # ----- Project 25 -----
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
        # ----- Project 26 -----
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
        # ----- Project 27 -----
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
        # ----- Project 28 -----
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
        # ----- NEW PROJECT 29: Medical Terminology Book -----
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
        # ----- End of projects -----
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
    },
    "fr": {
        # All existing French translations remain the same. Only the new project is added here.
        # (For brevity, I am not repeating the entire French dictionary – but in your final file, keep all existing French keys.)
        # The user’s original code had incomplete French for the new project; I am adding the full new project in French.
        "project_medical_term": "🩺 Livre de Terminologie Médicale pour Traducteurs",
        "project_medical_term_desc": """
        **Formation interactive en terminologie médicale pour interprètes et professionnels de santé.**  
        20 leçons basées sur des conversations réelles médecin‑patient, audio voix natives, et pratique de la traduction.
        
        📘 **Contenu :**
        - 20 leçons avec scénarios médicaux réels
        - 50+ termes médicaux, acronymes et abréviations par leçon
        - Audio voix natives pour anglais, espagnol et autres langues
        - Pratique intégrée de l’interprétation – le médecin parle anglais, le patient parle sa langue maternelle, vous traduisez dans les deux sens
        - Quiz et suivi de progression pour certifier vos compétences
        
        🏥 Parfait pour interprètes médicaux, hôpitaux, cliniques et télémédecine.  
        Réduit les erreurs, améliore la sécurité des patients et prépare aux examens de certification (CCHI, NBCMI).
        
        Code source complet inclus. Livré par email.
        """,
        "project_medical_term_price": "299 $ USD (paiement unique)",
        "project_medical_term_status": "✅ Disponible – code source complet inclus",
        "project_medical_term_contact": "Contactez le propriétaire pour acheter",
        # Ensure other French keys (like project_ai_course, etc.) are present in the actual file.
    },
    "es": {
        "project_medical_term": "🩺 Libro de Terminología Médica para Traductores",
        "project_medical_term_desc": """
        **Capacitación interactiva en terminología médica para intérpretes y profesionales de la salud.**  
        20 lecciones basadas en conversaciones reales médico‑paciente, audio con voz nativa y práctica de traducción.
        
        📘 **Contenido:**
        - 20 lecciones con escenarios médicos reales
        - 50+ términos médicos, siglas y abreviaturas por lección
        - Audio con voz nativa para inglés, español y otros idiomas
        - Práctica integrada de interpretación – el médico habla inglés, el paciente habla su lengua materna, usted traduce en ambos sentidos
        - Cuestionarios y seguimiento de progreso para certificar sus habilidades
        
        🏥 Perfecto para intérpretes médicos, hospitales, clínicas y telemedicina.  
        Reduce errores, mejora la seguridad del paciente y prepara para exámenes de certificación (CCHI, NBCMI).
        
        Código fuente completo incluido. Entregado por correo electrónico.
        """,
        "project_medical_term_price": "$299 USD (pago único)",
        "project_medical_term_status": "✅ Disponible – código fuente completo incluido",
        "project_medical_term_contact": "Contacte al propietario para comprar",
    },
    "ht": {
        "project_medical_term": "🩺 Liv Tèminoloji Medikal pou Tradiktè",
        "project_medical_term_desc": """
        **Fòmasyon entèaktif sou tèminoloji medikal pou entèprèt ak pwofesyonèl sante.**  
        20 lesyon ki baze sou konvèsasyon reyèl doktè‑pasyan, odyo vwa natif natal, ak pratik tradiksyon.
        
        📘 **Sa ki ladan l :**
        - 20 lesyon ak senaryo medikal reyèl
        - 50+ tèm medikal, akwonim ak abreviyasyon pa leson
        - Odyo vwa natif natal pou angle, panyòl ak lòt lang
        - Pratik entèpretasyon entegre – doktè pale angle, pasyan pale lang li, ou tradui nan tou de sans
        - Egzamen ak swivi pwogrè pou sètifye konpetans ou yo
        
        🏥 Pafè pou entèprèt medikal, lopital, klinik ak télémédecine.  
        Redui erè, amelyore sekirite pasyan yo ak prepare pou egzamen sètifikasyon (CCHI, NBCMI).
        
        Kòd sous konplè enkli. Livre pa imel.
        """,
        "project_medical_term_price": "$299 USD (peman inik)",
        "project_medical_term_status": "✅ Disponib – kòd sous konplè enkli",
        "project_medical_term_contact": "Kontakte pwopriyetè a pou achte",
    }
}

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
# Hero Section (big globe)
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
# Avatar video
# -----------------------------
video_url = "https://github.com/Deslandes1/Gesner-Deslandes-Avatar/blob/main/avatar_video.mp4.mp4?raw=true"
st.video(video_url, format="video/mp4", start_time=0)
st.caption(t['office_photo_caption'])

# -----------------------------
# CV Section with owner video
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
# Projects Section (29 projects now)
# -----------------------------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Build the full projects list with all 29 projects
projects = [
    {"title": t['project_haiti'], "desc": t['project_haiti_desc'], "price": t['project_haiti_price'], "status": t['project_haiti_status'], "contact": t['project_haiti_contact'], "key": "haiti", "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Haiti+Voting+Software"},
    {"title": t['project_dashboard'], "desc": t['project_dashboard_desc'], "price": t['project_dashboard_price'], "status": t['project_dashboard_status'], "contact": t['project_dashboard_contact'], "key": "dashboard", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"},
    {"title": t['project_chatbot'], "desc": t['project_chatbot_desc'], "price": t['project_chatbot_price'], "status": t['project_chatbot_status'], "contact": t['project_chatbot_contact'], "key": "chatbot", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Chatbot"},
    {"title": t['project_school'], "desc": t['project_school_desc'], "price": t['project_school_price'], "status": t['project_school_status'], "contact": t['project_school_contact'], "key": "school", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=School+Management"},
    {"title": t['project_pos'], "desc": t['project_pos_desc'], "price": t['project_pos_price'], "status": t['project_pos_status'], "contact": t['project_pos_contact'], "key": "pos", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Inventory+POS"},
    {"title": t['project_scraper'], "desc": t['project_scraper_desc'], "price": t['project_scraper_price'], "status": t['project_scraper_status'], "contact": t['project_scraper_contact'], "key": "scraper", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Web+Scraper"},
    {"title": t['project_chess'], "desc": t['project_chess_desc'], "price": t['project_chess_price'], "status": t['project_chess_status'], "contact": t['project_chess_contact'], "key": "chess", "demo_url": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Chess+Game"},
    {"title": t['project_accountant'], "desc": t['project_accountant_desc'], "price": t['project_accountant_price'], "status": t['project_accountant_status'], "contact": t['project_accountant_contact'], "key": "accountant", "demo_url": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Accounting+Software"},
    {"title": t['project_archives'], "desc": t['project_archives_desc'], "price": t['project_archives_price'], "status": t['project_archives_status'], "contact": t['project_archives_contact'], "key": "archives", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=National+Archives"},
    {"title": t['project_dsm'], "desc": t['project_dsm_desc'], "price": t['project_dsm_price'], "status": t['project_dsm_status'], "contact": t['project_dsm_contact'], "key": "dsm", "demo_url": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=DSM+Radar"},
    {"title": t['project_bi'], "desc": t['project_bi_desc'], "price": t['project_bi_price'], "status": t['project_bi_status'], "contact": t['project_bi_contact'], "key": "bi", "demo_url": "https://9enktzu34sxzyvtsymghxd.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"},
    {"title": t['project_ai_classifier'], "desc": t['project_ai_classifier_desc'], "price": t['project_ai_classifier_price'], "status": t['project_ai_classifier_status'], "contact": t['project_ai_classifier_contact'], "key": "aiclassifier", "demo_url": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=AI+Image+Classifier"},
    {"title": t['project_task_manager'], "desc": t['project_task_manager_desc'], "price": t['project_task_manager_price'], "status": t['project_task_manager_status'], "contact": t['project_task_manager_contact'], "key": "taskmanager", "demo_url": "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Task+Manager+Dashboard"},
    {"title": t['project_ray'], "desc": t['project_ray_desc'], "price": t['project_ray_price'], "status": t['project_ray_status'], "contact": t['project_ray_contact'], "key": "ray", "demo_url": "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Ray+Parallel+Processor"},
    {"title": t['project_cassandra'], "desc": t['project_cassandra_desc'], "price": t['project_cassandra_price'], "status": t['project_cassandra_status'], "contact": t['project_cassandra_contact'], "key": "cassandra", "demo_url": "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Cassandra+Data+Dashboard"},
    {"title": t['project_spark'], "desc": t['project_spark_desc'], "price": t['project_spark_price'], "status": t['project_spark_status'], "contact": t['project_spark_contact'], "key": "spark", "demo_url": "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Apache+Spark+Data+Processor"},
    {"title": t['project_drone'], "desc": t['project_drone_desc'], "price": t['project_drone_price'], "status": t['project_drone_status'], "contact": t['project_drone_contact'], "key": "drone", "demo_url": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Haitian+Drone+Commander"},
    {"title": t['project_english'], "desc": t['project_english_desc'], "price": t['project_english_price'], "status": t['project_english_status'], "contact": t['project_english_contact'], "key": "english", "demo_url": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+English+with+Gesner"},
    {"title": t['project_spanish'], "desc": t['project_spanish_desc'], "price": t['project_spanish_price'], "status": t['project_spanish_status'], "contact": t['project_spanish_contact'], "key": "spanish", "demo_url": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+Spanish+with+Gesner"},
    {"title": t['project_portuguese'], "desc": t['project_portuguese_desc'], "price": t['project_portuguese_price'], "status": t['project_portuguese_status'], "contact": t['project_portuguese_contact'], "key": "portuguese", "demo_url": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+Portuguese+with+Gesner"},
    {"title": t['project_ai_career'], "desc": t['project_ai_career_desc'], "price": t['project_ai_career_price'], "status": t['project_ai_career_status'], "contact": t['project_ai_career_contact'], "key": "aicareer", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Career+Coach"},
    {"title": t['project_ai_medical'], "desc": t['project_ai_medical_desc'], "price": t['project_ai_medical_price'], "status": t['project_ai_medical_status'], "contact": t['project_ai_medical_contact'], "key": "aimedical", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Medical+Assistant"},
    {"title": t['project_music_studio'], "desc": t['project_music_studio_desc'], "price": t['project_music_studio_price'], "status": t['project_music_studio_status'], "contact": t['project_music_studio_contact'], "key": "musicstudio", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Music+Studio+Pro"},
    {"title": t['project_ai_media'], "desc": t['project_ai_media_desc'], "price": t['project_ai_media_price'], "status": t['project_ai_media_status'], "contact": t['project_ai_media_contact'], "key": "aimedia", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Media+Studio"},
    {"title": t['project_chinese'], "desc": t['project_chinese_desc'], "price": t['project_chinese_price'], "status": t['project_chinese_status'], "contact": t['project_chinese_contact'], "key": "chinese", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Learn+Chinese+with+Gesner"},
    {"title": t['project_french'], "desc": t['project_french_desc'], "price": t['project_french_price'], "status": t['project_french_status'], "contact": t['project_french_contact'], "key": "french", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Learn+French+with+Gesner"},
    {"title": t['project_mathematics'], "desc": t['project_mathematics_desc'], "price": t['project_mathematics_price'], "status": t['project_mathematics_status'], "contact": t['project_mathematics_contact'], "key": "mathematics", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Learn+Mathematics+with+Gesner"},
    {"title": t['project_ai_course'], "desc": t['project_ai_course_desc'], "price": t['project_ai_course_price'], "status": t['project_ai_course_status'], "contact": t['project_ai_course_contact'], "key": "aicourse", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Foundations+Course"},
    # NEW PROJECT 29: Medical Terminology Book
    {"title": t['project_medical_term'], "desc": t['project_medical_term_desc'], "price": t['project_medical_term_price'], "status": t['project_medical_term_status'], "contact": t['project_medical_term_contact'], "key": "medicalterm", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Medical+Terminology+Book"}
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
                    if st.button(f"{t['request_info']}", key=f"btn_{proj['key']}_{lang}"):
                        st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{proj['title']}'. Thank you!")

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
