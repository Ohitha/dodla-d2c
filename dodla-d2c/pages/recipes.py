import streamlit as st

CATEGORY_COLORS = {
    "Beverages": "#e3f2fd",
    "Breakfast": "#fff8e1",
    "Mains": "#e8f5e9",
    "Desserts": "#fce4ec",
    "Breads": "#fff3e0",
}

def show():
    st.markdown("## 🍳 Recipes")
    st.markdown("<p style='color:#888;font-size:13px;margin-top:-12px'>Made fresh with Dodla dairy products</p>", unsafe_allow_html=True)

    recipes = st.session_state.recipes
    products = {p["id"]: p for p in st.session_state.products}

    if not recipes:
        st.info("Recipes coming soon!")
        return

    # ── Filter by category ────────────────────────────────
    categories = ["All"] + sorted(set(r["category"] for r in recipes))
    if "recipe_filter" not in st.session_state:
        st.session_state.recipe_filter = "All"

    cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cols[i]:
            if st.button(cat, key=f"rcat_{cat}", use_container_width=True,
                         type="primary" if st.session_state.recipe_filter == cat else "secondary"):
                st.session_state.recipe_filter = cat
                st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    active = st.session_state.recipe_filter
    filtered = recipes if active == "All" else [r for r in recipes if r["category"] == active]

    # ── Recipe cards grid ─────────────────────────────────
    for i in range(0, len(filtered), 2):
        row = filtered[i:i+2]
        cols = st.columns(2)
        for j, r in enumerate(row):
            with cols[j]:
                bg = CATEGORY_COLORS.get(r["category"], "#f5f5f5")
                st.markdown(f"""
                <div class="recipe-card" style="background:{bg}">
                  <div class="r-emoji">{r['emoji']}</div>
                  <div class="r-name">{r['name']}</div>
                  <div class="r-time">⏱ {r['time_mins']} min · {r['category']}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"View recipe →"):
                    # Products used
                    used = [products[pid] for pid in r.get("dodla_products", []) if pid in products]
                    if used:
                        tags = " ".join(f'<span class="badge b-blue">{p["emoji"]} {p["name"]}</span>' for p in used)
                        st.markdown(f"<div style='margin-bottom:12px'><strong>Dodla products used:</strong><br>{tags}</div>", unsafe_allow_html=True)

                    # Ingredients
                    st.markdown("**Ingredients:**")
                    for ing in r["ingredients"]:
                        st.markdown(f"- {ing}")

                    # Steps
                    st.markdown("**Method:**")
                    for step_i, step in enumerate(r["steps"], 1):
                        st.markdown(f"""
                        <div style="display:flex;gap:10px;margin-bottom:8px;align-items:flex-start">
                          <div style="min-width:24px;height:24px;border-radius:50%;background:#1a4a8c;
                               color:white;display:flex;align-items:center;justify-content:center;
                               font-size:12px;font-weight:700;margin-top:1px">{step_i}</div>
                          <div style="font-size:14px;line-height:1.5">{step}</div>
                        </div>""", unsafe_allow_html=True)

                    # Subscribe to products used
                    if used:
                        if st.button(f"🛒 Subscribe to these products", key=f"recipe_sub_{r['id']}", use_container_width=True):
                            added = 0
                            for p in used:
                                already = any(s["product_id"] == p["id"] and s["active"] for s in st.session_state.subscriptions)
                                if not already and p["in_stock"]:
                                    st.session_state.subscriptions.append({
                                        "id": f"sub_{len(st.session_state.subscriptions)+1}",
                                        "product_id": p["id"], "qty": 1,
                                        "frequency": "Daily", "active": True
                                    })
                                    added += 1
                            if added:
                                st.success(f"✅ Added {added} product(s) to your subscriptions!")
                            else:
                                st.info("You're already subscribed to all products in this recipe!")

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="dodla-card" style="text-align:center">
      <div style="font-size:20px">👨‍🍳</div>
      <div style="font-weight:700;margin-top:6px">More recipes every week</div>
      <div style="font-size:13px;color:#888;margin-top:4px">Made by our in-house nutritionist using fresh Dodla products</div>
    </div>
    """, unsafe_allow_html=True)
