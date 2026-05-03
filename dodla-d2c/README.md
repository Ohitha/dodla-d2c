# 🥛 Dodla Fresh — D2C Dairy App

A full-featured direct-to-consumer milk & dairy subscription web app for Dodla Dairy, built with Streamlit. Inspired by Provilac's industry-leading D2C experience.

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## Features

| Feature | Description |
|---|---|
| 🔐 OTP Login | Phone number + OTP authentication (demo OTP: `555555`) |
| 🏠 Dashboard | Today's delivery status, wallet balance, quick actions |
| 🛒 Shop | Full Dodla product catalog with category filters, subscribe instantly |
| 📋 Subscriptions | Manage plans — change qty, frequency, pause, cancel |
| 📅 Calendar | Monthly delivery view, pause individual days, vacation mode |
| 💳 Wallet | Balance, UPI recharge, transaction history, auto-deduct |
| 🍳 Recipes | 6 recipes using Dodla products with one-click subscribe |
| 👤 Profile | Loyalty coins (Dodla Coins), referral program, address management |

## Context Engineering

This project uses **old-school context engineering** — every decision is documented so any developer or AI agent can pick up the codebase cold:

- `CLAUDE.md` — Project bible: stack, file structure, session state keys, design rules
- `PRD.md` — Product requirements (what & why)
- `SPEC.md` — Technical specification (how)

## Local Development

```bash
git clone https://github.com/YOUR_USERNAME/dodla-d2c
cd dodla-d2c
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

**Demo login**: Any 10-digit number + OTP `555555`

## Deploy to Streamlit Cloud (Free)

1. Fork this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your fork → set `app.py` as the main file
4. Click **Deploy** — live in ~2 minutes!

## Project Structure

```
dodla-d2c/
├── CLAUDE.md          ← Context engineering: project bible
├── PRD.md             ← Product requirements
├── SPEC.md            ← Technical spec
├── app.py             ← Entry point + auth + router
├── requirements.txt
├── .streamlit/
│   └── config.toml    ← Dodla brand theme
├── pages/
│   ├── home.py
│   ├── shop.py
│   ├── subscriptions.py
│   ├── calendar_page.py
│   ├── wallet.py
│   ├── recipes.py
│   └── profile.py
└── data/
    ├── products.json
    └── recipes.json
```

## Inspired By

- [Provilac](https://provilac.com) — India's leading premium milk D2C app
- [ZEUX Innovation case study](https://www.zeuxinnovation.com/case-studies/redesigning-provilac-to-stand-out-among-milk-delivery-apps/) on redesigning Provilac

---

Built with ❤️ in Hyderabad for Dodla Dairy
