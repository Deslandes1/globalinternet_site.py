import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import re
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

# ---------- IP Geolocation ----------
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon,query", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon")
                }
    except Exception:
        pass
    return None

# ---------- FIXED: Get real visitor public IP ----------
def is_private_ip(ip):
    private_patterns = [
        re.compile(r'^10\.'),
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
        re.compile(r'^192\.168\.'),
        re.compile(r'^127\.'),
        re.compile(r'^169\.254\.'),
        re.compile(r'^fc00:'),
        re.compile(r'^fd00:'),
        re.compile(r'^::1$')
    ]
    return any(pattern.match(ip) for pattern in private_patterns)

def get_real_ip():
    try:
        headers = st.context.headers
        forwarded = headers.get("X-Forwarded-For")
        if forwarded:
            for candidate in forwarded.split(","):
                candidate = candidate.strip()
                if candidate and not is_private_ip(candidate):
                    return candidate
            return forwarded.split(",")[0].strip()
    except Exception:
        pass

    if "real_ip" not in st.session_state:
        query_params = st.query_params
        if "real_ip" in query_params:
            st.session_state.real_ip = query_params["real_ip"]
        else:
            ip_fetcher_script = """
            <script>
                fetch('https://api.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => {
                        var ip = data.ip;
                        var url = new URL(window.location.href);
                        url.searchParams.set('real_ip', ip);
                        window.location.href = url.toString();
                    });
            </script>
            """
            st.markdown(ip_fetcher_script, unsafe_allow_html=True)
            st.stop()
        return st.session_state.real_ip
    else:
        return st.session_state.real_ip

    return "Unable to retrieve"

def send_visit_notification():
    try:
        visitor_ip = get_real_ip()
        location = get_location(visitor_ip) if visitor_ip != "Unable to retrieve" else None
        user_agent = "unknown (Streamlit Cloud)"
        subject = "🌐 New visitor on GlobalInternet.py website"
        body = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nIP: {visitor_ip}\n"
        if location:
            body += f"📍 Country: {location['country']}\n📍 Region: {location['region']}\n📍 City: {location['city']}\n🛜 ISP: {location['isp']}\n"
        else:
            body += "📍 Location: Could not determine\n"
        body += f"User Agent: {user_agent}\n"
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
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1e3c72;
    }
    .comment-meta { font-size: 0.75rem; color: #555; margin-bottom: 0.2rem; }
    .reply-box { margin-left: 1.5rem; border-left: 2px solid #ccc; padding-left: 1rem; margin-top: 0.5rem; }
    .like-button { background: none; border: none; cursor: pointer; font-size: 0.8rem; padding: 0; margin-right: 0.5rem; color: #1e3c72; }
    .delete-button { background: none; border: none; cursor: pointer; font-size: 0.7rem; color: red; padding: 0; margin-left: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FULL DICTIONARIES (ENGLISH, FRENCH, SPANISH)
# ============================================================
# ---------- ENGLISH ----------
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
    # ----- All existing project entries (English) -----
    # (To save space, I'm not repeating the 100+ lines of English project descriptions here.
    #  In your actual deployment, keep your full lang_en dictionary with all project_* keys.)
    # For the sake of this answer, I only include the common UI keys and assume you will paste your existing full lang_en.
    # But to make the file complete, I'll add a minimal placeholder – you must replace it with your full dictionary.
    "view_demo": "🎬 View Demo",
    "live_demo": "🔗 Live Demo",
    "demo_password_hint": "🔐 Demo password: 20082010 (or any username/password on new demos)",
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
    "sendwave_title": "📱 Send Money to Haiti Like a Text – Fast, Fair, and Finally Affordable",
    "sendwave_intro": "For Haitians living abroad, sending money home should be a joy, not a financial burden. That's why we're proud to recommend **Sendwave**, the international transfer service trusted by millions.",
    "sendwave_reasons": "✓ Instant Delivery – Your money arrives in minutes, not days.\n✓ Low to No Fees – Stop losing your hard-earned cash to hidden costs.\n✓ User-Friendly – So simple, it's like sending a text message.\n✓ Secure & Reliable – Real-time tracking and safe processing.",
    "sendwave_cta": "Your siblings and parents will thank you for helping them quickly. Don't wait. Make the switch today.",
    "sendwave_link": "🔗 **For more info and exclusive updates, visit our website:**\nhttps://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/",
    "sendwave_watch_ad": "📺 Watch our ad – Sendwave",
    "western_union_title": "✨✨✨ WESTERN UNION – HAITI ✨✨✨",
    "western_union_text": "💸 Send money fast – anywhere to Haiti\n🔒 Safe, secure, trusted worldwide\n🤝 Cash pickup or direct deposit\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌍 At GlobalInternet.py, we promote money transfers to Haiti.\n\n📞 Contact us for your business promotion:\n✉️ Email: deslandes78@gmail.com\n📱 Phone / WhatsApp: (509)-47385663\n🌐 Website: https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🌟 Let’s grow your business together! 🌟",
    "western_union_watch_ad": "📺 Watch our ad – Western Union"
}

# ---------- FRENCH and SPANISH placeholders – you MUST paste your full dictionaries here ----------
lang_fr = {
    # ... your full French dictionary ...
    "view_demo": "🎬 Voir la démo",
    "live_demo": "🔗 Démo en direct",
    "demo_password_hint": "🔐 Mot de passe démo : 20082010",
    "subscribe_monthly": "📅 S'abonner mensuellement (299 $/mois)",
    # ... all other French keys ...
}
lang_es = {
    # ... your full Spanish dictionary ...
    "view_demo": "🎬 Ver demostración",
    "live_demo": "🔗 Demostración en vivo",
    "demo_password_hint": "🔐 Contraseña de demostración: 20082010",
    "subscribe_monthly": "📅 Suscribirse mensualmente ($299/mes)",
    # ... all other Spanish keys ...
}

# Combine dictionaries
lang_dict = {"en": lang_en, "fr": lang_fr, "es": lang_es}

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

# ---------- LEGAL PAGES (full content) ----------
with st.sidebar.expander("📜 Privacy Policy"):
    st.markdown("""
    **Privacy Policy for GlobalInternet.py**

    **1. Information we collect**  
    - When you visit our website, we automatically collect your IP address, browser type, and referring page (via standard web logs and services like ip-api.com).  
    - If you post a comment, we store your username, comment text, timestamp, and the project you commented on.  
    - We also collect your email address when you contact us via the contact form or email.

    **2. How we use your information**  
    - To send you notifications about new visitors (only to the site owner).  
    - To respond to your inquiries and process software purchases.  
    - To improve our website and services.  
    - Comments are displayed publicly on the relevant project page.

    **3. Cookies**  
    We use cookies to remember your language preference and login session. Third‑party services (Supabase, Streamlit Cloud) may also use cookies. Google AdSense may place cookies for personalized ads – see Google’s privacy policy.

    **4. Data sharing**  
    We do not sell your personal data. We share only with essential service providers:  
    - Supabase (database for comments)  
    - Streamlit Cloud (hosting)  
    - ip-api.com (IP geolocation)  
    - Google AdSense (advertising, if enabled)

    **5. Your rights**  
    You can request deletion of your comments by emailing deslandes78@gmail.com with the comment ID.

    **6. Contact**  
    For any privacy questions, contact Gesner Deslandes at deslandes78@gmail.com.
    """)

with st.sidebar.expander("📜 Terms of Service"):
    st.markdown("""
    **Terms of Service for GlobalInternet.py**

    **1. Acceptance**  
    By using this website and purchasing software, you agree to these Terms.

    **2. Software purchases**  
    - All software is delivered as source code via email.  
    - You receive a non‑exclusive, perpetual license to use, modify, and deploy the software for your own business or personal use.  
    - You may not resell the source code as‑is without significant modification.  
    - Monthly subscriptions grant access to updates and support for the duration of the subscription.

    **3. Refunds**  
    Because software is delivered digitally, all sales are final. No refunds will be issued after the source code has been sent. However, we offer a live demo before purchase – test thoroughly.

    **4. Demo access**  
    Demos are provided “as is” and may be reset or changed without notice.

    **5. Limitation of liability**  
    We are not liable for any damages arising from the use of our software or website. You assume all responsibility for proper implementation and backup.

    **6. Governing law**  
    These terms are governed by the laws of Haiti.

    **7. Changes**  
    We may update these terms at any time. Continued use of the website constitutes acceptance.
    """)

with st.sidebar.expander("📜 Disclaimer"):
    st.markdown("""
    **Disclaimer for GlobalInternet.py**

    **General**  
    The information and software provided on this website are for general informational purposes only. While we strive to keep the information correct and the software free of bugs, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the software, products, services, or related graphics.

    **No professional advice**  
    The software solutions presented are tools; they do not constitute legal, financial, or medical advice. You should consult a qualified professional for your specific situation.

    **External links**  
    Our website may contain links to external sites (e.g., Sendwave, Western Union, live demos). We have no control over the content or practices of those sites and accept no responsibility for them.

    **“As is” and “as available”**  
    Your use of any software or information on this website is solely at your own risk. We will not be liable for any loss or damage arising from the use of this website or any software purchased from us.

    **Google AdSense**  
    Third‑party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Users may opt out of personalized advertising by visiting Google Ad Settings.

    **Contact**  
    If you have any questions, please contact us at deslandes78@gmail.com.
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

# ----------------------------------------------------------------------
# MAIN WEBSITE CONTENT (hero, about, avatar, cv, team, robotics, etc.)
# ----------------------------------------------------------------------
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

# Humanoid Robotics Video
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

# Projects in Perspective
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

# Services
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

# ---------- Projects listing with compact comment section ----------
st.markdown(f"## {t['projects_title']}")
st.markdown(f"*{t['projects_sub']}*")

# Helper to display comments recursively (simple threading)
def display_comment(comment, level=0, project_key=None):
    indent = " " * (level * 2)
    st.markdown(f"""
    <div class="comment-box" style="margin-left: {level*20}px;">
        <div class="comment-meta">
            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]} · 👍 {comment['likes']}
            <button class="like-button" data-id="{comment['id']}">❤️ Like</button>
        </div>
        <p style="margin: 0 0 0.2rem 0;">{comment['comment']}</p>
    </div>
    """, unsafe_allow_html=True)
    # Like button (requires rerun) – we use Streamlit button in expander, but inside markdown we can't. We'll use a small button below.
    col_like, col_reply = st.columns([1,4])
    with col_like:
        if st.button(f"❤️ {comment['likes']}", key=f"like_{comment['id']}"):
            add_like(comment['id'])
            st.rerun()
    # Reply form
    with st.expander("💬 Reply", expanded=False):
        with st.form(key=f"reply_form_{comment['id']}"):
            reply_name = st.text_input("Your name", key=f"reply_name_{comment['id']}", placeholder="Anonymous")
            reply_text = st.text_area("Reply", key=f"reply_text_{comment['id']}", height=68)
            if st.form_submit_button("Post Reply"):
                if reply_text.strip():
                    add_comment(project_key, reply_name, reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
                    st.rerun()
                else:
                    st.warning("Please enter a reply.")
    # Fetch replies (children)
    replies = [c for c in st.session_state.get(f"comments_{project_key}", []) if c.get("parent_id") == comment['id']]
    for reply in replies:
        display_comment(reply, level+1, project_key)

# Function to show comment section for a project
def show_comment_section(project_key):
    # Fetch comments for this project from Supabase and store in session state
    if f"comments_{project_key}" not in st.session_state:
        st.session_state[f"comments_{project_key}"] = get_comments(project_key)
    comments = st.session_state[f"comments_{project_key}"]
    comment_count = len([c for c in comments if c.get("parent_id") == 0])
    with st.expander(f"💬 Comments ({comment_count})", expanded=False):
        # Display all top-level comments
        top_comments = [c for c in comments if c.get("parent_id") == 0]
        for comment in top_comments:
            display_comment(comment, 0, project_key)
        # Add new comment form
        st.markdown("---")
        with st.form(key=f"new_comment_{project_key}"):
            username = st.text_input("Your name (optional)", key=f"username_{project_key}", placeholder="Anonymous")
            new_comment = st.text_area("Your comment", key=f"comment_{project_key}", height=100)
            if st.form_submit_button("Post Comment"):
                if new_comment.strip():
                    add_comment(project_key, username, new_comment)
                    # Clear cache
                    st.session_state[f"comments_{project_key}"] = get_comments(project_key)
                    st.rerun()
                else:
                    st.warning("Please write a comment.")

# ---------- Build project list (same as before, but now with comment sections) ----------
project_keys = [
    "haiti", "dashboard", "chatbot", "school", "pos", "scraper", "chess", "accountant",
    "archives", "dsm", "bi", "ai_classifier", "task_manager", "ray", "cassandra", "spark",
    "drone", "english", "spanish", "portuguese", "ai_career", "ai_medical", "music_studio",
    "ai_media", "chinese", "french", "mathematics", "ai_course", "medical_term", "python_course", "hardware_course",
    "medical_vocab_book2", "medical_term_book3", "toefl_course", "french_course", "haiti_marketplace", "vectra_ai",
    "humanoid_robot", "hospital", "arbitration", "programming_book", "employee_mgmt", "miroir",
    "wordpress", "building_systems"
]

projects = []
for key in project_keys:
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
    elif key == "hospital":
        demo_url = "https://hospital-management-system-software-built-by-gesner-deslandes.streamlit.app/"
    elif key == "arbitration":
        demo_url = "https://develop-your-arbitration-skills-with-gesner-sskvqnmurdk4cuwpr7.streamlit.app/"
    elif key == "programming_book":
        demo_url = "https://let-s-learn-basic-syntaxes-symbols-with-gesner-in-coding-bdupj.streamlit.app/"
    elif key == "employee_mgmt":
        demo_url = "https://employee-management-software-by-gesner-deslandes-nbg7cuewryjif.streamlit.app/"
    elif key == "miroir":
        demo_url = "https://miroir-revelation-entreprise-de-grand-groave-built-by-gesner-d.streamlit.app/"
    elif key == "wordpress":
        demo_url = "https://aczydtm6hucjpvgpdcqomp.streamlit.app/"
    elif key == "building_systems":
        demo_url = "https://building-systems-architect-dashboard-software-built-by-gesner.streamlit.app/"
    projects.append({
        "title": t.get(f"project_{key}", "Project"),
        "desc": t.get(f"project_{key}_desc", "Description not available"),
        "full_price": t.get(f"project_{key}_full_price", "Contact for price"),
        "status": t.get(f"project_{key}_status", "Status"),
        "key": key,
        "demo_url": demo_url
    })

group_a = [p for p in projects if p["demo_url"]]
group_b = [p for p in projects if not p["demo_url"]]

if group_a:
    st.markdown("### 🎯 Software with Live Demo")
    for i in range(0, len(group_a), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_a):
                proj = group_a[idx]
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{proj['title']}</h3>
                        <p>{proj['desc']}</p>
                        <div class="price">💎 Full package: {proj['full_price']}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{proj['status']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<a href='{proj['demo_url']}' target='_blank'><button style='background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; margin-bottom:0.5rem; width:100%; cursor:pointer;'>{t['live_demo']}</button></a>", unsafe_allow_html=True)
                    st.caption(t['demo_password_hint'])
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{proj['key']}"):
                        st.info(f"To subscribe for {proj['title']} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    subject = f"Purchase: {proj['title']}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {proj['title']} at {proj['full_price']}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)
                    # ADD COMPACT COMMENT SECTION
                    show_comment_section(proj['key'])

if group_b:
    st.markdown("### 🛠️ Software Available for Purchase (No Public Demo)")
    for i in range(0, len(group_b), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(group_b):
                proj = group_b[idx]
                with col:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{proj['title']}</h3>
                        <p>{proj['desc']}</p>
                        <div class="price">💎 Full package: {proj['full_price']}</div>
                        <div class="price">📅 Monthly subscription: $299 USD / month</div>
                        <p><em>{proj['status']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("📹 No public demo – contact us for a private walkthrough.")
                    if st.button(t['subscribe_monthly'], key=f"subscribe_{proj['key']}"):
                        st.info(f"To subscribe for {proj['title']} at $299/month, please contact us directly: 📞 (509)-47385663 or ✉️ deslandes78@gmail.com")
                    subject = f"Purchase: {proj['title']}"
                    body = f"Hello Gesner,%0D%0A%0D%0AI am interested in purchasing the full package of: {proj['title']} at {proj['full_price']}.%0D%0A%0D%0APlease send me payment instructions and the delivery details.%0D%0A%0D%0AThank you."
                    mailto_link = f"mailto:deslandes78@gmail.com?subject={subject}&body={body}"
                    st.markdown(f'<a href="{mailto_link}" target="_blank"><button style="background-color:#28a745; color:white; border:none; border-radius:30px; padding:0.5rem 1rem; width:100%; margin-top:0.5rem; cursor:pointer;">{t["buy_now"]}</button></a>', unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:0.8rem; margin-top:0.5rem;'>{t['contact_note']}</p>", unsafe_allow_html=True)
                    # ADD COMPACT COMMENT SECTION
                    show_comment_section(proj['key'])

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
        <video id="sendwaveVideo" src="{sendwave_video_url}" muted playsinline loop controls style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"></video>
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
        <video id="westernUnionVideo" src="{western_union_video_url}" muted playsinline loop controls style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"></video>
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
