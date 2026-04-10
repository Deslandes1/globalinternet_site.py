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
    .profile-img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .office-img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        width: 100%;
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
        "office_photo_caption": "Our team working at GlobalInternet.py office – a busy day creating software solutions.",
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
            ("📦 24‑Hour Delivery", "We work fast – get your software by email, ready to use.")
        ],
        "projects_title": "🏆 Our Projects & Accomplishments",
        "projects_sub": "Completed software solutions delivered to clients – ready for you to purchase or customize.",
        # Project 1
        "project_haiti": "🇭🇹 Haiti Online Voting Software",
        "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
        "project_haiti_price": "$2,000 USD (one‑time fee)",
        "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
        "project_haiti_contact": "Contact us for a live demo",
        # Project 2
        "project_dashboard": "📊 Business Intelligence Dashboard",
        "project_dashboard_desc": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Available now",
        "project_dashboard_contact": "Demo available on request",
        # Project 3
        "project_chatbot": "🤖 AI Customer Support Chatbot",
        "project_chatbot_desc": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
        "project_chatbot_price": "$800 USD (basic) / $1,500 USD (advanced)",
        "project_chatbot_status": "✅ Available now",
        "project_chatbot_contact": "We can train on your specific content",
        # Project 4
        "project_school": "🏫 School Management System",
        "project_school_desc": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Available now",
        "project_school_contact": "Includes training and deployment",
        # Project 5
        "project_pos": "📦 Inventory & POS System",
        "project_pos_desc": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Available now",
        "project_pos_contact": "Customizable for your business needs",
        # Project 6
        "project_scraper": "📈 Custom Web Scraper & Data Pipeline",
        "project_scraper_desc": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
        "project_scraper_price": "$500 – $2,000 (depends on complexity)",
        "project_scraper_status": "✅ Available now",
        "project_scraper_contact": "Tell us your data source and we'll quote",
        # Project 7 – CHESS APP
        "project_chess": "♟️ Play Chess Against the Machine",
        "project_chess_desc": "Educational chess game with AI opponent (3 difficulty levels). Every move is explained – learn tactics like forks, pins, and discovered checks. Includes demo mode, move dashboard, and full game report download. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_chess_price": "$20 USD (one‑time fee)",
        "project_chess_status": "✅ Available now – lifetime access, free updates",
        "project_chess_contact": "Perfect for learning chess",
        # Project 8 – ACCOUNTANT
        "project_accountant": "🧮 Accountant Excel Advanced AI",
        "project_accountant_desc": "Professional accounting and loan management suite. Track cash income/expenses, manage loans (borrowers, due dates, payments), dashboard with balance, export all reports to Excel and PDF. Multi‑language (English, French, Spanish). Password protected.",
        "project_accountant_price": "$199 USD (one‑time fee)",
        "project_accountant_status": "✅ Available now – lifetime access, free updates",
        "project_accountant_contact": "Ideal for small businesses, associations, freelancers",
        # Project 9 – ARCHIVES
        "project_archives": "📜 Haiti Archives Nationales Database",
        "project_archives_desc": "Complete national archives database for Haitian citizens. Store NIF (Matricule Fiscale), CIN, Passport, Driver's License, voting history, sponsorships, and document uploads. Minister signature validation, annual password system, multilingual (English, French, Spanish, Kreyòl).",
        "project_archives_price": "$1,500 USD (one‑time fee)",
        "project_archives_status": "✅ Available now – includes source code, setup, and support",
        "project_archives_contact": "Ideal for government archives, ministries, and institutions",
        # Project 10 – DSM
        "project_dsm": "🛡️ DSM-2026: SYSTEM SECURED",
        "project_dsm_desc": "Advanced stratosphere monitoring radar – tracks aircraft, satellites, and missiles in real time. Simulated radar display with threat detection, multi‑language support, and downloadable intelligence reports.",
        "project_dsm_price": "$299 USD (one‑time fee)",
        "project_dsm_status": "✅ Available now – lifetime license, free updates",
        "project_dsm_contact": "Perfect for surveillance and security demonstrations",
        # Project 11 – BI DASHBOARD
        "project_bi": "📊 Business Intelligence Dashboard",
        "project_bi_desc": "Real‑time analytics dashboard for companies. Connect SQL, Excel, CSV – visualize KPIs, sales trends, inventory, and regional performance. Fully interactive with date filters and downloadable CSV reports. Multi‑language (English, French, Spanish, Kreyòl).",
        "project_bi_price": "$1,200 USD (one‑time fee)",
        "project_bi_status": "✅ Available now – lifetime access, free updates",
        "project_bi_contact": "Perfect for businesses, managers, and analysts",
        "view_demo": "🎬 View Demo",
        "demo_screenshot": "Screenshot preview (replace with actual image)",
        "live_demo": "🔗 Live Demo",
        "demo_password_hint": "🔐 Demo password: 20082010",
        "request_info": "Request Info",
        "donation_title": "💖 Support GlobalInternet.py",
        "donation_text": "Help us grow and continue building innovative software for Haiti and the world.",
        "donation_sub": "Your donation supports hosting, development tools, and free resources for local developers.",
        "donation_method": "🇭🇹 Easy & fast – Prisme transfer to Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Amount limit: Up to 100,000 HTG per transaction",
        "donation_instruction": "Just use the 'Prisme transfer' feature in your Moncash app to send your contribution.",
        "donation_bank_title": "🏦 Bank Transfer (UNIBANK US Account)",
        "donation_bank_account": "Account number: 105-2016-16594727",
        "donation_bank_note": "For international transfers, please use SWIFT code UNIBANKUS (or contact us for details).",
        "donation_future": "🔜 Coming soon: Bank‑to‑bank transfers in USD and HTG (international and local).",
        "donation_button": "💸 I've sent my donation – notify me",
        "donation_thanks": "Thank you so much! We will confirm receipt within 24 hours. Your support means the world to us! 🇭🇹",
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
        "office_photo_caption": "Notre équipe travaille au bureau de GlobalInternet.py – une journée chargée à créer des solutions logicielles.",
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
            ("📦 Livraison 24h", "Nous travaillons vite – recevez votre logiciel par e-mail, prêt à l'emploi.")
        ],
        "projects_title": "🏆 Nos projets et réalisations",
        "projects_sub": "Solutions logicielles complètes livrées aux clients – prêtes à être achetées ou personnalisées.",
        "project_haiti": "🇭🇹 Logiciel de vote en ligne Haïti",
        "project_haiti_desc": "Système complet d'élection présidentielle multilingue (Kreyòl, français, anglais, espagnol), suivi en direct, tableau de bord du Président du CEP (gérer les candidats, télécharger des photos, rapports d'étape), scrutin secret et mots de passe modifiables. Utilisé pour les élections nationales.",
        "project_haiti_price": "2 000 $ USD (paiement unique)",
        "project_haiti_status": "✅ Disponible – comprend le code source, l'installation et le support.",
        "project_haiti_contact": "Contactez-nous pour une démo en direct",
        "project_dashboard": "📊 Tableau de bord décisionnel",
        "project_dashboard_desc": "Tableau de bord analytique en temps réel pour entreprises. Connectez-vous à n'importe quelle base de données (SQL, Excel, CSV) et visualisez KPI, tendances des ventes, inventaire et rapports personnalisés. Entièrement interactif et personnalisable.",
        "project_dashboard_price": "1 200 $ USD",
        "project_dashboard_status": "✅ Disponible",
        "project_dashboard_contact": "Démo sur demande",
        "project_chatbot": "🤖 Chatbot de support client IA",
        "project_chatbot_desc": "Chatbot intelligent entraîné sur vos données commerciales. Répondez aux questions des clients 24h/24, réduisez la charge de support. S'intègre aux sites web, WhatsApp ou Telegram. Construit avec Python et NLP moderne.",
        "project_chatbot_price": "800 $ USD (basique) / 1 500 $ USD (avancé)",
        "project_chatbot_status": "✅ Disponible",
        "project_chatbot_contact": "Nous pouvons l'entraîner sur votre contenu spécifique",
        "project_school": "🏫 Système de gestion scolaire",
        "project_school_desc": "Plateforme complète pour les écoles : inscription des élèves, gestion des notes, suivi des présences, portail parents, génération de bulletins et collecte des frais. Rôles multiples (admin, enseignants, parents).",
        "project_school_price": "1 500 $ USD",
        "project_school_status": "✅ Disponible",
        "project_school_contact": "Inclut la formation et le déploiement",
        "project_pos": "📦 Gestion des stocks et point de vente",
        "project_pos_desc": "Gestion d'inventaire en ligne avec point de vente pour petites entreprises. Lecture de codes‑barres, alertes de stock, rapports de vente, gestion des fournisseurs. Fonctionne en ligne et hors ligne.",
        "project_pos_price": "1 000 $ USD",
        "project_pos_status": "✅ Disponible",
        "project_pos_contact": "Personnalisable selon vos besoins",
        "project_scraper": "📈 Extracteur web et pipeline de données",
        "project_scraper_desc": "Extraction automatisée de données depuis n'importe quel site web, nettoyée et livrée en Excel/JSON/CSV. Planification quotidienne, hebdomadaire ou mensuelle. Parfait pour études de marché, surveillance des prix ou génération de leads.",
        "project_scraper_price": "500 – 2 000 $ USD (selon complexité)",
        "project_scraper_status": "✅ Disponible",
        "project_scraper_contact": "Dites‑nous votre source de données, nous devisons",
        "project_chess": "♟️ Jouez aux échecs contre la machine",
        "project_chess_desc": "Jeu d'échecs éducatif avec IA (3 niveaux). Chaque coup est expliqué – apprenez les tactiques (fourchette, clouage, échec à la découverte). Mode démo, tableau de bord des coups, téléchargement du rapport complet. Multilingue (anglais, français, espagnol, kreyòl).",
        "project_chess_price": "20 $ USD (paiement unique)",
        "project_chess_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_chess_contact": "Parfait pour apprendre les échecs",
        "project_accountant": "🧮 Comptabilité Excel IA Avancée",
        "project_accountant_desc": "Suite professionnelle de comptabilité et gestion de prêts. Suivez vos entrées/sorties d'argent, gérez les prêts (emprunteurs, échéances, paiements), tableau de bord avec solde, exportez tous les rapports en Excel et PDF. Multilingue (anglais, français, espagnol).",
        "project_accountant_price": "199 $ USD (paiement unique)",
        "project_accountant_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_accountant_contact": "Idéal pour petites entreprises, associations, freelances",
        "project_archives": "📜 Base de données des Archives Nationales d'Haïti",
        "project_archives_desc": "Base de données complète pour les archives nationales haïtiennes. Stockez le NIF (Matricule Fiscale), la CIN, le passeport, le permis de conduire, l'historique de vote, les parrainages et les documents. Validation par signature ministérielle, système de mot de passe annuel, multilingue (anglais, français, espagnol, kreyòl).",
        "project_archives_price": "1 500 $ USD (paiement unique)",
        "project_archives_status": "✅ Disponible – comprend le code source, l'installation et le support",
        "project_archives_contact": "Idéal pour les archives gouvernementales, ministères et institutions",
        "project_dsm": "🛡️ DSM-2026: SYSTÈME SÉCURISÉ",
        "project_dsm_desc": "Radar de surveillance stratosphérique avancé – suit les avions, satellites et missiles en temps réel. Affichage radar simulé avec détection de menace, multilingue et rapports d'intelligence téléchargeables.",
        "project_dsm_price": "299 $ USD (paiement unique)",
        "project_dsm_status": "✅ Disponible – licence à vie, mises à jour gratuites",
        "project_dsm_contact": "Parfait pour les démonstrations de sécurité et de surveillance",
        "project_bi": "📊 Tableau de bord décisionnel",
        "project_bi_desc": "Tableau de bord analytique en temps réel pour entreprises. Connectez SQL, Excel, CSV – visualisez KPI, tendances des ventes, inventaire et performances régionales. Entièrement interactif avec filtres de dates et rapports CSV téléchargeables. Multilingue (anglais, français, espagnol, kreyòl).",
        "project_bi_price": "1 200 $ USD (paiement unique)",
        "project_bi_status": "✅ Disponible – accès à vie, mises à jour gratuites",
        "project_bi_contact": "Parfait pour les entreprises, gestionnaires et analystes",
        "view_demo": "🎬 Voir la démo",
        "demo_screenshot": "Aperçu (remplacer par l'image réelle)",
        "live_demo": "🔗 Démo en direct",
        "demo_password_hint": "🔐 Mot de passe de démo : 20082010",
        "request_info": "Demander des infos",
        "donation_title": "💖 Soutenez GlobalInternet.py",
        "donation_text": "Aidez‑nous à grandir et à continuer à construire des logiciels innovants pour Haïti et le monde.",
        "donation_sub": "Votre don soutient l'hébergement, les outils de développement et les ressources gratuites pour les développeurs locaux.",
        "donation_method": "🇭🇹 Facile et rapide – virement Prisme vers Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limite de montant : jusqu'à 100 000 HTG par transaction",
        "donation_instruction": "Utilisez la fonction 'Prisme transfer' dans votre application Moncash pour envoyer votre contribution.",
        "donation_bank_title": "🏦 Virement bancaire (Compte UNIBANK US)",
        "donation_bank_account": "Numéro de compte : 105-2016-16594727",
        "donation_bank_note": "Pour les transferts internationaux, utilisez le code SWIFT UNIBANKUS (ou contactez-nous pour plus d'informations).",
        "donation_future": "🔜 Bientôt : virements bancaires en USD et HTG (internationaux et locaux).",
        "donation_button": "💸 J'ai envoyé mon don – prévenez‑moi",
        "donation_thanks": "Merci infiniment ! Nous confirmerons la réception sous 24 heures. Votre soutien est inestimable ! 🇭🇹",
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
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Construye con Python. Entrega rápido. Innova con IA.",
        "hero_desc": "Desde Haití al mundo – software personalizado que funciona en línea.",
        "about_title": "👨‍💻 Sobre la empresa",
        "about_text": """
        **GlobalInternet.py** fue fundada por **Gesner Deslandes** – propietario, fundador e ingeniero principal.  
        Construimos **software basado en Python** bajo demanda para clientes de todo el mundo. Como Silicon Valley, pero con un toque haitiano y resultados sobresalientes.
        
        - 🧠 **Soluciones con IA** – chatbots, análisis de datos, automatización  
        - 🗳️ **Sistemas de votación completos** – seguros, multilingües, en tiempo real  
        - 🌐 **Aplicaciones web** – paneles de control, herramientas internas, plataformas en línea  
        - 📦 **Entrega completa** – le enviamos el código completo por correo y le guiamos en la instalación
        
        Ya sea que necesite un sitio web, una herramienta de software personalizada o una plataforma en línea a gran escala – nosotros lo construimos, usted lo posee.
        """,
        "office_photo_caption": "Nuestro equipo trabajando en la oficina de GlobalInternet.py – un día ocupado creando soluciones de software.",
        "founder": "Fundador y CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Ingeniero | Entusiasta de IA | Experto en Python",
        "cv_title": "📄 Sobre el propietario – Gesner Deslandes",
        "cv_intro": "Creador de software Python | Desarrollador web | Coordinador técnico",
        "cv_summary": """
        Líder y gerente excepcionalmente motivado, comprometido con la excelencia y la precisión.  
        **Competencias clave:** Liderazgo, Interpretación (inglés, francés, criollo haitiano), Orientación mecánica, Gestión, Microsoft Office.
        """,
        "cv_experience_title": "💼 Experiencia profesional",
        "cv_experience": """
        **Coordinador técnico** – Orfanato Be Like Brit (2021–presente)  
        Configuración de reuniones Zoom, mantenimiento de laptops/tablets, soporte técnico diario, operaciones digitales.

        **CEO y servicios de interpretación** – Turismo personalizado para grupos ONG, equipos misioneros e individuos.

        **Gestor de flota / Despachador** – J/P Haitian Relief Organization  
        Gestioné más de 20 vehículos, registros de conductores, calendarios de mantenimiento con Excel.

        **Intérprete médico** – International Child Care  
        Interpretación médica precisa inglés–francés–criollo.

        **Líder de equipo e intérprete** – ONG Can‑Do  
        Dirigí proyectos de reconstrucción.

        **Profesor de inglés** – Be Like Brit (preescolar a NS4)

        **Traductor de documentos** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Educación y formación",
        "cv_education": """
        - Escuela de formación profesional – Inglés americano  
        - Instituto Diesel de Haití – Mecánica diesel  
        - Certificación en ofimática (octubre 2000)  
        - Graduado de secundaria
        """,
        "cv_references": "📞 Referencias disponibles bajo solicitud.",
        "team_title": "👥 Nuestro equipo",
        "team_sub": "Conoce a los talentos detrás de GlobalInternet.py – contratados en abril de 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fundador y CEO", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Asistente del CEO", "since": "Abril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Programador Python", "since": "Abril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Programador Python", "since": "Abril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Secretaria", "since": "Abril 2026"}
        ],
        "services_title": "⚙️ Nuestros servicios",
        "services": [
            ("🐍 Desarrollo Python personalizado", "Scripts a medida, automatización, backends."),
            ("🤖 IA y Machine Learning", "Chatbots, modelos predictivos, insights de datos."),
            ("🗳️ Software de votación", "Seguro, multilingüe, resultados en vivo – como nuestro sistema Haití."),
            ("📊 Paneles de negocio", "Analítica en tiempo real y herramientas de informes."),
            ("🌐 Sitios web y apps", "Soluciones full‑stack desplegadas en línea."),
            ("📦 Entrega 24h", "Trabajamos rápido – reciba su software por correo, listo para usar.")
        ],
        "projects_title": "🏆 Nuestros proyectos y logros",
        "projects_sub": "Soluciones de software completas entregadas a clientes – listas para comprar o personalizar.",
        "project_haiti": "🇭🇹 Software de voto en línea Haití",
        "project_haiti_desc": "Sistema completo de elección presidencial multilingüe (Kreyòl, francés, inglés, español), monitoreo en vivo, panel del Presidente del CEP (gestionar candidatos, subir fotos, descargar informes de progreso), voto secreto y contraseñas modificables. Usado para elecciones nacionales.",
        "project_haiti_price": "$2,000 USD (pago único)",
        "project_haiti_status": "✅ Disponible – incluye código fuente, configuración y soporte.",
        "project_haiti_contact": "Contáctenos para una demo en vivo",
        "project_dashboard": "📊 Panel de inteligencia de negocio",
        "project_dashboard_desc": "Panel de análisis en tiempo real para empresas. Conéctese a cualquier base de datos (SQL, Excel, CSV) y visualice KPI, tendencias de ventas, inventario e informes personalizados. Totalmente interactivo y personalizable.",
        "project_dashboard_price": "$1,200 USD",
        "project_dashboard_status": "✅ Disponible",
        "project_dashboard_contact": "Demo disponible bajo solicitud",
        "project_chatbot": "🤖 Chatbot de soporte al cliente con IA",
        "project_chatbot_desc": "Chatbot inteligente entrenado con sus datos comerciales. Responda preguntas de clientes 24/7, reduzca la carga de soporte. Se integra con sitios web, WhatsApp o Telegram. Construido con Python y NLP moderno.",
        "project_chatbot_price": "$800 USD (básico) / $1,500 USD (avanzado)",
        "project_chatbot_status": "✅ Disponible",
        "project_chatbot_contact": "Podemos entrenarlo en su contenido específico",
        "project_school": "🏫 Sistema de gestión escolar",
        "project_school_desc": "Plataforma completa para escuelas: registro de estudiantes, gestión de calificaciones, seguimiento de asistencia, portal para padres, generación de boletines y cobro de tarifas. Roles múltiples (admin, profesores, padres).",
        "project_school_price": "$1,500 USD",
        "project_school_status": "✅ Disponible",
        "project_school_contact": "Incluye capacitación y despliegue",
        "project_pos": "📦 Sistema de inventario y punto de venta",
        "project_pos_desc": "Gestión de inventario basada en web con punto de venta para pequeñas empresas. Lectura de códigos de barras, alertas de stock, informes de ventas, gestión de proveedores. Funciona en línea y sin conexión.",
        "project_pos_price": "$1,000 USD",
        "project_pos_status": "✅ Disponible",
        "project_pos_contact": "Personalizable para sus necesidades",
        "project_scraper": "📈 Extractor web personalizado y pipeline de datos",
        "project_scraper_desc": "Extracción automatizada de datos de cualquier sitio web, limpiados y entregados como Excel/JSON/CSV. Programación diaria, semanal o mensual. Perfecto para investigación de mercado, monitoreo de precios o generación de leads.",
        "project_scraper_price": "$500 – $2,000 USD (depende de la complejidad)",
        "project_scraper_status": "✅ Disponible",
        "project_scraper_contact": "Díganos su fuente de datos y le cotizamos",
        "project_chess": "♟️ Juega al ajedrez contra la máquina",
        "project_chess_desc": "Juego de ajedrez educativo con IA (3 niveles). Cada movimiento se explica – aprende tácticas como horquillas, clavadas y jaques descubiertos. Modo demo, panel de movimientos, descarga de informe completo. Multilingüe (inglés, francés, español, kreyòl).",
        "project_chess_price": "$20 USD (pago único)",
        "project_chess_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_chess_contact": "Perfecto para aprender ajedrez",
        "project_accountant": "🧮 Contabilidad Excel IA Avanzada",
        "project_accountant_desc": "Suite profesional de contabilidad y gestión de préstamos. Registre ingresos/gastos, administre préstamos (prestatarios, fechas de vencimiento, pagos), panel con saldo, exporte todos los informes a Excel y PDF. Multilingüe (inglés, francés, español).",
        "project_accountant_price": "$199 USD (pago único)",
        "project_accountant_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_accountant_contact": "Ideal para pequeñas empresas, asociaciones, autónomos",
        "project_archives": "📜 Base de Datos de los Archivos Nacionales de Haití",
        "project_archives_desc": "Base de datos completa para archivos nacionales haitianos. Almacene NIF (Matrícula Fiscal), CIN, pasaporte, licencia de conducir, historial de votación, patrocinios y documentos. Validación con firma ministerial, sistema de contraseña anual, multilingüe (inglés, francés, español, kreyòl).",
        "project_archives_price": "$1,500 USD (pago único)",
        "project_archives_status": "✅ Disponible – incluye código fuente, configuración y soporte",
        "project_archives_contact": "Ideal para archivos gubernamentales, ministerios e instituciones",
        "project_dsm": "🛡️ DSM-2026: SISTEMA SEGURO",
        "project_dsm_desc": "Radar de vigilancia estratosférica avanzado – rastrea aviones, satélites y misiles en tiempo real. Visualización de radar simulada con detección de amenazas, soporte multilingüe e informes de inteligencia descargables.",
        "project_dsm_price": "$299 USD (pago único)",
        "project_dsm_status": "✅ Disponible – licencia de por vida, actualizaciones gratuitas",
        "project_dsm_contact": "Perfecto para demostraciones de seguridad y vigilancia",
        "project_bi": "📊 Panel de Inteligencia de Negocios",
        "project_bi_desc": "Panel de análisis en tiempo real para empresas. Conecte SQL, Excel, CSV – visualice KPI, tendencias de ventas, inventario y rendimiento regional. Totalmente interactivo con filtros de fecha e informes CSV descargables. Multilingüe (inglés, francés, español, kreyòl).",
        "project_bi_price": "$1,200 USD (pago único)",
        "project_bi_status": "✅ Disponible – acceso de por vida, actualizaciones gratuitas",
        "project_bi_contact": "Perfecto para empresas, gerentes y analistas",
        "view_demo": "🎬 Ver demo",
        "demo_screenshot": "Vista previa de la captura (reemplazar con imagen real)",
        "live_demo": "🔗 Demo en vivo",
        "demo_password_hint": "🔐 Contraseña de demostración: 20082010",
        "request_info": "Solicitar información",
        "donation_title": "💖 Apoye a GlobalInternet.py",
        "donation_text": "Ayúdenos a crecer y seguir construyendo software innovador para Haití y el mundo.",
        "donation_sub": "Su donación apoya el alojamiento, las herramientas de desarrollo y los recursos gratuitos para desarrolladores locales.",
        "donation_method": "🇭🇹 Fácil y rápido – transferencia Prisme a Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Límite de monto: hasta 100,000 HTG por transacción",
        "donation_instruction": "Use la función 'Prisme transfer' en su aplicación Moncash para enviar su contribución.",
        "donation_bank_title": "🏦 Transferencia bancaria (Cuenta UNIBANK US)",
        "donation_bank_account": "Número de cuenta: 105-2016-16594727",
        "donation_bank_note": "Para transferencias internacionales, utilice el código SWIFT UNIBANKUS (o contáctenos para más detalles).",
        "donation_future": "🔜 Próximamente: transferencias bancarias en USD y HTG (internacionales y locales).",
        "donation_button": "💸 Ya envié mi donación – notifíquenme",
        "donation_thanks": "¡Muchas gracias! Confirmaremos la recepción en 24 horas. ¡Su apoyo es invaluable! 🇭🇹",
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
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Konstwi ak Python. Livre vit. Innove ak IA.",
        "hero_desc": "Soti Ayiti rive nan lemonn – lojisyèl sou mezi ki mache sou entènèt.",
        "about_title": "👨‍💻 Konsènan konpayi an",
        "about_text": """
        **GlobalInternet.py** te fonde pa **Gesner Deslandes** – pwopriyetè, fondatè ak enjenyè prensipal.  
        Nou bati **lojisyèl ki baze sou Python** sou demand pou kliyan atravè lemonn. Tankou Silisyòm Valley, men ak yon manyen Ayisyen ak rezilta eksepsyonèl.
        
        - 🧠 **Solisyon ki mache ak AI** – chatbot, analiz done, otomatizasyon  
        - 🗳️ **Sistèm vòt konplè** – sekirize, plizyè lang, an tan reyèl  
        - 🌐 **Aplikasyon wèb** – tablodbò, zouti entèn, platfòm sou entènèt  
        - 📦 **Livrezon konplè** – nou voye kòd konplè a ba ou pa imèl epi nou gide ou pou enstalasyon
        
        Kit ou bezwen yon sit wèb, yon zouti lojisyèl sou mezi, oswa yon platfòm sou entènèt gwo echèl – nou konstwi li, se pou ou.
        """,
        "office_photo_caption": "Ekip nou ap travay nan biwo GlobalInternet.py – yon jounen okipe kreye solisyon lojisyèl.",
        "founder": "Fondatè ak CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Enjenyè | Amater AI | Ekspè Python",
        "cv_title": "📄 Sou pwopriyetè a – Gesner Deslandes",
        "cv_intro": "Kreyatè lojisyèl Python | Developè wèb | Kowòdonatè teknik",
        "cv_summary": """
        Lidè ak administratè ki motive anpil, angaje nan ekselans ak presizyon.  
        **Konpetans kle:** Lidèchip, Entèprèt (angle, fransè, kreyòl), Oryantasyon mekanik, Jesyon, Microsoft Office.
        """,
        "cv_experience_title": "💼 Eksperyans pwofesyonèl",
        "cv_experience": """
        **Kowòdonatè teknik** – Orfelina Be Like Brit (2021–kounye a)  
         Mete kanpe reyinyon Zoom, kenbe laptop/tablet, bay sipò teknik chak jou, asire operasyon dijital yo.

        **CEO ak Sèvis entèprèt** – Touris pèsonalize pou gwoup ONG, ekip misyon, ak moun endividyèl.

        **Manadjè flòt / Dispatcher** – J/P Haitian Relief Organization  
         Jere plis pase 20 machin, jounal chofè, orè antretyen ak Excel.

        **Entèprèt medikal** – International Child Care  
         Entèpretasyon medikal egzak angle–fransè–kreyòl.

        **Lidè ekip ak Entèprèt** – ONG Can‑Do  
         Dirije pwojè rekonstriksyon.

        **Pwofesè angle** – Be Like Brit (prezantè a NS4)

        **Tradiktè dokiman** – United Kingdom Glossary ak United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Edikasyon ak Fòmasyon",
        "cv_education": """
        - Lekòl fòmasyon pwofesyonèl – Anglè Ameriken  
        - Enstiti Diesel Ayiti – Mekanik diesel  
        - Sètifikasyon nan biwo (Oktòb 2000)  
        - Diplome lekòl segondè
        """,
        "cv_references": "📞 Referans disponib sou demand.",
        "team_title": "👥 Ekip nou an",
        "team_sub": "Rankontre talan ki dèyè GlobalInternet.py – anboche avril 2026.",
        "team_members": [
            {"name": "Gesner Deslandes", "role": "Fondatè ak CEO", "since": "2021"},
            {"name": "Gesner Junior Deslandes", "role": "Asistan CEO", "since": "Avril 2026"},
            {"name": "Roosevelt Deslandes", "role": "Pwogramè Python", "since": "Avril 2026"},
            {"name": "Sebastien Stephane Deslandes", "role": "Pwogramè Python", "since": "Avril 2026"},
            {"name": "Zendaya Christelle Deslandes", "role": "Sekretè", "since": "Avril 2026"}
        ],
        "services_title": "⚙️ Sèvis nou yo",
        "services": [
            ("🐍 Devlopman Python sou mezi", "Script adapte, otomatizasyon, sistèm bak."),
            ("🤖 AI ak Machine Learning", "Chatbot, modèl prediksyon, apèsi done."),
            ("🗳️ Lojisyèl vòt", "Sekirize, plizyè lang, rezilta an dirè – tankou sistèm Ayiti nou an."),
            ("📊 Tablodbò biznis", "Analiz an tan reyèl ak zouti rapò."),
            ("🌐 Sit wèb ak aplikasyon", "Solisyon full‑stack ki deplwaye sou entènèt."),
            ("📦 Livrezon 24 èdtan", "Nou travay vit – resevwa lojisyèl ou pa imèl, pare pou itilize.")
        ],
        "projects_title": "🏆 Pwojè ak reyalizasyon nou yo",
        "projects_sub": "Solisyon lojisyèl konplè ki te livré bay kliyan – pare pou achte oswa pèsonalize.",
        "project_haiti": "🇭🇹 Lojisyèl Vòt sou Entènèt Ayiti",
        "project_haiti_desc": "Sistèm eleksyon prezidansyèl konplè ak plizyè lang (Kreyòl, franse, angle, panyòl), siveyans an tan reyèl, tablodbò Prezidan CEP (jere kandida, telechaje foto, rapò pwogrè), bilten vòt sekrè ak modpas ki chanje. Itilize pou eleksyon nasyonal.",
        "project_haiti_price": "2,000 $ USD (peman inik)",
        "project_haiti_status": "✅ Disponib – gen ladan kòd sous, enstalasyon ak sipò.",
        "project_haiti_contact": "Kontakte nou pou yon demonstrasyon an dirè",
        "project_dashboard": "📊 Tablodbò entelijan biznis",
        "project_dashboard_desc": "Tablodbò analiz an tan reyèl pou konpayi yo. Konekte ak nenpòt baz done (SQL, Excel, CSV) epi visualize KPI, tandans lavant, envantè ak rapò pèsonalize. Totalman entèaktif ak pèsonalizab.",
        "project_dashboard_price": "1,200 $ USD",
        "project_dashboard_status": "✅ Disponib",
        "project_dashboard_contact": "Demonstrasyon disponib sou demand",
        "project_chatbot": "🤖 Chatbot sipò kliyan AI",
        "project_chatbot_desc": "Chatbot entèlijan ki antrene sou done biznis ou yo. Reponn kesyon kliyan 24/7, diminye chay sipò. Entegre ak sit wèb, WhatsApp oswa Telegram. Bati ak Python ak NLP modèn.",
        "project_chatbot_price": "800 $ USD (debaz) / 1,500 $ USD (avanse)",
        "project_chatbot_status": "✅ Disponib",
        "project_chatbot_contact": "Nou ka antrene l sou kontni espesifik ou",
        "project_school": "🏫 Sistèm jesyon lekòl",
        "project_school_desc": "Platfòm konplè pou lekòl : enskripsyon elèv, jesyon nòt, swivi prezans, portal paran, jenerasyon bilten nòt ak pèsepsyon frè. Plizyè wòl (administratè, pwofesè, paran).",
        "project_school_price": "1,500 $ USD",
        "project_school_status": "✅ Disponib",
        "project_school_contact": "Gen ladan fòmasyon ak deplwaman",
        "project_pos": "📦 Sistèm envantè ak pwen vant",
        "project_pos_desc": "Jesyon envantè sou wèb ak pwen vant pou ti biznis. Lekti kòd ba, alèt stock, rapò vant, jesyon founisè. Mache sou entènèt ak san entènèt.",
        "project_pos_price": "1,000 $ USD",
        "project_pos_status": "✅ Disponib",
        "project_pos_contact": "Pèsonalizab selon bezwen ou",
        "project_scraper": "📈 Ekstraktè wèb pèsonalize ak kanal done",
        "project_scraper_desc": "Ekstraksyon done otomatik nan nenpòt sit wèb, netwaye epi livre kòm Excel/JSON/CSV. Planifikasyon chak jou, chak semenn oswa chak mwa. Pafè pou rechèch mache, siveyans pri oswa jenerasyon leads.",
        "project_scraper_price": "500 – 2,000 $ USD (depann sou konpleksite)",
        "project_scraper_status": "✅ Disponib",
        "project_scraper_contact": "Di nou sous done ou, n ap ba ou pri",
        "project_chess": "♟️ Jwe Echèk Kont Machin nan",
        "project_chess_desc": "Jwèt echèk edikatif ak AI (3 nivo). Chak mouvman eksplike – aprann taktik tankou fouchèt, klou, echèk dekouvri. Gen mòd demo, tablodbò mouvman, ak rapò jwèt konplè. Plizyè lang (angle, franse, panyòl, kreyòl).",
        "project_chess_price": "20 $ USD (peman inik)",
        "project_chess_status": "✅ Disponib – aksè tout lavi, mizajou gratis",
        "project_chess_contact": "Pafè pou aprann echèk",
        "project_accountant": "🧮 Kontablite Excel AI Avanse",
        "project_accountant_desc": "Swit pwofesyonèl kontablite ak jesyon prè. Swiv lajan k ap antre ak sòti, jere prè (moun ki prete, dat, peman), tablodbò ak balans, ekspòte tout rapò an Excel ak PDF. Plizyè lang (angle, fransè, panyòl).",
        "project_accountant_price": "199 $ USD (peman inik)",
        "project_accountant_status": "✅ Disponib – aksè tout lavi, mizajou gratis",
        "project_accountant_contact": "Ideyal pou ti biznis, asosyasyon, moun k ap travay pou kont yo",
        "project_archives": "📜 Baz Done Achiv Nasyonal Ayiti",
        "project_archives_desc": "Baz done konplè pou achiv nasyonal Ayisyen. Sere NIF (Matrikil Fiskal), CIN, Paspò, Pèmi Kondwi, istwa vòt, patenarya ak dokiman. Validasyon ak siyati Minis la, sistèm modpas anyèl, plizyè lang (angle, fransè, panyòl, kreyòl).",
        "project_archives_price": "1,500 $ USD (peman inik)",
        "project_archives_status": "✅ Disponib – gen ladan kòd sous, enstalasyon ak sipò",
        "project_archives_contact": "Ideyal pou achiv gouvènmantal, minis ak enstitisyon",
        "project_dsm": "🛡️ DSM-2026: SISTÈM SEKIRI",
        "project_dsm_desc": "Radar siveyans stratosferik avanse – swiv avyon, satelit ak misil an tan reyèl. Afichaj radar simule ak deteksyon menas, plizyè lang, ak rapò entèlijans telechajab.",
        "project_dsm_price": "299 $ USD (peman inik)",
        "project_dsm_status": "✅ Disponib – lisans tout lavi, mizajou gratis",
        "project_dsm_contact": "Pafè pou demonstrasyon sekirite ak siveyans",
        "project_bi": "📊 Tablodbò Entelijan Biznis",
        "project_bi_desc": "Tablodbò analiz an tan reyèl pou konpayi yo. Konekte SQL, Excel, CSV – visualize KPI, tandans lavant, envantè ak pèfòmans rejyonal. Totalman entèaktif ak filtè dat ak rapò CSV telechajab. Plizyè lang (angle, franse, panyòl, kreyòl).",
        "project_bi_price": "1,200 $ USD (peman inik)",
        "project_bi_status": "✅ Disponib – aksè tout lavi, mizajou gratis",
        "project_bi_contact": "Pafè pou biznis, manadjè ak analis",
        "view_demo": "🎬 Wè demonstrasyon",
        "demo_screenshot": "Aperçu ekran (ranplase ak imaj reyèl)",
        "live_demo": "🔗 Demonstrasyon an dirè",
        "demo_password_hint": "🔐 Modpas demonstrasyon: 20082010",
        "request_info": "Mande enfòmasyon",
        "donation_title": "💖 Sipòte GlobalInternet.py",
        "donation_text": "Ede nou grandi epi kontinye bati lojisyèl inovatif pou Ayiti ak lemonn.",
        "donation_sub": "Donasyon ou sipòte hosting, zouti devlopman ak resous gratis pou devlopè lokal yo.",
        "donation_method": "🇭🇹 Fasil ak rapid – transfè Prisme nan Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limit kantite lajan : jiska 100,000 HTG pou chak tranzaksyon",
        "donation_instruction": "Sèvi ak fonksyon 'Prisme transfer' nan aplikasyon Moncash ou pou voye kontribisyon ou.",
        "donation_bank_title": "🏦 Vireman labank (Compte UNIBANK US)",
        "donation_bank_account": "Nimewo kont: 105-2016-16594727",
        "donation_bank_note": "Pou transfè entènasyonal, sèvi ak kòd SWIFT UNIBANKUS (oswa kontakte nou pou plis detay).",
        "donation_future": "🔜 Byento : transfè labank an USD ak HTG (entènasyonal ak lokal).",
        "donation_button": "💸 Mwen voye don an – notifye m",
        "donation_thanks": "Mèsi anpil! N ap konfime resepsyon nan 24 èdtan. Sipò ou gen anpil valè pou nou! 🇭🇹",
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

# Add office photo after the about text (inside the same column or below)
office_photo_path = "Busy Office Day.jpeg"
if os.path.exists(office_photo_path):
    st.image(office_photo_path, caption=t['office_photo_caption'], use_column_width=True, output_format="JPEG")
else:
    st.info(f"Office photo will appear here once uploaded as '{office_photo_path}'")

# -----------------------------
# CV Section with Photo
# -----------------------------
st.markdown(f"## {t['cv_title']}")

col_photo, col_info = st.columns([1, 2])
with col_photo:
    photo_path = "Gesner Deslandes.JPG"
    if os.path.exists(photo_path):
        img = Image.open(photo_path)
        st.image(img, caption="Gesner Deslandes", use_column_width=True, output_format="PNG")
    else:
        st.info(f"Owner's photo will appear here once uploaded to the repository as '{photo_path}'")
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
# Projects Section (11 projects – including BI Dashboard)
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
        "demo_url": "https://haiti-online-voting-software-ovcwwwrxbhaxyfcyohappnr.streamlit.app/",
        "screenshot": "https://via.placeholder.com/800x400?text=Haiti+Voting+Software"
    },
    {
        "title": t['project_dashboard'],
        "desc": t['project_dashboard_desc'],
        "price": t['project_dashboard_price'],
        "status": t['project_dashboard_status'],
        "contact": t['project_dashboard_contact'],
        "key": "dashboard",
        "demo_url": None,
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
        "demo_url": "https://playchessagainstthemachinemarch2026-hqnjksiy9jemcb4np5pzmp.streamlit.app/",
        "screenshot": "https://via.placeholder.com/800x400?text=Chess+Game"
    },
    {
        "title": t['project_accountant'],
        "desc": t['project_accountant_desc'],
        "price": t['project_accountant_price'],
        "status": t['project_accountant_status'],
        "contact": t['project_accountant_contact'],
        "key": "accountant",
        "demo_url": "https://kpbhc3s8vhggkeo7yh9gzz.streamlit.app/",
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
    },
    {
        "title": t['project_dsm'],
        "desc": t['project_dsm_desc'],
        "price": t['project_dsm_price'],
        "status": t['project_dsm_status'],
        "contact": t['project_dsm_contact'],
        "key": "dsm",
        "demo_url": "https://kbgydmzka2gmk4ubz3pzof.streamlit.app/",
        "screenshot": "https://via.placeholder.com/800x400?text=DSM+Radar"
    },
    {
        "title": t['project_bi'],
        "desc": t['project_bi_desc'],
        "price": t['project_bi_price'],
        "status": t['project_bi_status'],
        "contact": t['project_bi_contact'],
        "key": "bi",
        "demo_url": "https://9enktzu34sxzyvtsymghxd.streamlit.app/",
        "screenshot": "https://via.placeholder.com/800x400?text=BI+Dashboard"
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

                if proj.get("demo_url"):
                    st.markdown(f"<a href='{proj['demo_url']}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                else:
                    if st.button(f"{t['view_demo']}", key=f"demo_{proj['key']}_{lang}"):
                        with st.expander(f"📸 {proj['title']} – {t['demo_screenshot']}", expanded=True):
                            st.image(proj['screenshot'], use_column_width=True)
                            st.caption("Contact us for a live demo URL.")

                if st.button(f"{t['request_info']}", key=f"btn_{proj['key']}_{lang}"):
                    st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{proj['title']}'. Thank you!")

# -----------------------------
# Donation Section (UPDATED with UNIBANK account)
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
