import streamlit as st
from datetime import date

def show():
    today = date.today()
    u = st.session_state.user
    bal = st.session_state.wallet_balance
    subs = st.session_state.subscriptions
    products = {p["id"]: p for p in st.session_state.products}

    # ── Greeting ───────────────────────────────────────────
    hour = __import__("datetime").datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
    st.markdown(f"## {greeting}, {u['name'].split()[0]}! 👋")
    st.markdown(f"<p style='color:#888;font-size:13px;margin-top:-12px'>{today.strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

    # ── Low balance warning ───────────────────────────────
    daily_cost = sum(
        products[s["product_id"]]["price"] * s["qty"]
        for s in subs if s["active"] and s["product_id"] in products
    )
    if bal < daily_cost * 3:
        st.markdown(f"""
        <div class="low-bal">
          ⚠️ <strong>Low wallet balance</strong> — only {int(bal/daily_cost) if daily_cost else '?'} days of deliveries left.
          Tap Wallet to recharge.
        </div>""", unsafe_allow_html=True)

    # ── Today's delivery card ─────────────────────────────
    sub_lines = []
    for s in subs:
        if s["active"] and s["product_id"] in products:
            p = products[s["product_id"]]
            sub_lines.append(f"{p['name']} × {s['qty']}")
    delivery_text = " &nbsp;·&nbsp; ".join(sub_lines) if sub_lines else "No active subscriptions"

    st.markdown(f"""
    <div class="blue-card">
      <div style="font-size:12px;opacity:0.7;margin-bottom:4px">TODAY'S DELIVERY</div>
      <div style="font-size:18px;font-weight:700">{delivery_text}</div>
      <div style="font-size:13px;opacity:0.8;margin-top:4px">Delivered by 6:30 AM  ·  Banjara Hills</div>
      <div style="margin-top:10px">
        <span class="badge b-green">✓ Delivered</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
          <div class="val">24</div>
          <div class="lbl">Deliveries this month</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
          <div class="val" style="color:#2d8a4e">₹{bal:.0f}</div>
          <div class="lbl">Wallet balance</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
          <div class="val" style="color:#f5a623">{u['coins']}</div>
          <div class="lbl">Dodla coins</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Active subscriptions quick view ───────────────────
    st.markdown("#### 📋 My Subscriptions")
    for i, s in enumerate(subs):
        if not s["active"] or s["product_id"] not in products:
            continue
        p = products[s["product_id"]]
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"""
            <div style="padding:6px 0">
              <div style="font-weight:700;font-size:14px">{p['emoji']} {p['name']}</div>
              <div style="font-size:12px;color:#888">{s['frequency']} · ₹{p['price']}/unit</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            new_qty = st.number_input("qty", min_value=0, max_value=10, value=s["qty"],
                                      key=f"home_qty_{i}", label_visibility="collapsed")
            if new_qty != s["qty"]:
                st.session_state.subscriptions[i]["qty"] = new_qty
                st.rerun()
        with col3:
            st.markdown(f"<div style='text-align:right;padding-top:10px;font-weight:700;color:#1a4a8c'>₹{p['price']*s['qty']}/day</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📋 Manage all subscriptions", use_container_width=True):
            st.session_state.page = "Subscriptions"
            st.rerun()
    with col_b:
        if st.button("🛒 Add more products", use_container_width=True):
            st.session_state.page = "Shop"
            st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Quick actions ─────────────────────────────────────
    st.markdown("#### ⚡ Quick actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📅 Pause\ndelivery", use_container_width=True):
            st.session_state.page = "Calendar"
            st.rerun()
    with c2:
        if st.button("💳 Add\nmoney", use_container_width=True):
            st.session_state.page = "Wallet"
            st.rerun()
    with c3:
        if st.button("🍳 Browse\nrecipes", use_container_width=True):
            st.session_state.page = "Recipes"
            st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── New arrivals ──────────────────────────────────────
    st.markdown("#### 🆕 New arrivals")
    new_products = [p for p in st.session_state.products if p["id"] in ["p9", "p12", "p6"]]
    cols = st.columns(3)
    for i, p in enumerate(new_products):
        with cols[i]:
            st.markdown(f"""
            <div class="product-card" style="text-align:center">
              <div class="p-emoji">{p['emoji']}</div>
              <div class="p-name">{p['name']}</div>
              <div class="p-price">₹{p['price']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("View", key=f"new_{p['id']}", use_container_width=True):
                st.session_state.page = "Shop"
                st.rerun()
