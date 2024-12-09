# pages/2_Subscribers.py
import streamlit as st
from utils.database import Database

def render_subscribers():
    st.title("Subscriber Management")
    db = Database()
    
    # Add new subscriber
    with st.expander("Add New Subscriber", expanded=True):
        with st.form("new_subscriber"):
            name = st.text_input("Name")
            phone = st.text_input("Phone Number (with country code)")
            threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
            
            submitted = st.form_submit_button("Add Subscriber")
            if submitted and name and phone:
                db.add_subscriber(phone, name, threshold)
                st.success("Subscriber added successfully!")
    
    # View subscribers
    st.subheader("Current Subscribers")
    subscribers = db.get_subscribers()
    if not subscribers.empty:
        st.dataframe(subscribers)
        
        # Deactivate subscriber
        with st.expander("Deactivate Subscriber"):
            phone = st.selectbox("Select subscriber to deactivate",
                               subscribers['phone'].tolist())
            if st.button("Deactivate"):
                db.deactivate_subscriber(phone)
                st.success("Subscriber deactivated!")
                st.rerun()
    else:
        st.info("No active subscribers")
