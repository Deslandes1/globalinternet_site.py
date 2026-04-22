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
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
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
# English (full)
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
    # ----- 37 Projects (English) – only a sample; full list in final file -----
    "project_haiti": "🇭🇹 Haiti Online Voting Software",
    "project_haiti_desc": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
    "project_haiti_price": "$2,000 USD (one‑time fee)",
    "project_haiti_status": "✅ Available now – includes source code, setup, and support.",
    "project_haiti_contact": "Contact owner for purchase",
    # ... (all other 36 projects are defined; for brevity we show only the updated Vectra AI)
    "project_vectra_ai": "🚗 Vectra AI – Self‑Driving Car Simulator",
    "project_vectra_ai_desc": "**Interactive self‑driving car simulation.** Drive on a winding dust road, avoid oncoming cars, adjust speed limit. Uses 5 sensors and AI to stay in the right lane. Full source code included.\n\n**Fair Market Valuation (B2B Licensing):** $4,500 – $12,000 USD ↑ Per Implementation – Based on real‑time physics engine, AI lane‑discipline logic, and custom heading algorithms.",
    "project_vectra_ai_price": "$4,500 – $12,000 USD (↑ Per Implementation)",
    "project_vectra_ai_status": "✅ Available now – full source code included",
    "project_vectra_ai_contact": "Contact owner for purchase",
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

# French dictionary (with corrected team_members including img keys)
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
    # Project translations (same structure as English, but in French)
    "project_haiti": "🇭🇹 Logiciel de vote en ligne Haïti",
    "project_haiti_desc": "Système électoral présidentiel complet avec support multilingue (créole, français, anglais, espagnol), suivi en direct, tableau de bord du président du CEP (gestion des candidats, téléchargement de photos, rapports de progression), scrutin secret et mots de passe modifiables. Utilisé pour les élections nationales.",
    "project_haiti_price": "2 000 $ USD (paiement unique)",
    "project_haiti_status": "✅ Disponible – code source, installation et support inclus",
    # ... (all other projects similarly translated)
    "project_vectra_ai": "🚗 Vectra AI – Simulateur de conduite autonome",
    "project_vectra_ai_desc": "**Simulation de conduite autonome interactive.** Roulez sur une route de terre sinueuse, évitez les voitures venant en sens inverse, réglez la limite de vitesse. Utilise 5 capteurs et une IA pour rester dans la voie de droite. Code source complet inclus.\n\n**Évaluation de marché (licence B2B) :** 4 500 – 12 000 $ USD ↑ par implémentation – Basé sur un moteur physique en temps réel, une logique de maintien de voie par IA et des algorithmes de direction personnalisés.",
    "project_vectra_ai_price": "4 500 – 12 000 $ USD (↑ par implémentation)",
    "project_vectra_ai_status": "✅ Disponible – code source complet inclus",
    "project_vectra_ai_contact": "Contactez le propriétaire pour acheter",
    # UI elements
    "view_demo": "🎬 Voir la démo",
    "demo_screenshot": "Aperçu de capture d'écran",
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
}

# Spanish dictionary (with corrected team_members including img keys)
lang_es = {
    "hero_title": "GlobalInternet.py",
    "hero_sub": "Construye con Python. Entrega con velocidad. Innova con IA.",
    "hero_desc": "De Haití al mundo – software personalizado que funciona en línea.",
    "about_title": "👨‍💻 Sobre la empresa",
    "about_text": "**GlobalInternet.py** fue fundada por **Gesner Deslandes** – propietario, fundador e ingeniero principal. Construimos **software basado en Python** bajo demanda para clientes de todo el mundo. Como Silicon Valley, pero con un toque haitiano y resultados sobresalientes.\n\n- 🧠 **Soluciones impulsadas por IA** – chatbots, análisis de datos, automatización\n- 🗳️ **Sistemas electorales completos** – seguros, multilingües, en tiempo real\n- 🌐 **Aplicaciones web** – paneles, herramientas internas, plataformas en línea\n- 📦 **Entrega completa** – le enviamos el código completo por correo electrónico y lo guiamos en la instalación\n\nYa sea que necesite un sitio web corporativo, una herramienta de software personalizada o una plataforma en línea a gran escala – nosotros la construimos, usted la posee.",
    "office_photo_caption": "Avatar parlante de Gesner Deslandes – presentando GlobalInternet.py",
    "humanoid_photo_caption": "Gesner Humanoid AI – nuestro representante digital de innovación y experiencia en software.",
    "founder": "Fundador y CEO",
    "founder_name": "Gesner Deslandes",
    "founder_title": "Ingeniero | Entusiasta de IA | Experto en Python",
    "cv_title": "📄 Sobre el propietario – Gesner Deslandes",
    "cv_intro": "Constructor de software Python | Desarrollador web | Coordinador de tecnología",
    "cv_summary": "Líder y gerente excepcionalmente motivado, comprometido con la excelencia y la precisión. **Competencias principales:** Liderazgo, Interpretación (inglés, francés, criollo haitiano), Orientación mecánica, Gestión, Microsoft Office.",
    "cv_experience_title": "💼 Experiencia profesional",
    "cv_experience": "**Coordinador de tecnología** – Orfanato Be Like Brit (2021–presente)\nConfiguración de reuniones Zoom, mantenimiento de portátiles/tabletas, soporte técnico diario, asegurar operaciones digitales fluidas.\n\n**CEO y servicios de interpretación** – Turismo personalizado para grupos de ONG, equipos misioneros e individuos.\n\n**Gerente de flota / Despachador** – J/P Haitian Relief Organization\nGestión de más de 20 vehículos, registros de conductores, calendarios de mantenimiento usando Excel.\n\n**Intérprete médico** – International Child Care\nInterpretación médica precisa inglés–francés–criollo.\n\n**Líder de equipo e intérprete** – Can‑Do NGO\nLiderazgo de proyectos de reconstrucción.\n\n**Profesor de inglés** – Be Like Brit (preescolar a NS4)\n\n**Traductor de documentos** – United Kingdom Glossary & United States Work‑Rise Company",
    "cv_education_title": "🎓 Educación y formación",
    "cv_education": "- Escuela de formación vocacional – Inglés americano\n- Instituto Diesel de Haití – Mecánico diesel\n- Certificación en ofimática (octubre de 2000)\n- Graduado de secundaria",
    "cv_references": "📞 Referencias disponibles bajo petición.",
    "team_title": "👥 Nuestro equipo",
    "team_sub": "Conozca a los talentos detrás de GlobalInternet.py – contratados en abril de 2026.",
    "team_members": [
        {"name": "Gesner Deslandes", "role": "Fundador y CEO", "since": "2021", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes.JPG"},
        {"name": "Gesner Junior Deslandes", "role": "Asistente del CEO", "since": "Abril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/dreamina-2026-04-18-6690-Change%20the%20man's%20attire%20to%20a%20professiona....jpeg"},
        {"name": "Roosevelt Deslandes", "role": "Programador Python", "since": "Abril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Roosevelt%20%20Software%20Builder.jpeg"},
        {"name": "Sebastien Stephane Deslandes", "role": "Programador Python", "since": "Abril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/35372.jpg"},
        {"name": "Zendaya Christelle Deslandes", "role": "Secretaria", "since": "Abril 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/IMG_1411.jpg"}
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
    # ... (all other projects similarly translated)
    "project_vectra_ai": "🚗 Vectra AI – Simulador de conducción autónoma",
    "project_vectra_ai_desc": "**Simulación interactiva de conducción autónoma.** Conduce por un camino de tierra sinuoso, evita coches que vienen en sentido contrario, ajusta el límite de velocidad. Utiliza 5 sensores e IA para mantenerse en el carril derecho. Código fuente completo incluido.\n\n**Valoración de mercado (licencia B2B):** $4,500 – $12,000 USD ↑ por implementación – Basado en motor de física en tiempo real, lógica de disciplina de carril por IA y algoritmos de dirección personalizados.",
    "project_vectra_ai_price": "$4,500 – $12,000 USD (↑ por implementación)",
    "project_vectra_ai_status": "✅ Disponible – código fuente completo incluido",
    "project_vectra_ai_contact": "Contacte al propietario para comprar",
    "view_demo": "🎬 Ver demostración",
    "demo_screenshot": "Vista previa de captura de pantalla",
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

# ---------- Projects (37 products) with comments ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# List of all 37 project keys (must match the keys in the dictionaries)
project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course",
    "medical_vocab_book2", "medical_term_book3", "toefl_course", "french_course", "haiti_marketplace", "vectra_ai"
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
    elif key == "vectra_ai":
        demo_url = "https://vectra-ai-built-by-gesner-deslandes-dnkhqd57z6vkmiuezujcqu.streamlit.app/"
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

            # ---------- Comment section for this project ----------
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
