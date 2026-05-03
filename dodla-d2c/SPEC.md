# SPEC.md — Dodla D2C App: Technical Specification

## Session State Initialization (app.py must do this on every load)

```python
DEFAULTS = {
    "logged_in": False,
    "user": {
        "name": "Ravi Kumar",
        "phone": "9876543210",
        "address": "Flat 4B, Prestige Towers, Banjara Hills, Hyderabad",
        "coins": 1240,
        "level": "Gold",  # Blue | Gold | Platinum
        "referral_code": "RAVI50",
    },
    "wallet_balance": 340.0,
    "subscriptions": [
        {"id": "sub_1", "product_id": "p1", "qty": 2, "frequency": "daily", "active": True},
        {"id": "sub_2", "product_id": "p4", "qty": 1, "frequency": "alternate", "active": True},
    ],
    "paused_days": [27],  # day numbers this month that are paused
    "transactions": [
        {"date": "2025-04-30", "type": "debit", "desc": "Delivery", "amount": -74, "items": "Toned Milk ×2, Curd ×1"},
        {"date": "2025-04-28", "type": "credit", "desc": "Recharge via UPI", "amount": 500},
        {"date": "2025-04-27", "type": "debit", "desc": "Delivery", "amount": -52, "items": "Toned Milk ×2"},
        {"date": "2025-04-25", "type": "credit", "desc": "Referral bonus — Priya", "amount": 50},
        {"date": "2025-04-24", "type": "debit", "desc": "Delivery", "amount": -74},
    ],
    "cart": [],
    "otp_sent": False,
    "otp_phone": "",
}
```

## Data Files

### data/products.json
```json
[
  {"id":"p1","name":"Toned Milk 500ml","category":"Milk","price":26,"emoji":"🥛","desc":"Pasteurized, homogenized. 3% fat.","in_stock":true},
  {"id":"p2","name":"Full Cream Milk 500ml","category":"Milk","price":30,"emoji":"🥛","desc":"Rich, creamy. 6% fat.","in_stock":true},
  {"id":"p3","name":"Long Life UHT Milk 1L","category":"Milk","price":68,"emoji":"🍶","desc":"90-day shelf life. No refrigeration needed.","in_stock":true},
  {"id":"p4","name":"Curd 200g","category":"Curd & Buttermilk","price":22,"emoji":"🫙","desc":"Fresh set curd, creamy texture.","in_stock":true},
  {"id":"p5","name":"Spiced Buttermilk 200ml","category":"Curd & Buttermilk","price":12,"emoji":"🥤","desc":"Tempered with cumin & ginger.","in_stock":true},
  {"id":"p6","name":"Lassi 200ml","category":"Curd & Buttermilk","price":28,"emoji":"🥛","desc":"Sweet mango or plain.","in_stock":true},
  {"id":"p7","name":"Pure Ghee 200ml","category":"Ghee & Butter","price":185,"emoji":"🫙","desc":"A2 cow ghee, slow churned.","in_stock":true},
  {"id":"p8","name":"Butter 100g","category":"Ghee & Butter","price":55,"emoji":"🧈","desc":"Fresh churned, lightly salted.","in_stock":false,"restock":"May 10"},
  {"id":"p9","name":"Doodh Peda 6pc","category":"Sweets","price":85,"emoji":"🍮","desc":"Traditional milk sweets.","in_stock":true},
  {"id":"p10","name":"Chocolate Flavoured Milk 200ml","category":"Sweets","price":30,"emoji":"🍫","desc":"Kids favourite. No artificial colours.","in_stock":true},
  {"id":"p11","name":"Paneer 200g","category":"Paneer","price":95,"emoji":"🧀","desc":"Soft, fresh. Doubles in dishes.","in_stock":true},
  {"id":"p12","name":"Ice Cream Vanilla 500ml","category":"Sweets","price":120,"emoji":"🍦","desc":"Creamy, real milk base.","in_stock":true}
]
```

### data/recipes.json (6 recipes)
Each recipe: id, name, time_mins, emoji, ingredients (list), steps (list), dodla_products (list of product ids used)

## Page Specs

### app.py (entry point)
- Init all session_state keys if not present
- Show auth gate if not logged_in
- Else show main app with st.sidebar navigation
- Sidebar: Dodla logo, user name, wallet balance, nav links

### pages/01_home.py
- Header: greeting + date
- Delivery status card: today's items, status (Delivered/Scheduled/Paused), time
- 2-column stats: "This month: X deliveries" | "Wallet: ₹X"
- Subscriptions quick view (2 items max, "Manage all →" link)
- Qty +/- controls on each subscription inline
- "New arrivals" horizontal scroll (3 products)
- Low balance warning banner if wallet < 100

### pages/02_shop.py
- Category filter chips (All, Milk, Curd & Buttermilk, Ghee & Butter, Sweets, Paneer)
- Product grid: 2 columns
- Each product card: emoji, name, desc, price, "Subscribe" or "Out of Stock" button
- On Subscribe → add to session_state.subscriptions, show success toast
- Out of stock → disabled button, show restock date

### pages/03_subscriptions.py
- List all active subscriptions
- Each: product name, frequency badge, qty +/-, pause toggle, cancel button
- "Add more products →" link to shop
- Total daily spend calculation at bottom

### pages/04_calendar.py
- Month title (current month)
- Calendar grid using HTML/CSS via st.markdown (7 columns)
- Color coding: Delivered (blue), Scheduled (light blue), Paused (amber), Today (bold)
- Tap day → toggle pause (future days only)
- Delivery instructions select + text input
- "Confirm changes" button

### pages/05_wallet.py
- Big balance display (green)
- "~X days of deliveries" sub-label
- Recharge buttons: ₹100, ₹200, ₹500, ₹1000 + custom amount input
- "Pay via UPI" simulated button → adds to balance + adds credit transaction
- Transaction list: icon, desc, date, amount (red debit / green credit)

### pages/06_profile.py
- Avatar circle with initials
- Name, phone, address
- Loyalty coins card: coin count, level badge, progress bar to next level, Redeem button
- Referral card: code display, copy button, "₹50 for you and your friend"
- Menu items: Manage Addresses, Notification Settings, Help & FAQ, Log Out

### pages/07_recipes.py
- Grid of recipe cards (2 cols): emoji, name, time
- Click recipe → expander with full ingredients + steps + "Products used" tags

## Styling Approach
Use `st.markdown` with inline CSS for:
- Colored metric cards (blue/green/amber)
- Status badges (pill shapes)
- Calendar grid (HTML table in markdown)
- Horizontal product scroll

Use `st.columns` for all grid layouts.
Use `st.expander` for recipes and transaction details.
Use `st.success/warning/error` for system messages.

## Deployment
- `requirements.txt`: streamlit, pandas, Pillow (if needed)
- `.streamlit/config.toml`: set primaryColor, font
- `README.md`: one-click deploy badge for Streamlit Cloud
