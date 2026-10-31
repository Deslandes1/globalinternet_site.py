# 🌐 GlobalInternet.py — Python Software Company Website

> **Build with Python. Deliver with Speed. Innovate with AI.**  
> From Haiti to the world — custom software that works online.

A full-featured, multi-language Streamlit website showcasing 50+ Python-based software products, with live demos, threaded comments, AI voice narration, visitor analytics, and built-in security.

**Live Site:** [globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)

---

## ✨ Features

### 🌍 Multi-Language Interface
- Complete UI translations in **English**, **French**, and **Spanish**.
- Independent **voice narrator** language selector — English, French, Spanish, and Chinese.
- Language preference persists across the session.

### 🎙️ AI Voice Overview
- Powered by Google **gTTS** — a full spoken company overview.
- Pre-translated scripts in 4 languages.
- Graceful fallback when gTTS is unavailable.

### 🖼️ Portfolio — 50+ Software Projects
Every project card includes:
- Title, description, full package price, and monthly subscription rate.
- Live demo link with password hint.
- **Subscribe Monthly** and **Buy Now** buttons (mailto-based — no payment gateway required).
- Per-project **comment section** with replies, threading, and likes.

**Categories covered:**
- 🗳️ **Government** — Haiti Online Voting System, Haiti Archives Nationales Database
- 💼 **Business** — Business Intelligence, Employee Management, POS/Inventory, Accountant Excel AI, WordPress Suite, Building Systems Architect
- 🤖 **AI & ML** — Customer Support Chatbot, AI Image Classifier, AI Career Coach, AI Medical Assistant, Let's Learn AI
- 📚 **Education** — English, Spanish, Portuguese, French, Chinese, Mathematics, Python, AI Foundations, TOEFL, Medical Terminology (Books 1–3), Arbitration Skills
- ⚡ **Tech Demos** — Apache Spark, Ray Parallel Processing, Cassandra Dashboard, Kubernetes Dashboard
- 🚁 **Robotics & Simulation** — Haitian Drone Commander, Humanoid Robot Suite, Vectra AI Simulator, Haiti Radar 2 Tracker, DSM-2026
- 🎧 **Creative** — Music Studio Pro, AI Media Studio
- 🏥 **Healthcare** — Hospital Management System
- 📱 **Retail** — Luxurious Magnetic iPhone Case

### 💬 Threaded Comment System (Supabase)
- Per-project comments stored in Supabase.
- Nested replies, likes (`increment_likes` RPC), and password-protected admin deletion.
- Session-cached loading for performance.

### 🛡️ Global Security Shield
A custom `WebAppShield` class that:
- Detects **SQL injection**, **XSS**, **path traversal**, **command injection**, and **malicious user agents** (sqlmap, nikto, nmap).
- Sanitizes `st.query_params` on every page load.
- Logs threats to an external monitoring dashboard.
- Immediately blocks malicious requests with `st.stop()`.

### 📧 Visitor Notification System
- Captures real IP (via `X-Forwarded-For` or `ipify.org` fallback).
- Geolocates visitors via `ip-api.com` — country, region, city, ISP.
- Emails the site owner for every new session using **Gmail SMTP SSL**.
- Runs once per session via `st.session_state`.

### 📢 Money Transfer Promotions
- **Sendwave** — full promo section with auto-playing muted ad.
- **Western Union** — parallel promo section with its own video.

### 💖 Donation Box
Accept donations via:
- **Prisme Transfer** → Moncash (Digicel) — Haiti
- **SendWave** — international
- **UNIBANK US** — bank transfer (Account: `105-2016-16594727`)

### 📱 Social Media Sidebar
- LinkedIn, Facebook, TikTok, YouTube — with hover effects.

### 📜 Legal Pages
- Privacy Policy
- Terms of Service
- Disclaimer

### 🎨 Clean UI
- Light-blue gradient background with white cards.
- Hover animations and responsive grid layout.
- Smooth section flow: Hero → About → Owner CV → Team → Robotics → Future Projects → Services → Portfolio → Promotions → Donation → Contact → Footer.

### 🔍 SEO & Verification
- **Mitgo verification** meta tags × 3
- **Google AdSense** account meta tag (`ca-pub-1238061430437782`)

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Streamlit |
| Language | Python 3.9+ |
| Database | Supabase (Postgres via REST) |
| Authentication | Session-state based |
| Voice | gTTS |
| Email | smtplib — Gmail SMTP SSL |
| Geolocation | ip-api.com, ipify.org |
| Security | Custom `WebAppShield` (regex + threat logging) |
| Hosting | Streamlit Cloud + GitHub |
| Assets | GitHub raw links, flagcdn.com |

---

## 📂 Repository Structure
