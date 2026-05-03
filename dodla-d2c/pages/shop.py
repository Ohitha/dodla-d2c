import streamlit as st

CATEGORIES = ["All", "Milk", "Curd & Buttermilk", "Ghee & Butter", "Paneer", "Sweets"]

def is_subscribed(product_id):
    return any(s["product_id"] == product_id and s["active"]
               for s in st.session_state.subscriptions)

def add_subscription(product_id):
    if not is_subscribed(product_id):
        new_id = f"sub_{len(st.session_state.subscriptions)+1}"
        st.session_state.subscriptions.append({
            "id": new_id,
            "product_id": product_id,
            "qty": 1,
            "frequency": "Daily",
            "active": True
        })

def show():
    st.markdown("## 🛒 Shop")
    st.markdown("<p style='color:#888;font-size:13px;margin-top:-12px'>Subscribe to get daily doorstep delivery</p>", unsafe_allow_html=True)

    # ── Category filter ───────────────────────────────────
    if "shop_filter" not in st.session_state:
        st.session_state.shop_filter = "All"

    cols = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cols[i]:
            if st.button(cat, key=f"cat_{cat}", use_container_width=True,
                         type="primary" if st.session_state.shop_filter == cat else "secondary"):
                st.session_state.shop_filter = cat
                st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Product grid ──────────────────────────────────────
    products = st.session_state.products
    active_filter = st.session_state.shop_filter
    filtered = products if active_filter == "All" else [p for p in products if p["category"] == active_filter]

    if not filtered:
        st.info("No products in this category yet.")
        return

    # Render 2 columns
    for i in range(0, len(filtered), 2):
        row = filtered[i:i+2]
        cols = st.columns(2)
        for j, p in enumerate(row):
            with cols[j]:
                subscribed = is_subscribed(p["id"])
                oos_note = ""
                if not p["in_stock"]:
                    oos_note = f'<div style="font-size:11px;color:#e65100;margin-top:4px">🔴 Out of stock · Restock: {p.get("restock","Soon")}</div>'

                st.markdown(f"""
                <div class="product-card">
                  <div class="p-emoji">{p['emoji']}</div>
                  <div class="p-name">{p['name']}</div>
                  <div class="p-desc">{p['desc']}</div>
                  <div class="p-price">₹{p['price']}<span style="font-size:11px;color:#999;font-weight:400">/unit</span></div>
                  {oos_note}
                </div>""", unsafe_allow_html=True)

                if subscribed:
                    st.button("✅ Subscribed", key=f"sub_{p['id']}", disabled=True, use_container_width=True)
                elif not p["in_stock"]:
                    st.button("⏳ Out of stock", key=f"oos_{p['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("+ Subscribe", key=f"add_{p['id']}", use_container_width=True, type="primary"):
                        add_subscription(p["id"])
                        st.success(f"✅ {p['name']} added to your subscriptions!")
                        st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="dodla-card" style="text-align:center">
      <div style="font-size:20px">🚚</div>
      <div style="font-weight:700;margin-top:6px">Free delivery every morning</div>
      <div style="font-size:13px;color:#888;margin-top:4px">Order by midnight · Delivered by 6:30 AM · Cancel anytime</div>
    </div>
    """, unsafe_allow_html=True)
