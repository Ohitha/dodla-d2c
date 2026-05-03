# CLAUDE.md — Dodla D2C App
> This file is the single source of truth for any AI agent or developer working on this repo.
> Read this fully before touching any file.

## Project Identity
- **Product**: Dodla Dairy Direct-to-Consumer Web App
- **Inspired by**: Provilac (provilac.com) — India's leading premium milk D2C app
- **Brand**: Dodla Dairy (Hyderabad) — large-scale dairy brand entering D2C
- **Goal**: Subscription-first dairy delivery with wallet, calendar, loyalty & shop

## Stack
| Layer | Technology |
|---|---|
| Frontend/App | Streamlit (Python) |
| State | `st.session_state` (dict-based, keys defined in SPEC.md) |
| Data | JSON files in `/data/` (seed data, no DB for MVP) |
| Auth | Fake OTP login (mock, no real SMS) |
| Payments | Simulated (Razorpay UI mockup, no real calls) |
| Deploy | Streamlit Community Cloud |
| Repo | GitHub |

## File Structure
```
dodla-d2c/
├── CLAUDE.md              ← YOU ARE HERE — read first always
├── PRD.md                 ← Product requirements (what & why)
├── SPEC.md                ← Technical spec (how)
├── app.py                 ← Entry point, router, session init
├── requirements.txt
├── .streamlit/
│   └── config.toml        ← Theme = Dodla blue (#1a4a8c)
├── pages/
│   ├── 01_home.py         ← Dashboard + today's delivery status
│   ├── 02_shop.py         ← Product catalog + add to subscription
│   ├── 03_subscriptions.py← Manage active subscriptions, qty, pause
│   ├── 04_calendar.py     ← Monthly delivery calendar, pause days
│   ├── 05_wallet.py       ← Balance, recharge, transactions
│   ├── 06_profile.py      ← User info, loyalty coins, referral, addresses
│   └── 07_recipes.py      ← Recipes using Dodla products (Provilac feature)
├── components/
│   ├── nav.py             ← Shared top nav bar component
│   ├── cards.py           ← Reusable card UI helpers
│   └── auth.py            ← Login/OTP gate component
├── data/
│   ├── products.json      ← All Dodla SKUs with price, category, image_emoji
│   ├── user.json          ← Mock user profile + wallet + loyalty
│   ├── deliveries.json    ← This month's delivery log (date, status, items)
│   └── recipes.json       ← 6 recipes using Dodla products
└── context/
    ├── PRD.md             ← copy
    └── SPEC.md            ← copy
```

## Session State Keys (never rename these)
| Key | Type | Description |
|---|---|---|
| `logged_in` | bool | Is user authenticated |
| `user` | dict | User profile (name, phone, address, coins, level) |
| `wallet_balance` | float | Current wallet balance in ₹ |
| `subscriptions` | list[dict] | Active product subscriptions |
| `deliveries` | list[dict] | This month's delivery log |
| `cart` | list[dict] | Items added in shop not yet subscribed |
| `paused_days` | list[int] | Day numbers paused this month |
| `transactions` | list[dict] | Wallet transaction history |

## Design Rules (mirroring Provilac premium feel)
1. **Primary color**: `#1a4a8c` (Dodla blue) — use for headers, CTAs, active states
2. **Accent**: `#f5a623` (warm amber) — use for loyalty coins, highlights
3. **Success green**: `#2d8a4e` — wallet balance, delivered status
4. **Font**: Streamlit default (clean, sans-serif)
5. **Mobile-first** layout: max content width ~700px, use `st.columns([1,2,1])` for centering
6. **Every page** must have: page title with emoji, clear CTA, no dead ends
7. **Provilac-parity features**: calendar pause, wallet system, pro coins loyalty, recipes section, referral

## Business Logic Rules
- Delivery cutoff: changes must be made before midnight for next-day effect
- Wallet auto-deducts on delivery; show "low balance" warning if < 3 days of deliveries
- Loyalty coins: 1 coin per ₹10 spent; Blue (0-999), Gold (1000-2499), Platinum (2500+)
- Referral: ₹50 credit for both referrer and referee on first delivery
- Pause: up to 30 days per year; show count remaining
- Out of stock: show badge, disable "Subscribe" button, show expected restock date

## DO NOT
- Do not use database connections — use JSON files in /data/
- Do not use real payment APIs — simulate with session_state
- Do not break the session_state key names defined above
- Do not use `st.experimental_rerun` — use `st.rerun()`
- Do not add pages without updating this CLAUDE.md

## Agent Workflow
1. Read CLAUDE.md (this file) completely
2. Read PRD.md to understand what the user wants
3. Read SPEC.md for exact implementation details
4. Check existing code before writing new code
5. Test by running `streamlit run app.py` mentally against the spec
6. Commit with meaningful messages: `feat(wallet): add recharge flow`

