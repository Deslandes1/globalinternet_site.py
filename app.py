import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
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
# Translation Dictionary (COMPLETE for all 4 languages)
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
        # ----- Project 29 -----
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
        # ----- Project 30 -----
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
        # ----- Project 31 -----
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
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Construisez avec Python. Livrez rapidement. Innovez avec l'IA.",
        "hero_desc": "D'Haïti au monde – des logiciels sur mesure qui fonctionnent en ligne.",
        "about_title": "👨‍💻 À propos de l'entreprise",
        "about_text": """
        **GlobalInternet.py** a été fondé par **Gesner Deslandes** – propriétaire, fondateur et ingénieur principal.  
        Nous construisons des **logiciels basés sur Python** à la demande pour des clients du monde entier. Comme la Silicon Valley, mais avec une touche haïtienne et des résultats exceptionnels.
        
        - 🧠 **Solutions alimentées par l'IA** – chatbots, analyse de données, automatisation  
        - 🗳️ **Systèmes électoraux complets** – sécurisés, multilingues, en temps réel  
        - 🌐 **Applications web** – tableaux de bord, outils internes, plateformes en ligne  
        - 📦 **Livraison complète** – nous vous envoyons le code complet par email et vous guidons lors de l'installation
        
        Que vous ayez besoin d'un site web d'entreprise, d'un outil logiciel personnalisé ou d'une plateforme en ligne à grande échelle – nous le construisons, vous le possédez.
        """,
        "office_photo_caption": "Avatar parlant de Gesner Deslandes – présentation de GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – notre représentant numérique de l'innovation et de l'expertise logicielle.",
        "founder": "Fondateur et PDG",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Ingénieur | Passionné d'IA | Expert Python",
        "cv_title": "📄 À propos du propriétaire – Gesner Deslandes",
        "cv_intro": "Constructeur de logiciels Python | Développeur web | Coordinateur technologique",
        "cv_summary": """
        Leader et gestionnaire exceptionnellement motivé, engagé envers l'excellence et la précision.  
        **Compétences clés :** Leadership, Interprétation (anglais, français, créole haïtien), Orientation mécanique, Gestion, Microsoft Office.
        """,
        "cv_experience_title": "💼 Expérience professionnelle",
        "cv_experience": """
        **Coordinateur technologique** – Orphelinat Be Like Brit (2021–présent)  
        Configuration des réunions Zoom, maintenance des ordinateurs portables/tablettes, support technique quotidien, assurance d'opérations numériques fluides.

        **PDG et services d'interprétation** – Tourisme personnalisé pour groupes d'ONG, équipes de mission et particuliers.

        **Gestionnaire de parc / répartiteur** – J/P Haitian Relief Organization  
        Gestion de plus de 20 véhicules, journaux de bord, calendriers de maintenance avec Excel.

        **Interprète médical** – International Child Care  
        Interprétation médicale précise anglais–français–créole.

        **Chef d'équipe et interprète** – Can‑Do NGO  
        Direction de projets de reconstruction.

        **Professeur d'anglais** – Be Like Brit (préscolaire à NS4)

        **Traducteur de documents** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Éducation et formation",
        "cv_education": """
        - École de formation professionnelle – Anglais américain  
        - Institut Diesel d'Haïti – Mécanicien diesel  
        - Certification en bureautique (octobre 2000)  
        - Diplômé du secondaire
        """,
        "cv_references": "📞 Références disponibles sur demande.",
        "team_title": "👥 Notre équipe",
        "team_sub": "Rencontrez les talents derrière GlobalInternet.py – embauchés en avril 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fondateur et PDG", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Assistant du PDG", "since": "Avril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Programmeur Python", "since": "Avril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Programmeur Python", "since": "Avril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Secrétaire", "since": "Avril 2026"}
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
        "project_haiti": "🇭🇹 Logiciel de vote en ligne Haïti",
        "project_haiti_desc": "Système électoral présidentiel complet avec support multilingue (créole, français, anglais, espagnol), suivi en direct, tableau de bord du président du CEP (gestion des candidats, téléchargement de photos, rapports de progression), scrutin secret et mots de passe modifiables. Utilisé pour les élections nationales.",
        "project_haiti_price": "2 000 $ USD (paiement unique)",
        "project_haiti_status": "✅ Disponible – code source, installation et support inclus",
        "project_haiti_contact": "Contactez le propriétaire pour acheter",
        "project_dashboard": "📊 Tableau de bord d'intelligence d'affaires",
        "project_dashboard_desc": "Tableau de bord d'analytique en temps réel pour entreprises. Connectez‑vous à toute base de données (SQL, Excel, CSV) et visualisez KPI, tendances des ventes, inventaire et rapports personnalisés. Entièrement interactif et personnalisable.",
        "project_dashboard_price": "1 200 $ USD",
        "project_dashboard_status": "✅ Disponible",
        "project_dashboard_contact": "Contactez le propriétaire pour acheter",
        "project_chatbot": "🤖 Chatbot de support client IA",
        "project_chatbot_desc": "Chatbot intelligent entraîné sur vos données d'entreprise. Répondez aux questions des clients 24/7, réduisez la charge de support. Intègre les sites web, WhatsApp ou Telegram. Construit avec Python et NLP moderne.",
        "project_chatbot_price": "800 $ USD (basique) / 1 500 $ USD (avancé)",
        "project_chatbot_status": "✅ Disponible",
        "project_chatbot_contact": "Contactez le propriétaire pour acheter",
        "project_school": "🏫 Système de gestion scolaire",
        "project_school_desc": "Plateforme complète pour écoles : inscription des étudiants, gestion des notes, suivi des présences, portail parents, génération de bulletins et collecte des frais. Rôles multi‑utilisateurs (admin, enseignants, parents).",
        "project_school_price": "1 500 $ USD",
        "project_school_status": "✅ Disponible",
        "project_school_contact": "Contactez le propriétaire pour acheter",
        "project_pos": "📦 Système d'inventaire et point de vente",
        "project_pos_desc": "Gestion d'inventaire web avec point de vente pour petites entreprises. Lecture de codes‑barres, alertes de stock, rapports de vente, gestion des fournisseurs. Fonctionne en ligne et hors ligne.",
        "project_pos_price": "1 000 $ USD",
        "project_pos_status": "✅ Disponible",
        "project_pos_contact": "Contactez le propriétaire pour acheter",
        "project_scraper": "📈 Extracteur web personnalisé et pipeline de données",
        "project_scraper_desc": "Extraction automatisée de données de n'importe quel site web, nettoyée et livrée en Excel/JSON/CSV. Planification quotidienne, hebdomadaire ou mensuelle. Parfait pour la veille marché, surveillance des prix ou génération de leads.",
        "project_scraper_price": "500 – 2 000 $ USD (selon complexité)",
        "project_scraper_status": "✅ Disponible",
        "project_scraper_contact": "Contactez le propriétaire pour acheter",
        "project_chess": "♟️ Jouez aux échecs contre la machine",
        "project_chess_desc": "Jeu d'échecs éducatif avec adversaire IA (3 niveaux de difficulté). Chaque mouvement est expliqué – apprenez les tactiques comme les fourchettes, les clouages et les échecs à la découverte. Inclut mode démo, tableau de bord des mouvements et téléchargement du rapport complet. Multilingue (anglais, français, espagnol, créole).",
        "project_chess_price": "20 $ USD (paiement unique)",
        "project_chess_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_chess_contact": "Contactez le propriétaire pour acheter",
        "project_accountant": "🧮 Comptable Excel avancé IA",
        "project_accountant_desc": "Suite comptable et de gestion de prêts professionnelle. Suivi des revenus/dépenses, gestion des prêts (emprunteurs, dates d'échéance, paiements), tableau de bord avec solde, exportation de tous les rapports vers Excel et PDF. Multilingue (anglais, français, espagnol).",
        "project_accountant_price": "199 $ USD (paiement unique)",
        "project_accountant_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_accountant_contact": "Contactez le propriétaire pour acheter",
        "project_archives": "📜 Base de données des Archives Nationales d'Haïti",
        "project_archives_desc": "Base de données complète des archives nationales pour les citoyens haïtiens. Stocke NIF (Matricule Fiscale), CIN, Passeport, Permis de conduire, historique de vote, parrainages et téléchargements de documents. Validation de signature ministérielle, système de mot de passe annuel, multilingue (anglais, français, espagnol, créole).",
        "project_archives_price": "1 500 $ USD (paiement unique)",
        "project_archives_status": "✅ Disponible – code source, installation et support inclus",
        "project_archives_contact": "Contactez le propriétaire pour acheter",
        "project_dsm": "🛡️ DSM-2026: SYSTÈME SÉCURISÉ",
        "project_dsm_desc": "Radar de surveillance de la stratosphère avancé – suit les avions, satellites et missiles en temps réel. Affichage radar simulé avec détection de menace, support multilingue et rapports de renseignement téléchargeables.",
        "project_dsm_price": "299 $ USD (paiement unique)",
        "project_dsm_status": "✅ Disponible – licence à vie, mises à jour gratuites",
        "project_dsm_contact": "Contactez le propriétaire pour acheter",
        "project_bi": "📊 Tableau de bord d'intelligence d'affaires",
        "project_bi_desc": "Tableau de bord d'analytique en temps réel pour entreprises. Connectez SQL, Excel, CSV – visualisez KPI, tendances des ventes, inventaire et performances régionales. Entièrement interactif avec filtres de dates et rapports CSV téléchargeables. Multilingue (anglais, français, espagnol, créole).",
        "project_bi_price": "1 200 $ USD (paiement unique)",
        "project_bi_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_bi_contact": "Contactez le propriétaire pour acheter",
        "project_ai_classifier": "🧠 Classificateur d'images IA (MobileNetV2)",
        "project_ai_classifier_desc": "Téléchargez une image et l'IA l'identifie parmi 1000 catégories (animaux, véhicules, nourriture, objets du quotidien). Utilise TensorFlow MobileNetV2 pré‑entraîné sur ImageNet. Multilingue, protégé par mot de passe, démo prête.",
        "project_ai_classifier_price": "1 200 $ USD (paiement unique)",
        "project_ai_classifier_status": "✅ Disponible – code source, installation et support inclus",
        "project_ai_classifier_contact": "Contactez le propriétaire pour acheter",
        "project_task_manager": "🗂️ Tableau de bord de gestion des tâches",
        "project_task_manager_desc": "Gérez les tâches, suivez les progrès et analysez la productivité avec des graphiques en temps réel et le mode sombre. Inspiré de l'interface basée sur les composants de React. Multilingue, stockage persistant, tableau de bord analytique.",
        "project_task_manager_price": "1 200 $ USD (paiement unique)",
        "project_task_manager_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_task_manager_contact": "Contactez le propriétaire pour acheter",
        "project_ray": "⚡ Processeur de texte parallèle Ray",
        "project_ray_desc": "Traitez du texte en parallèle sur plusieurs cœurs CPU. Comparez la vitesse d'exécution séquentielle vs parallèle. Inspiré du framework de calcul distribué Ray de l'UC Berkeley.",
        "project_ray_price": "1 200 $ USD (paiement unique)",
        "project_ray_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_ray_contact": "Contactez le propriétaire pour acheter",
        "project_cassandra": "🗄️ Tableau de bord de données Cassandra",
        "project_cassandra_desc": "Démonstration de base de données NoSQL distribuée. Ajoutez des commandes, recherchez par client et explorez l'analytique en temps réel. Modélisé d'après Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "1 200 $ USD (paiement unique)",
        "project_cassandra_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_cassandra_contact": "Contactez le propriétaire pour acheter",
        "project_spark": "🌊 Processeur de données Apache Spark",
        "project_spark_desc": "Téléchargez un fichier CSV et exécutez des agrégations de type SQL (group by, sum, avg, count) en utilisant Spark. Résultats et graphiques en temps réel. Inspiré du moteur big data utilisé par des milliers d'entreprises.",
        "project_spark_price": "1 200 $ USD (paiement unique)",
        "project_spark_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_spark_contact": "Contactez le propriétaire pour acheter",
        "project_drone": "🚁 Commandant de drone haïtien",
        "project_drone_desc": "Contrôlez le premier drone fabriqué en Haïti depuis votre téléphone. Mode simulation, support réel du drone (MAVLink), armement, décollage, atterrissage, vol vers coordonnées GPS, télémétrie en direct, historique des commandes. Multilingue, tableau de bord professionnel.",
        "project_drone_price": "2 000 $ USD (paiement unique)",
        "project_drone_status": "✅ Disponible – code source, installation et 1 an de support inclus",
        "project_drone_contact": "Contactez le propriétaire pour acheter",
        "project_english": "🇬🇧 Apprenons l'anglais avec Gesner",
        "project_english_desc": "Application interactive d'apprentissage de l'anglais. Couvre le vocabulaire, la grammaire, la prononciation et la pratique de la conversation. Interface multilingue, suivi des progrès, quiz et certificats. Parfait pour les débutants et les apprenants intermédiaires.",
        "project_english_price": "299 $ USD (paiement unique)",
        "project_english_status": "✅ Disponible – code source, installation et support inclus",
        "project_english_contact": "Contactez le propriétaire pour acheter",
        "project_spanish": "🇪🇸 Apprenons l'espagnol avec Gesner",
        "project_spanish_desc": "Plateforme complète d'apprentissage de l'espagnol. Leçons sur le vocabulaire, les conjugaisons, la compréhension orale et les notes culturelles. Inclut des exercices interactifs, la reconnaissance vocale et un tableau de bord de progression.",
        "project_spanish_price": "299 $ USD (paiement unique)",
        "project_spanish_status": "✅ Disponible – code source, installation et support inclus",
        "project_spanish_contact": "Contactez le propriétaire pour acheter",
        "project_portuguese": "🇵🇹 Apprenons le portugais avec Gesner",
        "project_portuguese_desc": "Application d'apprentissage du portugais brésilien et européen. Couvre les phrases essentielles, la grammaire, les temps verbaux et les dialogues de la vie réelle. Inclut des flashcards, un guide de prononciation et des badges de réussite. Support multilingue.",
        "project_portuguese_price": "299 $ USD (paiement unique)",
        "project_portuguese_status": "✅ Disponible – code source, installation et support inclus",
        "project_portuguese_contact": "Contactez le propriétaire pour acheter",
        "project_ai_career": "🚀 Coach de carrière IA – Optimiseur de CV",
        "project_ai_career_desc": "**Optimisez votre CV et réussissez vos entretiens avec l'IA.** Téléchargez votre CV et une description de poste – notre IA analyse les deux et fournit : des mots-clés à ajouter, des améliorations de compétences, des suggestions de formatage et des questions d'entretien prédites. Parfait pour les chercheurs d'emploi, étudiants et professionnels. Code source complet inclus.",
        "project_ai_career_price": "149 $ USD (paiement unique)",
        "project_ai_career_status": "✅ Disponible – code source complet inclus",
        "project_ai_career_contact": "Contactez le propriétaire pour acheter",
        "project_ai_medical": "🧪 Assistant IA en littérature médicale et scientifique",
        "project_ai_medical_desc": "**Posez n'importe quelle question médicale ou scientifique – obtenez des réponses basées sur des recherches réelles.** Notre IA recherche dans PubMed, la plus grande base de données de littérature médicale, extrait les résumés pertinents et génère des réponses factuelles avec citations et liens directs. Code source complet inclus.",
        "project_ai_medical_price": "149 $ USD (paiement unique)",
        "project_ai_medical_status": "✅ Disponible – code source complet inclus",
        "project_ai_medical_contact": "Contactez le propriétaire pour acheter",
        "project_music_studio": "🎧 Music Studio Pro – Suite complète de production musicale",
        "project_music_studio_desc": "**Logiciel professionnel de production musicale** – enregistrez, mixez et créez des beats. Inclut enregistrement vocal, effets studio (EQ, compresseur, réverbération, correction de hauteur), beatmaker multi‑pistes, boucles continues, enregistrement vocal sur pistes, correcteur automatique. Code source complet inclus.",
        "project_music_studio_price": "299 $ USD (paiement unique)",
        "project_music_studio_status": "✅ Disponible – code source complet inclus",
        "project_music_studio_contact": "Contactez le propriétaire pour acheter",
        "project_ai_media": "🎭 Studio média IA – Éditeur photo et vidéo parlant",
        "project_ai_media_desc": "**Créez des vidéos professionnelles à partir de photos, audio ou clips vidéo.** Quatre modes puissants : photo + parole, photo + audio téléchargé, photo + musique de fond, vidéo + musique de fond. Code source complet inclus.",
        "project_ai_media_price": "149 $ USD (paiement unique)",
        "project_ai_media_status": "✅ Disponible – code source complet inclus",
        "project_ai_media_contact": "Contactez le propriétaire pour acheter",
        "project_chinese": "🇨🇳 Apprenons le chinois avec Gesner – Livre 1",
        "project_chinese_desc": "**Cours complet de mandarin pour débutants.** 20 leçons interactives sur les conversations quotidiennes, le vocabulaire, la grammaire, la prononciation et les quiz. Code source complet inclus.",
        "project_chinese_price": "299 $ USD (paiement unique)",
        "project_chinese_status": "✅ Disponible – code source complet inclus",
        "project_chinese_contact": "Contactez le propriétaire pour acheter",
        "project_french": "🇫🇷 Apprenons le français avec Gesner – Livre 1",
        "project_french_desc": "**Cours complet de français pour débutants.** 20 leçons interactives sur les conversations quotidiennes, le vocabulaire, la grammaire, la prononciation et les quiz. Code source complet inclus.",
        "project_french_price": "299 $ USD (paiement unique)",
        "project_french_status": "✅ Disponible – code source complet inclus",
        "project_french_contact": "Contactez le propriétaire pour acheter",
        "project_mathematics": "📐 Apprenons les mathématiques avec Gesner – Livre 1",
        "project_mathematics_desc": "**Cours complet de mathématiques pour débutants.** 20 leçons couvrant l'arithmétique de base, la géométrie, les fractions, les décimales, les pourcentages, les problèmes de mots, etc. Code source complet inclus.",
        "project_mathematics_price": "299 $ USD (paiement unique)",
        "project_mathematics_status": "✅ Disponible – code source complet inclus",
        "project_mathematics_contact": "Contactez le propriétaire pour acheter",
        "project_ai_course": "🤖 Cours Fondamentaux de l'IA et certification",
        "project_ai_course_desc": "**Cours de maîtrise de l'IA en 28 jours – du débutant à l'expert certifié.** Apprenez ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, et plus. Code source complet inclus.",
        "project_ai_course_price": "299 $ USD (paiement unique)",
        "project_ai_course_status": "✅ Disponible – code source complet inclus",
        "project_ai_course_contact": "Contactez le propriétaire pour acheter",
        "project_medical_term": "🩺 Livre de terminologie médicale pour traducteurs",
        "project_medical_term_desc": "**Formation interactive en terminologie médicale pour interprètes et professionnels de santé.** 20 leçons basées sur des conversations réelles médecin‑patient, audio voix natives, et pratique de la traduction. Code source complet inclus.",
        "project_medical_term_price": "299 $ USD (paiement unique)",
        "project_medical_term_status": "✅ Disponible – code source complet inclus",
        "project_medical_term_contact": "Contactez le propriétaire pour acheter",
        "project_python_course": "🐍 Apprenons à coder en Python avec Gesner",
        "project_python_course_desc": "**Cours complet de programmation Python – du débutant à l'avancé.** 20 leçons interactives avec code de démonstration, 5 exercices pratiques par leçon et support audio. Code source complet inclus.",
        "project_python_course_price": "299 $ USD (paiement unique)",
        "project_python_course_status": "✅ Disponible – code source complet inclus",
        "project_python_course_contact": "Contactez le propriétaire pour acheter",
        "project_hardware_course": "🔌 Apprenons à connecter logiciel et matériel avec Gesner",
        "project_hardware_course_desc": "**Connectez un logiciel à 20 composants matériels – projets IoT et robotique.** 20 leçons couvrant cartes réseau, Wi‑Fi, Bluetooth, GPS, GPIO, capteurs, moteurs, écrans, etc. Code source complet inclus.",
        "project_hardware_course_price": "299 $ USD (paiement unique)",
        "project_hardware_course_status": "✅ Disponible – code source complet inclus",
        "project_hardware_course_contact": "Contactez le propriétaire pour acheter",
        "view_demo": "🎬 Voir la démo",
        "demo_screenshot": "Aperçu de la capture d'écran (remplacez par l'image réelle)",
        "live_demo": "🔗 Démo en direct",
        "demo_password_hint": "🔐 Mot de passe démo : 20082010",
        "request_info": "Demander des informations",
        "buy_now": "💵 Acheter maintenant",
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
        "footer_pride": "🇭🇹 Fier d'être Haïtien – servant le monde avec Python et l'IA 🇭🇹"
    },
    "es": {
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Construye con Python. Entrega con velocidad. Innova con IA.",
        "hero_desc": "De Haití al mundo – software personalizado que funciona en línea.",
        "about_title": "👨‍💻 Sobre la empresa",
        "about_text": """
        **GlobalInternet.py** fue fundada por **Gesner Deslandes** – propietario, fundador e ingeniero principal.  
        Construimos **software basado en Python** bajo demanda para clientes de todo el mundo. Como Silicon Valley, pero con un toque haitiano y resultados sobresalientes.
        
        - 🧠 **Soluciones impulsadas por IA** – chatbots, análisis de datos, automatización  
        - 🗳️ **Sistemas electorales completos** – seguros, multilingües, en tiempo real  
        - 🌐 **Aplicaciones web** – paneles, herramientas internas, plataformas en línea  
        - 📦 **Entrega completa** – le enviamos el código completo por correo electrónico y lo guiamos en la instalación
        
        Ya sea que necesite un sitio web corporativo, una herramienta de software personalizada o una plataforma en línea a gran escala – nosotros la construimos, usted la posee.
        """,
        "office_photo_caption": "Avatar parlante de Gesner Deslandes – presentando GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – nuestro representante digital de innovación y experiencia en software.",
        "founder": "Fundador y CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Ingeniero | Entusiasta de IA | Experto en Python",
        "cv_title": "📄 Sobre el propietario – Gesner Deslandes",
        "cv_intro": "Constructor de software Python | Desarrollador web | Coordinador de tecnología",
        "cv_summary": """
        Líder y gerente excepcionalmente motivado, comprometido con la excelencia y la precisión.  
        **Competencias principales:** Liderazgo, Interpretación (inglés, francés, criollo haitiano), Orientación mecánica, Gestión, Microsoft Office.
        """,
        "cv_experience_title": "💼 Experiencia profesional",
        "cv_experience": """
        **Coordinador de tecnología** – Orfanato Be Like Brit (2021–presente)  
        Configuración de reuniones Zoom, mantenimiento de portátiles/tabletas, soporte técnico diario, asegurar operaciones digitales fluidas.

        **CEO y servicios de interpretación** – Turismo personalizado para grupos de ONG, equipos misioneros e individuos.

        **Gerente de flota / Despachador** – J/P Haitian Relief Organization  
        Gestión de más de 20 vehículos, registros de conductores, calendarios de mantenimiento usando Excel.

        **Intérprete médico** – International Child Care  
        Interpretación médica precisa inglés–francés–criollo.

        **Líder de equipo e intérprete** – Can‑Do NGO  
        Liderazgo de proyectos de reconstrucción.

        **Profesor de inglés** – Be Like Brit (preescolar a NS4)

        **Traductor de documentos** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Educación y formación",
        "cv_education": """
        - Escuela de formación vocacional – Inglés americano  
        - Instituto Diesel de Haití – Mecánico diesel  
        - Certificación en ofimática (octubre de 2000)  
        - Graduado de secundaria
        """,
        "cv_references": "📞 Referencias disponibles bajo petición.",
        "team_title": "👥 Nuestro equipo",
        "team_sub": "Conozca a los talentos detrás de GlobalInternet.py – contratados en abril de 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fundador y CEO", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Asistente del CEO", "since": "Abril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Programador Python", "since": "Abril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Programador Python", "since": "Abril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Secretaria", "since": "Abril 2026"}
        ],
        "services_title": "⚙️ Nuestros servicios",
        "services": [
            ("🐍 Desarrollo Python personalizado", "Scripts a medida, automatización, sistemas backend."),
            ("🤖 IA y aprendizaje automático", "Chatbots, modelos predictivos, análisis de datos."),
            ("🗳️ Software electoral", "Seguro, multilingüe, resultados en vivo – como nuestro sistema Haití."),
            ("📊 Paneles de inteligencia empresarial", "Analítica en tiempo real y herramientas de informes."),
            ("🌐 Sitios web y aplicaciones web", "Soluciones full‑stack desplegadas en línea."),
            ("📦 Entrega en 24 horas", "Trabajamos rápido – reciba su software por correo electrónico, listo para usar."),
            ("📢 Publicidad y marketing", "Campañas digitales, gestión de redes sociales, segmentación con IA, informes de rendimiento. Desde $150 hasta $1,200 dependiendo del alcance.")
        ],
        "projects_title": "🏆 Nuestros proyectos y logros",
        "projects_sub": "Soluciones de software completas entregadas a los clientes – listas para comprar o personalizar.",
        "project_haiti": "🇭🇹 Software de votación en línea Haití",
        "project_haiti_desc": "Sistema electoral presidencial completo con soporte multilingüe (criollo, francés, inglés, español), monitoreo en vivo, panel del presidente del CEP (gestión de candidatos, carga de fotos, informes de progreso), voto secreto y contraseñas modificables. Utilizado para elecciones nacionales.",
        "project_haiti_price": "$2,000 USD (pago único)",
        "project_haiti_status": "✅ Disponible – incluye código fuente, instalación y soporte.",
        "project_haiti_contact": "Contacte al propietario para comprar",
        "project_dashboard": "📊 Panel de inteligencia empresarial",
        "project_dashboard_desc": "Panel de análisis en tiempo real para empresas. Conéctese a cualquier base de datos (SQL, Excel, CSV) y visualice KPI, tendencias de ventas, inventario e informes personalizados. Totalmente interactivo y personalizable.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Disponible",
        "project_dashboard_contact": "Contacte al propietario para comprar",
        "project_chatbot": "🤖 Chatbot de soporte al cliente con IA",
        "project_chatbot_desc": "Chatbot inteligente entrenado con sus datos comerciales. Responda preguntas de clientes 24/7, reduzca la carga de soporte. Se integra con sitios web, WhatsApp o Telegram. Construido con Python y NLP moderno.",
        "project_chatbot_price": "$800 USD (básico) / $1,500 USD (avanzado)",
        "project_chatbot_status": "✅ Disponible",
        "project_chatbot_contact": "Contacte al propietario para comprar",
        "project_school": "🏫 Sistema de gestión escolar",
        "project_school_desc": "Plataforma completa para escuelas: registro de estudiantes, gestión de calificaciones, seguimiento de asistencia, portal para padres, generación de boletas y cobro de tarifas. Roles multi‑usuario (admin, profesores, padres).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Disponible",
        "project_school_contact": "Contacte al propietario para comprar",
        "project_pos": "📦 Sistema de inventario y punto de venta",
        "project_pos_desc": "Gestión de inventario web con punto de venta para pequeñas empresas. Escaneo de códigos de barras, alertas de stock, informes de ventas, gestión de proveedores. Funciona en línea y sin conexión.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Disponible",
        "project_pos_contact": "Contacte al propietario para comprar",
        "project_scraper": "📈 Extractor web personalizado y tubería de datos",
        "project_scraper_desc": "Extracción automatizada de datos de cualquier sitio web, limpia y entregada como Excel/JSON/CSV. Programe ejecuciones diarias, semanales o mensuales. Perfecto para investigación de mercado, monitoreo de precios o generación de leads.",
        "project_scraper_price": "$500 – $2,000 (depende de la complejidad)",
        "project_scraper_status": "✅ Disponible",
        "project_scraper_contact": "Contacte al propietario para comprar",
        "project_chess": "♟️ Juega al ajedrez contra la máquina",
        "project_chess_desc": "Juego de ajedrez educativo con oponente IA (3 niveles de dificultad). Cada movimiento se explica – aprenda tácticas como horquillas, clavadas y jaques descubiertos. Incluye modo demo, panel de movimientos y descarga del informe completo. Multilingüe (inglés, francés, español, criollo).",
        "project_chess_price": "$20 USD (pago único)",
        "project_chess_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_chess_contact": "Contacte al propietario para comprar",
        "project_accountant": "🧮 Contador Excel avanzado con IA",
        "project_accountant_desc": "Suite profesional de contabilidad y gestión de préstamos. Seguimiento de ingresos/gastos, gestión de préstamos (prestatarios, fechas de vencimiento, pagos), panel con saldo, exportación de todos los informes a Excel y PDF. Multilingüe (inglés, francés, español).",
        "project_accountant_price": "$199 USD (pago único)",
        "project_accountant_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_accountant_contact": "Contacte al propietario para comprar",
        "project_archives": "📜 Base de datos de Archivos Nacionales de Haití",
        "project_archives_desc": "Base de datos completa de archivos nacionales para ciudadanos haitianos. Almacena NIF (Matrícula Fiscal), CIN, Pasaporte, Licencia de Conducir, historial de votación, patrocinios y cargas de documentos. Validación de firma ministerial, sistema de contraseña anual, multilingüe (inglés, francés, español, criollo).",
        "project_archives_price": "$1,500 USD (pago único)",
        "project_archives_status": "✅ Disponible – incluye código fuente, instalación y soporte",
        "project_archives_contact": "Contacte al propietario para comprar",
        "project_dsm": "🛡️ DSM-2026: SISTEMA SEGURADO",
        "project_dsm_desc": "Radar avanzado de monitoreo de estratosfera – rastrea aviones, satélites y misiles en tiempo real. Pantalla de radar simulada con detección de amenazas, soporte multilingüe e informes de inteligencia descargables.",
        "project_dsm_price": "$299 USD (pago único)",
        "project_dsm_status": "✅ Disponible – licencia de por vida, actualizaciones gratuitas",
        "project_dsm_contact": "Contacte al propietario para comprar",
        "project_bi": "📊 Panel de inteligencia empresarial",
        "project_bi_desc": "Panel de análisis en tiempo real para empresas. Conecte SQL, Excel, CSV – visualice KPI, tendencias de ventas, inventario y rendimiento regional. Totalmente interactivo con filtros de fecha e informes CSV descargables. Multilingüe (inglés, francés, español, criollo).",
        "project_bi_price": "$1,200 USD (pago único)",
        "project_bi_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_bi_contact": "Contacte al propietario para comprar",
        "project_ai_classifier": "🧠 Clasificador de imágenes con IA (MobileNetV2)",
        "project_ai_classifier_desc": "Sube una imagen y la IA la identifica entre 1000 categorías (animales, vehículos, comida, objetos cotidianos). Utiliza TensorFlow MobileNetV2 preentrenado en ImageNet. Multilingüe, protegido por contraseña, demo lista.",
        "project_ai_classifier_price": "$1,200 USD (pago único)",
        "project_ai_classifier_status": "✅ Disponible – incluye código fuente, instalación y soporte",
        "project_ai_classifier_contact": "Contacte al propietario para comprar",
        "project_task_manager": "🗂️ Panel de gestión de tareas",
        "project_task_manager_desc": "Gestiona tareas, rastrea el progreso y analiza la productividad con gráficos en tiempo real y modo oscuro. Inspirado en la interfaz basada en componentes de React. Multilingüe, almacenamiento persistente, panel analítico.",
        "project_task_manager_price": "$1,200 USD (pago único)",
        "project_task_manager_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_task_manager_contact": "Contacte al propietario para comprar",
        "project_ray": "⚡ Procesador de texto paralelo Ray",
        "project_ray_desc": "Procesa texto en paralelo en múltiples núcleos de CPU. Compara la velocidad de ejecución secuencial vs paralela. Inspirado en el framework de computación distribuida Ray de UC Berkeley.",
        "project_ray_price": "$1,200 USD (pago único)",
        "project_ray_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_ray_contact": "Contacte al propietario para comprar",
        "project_cassandra": "🗄️ Panel de datos Cassandra",
        "project_cassandra_desc": "Demostración de base de datos NoSQL distribuida. Agrega pedidos, busca por cliente y explora análisis en tiempo real. Modelado según Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "$1,200 USD (pago único)",
        "project_cassandra_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_cassandra_contact": "Contacte al propietario para comprar",
        "project_spark": "🌊 Procesador de datos Apache Spark",
        "project_spark_desc": "Sube un archivo CSV y ejecuta agregaciones tipo SQL (group by, sum, avg, count) usando Spark. Resultados y gráficos en tiempo real. Inspirado en el motor de big data utilizado por miles de empresas.",
        "project_spark_price": "$1,200 USD (pago único)",
        "project_spark_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_spark_contact": "Contacte al propietario para comprar",
        "project_drone": "🚁 Comandante de dron haitiano",
        "project_drone_desc": "Controla el primer dron fabricado en Haití desde tu teléfono. Modo simulación, soporte real de dron (MAVLink), armar, despegar, aterrizar, volar a coordenadas GPS, telemetría en vivo, historial de comandos. Multilingüe, panel profesional.",
        "project_drone_price": "$2,000 USD (pago único)",
        "project_drone_status": "✅ Disponible – incluye código fuente, instalación y 1 año de soporte",
        "project_drone_contact": "Contacte al propietario para comprar",
        "project_english": "🇬🇧 Aprendamos inglés con Gesner",
        "project_english_desc": "Aplicación interactiva de aprendizaje de inglés. Cubre vocabulario, gramática, pronunciación y práctica de conversación. Interfaz multilingüe, seguimiento de progreso, cuestionarios y certificados. Perfecto para principiantes y estudiantes intermedios.",
        "project_english_price": "$299 USD (pago único)",
        "project_english_status": "✅ Disponible – incluye código fuente, instalación y soporte",
        "project_english_contact": "Contacte al propietario para comprar",
        "project_spanish": "🇪🇸 Aprendamos español con Gesner",
        "project_spanish_desc": "Plataforma completa de aprendizaje de español. Lecciones sobre vocabulario, conjugaciones verbales, comprensión auditiva y notas culturales. Incluye ejercicios interactivos, reconocimiento de voz y panel de progreso.",
        "project_spanish_price": "$299 USD (pago único)",
        "project_spanish_status": "✅ Disponible – incluye código fuente, instalación y soporte",
        "project_spanish_contact": "Contacte al propietario para comprar",
        "project_portuguese": "🇵🇹 Aprendamos portugués con Gesner",
        "project_portuguese_desc": "Aplicación de aprendizaje de portugués brasileño y europeo. Cubre frases esenciales, gramática, tiempos verbales y diálogos de la vida real. Incluye tarjetas didácticas, guía de pronunciación e insignias de logro. Soporte multilingüe.",
        "project_portuguese_price": "$299 USD (pago único)",
        "project_portuguese_status": "✅ Disponible – incluye código fuente, instalación y soporte",
        "project_portuguese_contact": "Contacte al propietario para comprar",
        "project_ai_career": "🚀 Entrenador de carrera con IA – Optimizador de CV",
        "project_ai_career_desc": "**Optimiza tu CV y triunfa en entrevistas con IA.** Sube tu CV y una descripción de trabajo – nuestra IA analiza ambos y proporciona: palabras clave a añadir, mejoras de habilidades, sugerencias de formato y preguntas de entrevista predichas. Perfecto para buscadores de empleo, estudiantes y profesionales. Código fuente completo incluido.",
        "project_ai_career_price": "$149 USD (pago único)",
        "project_ai_career_status": "✅ Disponible – código fuente completo incluido",
        "project_ai_career_contact": "Contacte al propietario para comprar",
        "project_ai_medical": "🧪 Asistente de literatura médica y científica con IA",
        "project_ai_medical_desc": "**Haz cualquier pregunta médica o científica – obtén respuestas respaldadas por investigaciones reales.** Nuestra IA busca en PubMed, la base de datos más grande de literatura médica, recupera resúmenes relevantes y genera respuestas basadas en evidencia con citas y enlaces directos. Código fuente completo incluido.",
        "project_ai_medical_price": "$149 USD (pago único)",
        "project_ai_medical_status": "✅ Disponible – código fuente completo incluido",
        "project_ai_medical_contact": "Contacte al propietario para comprar",
        "project_music_studio": "🎧 Music Studio Pro – Suite completa de producción musical",
        "project_music_studio_desc": "**Software profesional de producción musical** – graba, mezcla y crea ritmos. Incluye grabación de voz, efectos de estudio (EQ, compresor, reverberación, corrección de tono), creador de ritmos multipista, bucles continuos, grabación de voz sobre pistas, corrector automático. Código fuente completo incluido.",
        "project_music_studio_price": "$299 USD (pago único)",
        "project_music_studio_status": "✅ Disponible – código fuente completo incluido",
        "project_music_studio_contact": "Contacte al propietario para comprar",
        "project_ai_media": "🎭 Estudio multimedia con IA – Editor de fotos y videos parlantes",
        "project_ai_media_desc": "**Crea videos profesionales a partir de fotos, audio o clips de video.** Cuatro modos potentes: foto + voz, foto + audio subido, foto + música de fondo, video + música de fondo. Código fuente completo incluido.",
        "project_ai_media_price": "$149 USD (pago único)",
        "project_ai_media_status": "✅ Disponible – código fuente completo incluido",
        "project_ai_media_contact": "Contacte al propietario para comprar",
        "project_chinese": "🇨🇳 Aprendamos chino con Gesner – Libro 1",
        "project_chinese_desc": "**Curso completo de mandarín para principiantes.** 20 lecciones interactivas sobre conversaciones diarias, vocabulario, gramática, pronunciación y cuestionarios. Código fuente completo incluido.",
        "project_chinese_price": "$299 USD (pago único)",
        "project_chinese_status": "✅ Disponible – código fuente completo incluido",
        "project_chinese_contact": "Contacte al propietario para comprar",
        "project_french": "🇫🇷 Aprendamos francés con Gesner – Libro 1",
        "project_french_desc": "**Curso completo de francés para principiantes.** 20 lecciones interactivas sobre conversaciones diarias, vocabulario, gramática, pronunciación y cuestionarios. Código fuente completo incluido.",
        "project_french_price": "$299 USD (pago único)",
        "project_french_status": "✅ Disponible – código fuente completo incluido",
        "project_french_contact": "Contacte al propietario para comprar",
        "project_mathematics": "📐 Aprendamos matemáticas con Gesner – Libro 1",
        "project_mathematics_desc": "**Curso completo de matemáticas para principiantes.** 20 lecciones que cubren aritmética básica, geometría, fracciones, decimales, porcentajes, problemas verbales y más. Código fuente completo incluido.",
        "project_mathematics_price": "$299 USD (pago único)",
        "project_mathematics_status": "✅ Disponible – código fuente completo incluido",
        "project_mathematics_contact": "Contacte al propietario para comprar",
        "project_ai_course": "🤖 Curso Fundamentos de IA y certificación",
        "project_ai_course_desc": "**Curso de maestría en IA de 28 días – de principiante a experto certificado.** Aprende ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, y más. Código fuente completo incluido.",
        "project_ai_course_price": "$299 USD (pago único)",
        "project_ai_course_status": "✅ Disponible – código fuente completo incluido",
        "project_ai_course_contact": "Contacte al propietario para comprar",
        "project_medical_term": "🩺 Libro de terminología médica para traductores",
        "project_medical_term_desc": "**Capacitación interactiva en terminología médica para intérpretes y profesionales de la salud.** 20 lecciones basadas en conversaciones reales médico‑paciente, audio con voz nativa y práctica de traducción. Código fuente completo incluido.",
        "project_medical_term_price": "$299 USD (pago único)",
        "project_medical_term_status": "✅ Disponible – código fuente completo incluido",
        "project_medical_term_contact": "Contacte al propietario para comprar",
        "project_python_course": "🐍 Aprendamos a programar en Python con Gesner",
        "project_python_course_desc": "**Curso completo de programación Python – desde principiante hasta avanzado.** 20 lecciones interactivas con código de demostración, 5 ejercicios prácticos por lección y soporte de audio. Código fuente completo incluido.",
        "project_python_course_price": "$299 USD (pago único)",
        "project_python_course_status": "✅ Disponible – código fuente completo incluido",
        "project_python_course_contact": "Contacte al propietario para comprar",
        "project_hardware_course": "🔌 Aprendamos a conectar software y hardware con Gesner",
        "project_hardware_course_desc": "**Conecte software con 20 componentes de hardware – proyectos IoT y robótica.** 20 lecciones que cubren tarjetas de red, Wi‑Fi, Bluetooth, GPS, GPIO, sensores, motores, pantallas, etc. Código fuente completo incluido.",
        "project_hardware_course_price": "$299 USD (pago único)",
        "project_hardware_course_status": "✅ Disponible – código fuente completo incluido",
        "project_hardware_course_contact": "Contacte al propietario para comprar",
        "view_demo": "🎬 Ver demostración",
        "demo_screenshot": "Vista previa de captura de pantalla (reemplazar con imagen real)",
        "live_demo": "🔗 Demostración en vivo",
        "demo_password_hint": "🔐 Contraseña de demostración: 20082010",
        "request_info": "Solicitar información",
        "buy_now": "💵 Comprar ahora",
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
        "footer_pride": "🇭🇹 Orgullosamente haitiano – sirviendo al mundo con Python e IA 🇭🇹"
    },
    "ht": {
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Konstwi avèk Python. Livre vit. Innove avèk AI.",
        "hero_desc": "Soti Ayiti rive nan lemonn – lojisyèl sou miz ki mache sou entènèt.",
        "about_title": "👨‍💻 Konsènan Konpayi an",
        "about_text": """
        **GlobalInternet.py** te fonde pa **Gesner Deslandes** – pwopriyetè, fondatè, ak enjenyè anch.  
        Nou konstwi **lojisyèl ki baze sou Python** sou demann pou kliyan atravè lemonn. Tankou Silisyòm, men ak yon manyen Ayisyen ak rezilta eksepsyonèl.
        
        - 🧠 **Solisyon ki mache ak AI** – chatbots, analiz done, otomatizasyon  
        - 🗳️ **Sistèm elektoral konplè** – sekirize, miltilang, an tan reyèl  
        - 🌐 **Aplikasyon entènèt** – tablodbò, zouti entèn, platfòm sou entènèt  
        - 📦 **Livre konplè** – nou voye kòd konplè a ba ou pa imel epi nou gide ou nan enstalasyon an
        
        Kit ou bezwen yon sit entènèt konpayi, yon zouti lojisyèl pèsonalize, oswa yon platfòm sou entènèt gwo echèl – nou konstwi li, se pou ou.
        """,
        "office_photo_caption": "Avatar k ap pale Gesner Deslandes – prezante GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – reprezantan dijital nou an nan inovasyon ak ekspètiz lojisyèl.",
        "founder": "Fondatè ak CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Enjenyè | Amater AI | Ekspè Python",
        "cv_title": "📄 Konsènan pwopriyetè a – Gesner Deslandes",
        "cv_intro": "Konstriktè lojisyèl Python | Devlòpè entènèt | Koòdonatè teknoloji",
        "cv_summary": """
        Lidè ak administratè ki gen anpil motivasyon, angaje nan ekselans ak presizyon.  
        **Konpetans prensipal:** Lidèchip, Entèpretasyon (angle, franse, kreyòl ayisyen), Oryantasyon mekanik, Jesyon, Microsoft Office.
        """,
        "cv_experience_title": "💼 Eksperyans pwofesyonèl",
        "cv_experience": """
        **Koòdonatè teknoloji** – Orfelina Be Like Brit (2021–prezan)  
        Mete sou pye reyinyon Zoom, antretyen laptops/tablet, sipò teknik chak jou, asire operasyon dijital lis.

        **CEO ak sèvis entèpretasyon** – Touris pèsonalize pou gwoup ONG, ekip misyon, ak moun.

        **Manadjè flòt / Dispatcher** – J/P Haitian Relief Organization  
        Jere plis pase 20 veyikil, jounal kondiktè, orè antretyen lè l sèvi avèk Excel.

        **Entèprèt medikal** – International Child Care  
        Entèpretasyon medikal egzak angle–franse–kreyòl.

        **Lidè ekip ak entèprèt** – Can‑Do NGO  
        Dirije pwojè rekonstriksyon.

        **Pwofesè angle** – Be Like Brit (prèskolè rive NS4)

        **Tradiktè dokiman** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Edikasyon ak fòmasyon",
        "cv_education": """
        - Lekòl fòmasyon pwofesyonèl – Angle Ameriken  
        - Enstiti dyezèl Ayiti – Mekanisyen dyezèl  
        - Sètifikasyon enfòmatik (Oktòb 2000)  
        - Diplome lekòl segondè
        """,
        "cv_references": "📞 Referans disponib sou demann.",
        "team_title": "👥 Ekip nou an",
        "team_sub": "Rankontre moun talan dèyè GlobalInternet.py – anboche Avril 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fondatè ak CEO", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Asistan CEO", "since": "Avril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Pwogramè Python", "since": "Avril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Pwogramè Python", "since": "Avril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Sekretè", "since": "Avril 2026"}
        ],
        "services_title": "⚙️ Sèvis nou yo",
        "services": [
            ("🐍 Devlopman Python pèsonalize", "Script sou miz, otomatizasyon, sistèm backend."),
            ("🤖 AI ak aprantisaj machin", "Chatbots, modèl prediktif, analiz done."),
            ("🗳️ Lojisyèl elektoral", "Sekirize, miltilang, rezilta an dirèk – tankou sistèm Ayiti nou an."),
            ("📊 Tablodbò biznis", "Analitik an tan reyèl ak zouti rapò."),
            ("🌐 Sit entènèt ak aplikasyon entènèt", "Solisyon full‑stack deplwaye sou entènèt."),
            ("📦 Livrezon 24 èdtan", "Nou travay vit – resevwa lojisyèl ou an pa imel, pare pou itilize."),
            ("📢 Piblisite ak maketing", "Kampay dijital, jesyon medya sosyal, sibay ki mache ak AI, rapò pèfòmans. Soti $150 rive $1,200 selon dimansyon an.")
        ],
        "projects_title": "🏆 Pwojè ak akonplisman nou yo",
        "projects_sub": "Solisyon lojisyèl konplè livrezon bay kliyan – pare pou achte oswa pèsonalize.",
        "project_haiti": "🇭🇹 Lojisyèl vòt sou entènèt Ayiti",
        "project_haiti_desc": "Sistèm elektoral prezidansyèl konplè ak sipò miltilang (Kreyòl, Franse, Angle, Panyòl), siveyans an dirèk, tablodbò Prezidan CEP (jere kandida, telechaje foto, rapò pwogrè), bilten vòt sekrè, ak modpas ki ka chanje. Itilize pou eleksyon nasyonal.",
        "project_haiti_price": "$2,000 USD (peman inik)",
        "project_haiti_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_haiti_contact": "Kontakte pwopriyetè a pou achte",
        "project_dashboard": "📊 Tablodbò entèlijans biznis",
        "project_dashboard_desc": "Tablodbò analitik an tan reyèl pou konpayi. Konekte ak nenpòt baz done (SQL, Excel, CSV) ak visualize KPI, tandans lavant, envantè, ak rapò pèsonalize. Entèaktif totalman ak pèsonalizab.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Disponib",
        "project_dashboard_contact": "Kontakte pwopriyetè a pou achte",
        "project_chatbot": "🤖 Chatbot sipò kliyan AI",
        "project_chatbot_desc": "Chatbot entèlijan ki antrene sou done biznis ou. Reponn kesyon kliyan 24/7, diminye chaj sipò. Entegre ak sit entènèt, WhatsApp, oswa Telegram. Bati ak Python ak NLP modèn.",
        "project_chatbot_price": "$800 USD (debaz) / $1,500 USD (avanse)",
        "project_chatbot_status": "✅ Disponib",
        "project_chatbot_contact": "Kontakte pwopriyetè a pou achte",
        "project_school": "🏫 Sistèm jesyon lekòl",
        "project_school_desc": "Platfòm konplè pou lekòl: enskripsyon elèv, jesyon nòt, swivi prezans, portal paran, jenere rapò, ak pèsepsyon frè. Wòl milti‑itilizatè (admin, pwofesè, paran).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Disponib",
        "project_school_contact": "Kontakte pwopriyetè a pou achte",
        "project_pos": "📦 Sistèm envantè ak pwen vant",
        "project_pos_desc": "Jesyon envantè sou entènèt ak pwen vant pou ti biznis. Eskane kòd ba, alèt stock, rapò lavant, jesyon founisè. Travay sou entènèt ak san entènèt.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Disponib",
        "project_pos_contact": "Kontakte pwopriyetè a pou achte",
        "project_scraper": "📈 Ekstraktè entènèt pèsonalize ak tiyo done",
        "project_scraper_desc": "Ekstraksyon done otomatik nan nenpòt sit entènèt, netwaye ak livre kòm Excel/JSON/CSV. Planifye kouri chak jou, chak semenn, oswa chak mwa. Pafè pou rechèch mache, siveyans pri, oswa jenerasyon leads.",
        "project_scraper_price": "$500 – $2,000 (depann sou konpleksite)",
        "project_scraper_status": "✅ Disponib",
        "project_scraper_contact": "Kontakte pwopriyetè a pou achte",
        "project_chess": "♟️ Jwe echèk kont machin nan",
        "project_chess_desc": "Jwèt echèk edikatif ak opozan AI (3 nivo difikilte). Chak mouvman eksplike – aprann taktik tankou fouchèt, klou, ak echèk dekouvri. Gen ladan mod demosyon, tablodbò mouvman, ak telechajman rapò konplè. Miltilang (Angle, Franse, Panyòl, Kreyòl).",
        "project_chess_price": "$20 USD (peman inik)",
        "project_chess_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_chess_contact": "Kontakte pwopriyetè a pou achte",
        "project_accountant": "🧮 Kontab Excel avanse AI",
        "project_accountant_desc": "Gwoup pwofesyonèl kontablite ak jesyon prè. Swivi revni/depans, jere prè (moun k ap prete, dat limit, peman), tablodbò ak balans, ekspòte tout rapò nan Excel ak PDF. Miltilang (Angle, Franse, Panyòl).",
        "project_accountant_price": "$199 USD (peman inik)",
        "project_accountant_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_accountant_contact": "Kontakte pwopriyetè a pou achte",
        "project_archives": "📜 Baz done Achiv Nasyonal Ayiti",
        "project_archives_desc": "Baz done konplè achiv nasyonal pou sitwayen Ayisyen. Sere NIF (Matrikil Fiskal), CIN, Paspò, Pèmi Kondwi, istwa vòt, parennaj, ak telechajman dokiman. Validasyon siyati minis, sistèm modpas anyèl, miltilang (Angle, Franse, Panyòl, Kreyòl).",
        "project_archives_price": "$1,500 USD (peman inik)",
        "project_archives_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_archives_contact": "Kontakte pwopriyetè a pou achte",
        "project_dsm": "🛡️ DSM-2026: SISTÈM SEKIRIZE",
        "project_dsm_desc": "Radar avanse siveyans stratosfè – swivi avyon, satelit, ak misil an tan reyèl. Ekspozisyon radar simulation ak deteksyon menas, sipò miltilang, ak rapò entèlijans telechajab.",
        "project_dsm_price": "$299 USD (peman inik)",
        "project_dsm_status": "✅ Disponib – lisans pou tout lavi, mizajou gratis",
        "project_dsm_contact": "Kontakte pwopriyetè a pou achte",
        "project_bi": "📊 Tablodbò entèlijans biznis",
        "project_bi_desc": "Tablodbò analitik an tan reyèl pou konpayi. Konekte SQL, Excel, CSV – visualize KPI, tandans lavant, envantè, ak pèfòmans rejyonal. Entèaktif totalman ak filt dat ak rapò CSV telechajab. Miltilang (Angle, Franse, Panyòl, Kreyòl).",
        "project_bi_price": "$1,200 USD (peman inik)",
        "project_bi_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_bi_contact": "Kontakte pwopriyetè a pou achte",
        "project_ai_classifier": "🧠 Klasifikatè imaj AI (MobileNetV2)",
        "project_ai_classifier_desc": "Telechaje yon imaj epi AI idantifye li nan 1000 kategori (bèt, veyikil, manje, objè chak jou). Sèvi ak TensorFlow MobileNetV2 pre-antrene sou ImageNet. Miltilang, pwoteje pa modpas, demo pare.",
        "project_ai_classifier_price": "$1,200 USD (peman inik)",
        "project_ai_classifier_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_ai_classifier_contact": "Kontakte pwopriyetè a pou achte",
        "project_task_manager": "🗂️ Tablodbò jesyon travay",
        "project_task_manager_desc": "Jere travay, swivi pwogrè, ak analize pwodiktivite ak grafik an tan reyèl ak mòd nwa. Enspire pa koòdone ki baze sou eleman React. Miltilang, depo ki pèsiste, tablodbò analitik.",
        "project_task_manager_price": "$1,200 USD (peman inik)",
        "project_task_manager_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_task_manager_contact": "Kontakte pwopriyetè a pou achte",
        "project_ray": "⚡ Processeurs tèks paralèl Ray",
        "project_ray_desc": "Trete tèks an paralèl sou plizyè nwayo CPU. Konpare vitès ekzekisyon sekansyèl vs paralèl. Enspire pa fondasyon informatique distribué Ray nan UC Berkeley.",
        "project_ray_price": "$1,200 USD (peman inik)",
        "project_ray_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_ray_contact": "Kontakte pwopriyetè a pou achte",
        "project_cassandra": "🗄️ Tablodbò done Cassandra",
        "project_cassandra_desc": "Demostrasyon baz done NoSQL distribye. Ajoute lòd, chèche pa kliyan, ak eksplore analitik an tan reyèl. Modelize daprè Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "$1,200 USD (peman inik)",
        "project_cassandra_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_cassandra_contact": "Kontakte pwopriyetè a pou achte",
        "project_spark": "🌊 Processeurs done Apache Spark",
        "project_spark_desc": "Telechaje yon dosye CSV epi kouri agrega ki tankou SQL (group by, sum, avg, count) lè l sèvi avèk Spark. Rezilta ak grafik an tan reyèl. Enspire pa motè big data ke dè milye de konpayi itilize.",
        "project_spark_price": "$1,200 USD (peman inik)",
        "project_spark_status": "✅ Disponib – aksè pou tout lavi, mizajou gratis",
        "project_spark_contact": "Kontakte pwopriyetè a pou achte",
        "project_drone": "🚁 Kòmandan dron Ayisyen",
        "project_drone_desc": "Kontwole premye dron ki fèt an Ayiti apati telefòn ou. Mòd simulation, sipò dron reyèl (MAVLink), arme, dekolaj, aterisaj, vole nan kowòdone GPS, télémétrie an dirèk, istwa kòmand. Miltilang, tablodbò pwofesyonèl.",
        "project_drone_price": "$2,000 USD (peman inik)",
        "project_drone_status": "✅ Disponib – kòd sous, enstalasyon, ak 1 ane sipò enkli",
        "project_drone_contact": "Kontakte pwopriyetè a pou achte",
        "project_english": "🇬🇧 Annou aprann angle ak Gesner",
        "project_english_desc": "Aplikasyon entèaktif aprantisaj angle. Kouvri vokabilè, gramè, pwononsyasyon, ak pratik konvèsasyon. Koòdone miltilang, swivi pwogrè, kesyon, ak sètifika. Pafè pou débutan ak aprann entèmedyè.",
        "project_english_price": "$299 USD (peman inik)",
        "project_english_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_english_contact": "Kontakte pwopriyetè a pou achte",
        "project_spanish": "🇪🇸 Annou aprann panyòl ak Gesner",
        "project_spanish_desc": "Platfòm aprantisaj panyòl konplè. Lesyon sou vokabilè, konjigezon vèb, konpreyansyon oditif, ak nòt kiltirèl. Gen ladan egzèsis entèaktif, rekonesans vokal, ak tablodbò pwogrè.",
        "project_spanish_price": "$299 USD (peman inik)",
        "project_spanish_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_spanish_contact": "Kontakte pwopriyetè a pou achte",
        "project_portuguese": "🇵🇹 Annou aprann pòtigè ak Gesner",
        "project_portuguese_desc": "Aplikasyon aprantisaj pòtigè brezilyen ak ewopeyen. Kouvri fraz esansyèl, gramè, tan vèb, ak dyalòg lavi reyèl. Gen ladan fich didaktik, gid pwononsyasyon, ak badj reyalizasyon. Sipò miltilang.",
        "project_portuguese_price": "$299 USD (peman inik)",
        "project_portuguese_status": "✅ Disponib – kòd sous, enstalasyon, ak sipò enkli",
        "project_portuguese_contact": "Kontakte pwopriyetè a pou achte",
        "project_ai_career": "🚀 Koòch karyè AI – Optimizeur CV",
        "project_ai_career_desc": "**Optimize CV ou a ak reyisi antrevi ak AI.** Telechaje CV ou ak yon deskripsyon travay – AI nou an analize tou de epi bay: mo kle pou ajoute, amelyorasyon konpetans, sijesyon fòma, ak kesyon antrevi prevwa. Pafè pou moun k ap chèche travay, elèv, ak pwofesyonèl. Kòd sous konplè enkli.",
        "project_ai_career_price": "$149 USD (peman inik)",
        "project_ai_career_status": "✅ Disponib – kòd sous konplè enkli",
        "project_ai_career_contact": "Kontakte pwopriyetè a pou achte",
        "project_ai_medical": "🧪 Asistan literati medikal ak syantifik AI",
        "project_ai_medical_desc": "**Poze nenpòt kesyon medikal oswa syantifik – jwenn repons ki baze sou rechèch reyèl.** AI nou an fouye nan PubMed, pi gwo baz done literati medikal, rekipere rezime ki enpòtan, ak jenere repons ki baze sou prèv ak sitasyon ak lyen dirèk. Kòd sous konplè enkli.",
        "project_ai_medical_price": "$149 USD (peman inik)",
        "project_ai_medical_status": "✅ Disponib – kòd sous konplè enkli",
        "project_ai_medical_contact": "Kontakte pwopriyetè a pou achte",
        "project_music_studio": "🎧 Music Studio Pro – Gwoup konplè pwodiksyon mizik",
        "project_music_studio_desc": "**Lojisyèl pwodiksyon mizik pwofesyonèl** – anrejistre, melanje, ak kreye rit. Gen ladan anrejistreman vwa, efè estidyo (EQ, COMPRESSOR, reverb, korèksyon ton), kreyatè rit milti‑track, bouk kontinyèl, anrejistreman vwa sou track, korèktè otomatik. Kòd sous konplè enkli.",
        "project_music_studio_price": "$299 USD (peman inik)",
        "project_music_studio_status": "✅ Disponib – kòd sous konplè enkli",
        "project_music_studio_contact": "Kontakte pwopriyetè a pou achte",
        "project_ai_media": "🎭 Studio medya AI – Editè foto ak videyo k ap pale",
        "project_ai_media_desc": "**Kreye videyo pwofesyonèl apati foto, odyo, oswa klip videyo.** Kat mòd pwisan: foto + lapawòl, foto + odyo telechaje, foto + mizik anba, videyo + mizik anba. Kòd sous konplè enkli.",
        "project_ai_media_price": "$149 USD (peman inik)",
        "project_ai_media_status": "✅ Disponib – kòd sous konplè enkli",
        "project_ai_media_contact": "Kontakte pwopriyetè a pou achte",
        "project_chinese": "🇨🇳 Annou aprann Chinwa ak Gesner – Liv 1",
        "project_chinese_desc": "**Kou konplè mandaren pou débutan.** 20 lesyon entèaktif sou konvèsasyon chak jou, vokabilè, gramè, pwononsyasyon, ak kesyon. Kòd sous konplè enkli.",
        "project_chinese_price": "$299 USD (peman inik)",
        "project_chinese_status": "✅ Disponib – kòd sous konplè enkli",
        "project_chinese_contact": "Kontakte pwopriyetè a pou achte",
        "project_french": "🇫🇷 Annou aprann Franse ak Gesner – Liv 1",
        "project_french_desc": "**Kou konplè franse pou débutan.** 20 lesyon entèaktif sou konvèsasyon chak jou, vokabilè, gramè, pwononsyasyon, ak kesyon. Kòd sous konplè enkli.",
        "project_french_price": "$299 USD (peman inik)",
        "project_french_status": "✅ Disponib – kòd sous konplè enkli",
        "project_french_contact": "Kontakte pwopriyetè a pou achte",
        "project_mathematics": "📐 Annou aprann Matematik ak Gesner – Liv 1",
        "project_mathematics_desc": "**Kou konplè matematik pou débutan.** 20 lesyon ki kouvri aritmetik debaz, jeyometri, fraksyon, desimal, pousantaj, pwoblèm mo, ak plis ankò. Kòd sous konplè enkli.",
        "project_mathematics_price": "$299 USD (peman inik)",
        "project_mathematics_status": "✅ Disponib – kòd sous konplè enkli",
        "project_mathematics_contact": "Kontakte pwopriyetè a pou achte",
        "project_ai_course": "🤖 Kou Fondasyon AI ak sètifikasyon",
        "project_ai_course_desc": "**Kou metrize AI 28 jou – soti débutan rive ekspè sètifye.** Aprann ChatGPT, Gemini, MidJourney, Runway, ElevenLabs, Make.com, ak plis ankò. Kòd sous konplè enkli.",
        "project_ai_course_price": "$299 USD (peman inik)",
        "project_ai_course_status": "✅ Disponib – kòd sous konplè enkli",
        "project_ai_course_contact": "Kontakte pwopriyetè a pou achte",
        "project_medical_term": "🩺 Liv Tèminoloji Medikal pou Tradiktè",
        "project_medical_term_desc": "**Fòmasyon entèaktif sou tèminoloji medikal pou entèprèt ak pwofesyonèl sante.** 20 lesyon ki baze sou konvèsasyon reyèl doktè‑pasyan, odyo vwa natif natal, ak pratik tradiksyon. Kòd sous konplè enkli.",
        "project_medical_term_price": "$299 USD (peman inik)",
        "project_medical_term_status": "✅ Disponib – kòd sous konplè enkli",
        "project_medical_term_contact": "Kontakte pwopriyetè a pou achte",
        "project_python_course": "🐍 Annou aprann kode an Python ak Gesner",
        "project_python_course_desc": "**Kou konplè pwogramasyon Python – soti débutan rive avanse.** 20 lesyon entèaktif ak kòd demonstrasyon, 5 egzèsis pratik pa lesyon ak sipò odyo. Kòd sous konplè enkli.",
        "project_python_course_price": "$299 USD (peman inik)",
        "project_python_course_status": "✅ Disponib – kòd sous konplè enkli",
        "project_python_course_contact": "Kontakte pwopriyetè a pou achte",
        "project_hardware_course": "🔌 Annou aprann konekte lojisyèl ak pyès medam ak Gesner",
        "project_hardware_course_desc": "**Konekte lojisyèl ak 20 pyès medam – pwojè IoT ak robotik.** 20 lesyon sou kat rezo, Wi‑Fi, Bluetooth, GPS, GPIO, detèktè, motè, ekran, elatriye. Kòd sous konplè enkli.",
        "project_hardware_course_price": "$299 USD (peman inik)",
        "project_hardware_course_status": "✅ Disponib – kòd sous konplè enkli",
        "project_hardware_course_contact": "Kontakte pwopriyetè a pou achte",
        "view_demo": "🎬 Gade demo",
        "demo_screenshot": "Previsualisation ekran (ranplase ak imaj reyèl)",
        "live_demo": "🔗 Demo an dirèk",
        "demo_password_hint": "🔐 Modpas demo: 20082010",
        "request_info": "Mande enfòmasyon",
        "buy_now": "💵 Achte kounye a",
        "donation_title": "💖 Sipòte GlobalInternet.py",
        "donation_text": "Ede nou grandi epi kontinye bati lojisyèl inovatè pou Ayiti ak lemonn.",
        "donation_sub": "Donasyon ou a sipòte hosting, zouti devlopman, ak resous gratis pou devlopè lokal yo.",
        "donation_method": "🇭🇹 Fasil ak rapid – Transfer Prisme nan Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limit kantite lajan: Jiska 100,000 HTG pou chak tranzaksyon",
        "donation_instruction": "Sèvi ak fonksyon 'Transfer Prisme' nan aplikasyon Moncash ou a pou voye kontribisyon ou a Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Veso entènasyonal atravè <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Voye lajan dirèkteman nan nimewo telefòn nou an lè l sèvi avèk aplikasyon SendWave (disponib atravè lemonn).",
        "donation_sendwave_phone": "Nimewo moun k ap resevwa: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Veso labank (Compte UNIBANK US)",
        "donation_bank_account": "Nimewo kont: 105-2016-16594727",
        "donation_bank_note": "Pou veso entènasyonal, tanpri sèvi ak kòd SWIFT UNIBANKUS (oswa kontakte nou pou plis detay).",
        "donation_future": "🔜 Ap vini: Veso labank nan USD ak HTG (entènasyonal ak lokal).",
        "donation_button": "💸 Mwen voye donasyon mwen an – notifye mwen",
        "donation_thanks": "Mèsi anpil! N ap konfime resepsyon nan 24 èdtan. Donasyon ou atravè Prisme Transfer, Sendwave, oswa Moncash (Digicel) ale dirèkteman nan Gesner Deslandes nan (509)-47385663. Sipò ou a vle di anpil pou nou! 🇭🇹",
        "contact_title": "📞 Annou bati yon bagay gwo",
        "contact_ready": "Pou kòmanse pwojè ou a?",
        "contact_phone": "📞 Telefòn / WhatsApp: (509)-47385663",
        "contact_email": "✉️ Imel: deslandes78@gmail.com",
        "contact_delivery": "Nou livre pakè lojisyèl konplè pa imel – rapid, serye, ak adapte ba ou.",
        "contact_tagline": "GlobalInternet.py – Patnè Python ou a, soti Ayiti rive nan lemonn.",
        "footer_rights": "Tout dwa rezève.",
        "footer_founded": "Fonde pa Gesner Deslandes | Bati ak Streamlit | Hébergé sou GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Fiyè Ayisyen – sèvi lemonn ak Python ak AI 🇭🇹"
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
t = lang_dict[lang]

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
# Projects Section (31 projects)
# -----------------------------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Build the full projects list with all 31 projects
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
    {"title": t['project_medical_term'], "desc": t['project_medical_term_desc'], "price": t['project_medical_term_price'], "status": t['project_medical_term_status'], "contact": t['project_medical_term_contact'], "key": "medicalterm", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Medical+Terminology+Book"},
    {"title": t['project_python_course'], "desc": t['project_python_course_desc'], "price": t['project_python_course_price'], "status": t['project_python_course_status'], "contact": t['project_python_course_contact'], "key": "pythoncourse", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Python+Coding+Course"},
    {"title": t['project_hardware_course'], "desc": t['project_hardware_course_desc'], "price": t['project_hardware_course_price'], "status": t['project_hardware_course_status'], "contact": t['project_hardware_course_contact'], "key": "hardwarecourse", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Software+and+Hardware+Course"}
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
