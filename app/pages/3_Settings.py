# pages/3_Settings.py
import streamlit as st
from config.config import Config

def render_settings():
    st.title("System Settings")
    
    st.subheader("Twilio Configuration")
    account_sid = st.text_input("Account SID", 
                               value="*" * 10, 
                               type="password")
    auth_token = st.text_input("Auth Token", 
                              value="*" * 10, 
                              type="password")
    phone_number = st.text_input("Twilio Phone Number", 
                                value=Config.TWILIO_PHONE_NUMBER)
    
    if st.button("Save Settings"):
        # Save to .env file
        with open(".env", "w") as f:
            f.write(f"TWILIO_ACCOUNT_SID={account_sid}\n")
            f.write(f"TWILIO_AUTH_TOKEN={auth_token}\n")
            f.write(f"TWILIO_PHONE_NUMBER={phone_number}\n")
        st.success("Settings saved!")
