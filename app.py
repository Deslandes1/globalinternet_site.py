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

# ========== SECURITY: AUTOMATED THREAT DETECTION ==========
# NO IPs are pre-blocked - your IP 35.185.209.55 is NOT blocked

BLOCKED_IPS = set([])
suspicious_ips = defaultdict(list)

MALICIOUS_PATHS = [
    "/wp-admin", "/wp-login.php", "/wordpress",
    "/admin", "/administrator", "/admin.php",
    ".env", ".git", ".aws", ".config",
    "/phpmyadmin", "/mysql", "/pma",
    "/backup", "/dump", "/sql",
    "/shell", "/cmd", "/exec",
    "../", "..%2f", "..%252f",
    "' OR '1'='1", "' UNION SELECT",
    "<script", "javascript:", "onerror=",
]

SUSPICIOUS_USER_AGENTS = [
    "python-requests", "curl", "wget", "go-http-client",
    "nikto", "nmap", "sqlmap", "burp", "masscan", "zgrab",
]

def detect_malicious_activity(ip, path, user_agent):
    reasons = []
    for malicious in MALICIOUS_PATHS:
        if malicious.lower() in path.lower():
            reasons.append(f"Suspicious path: {malicious}")
            break
    for suspicious in SUSPICIOUS_USER_AGENTS:
        if suspicious.lower() in user_agent.lower():
            reasons.append(f"Suspicious User-Agent: {user_agent}")
            break
    now = datetime.now()
    suspicious_ips[ip] = [ts for ts in suspicious_ips[ip] if now - ts < timedelta(seconds=60)]
    suspicious_ips[ip].append(now)
    if len(suspicious_ips[ip]) > 50:
        reasons.append(f"Rapid requests: {len(suspicious_ips[ip])} in 60 seconds")
    return reasons

def auto_block_ip(ip, reasons):
    if ip not in BLOCKED_IPS:
        BLOCKED_IPS.add(ip)
        try:
            with open("blocked_ips.log", "a") as f:
                f.write(f"{datetime.now()} - BLOCKED IP: {ip} - Reasons: {', '.join(reasons)}\n")
        except:
            pass

def security_check():
    try:
        visitor_ip = requests.get("https://api.ipify.org", timeout=5).text
        if visitor_ip in BLOCKED_IPS:
            st.error("🚫 ACCESS DENIED: Your IP has been blocked due to suspicious activity.")
            st.stop()
        path = st.context.headers.get("X-Forwarded-Path", "/") if hasattr(st, 'context') else "/"
        user_agent = st.context.headers.get("User-Agent", "unknown") if hasattr(st, 'context') else "unknown"
        reasons = detect_malicious_activity(visitor_ip, path, user_agent)
        if reasons:
            auto_block_ip(visitor_ip, reasons)
            st.error("🚫 ACCESS DENIED: Suspicious activity detected.")
            st.stop()
    except:
        pass

security_check()
# ========== END SECURITY ==========

# ========== RATE LIMITING ==========
def check_rate_limit(max_requests=200, window_seconds=60):
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

# ---------- Supabase setup ----------
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None
    st.warning("⚠️ Comments disabled. Supabase not configured.")

st.set_page_config(page_title="GlobalInternet.py – Python Software Company", page_icon="🌐", layout="wide")

# ---------- Functions for comments & likes ----------
def get_comments(project_key):
    if not supabase:
        return []
    try:
        response = supabase.table("comments").select("*").eq("project_key", project_key).order("timestamp", desc=False).execute()
        return response.data
    except:
        return []

def add_comment(project_key, username, comment, parent_id=0, reply_to_username=""):
    if not supabase:
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
    except:
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

# ---------- Email notification (FIXED - ONLY ONE EMAIL PER SESSION) ----------
def send_visit_notification():
    # Only send ONE email per browser session (no more spam from refreshes/clicks)
    if "email_sent" in st.session_state:
        return
    
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
            st.session_state.email_sent = True  # Mark as sent for this session
    except:
        pass

# Send notification only once per session
send_visit_notification()
check_rate_limit()

# ---------- Language Selection ----------
if "language" not in st.session_state:
    st.session_state.language = "English"

def set_language():
    st.session_state.language = st.session_state._language

# ---------- Complete Multi-language Dictionary (English, French, Chinese, Portuguese) ----------
t = {
    "English": {
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
        "footer_pride": "🇭🇹 Proudly Haitian – serving the world with Python and AI 🇭🇹",
        "comment_section": "💬 Comments & Questions",
        "leave_comment": "Leave a comment",
        "your_name": "Your name (optional)",
        "post_comment": "Post Comment",
        "reply": "💬 Reply",
        "language_select": "🌐 Language",
    },
    "French": {
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Construisez avec Python. Livrez rapidement. Innovez avec l'IA.",
        "hero_desc": "D'Haïti au monde – des logiciels sur mesure qui fonctionnent en ligne.",
        "about_title": "👨‍💻 À propos de l'entreprise",
        "about_text": """
        **GlobalInternet.py** a été fondé par **Gesner Deslandes** – propriétaire, fondateur et ingénieur principal.  
        Nous construisons des logiciels sur mesure pour des clients du monde entier. Comme la Silicon Valley, mais avec une touche haïtienne et des résultats exceptionnels.
        
        - 🧠 **Solutions alimentées par l'IA** – chatbots, analyse de données, automatisation  
        - 🗳️ **Systèmes électoraux complets** – sécurisés, multilingues, en temps réel  
        - 🌐 **Applications web** – tableaux de bord, outils internes, plateformes en ligne  
        - 📦 **Livraison complète** – nous vous envoyons le code complet par email et vous guidons dans l'installation
        
        Que vous ayez besoin d'un site web, d'un outil logiciel personnalisé ou d'une plateforme en ligne complète – nous le construisons, vous le possédez.
        """,
        "office_photo_caption": "Gesner Deslandes parle – présentant GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – notre représentant numérique de l'innovation et de l'expertise logicielle.",
        "founder": "Fondateur & PDG",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Ingénieur | Passionné d'IA | Expert Python",
        "cv_title": "📄 À propos du propriétaire – Gesner Deslandes",
        "cv_intro": "Développeur Python | Créateur de sites web | Coordinateur technique",
        "cv_summary": """
        Leader et gestionnaire exceptionnel avec un engagement envers l'excellence et la précision.  
        **Compétences clés:** Leadership, Interprétation (Anglais, Français, Créole Haïtien), Orientation mécanique, Gestion, Microsoft Office.
        """,
        "cv_experience_title": "💼 Expérience professionnelle",
        "cv_experience": """
        **Coordinateur technique** – Orphelinat Be Like Brit (2021–Présent)  
        Configuration des réunions Zoom, maintenance des ordinateurs portables/tablettes, support technique quotidien.

        **PDG et services d'interprétation** – Tourisme personnalisé pour groupes ONG, équipes missionnaires et particuliers.

        **Gestionnaire de parc / Répartiteur** – J/P Haitian Relief Organization  
        Gestion de 20+ véhicules, journaux de conduite, calendriers de maintenance.

        **Interprète médical** – International Child Care  
        Interprétation médicale précise anglais–français–créole.

        **Chef d'équipe et interprète** – Can‑Do NGO  
        Direction de projets de reconstruction.

        **Professeur d'anglais** – Be Like Brit (Préscolaire à NS4)

        **Traducteur de documents** – United Kingdom Glossary et United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Éducation et formation",
        "cv_education": """
        - École de formation professionnelle – Anglais américain  
        - Institut Diesel d'Haïti – Mécanicien diesel  
        - Certification en informatique de bureau (Octobre 2000)  
        - Diplômé du secondaire
        """,
        "cv_references": "📞 Références disponibles sur demande.",
        "team_title": "👥 Notre équipe",
        "team_sub": "Rencontrez les talents derrière GlobalInternet.py – embauchés avril 2026.",
        "services_title": "⚙️ Nos services",
        "services": [
            ("🐍 Développement Python personnalisé", "Scripts sur mesure, automatisation, systèmes backend."),
            ("🤖 IA et apprentissage automatique", "Chatbots, modèles prédictifs, analyses de données."),
            ("🗳️ Logiciel de vote et d'élection", "Sécurisé, multilingue, résultats en direct – comme notre système Haïtien."),
            ("📊 Tableaux de bord d'entreprise", "Analytique en temps réel et outils de reporting."),
            ("🌐 Sites web et applications web", "Solutions full-stack déployées en ligne."),
            ("📦 Livraison en 24 heures", "Nous travaillons rapidement – recevez votre logiciel par email, prêt à l'emploi."),
            ("📢 Publicité et marketing", "Campagnes digitales, gestion des réseaux sociaux, ciblage IA, rapports de performance.")
        ],
        "projects_title": "🏆 Nos projets et réalisations",
        "projects_sub": "Solutions logicielles livrées aux clients – prêtes à être achetées ou personnalisées.",
        "view_demo": "🎬 Voir la démo",
        "live_demo": "🔗 Démo en direct",
        "demo_password_hint": "🔐 Mot de passe démo: 20082010",
        "request_info": "Demander des informations",
        "buy_now": "💵 Acheter maintenant",
        "donation_title": "💖 Soutenez GlobalInternet.py",
        "donation_text": "Aidez-nous à grandir et à continuer à développer des logiciels innovants pour Haïti et le monde.",
        "donation_sub": "Votre don soutient l'hébergement, les outils de développement et les ressources gratuites pour les développeurs locaux.",
        "donation_method": "🇭🇹 Facile et rapide – Transfert Prisme vers Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limite de montant: Jusqu'à 100 000 HTG par transaction",
        "donation_instruction": "Utilisez la fonction 'Prisme transfer' dans votre application Moncash pour envoyer votre contribution à Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Transfert international via <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Envoyez de l'argent directement à notre numéro de téléphone via l'application SendWave (disponible dans le monde entier).",
        "donation_sendwave_phone": "Téléphone du destinataire: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Virement bancaire (Compte UNIBANK US)",
        "donation_bank_account": "Numéro de compte: 105-2016-16594727",
        "donation_bank_note": "Pour les transferts internationaux, veuillez utiliser le code SWIFT UNIBANKUS (ou contactez-nous pour plus de détails).",
        "donation_future": "🔜 À venir: Virements bancaires en USD et HTG (internationaux et locaux).",
        "donation_button": "💸 J'ai envoyé mon don – prévenez-moi",
        "donation_thanks": "Merci beaucoup ! Nous confirmerons la réception dans les 24 heures. Votre don via Prisme Transfer, Sendwave ou Moncash (Digicel) va directement à Gesner Deslandes au (509)-47385663. Votre soutien signifie tout pour nous ! 🇭🇹",
        "contact_title": "📞 Construisons quelque chose de grand",
        "contact_ready": "Prêt à démarrer votre projet?",
        "contact_phone": "📞 Téléphone / WhatsApp: (509)-47385663",
        "contact_email": "✉️ Email: deslandes78@gmail.com",
        "contact_delivery": "Nous livrons des logiciels complets par email – rapides, fiables et adaptés à vos besoins.",
        "contact_tagline": "GlobalInternet.py – Votre partenaire Python, d'Haïti au monde.",
        "footer_rights": "Tous droits réservés.",
        "footer_founded": "Fondé par Gesner Deslandes | Construit avec Streamlit | Hébergé sur GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Fièrement Haïtien – au service du monde avec Python et l'IA 🇭🇹",
        "comment_section": "💬 Commentaires et questions",
        "leave_comment": "Laisser un commentaire",
        "your_name": "Votre nom (optionnel)",
        "post_comment": "Publier le commentaire",
        "reply": "💬 Répondre",
        "language_select": "🌐 Langue",
    },
    "Chinese": {
        "hero_title": "GlobalInternet.py",
        "hero_sub": "用Python构建。快速交付。用AI创新。",
        "hero_desc": "从海地到世界 – 可在线上工作的定制软件。",
        "about_title": "👨‍💻 关于公司",
        "about_text": """
        **GlobalInternet.py** 由 **Gesner Deslandes** 创立 – 所有者、创始人兼首席工程师。  
        我们为全球客户按需构建**基于Python的软件**。像硅谷一样，但带有海地特色和卓越成果。
        
        - 🧠 **AI驱动解决方案** – 聊天机器人、数据分析、自动化  
        - 🗳️ **完整的选举和投票系统** – 安全、多语言、实时  
        - 🌐 **Web应用程序** – 仪表板、内部工具、在线平台  
        - 📦 **完整包交付** – 我们通过电子邮件向您发送完整代码并指导您安装
        
        无论您需要公司网站、定制软件工具还是完整的在线平台 – 我们构建，您拥有。
        """,
        "office_photo_caption": "Gesner Deslandes 说话头像 – 介绍 GlobalInternet.py",
        "humanoid_photo_caption": "Gesner 人形AI – 我们创新和软件专业知识的数字代表。",
        "founder": "创始人兼CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "工程师 | AI爱好者 | Python专家",
        "cv_title": "📄 关于所有者 – Gesner Deslandes",
        "cv_intro": "Python软件构建者 | 网页开发者 | 技术协调员",
        "cv_summary": """
        极具动力的领导者和经理，致力于卓越和精确。  
        **核心能力：** 领导力、口译（英语、法语、海地克里奥尔语）、机械导向、管理、Microsoft Office。
        """,
        "cv_experience_title": "💼 专业经验",
        "cv_experience": """
        **技术协调员** – Be Like Brit 孤儿院（2021年至今）  
        设置Zoom会议、维护笔记本电脑/平板电脑、提供日常技术支持、确保数字运营顺畅。

        **CEO兼口译服务** – 为NGO团体、宣教团队和个人提供个性化旅游服务。

        **车队经理/调度员** – J/P Haitian Relief Organization  
        管理20多辆车、司机日志、使用Excel进行维护计划。

        **医疗口译员** – International Child Care  
        准确的英语-法语-克里奥尔语医疗口译。

        **团队负责人兼口译员** – Can‑Do NGO  
        领导重建项目。

        **英语教师** – Be Like Brit（学前班到NS4）

        **文件翻译员** – United Kingdom Glossary & United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 教育与培训",
        "cv_education": """
        - 职业培训学校 – 美式英语  
        - 海地柴油学院 – 柴油机械师  
        - 办公计算认证（2000年10月）  
        - 高中毕业生
        """,
        "cv_references": "📞 可根据要求提供推荐信。",
        "team_title": "👥 我们的团队",
        "team_sub": "认识 GlobalInternet.py 背后的才华横溢的团队 – 2026年4月聘用。",
        "services_title": "⚙️ 我们的服务",
        "services": [
            ("🐍 定制Python开发", "定制脚本、自动化、后端系统。"),
            ("🤖 AI与机器学习", "聊天机器人、预测模型、数据洞察。"),
            ("🗳️ 选举和投票软件", "安全、多语言、实时结果 – 像我们的海地系统一样。"),
            ("📊 商业仪表板", "实时分析和报告工具。"),
            ("🌐 网站和Web应用程序", "在线部署的全栈解决方案。"),
            ("📦 24小时交付", "我们工作快速 – 通过电子邮件获取您的软件，随时可用。"),
            ("📢 广告与营销", "数字营销活动、社交媒体管理、AI驱动定向、绩效报告。根据范围从150美元到1,200美元。")
        ],
        "projects_title": "🏆 我们的项目和成就",
        "projects_sub": "交付给客户的完整软件解决方案 – 可供您购买或定制。",
        "view_demo": "🎬 查看演示",
        "live_demo": "🔗 在线演示",
        "demo_password_hint": "🔐 演示密码: 20082010",
        "request_info": "索取信息",
        "buy_now": "💵 立即购买",
        "donation_title": "💖 支持 GlobalInternet.py",
        "donation_text": "帮助我们成长并继续为海地和世界构建创新软件。",
        "donation_sub": "您的捐款支持托管、开发工具和为本地开发者提供的免费资源。",
        "donation_method": "🇭🇹 简单快捷 – 通过Moncash (Digicel)进行Prisme转账",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "金额限制: 每笔交易最高100,000 HTG",
        "donation_instruction": "只需在您的Moncash应用中使用'Prisme transfer'功能将您的捐款发送给Gesner Deslandes。",
        "donation_sendwave_title": "🌍 通过<span class='blue-text'>SendWave</span>进行国际转账",
        "donation_sendwave_instruction": "使用SendWave应用（全球可用）直接将资金发送到我们的电话号码。",
        "donation_sendwave_phone": "收款人电话: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 银行转账（UNIBANK美国账户）",
        "donation_bank_account": "账户号码: 105-2016-16594727",
        "donation_bank_note": "对于国际转账，请使用SWIFT代码UNIBANKUS（或联系我们获取详细信息）。",
        "donation_future": "🔜 即将推出：美元和HTG的银行对银行转账（国际和本地）。",
        "donation_button": "💸 我已发送捐款 – 通知我",
        "donation_thanks": "非常感谢！我们将在24小时内确认收款。您通过Prisme Transfer、Sendwave或Moncash（Digicel）向(509)-47385663的Gesner Deslandes捐款。您的支持对我们意义重大！🇭🇹",
        "contact_title": "📞 让我们一起构建伟大的东西",
        "contact_ready": "准备开始您的项目？",
        "contact_phone": "📞 电话/WhatsApp: (509)-47385663",
        "contact_email": "✉️ 邮箱: deslandes78@gmail.com",
        "contact_delivery": "我们通过电子邮件交付完整的软件包 – 快速、可靠、为您量身定制。",
        "contact_tagline": "GlobalInternet.py – 您的Python合作伙伴，从海地到世界。",
        "footer_rights": "版权所有。",
        "footer_founded": "由Gesner Deslandes创立 | 使用Streamlit构建 | 托管于GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 自豪的海地人 – 用Python和AI服务世界 🇭🇹",
        "comment_section": "💬 评论与问题",
        "leave_comment": "发表评论",
        "your_name": "您的名字（可选）",
        "post_comment": "发布评论",
        "reply": "💬 回复",
        "language_select": "🌐 语言",
    },
    "Portuguese": {
        "hero_title": "GlobalInternet.py",
        "hero_sub": "Construa com Python. Entregue com Velocidade. Inove com IA.",
        "hero_desc": "Do Haiti para o mundo – software personalizado que funciona online.",
        "about_title": "👨‍💻 Sobre a Empresa",
        "about_text": """
        **GlobalInternet.py** foi fundada por **Gesner Deslandes** – proprietário, fundador e engenheiro principal.  
        Construímos **software baseado em Python** sob demanda para clientes em todo o mundo. Como o Vale do Silício, mas com um toque haitiano e resultados excepcionais.
        
        - 🧠 **Soluções alimentadas por IA** – chatbots, análise de dados, automação  
        - 🗳️ **Sistemas eleitorais completos** – seguros, multilíngues, em tempo real  
        - 🌐 **Aplicações web** – dashboards, ferramentas internas, plataformas online  
        - 📦 **Entrega completa** – enviamos o código completo por e-mail e guiamos você na instalação
        
        Quer você precise de um site corporativo, uma ferramenta de software personalizada ou uma plataforma online completa – nós construímos, você possui.
        """,
        "office_photo_caption": "Gesner Deslandes falando avatar – apresentando GlobalInternet.py",
        "humanoid_photo_caption": "Gesner Humanoid AI – nosso representante digital de inovação e expertise em software.",
        "founder": "Fundador e CEO",
        "founder_name": "Gesner Deslandes",
        "founder_title": "Engenheiro | Entusiasta de IA | Especialista em Python",
        "cv_title": "📄 Sobre o Proprietário – Gesner Deslandes",
        "cv_intro": "Construtor de Software Python | Desenvolvedor Web | Coordenador de Tecnologia",
        "cv_summary": """
        Líder e gerente excepcionalmente motivado, com compromisso com a excelência e precisão.  
        **Competências principais:** Liderança, Interpretação (Inglês, Francês, Crioulo Haitiano), Orientação mecânica, Gestão, Microsoft Office.
        """,
        "cv_experience_title": "💼 Experiência Profissional",
        "cv_experience": """
        **Coordenador de Tecnologia** – Orfanato Be Like Brit (2021–Presente)  
        Configurar reuniões Zoom, manter laptops/tablets, fornecer suporte técnico diário, garantir operações digitais eficientes.

        **CEO e Serviços de Interpretação** – Turismo personalizado para grupos de ONGs, equipes missionárias e indivíduos.

        **Gerente de Frota / Despachante** – J/P Haitian Relief Organization  
        Gerenciei mais de 20 veículos, registros de motoristas, cronogramas de manutenção usando Excel.

        **Intérprete Médico** – International Child Care  
        Interpretação médica precisa Inglês–Francês–Crioulo.

        **Líder de Equipe e Intérprete** – Can‑Do NGO  
        Liderei projetos de reconstrução.

        **Professor de Inglês** – Be Like Brit (Pré-escola ao NS4)

        **Tradutor de Documentos** – United Kingdom Glossary e United States Work‑Rise Company
        """,
        "cv_education_title": "🎓 Educação e Treinamento",
        "cv_education": """
        - Escola de Treinamento Vocacional – Inglês Americano  
        - Instituto Diesel do Haiti – Mecânico de Diesel  
        - Certificação em Informática (Outubro de 2000)  
        - Ensino Médio Completo
        """,
        "cv_references": "📞 Referências disponíveis mediante solicitação.",
        "team_title": "👥 Nossa Equipe",
        "team_sub": "Conheça os talentos por trás da GlobalInternet.py – contratados em abril de 2026.",
        "services_title": "⚙️ Nossos Serviços",
        "services": [
            ("🐍 Desenvolvimento Python Personalizado", "Scripts personalizados, automação, sistemas backend."),
            ("🤖 IA e Aprendizado de Máquina", "Chatbots, modelos preditivos, insights de dados."),
            ("🗳️ Software de Eleição e Votação", "Seguro, multilíngue, resultados ao vivo – como nosso sistema do Haiti."),
            ("📊 Dashboards de Negócios", "Análise em tempo real e ferramentas de relatórios."),
            ("🌐 Sites e Aplicativos Web", "Soluções full-stack implantadas online."),
            ("📦 Entrega em 24 Horas", "Trabalhamos rápido – receba seu software por e-mail, pronto para usar."),
            ("📢 Publicidade e Marketing", "Campanhas digitais, gerenciamento de mídias sociais, segmentação por IA, relatórios de desempenho. De $150 a $1.200 dependendo do escopo.")
        ],
        "projects_title": "🏆 Nossos Projetos e Realizações",
        "projects_sub": "Soluções de software entregues aos clientes – prontas para você comprar ou personalizar.",
        "view_demo": "🎬 Ver Demonstração",
        "live_demo": "🔗 Demonstração ao Vivo",
        "demo_password_hint": "🔐 Senha de demonstração: 20082010",
        "request_info": "Solicitar Informações",
        "buy_now": "💵 Comprar Agora",
        "donation_title": "💖 Apoie a GlobalInternet.py",
        "donation_text": "Ajude-nos a crescer e continuar construindo software inovador para o Haiti e o mundo.",
        "donation_sub": "Sua doação apoia hospedagem, ferramentas de desenvolvimento e recursos gratuitos para desenvolvedores locais.",
        "donation_method": "🇭🇹 Fácil e rápido – Transferência Prisme para Moncash (Digicel)",
        "donation_phone": "📱 (509)-47385663",
        "donation_limit": "Limite de valor: Até 100.000 HTG por transação",
        "donation_instruction": "Basta usar o recurso 'Prisme transfer' no seu aplicativo Moncash para enviar sua contribuição a Gesner Deslandes.",
        "donation_sendwave_title": "🌍 Transferência internacional via <span class='blue-text'>SendWave</span>",
        "donation_sendwave_instruction": "Envie dinheiro diretamente para nosso número de telefone usando o aplicativo SendWave (disponível mundialmente).",
        "donation_sendwave_phone": "Telefone do destinatário: (509) 4738-5663 (Gesner Deslandes)",
        "donation_bank_title": "🏦 Transferência Bancária (Conta UNIBANK US)",
        "donation_bank_account": "Número da conta: 105-2016-16594727",
        "donation_bank_note": "Para transferências internacionais, use o código SWIFT UNIBANKUS (ou entre em contato para mais detalhes).",
        "donation_future": "🔜 Em breve: Transferências bancárias em USD e HTG (internacionais e locais).",
        "donation_button": "💸 Enviei minha doação – me notifique",
        "donation_thanks": "Muito obrigado! Confirmaremos o recebimento dentro de 24 horas. Sua doação via Prisme Transfer, Sendwave ou Moncash (Digicel) vai diretamente para Gesner Deslandes no (509)-47385663. Seu apoio significa muito para nós! 🇭🇹",
        "contact_title": "📞 Vamos Construir Algo Grande",
        "contact_ready": "Pronto para começar seu projeto?",
        "contact_phone": "📞 Telefone / WhatsApp: (509)-47385663",
        "contact_email": "✉️ Email: deslandes78@gmail.com",
        "contact_delivery": "Entregamos pacotes de software completos por e-mail – rápidos, confiáveis e adaptados a você.",
        "contact_tagline": "GlobalInternet.py – Seu parceiro Python, do Haiti para o mundo.",
        "footer_rights": "Todos os direitos reservados.",
        "footer_founded": "Fundado por Gesner Deslandes | Construído com Streamlit | Hospedado no GitHub + Streamlit Cloud",
        "footer_pride": "🇭🇹 Orgulhosamente Haitiano – servindo o mundo com Python e IA 🇭🇹",
        "comment_section": "💬 Comentários e Perguntas",
        "leave_comment": "Deixar um comentário",
        "your_name": "Seu nome (opcional)",
        "post_comment": "Publicar Comentário",
        "reply": "💬 Responder",
        "language_select": "🌐 Idioma",
    }
}

team_members = [
    {"name": "Gesner Deslandes", "role": "Founder & CEO", "since": "2021", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes.JPG"},
    {"name": "Gesner Junior Deslandes", "role": "Assistant to CEO", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/dreamina-2026-04-18-6690-Change%20the%20man's%20attire%20to%20a%20professiona....jpeg"},
    {"name": "Roosevelt Deslandes", "role": "Python Programmer", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Roosevelt%20%20Software%20Builder.jpeg"},
    {"name": "Sebastien Stephane Deslandes", "role": "Python Programmer", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/35372.jpg"},
    {"name": "Zendaya Christelle Deslandes", "role": "Secretary", "since": "April 2026", "img": "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/IMG_1411.jpg"}
]

# Project data for all 31 projects
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

project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course"
]

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
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar with Language Selector (4 languages) ----------
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=60)
st.sidebar.selectbox(
    t[st.session_state.language]["language_select"],
    options=["English", "French", "Chinese", "Portuguese"],
    key="_language",
    on_change=set_language
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Founder & Developer:**")
st.sidebar.markdown("Gesner Deslandes")
st.sidebar.markdown("📞 WhatsApp: (509) 4738-5663")
st.sidebar.markdown("📧 Email: deslandes78@gmail.com")
st.sidebar.markdown("---")
st.sidebar.markdown("### © 2026 GlobalInternet.py")
st.sidebar.markdown("All rights reserved")

# Get current language dictionary
lang = t[st.session_state.language]

# ---------- Hero Section ----------
st.markdown(f"""
<div class="hero">
    <span class="big-globe">🌐</span>
    <h1>{lang['hero_title']}</h1>
    <p>{lang['hero_sub']}</p>
    <p style="font-size:1rem;">{lang['hero_desc']}</p>
</div>
""", unsafe_allow_html=True)

# ---------- About Section ----------
st.markdown(f"## {lang['about_title']}")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(lang['about_text'])
with col2:
    st.markdown(f"""
    <div class="card">
        <h3>{lang['founder']}</h3>
        <p><strong>{lang['founder_name']}</strong></p>
        <p>{lang['founder_title']}</p>
        <p>📞 (509)-47385663</p>
        <p>✉️ deslandes78@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Avatar Video ----------
video_url = "https://github.com/Deslandes1/Gesner-Deslandes-Avatar/blob/main/avatar_video.mp4.mp4?raw=true"
st.video(video_url, format="video/mp4", start_time=0)
st.caption(lang['office_photo_caption'])

# ---------- CV Section ----------
st.markdown(f"## {lang['cv_title']}")
col_photo, col_info = st.columns([1, 2])
with col_photo:
    owner_video_url = "https://raw.githubusercontent.com/Deslandes1/globalinternet_site.py/main/Gesner%20Deslandes%20The%20Owner%20(1).mp4"
    st.video(owner_video_url)
    st.caption("Gesner Deslandes - Owner & Founder")
with col_info:
    st.markdown(f"### {lang['cv_intro']}")
    st.markdown(lang['cv_summary'])
with st.expander(f"{lang['cv_experience_title']} (click to view)"):
    st.markdown(lang['cv_experience'])
with st.expander(f"{lang['cv_education_title']} (click to view)"):
    st.markdown(lang['cv_education'])
st.caption(lang['cv_references'])
st.divider()

# ---------- Team Section ----------
st.markdown(f"## {lang['team_title']}")
st.markdown(f"*{lang['team_sub']}*")
cols = st.columns(len(team_members))
for idx, member in enumerate(team_members):
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
st.markdown(f"## {lang['services_title']}")
services = lang['services']
cols = st.columns(3)
for i, (title, desc) in enumerate(services):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- Projects Section WITH COMMENTS ----------
st.markdown(f"## {lang['projects_title']}")
st.markdown(f"*{lang['projects_sub']}*")

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
                    st.markdown(f"<a href='{demo_urls[key]}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{lang['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(lang['demo_password_hint'])
                else:
                    st.info("📹 Live demo available upon request. Contact us for a private walkthrough.")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    subject = f"Purchase: {title}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the software: {title} at {price}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; cursor:pointer;">💵 {lang["buy_now"]}</button></a>', unsafe_allow_html=True)
                with col_btn2:
                    if st.button(f"{lang['request_info']}", key=f"info_{key}"):
                        st.info(f"Please contact us at deslandes78@gmail.com or call (509)-47385663 to discuss '{title}'. Thank you!")

            # ========== COMMENT SECTION ==========
            st.markdown(f"#### {lang['comment_section']}")
            comments = get_comments(key)
            
            for comment in comments:
                if comment["parent_id"] == 0:
                    st.markdown(f"""
                    <div class="comment-box">
                        <div class="comment-meta">
                            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]}
                        </div>
                        <div>{comment['comment']}</div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"❤️ {comment['likes']}", key=f"like_{key}_{comment['id']}"):
                        add_like(comment['id'])
                        st.rerun()
                    
                    if st.button(lang['reply'], key=f"reply_{key}_{comment['id']}"):
                        st.session_state[f"reply_to_{comment['id']}"] = True
                    
                    if st.session_state.get(f"reply_to_{comment['id']}", False):
                        with st.form(key=f"reply_form_{comment['id']}"):
                            reply_name = st.text_input(lang['your_name'], key=f"reply_name_{comment['id']}")
                            reply_text = st.text_area(lang['leave_comment'], key=f"reply_text_{comment['id']}")
                            if st.form_submit_button(lang['post_comment']):
                                if reply_text.strip():
                                    add_comment(key, reply_name if reply_name.strip() else "Anonymous", reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
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
                        if st.button(f"❤️ {reply['likes']}", key=f"like_reply_{key}_{reply['id']}"):
                            add_like(reply['id'])
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form(key=f"comment_form_{key}"):
                st.markdown(f"**{lang['leave_comment']}**")
                name = st.text_input(lang['your_name'], key=f"name_{key}")
                comment_text = st.text_area("", key=f"comment_{key}")
                if st.form_submit_button(lang['post_comment']):
                    if comment_text.strip():
                        add_comment(key, name if name.strip() else "Anonymous", comment_text)
                        st.rerun()
                    else:
                        st.warning("Please enter a comment.")
            st.markdown("---")
            # ========== END COMMENT SECTION ==========

# ---------- Donation Section ----------
st.markdown(f"## {lang['donation_title']}")
st.markdown(f"""
<div class="donation-box">
    <h3>{lang['donation_text']}</h3>
    <p>{lang['donation_sub']}</p>
    <br>
    <p><strong>{lang['donation_method']}</strong></p>
    <p style="font-size:1.5rem; font-weight:bold;">{lang['donation_phone']}</p>
    <p><strong>{lang['donation_limit']}</strong></p>
    <p><em>{lang['donation_instruction']}</em></p>
    <br>
    <p><strong>{lang['donation_sendwave_title']}</strong></p>
    <p>{lang['donation_sendwave_instruction']}</p>
    <p style="font-size:1.2rem; font-weight:bold;">{lang['donation_sendwave_phone']}</p>
    <br>
    <p><strong>{lang['donation_bank_title']}</strong></p>
    <p style="font-size:1.2rem; font-weight:bold;">{lang['donation_bank_account']}</p>
    <p><em>{lang['donation_bank_note']}</em></p>
    <br>
    <p><strong>{lang['donation_future']}</strong></p>
</div>
""", unsafe_allow_html=True)

if st.button(lang['donation_button']):
    st.success(lang['donation_thanks'])

# ---------- Contact Section ----------
st.markdown(f"## {lang['contact_title']}")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: center; background-color: #e9ecef; padding: 2rem; border-radius: 20px;">
        <h3>{lang['contact_ready']}</h3>
        <p>{lang['contact_phone']}</p>
        <p>{lang['contact_email']}</p>
        <p>{lang['contact_delivery']}</p>
        <p><em>{lang['contact_tagline']}</em></p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} GlobalInternet.py – {lang['footer_rights']}</p>
    <p>{lang['footer_founded']}</p>
    <p>{lang['footer_pride']}</p>
</div>
""", unsafe_allow_html=True)