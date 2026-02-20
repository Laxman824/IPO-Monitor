# # pages/3_Settings.py
# import streamlit as st
# import json
# import os
# from datetime import datetime
# from config.config import Config

# def render_settings():
#     st.title("⚙️ System Settings")
    
#     # Create tabs for different settings
#     tab1, tab2, tab3 = st.tabs(["Notification Settings", "System Configuration", "Logs & Status"])
    
#     # Notification Settings
#     with tab1:
#         st.subheader("WhatsApp Notification Settings")
        
#         # Twilio Configuration
#         with st.expander("Twilio Configuration", expanded=True):
#             account_sid = st.text_input(
#                 "Account SID",
#                 value=Config.TWILIO_ACCOUNT_SID if Config.TWILIO_ACCOUNT_SID else "",
#                 type="password"
#             )
#             auth_token = st.text_input(
#                 "Auth Token",
#                 value=Config.TWILIO_AUTH_TOKEN if Config.TWILIO_AUTH_TOKEN else "",
#                 type="password"
#             )
#             phone_number = st.text_input(
#                 "WhatsApp Number",
#                 value=Config.TWILIO_PHONE_NUMBER if Config.TWILIO_PHONE_NUMBER else "",
#                 help="Format: +1234567890"
#             )
        
#         # Alert Templates
#         with st.expander("Alert Templates"):
#             st.markdown("### Message Templates")
#             high_gain_template = st.text_area(
#                 "High Gain Alert Template",
#                 value="""🚨 IPO Alert!
                
# IPO: {ipo_name}
# Gain: {gain}%
# Price: ₹{price}
# GMP: ₹{gmp}
# Type: {ipo_type}

# Subscribe for more alerts: {subscription_link}""",
#                 height=200
#             )
            
#             daily_summary_template = st.text_area(
#                 "Daily Summary Template",
#                 value="""📊 Daily IPO Summary

# Date: {date}
# Total Active IPOs: {total_ipos}
# High Gain IPOs: {high_gain_count}

# Top Performers:
# {top_performers}

# Full details: {dashboard_link}""",
#                 height=200
#             )
    
#     # System Configuration
#     with tab2:
#         st.subheader("System Configuration")
        
#         # Scraping Settings
#         with st.expander("Scraping Configuration", expanded=True):
#             col1, col2 = st.columns(2)
#             with col1:
#                 refresh_interval = st.number_input(
#                     "Data Refresh Interval (minutes)",
#                     min_value=5,
#                     max_value=60,
#                     value=15
#                 )
#             with col2:
#                 retry_attempts = st.number_input(
#                     "Max Retry Attempts",
#                     min_value=1,
#                     max_value=10,
#                     value=3
#                 )
            
#             user_agent = st.text_input(
#                 "User Agent",
#                 value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#             )
        
#         # Alert Settings
#         with st.expander("Alert Configuration"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 alert_cooldown = st.number_input(
#                     "Alert Cooldown (minutes)",
#                     min_value=5,
#                     max_value=120,
#                     value=30
#                 )
#             with col2:
#                 max_daily_alerts = st.number_input(
#                     "Max Daily Alerts per User",
#                     min_value=1,
#                     max_value=50,
#                     value=10
#                 )
    
#     # Logs & Status
#     with tab3:
#         st.subheader("System Status")
        
#         # System Health Metrics
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric(
#                 "System Status",
#                 "Active",
#                 "Online since 12h 30m"
#             )
#         with col2:
#             st.metric(
#                 "Last Successful Scrape",
#                 "2 min ago",
#                 "-3 min"
#             )
#         with col3:
#             st.metric(
#                 "Alert Success Rate",
#                 "98.5%",
#                 "1.5%"
#             )
        
#         # Recent Activity Log
#         st.markdown("### Recent Activity")
#         log_entries = [
#             {"timestamp": "2024-02-10 15:30:00", "type": "INFO", "message": "Data refresh completed"},
#             {"timestamp": "2024-02-10 15:29:55", "type": "SUCCESS", "message": "Sent alerts to 5 subscribers"},
#             {"timestamp": "2024-02-10 15:29:00", "type": "WARNING", "message": "Retry attempt 1 for data scraping"}
#         ]
        
#         for entry in log_entries:
#             color = "green" if entry["type"] == "SUCCESS" else "orange" if entry["type"] == "WARNING" else "blue"
#             st.markdown(f"""
#             <div style='padding: 5px; margin: 2px 0; border-left: 3px solid {color};'>
#                 <small>{entry['timestamp']}</small><br>
#                 <span style='color: {color};'><strong>{entry['type']}</strong></span>: {entry['message']}
#             </div>
#             """, unsafe_allow_html=True)
    
#     # Save Settings Button
#     if st.button("Save Settings", type="primary", use_container_width=True):
#         # Save configuration to .env file
#         with open(".env", "w") as f:
#             f.write(f"TWILIO_ACCOUNT_SID={account_sid}\n")
#             f.write(f"TWILIO_AUTH_TOKEN={auth_token}\n")
#             f.write(f"TWILIO_PHONE_NUMBER={phone_number}\n")
        
#         # Save other settings to config file
#         config = {
#             "refresh_interval": refresh_interval,
#             "retry_attempts": retry_attempts,
#             "user_agent": user_agent,
#             "alert_cooldown": alert_cooldown,
#             "max_daily_alerts": max_daily_alerts,
#             "templates": {
#                 "high_gain": high_gain_template,
#                 "daily_summary": daily_summary_template
#             }
#         }
        
#         with open("config.json", "w") as f:
#             json.dump(config, f, indent=4)
        
#         st.success("✅ Settings saved successfully!")

# if __name__ == "__main__":
#     render_settings()


# pages/3_Settings.py
import streamlit as st
from utils.database import Database
from config.config import Config
from datetime import datetime
import json
import os

st.set_page_config(
    page_title="Settings | IPO Monitor",
    page_icon="⚙️",
    layout="wide",
)

# ── CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, header, footer, .stDeployButton { display: none !important; }

.set-hero {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem;
    text-align: center; border: 1px solid rgba(255,255,255,.06);
}
.set-hero h1 {
    font-size: 2.2rem; font-weight: 900;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;
}
.set-hero p { color: #94a3b8; margin: .3rem 0 0; }

.section-title {
    font-size: 1.3rem; font-weight: 700; color: #e2e8f0;
    margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: .5rem;
}
.section-title .line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,.4), transparent);
}

.config-card {
    background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
    border: 1px solid rgba(255,255,255,.06); border-radius: 14px;
    padding: 1.5rem; margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Init ────────────────────────────────────────────────────────────
db = Database()
config = Config.get()

# ── Hero ────────────────────────────────────────────────────────────
st.markdown("""
<div class="set-hero">
    <h1>⚙️ Settings & Configuration</h1>
    <p>Manage application settings, notifications, and data</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎛️ General", "🔔 Notifications", "🗄️ Data Management", "ℹ️ About"
])

# ── General Settings ────────────────────────────────────────────────
with tab1:
    st.markdown(
        '<div class="section-title">🎛️ General Settings <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    with st.form("general_settings"):
        c1, c2 = st.columns(2)
        with c1:
            default_threshold = st.slider(
                "Default Gain Threshold (%)",
                0, 200,
                int(db.get_setting("default_threshold", config.DEFAULT_GAIN_THRESHOLD)),
            )
            cache_ttl = st.number_input(
                "Cache TTL (seconds)",
                60, 3600,
                int(db.get_setting("cache_ttl", config.CACHE_TTL)),
                step=60,
            )
        with c2:
            auto_refresh = st.toggle(
                "Auto-refresh enabled",
                value=db.get_setting("auto_refresh", "false") == "true",
            )
            refresh_interval = st.number_input(
                "Refresh Interval (minutes)",
                1, 60,
                int(db.get_setting("refresh_interval", "5")),
            )

        scraper_url = st.text_input(
            "Primary Scraper URL",
            value=db.get_setting("scraper_url", config.IPO_URL),
        )

        if st.form_submit_button("💾 Save General Settings", use_container_width=True):
            db.set_setting("default_threshold", str(default_threshold))
            db.set_setting("cache_ttl", str(cache_ttl))
            db.set_setting("auto_refresh", str(auto_refresh).lower())
            db.set_setting("refresh_interval", str(refresh_interval))
            db.set_setting("scraper_url", scraper_url)
            st.success("✅ General settings saved!")
            st.toast("Settings updated!", icon="✅")

# ── Notification Settings ───────────────────────────────────────────
with tab2:
    st.markdown(
        '<div class="section-title">🔔 Notification Settings <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    with st.form("notif_settings"):
        st.markdown("**WhatsApp (Twilio)**")
        c1, c2 = st.columns(2)
        with c1:
            twilio_sid = st.text_input(
                "Account SID",
                value=db.get_setting("twilio_sid", ""),
                type="password",
            )
        with c2:
            twilio_token = st.text_input(
                "Auth Token",
                value=db.get_setting("twilio_token", ""),
                type="password",
            )
        twilio_from = st.text_input(
            "WhatsApp From Number",
            value=db.get_setting("twilio_from", config.TWILIO_WHATSAPP_FROM),
        )

        st.markdown("---")
        st.markdown("**Email (SMTP)**")
        c1, c2 = st.columns(2)
        with c1:
            smtp_host = st.text_input(
                "SMTP Host",
                value=db.get_setting("smtp_host", config.SMTP_HOST),
            )
            smtp_user = st.text_input(
                "SMTP User",
                value=db.get_setting("smtp_user", ""),
            )
        with c2:
            smtp_port = st.number_input(
                "SMTP Port",
                value=int(db.get_setting("smtp_port", str(config.SMTP_PORT))),
            )
            smtp_pass = st.text_input(
                "SMTP Password",
                value=db.get_setting("smtp_pass", ""),
                type="password",
            )

        if st.form_submit_button("💾 Save Notification Settings", use_container_width=True):
            db.set_setting("twilio_sid", twilio_sid)
            db.set_setting("twilio_token", twilio_token)
            db.set_setting("twilio_from", twilio_from)
            db.set_setting("smtp_host", smtp_host)
            db.set_setting("smtp_port", str(smtp_port))
            db.set_setting("smtp_user", smtp_user)
            db.set_setting("smtp_pass", smtp_pass)
            st.success("✅ Notification settings saved!")

    # Test notification
    st.markdown("---")
    st.markdown("**🧪 Test Notifications**")
    tc1, tc2 = st.columns(2)
    with tc1:
        test_phone = st.text_input("Test phone", placeholder="+919876543210")
        if st.button("📱 Send Test WhatsApp", use_container_width=True):
            if test_phone:
                from utils.notifications import NotificationManager
                nm = NotificationManager()
                r = nm.send_whatsapp_message(test_phone, "🧪 Test message from IPO Monitor!")
                if r["status"] == "success":
                    st.success("✅ Test message sent!")
                else:
                    st.error(f"❌ {r['message']}")
            else:
                st.warning("Enter a phone number first.")
    with tc2:
        test_email = st.text_input("Test email", placeholder="test@example.com")
        if st.button("📧 Send Test Email", use_container_width=True):
            if test_email:
                from utils.notifications import NotificationManager
                nm = NotificationManager()
                r = nm.send_email(test_email, "IPO Monitor Test", "This is a test email!")
                if r["status"] == "success":
                    st.success("✅ Test email sent!")
                else:
                    st.error(f"❌ {r['message']}")
            else:
                st.warning("Enter an email first.")

# ── Data Management ─────────────────────────────────────────────────
with tab3:
    st.markdown(
        '<div class="section-title">🗄️ Data Management <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**📤 Export Data**")
        export_type = st.selectbox("Export", ["Subscribers", "IPO History", "Notification Log", "Settings"])

        if st.button("📥 Download CSV", use_container_width=True):
            if export_type == "Subscribers":
                data = db.get_subscribers(active_only=False)
            elif export_type == "IPO History":
                data = db.get_ipo_history(days=365)
            elif export_type == "Notification Log":
                data = db.get_notification_log(limit=1000)
            else:
                settings = db.get_all_settings()
                data = pd.DataFrame(list(settings.items()), columns=["Key", "Value"])

            if not data.empty:
                import pandas as pd
                csv = data.to_csv(index=False)
                st.download_button(
                    f"⬇️ Download {export_type}.csv",
                    csv,
                    f"{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    use_container_width=True,
                )
            else:
                st.info("No data to export.")

    with c2:
        st.markdown("**🧹 Maintenance**")

        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Cache cleared!")

        if st.button("🧹 Clean Old History (>90 days)", use_container_width=True):
            try:
                import sqlite3
                conn = sqlite3.connect(db.db_path)
                conn.execute(
                    "DELETE FROM ipo_history WHERE scraped_at < datetime('now', '-90 days')"
                )
                conn.commit()
                conn.close()
                st.success("✅ Old history cleaned!")
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown("**⚠️ Danger Zone**")
        with st.expander("🔴 Reset Database", expanded=False):
            st.warning("This will delete ALL data permanently!")
            confirm = st.text_input("Type 'RESET' to confirm", key="reset_confirm")
            if st.button("💣 Reset Everything", use_container_width=True, type="primary"):
                if confirm == "RESET":
                    try:
                        if os.path.exists(db.db_path):
                            os.remove(db.db_path)
                        db._setup_database()
                        st.success("✅ Database reset complete.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Type 'RESET' to confirm.")

# ── About ───────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        '<div class="section-title">ℹ️ About <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"""
    <div style="background:linear-gradient(145deg,#1e1b4b,#1a1a2e);
                border:1px solid rgba(255,255,255,.06);border-radius:16px;
                padding:2rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:.5rem;">📈</div>
        <h2 style="color:#e2e8f0;margin:0;">{config.APP_NAME}</h2>
        <p style="color:#a78bfa;font-size:1.1rem;">v{config.APP_VERSION}</p>
        <p style="color:#64748b;margin-top:1rem;">
            Real-time IPO Grey Market Premium tracker with alerts & analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🛠️ Tech Stack**")
        st.markdown("""
        | Component | Technology |
        |-----------|-----------|
        | Frontend  | Streamlit |
        | Charts    | Plotly |
        | Database  | SQLite |
        | Scraping  | BeautifulSoup |
        | Notifications | Twilio / SMTP |
        """)

    with c2:
        st.markdown("**📊 System Info**")
        db_size = os.path.getsize(db.db_path) / 1024 if os.path.exists(db.db_path) else 0
        sub_count = db.get_subscriber_count()
        history = db.get_ipo_history(days=365)

        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | DB Size | {db_size:.1f} KB |
        | Subscribers | {sub_count['total']} |
        | History Records | {len(history)} |
        | Cache TTL | {config.CACHE_TTL}s |
        | Python | 3.11+ |
        """)