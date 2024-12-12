# # pages/1_Dashboard.py
# import streamlit as st
# from utils.database import Database
# from utils.scraper import IPOScraper
# from utils.notifications import NotificationManager
# import plotly.express as px
# from datetime import datetime

# def show_subscriber_form():
#     st.subheader("Subscribe to IPO Alerts")
    
#     try:
#         db = Database()
#         notification_manager = NotificationManager()
        
#         # Verify Twilio setup first
#         verify_result = notification_manager.verify_credentials()
#         if verify_result["status"] != "success":
#             st.error(f"Twilio setup error: {verify_result['message']}")
#             st.info("Please contact administrator to fix the Twilio configuration.")
#             return
        
#         with st.form("subscriber_form", clear_on_submit=True):
#             col1, col2 = st.columns(2)
#             with col1:
#                 name = st.text_input("Full Name")
#                 phone = st.text_input("WhatsApp Number (e.g., +919876543210)")
#             with col2:
#                 gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
#                 alert_frequency = st.selectbox(
#                     "Alert Frequency",
#                     ["Immediate", "Daily", "Weekly"]
#                 )
            
#             submitted = st.form_submit_button("Subscribe Now")
#             if submitted:
#                 if not name or not phone:
#                     st.error("Please fill in all required fields!")
#                     return
                    
#                 preferences = {
#                     "gain_threshold": gain_threshold,
#                     "alert_frequency": alert_frequency
#                 }
                
#                 # First add to database
#                 if db.add_subscriber(phone, name, gain_threshold, preferences):
#                     welcome_message = f"""Welcome to IPO GMP Monitor! 🎉

# Hi {name},

# You've been successfully subscribed with:
# - Gain Threshold: {gain_threshold}%
# - Alert Frequency: {alert_frequency}

# You'll receive alerts when IPOs match your criteria.
# To stop receiving alerts, reply STOP."""

#                     # Send WhatsApp message
#                     result = notification_manager.send_whatsapp_message(phone, welcome_message)
                    
#                     if result["status"] == "success":
#                         st.success("✅ Successfully subscribed! Check your WhatsApp for confirmation.")
#                         st.session_state.show_form = False
#                     else:
#                         st.warning(f"""Added to database but couldn't send WhatsApp message:
#                         {result['message']}
                        
#                         Please make sure:
#                         1. Your phone number is correct
#                         2. You've joined the WhatsApp sandbox
#                         3. Contact support if the issue persists""")
#                 else:
#                     st.error("Failed to add subscriber to database.")
                    
#     except ValueError as ve:
#         st.error(f"Configuration Error: {str(ve)}")
#         st.info("Please contact administrator to fix the configuration.")
#     except Exception as e:
#         st.error(f"Unexpected error: {str(e)}")
#         st.info("Please try again later or contact support.")

# def render_dashboard():
#     st.title("📈 IPO GMP Monitor")
    
#     # Initialize
#     db = Database()
#     scraper = IPOScraper()
    
#     # Add Subscribe button in sidebar
#     with st.sidebar:
#         st.markdown("### 📱 IPO Alerts")
#         if st.button("Subscribe to Alerts"):
#             st.session_state.show_form = True
    
#     # Show subscription form in a container if button clicked
#     if st.session_state.get('show_form', False):
#         with st.expander("📝 Subscription Form", expanded=True):
#             show_subscriber_form()
    
#     # Get IPO data
#     df = scraper.scrape_ipo_data()
    
#     if df is not None:
#         # Stats Row
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Active IPOs", len(df))
#         with col2:
#             high_gain = len(df[df['Gain'] >= 50])
#             st.metric("High Gain IPOs", high_gain)
#         with col3:
#             avg_gain = df['Gain'].mean()
#             st.metric("Average Gain", f"{avg_gain:.1f}%")
#         with col4:
#             max_gain = df['Gain'].max()
#             st.metric("Highest Gain", f"{max_gain:.1f}%")
        
#         # Charts Row
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # GMP Distribution Chart
#             fig1 = px.box(df, x='Type', y='Gain',
#                          title='IPO Gain Distribution by Category')
#             st.plotly_chart(fig1, use_container_width=True)
        
#         with col2:
#             # Top Performers
#             fig2 = px.bar(df.nlargest(5, 'Gain'), 
#                          x='Current IPOs', y='Gain',
#                          title='Top 5 IPOs by Gain %')
#             st.plotly_chart(fig2, use_container_width=True)
        
#         # Data Tables
#         st.markdown("### 📊 IPO Data")
#         tabs = st.tabs(["🔥 High Gain IPOs", "📋 All IPOs"])
        
#         with tabs[0]:
#             high_gain_ipos = df[df['Gain'] >= 50].sort_values('Gain', ascending=False)
#             if not high_gain_ipos.empty:
#                 st.dataframe(
#                     high_gain_ipos,
#                     column_config={
#                         "Current IPOs": "Company",
#                         "IPO GMP": st.column_config.NumberColumn("GMP (₹)", format="₹%d"),
#                         "Gain": st.column_config.NumberColumn("Gain %", format="%d%%")
#                     },
#                     hide_index=True,
#                     use_container_width=True
#                 )
#             else:
#                 st.info("No high gain IPOs currently")
        
#         with tabs[1]:
#             st.dataframe(
#                 df,
#                 column_config={
#                     "Current IPOs": "Company",
#                     "IPO GMP": st.column_config.NumberColumn("GMP (₹)", format="₹%d"),
#                     "Gain": st.column_config.NumberColumn("Gain %", format="%d%%")
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
            
#         # Subscriber Count (if any)
#         with st.sidebar:
#             subscribers = db.get_subscribers()
#             st.metric("Active Subscribers", len(subscribers))
            
#         # Last updated timestamp
#         st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
#     else:
#         st.error("Error fetching IPO data. Please try again later.")

# if __name__ == "__main__":
#     render_dashboard()
# pages/1_Dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.database import Database
from utils.scraper import IPOScraper
from utils.notifications import NotificationManager
from datetime import datetime
import time

def set_theme():
    """Configure page theme and layout"""
    # Custom CSS for dark/light mode
    dark_theme = """
    <style>
        .dark-theme {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .metric-card {
            background-color: #2D2D2D;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
    </style>
    """
    
    light_theme = """
    <style>
        .light-theme {
            background-color: #FFFFFF;
            color: #000000;
        }
        .metric-card {
            background-color: #F8F9FA;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
    </style>
    """
    
    st.markdown(dark_theme if st.session_state.get('theme', 'dark') == 'dark' else light_theme, unsafe_allow_html=True)

def show_metrics(df):
    """Display key metrics in a modern card layout"""
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0">Active IPOs</h3>
                <h2 style="color:#4CAF50;margin:0">{}</h2>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
            
    with col2:
        high_gain = len(df[df['Gain'] >= 50])
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0">High Gain IPOs</h3>
                <h2 style="color:#FF6B6B;margin:0">{}</h2>
            </div>
            """.format(high_gain), unsafe_allow_html=True)
            
    with col3:
        avg_gain = df['Gain'].mean()
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0">Average Gain</h3>
                <h2 style="color:#4ECDC4;margin:0">{:.1f}%</h2>
            </div>
            """.format(avg_gain), unsafe_allow_html=True)
            
    with col4:
        max_gain = df['Gain'].max()
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0">Highest Gain</h3>
                <h2 style="color:#FFB900;margin:0">{:.1f}%</h2>
            </div>
            """.format(max_gain), unsafe_allow_html=True)

def create_charts(df):
    """Create interactive visualizations"""
    st.markdown("### 📈 Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GMP Distribution Chart with custom styling
        fig1 = px.box(df, x='Type', y='Gain',
                     title='IPO Gain Distribution by Category',
                     color='Type',
                     color_discrete_sequence=['#4CAF50', '#FF6B6B', '#4ECDC4'])
        
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#666666',
            title_font_size=20,
            showlegend=True,
            title_x=0.5
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Top Performers Chart
        top_performers = df.nlargest(5, 'Gain')
        fig2 = go.Figure(data=[
            go.Bar(
                x=top_performers['Current IPOs'],
                y=top_performers['Gain'],
                marker_color='#4CAF50'
            )
        ])
        
        fig2.update_layout(
            title='Top 5 IPOs by Gain %',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#666666',
            title_font_size=20,
            showlegend=False,
            title_x=0.5
        )
        st.plotly_chart(fig2, use_container_width=True)

# def show_subscriber_form():
#     """Display subscription form with enhanced UI"""
#     st.markdown("### 📱 Subscribe to IPO Alerts")
    
#     db = Database()
#     notification_manager = NotificationManager()
    
#     with st.form("subscriber_form", clear_on_submit=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("Full Name", placeholder="Enter your name")
#             phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
#         with col2:
#             gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
#             alert_frequency = st.selectbox(
#                 "Alert Frequency",
#                 ["Immediate", "Daily", "Weekly"]
#             )
        
#         # Custom styled submit button
#         submitted = st.form_submit_button("Subscribe Now", 
#                                         help="Click to subscribe for IPO alerts")
#         if submitted and name and phone:
#             # Process subscription...
#             pass
def show_subscriber_form():
    st.markdown("### 📱 Subscribe to IPO Alerts")
    
    db = Database()
    notification_manager = NotificationManager()
    
    # Request push notification permission
    notification_manager.request_push_permission()
    
    with st.form("subscriber_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your name")
            phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
        with col2:
            gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
            alert_frequency = st.selectbox(
                "Alert Frequency",
                ["Immediate", "Daily", "Weekly"]
            )
            
        # Notification preferences
        st.write("Notification Preferences")
        col1, col2 = st.columns(2)
        with col1:
            enable_whatsapp = st.checkbox("WhatsApp Notifications", value=True)
            enable_push = st.checkbox("Browser Push Notifications", value=True)
        with col2:
            st.info("Browser notifications will appear on your desktop/mobile")
        
        submitted = st.form_submit_button("Subscribe Now")
        if submitted and name and phone:
            preferences = {
                "gain_threshold": gain_threshold,
                "alert_frequency": alert_frequency,
                "notifications": {
                    "whatsapp": enable_whatsapp,
                    "push": enable_push
                }
            }
            
            try:
                # Add subscriber to database
                subscriber_id = db.add_subscriber(phone, name, gain_threshold, preferences)
                
                if subscriber_id:
                    success_messages = []
                    error_messages = []
                    
                    # Send welcome notifications based on preferences
                    if enable_whatsapp:
                        whatsapp_result = notification_manager.send_whatsapp_message(
                            phone,
                            f"Welcome to IPO GMP Monitor, {name}! You'll receive alerts when IPOs match your criteria."
                        )
                        if whatsapp_result['status'] == 'success':
                            success_messages.append("✅ WhatsApp notifications enabled")
                        else:
                            error_messages.append(f"❌ WhatsApp setup failed: {whatsapp_result['message']}")
                    
                    if enable_push:
                        push_result = notification_manager.send_push_notification(
                            "Welcome to IPO Monitor!",
                            f"Hi {name}, you'll receive alerts for IPOs with {gain_threshold}%+ gains.",
                            subscriber_id
                        )
                        if push_result['status'] == 'success':
                            success_messages.append("✅ Browser notifications enabled")
                        else:
                            error_messages.append(f"❌ Browser notifications failed: {push_result['message']}")
                    
                    # Show results
                    if success_messages:
                        st.success("\n".join(success_messages))
                    if error_messages:
                        st.warning("\n".join(error_messages))
                        
                    st.session_state.show_form = False
                    
                else:
                    st.error("Failed to add subscriber to database.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please try again or contact support.")
def render_dashboard():
    st.set_page_config(page_title="IPO Monitor", 
                      page_icon="📈",
                      layout="wide",
                      initial_sidebar_state="expanded")
    
    # Theme selector in sidebar
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        theme = st.radio("Choose Theme", ['Light', 'Dark'], 
                        index=0 if st.session_state.get('theme', 'dark') == 'light' else 1)
        st.session_state.theme = theme.lower()
    
    set_theme()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1>📈 IPO GMP Monitor</h1>
        <p style="color: #666;">Real-time IPO Grey Market Premium Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize
    scraper = IPOScraper()
    
    # Auto-refresh functionality
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Add refresh button and auto-refresh option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        if st.button('🔄 Refresh Data'):
            st.session_state.last_refresh = time.time()
            st.experimental_rerun()
    
    # Get data
    df = scraper.scrape_ipo_data()
    
    if df is not None:
        # Show metrics
        show_metrics(df)
        
        # Show charts
        create_charts(df)
        
        # Data Tables with tabs
        st.markdown("### 📋 IPO Details")
        tabs = st.tabs(["🔥 High Gain IPOs", "📋 All IPOs", "📊 Analysis"])
        
        with tabs[0]:
            high_gain_ipos = df[df['Gain'] >= 50].sort_values('Gain', ascending=False)
            if not high_gain_ipos.empty:
                st.dataframe(high_gain_ipos, use_container_width=True)
            else:
                st.info("No high gain IPOs currently")
        
        with tabs[1]:
            st.dataframe(df, use_container_width=True)
            
        with tabs[2]:
            # Additional analysis tab
            col1, col2 = st.columns(2)
            with col1:
                st.write("IPO Type Distribution")
                type_dist = df['Type'].value_counts()
                fig = px.pie(values=type_dist.values, 
                           names=type_dist.index,
                           title="IPO Distribution by Type")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("Gain Range Distribution")
                fig = px.histogram(df, x='Gain',
                                 nbins=20,
                                 title="Distribution of IPO Gains")
                st.plotly_chart(fig, use_container_width=True)
        
        # Subscription form
        if st.sidebar.button("📱 Subscribe to Alerts"):
            st.session_state.show_form = True
        
        if st.session_state.get('show_form', False):
            show_subscriber_form()
            
    else:
        st.error("Error fetching IPO data. Please try again later.")
        
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <p style="color: #666;">Made with ❤️ by Your Company</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()