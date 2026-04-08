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
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card h3 {
        color: #1e3c72;
        margin-top: 0;
    }
    .price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff6b35;
        margin: 0.5rem 0;
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
# Projects / Accomplishments Section
# -----------------------------
st.markdown("## 🏆 Our Projects & Accomplishments")
st.markdown("*Completed software solutions delivered to clients – ready for you to purchase or customize.*")

# List of projects (title, description, price, status, contact)
projects = [
    {
        "title": "🇭🇹 Haiti Online Voting Software",
        "description": "Complete presidential election system with multi‑language support (Kreyòl, French, English, Spanish), real‑time live monitoring, CEP President dashboard (manage candidates, upload photos, download progress reports), secret ballot, and changeable passwords. Used for national elections.",
        "price": "$2,000 USD (one‑time fee)",
        "status": "✅ Available now – includes source code, setup, and support.",
        "contact": "Contact us for a live demo"
    },
    {
        "title": "📊 Business Intelligence Dashboard",
        "description": "Real‑time analytics dashboard for companies. Connect to any database (SQL, Excel, CSV) and visualize KPIs, sales trends, inventory, and custom reports. Fully interactive and customizable.",
        "price": "$1,200 USD",
        "status": "✅ Available now",
        "contact": "Demo available on request"
    },
    {
        "title": "🤖 AI Customer Support Chatbot",
        "description": "Intelligent chatbot trained on your business data. Answer customer questions 24/7, reduce support workload. Integrates with websites, WhatsApp, or Telegram. Built with Python and modern NLP.",
        "price": "$800 USD (basic) / $1,500 USD (advanced)",
        "status": "✅ Available now",
        "contact": "We can train on your specific content"
    },
    {
        "title": "🏫 School Management System",
        "description": "Complete platform for schools: student registration, grade management, attendance tracking, parent portal, report card generation, and fee collection. Multi‑user roles (admin, teachers, parents).",
        "price": "$1,500 USD",
        "status": "✅ Available now",
        "contact": "Includes training and deployment"
    },
    {
        "title": "📦 Inventory & POS System",
        "description": "Web‑based inventory management with point‑of‑sale for small businesses. Barcode scanning, stock alerts, sales reports, supplier management. Works online and offline.",
        "price": "$1,000 USD",
        "status": "✅ Available now",
        "contact": "Customizable for your business needs"
    },
    {
        "title": "📈 Custom Web Scraper & Data Pipeline",
        "description": "Automated data extraction from any website, cleaned and delivered as Excel/JSON/CSV. Schedule daily, weekly, or monthly runs. Perfect for market research, price monitoring, or lead generation.",
        "price": "$500 – $2,000 (depends on complexity)",
        "status": "✅ Available now",
        "contact": "Tell us your data source and we'll quote"
    }
]

# Display projects in rows of 2 or 3 columns
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
                    <p>{proj['description']}</p>
                    <div class="price">{proj['price']}</div>
                    <p><em>{proj['status']}</em></p>
                    <p>📞 {proj['contact']}</p>
                </div>
                """, unsafe_allow_html=True)
                # Optional button for each project (can lead to contact)
                if st.button(f"Request Info – {proj['title']}", key=f"btn_{idx}"):
                    st.info(f"Please email us at deslandes78@gmail.com or call (509)-47385663 to discuss '{proj['title']}'. Thank you!")

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
