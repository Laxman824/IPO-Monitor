# # pages/1_Dashboard.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime
# from utils.scraper import IPOScraper

# def render_dashboard():
#     st.set_page_config(layout="wide")
    
#     # Main title with styling
#     st.markdown("""
#     <div style='text-align: center'>
#         <h1>📈 IPO GMP Monitor Dashboard</h1>
#         <p style='color: gray'>Live IPO Grey Market Premium Tracking</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar filters
#     st.sidebar.header("📊 Filters")
#     gain_threshold = st.sidebar.slider("Minimum Gain %", 0, 100, 50)
#     ipo_type = st.sidebar.multiselect(
#         "IPO Type",
#         ["Mainboard", "NSE SME", "BSE SME"],
#         default=["Mainboard", "NSE SME", "BSE SME"]
#     )
    
#     # Get IPO data
#     df = IPOScraper.scrape_ipo_data()
    
#     if df is not None:
#         # Filter data based on selections
#         filtered_df = df[df['Type'].isin(ipo_type)]
#         high_gain_ipos = filtered_df[filtered_df['Gain'] >= gain_threshold]
        
#         # Top metrics
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric(
#                 "Active IPOs",
#                 len(filtered_df),
#                 delta=f"{len(high_gain_ipos)} High Gain"
#             )
#         with col2:
#             avg_gain = filtered_df['Gain'].mean()
#             st.metric(
#                 "Average Gain",
#                 f"{avg_gain:.1f}%",
#                 delta=f"{avg_gain - 50:.1f}% vs Target"
#             )
#         with col3:
#             max_gain = filtered_df['Gain'].max()
#             st.metric(
#                 "Highest Gain",
#                 f"{max_gain:.1f}%",
#                 delta="Current Best"
#             )
#         with col4:
#             total_subscription = len(filtered_df[filtered_df['Gain'] > 0])
#             st.metric(
#                 "Positive GMP IPOs",
#                 total_subscription,
#                 delta=f"{(total_subscription/len(filtered_df)*100):.1f}%"
#             )
        
#         # Create two columns for charts
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("📊 GMP Distribution by Type")
#             fig1 = px.box(filtered_df, x='Type', y='Gain',
#                          color='Type',
#                          title='IPO Gain Distribution by Category')
#             st.plotly_chart(fig1, use_container_width=True)
        
#         with col2:
#             st.subheader("🎯 Top Performers")
#             top_performers = filtered_df.nlargest(5, 'Gain')
#             fig2 = go.Figure(data=[
#                 go.Bar(
#                     x=top_performers['Current IPOs'],
#                     y=top_performers['Gain'],
#                     marker_color='lightgreen'
#                 )
#             ])
#             fig2.update_layout(title='Top 5 IPOs by Gain %')
#             st.plotly_chart(fig2, use_container_width=True)
        
#         # High Gain IPO Alerts
#         st.subheader("🚨 High Gain IPO Alerts")
#         if not high_gain_ipos.empty:
#             for _, ipo in high_gain_ipos.iterrows():
#                 with st.container():
#                     col1, col2, col3 = st.columns([2,1,1])
#                     with col1:
#                         st.markdown(f"**{ipo['Current IPOs']}**")
#                     with col2:
#                         st.markdown(f"Gain: **{ipo['Gain']}%**")
#                     with col3:
#                         st.markdown(f"Type: *{ipo['Type']}*")
#         else:
#             st.info("No IPOs currently meet the gain threshold criteria")
        
#         # Detailed Data Tables
#         tab1, tab2 = st.tabs(["📈 High Gain IPOs", "📋 All IPOs"])
        
#         with tab1:
#             if not high_gain_ipos.empty:
#                 st.dataframe(
#                     high_gain_ipos,
#                     column_config={
#                         "Current IPOs": "Company",
#                         "IPO GMP": st.column_config.NumberColumn(
#                             "GMP (₹)",
#                             format="₹%d"
#                         ),
#                         "Gain": st.column_config.NumberColumn(
#                             "Gain %",
#                             format="%d%%"
#                         )
#                     },
#                     hide_index=True,
#                     use_container_width=True
#                 )
#             else:
#                 st.info("No high gain IPOs found")
        
#         with tab2:
#             st.dataframe(
#                 filtered_df,
#                 column_config={
#                     "Current IPOs": "Company",
#                     "IPO GMP": st.column_config.NumberColumn(
#                         "GMP (₹)",
#                         format="₹%d"
#                     ),
#                     "Gain": st.column_config.NumberColumn(
#                         "Gain %",
#                         format="%d%%"
#                     )
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
        
#         # Add last updated timestamp
#         st.sidebar.markdown("---")
#         st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     else:
#         st.error("Error fetching IPO data. Please try again later.")

# if __name__ == "__main__":
#     render_dashboard()

# pages/1_Dashboard.py
import streamlit as st
from utils.database import Database
from utils.scraper import IPOScraper
from utils.notifications import NotificationManager
import plotly.express as px
from datetime import datetime

def show_subscriber_form():
    st.subheader("Subscribe to IPO Alerts")
    
    try:
        db = Database()
        notification_manager = NotificationManager()
        
        # Verify Twilio setup first
        verify_result = notification_manager.verify_credentials()
        if verify_result["status"] != "success":
            st.error(f"Twilio setup error: {verify_result['message']}")
            st.info("Please contact administrator to fix the Twilio configuration.")
            return
        
        with st.form("subscriber_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                phone = st.text_input("WhatsApp Number (e.g., +919876543210)")
            with col2:
                gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
                alert_frequency = st.selectbox(
                    "Alert Frequency",
                    ["Immediate", "Daily", "Weekly"]
                )
            
            submitted = st.form_submit_button("Subscribe Now")
            if submitted:
                if not name or not phone:
                    st.error("Please fill in all required fields!")
                    return
                    
                preferences = {
                    "gain_threshold": gain_threshold,
                    "alert_frequency": alert_frequency
                }
                
                # First add to database
                if db.add_subscriber(phone, name, gain_threshold, preferences):
                    welcome_message = f"""Welcome to IPO GMP Monitor! 🎉

Hi {name},

You've been successfully subscribed with:
- Gain Threshold: {gain_threshold}%
- Alert Frequency: {alert_frequency}

You'll receive alerts when IPOs match your criteria.
To stop receiving alerts, reply STOP."""

                    # Send WhatsApp message
                    result = notification_manager.send_whatsapp_message(phone, welcome_message)
                    
                    if result["status"] == "success":
                        st.success("✅ Successfully subscribed! Check your WhatsApp for confirmation.")
                        st.session_state.show_form = False
                    else:
                        st.warning(f"""Added to database but couldn't send WhatsApp message:
                        {result['message']}
                        
                        Please make sure:
                        1. Your phone number is correct
                        2. You've joined the WhatsApp sandbox
                        3. Contact support if the issue persists""")
                else:
                    st.error("Failed to add subscriber to database.")
                    
    except ValueError as ve:
        st.error(f"Configuration Error: {str(ve)}")
        st.info("Please contact administrator to fix the configuration.")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.info("Please try again later or contact support.")

def render_dashboard():
    st.title("📈 IPO GMP Monitor")
    
    # Initialize
    db = Database()
    scraper = IPOScraper()
    
    # Add Subscribe button in sidebar
    with st.sidebar:
        st.markdown("### 📱 IPO Alerts")
        if st.button("Subscribe to Alerts"):
            st.session_state.show_form = True
    
    # Show subscription form in a container if button clicked
    if st.session_state.get('show_form', False):
        with st.expander("📝 Subscription Form", expanded=True):
            show_subscriber_form()
    
    # Get IPO data
    df = scraper.scrape_ipo_data()
    
    if df is not None:
        # Stats Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active IPOs", len(df))
        with col2:
            high_gain = len(df[df['Gain'] >= 50])
            st.metric("High Gain IPOs", high_gain)
        with col3:
            avg_gain = df['Gain'].mean()
            st.metric("Average Gain", f"{avg_gain:.1f}%")
        with col4:
            max_gain = df['Gain'].max()
            st.metric("Highest Gain", f"{max_gain:.1f}%")
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            # GMP Distribution Chart
            fig1 = px.box(df, x='Type', y='Gain',
                         title='IPO Gain Distribution by Category')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Top Performers
            fig2 = px.bar(df.nlargest(5, 'Gain'), 
                         x='Current IPOs', y='Gain',
                         title='Top 5 IPOs by Gain %')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Data Tables
        st.markdown("### 📊 IPO Data")
        tabs = st.tabs(["🔥 High Gain IPOs", "📋 All IPOs"])
        
        with tabs[0]:
            high_gain_ipos = df[df['Gain'] >= 50].sort_values('Gain', ascending=False)
            if not high_gain_ipos.empty:
                st.dataframe(
                    high_gain_ipos,
                    column_config={
                        "Current IPOs": "Company",
                        "IPO GMP": st.column_config.NumberColumn("GMP (₹)", format="₹%d"),
                        "Gain": st.column_config.NumberColumn("Gain %", format="%d%%")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No high gain IPOs currently")
        
        with tabs[1]:
            st.dataframe(
                df,
                column_config={
                    "Current IPOs": "Company",
                    "IPO GMP": st.column_config.NumberColumn("GMP (₹)", format="₹%d"),
                    "Gain": st.column_config.NumberColumn("Gain %", format="%d%%")
                },
                hide_index=True,
                use_container_width=True
            )
            
        # Subscriber Count (if any)
        with st.sidebar:
            subscribers = db.get_subscribers()
            st.metric("Active Subscribers", len(subscribers))
            
        # Last updated timestamp
        st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    else:
        st.error("Error fetching IPO data. Please try again later.")

if __name__ == "__main__":
    render_dashboard()