import streamlit as st

DODLA_BLUE = "#1a4a8c"
DODLA_LIGHT = "#eef2f9"
DODLA_ACCENT = "#f5a623"
DODLA_GREEN = "#2d8a4e"
DODLA_RED = "#c0392b"

GLOBAL_CSS = f"""
<style>
  /* ── Reset & Base ── */
  .block-container {{ max-width: 720px !important; padding: 1rem 1.2rem 3rem !important; }}
  h1, h2, h3 {{ color: {DODLA_BLUE}; }}
  a {{ color: {DODLA_BLUE}; }}

  /* ── Status Badges ── */
  .badge {{
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 600; margin: 2px 0;
  }}
  .badge-success {{ background: #e8f5e9; color: {DODLA_GREEN}; }}
  .badge-pending {{ background: #fff8e1; color: #f57c00; }}
  .badge-paused  {{ background: #fff3e0; color: #e65100; }}
  .badge-blue    {{ background: {DODLA_LIGHT}; color: {DODLA_BLUE}; }}
  .badge-gold    {{ background: #fff8e1; color: #b8860b; }}
  .badge-platinum {{ background: #ede7f6; color: #6a1b9a; }}

  /* ── Cards ── */
  .dodla-card {{
    background: white; border-radius: 14px;
    border: 1px solid #e8edf5; padding: 16px 18px;
    margin-bottom: 12px; box-shadow: 0 1px 4px rgba(26,74,140,0.06);
  }}
  .dodla-card-blue {{
    background: {DODLA_BLUE}; border-radius: 14px;
    padding: 16px 18px; margin-bottom: 12px; color: white;
  }}
  .dodla-card-green {{
    background: {DODLA_GREEN}; border-radius: 14px;
    padding: 16px 18px; margin-bottom: 12px; color: white; text-align: center;
  }}

  /* ── Metric Tiles ── */
  .metric-tile {{
    background: {DODLA_LIGHT}; border-radius: 12px;
    padding: 14px; text-align: center;
  }}
  .metric-tile .value {{ font-size: 28px; font-weight: 700; color: {DODLA_BLUE}; }}
  .metric-tile .label {{ font-size: 12px; color: #666; margin-top: 2px; }}

  /* ── Product Cards ── */
  .product-card {{
    background: white; border-radius: 12px;
    border: 1.5px solid #e8edf5; padding: 14px;
    height: 100%; transition: border-color 0.2s;
  }}
  .product-card:hover {{ border-color: {DODLA_BLUE}; }}
  .product-card .p-emoji {{ font-size: 32px; }}
  .product-card .p-name {{ font-size: 14px; font-weight: 600; margin-top: 6px; color: #1a1a2e; }}
  .product-card .p-desc {{ font-size: 12px; color: #666; margin-top: 3px; line-height: 1.4; }}
  .product-card .p-price {{ font-size: 16px; font-weight: 700; color: {DODLA_BLUE}; margin-top: 8px; }}

  /* ── Calendar ── */
  .cal-table {{ width: 100%; border-collapse: separate; border-spacing: 3px; }}
  .cal-table th {{ text-align: center; font-size: 11px; color: #888; padding: 4px 0; }}
  .cal-day {{
    width: 36px; height: 36px; text-align: center; vertical-align: middle;
    border-radius: 50%; font-size: 13px; cursor: pointer;
  }}
  .cal-delivered {{ background: {DODLA_BLUE}; color: white; font-weight: 600; }}
  .cal-scheduled {{ background: {DODLA_LIGHT}; color: {DODLA_BLUE}; font-weight: 500; }}
  .cal-paused    {{ background: #fff3e0; color: #e65100; }}
  .cal-today     {{ border: 2.5px solid {DODLA_BLUE}; color: {DODLA_BLUE}; font-weight: 700; }}
  .cal-empty     {{ background: transparent; }}

  /* ── Transaction rows ── */
  .txn-credit {{ color: {DODLA_GREEN}; font-weight: 600; }}
  .txn-debit  {{ color: {DODLA_RED}; font-weight: 600; }}

  /* ── Wallet Banner ── */
  .wallet-big {{ font-size: 48px; font-weight: 800; color: white; line-height: 1; }}
  .wallet-sub {{ font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 4px; }}

  /* ── Section Divider ── */
  .sec-header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 10px;
  }}
  .sec-header h4 {{ margin: 0; color: {DODLA_BLUE}; font-size: 15px; }}
  .sec-link {{ font-size: 13px; color: {DODLA_BLUE}; cursor: pointer; }}

  /* ── Input overrides ── */
  .stNumberInput > div {{ max-width: 120px !important; }}
  div[data-testid="stNumberInput"] {{ width: 120px; }}

  /* ── Warning Banner ── */
  .low-balance-banner {{
    background: #fff3e0; border-left: 4px solid {DODLA_ACCENT};
    padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;
    font-size: 13px; color: #bf6a00;
  }}

  /* ── Loyalty Progress Bar ── */
  .loyalty-bar-bg {{
    background: #e8edf5; border-radius: 10px; height: 10px; margin: 8px 0;
  }}
  .loyalty-bar-fill {{
    height: 10px; border-radius: 10px; background: {DODLA_ACCENT};
  }}

  /* ── Sidebar Logo ── */
  .sidebar-logo {{
    font-size: 26px; font-weight: 800; color: {DODLA_BLUE};
    letter-spacing: -1px; margin-bottom: 4px;
  }}
  .sidebar-logo span {{ color: {DODLA_ACCENT}; }}

  /* Streamlit sidebar override */
  section[data-testid="stSidebar"] {{ min-width: 200px !important; max-width: 240px !important; }}

  /* Hide default Streamlit nav page titles decoration */
  [data-testid="stSidebarNav"] li span {{ font-size: 14px; }}
</style>
"""

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def card(content_html, style=""):
    st.markdown(f'<div class="dodla-card" style="{style}">{content_html}</div>', unsafe_allow_html=True)

def blue_card(content_html):
    st.markdown(f'<div class="dodla-card-blue">{content_html}</div>', unsafe_allow_html=True)

def green_card(content_html):
    st.markdown(f'<div class="dodla-card-green">{content_html}</div>', unsafe_allow_html=True)

def badge(text, color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def metric_tile(value, label):
    return f"""
    <div class="metric-tile">
      <div class="value">{value}</div>
      <div class="label">{label}</div>
    </div>"""

def product_card_html(p):
    oos = "" if p["in_stock"] else f'<br><small style="color:#e65100">Expected restock: {p.get("restock","Soon")}</small>'
    return f"""
    <div class="product-card">
      <div class="p-emoji">{p['emoji']}</div>
      <div class="p-name">{p['name']}</div>
      <div class="p-desc">{p['desc']}</div>
      <div class="p-price">₹{p['price']}</div>
      {oos}
    </div>"""

def low_balance_warning(balance, daily_cost):
    days = int(balance / daily_cost) if daily_cost > 0 else 99
    if days < 3:
        st.markdown(f"""
        <div class="low-balance-warning">
          ⚠️ <strong>Low wallet balance!</strong> You have ≈{days} day(s) of deliveries left.
          <a href="/wallet" style="color:#bf6a00;font-weight:600"> Recharge now →</a>
        </div>""", unsafe_allow_html=True)

def loyalty_level_badge(coins):
    if coins >= 2500:
        return badge("🏆 Platinum", "platinum")
    elif coins >= 1000:
        return badge("⭐ Gold", "gold")
    else:
        return badge("💙 Blue", "blue")

def loyalty_progress_html(coins):
    if coins >= 2500:
        pct = 100
        next_level = "Platinum — Max level!"
    elif coins >= 1000:
        pct = int((coins - 1000) / (2500 - 1000) * 100)
        next_level = f"{2500 - coins} coins to Platinum"
    else:
        pct = int(coins / 1000 * 100)
        next_level = f"{1000 - coins} coins to Gold"
    return f"""
    <div class="loyalty-bar-bg">
      <div class="loyalty-bar-fill" style="width:{pct}%"></div>
    </div>
    <small style="color:#888">{next_level}</small>"""
