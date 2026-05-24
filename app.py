import streamlit as st
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import re
from supabase import create_client, Client

# ============================================================
# MITGO VERIFICATION META TAGS
# ============================================================
st.markdown("""
<head>
    <meta name="mitgo-verification" content="f264c89d-a0eb-47df-9591-9cd2d09e17d9" />
    <meta name="mitgo-verification" content="c807768c-7df7-4ebd-95a8-3737a906f92d" />
    <meta name="mitgo-verification" content="9030315c-9bfb-49af-940b-5526ce5dca6e" />
</head>
""", unsafe_allow_html=True)

# ============================================================
# GLOBAL SECURITY SHIELD
# ============================================================
import json
from typing import Any, Dict, Optional, Tuple

DEFAULT_PATTERNS = {
    "sql_injection": [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(union.*select)",
        r"(insert.*into)",
        r"(delete.*from)",
        r"(drop.*table)",
        r"(select.*from.*where)",
        r"(or\s+1\s*=\s*1)"
    ],
    "xss": [
        r"<script",
        r"javascript:",
        r"onload=",
        r"onerror=",
        r"onclick=",
        r"alert\(",
        r"prompt\("
    ],
    "path_traversal": [
        r"\.\./",
        r"\.\.\\",
        r"\.\.%2f"
    ],
    "command_injection": [
        r"(\|)|(\&)|(;)",
        r"(ping)|(nslookup)|(wget)"
    ],
    "malicious_user_agents": [
        r"sqlmap",
        r"nikto",
        r"nmap"
    ]
}

class SecurityException(Exception):
    pass

class WebAppShield:
    def __init__(self, app_name: str, api_key: str, dashboard_url: Optional[str] = None):
        self.app_name = app_name
        self.api_key = api_key
        self.dashboard_url = dashboard_url or "https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
        self.patterns = DEFAULT_PATTERNS.copy()
        self.custom_patterns = {}

    def add_custom_pattern(self, attack_type: str, pattern: str):
        if attack_type not in self.custom_patterns:
            self.custom_patterns[attack_type] = []
        self.custom_patterns[attack_type].append(pattern)

    def is_malicious(self, text: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(text, str):
            return False, None
        for attack_type, patterns in self.patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        for attack_type, patterns in self.custom_patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        return False, None

    def sanitize_input(self, value: Any) -> Any:
        if isinstance(value, str):
            malicious, attack_type = self.is_malicious(value)
            if malicious:
                raise SecurityException(f"Blocked: potential {attack_type} attack")
            return value
        elif isinstance(value, dict):
            return {k: self.sanitize_input(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.sanitize_input(i) for i in value]
        else:
            return value

    def log_threat(self, request_data: Dict):
        try:
            payload = {
                "app_name": self.app_name,
                "api_key": self.api_key,
                "timestamp": datetime.utcnow().isoformat(),
                "data": request_data
            }
            log_url = f"{self.dashboard_url}{json.dumps(payload)}"
            requests.get(log_url, timeout=2)
        except Exception:
            pass

    def protect_streamlit(self):
        if hasattr(st, 'query_params') and st.query_params:
            for key, value in st.query_params.items():
                try:
                    self.sanitize_input(value)
                except SecurityException as e:
                    st.error("🚨 Security alert: Malicious input detected and blocked.")
                    self.log_threat({
                        "type": "query_param",
                        "key": key,
                        "value": value,
                        "error": str(e)
                    })
                    st.stop()
        st.sidebar.markdown("🛡️ **Global Security Shield active**")

shield = WebAppShield(
    app_name="GlobalInternet.py Main Website",
    api_key="gl-MssTDLE9cATE4Iu7_tQkcxaFWcwwMr3e7S_Mdwgg",
    dashboard_url="https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
)
# ============================================================

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
        safe_comment = shield.sanitize_input(comment.strip())
        safe_username = shield.sanitize_input(username.strip() if username else "Anonymous")
    except SecurityException as e:
        st.error("Security alert: Your comment was blocked because it contains suspicious content.")
        shield.log_threat({
            "type": "comment_blocked",
            "project_key": project_key,
            "username": username,
            "comment": comment,
            "error": str(e)
        })
        return False

    try:
        supabase.table("comments").insert({
            "project_key": project_key,
            "username": safe_username,
            "comment": safe_comment,
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

shield.protect_streamlit()

# ============================================================
# BACKGROUND AND CSS (same as before, trimmed for brevity)
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f0ff 0%, #b8d9ff 100%) !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(200, 220, 250, 0.95) !important;
    }
    .hero, .card, .team-card, .future-project-card, .donation-box, .footer, .comment-box {
        background-color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stApp .main .block-container {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

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
    .big-globe {
        font-size: 120px;
        display: block;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: spin 8s linear infinite;
    }
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
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
    .stApp {
        margin: 0;
        padding: 0;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <head>
        <meta name="google-adsense-account" content="ca-pub-1238061430437782">
    </head>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DICTIONARIES (ONLY THE CHANGED PARTS FOR MAGNETIC CASE)
# ============================================================

lang_en = {
    # ... all previous content (keep as before) ...
    # For brevity, I'm showing only the magnetic case entry.
    # In your actual file, keep all previous entries exactly.
    "project_magnetic_case": "🛡️ Luxurious Magnetic Case for iPhone – Matte Translucent with Lens Protection",
    "project_magnetic_case_desc": "Premium matte translucent magnetic case with built-in lens protection. Compatible with MagSafe wireless chargers. Works with iPhone 17/16/15/14/13/12/11 Pro Max. ⭐ 4.7/5 – 17,158 reviews – 100k+ sold.\n\n**Price:** ~~HTG619.47~~ **HTG526.55** (-15%)\n*Prix hors taxe*\nHTG116.15 off over HTG1,355.09",
    "project_magnetic_case_full_price": "HTG526.55 ~~HTG619.47~~ (-15%)",
    "project_magnetic_case_status": "✅ In stock – Ships from AliExpress",
    "project_magnetic_case_aliexpress_link": "https://fr.aliexpress.com/item/1005007502032342.html?spm=oneshop.sub_buy_again.waterfall.1.2d1e7f6bBPweaX&skuId=12000041043858411&pdp_ext_f=%7B%22sku_id%22%3A%2212000041043858411%22%7D&aecmd=true&gatewayAdapt=glo2fra",
    # ... all other keys ...
}

# Similarly update French and Spanish versions
lang_fr = lang_en.copy()
lang_fr.update({
    "project_magnetic_case": "🛡️ Coque magnétique de luxe pour iPhone – Translucide mate avec protection d'objectif",
    "project_magnetic_case_desc": "Coque magnétique mate translucide haut de gamme avec protection intégrée de l'objectif. Compatible avec les chargeurs sans fil MagSafe. Fonctionne avec iPhone 17/16/15/14/13/12/11 Pro Max. ⭐ 4.7/5 – 17 158 avis – 100k+ vendus.\n\n**Prix :** ~~HTG619.47~~ **HTG526.55** (-15%)\n*Prix hors taxe*\nHTG116.15 d'économie pour tout achat de plus de HTG1,355.09",
    "project_magnetic_case_full_price": "HTG526.55 ~~HTG619.47~~ (-15%)",
})

lang_es = lang_en.copy()
lang_es.update({
    "project_magnetic_case": "🛡️ Funda magnética de lujo para iPhone – Translúcida mate con protección de lente",
    "project_magnetic_case_desc": "Funda magnética mate translúcida premium con protección de lente integrada. Compatible con cargadores inalámbricos MagSafe. Funciona con iPhone 17/16/15/14/13/12/11 Pro Max. ⭐ 4.7/5 – 17,158 reseñas – 100k+ vendidas.\n\n**Precio:** ~~HTG619.47~~ **HTG526.55** (-15%)\n*Precio sin impuestos*\nAhorra HTG116.15 al gastar más de HTG1,355.09",
    "project_magnetic_case_full_price": "HTG526.55 ~~HTG619.47~~ (-15%)",
})

# ============================================================
# REST OF THE APPLICATION (keep everything exactly as before)
# ============================================================
# ... (all the language selector, sidebar, hero, about, cv, team, services, projects loops, donations, footer, etc.) ...
# Make sure the st.image width is set to 'stretch' as fixed earlier.
