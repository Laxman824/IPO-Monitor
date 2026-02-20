
# #vesrion2 working
# # pages/2_Subscribers.py
# import streamlit as st
# from utils.database import Database
# from utils.notifications import NotificationManager
# from datetime import datetime

# def render_subscribers():
#     st.title("📱 Subscriber Management")
    
#     # Initialize database and notification manager
#     db = Database()
#     notification_manager = NotificationManager()
    
#     # Create two columns layout
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("Add New Subscriber")
#         with st.form("new_subscriber", clear_on_submit=True):
#             name = st.text_input("Full Name", placeholder="Enter subscriber's name")
#             phone = st.text_input("WhatsApp Number", placeholder="e.g., +919876543210")
            
#             # Create two columns for thresholds
#             threshold_col1, threshold_col2 = st.columns(2)
#             with threshold_col1:
#                 gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
#             with threshold_col2:
#                 alert_frequency = st.selectbox(
#                     "Alert Frequency",
#                     ["Immediate", "Daily", "Weekly"]
#                 )
            
#             # Custom preferences
#             st.write("Notification Preferences")
#             col1, col2 = st.columns(2)
#             with col1:
#                 notify_mainboard = st.checkbox("Mainboard IPOs", value=True)
#                 notify_bse = st.checkbox("BSE SME IPOs", value=True)
#             with col2:
#                 notify_nse = st.checkbox("NSE SME IPOs", value=True)
#                 notify_gmp_changes = st.checkbox("GMP Changes", value=True)
            
#             submitted = st.form_submit_button("Add Subscriber", use_container_width=True)
#             if submitted:
#                 if name and phone:
#                     try:
#                         # Format phone number if needed
#                         if not phone.startswith('whatsapp:'):
#                             formatted_phone = f"whatsapp:{phone}"
#                         else:
#                             formatted_phone = phone
                        
#                         # Prepare preferences
#                         preferences = {
#                             "mainboard": notify_mainboard,
#                             "bse_sme": notify_bse,
#                             "nse_sme": notify_nse,
#                             "gmp_changes": notify_gmp_changes,
#                             "alert_frequency": alert_frequency
#                         }
                        
#                         # Send welcome message first
#                         welcome_message = f"""Welcome to IPO GMP Monitor! 🎉

# Hi {name},

# You've been successfully subscribed to IPO alerts with the following preferences:
# - Gain Threshold: {gain_threshold}%
# - Alert Frequency: {alert_frequency}
# - Mainboard IPOs: {'Yes' if notify_mainboard else 'No'}
# - BSE SME IPOs: {'Yes' if notify_bse else 'No'}
# - NSE SME IPOs: {'Yes' if notify_nse else 'No'}

# You'll receive alerts when IPOs match your criteria.
# To stop receiving alerts, reply with 'STOP'.

# Thank you for subscribing! 🙏"""

#                         # Try to send welcome message
#                         message_sent = notification_manager.send_whatsapp_message(
#                             formatted_phone, 
#                             welcome_message
#                         )
                        
#                         if message_sent:
#                             # Add to database only if message was sent successfully
#                             if db.add_subscriber(formatted_phone, name, gain_threshold, preferences):
#                                 st.success(f"✅ Successfully added {name} and sent welcome message!")
#                                 # Log the successful subscription
#                                 db.log_activity('INFO', f'New subscriber added: {name} ({formatted_phone})')
#                             else:
#                                 st.error("Failed to add subscriber to database!")
#                         else:
#                             st.error("Failed to send welcome message. Please check the phone number and Twilio configuration.")
                            
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")
#                         db.log_activity('ERROR', f'Failed to add subscriber: {str(e)}')
#                 else:
#                     st.error("Please fill in all required fields!")

#     # Display current subscribers and stats
#     st.markdown("---")
#     st.subheader("Current Subscribers")
    
#     try:
#         subscribers = db.get_subscribers(active_only=True)
#         if not subscribers.empty:
#             st.dataframe(subscribers[['name', 'phone', 'gain_threshold', 'created_at']])
#         else:
#             st.info("No subscribers found. Add your first subscriber above!")
#     except Exception as e:
#         st.error(f"Error loading subscribers: {str(e)}")

# if __name__ == "__main__":
#     render_subscribers()


# pages/2_Subscribers.py
import streamlit as st
import pandas as pd
from utils.database import Database
from datetime import datetime

st.set_page_config(
    page_title="Subscribers | IPO Monitor",
    page_icon="👥",
    layout="wide",
)

# ── CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, header, footer, .stDeployButton { display: none !important; }

.sub-hero {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem;
    text-align: center; border: 1px solid rgba(255,255,255,.06);
}
.sub-hero h1 {
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;
}
.sub-hero p { color: #94a3b8; margin: .3rem 0 0; }

.stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.stat-box {
    flex: 1; background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
    border: 1px solid rgba(255,255,255,.06); border-radius: 16px;
    padding: 1.3rem; text-align: center;
}
.stat-box .val {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-box .lbl { color: #94a3b8; font-size: .85rem; }

.sub-card {
    background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
    border: 1px solid rgba(255,255,255,.06); border-radius: 14px;
    padding: 1.2rem 1.5rem; margin-bottom: .6rem;
    display: flex; align-items: center; justify-content: space-between;
    transition: all .2s;
}
.sub-card:hover { border-color: rgba(99,102,241,.35); transform: translateX(4px); }
.sub-name { font-weight: 600; color: #e2e8f0; font-size: 1.05rem; }
.sub-meta { color: #64748b; font-size: .82rem; margin-top: 2px; }
.sub-status {
    font-size: .75rem; padding: 3px 10px; border-radius: 20px;
    font-weight: 600; text-transform: uppercase;
}
.status-active   { background: rgba(34,197,94,.12); color: #22c55e; }
.status-inactive { background: rgba(239,68,68,.12); color: #ef4444; }

.section-title {
    font-size: 1.3rem; font-weight: 700; color: #e2e8f0;
    margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: .5rem;
}
.section-title .line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,.4), transparent);
}
</style>
""", unsafe_allow_html=True)

# ── Init ────────────────────────────────────────────────────────────
db = Database()

# ── Hero ────────────────────────────────────────────────────────────
st.markdown("""
<div class="sub-hero">
    <h1>👥 Subscriber Management</h1>
    <p>Add, edit, and manage IPO alert subscribers</p>
</div>
""", unsafe_allow_html=True)

# ── Stats ───────────────────────────────────────────────────────────
stats = db.get_subscriber_count()
st.markdown(f"""
<div class="stat-row">
    <div class="stat-box">
        <div class="val">{stats['total']}</div>
        <div class="lbl">Total Subscribers</div>
    </div>
    <div class="stat-box">
        <div class="val">{stats['active']}</div>
        <div class="lbl">Active</div>
    </div>
    <div class="stat-box">
        <div class="val">{stats['inactive']}</div>
        <div class="lbl">Inactive</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 All Subscribers", "➕ Add New", "📊 Analytics"])

with tab1:
    # Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔍", placeholder="Search by name or phone…",
                               label_visibility="collapsed", key="sub_search")
    with c2:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive"],
                                     label_visibility="collapsed")
    with c3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Load data
    show_active = None
    if status_filter == "Active":
        show_active = True
    elif status_filter == "Inactive":
        show_active = False

    subs = db.get_subscribers(active_only=False)

    if show_active is not None:
        subs = subs[subs["active"] == (1 if show_active else 0)]

    if search:
        mask = (
            subs["name"].str.contains(search, case=False, na=False) |
            subs["phone"].str.contains(search, case=False, na=False)
        )
        subs = subs[mask]

    if subs.empty:
        st.info("No subscribers found.")
    else:
        # Render cards
        for _, row in subs.iterrows():
            active = row.get("active", 0)
            status_cls = "status-active" if active else "status-inactive"
            status_txt = "Active" if active else "Inactive"
            threshold = row.get("gain_threshold", 50)
            created = row.get("created_at", "—")

            st.markdown(f"""
            <div class="sub-card">
                <div>
                    <div class="sub-name">{row['name']}</div>
                    <div class="sub-meta">📱 {row['phone']} &nbsp;•&nbsp;
                        🎯 {threshold}% threshold &nbsp;•&nbsp;
                        📅 {str(created)[:10]}</div>
                </div>
                <span class="sub-status {status_cls}">{status_txt}</span>
            </div>
            """, unsafe_allow_html=True)

        # Action buttons per subscriber
        st.markdown("---")
        st.markdown(
            '<div class="section-title">⚡ Quick Actions <span class="line"></span></div>',
            unsafe_allow_html=True,
        )

        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            phone_input = st.selectbox(
                "Select subscriber",
                subs["phone"].tolist(),
                format_func=lambda p: f"{subs[subs['phone']==p]['name'].iloc[0]} ({p})",
            )
        with action_col2:
            if st.button("🔴 Deactivate", use_container_width=True):
                if db.deactivate_subscriber(phone_input):
                    st.success(f"Deactivated {phone_input}")
                    st.rerun()
        with action_col3:
            if st.button("🟢 Activate", use_container_width=True):
                if db.activate_subscriber(phone_input):
                    st.success(f"Activated {phone_input}")
                    st.rerun()

        # Raw table
        with st.expander("📄 Raw Data"):
            display_cols = ["name", "phone", "gain_threshold", "active", "created_at"]
            available = [c for c in display_cols if c in subs.columns]
            st.dataframe(subs[available], use_container_width=True, hide_index=True)

with tab2:
    st.markdown(
        '<div class="section-title">➕ Add New Subscriber <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    with st.form("add_subscriber", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("Full Name *", placeholder="Enter name")
            new_phone = st.text_input("Phone Number *", placeholder="+919876543210")
            new_email = st.text_input("Email", placeholder="email@example.com")
        with c2:
            new_threshold = st.slider("Gain Threshold (%)", 0, 200, 50)
            new_frequency = st.selectbox("Alert Frequency",
                                         ["Immediate", "Daily", "Weekly"])
            new_wa = st.checkbox("Enable WhatsApp", value=True)
            new_push = st.checkbox("Enable Push Notifications", value=True)

        add_btn = st.form_submit_button("➕ Add Subscriber", use_container_width=True)

        if add_btn:
            if not new_name or not new_phone:
                st.error("Name and phone are required.")
            else:
                prefs = {
                    "alert_frequency": new_frequency,
                    "notifications": {"whatsapp": new_wa, "push": new_push},
                }
                if db.add_subscriber(new_phone, new_name, new_threshold, prefs, new_email):
                    st.success(f"✅ {new_name} added successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Failed to add subscriber.")

with tab3:
    st.markdown(
        '<div class="section-title">📊 Subscriber Analytics <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    all_subs = db.get_subscribers(active_only=False)
    if all_subs.empty:
        st.info("No subscriber data to analyze yet.")
    else:
        import plotly.express as px

        c1, c2 = st.columns(2)
        with c1:
            active_counts = all_subs["active"].value_counts()
            labels = ["Active" if k else "Inactive" for k in active_counts.index]
            fig = px.pie(
                values=active_counts.values,
                names=labels,
                title="Active vs Inactive",
                color_discrete_sequence=["#22c55e", "#ef4444"],
                hole=0.5,
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                title_x=0.5,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.histogram(
                all_subs, x="gain_threshold", nbins=15,
                title="Threshold Distribution",
                color_discrete_sequence=["#a78bfa"],
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                title_x=0.5,
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Notification log
        st.markdown(
            '<div class="section-title">📨 Recent Notifications <span class="line"></span></div>',
            unsafe_allow_html=True,
        )
        logs = db.get_notification_log(limit=20)
        if logs.empty:
            st.info("No notifications sent yet.")
        else:
            st.dataframe(logs, use_container_width=True, hide_index=True)