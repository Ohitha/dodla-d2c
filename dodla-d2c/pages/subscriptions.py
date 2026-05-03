import streamlit as st

FREQUENCIES = ["Daily", "Alternate days", "Weekdays only", "Weekends only"]

def show():
    st.markdown("## 📋 My Subscriptions")
    products = {p["id"]: p for p in st.session_state.products}
    subs = st.session_state.subscriptions

    active = [s for s in subs if s["active"]]
    paused_subs = [s for s in subs if not s["active"]]

    if not active and not paused_subs:
        st.info("You have no subscriptions yet.")
        if st.button("🛒 Browse products", type="primary"):
            st.session_state.page = "Shop"
            st.rerun()
        return

    # ── Daily cost summary ────────────────────────────────
    daily_cost = sum(
        products[s["product_id"]]["price"] * s["qty"]
        for s in active if s["product_id"] in products
    )
    st.markdown(f"""
    <div class="blue-card">
      <div style="font-size:12px;opacity:0.7">DAILY SPEND</div>
      <div style="font-size:28px;font-weight:800">₹{daily_cost}</div>
      <div style="font-size:13px;opacity:0.8">~₹{daily_cost*30} / month · {len(active)} active plan{'s' if len(active)!=1 else ''}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Active subscriptions ──────────────────────────────
    st.markdown("#### Active plans")
    changed = False
    for i, s in enumerate(st.session_state.subscriptions):
        if not s["active"]:
            continue
        if s["product_id"] not in products:
            continue
        p = products[s["product_id"]]

        with st.container():
            st.markdown(f"""
            <div class="dodla-card">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <div style="font-size:16px;font-weight:700">{p['emoji']} {p['name']}</div>
                  <div style="font-size:12px;color:#888;margin-top:3px">₹{p['price']} per unit</div>
                </div>
                <span class="badge b-green">Active</span>
              </div>
            </div>""", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                freq = st.selectbox("Frequency", FREQUENCIES,
                                    index=FREQUENCIES.index(s["frequency"]) if s["frequency"] in FREQUENCIES else 0,
                                    key=f"freq_{i}", label_visibility="collapsed")
                if freq != s["frequency"]:
                    st.session_state.subscriptions[i]["frequency"] = freq
                    changed = True

            with col2:
                qty = st.number_input("Quantity", min_value=1, max_value=10, value=s["qty"],
                                      key=f"qty_{i}", label_visibility="collapsed")
                if qty != s["qty"]:
                    st.session_state.subscriptions[i]["qty"] = qty
                    changed = True

            with col3:
                st.markdown(f"<div style='text-align:center;font-weight:800;color:#1a4a8c;padding-top:6px'>₹{p['price']*s['qty']}</div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("⏸ Pause", key=f"pause_{i}", use_container_width=True):
                    st.session_state.subscriptions[i]["active"] = False
                    st.success(f"Paused {p['name']}")
                    st.rerun()
            with c2:
                if st.button("🗑 Cancel", key=f"cancel_{i}", use_container_width=True):
                    st.session_state.subscriptions.pop(i)
                    st.warning(f"Removed {p['name']}")
                    st.rerun()

            st.markdown("---")

    if changed:
        st.success("✅ Changes saved!")

    # ── Paused subscriptions ──────────────────────────────
    if paused_subs:
        st.markdown("#### ⏸ Paused plans")
        for i, s in enumerate(st.session_state.subscriptions):
            if s["active"] or s["product_id"] not in products:
                continue
            p = products[s["product_id"]]
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div style="padding:8px 0">
                  <span style="color:#888">{p['emoji']} {p['name']}</span>
                  <span class="badge b-red" style="margin-left:8px">Paused</span>
                </div>""", unsafe_allow_html=True)
            with col2:
                if st.button("Resume ▶", key=f"resume_{i}", use_container_width=True, type="primary"):
                    st.session_state.subscriptions[i]["active"] = True
                    st.success(f"Resumed {p['name']}")
                    st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)
    if st.button("🛒 Add more products", use_container_width=True, type="primary"):
        st.session_state.page = "Shop"
        st.rerun()
