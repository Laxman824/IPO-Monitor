
#vesrion2 working
# pages/2_Subscribers.py
import streamlit as st
from utils.database import Database
from utils.notifications import NotificationManager
from datetime import datetime

def render_subscribers():
    st.title("📱 Subscriber Management")
    
    # Initialize database and notification manager
    db = Database()
    notification_manager = NotificationManager()
    
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
                    try:
                        # Format phone number if needed
                        if not phone.startswith('whatsapp:'):
                            formatted_phone = f"whatsapp:{phone}"
                        else:
                            formatted_phone = phone
                        
                        # Prepare preferences
                        preferences = {
                            "mainboard": notify_mainboard,
                            "bse_sme": notify_bse,
                            "nse_sme": notify_nse,
                            "gmp_changes": notify_gmp_changes,
                            "alert_frequency": alert_frequency
                        }
                        
                        # Send welcome message first
                        welcome_message = f"""Welcome to IPO GMP Monitor! 🎉

Hi {name},

You've been successfully subscribed to IPO alerts with the following preferences:
- Gain Threshold: {gain_threshold}%
- Alert Frequency: {alert_frequency}
- Mainboard IPOs: {'Yes' if notify_mainboard else 'No'}
- BSE SME IPOs: {'Yes' if notify_bse else 'No'}
- NSE SME IPOs: {'Yes' if notify_nse else 'No'}

You'll receive alerts when IPOs match your criteria.
To stop receiving alerts, reply with 'STOP'.

Thank you for subscribing! 🙏"""

                        # Try to send welcome message
                        message_sent = notification_manager.send_whatsapp_message(
                            formatted_phone, 
                            welcome_message
                        )
                        
                        if message_sent:
                            # Add to database only if message was sent successfully
                            if db.add_subscriber(formatted_phone, name, gain_threshold, preferences):
                                st.success(f"✅ Successfully added {name} and sent welcome message!")
                                # Log the successful subscription
                                db.log_activity('INFO', f'New subscriber added: {name} ({formatted_phone})')
                            else:
                                st.error("Failed to add subscriber to database!")
                        else:
                            st.error("Failed to send welcome message. Please check the phone number and Twilio configuration.")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        db.log_activity('ERROR', f'Failed to add subscriber: {str(e)}')
                else:
                    st.error("Please fill in all required fields!")

    # Display current subscribers and stats
    st.markdown("---")
    st.subheader("Current Subscribers")
    
    try:
        subscribers = db.get_subscribers(active_only=True)
        if not subscribers.empty:
            st.dataframe(subscribers[['name', 'phone', 'gain_threshold', 'created_at']])
        else:
            st.info("No subscribers found. Add your first subscriber above!")
    except Exception as e:
        st.error(f"Error loading subscribers: {str(e)}")

if __name__ == "__main__":
    render_subscribers()
