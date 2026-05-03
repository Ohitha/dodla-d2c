import streamlit as st

def show():
    st.markdown("## 👤 Profile")
    u = st.session_state.user
    coins = u["coins"]

    # ── Avatar + info ─────────────────────────────────────
    initials = "".join(n[0] for n in u["name"].split()[:2]).upper()
    level = u["level"]
    level_badge = {"Gold": "⭐ Gold", "Platinum": "🏆 Platinum", "Blue": "💙 Blue"}.get(level, level)
    level_color = {"Gold": "b-amber", "Platinum": "b-purple", "Blue": "b-blue"}.get(level, "b-blue")

    st.markdown(f"""
    <div class="dodla-card">
      <div style="display:flex;align-items:center;gap:16px">
        <div style="width:60px;height:60px;border-radius:50%;background:#eef2f9;
             display:flex;align-items:center;justify-content:center;
             font-size:22px;font-weight:800;color:#1a4a8c">{initials}</div>
        <div>
          <div style="font-size:18px;font-weight:800">{u['name']}</div>
          <div style="font-size:13px;color:#888">+91 {u['phone']}</div>
          <div style="margin-top:6px"><span class="badge {level_color}">{level_badge}</span></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Edit profile ──────────────────────────────────────
    with st.expander("✏️ Edit profile"):
        new_name = st.text_input("Name", value=u["name"])
        new_addr = st.text_area("Delivery address", value=u["address"], height=80)
        if st.button("Save changes", type="primary"):
            st.session_state.user["name"] = new_name
            st.session_state.user["address"] = new_addr
            st.success("✅ Profile updated!")
            st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Loyalty coins ─────────────────────────────────────
    st.markdown("#### 🪙 Dodla Coins")

    # Progress to next level
    if coins >= 2500:
        pct = 100
        next_txt = "🏆 Maximum level reached!"
    elif coins >= 1000:
        pct = int((coins - 1000) / (2500 - 1000) * 100)
        next_txt = f"{2500 - coins} coins to Platinum"
    else:
        pct = int(coins / 1000 * 100)
        next_txt = f"{1000 - coins} coins to Gold"

    st.markdown(f"""
    <div class="dodla-card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:36px;font-weight:900;color:#f5a623">{coins:,}</div>
          <div style="font-size:13px;color:#888">Dodla Coins earned</div>
        </div>
        <div style="text-align:right">
          <div style="font-size:13px;color:#888">Redeem rate</div>
          <div style="font-size:18px;font-weight:700;color:#1a4a8c">100 coins = ₹10</div>
        </div>
      </div>
      <div class="loyalty-bar" style="margin-top:12px">
        <div class="loyalty-fill" style="width:{pct}%"></div>
      </div>
      <div style="font-size:12px;color:#888">{next_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        redeem_coins = st.number_input("Coins to redeem", min_value=100, max_value=coins,
                                        step=100, value=min(500, coins))
    with col2:
        st.markdown(f"<div style='padding-top:28px;font-weight:700;color:#2d8a4e'>= ₹{redeem_coins//10} wallet credit</div>", unsafe_allow_html=True)

    if st.button("🪙 Redeem coins", type="primary", use_container_width=True):
        credit = redeem_coins // 10
        st.session_state.user["coins"] -= redeem_coins
        st.session_state.wallet_balance += credit
        from datetime import date
        today = date.today().strftime("%b %d")
        st.session_state.transactions.insert(0, {
            "date": today, "type": "credit", "icon": "🪙",
            "desc": f"Coins redeemed ({redeem_coins} coins)", "detail": "", "amount": credit
        })
        st.success(f"✅ ₹{credit} added to your wallet!")
        st.rerun()

    st.markdown("""
    <div style="margin-top:10px;font-size:12px;color:#999;line-height:1.8">
      💡 Earn 1 coin for every ₹10 spent on deliveries<br>
      ⭐ Gold: 1,000 coins &nbsp;|&nbsp; 🏆 Platinum: 2,500 coins
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Referral ──────────────────────────────────────────
    st.markdown("#### 🎁 Refer & Earn")
    st.markdown(f"""
    <div class="blue-card">
      <div style="font-size:14px;opacity:0.8;margin-bottom:8px">YOUR REFERRAL CODE</div>
      <div style="font-size:32px;font-weight:900;letter-spacing:4px">{u['referral_code']}</div>
      <div style="font-size:13px;opacity:0.8;margin-top:10px">
        Share with friends — you both get <strong>₹50 wallet credit</strong> after their first delivery
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📤 Share referral code", use_container_width=True):
        st.success(f"Copied! Share this link: dodla.app/ref/{u['referral_code']}")

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Delivery address ──────────────────────────────────
    st.markdown("#### 📍 Delivery Address")
    st.markdown(f"""
    <div class="dodla-card">
      <div style="font-size:14px">{u['address']}</div>
      <div style="font-size:12px;color:#888;margin-top:6px">Primary address</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Settings menu ─────────────────────────────────────
    st.markdown("#### ⚙️ Settings")

    menu_items = [
        ("🔔", "Notification preferences", "Get alerts for delivery, payments & offers"),
        ("📄", "Invoices & billing", "Download monthly invoices"),
        ("❓", "Help & FAQ", "Common questions answered"),
        ("📞", "Contact support", "Call or chat with our team"),
    ]
    for icon, title, desc in menu_items:
        st.markdown(f"""
        <div class="dodla-card" style="cursor:pointer;display:flex;justify-content:space-between;align-items:center">
          <div>
            <div style="font-weight:600">{icon} {title}</div>
            <div style="font-size:12px;color:#888;margin-top:2px">{desc}</div>
          </div>
          <div style="color:#ccc;font-size:18px">›</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)
    if st.button("🚪 Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.otp_sent = False
        st.rerun()

    st.markdown("<p style='text-align:center;font-size:11px;color:#ccc;margin-top:16px'>Dodla Fresh v1.0 · Made with ❤️ in Hyderabad</p>", unsafe_allow_html=True)
