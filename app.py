import streamlit as st
from PIL import Image
import base64
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="GlobalInternet.py – Python Software Company",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS for Professional Look
# -----------------------------
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    /* Cards */
    .card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card h3 {
        color: #1e3c72;
        margin-top: 0;
    }
    /* Button style */
    .stButton button {
        background-color: #ff6b35;
        color: white;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover {
        background-color: #e85d2a;
    }
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background-color: #1e3c72;
        color: white;
        border-radius: 20px;
        margin-top: 3rem;
    }
    /* Flag */
    .flag-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    /* Donation box */
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
# Header / Hero Section
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://flagcdn.com/w320/ht.png", width=100)
    st.markdown('<div class="flag-container"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>GlobalInternet.py</h1>
    <p>Build with Python. Deliver with Speed. Innovate with AI.</p>
    <p style="font-size:1rem;">From Haiti to the world – custom software that works online.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# About Section
# -----------------------------
st.markdown("## 👨‍💻 About the Company")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **GlobalInternet.py** was founded by **Gesner Deslandes** – owner, founder, and lead engineer.  
    We build **Python‑based software** on demand for clients worldwide. Like Silicon Valley, but with a Haitian touch and outstanding outcomes.
    
    - 🧠 **AI‑powered solutions** – chatbots, data analysis, automation  
    - 🗳️ **Complete election & voting systems** – secure, multi‑language, real‑time  
    - 🌐 **Web applications** – dashboards, internal tools, online platforms  
    - 📦 **Full package delivery** – we email you the complete code and guide you through installation
    
    Whether you need a company website, a custom software tool, or a full‑scale online platform – we build it, you own it.
    """)
with col2:
    st.markdown("""
    <div class="card">
        <h3>Founder & CEO</h3>
        <p><strong>Gesner Deslandes</strong></p>
        <p>Engineer | AI Enthusiast | Python Expert</p>
        <p>📞 (509)-47385663</p>
        <p>✉️ deslandes78@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Services We Offer
# -----------------------------
st.markdown("## ⚙️ Our Services")
services = [
    ("🐍 Custom Python Development", "Tailored scripts, automation, backend systems."),
    ("🤖 AI & Machine Learning", "Chatbots, predictive models, data insights."),
    ("🗳️ Election & Voting Software", "Secure, multi‑language, live results – like our Haiti system."),
    ("📊 Business Dashboards", "Real‑time analytics and reporting tools."),
    ("🌐 Website & Web Apps", "Full‑stack solutions deployed online."),
    ("📦 24‑Hour Delivery", "We work fast – get your software by email, ready to use.")
]
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
# Portfolio – Showcase Recent Work
# -----------------------------
st.markdown("## 🏆 Recent Project: Haiti Online Voting Software")
st.markdown("""
<div class="card">
    <h3>Haiti Presidential Election System</h3>
    <p>A complete, secure, multi‑language online voting platform built for the Haitian government / CEP.</p>
    <ul>
        <li>4 languages (Kreyòl, French, English, Spanish)</li>
        <li>Real‑time live monitoring for election officials</li>
        <li>CEP President dashboard – manage candidates, upload photos, download progress reports</li>
        <li>Secret ballot with anonymized votes</li>
        <li>Password‑protected access, changeable passwords via email verification</li>
    </ul>
    <p><strong>Price:</strong> $2,000 USD (one‑time fee, includes source code, setup, and support)</p>
    <p><em>Available for immediate deployment. Contact us for a live demo.</em></p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Donation Section – Support via Moncash (Prisme Transfer)
# -----------------------------
st.markdown("## 💖 Support GlobalInternet.py")
st.markdown("""
<div class="donation-box">
    <h3>Help us grow and continue building innovative software for Haiti and the world.</h3>
    <p>Your donation supports hosting, development tools, and free resources for local developers.</p>
    <br>
    <p><strong>🇭🇹 Easy & fast – Prisme transfer to Moncash (Digicel)</strong></p>
    <p style="font-size:1.5rem; font-weight:bold;">📱 (509)-47385663</p>
    <p><strong>Amount limit:</strong> Up to 100,000 HTG per transaction</p>
    <p><em>Just use the "Prisme transfer" feature in your Moncash app to send your contribution.</em></p>
    <br>
    <p><strong>🔜 Coming soon:</strong> Bank‑to‑bank transfers in USD and HTG (international and local).</p>
</div>
""", unsafe_allow_html=True)

# Simple button to show a thank you message
if st.button("💸 I've sent my donation – notify me"):
    st.success("Thank you so much! We will confirm receipt within 24 hours. Your support means the world to us! 🇭🇹")

# -----------------------------
# Contact & Call to Action
# -----------------------------
st.markdown("## 📞 Let’s Build Something Great")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; background-color: #e9ecef; padding: 2rem; border-radius: 20px;">
        <h3>Ready to start your project?</h3>
        <p>📞 <strong>Phone / WhatsApp:</strong> (509)-47385663</p>
        <p>✉️ <strong>Email:</strong> deslandes78@gmail.com</p>
        <p>We deliver full software packages by email – fast, reliable, and tailored to you.</p>
        <p><em>GlobalInternet.py – Your Python partner, from Haiti to the world.</em></p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(f"""
<div class="footer">
    <p>© {datetime.now().year} GlobalInternet.py – All rights reserved.</p>
    <p>Founded by Gesner Deslandes | Built with Streamlit | Hosted on GitHub + Streamlit Cloud</p>
    <p>🇭🇹 Proudly Haitian – serving the world with Python and AI 🇭🇹</p>
</div>
""", unsafe_allow_html=True)
