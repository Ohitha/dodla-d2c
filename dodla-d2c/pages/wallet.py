import streamlit as st

RECHARGE_AMOUNTS = [100, 200, 500, 1000]

def add_money(amount):
    st.session_state.wallet_balance += amount
    from datetime import date
    today = date.today().strftime("%b %d")
    st.session_state.transactions.insert(0, {
        "date": today, "type": "credit", "icon": "💳",
        "desc": f"Recharge via UPI", "detail": f"₹{amount}", "amount": amount
    })

def show():
    st.markdown("## 💳 Wallet")
    bal = st.session_state.wallet_balance

    # ── Balance banner ────────────────────────────────────
    products = {p["id"]: p for p in st.session_state.products}
    daily_cost = sum(
        products[s["product_id"]]["price"] * s["qty"]
        for s in st.session_state.subscriptions
        if s["active"] and s["product_id"] in products
    )
    days_left = int(bal / daily_cost) if daily_cost > 0 else "∞"

    st.markdown(f"""
    <div class="green-card">
      <div style="font-size:13px;opacity:0.8;margin-bottom:4px">AVAILABLE BALANCE</div>
      <div style="font-size:52px;font-weight:900;line-height:1">₹{bal:.0f}</div>
      <div style="font-size:14px;opacity:0.85;margin-top:6px">
        ≈ {days_left} days of deliveries remaining
      </div>
    </div>
    """, unsafe_allow_html=True)

    if bal < daily_cost * 3:
        st.warning("⚠️ Balance is low. Recharge to avoid delivery interruptions.")

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Quick recharge ────────────────────────────────────
    st.markdown("#### Recharge wallet")
    cols = st.columns(4)
    for i, amt in enumerate(RECHARGE_AMOUNTS):
        with cols[i]:
            if st.button(f"+ ₹{amt}", key=f"rch_{amt}", use_container_width=True):
                add_money(amt)
                st.success(f"✅ ₹{amt} added to your wallet!")
                st.rerun()

    # Custom amount
    st.markdown("<p style='font-size:13px;color:#888;margin-top:12px'>Or enter custom amount:</p>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        custom = st.number_input("Amount", min_value=50, max_value=10000, value=300,
                                  step=50, label_visibility="collapsed")
    with c2:
        if st.button("Pay", type="primary", use_container_width=True):
            add_money(custom)
            st.success(f"✅ ₹{custom} added!")
            st.rerun()

    st.markdown("""
    <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:#888">
        <span>📱</span> UPI
      </div>
      <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:#888">
        <span>💳</span> Debit / Credit Card
      </div>
      <div style="display:flex;align-items:center;gap:6px;font-size:13px;color:#888">
        <span>🏦</span> Net Banking
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Auto-deduct info ──────────────────────────────────
    st.markdown(f"""
    <div class="dodla-card">
      <div style="font-weight:700;margin-bottom:6px">💡 How the wallet works</div>
      <ul style="font-size:13px;color:#555;margin:0;padding-left:18px;line-height:2">
        <li>₹{daily_cost:.0f}/day is automatically deducted for your deliveries</li>
        <li>Recharge anytime — no minimum order</li>
        <li>Pause deliveries from the Calendar if you're travelling</li>
        <li>Refunds credited within 3 business days</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Transactions ──────────────────────────────────────
    st.markdown("#### Transaction history")
    txns = st.session_state.transactions

    if not txns:
        st.info("No transactions yet.")
        return

    for t in txns:
        is_credit = t["type"] == "credit"
        amt_html = f'<span class="txn-amt-cr">+₹{abs(t["amount"])}</span>' if is_credit else f'<span class="txn-amt-db">−₹{abs(t["amount"])}</span>'
        detail_html = f'<div style="font-size:11px;color:#aaa">{t.get("detail","")}</div>' if t.get("detail") else ""
        st.markdown(f"""
        <div class="txn-row">
          <div style="display:flex;align-items:center;gap:12px">
            <div style="width:36px;height:36px;border-radius:50%;
                 background:{'#e8f5e9' if is_credit else '#fdecea'};
                 display:flex;align-items:center;justify-content:center;font-size:16px">
              {t['icon']}
            </div>
            <div>
              <div style="font-weight:600;font-size:14px">{t['desc']}</div>
              <div style="font-size:12px;color:#999">{t['date']}</div>
              {detail_html}
            </div>
          </div>
          <div style="font-size:15px">{amt_html}</div>
        </div>
        """, unsafe_allow_html=True)
