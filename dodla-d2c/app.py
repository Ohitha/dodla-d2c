import streamlit as st
import json
import os

# Always resolve paths relative to this file, not the working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Dodla Fresh",
    page_icon="🥛",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── Load data ──────────────────────────────────────────────
@st.cache_data
def load_products():
    with open(os.path.join(BASE_DIR, "data", "products.json")) as f:
        return json.load(f)

@st.cache_data
def load_recipes():
    with open(os.path.join(BASE_DIR, "data", "recipes.json")) as f:
        return json.load(f)

# ── Session State Init ─────────────────────────────────────
def init_state():
    defaults = {
        "logged_in": False,
        "otp_sent": False,
        "otp_phone": "",
        "user": {
            "name": "Ravi Kumar",
            "phone": "9876543210",
            "address": "Flat 4B, Prestige Towers, Banjara Hills, Hyderabad",
            "coins": 1240,
            "level": "Gold",
            "referral_code": "RAVI50",
        },
        "wallet_balance": 340.0,
        "subscriptions": [
            {"id": "sub_1", "product_id": "p1", "qty": 2, "frequency": "Daily", "active": True},
            {"id": "sub_2", "product_id": "p4", "qty": 1, "frequency": "Alternate days", "active": True},
        ],
        "paused_days": [27],
        "transactions": [
            {"date": "May 1", "type": "debit",  "icon": "📦", "desc": "Delivery", "detail": "Toned Milk ×2, Curd ×1", "amount": -74},
            {"date": "Apr 28","type": "credit", "icon": "💳", "desc": "Recharge via UPI", "detail": "", "amount": 500},
            {"date": "Apr 27","type": "debit",  "icon": "📦", "desc": "Delivery", "detail": "Toned Milk ×2", "amount": -52},
            {"date": "Apr 25","type": "credit", "icon": "🎁", "desc": "Referral bonus — Priya", "detail": "", "amount": 50},
            {"date": "Apr 24","type": "debit",  "icon": "📦", "desc": "Delivery", "detail": "Toned Milk ×2, Curd ×1", "amount": -74},
        ],
        "cart": [],
        "products": [],
        "recipes": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if not st.session_state.products:
        st.session_state.products = load_products()
    if not st.session_state.recipes:
        st.session_state.recipes = load_recipes()

init_state()

# ── CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { max-width: 700px !important; padding: 1rem 1.2rem 4rem !important; }
  .dodla-card {
    background: white; border-radius: 14px; border: 1px solid #e0e8f5;
    padding: 16px 18px; margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(26,74,140,0.07);
  }
  .blue-card {
    background: #1a4a8c; border-radius: 14px; padding: 18px 20px;
    margin-bottom: 14px; color: white;
  }
  .green-card {
    background: #2d8a4e; border-radius: 14px; padding: 18px 20px;
    margin-bottom: 14px; color: white; text-align: center;
  }
  .badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
  }
  .b-green  { background:#e8f5e9; color:#2d8a4e; }
  .b-blue   { background:#eef2f9; color:#1a4a8c; }
  .b-amber  { background:#fff8e1; color:#b8860b; }
  .b-red    { background:#fdecea; color:#c0392b; }
  .b-purple { background:#ede7f6; color:#6a1b9a; }
  .metric-box {
    background: #eef2f9; border-radius: 12px; padding: 16px;
    text-align: center; height: 100%;
  }
  .metric-box .val { font-size: 30px; font-weight: 800; color: #1a4a8c; }
  .metric-box .lbl { font-size: 12px; color: #666; margin-top: 2px; }
  .product-card {
    background: white; border-radius: 12px; border: 1.5px solid #e0e8f5;
    padding: 14px; margin-bottom: 8px; height: 100%;
  }
  .p-emoji { font-size: 34px; }
  .p-name  { font-size: 14px; font-weight: 700; margin-top: 6px; color: #1a1a2e; }
  .p-desc  { font-size: 12px; color: #777; margin-top: 3px; line-height: 1.4; }
  .p-price { font-size: 16px; font-weight: 800; color: #1a4a8c; margin-top: 8px; }
  .txn-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid #f0f4fb;
  }
  .txn-row:last-child { border-bottom: none; }
  .txn-amt-cr { color: #2d8a4e; font-weight: 700; }
  .txn-amt-db { color: #c0392b; font-weight: 700; }
  .cal-wrapper { overflow-x: auto; }
  table.cal { width: 100%; border-collapse: separate; border-spacing: 3px; }
  table.cal th { text-align:center; font-size:11px; color:#999; padding:4px 0; }
  table.cal td {
    width: 36px; height: 36px; text-align: center; vertical-align: middle;
    border-radius: 50%; font-size: 13px;
  }
  .cd { background:#1a4a8c; color:white; font-weight:700; border-radius:50%; }
  .cs { background:#eef2f9; color:#1a4a8c; font-weight:600; border-radius:50%; }
  .cp { background:#fff3e0; color:#e65100; border-radius:50%; }
  .ct { border: 2.5px solid #1a4a8c; color:#1a4a8c; font-weight:800; border-radius:50%; }
  .loyalty-bar { background:#e8edf5; border-radius:10px; height:10px; margin:8px 0; }
  .loyalty-fill { height:10px; border-radius:10px; background:#f5a623; }
  .low-bal {
    background:#fff3e0; border-left:4px solid #f5a623;
    padding:10px 14px; border-radius:8px; margin-bottom:14px;
    font-size:13px; color:#bf6a00;
  }
  .logo { font-size:24px; font-weight:900; color:#1a4a8c; letter-spacing:-1px; }
  .logo span { color:#f5a623; }
  .recipe-card {
    background:white; border-radius:12px; border:1.5px solid #e0e8f5;
    padding:14px; text-align:center; cursor:pointer;
  }
  .recipe-card .r-emoji { font-size:36px; }
  .recipe-card .r-name { font-size:13px; font-weight:700; margin-top:6px; }
  .recipe-card .r-time { font-size:11px; color:#999; margin-top:3px; }
  hr.dodla { border:none; border-top:1px solid #e8edf5; margin:16px 0; }
  div[data-testid="stSidebar"] { min-width:200px !important; max-width:230px !important; }
</style>
""", unsafe_allow_html=True)

# ── Auth Screen ────────────────────────────────────────────
def show_login():
    st.markdown('<div style="text-align:center;padding:2rem 0 1rem"><div class="logo">Dodla<span>.</span></div><p style="color:#666;font-size:14px">Fresh dairy, every morning 🥛</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="dodla-card">', unsafe_allow_html=True)
    st.markdown("### Welcome back")
    st.markdown("Enter your phone number to continue")

    phone = st.text_input("Mobile number", placeholder="9876543210", max_chars=10, label_visibility="collapsed")

    if not st.session_state.otp_sent:
        if st.button("Send OTP →", use_container_width=True, type="primary"):
            if len(phone) == 10 and phone.isdigit():
                st.session_state.otp_sent = True
                st.session_state.otp_phone = phone
                st.rerun()
            else:
                st.error("Enter a valid 10-digit mobile number")
    else:
        st.success(f"OTP sent to +91 {st.session_state.otp_phone} (use **555555**)")
        otp = st.text_input("Enter OTP", placeholder="555555", max_chars=6, label_visibility="collapsed")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verify & Login", use_container_width=True, type="primary"):
                if otp == "555555":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Wrong OTP. Use 555555")
        with col2:
            if st.button("Change number", use_container_width=True):
                st.session_state.otp_sent = False
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-size:12px;color:#aaa;margin-top:2rem">By continuing you agree to Dodla\'s Terms & Privacy Policy</p>', unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────
def show_sidebar():
    with st.sidebar:
        st.markdown('<div class="logo">Dodla<span>.</span></div>', unsafe_allow_html=True)
        u = st.session_state.user
        bal = st.session_state.wallet_balance

        level = u["level"]
        level_color = {"Gold": "#b8860b", "Platinum": "#6a1b9a", "Blue": "#1a4a8c"}.get(level, "#1a4a8c")
        st.markdown(f"""
        <div style="margin:12px 0 8px">
          <div style="font-weight:700;font-size:15px">{u['name']}</div>
          <div style="font-size:12px;color:#888">+91 {u['phone']}</div>
          <div style="margin-top:6px">
            <span style="background:#fff8e1;color:{level_color};padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700">
              {'⭐' if level=='Gold' else '🏆' if level=='Platinum' else '💙'} {level}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#eef2f9;border-radius:10px;padding:10px 12px;margin-bottom:16px">
          <div style="font-size:11px;color:#888">Wallet Balance</div>
          <div style="font-size:22px;font-weight:800;color:#2d8a4e">₹{bal:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Navigate**")
        pages = {
            "🏠 Home": "Home",
            "🛒 Shop": "Shop",
            "📋 Subscriptions": "Subscriptions",
            "📅 Calendar": "Calendar",
            "💳 Wallet": "Wallet",
            "🍳 Recipes": "Recipes",
            "👤 Profile": "Profile",
        }
        if "page" not in st.session_state:
            st.session_state.page = "Home"

        for label, page_name in pages.items():
            is_active = st.session_state.page == page_name
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, use_container_width=True, key=f"nav_{page_name}"):
                st.session_state.page = page_name
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Log out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.otp_sent = False
            st.rerun()

# ── Page Router ───────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    page = st.session_state.get("page", "Home")

    if page == "Home":
        from pages import home
        home.show()
    elif page == "Shop":
        from pages import shop
        shop.show()
    elif page == "Subscriptions":
        from pages import subscriptions
        subscriptions.show()
    elif page == "Calendar":
        from pages import calendar_page
        calendar_page.show()
    elif page == "Wallet":
        from pages import wallet
        wallet.show()
    elif page == "Recipes":
        from pages import recipes
        recipes.show()
    elif page == "Profile":
        from pages import profile
        profile.show()
