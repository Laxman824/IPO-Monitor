# # pages/2_Subscribers.py
# import streamlit as st
# from utils.database import Database
# from datetime import datetime

# def render_subscribers():
#     st.title("📱 Subscriber Management")
    
#     # Initialize database
#     db = Database()
    
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
#                     preferences = {
#                         "mainboard": notify_mainboard,
#                         "bse_sme": notify_bse,
#                         "nse_sme": notify_nse,
#                         "gmp_changes": notify_gmp_changes,
#                         "alert_frequency": alert_frequency
#                     }
#                     db.add_subscriber(phone, name, gain_threshold, preferences)
#                     st.success(f"✅ Successfully added {name} to subscribers!")
#                 else:
#                     st.error("Please fill in all required fields!")

#     with col2:
#         st.subheader("Quick Stats")
#         total_subs = len(db.get_subscribers())
#         active_subs = len(db.get_subscribers(active_only=True))
        
#         # Stats in a card-like container
#         with st.container():
#             st.metric("Total Subscribers", total_subs)
#             st.metric("Active Subscribers", active_subs)
#             st.metric("Inactive Subscribers", total_subs - active_subs)
    
#     # Subscriber List
#     st.markdown("---")
#     st.subheader("Current Subscribers")
    
#     # Tabs for Active and Inactive subscribers
#     tab1, tab2 = st.tabs(["Active Subscribers", "Inactive Subscribers"])
    
#     with tab1:
#         active_subscribers = db.get_subscribers(active_only=True)
#         if not active_subscribers.empty:
#             for _, sub in active_subscribers.iterrows():
#                 with st.expander(f"📱 {sub['name']} ({sub['phone']})"):
#                     col1, col2, col3 = st.columns([2,1,1])
#                     with col1:
#                         st.write(f"**Name:** {sub['name']}")
#                         st.write(f"**Phone:** {sub['phone']}")
#                     with col2:
#                         st.write(f"**Threshold:** {sub['gain_threshold']}%")
#                         st.write(f"**Status:** Active")
#                     with col3:
#                         if st.button("Deactivate", key=f"deact_{sub['phone']}"):
#                             db.deactivate_subscriber(sub['phone'])
#                             st.rerun()
#         else:
#             st.info("No active subscribers found")
    
#     with tab2:
#         inactive_subscribers = db.get_subscribers(active_only=False)
#         if not inactive_subscribers.empty:
#             for _, sub in inactive_subscribers.iterrows():
#                 with st.expander(f"📱 {sub['name']} ({sub['phone']})"):
#                     col1, col2, col3 = st.columns([2,1,1])
#                     with col1:
#                         st.write(f"**Name:** {sub['name']}")
#                         st.write(f"**Phone:** {sub['phone']}")
#                     with col2:
#                         st.write(f"**Threshold:** {sub['gain_threshold']}%")
#                         st.write(f"**Status:** Inactive")
#                     with col3:
#                         if st.button("Reactivate", key=f"react_{sub['phone']}"):
#                             db.activate_subscriber(sub['phone'])
#                             st.rerun()
#         else:
#             st.info("No inactive subscribers found")

# if __name__ == "__main__":
#     render_subscribers()
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
from utils.database import Database
from utils.notifications import NotificationManager

def render_subscribers():
    st.title("📱 Subscriber Management")
    
    db = Database()
    notification_manager = NotificationManager()
    
    with st.form("new_subscriber", clear_on_submit=True):
        name = st.text_input("Full Name")
        phone = st.text_input("WhatsApp Number (e.g., +919876543210)")
        
        gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
        alert_frequency = st.selectbox(
            "Alert Frequency",
            ["Immediate", "Daily", "Weekly"]
        )
        
        submitted = st.form_submit_button("Request Subscription")
        if submitted and name and phone:
            preferences = {
                "gain_threshold": gain_threshold,
                "alert_frequency": alert_frequency
            }
            
            # Send approval request to owner
            if notification_manager.send_approval_request(name, phone, preferences):
                # Add to pending subscribers
                if db.add_pending_subscriber(phone, name, preferences):
                    st.success("""✅ Subscription request sent!
                    
                    The owner will review your request and you'll receive a confirmation message on WhatsApp.""")
                else:
                    st.error("Failed to process request. Please try again.")
            else:
                st.error("Failed to send approval request. Please try again.")

    # Show pending subscribers to owner
    if st.session_state.get('is_owner', False):  # Add owner authentication as needed
        st.markdown("---")
        st.subheader("Pending Approvals")
        pending = db.get_subscribers(status='pending')
        if not pending.empty:
            for _, sub in pending.iterrows():
                with st.expander(f"📱 {sub['name']} ({sub['phone']})"):
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.write(f"**Name:** {sub['name']}")
                        st.write(f"**Phone:** {sub['phone']}")
                        st.write(f"**Threshold:** {sub['gain_threshold']}%")
                    with col2:
                        if st.button("Approve", key=f"approve_{sub['phone']}"):
                            if db.approve_subscriber(sub['phone']):
                                notification_manager.notify_subscriber_status(
                                    sub['phone'], sub['name'], approved=True)
                                st.success("Subscriber approved!")
                                st.rerun()
        else:
            st.info("No pending approvals")