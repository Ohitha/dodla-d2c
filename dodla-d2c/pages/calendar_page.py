import streamlit as st
import calendar
from datetime import date

DELIVERY_INSTRUCTIONS = [
    "Leave at door",
    "Ring bell",
    "No doorbell — early morning",
    "Hand to security",
    "Place in milk box",
]

def show():
    st.markdown("## 📅 Delivery Calendar")

    today = date.today()
    month_name = today.strftime("%B %Y")
    st.markdown(f"<p style='color:#888;font-size:14px;margin-top:-12px'>{month_name} — tap any future date to pause/resume</p>", unsafe_allow_html=True)

    paused_days = set(st.session_state.paused_days)
    today_day = today.day
    _, num_days = calendar.monthrange(today.year, today.month)
    first_weekday = calendar.monthrange(today.year, today.month)[0]  # 0=Mon

    # Build calendar HTML
    day_headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    headers_html = "".join(f"<th>{d}</th>" for d in day_headers)

    cells = ["<td></td>"] * first_weekday  # empty cells before day 1
    for d in range(1, num_days + 1):
        if d < today_day:
            cls = "cd"  # delivered
        elif d == today_day:
            cls = "ct"  # today
        elif d in paused_days:
            cls = "cp"  # paused
        else:
            cls = "cs"  # scheduled

        cells.append(f'<td class="{cls}">{d}</td>')

    # Pad to complete last row
    while len(cells) % 7 != 0:
        cells.append("<td></td>")

    rows_html = ""
    for i in range(0, len(cells), 7):
        rows_html += "<tr>" + "".join(cells[i:i+7]) + "</tr>"

    cal_html = f"""
    <div class="cal-wrapper">
    <table class="cal">
      <thead><tr>{headers_html}</tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>
    <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap;font-size:12px">
      <span><span class="badge b-blue" style="background:#1a4a8c;color:white">25</span> Delivered</span>
      <span><span class="badge b-blue">26</span> Scheduled</span>
      <span><span class="badge b-red" style="background:#fff3e0;color:#e65100">27</span> Paused</span>
      <span><span style="border:2.5px solid #1a4a8c;border-radius:50%;padding:1px 7px;font-weight:800;color:#1a4a8c">{today_day}</span> Today</span>
    </div>
    """
    st.markdown(cal_html, unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Pause/resume controls ──────────────────────────────
    st.markdown("#### Pause or resume a day")
    col1, col2 = st.columns(2)
    with col1:
        pause_day = st.number_input("Pause day", min_value=today_day+1, max_value=num_days,
                                     value=min(today_day+1, num_days), label_visibility="visible")
    with col2:
        action = st.selectbox("Action", ["Pause delivery", "Resume delivery"])

    if st.button("Apply change", type="primary", use_container_width=True):
        if action == "Pause delivery":
            if pause_day not in st.session_state.paused_days:
                st.session_state.paused_days.append(int(pause_day))
                st.success(f"✅ Delivery paused for day {int(pause_day)}")
            else:
                st.info(f"Day {int(pause_day)} is already paused")
        else:
            if int(pause_day) in st.session_state.paused_days:
                st.session_state.paused_days.remove(int(pause_day))
                st.success(f"▶ Delivery resumed for day {int(pause_day)}")
            else:
                st.info(f"Day {int(pause_day)} is not paused")
        st.rerun()

    # ── Pause summary ─────────────────────────────────────
    if st.session_state.paused_days:
        future_paused = sorted([d for d in st.session_state.paused_days if d >= today_day])
        if future_paused:
            days_str = ", ".join(str(d) for d in future_paused)
            st.markdown(f"""
            <div class="dodla-card">
              <div style="font-weight:700">⏸ Upcoming pauses</div>
              <div style="color:#888;font-size:13px;margin-top:4px">
                Day(s) {days_str} of {month_name}
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Vacation mode ─────────────────────────────────────
    st.markdown("#### 🏖 Vacation mode")
    st.markdown("<p style='font-size:13px;color:#888'>Pause all deliveries for a date range</p>", unsafe_allow_html=True)
    vc1, vc2 = st.columns(2)
    with vc1:
        vac_start = st.number_input("From day", min_value=today_day+1, max_value=num_days,
                                     value=min(today_day+2, num_days), key="vac_start")
    with vc2:
        vac_end = st.number_input("To day", min_value=today_day+1, max_value=num_days,
                                   value=min(today_day+5, num_days), key="vac_end")
    if st.button("🏖 Pause all in range", use_container_width=True):
        added = 0
        for d in range(int(vac_start), int(vac_end)+1):
            if d not in st.session_state.paused_days:
                st.session_state.paused_days.append(d)
                added += 1
        st.success(f"✅ Paused {added} day(s) from day {int(vac_start)} to {int(vac_end)}")
        st.rerun()

    st.markdown("<hr class='dodla'>", unsafe_allow_html=True)

    # ── Delivery instructions ─────────────────────────────
    st.markdown("#### 📝 Delivery instructions")
    if "delivery_instruction" not in st.session_state:
        st.session_state.delivery_instruction = DELIVERY_INSTRUCTIONS[0]
    if "delivery_note" not in st.session_state:
        st.session_state.delivery_note = ""

    instr = st.selectbox("Select instruction", DELIVERY_INSTRUCTIONS,
                          index=DELIVERY_INSTRUCTIONS.index(st.session_state.delivery_instruction)
                          if st.session_state.delivery_instruction in DELIVERY_INSTRUCTIONS else 0)

    note = st.text_area("Additional note for delivery partner",
                         value=st.session_state.delivery_note,
                         placeholder="e.g. Please don't ring the bell before 7 AM...",
                         max_chars=200)

    if st.button("💾 Save instructions", use_container_width=True, type="primary"):
        st.session_state.delivery_instruction = instr
        st.session_state.delivery_note = note
        st.success("✅ Delivery instructions saved!")
