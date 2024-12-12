# pages/3_Settings.py
import streamlit as st
import json
import os
from datetime import datetime
from config.config import Config

def render_settings():
    st.title("⚙️ System Settings")
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["Notification Settings", "System Configuration", "Logs & Status"])
    
    # Notification Settings
    with tab1:
        st.subheader("WhatsApp Notification Settings")
        
        # Twilio Configuration
        with st.expander("Twilio Configuration", expanded=True):
            account_sid = st.text_input(
                "Account SID",
                value=Config.TWILIO_ACCOUNT_SID if Config.TWILIO_ACCOUNT_SID else "",
                type="password"
            )
            auth_token = st.text_input(
                "Auth Token",
                value=Config.TWILIO_AUTH_TOKEN if Config.TWILIO_AUTH_TOKEN else "",
                type="password"
            )
            phone_number = st.text_input(
                "WhatsApp Number",
                value=Config.TWILIO_PHONE_NUMBER if Config.TWILIO_PHONE_NUMBER else "",
                help="Format: +1234567890"
            )
        
        # Alert Templates
        with st.expander("Alert Templates"):
            st.markdown("### Message Templates")
            high_gain_template = st.text_area(
                "High Gain Alert Template",
                value="""🚨 IPO Alert!
                
IPO: {ipo_name}
Gain: {gain}%
Price: ₹{price}
GMP: ₹{gmp}
Type: {ipo_type}

Subscribe for more alerts: {subscription_link}""",
                height=200
            )
            
            daily_summary_template = st.text_area(
                "Daily Summary Template",
                value="""📊 Daily IPO Summary

Date: {date}
Total Active IPOs: {total_ipos}
High Gain IPOs: {high_gain_count}

Top Performers:
{top_performers}

Full details: {dashboard_link}""",
                height=200
            )
    
    # System Configuration
    with tab2:
        st.subheader("System Configuration")
        
        # Scraping Settings
        with st.expander("Scraping Configuration", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                refresh_interval = st.number_input(
                    "Data Refresh Interval (minutes)",
                    min_value=5,
                    max_value=60,
                    value=15
                )
            with col2:
                retry_attempts = st.number_input(
                    "Max Retry Attempts",
                    min_value=1,
                    max_value=10,
                    value=3
                )
            
            user_agent = st.text_input(
                "User Agent",
                value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        
        # Alert Settings
        with st.expander("Alert Configuration"):
            col1, col2 = st.columns(2)
            with col1:
                alert_cooldown = st.number_input(
                    "Alert Cooldown (minutes)",
                    min_value=5,
                    max_value=120,
                    value=30
                )
            with col2:
                max_daily_alerts = st.number_input(
                    "Max Daily Alerts per User",
                    min_value=1,
                    max_value=50,
                    value=10
                )
    
    # Logs & Status
    with tab3:
        st.subheader("System Status")
        
        # System Health Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "System Status",
                "Active",
                "Online since 12h 30m"
            )
        with col2:
            st.metric(
                "Last Successful Scrape",
                "2 min ago",
                "-3 min"
            )
        with col3:
            st.metric(
                "Alert Success Rate",
                "98.5%",
                "1.5%"
            )
        
        # Recent Activity Log
        st.markdown("### Recent Activity")
        log_entries = [
            {"timestamp": "2024-02-10 15:30:00", "type": "INFO", "message": "Data refresh completed"},
            {"timestamp": "2024-02-10 15:29:55", "type": "SUCCESS", "message": "Sent alerts to 5 subscribers"},
            {"timestamp": "2024-02-10 15:29:00", "type": "WARNING", "message": "Retry attempt 1 for data scraping"}
        ]
        
        for entry in log_entries:
            color = "green" if entry["type"] == "SUCCESS" else "orange" if entry["type"] == "WARNING" else "blue"
            st.markdown(f"""
            <div style='padding: 5px; margin: 2px 0; border-left: 3px solid {color};'>
                <small>{entry['timestamp']}</small><br>
                <span style='color: {color};'><strong>{entry['type']}</strong></span>: {entry['message']}
            </div>
            """, unsafe_allow_html=True)
    
    # Save Settings Button
    if st.button("Save Settings", type="primary", use_container_width=True):
        # Save configuration to .env file
        with open(".env", "w") as f:
            f.write(f"TWILIO_ACCOUNT_SID={account_sid}\n")
            f.write(f"TWILIO_AUTH_TOKEN={auth_token}\n")
            f.write(f"TWILIO_PHONE_NUMBER={phone_number}\n")
        
        # Save other settings to config file
        config = {
            "refresh_interval": refresh_interval,
            "retry_attempts": retry_attempts,
            "user_agent": user_agent,
            "alert_cooldown": alert_cooldown,
            "max_daily_alerts": max_daily_alerts,
            "templates": {
                "high_gain": high_gain_template,
                "daily_summary": daily_summary_template
            }
        }
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        
        st.success("✅ Settings saved successfully!")
# Add to pages/3_Settings.py

def check_twilio_setup():
    st.subheader("🔧 Twilio Configuration Check")
    
    with st.expander("Debug Twilio Setup", expanded=True):
        st.write("Current Configuration:")
        
        # Check if credentials exist
        if not Config.TWILIO_ACCOUNT_SID:
            st.error("❌ TWILIO_ACCOUNT_SID is missing")
        else:
            st.success(f"✅ TWILIO_ACCOUNT_SID: ...{Config.TWILIO_ACCOUNT_SID[-4:]}")
            
        if not Config.TWILIO_AUTH_TOKEN:
            st.error("❌ TWILIO_AUTH_TOKEN is missing")
        else:
            st.success("✅ TWILIO_AUTH_TOKEN is set")
            
        if not Config.TWILIO_PHONE_NUMBER:
            st.error("❌ TWILIO_PHONE_NUMBER is missing")
        else:
            st.success(f"✅ TWILIO_PHONE_NUMBER: {Config.TWILIO_PHONE_NUMBER}")
        
        if st.button("Test Twilio Connection"):
            try:
                notification_manager = NotificationManager()
                result = notification_manager.verify_credentials()
                
                if result["status"] == "success":
                    st.success(f"✅ Successfully connected to Twilio account: {result['account_name']}")
                else:
                    st.error(f"❌ Failed to connect: {result['message']}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
if __name__ == "__main__":
    render_settings()