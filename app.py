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
        # Project 7 – CHESS APP
        "project_chess": "♟️ Play Chess Against the Machine",
        "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_chess_price": "$20 USD (one‑time fee)",
        "project_chess_status": "✅ Available now – lifetime access, free updates",
        "project_chess_contact": "Contact owner for purchase",
        # Project 8 – ACCOUNTANT
        "project_accountant": "🧮 Accountant Excel Advanced AI",
        "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish).",
        "project_accountant_price": "$199 USD (one‑time fee)",
        "project_accountant_status": "✅ Available now – lifetime access, free updates",
        "project_accountant_contact": "Contact owner for purchase",
        # Project 9 – ARCHIVES
        "project_archives": "📜 Haiti Archives Nationales Database",
        "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
        "project_archives_price": "$1,500 USD (one‑time fee)",
        "project_archives_status": "✅ Available now – includes source code, setup, and support",
        "project_archives_contact": "Contact owner for purchase",
        # Project 10 – DSM
        "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
        "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
        "project_dsm_price": "$299 USD (one‑time fee)",
        "project_dsm_status": "✅ Available now – lifetime license, free updates",
        "project_dsm_contact": "Contact owner for purchase",
        # Project 11 – BI DASHBOARD (original)
        "project_bi": "📊 Business Intelligence Dashboard",
        "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_bi_price": "$1,200 USD (one‑time fee)",
        "project_bi_status": "✅ Available now – lifetime access, free updates",
        "project_bi_contact": "Contact owner for purchase",
        # Project 12 – AI IMAGE CLASSIFIER
        "project_ai_classifier": "🧠 AI Image Classifier (MobileNetV2)",
        "project_ai_classifier_desc": "Upload an image and the AI identifies it from 1000 categories (animals, vehicles, food, everyday objects). Uses TensorFlow MobileNetV2 pre‑trained on ImageNet. Multi‑language, password protected, demo ready.",
        "project_ai_classifier_price": "$1,200 USD (one‑time fee)",
        "project_ai_classifier_status": "✅ Available now – includes source code, setup, and support",
        "project_ai_classifier_contact": "Contact owner for purchase",
        # Project 13 – TASK MANAGER DASHBOARD
        "project_task_manager": "🗂️ Task Manager Dashboard",
        "project_task_manager_desc": "Manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Inspired by React’s component‑based UI. Multi‑language, persistent storage, analytics dashboard.",
        "project_task_manager_price": "$1,200 USD (one‑time fee)",
        "project_task_manager_status": "✅ Available now – lifetime access, free updates",
        "project_task_manager_contact": "Contact owner for purchase",
        # Project 14 – RAY PARALLEL TEXT PROCESSOR
        "project_ray": "⚡ Ray Parallel Text Processor",
        "project_ray_desc": "Process text in parallel across multiple CPU cores. Compare sequential vs. parallel execution speed. Inspired by UC Berkeley’s distributed computing framework Ray.",
        "project_ray_price": "$1,200 USD (one‑time fee)",
        "project_ray_status": "✅ Available now – lifetime access, free updates",
        "project_ray_contact": "Contact owner for purchase",
        # Project 15 – CASSANDRA DATA DASHBOARD
        "project_cassandra": "🗄️ Cassandra Data Dashboard",
        "project_cassandra_desc": "Distributed NoSQL database demo. Add orders, search by customer, and explore real‑time analytics. Modeled after Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "$1,200 USD (one‑time fee)",
        "project_cassandra_status": "✅ Available now – lifetime access, free updates",
        "project_cassandra_contact": "Contact owner for purchase",
        # Project 16 – APACHE SPARK DATA PROCESSOR
        "project_spark": "🌊 Apache Spark Data Processor",
        "project_spark_desc": "Upload a CSV file and run SQL‑like aggregations (group by, sum, avg, count) using Spark. Real‑time results and charts. Inspired by the big‑data engine used by thousands of companies.",
        "project_spark_price": "$1,200 USD (one‑time fee)",
        "project_spark_status": "✅ Available now – lifetime access, free updates",
        "project_spark_contact": "Contact owner for purchase",
        # Project 17 – HAITIAN DRONE COMMANDER
        "project_drone": "🚁 Haitian Drone Commander",
        "project_drone_desc": "Control the first Haitian‑made drone from your phone. Simulation mode, real drone support (MAVLink), arm, takeoff, land, fly to GPS coordinates, live telemetry, command history. Multi‑language, professional dashboard.",
        "project_drone_price": "$2,000 USD (one‑time fee)",
        "project_drone_status": "✅ Available now – includes source code, setup, and 1 year support",
        "project_drone_contact": "Contact owner for purchase",
        # Project 18 – ENGLISH LEARNING APP
        "project_english": "🇬🇧 Let's Learn English with Gesner",
        "project_english_desc": "Interactive English language learning app. Covers vocabulary, grammar, pronunciation, and conversation practice. Multi‑language interface, progress tracking, quizzes, and certificates. Perfect for beginners to intermediate learners.",
        "project_english_price": "$299 USD (one‑time fee)",
        "project_english_status": "✅ Available now – includes source code, setup, and support",
        "project_english_contact": "Contact owner for purchase",
        # Project 19 – SPANISH LEARNING APP
        "project_spanish": "🇪🇸 Let's Learn Spanish with Gesner",
        "project_spanish_desc": "Complete Spanish language learning platform. Lessons on vocabulary, verb conjugations, listening comprehension, and cultural notes. Includes interactive exercises, speech recognition, and progress dashboard.",
        "project_spanish_price": "$299 USD (one‑time fee)",
        "project_spanish_status": "✅ Available now – includes source code, setup, and support",
        "project_spanish_contact": "Contact owner for purchase",
        # Project 20 – PORTUGUESE LEARNING APP
        "project_portuguese": "🇵🇹 Let's Learn Portuguese with Gesner",
        "project_portuguese_desc": "Brazilian and European Portuguese learning app. Covers essential phrases, grammar, verb tenses, and real‑life dialogues. Includes flashcards, pronunciation guide, and achievement badges. Multi‑language support.",
        "project_portuguese_price": "$299 USD (one‑time fee)",
        "project_portuguese_status": "✅ Available now – includes source code, setup, and support",
        "project_portuguese_contact": "Contact owner for purchase",
        # Project 21 – AI CAREER COACH
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
        # Project 22 – AI MEDICAL ASSISTANT
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
        # Project 23 – MUSIC STUDIO PRO
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
        # Project 24 – AI MEDIA STUDIO
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
        # NEW PROJECT 25 – CHINESE LEARNING APP
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
        - 🗳️ **Systèmes de vote complets** – sécurisés, multilingues, en temps réel  
        - 🌐 **Applications web** – tableaux de bord, outils internes, plateformes en ligne  
        - 📦 **Livraison complète** – nous vous envoyons le code complet par e-mail et vous guidons pour l'installation
        
        Que vous ayez besoin d'un site web, d'un outil logiciel personnalisé ou d'une plateforme en ligne complète – nous le construisons, vous le possédez.
        """,
        "office_photo_caption": "Avatar parlant de Gesner Deslandes – présentation de GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – notre représentant numérique de l'innovation et de l'expertise logicielle.",
        "founder": "Fondateur & PDG",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Ingénieur | Passionné d'IA | Expert Python",
        "cv_title": "📄 À propos du propriétaire – Gesner Deslandes",
        "cv_intro": "Développeur Python | Créateur de sites web | Coordinateur technique",
        "cv_summary": """
        Leader et gestionnaire exceptionnellement motivé, engagé envers l'excellence et la précision.  
        **Compétences clés :** Leadership, Interprétariat (anglais, français, créole), Orientation mécanique, Gestion, Microsoft Office.
        """,
        "cv_experience_title": "💼 Expérience professionnelle",
        "cv_experience": """
        **Coordinateur technique** – Orphelinat Be Like Brit (2021–aujourd'hui)  
        Configuration de réunions Zoom, maintenance d'ordinateurs portables/tablettes, support technique quotidien, gestion des opérations numériques.

        **PDG & Services d'interprétariat** – Tourisme personnalisé pour groupes ONG, missions et particuliers.

        **Gestionnaire de parc / Répartiteur** – J/P Haitian Relief Organization  
        Gestion de plus de 20 véhicules, journaux de bord, calendriers d'entretien avec Excel.

        **Interprète médical** – International Child Care  
        Interprétation médicale précise anglais–français–créole.

        **Chef d'équipe & Interprète** – ONG Can‑Do  
        Direction de projets de reconstruction.

        **Professeur d'anglais** – Be Like Brit (maternelle à NS4)

        **Traducteur de documents** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Éducation et formation",
        "cv_education": """
        - École de formation professionnelle – Anglais américain  
        - Institut Diesel d'Haïti – Mécanique diesel  
        - Certification en bureautique (octobre 2000)  
        - Diplômé du secondaire
        """,
        "cv_references": "📞 Références disponibles sur demande.",
        "team_title": "👥 Notre équipe",
        "team_sub": "Rencontrez les talents derrière GlobalInternet.py – embauchés en avril 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fondateur & PDG", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Assistant du PDG", "since": "Avril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Programmeur Python", "since": "Avril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Programmeur Python", "since": "Avril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Secrétaire", "since": "Avril 2026"}
        ],
        "services_title": "⚙️ Nos services",
        "services": [
            ("🐍 Développement Python sur mesure", "Scripts personnalisés, automatisation, backends."),
            ("🤖 IA & Machine Learning", "Chatbots, modèles prédictifs, analyses."),
            ("🗳️ Logiciel de vote", "Sécurisé, multilingue, résultats en direct – comme notre système Haïti."),
            ("📊 Tableaux de bord", "Analytique en temps réel et rapports."),
            ("🌐 Sites web et apps", "Solutions complètes déployées en ligne."),
            ("📦 Livraison 24h", "Nous travaillons vite – recevez votre logiciel par e-mail, prêt à l'emploi."),
            ("📢 Publicité & Marketing", "Campagnes digitales, gestion des réseaux sociaux, ciblage IA, rapports de performance. De 150 à 1 200 USD selon l'étendue.")
        ],
        "projects_title": "🏆 Nos projets et réalisations",
        "projects_sub": "Solutions logicielles complètes livrées aux clients – prêtes à être achetées ou personnalisées.",
        "project_haiti": "🇭🇹 Logiciel de vote en ligne Haïti",
        "project_haiti_desc": "Système complet d'élection présidentielle multilingue (Kreyòl, français, anglais, espagnol), suivi en direct, tableau de bord du Président du CEP (gérer les candidats, télécharger des photos, rapports d'étape), scrutin secret et mots de passe modifiables. Utilisé pour les élections nationales.",
        "project_haiti_price": "2 000 $ USD (paiement unique)",
        "project_haiti_status": "✅ Disponible – comprend le code source, l'installation et le support.",
        "project_haiti_contact": "Contactez le propriétaire pour acheter",
        "project_dashboard": "📊 Tableau de bord décisionnel",
        "project_dashboard_desc": "Tableau de bord analytique en temps réel pour entreprises. Connectez-vous à n'importe quelle base de données (SQL, Excel, CSV) et visualisez KPI, tendances des ventes, inventaire et rapports personnalisés. Entièrement interactif et personnalisable.",
        "project_dashboard_price": "1 200 $ USD",
        "project_dashboard_status": "✅ Disponible",
        "project_dashboard_contact": "Contactez le propriétaire pour acheter",
        "project_chatbot": "🤖 Chatbot de support client IA",
        "project_chatbot_desc": "Chatbot intelligent entraîné sur vos données commerciales. Répondez aux questions des clients 24h/24, réduisez la charge de support. S'intègre aux sites web, WhatsApp ou Telegram. Construit avec Python et NLP moderne.",
        "project_chatbot_price": "800 $ USD (basique) / 1 500 $ USD (avancé)",
        "project_chatbot_status": "✅ Disponible",
        "project_chatbot_contact": "Contactez le propriétaire pour acheter",
        "project_school": "🏫 Système de gestion scolaire",
        "project_school_desc": "Plateforme complète pour les écoles : inscription des élèves, gestion des notes, suivi des présences, portail parents, génération de bulletins et collecte des frais. Rôles multiples (admin, enseignants, parents).",
        "project_school_price": "1 500 $ USD",
        "project_school_status": "✅ Disponible",
        "project_school_contact": "Contactez le propriétaire pour acheter",
        "project_pos": "📦 Gestion des stocks et point de vente",
        "project_pos_desc": "Gestion d'inventaire en ligne avec point de vente pour petites entreprises. Lecture de codes‑barres, alertes de stock, rapports de vente, gestion des fournisseurs. Fonctionne en ligne et hors ligne.",
        "project_pos_price": "1 000 $ USD",
        "project_pos_status": "✅ Disponible",
        "project_pos_contact": "Contactez le propriétaire pour acheter",
        "project_scraper": "📈 Extracteur web et pipeline de données",
        "project_scraper_desc": "Extraction automatisée de données depuis n'importe quel site web, nettoyée et livrée en Excel/JSON/CSV. Planification quotidienne, hebdomadaire ou mensuelle. Parfait pour études de marché, surveillance des prix ou génération de leads.",
        "project_scraper_price": "500 – 2 000 $ USD (selon complexité)",
        "project_scraper_status": "✅ Disponible",
        "project_scraper_contact": "Contactez le propriétaire pour acheter",
        "project_chess": "♟️ Jouez aux échecs contre la machine",
        "project_chess_desc": "Jeu d'échecs éducatif avec IA (3 niveaux). Chaque coup est expliqué – apprenez les tactiques (fourchette, clouage, échec à la découverte). Mode démo, tableau de bord des coups, téléchargement du rapport complet. Multilingue (anglais, français, espagnol, kreyòl).",
        "project_chess_price": "20 $ USD (paiement unique)",
        "project_chess_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_chess_contact": "Contactez le propriétaire pour acheter",
        "project_accountant": "🧮 Comptabilité Excel IA Avancée",
        "project_accountant_desc": "Suite professionnelle de comptabilité et gestion de prêts. Suivez vos entrées/sorties d'argent, gérez les prêts (emprunteurs, échéances, paiements), tableau de bord avec solde, exportez tous les rapports en Excel et PDF. Multilingue (anglais, français, espagnol).",
        "project_accountant_price": "199 $ USD (paiement unique)",
        "project_accountant_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_accountant_contact": "Contactez le propriétaire pour acheter",
        "project_archives": "📜 Base de données des Archives Nationales d'Haïti",
        "project_archives_desc": "Base de données complète pour les archives nationales haïtiennes. Stockez le NIF (Matricule Fiscale), la CIN, le passeport, le permis de conduire, l'historique de vote, les parrainages et les documents. Validation par signature ministérielle, système de mot de passe annuel, multilingue (anglais, français, espagnol, kreyòl).",
        "project_archives_price": "1 500 $ USD (paiement unique)",
        "project_archives_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_archives_contact": "Contactez le propriétaire pour acheter",
        "project_dsm": "🛡️ DSM-2026: SYSTÈME SÉCURISÉ",
        "project_dsm_desc": "Radar de surveillance stratosphérique avancé – suit les avions, satellites et missiles en temps réel. Affichage radar simulé avec détection de menace, multilingue et rapports d'intelligence téléchargeables.",
        "project_dsm_price": "299 $ USD (paiement unique)",
        "project_dsm_status": "✅ Disponible – licence à vie, mises à jour gratuites",
        "project_dsm_contact": "Contactez le propriétaire pour acheter",
        "project_bi": "📊 Tableau de bord décisionnel",
        "project_bi_desc": "Tableau de bord analytique en temps réel pour entreprises. Connectez SQL, Excel, CSV – visualisez KPI, tendances des ventes, inventaire et performances régionales. Entièrement interactif avec filtres de dates et rapports CSV téléchargeables. Multilingue (anglais, français, espagnol, kreyòl).",
        "project_bi_price": "1 200 $ USD (paiement unique)",
        "project_bi_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_bi_contact": "Contactez le propriétaire pour acheter",
        "project_ai_classifier": "🧠 Classificateur d'images IA (MobileNetV2)",
        "project_ai_classifier_desc": "Téléchargez une image et l'IA l'identifie parmi 1000 catégories (animaux, véhicules, nourriture, objets du quotidien). Utilise TensorFlow MobileNetV2 pré‑entraîné sur ImageNet. Multilingue, protégé par mot de passe, démo prête.",
        "project_ai_classifier_price": "1 200 $ USD (paiement unique)",
        "project_ai_classifier_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_ai_classifier_contact": "Contactez le propriétaire pour acheter",
        "project_task_manager": "🗂️ Tableau de bord des tâches",
        "project_task_manager_desc": "Gérez vos tâches, suivez votre progression et analysez votre productivité avec des graphiques en temps réel et un mode sombre. Inspiré par l'interface composant/état de React. Multilingue, stockage persistant, tableau de bord analytique.",
        "project_task_manager_price": "1 200 $ USD (paiement unique)",
        "project_task_manager_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_task_manager_contact": "Contactez le propriétaire pour acheter",
        "project_ray": "⚡ Processeur de texte parallèle Ray",
        "project_ray_desc": "Traitez du texte en parallèle sur plusieurs cœurs CPU. Comparez la vitesse d'exécution séquentielle vs parallèle. Inspiré par le framework de calcul distribué Ray de UC Berkeley.",
        "project_ray_price": "1 200 $ USD (paiement unique)",
        "project_ray_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_ray_contact": "Contactez le propriétaire pour acheter",
        "project_cassandra": "🗄️ Tableau de bord Cassandra",
        "project_cassandra_desc": "Démonstration de base de données NoSQL distribuée. Ajoutez des commandes, recherchez par client et explorez des analyses en temps réel. Modélisé d'après Apache Cassandra (Netflix, Instagram).",
        "project_cassandra_price": "1 200 $ USD (paiement unique)",
        "project_cassandra_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_cassandra_contact": "Contactez le propriétaire pour acheter",
        "project_spark": "🌊 Processeur de données Apache Spark",
        "project_spark_desc": "Téléchargez un fichier CSV et exécutez des agrégations de type SQL (group by, sum, avg, count) avec Spark. Résultats et graphiques en temps réel. Inspiré par le moteur big data utilisé par des milliers d'entreprises.",
        "project_spark_price": "1 200 $ USD (paiement unique)",
        "project_spark_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_spark_contact": "Contactez le propriétaire pour acheter",
        "project_drone": "🚁 Commandant de drone haïtien",
        "project_drone_desc": "Contrôlez le premier drone fabriqué en Haïti depuis votre téléphone. Mode simulation, support drone réel (MAVLink), armer, décoller, atterrir, voler vers des coordonnées GPS, télémétrie en direct, historique des commandes. Multilingue, tableau de bord professionnel.",
        "project_drone_price": "2 000 $ USD (paiement unique)",
        "project_drone_status": "✅ Disponible – comprend le code source, l'installation et 1 an de support",
        "project_drone_contact": "Contactez le propriétaire pour acheter",
        "project_english": "🇬🇧 Apprenons l'anglais avec Gesner",
        "project_english_desc": "Application interactive d'apprentissage de l'anglais. Couvre le vocabulaire, la grammaire, la prononciation et la pratique de la conversation. Interface multilingue, suivi des progrès, quiz et certificats. Parfait pour les débutants aux niveaux intermédiaires.",
        "project_english_price": "299 $ USD (paiement unique)",
        "project_english_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_english_contact": "Contactez le propriétaire pour acheter",
        "project_spanish": "🇪🇸 Apprenons l'espagnol avec Gesner",
        "project_spanish_desc": "Plateforme complète d'apprentissage de l'espagnol. Leçons sur le vocabulaire, les conjugaisons, la compréhension orale et les notes culturelles. Inclut des exercices interactifs, reconnaissance vocale et tableau de bord de progression.",
        "project_spanish_price": "299 $ USD (paiement unique)",
        "project_spanish_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_spanish_contact": "Contactez le propriétaire pour acheter",
        "project_portuguese": "🇵🇹 Apprenons le portugais avec Gesner",
        "project_portuguese_desc": "Application d'apprentissage du portugais brésilien et européen. Couvre les phrases essentielles, la grammaire, les temps verbaux et les dialogues réels. Inclut des flashcards, guide de prononciation et badges de réussite. Multilingue.",
        "project_portuguese_price": "299 $ USD (paiement unique)",
        "project_portuguese_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_portuguese_contact": "Contactez le propriétaire pour acheter",
        "project_ai_career": "🚀 Coach de Carrière IA – Optimiseur de CV",
        "project_ai_career_desc": """
        **Optimisez votre CV et réussissez vos entretiens avec l'IA.**  
        Téléchargez votre CV et une description de poste – notre IA analyse les deux et fournit :
        
        📌 **Mots‑clés à ajouter** – termes manquants de la description  
        🛠️ **Améliorations de compétences** – ce qu'il faut mettre en avant  
        📄 **Suggestions de mise en forme** – pour faire ressortir votre CV  
        ❓ **Questions d'entretien prédites** – basées sur votre CV et le poste
        
        Parfait pour les chercheurs d'emploi, étudiants et professionnels. Fonctionne pour tout secteur et langue (anglais, français, espagnol, kreyòl).  
        *Le logiciel complet comprend le code source, le guide d'installation et les mises à jour à vie. Livré par email.*
        """,
        "project_ai_career_price": "149 $ USD (paiement unique)",
        "project_ai_career_status": "✅ Disponible – code source complet inclus",
        "project_ai_career_contact": "Contactez le propriétaire pour acheter",
        "project_ai_medical": "🧪 Assistant Médical et Scientifique IA",
        "project_ai_medical_desc": """
        **Posez n'importe quelle question médicale – obtenez des réponses basées sur la recherche réelle.**  
        Notre IA recherche dans PubMed, la plus grande base de données de littérature médicale, extrait les résumés pertinents et génère des réponses factuelles avec **citations et liens directs** vers les études originales.
        
        ✅ **Vérifiable** – chaque affirmation provient d'articles publiés  
        ✅ **Privé** – peut fonctionner localement, aucune donnée ne quitte votre appareil  
        ✅ **À jour** – recherche la littérature actuelle, pas seulement les données d'entraînement  
        ✅ **Idéal pour** – médecins, infirmiers, étudiants en médecine, chercheurs, hôpitaux et cliniques
        
        Comprend le code source complet, guide d'installation et mises à jour à vie. Livré par email.
        """,
        "project_ai_medical_price": "149 $ USD (paiement unique)",
        "project_ai_medical_status": "✅ Disponible – code source complet inclus",
        "project_ai_medical_contact": "Contactez le propriétaire pour acheter",
        "project_music_studio": "🎧 Music Studio Pro – Suite complète de production musicale",
        "project_music_studio_desc": """
        **Logiciel professionnel de production musicale** – enregistrez, mixez et créez des beats. Comprend :
        
        🎤 **Enregistrement vocal** avec aperçu en temps réel  
        🎛️ **Effets studio** – EQ, compresseur, réverbération, correction de hauteur  
        🥁 **Créateur de beats multi‑pistes** – 8 pistes de batterie avec séquenceur 16 pas  
        🎹 **Boucles continues** – basse profonde et pad éthéré avec contrôle de volume  
        🎵 **Chanter sur pistes** – enregistrez la voix sur n'importe quelle piste d'accompagnement  
        🔊 **Enregistreur vocal Auto‑Tune** – correction de hauteur et effets professionnels
        
        Parfait pour musiciens, producteurs et créateurs de contenu. Code source complet inclus.
        """,
        "project_music_studio_price": "299 $ USD (paiement unique)",
        "project_music_studio_status": "✅ Disponible – code source complet inclus",
        "project_music_studio_contact": "Contactez le propriétaire pour acheter",
        "project_ai_media": "🎭 AI Media Studio – Photo Parlante & Éditeur Vidéo",
        "project_ai_media_desc": """
        **Créez des vidéos professionnelles à partir de photos, audio ou clips vidéo.**  
        Choisissez parmi quatre modes puissants :
        
        📷 **Photo + Parole** – téléchargez une photo, tapez n'importe quel texte → voix masculine parle  
        📷 **Photo + Audio téléchargé** – ajoutez votre propre voix ou effet sonore  
        📷 **Photo + Musique de fond** – sélectionnez parmi 50 pistes ou téléchargez la vôtre  
        🎥 **Vidéo + Musique de fond** – ajoutez de la musique à n'importe quelle vidéo
        
        Fond personnalisable (couleur unie ou image), contrôle du volume et aperçu instantané.  
        Parfait pour le contenu des médias sociaux, présentations et projets personnels.
        """,
        "project_ai_media_price": "149 $ USD (paiement unique)",
        "project_ai_media_status": "✅ Disponible – code source complet inclus",
        "project_ai_media_contact": "Contactez le propriétaire pour acheter",
        # NEW PROJECT 25 – CHINESE
        "project_chinese": "🇨🇳 Apprenons le chinois avec Gesner – Livre 1",
        "project_chinese_desc": """
        **Cours complet de chinois mandarin pour débutants.**  
        20 leçons interactives couvrant conversations quotidiennes, vocabulaire, grammaire, prononciation et quiz.
        
        📘 **Contenu :**
        - 20 leçons avec dialogues réels
        - 100+ mots de vocabulaire avec audio natif
        - 10 règles de grammaire essentielles avec exemples
        - Pratique de la prononciation avec pinyin
        - Quiz interactif pour chaque leçon
        - Nombres cardinaux et ordinaux (1-10)
        - Expressions idiomatiques chinoises courantes
        
        🎧 **Audio :** Voix chinoise naturelle (zh-CN-XiaoxiaoNeural) pour tous les textes.
        
        Parfait pour étudiants, professeurs et autodidactes. Code source complet inclus.
        """,
        "project_chinese_price": "299 $ USD (paiement unique)",
        "project_chinese_status": "✅ Disponible – code source complet inclus",
        "project_chinese_contact": "Contactez le propriétaire pour acheter",
        "view_demo": "🎬 Voir la démo",
        "demo_screenshot": "Aperçu (remplacer par l'image réelle)",
        "live_demo": "🔗 Démo en direct",
        "demo_password_hint": "🔐 Mot de passe de démo : 20082010",
        "request_info": "Demander des infos",
        "buy_now": "💵 Acheter maintenant",
        "donation_title": "💖 Soutenez GlobalInternet.py",
        "donation_text": "Aidez‑nous à grandir et à continuer à construire des logiciels innovants pour Haïti et le monde.",
        "donation_sub": "Votre don soutient l'hébergement, les outils de développement et les ressources gratuites pour les développeurs locaux.",
        "donation_method": "🇭🇹 Facile et rapide – virement Prisme vers Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limite de montant : jusqu'à 100 000 HTG par transaction",
        "donation_instruction": "Utilisez la fonction 'Prisme transfer' dans votre application Moncash pour envoyer votre contribution à Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Transfert international via <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Envoyez de l'argent directement à notre numéro de téléphone via l'application SendWave (disponible dans le monde entier).",
        "donation_sendwave_phone": "Téléphone du bénéficiaire : (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Virement bancaire (Compte UNIBANK US)",
        "donation_bank_account": "Numéro de compte : 105-2016-16594727",
        "donation_bank_note": "Pour les transferts internationaux, utilisez le code SWIFT UNIBANKUS (ou contactez-nous pour plus d'informations).",
        "donation_future": "🔜 Bientôt : virements bancaires en USD et HTG (internationaux et locaux).",
        "donation_button": "💸 J'ai envoyé mon don – prévenez‑moi",
        "donation_thanks": "Merci infiniment ! Nous confirmerons la réception sous 24 heures. Votre don via Prisme Transfer, Sendwave ou Moncash (Digicel) va directement à Gesner Deslandes au (509)-47385663. Votre soutien est inestimable ! 🇭🇹",
        "contact_title": "📞 Construisons quelque chose de grand",
        "contact_ready": "Prêt à démarrer votre projet ?",
        "contact_phone": "📞 Téléphone / WhatsApp : (509)-47385663",
        "contact_email": "✉️ Email : deslandes78@gmail.com",
        "contact_delivery": "Nous livrons des logiciels complets par e-mail – rapide, fiable et adapté à vous.",
        "contact_tagline": "GlobalInternet.py – Votre partenaire Python, d'Haïti au monde.",
        "footer_rights": "Tous droits réservés.",
        "footer_founded": "Fondé par Gesner Deslandes | Construit avec Streamlit | Hébergé sur GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Fièrement haïtien – au service du monde avec Python et l'IA 🇭🇹"
    },
    "es": {
        # Spanish translations – only showing the new Chinese project for brevity.
        # The full Spanish dictionary should include all projects similarly.
        "project_chinese": "🇨🇳 Aprendamos chino con Gesner – Libro 1",
        "project_chinese_desc": """
        **Curso completo de chino mandarín para principiantes.**  
        20 lecciones interactivas con conversaciones cotidianas, vocabulario, gramática, pronunciación y cuestionarios.
        
        📘 **Contenido:**
        - 20 lecciones con diálogos reales
        - 100+ palabras de vocabulario con audio nativo
        - 10 reglas gramaticales esenciales con ejemplos
        - Práctica de pronunciación con pinyin
        - Cuestionario interactivo por lección
        - Números cardinales y ordinales (1-10)
        - Modismos chinos comunes
        
        🎧 **Audio:** Voz china natural (zh-CN-XiaoxiaoNeural) para todos los textos.
        
        Perfecto para estudiantes, profesores y autodidactas. Código fuente completo incluido.
        """,
        "project_chinese_price": "$299 USD (pago único)",
        "project_chinese_status": "✅ Disponible – código fuente completo incluido",
        "project_chinese_contact": "Contacte al propietario para comprar",
        "view_demo": "🎬 Ver demo",
        "demo_screenshot": "Vista previa de la captura (reemplazar con imagen real)",
        "live_demo": "🔗 Demo en vivo",
        "demo_password_hint": "🔐 Contraseña de demostración: 20082010",
        "request_info": "Solicitar información",
        "buy_now": "💵 Comprar ahora",
        "donation_title": "💖 Apoye a GlobalInternet.py",
        "donation_text": "Ayúdenos a crecer y seguir construyendo software innovador para Haití y el mundo.",
        "donation_sub": "Su donación apoya el alojamiento, las herramientas de desarrollo y los recursos gratuitos para desarrolladores locales.",
        "donation_method": "🇭🇹 Fácil y rápido – transferencia Prisme a Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Límite de monto: hasta 100,000 HTG por transacción",
        "donation_instruction": "Use la función 'Prisme transfer' en su aplicación Moncash para enviar su contribución a Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Transferencia internacional vía <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Envíe dinero directamente a nuestro número de teléfono usando la aplicación SendWave (disponible en todo el mundo).",
        "donation_sendwave_phone": "Teléfono del beneficiario: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Transferencia bancaria (Cuenta UNIBANK US)",
        "donation_bank_account": "Número de cuenta: 105-2016-16594727",
        "donation_bank_note": "Para transferencias internacionales, utilice el código SWIFT UNIBANKUS (o contáctenos para más detalles).",
        "donation_future": "🔜 Próximamente: transferencias bancarias en USD y HTG (internacionales y locales).",
        "donation_button": "💸 Ya envié mi donación – notifíquenme",
        "donation_thanks": "¡Muchas gracias! Confirmaremos la recepción en 24 horas. Su donación a través de Prisme Transfer, Sendwave o Moncash (Digicel) va directamente a Gesner Deslandes al (509)-47385663. ¡Su apoyo es invaluable! 🇭🇹",
        "contact_title": "📞 Construyamos algo grande",
        "contact_ready": "¿Listo para comenzar su proyecto?",
        "contact_phone": "📞 Teléfono / WhatsApp: (509)-47385663",
        "contact_email": "✉️ Correo: deslandes78@gmail.com",
        "contact_delivery": "Entregamos paquetes de software completos por correo – rápido, confiable y adaptado a usted.",
        "contact_tagline": "GlobalInternet.py – Su socio Python, desde Haití hasta el mundo.",
        "footer_rights": "Todos los derechos reservados.",
        "footer_founded": "Fundado por Gesner Deslandes | Construido con Streamlit | Alojado en GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Orgullosamente haitiano – sirviendo al mundo con Python e IA 🇭🇹"
    },
    "ht": {
        # Kreyòl translations – only showing the new Chinese project for brevity.
        "project_chinese": "🇨🇳 Ann aprann chinwa ak Gesner – Liv 1",
        "project_chinese_desc": """
        **Kou konplè chinwa Mandarin pou débutan.**  
        20 leson entèaktif ki kouvri konvèsasyon chak jou, vokabilè, gramè, pwononsyasyon ak kesyonè.
        
        📘 **Sa ki ladan l :**
        - 20 leson ak dyalòg reyèl
        - 100+ mo vokabilè ak odyo natif
        - 10 règ gramè esansyèl ak egzanp
        - Pratik pwononsyasyon ak pinyin
        - Kesyonè entèaktif pou chak leson
        - Nimewo kadinal ak ordinal (1-10)
        - Ekspresyon idyomatik chinwa komen
        
        🎧 **Odyo:** Vwa chinwa natirèl (zh-CN-XiaoxiaoNeural) pou tout tèks yo.
        
        Pafè pou elèv, pwofesè, ak moun k ap aprann pou kont yo. Kòd sous konplè enkli.
        """,
        "project_chinese_price": "$299 USD (peman inik)",
        "project_chinese_status": "✅ Disponib – kòd sous konplè enkli",
        "project_chinese_contact": "Kontakte pwopriyetè a pou achte",
        "view_demo": "🎬 Wè demonstrasyon",
        "demo_screenshot": "Aperçu ekran (ranplase ak imaj reyèl)",
        "live_demo": "🔗 Demonstrasyon an dirè",
        "demo_password_hint": "🔐 Modpas demonstrasyon: 20082010",
        "request_info": "Mande enfòmasyon",
        "buy_now": "💵 Achte kounye a",
        "donation_title": "💖 Sipòte GlobalInternet.py",
        "donation_text": "Ede nou grandi epi kontinye bati lojisyèl inovatif pou Ayiti ak lemonn.",
        "donation_sub": "Donasyon ou sipòte hosting, zouti devlopman ak resous gratis pou devlopè lokal yo.",
        "donation_method": "🇭🇹 Fasil ak rapid – transfè Prisme nan Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limit kantite lajan : jiska 100,000 HTG pou chak tranzaksyon",
        "donation_instruction": "Sèvi ak fonksyon 'Prisme transfer' nan aplikasyon Moncash ou pou voye kontribisyon ou a Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Transfè entènasyonal via <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Voye lajan dirèkteman nan nimewo telefòn nou an lè w itilize aplikasyon SendWave (disponib atravè lemonn).",
        "donation_sendwave_phone": "Nimewo moun k ap resevwa: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Vireman labank (Compte UNIBANK US)",
        "donation_bank_account": "Nimewo kont: 105-2016-16594727",
        "donation_bank_note": "Pou transfè entènasyonal, sèvi ak kòd SWIFT UNIBANKUS (oswa kontakte nou pou plis detay).",
        "donation_future": "🔜 Byento : transfè labank an USD ak HTG (entènasyonal ak lokal).",
        "donation_button": "💸 Mwen voye don an – notifye m",
        "donation_thanks": "Mèsi anpil! N ap konfime resepsyon nan 24 èdtan. Donasyon ou atravè Prisme Transfer, Sendwave, oswa Moncash (Digicel) ale dirèkteman bay Gesner Deslandes nan (509)-47385663. Sipò ou gen anpil valè pou nou! 🇭🇹",
        "contact_title": "📞 Ann konstwi yon gwo bagay",
        "contact_ready": "Pare pou kòmanse pwojè ou?",
        "contact_phone": "📞 Telefòn / WhatsApp : (509)-47385663",
        "contact_email": "✉️ Imèl : deslandes78@gmail.com",
        "contact_delivery": "Nou livre pakè lojisyèl konplè pa imèl – rapid, serye ak adapte a ou.",
        "contact_tagline": "GlobalInternet.py – Patnè Python ou, soti Ayiti rive lemonn.",
        "footer_rights": "Tout dwa rezève.",
        "footer_founded": "Fonde pa Gesner Deslandes | Bati ak Streamlit | Hébergé sou GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Fyèman Ayisyen – sèvi lemonn ak Python ak AI 🇭🇹"
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
# Projects Section (25 projects)
# -----------------------------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Build the full projects list (all 25)
projects = [
    # Project 1
    {"title": t['project_haiti'], "desc": t['project_haiti_desc'], "price": t['project_haiti_price'], "status": t['project_haiti_status'], "contact": t['project_haiti_contact'], "key": "haiti", "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Haiti+Voting+Software"},
    # Project 2
    {"title": t['project_dashboard'], "desc": t['project_dashboard_desc'], "price": t['project_dashboard_price'], "status": t['project_dashboard_status'], "contact": t['project_dashboard_contact'], "key": "dashboard", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"},
    # Project 3
    {"title": t['project_chatbot'], "desc": t['project_chatbot_desc'], "price": t['project_chatbot_price'], "status": t['project_chatbot_status'], "contact": t['project_chatbot_contact'], "key": "chatbot", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Chatbot"},
    # Project 4
    {"title": t['project_school'], "desc": t['project_school_desc'], "price": t['project_school_price'], "status": t['project_school_status'], "contact": t['project_school_contact'], "key": "school", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=School+Management"},
    # Project 5
    {"title": t['project_pos'], "desc": t['project_pos_desc'], "price": t['project_pos_price'], "status": t['project_pos_status'], "contact": t['project_pos_contact'], "key": "pos", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Inventory+POS"},
    # Project 6
    {"title": t['project_scraper'], "desc": t['project_scraper_desc'], "price": t['project_scraper_price'], "status": t['project_scraper_status'], "contact": t['project_scraper_contact'], "key": "scraper", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Web+Scraper"},
    # Project 7
    {"title": t['project_chess'], "desc": t['project_chess_desc'], "price": t['project_chess_price'], "status": t['project_chess_status'], "contact": t['project_chess_contact'], "key": "chess", "demo_url": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Chess+Game"},
    # Project 8
    {"title": t['project_accountant'], "desc": t['project_accountant_desc'], "price": t['project_accountant_price'], "status": t['project_accountant_status'], "contact": t['project_accountant_contact'], "key": "accountant", "demo_url": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Accounting+Software"},
    # Project 9
    {"title": t['project_archives'], "desc": t['project_archives_desc'], "price": t['project_archives_price'], "status": t['project_archives_status'], "contact": t['project_archives_contact'], "key": "archives", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=National+Archives"},
    # Project 10
    {"title": t['project_dsm'], "desc": t['project_dsm_desc'], "price": t['project_dsm_price'], "status": t['project_dsm_status'], "contact": t['project_dsm_contact'], "key": "dsm", "demo_url": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=DSM+Radar"},
    # Project 11
    {"title": t['project_bi'], "desc": t['project_bi_desc'], "price": t['project_bi_price'], "status": t['project_bi_status'], "contact": t['project_bi_contact'], "key": "bi", "demo_url": "https://9enktzu34sxzyvtsymghxd.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"},
    # Project 12
    {"title": t['project_ai_classifier'], "desc": t['project_ai_classifier_desc'], "price": t['project_ai_classifier_price'], "status": t['project_ai_classifier_status'], "contact": t['project_ai_classifier_contact'], "key": "aiclassifier", "demo_url": "https://f9n6ijhw7svgp69ebmtzdw.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=AI+Image+Classifier"},
    # Project 13
    {"title": t['project_task_manager'], "desc": t['project_task_manager_desc'], "price": t['project_task_manager_price'], "status": t['project_task_manager_status'], "contact": t['project_task_manager_contact'], "key": "taskmanager", "demo_url": "https://task-manager-dashboard-react-6mktxsbvhgy8qrhbwyjdzs.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Task+Manager+Dashboard"},
    # Project 14
    {"title": t['project_ray'], "desc": t['project_ray_desc'], "price": t['project_ray_price'], "status": t['project_ray_status'], "contact": t['project_ray_contact'], "key": "ray", "demo_url": "https://parallel-text-proceappr-guqq5nfzysxa9kkx9cg9lx.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Ray+Parallel+Processor"},
    # Project 15
    {"title": t['project_cassandra'], "desc": t['project_cassandra_desc'], "price": t['project_cassandra_price'], "status": t['project_cassandra_status'], "contact": t['project_cassandra_contact'], "key": "cassandra", "demo_url": "https://apache-cassandra-mcfkzydlc5qgx2wbcacxtu.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Cassandra+Data+Dashboard"},
    # Project 16
    {"title": t['project_spark'], "desc": t['project_spark_desc'], "price": t['project_spark_price'], "status": t['project_spark_status'], "contact": t['project_spark_contact'], "key": "spark", "demo_url": "https://apache-spark-data-proceappr-4pui6brcjmaxfs6flnwapy.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Apache+Spark+Data+Processor"},
    # Project 17
    {"title": t['project_drone'], "desc": t['project_drone_desc'], "price": t['project_drone_price'], "status": t['project_drone_status'], "contact": t['project_drone_contact'], "key": "drone", "demo_url": "https://drone-control-software-4lgtsedbmq4efzvpwxb8r7.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Haitian+Drone+Commander"},
    # Project 18
    {"title": t['project_english'], "desc": t['project_english_desc'], "price": t['project_english_price'], "status": t['project_english_status'], "contact": t['project_english_contact'], "key": "english", "demo_url": "https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+English+with+Gesner"},
    # Project 19
    {"title": t['project_spanish'], "desc": t['project_spanish_desc'], "price": t['project_spanish_price'], "status": t['project_spanish_status'], "contact": t['project_spanish_contact'], "key": "spanish", "demo_url": "https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+Spanish+with+Gesner"},
    # Project 20
    {"title": t['project_portuguese'], "desc": t['project_portuguese_desc'], "price": t['project_portuguese_price'], "status": t['project_portuguese_status'], "contact": t['project_portuguese_contact'], "key": "portuguese", "demo_url": "https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/", "screenshot": "https://via.placeholder.com/800x400?text=Learn+Portuguese+with+Gesner"},
    # Project 21
    {"title": t['project_ai_career'], "desc": t['project_ai_career_desc'], "price": t['project_ai_career_price'], "status": t['project_ai_career_status'], "contact": t['project_ai_career_contact'], "key": "aicareer", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Career+Coach"},
    # Project 22
    {"title": t['project_ai_medical'], "desc": t['project_ai_medical_desc'], "price": t['project_ai_medical_price'], "status": t['project_ai_medical_status'], "contact": t['project_ai_medical_contact'], "key": "aimedical", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Medical+Assistant"},
    # Project 23
    {"title": t['project_music_studio'], "desc": t['project_music_studio_desc'], "price": t['project_music_studio_price'], "status": t['project_music_studio_status'], "contact": t['project_music_studio_contact'], "key": "musicstudio", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Music+Studio+Pro"},
    # Project 24
    {"title": t['project_ai_media'], "desc": t['project_ai_media_desc'], "price": t['project_ai_media_price'], "status": t['project_ai_media_status'], "contact": t['project_ai_media_contact'], "key": "aimedia", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=AI+Media+Studio"},
    # NEW PROJECT 25 – CHINESE
    {"title": t['project_chinese'], "desc": t['project_chinese_desc'], "price": t['project_chinese_price'], "status": t['project_chinese_status'], "contact": t['project_chinese_contact'], "key": "chinese", "demo_url": None, "screenshot": "https://via.placeholder.com/800x400?text=Learn+Chinese+with+Gesner"}
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
