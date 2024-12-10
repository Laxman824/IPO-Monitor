# pages/2_Subscribers.py
import streamlit as st
from utils.database import Database
from datetime import datetime

def render_subscribers():
    st.title("📱 Subscriber Management")
    
    # Initialize database
    db = Database()
    
    # Create two columns layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add New Subscriber")
        with st.form("new_subscriber", clear_on_submit=True):
            name = st.text_input("Full Name", placeholder="Enter subscriber's name")
            phone = st.text_input("WhatsApp Number", placeholder="e.g., +919876543210")
            
            # Create two columns for thresholds
            threshold_col1, threshold_col2 = st.columns(2)
            with threshold_col1:
                gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
            with threshold_col2:
                alert_frequency = st.selectbox(
                    "Alert Frequency",
                    ["Immediate", "Daily", "Weekly"]
                )
            
            # Custom preferences
            st.write("Notification Preferences")
            col1, col2 = st.columns(2)
            with col1:
                notify_mainboard = st.checkbox("Mainboard IPOs", value=True)
                notify_bse = st.checkbox("BSE SME IPOs", value=True)
            with col2:
                notify_nse = st.checkbox("NSE SME IPOs", value=True)
                notify_gmp_changes = st.checkbox("GMP Changes", value=True)
            
            submitted = st.form_submit_button("Add Subscriber", use_container_width=True)
            if submitted:
                if name and phone:
                    preferences = {
                        "mainboard": notify_mainboard,
                        "bse_sme": notify_bse,
                        "nse_sme": notify_nse,
                        "gmp_changes": notify_gmp_changes,
                        "alert_frequency": alert_frequency
                    }
                    db.add_subscriber(phone, name, gain_threshold, preferences)
                    st.success(f"✅ Successfully added {name} to subscribers!")
                else:
                    st.error("Please fill in all required fields!")

    with col2:
        st.subheader("Quick Stats")
        total_subs = len(db.get_subscribers())
        active_subs = len(db.get_subscribers(active_only=True))
        
        # Stats in a card-like container
        with st.container():
            st.metric("Total Subscribers", total_subs)
            st.metric("Active Subscribers", active_subs)
            st.metric("Inactive Subscribers", total_subs - active_subs)
    
    # Subscriber List
    st.markdown("---")
    st.subheader("Current Subscribers")
    
    # Tabs for Active and Inactive subscribers
    tab1, tab2 = st.tabs(["Active Subscribers", "Inactive Subscribers"])
    
    with tab1:
        active_subscribers = db.get_subscribers(active_only=True)
        if not active_subscribers.empty:
            for _, sub in active_subscribers.iterrows():
                with st.expander(f"📱 {sub['name']} ({sub['phone']})"):
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.write(f"**Name:** {sub['name']}")
                        st.write(f"**Phone:** {sub['phone']}")
                    with col2:
                        st.write(f"**Threshold:** {sub['gain_threshold']}%")
                        st.write(f"**Status:** Active")
                    with col3:
                        if st.button("Deactivate", key=f"deact_{sub['phone']}"):
                            db.deactivate_subscriber(sub['phone'])
                            st.rerun()
        else:
            st.info("No active subscribers found")
    
    with tab2:
        inactive_subscribers = db.get_subscribers(active_only=False)
        if not inactive_subscribers.empty:
            for _, sub in inactive_subscribers.iterrows():
                with st.expander(f"📱 {sub['name']} ({sub['phone']})"):
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.write(f"**Name:** {sub['name']}")
                        st.write(f"**Phone:** {sub['phone']}")
                    with col2:
                        st.write(f"**Threshold:** {sub['gain_threshold']}%")
                        st.write(f"**Status:** Inactive")
                    with col3:
                        if st.button("Reactivate", key=f"react_{sub['phone']}"):
                            db.activate_subscriber(sub['phone'])
                            st.rerun()
        else:
            st.info("No inactive subscribers found")

if __name__ == "__main__":
    render_subscribers()