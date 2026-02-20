
# # # pages/1_Dashboard.py
# # import streamlit as st
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from utils.database import Database
# # from utils.scraper import IPOScraper
# # from utils.notifications import NotificationManager
# # from datetime import datetime
# # import time

# # def set_theme():
# #     """Configure page theme and layout"""
# #     # Custom CSS for dark/light mode
# #     dark_theme = """
# #     <style>
# #         .dark-theme {
# #             background-color: #1E1E1E;
# #             color: #FFFFFF;
# #         }
# #         .metric-card {
# #             background-color: #2D2D2D;
# #             padding: 1rem;
# #             border-radius: 0.5rem;
# #             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# #         }
# #         .stButton>button {
# #             background-color: #4CAF50;
# #             color: white;
# #             border: none;
# #             border-radius: 4px;
# #             padding: 0.5rem 1rem;
# #         }
# #     </style>
# #     """
    
# #     light_theme = """
# #     <style>
# #         .light-theme {
# #             background-color: #FFFFFF;
# #             color: #000000;
# #         }
# #         .metric-card {
# #             background-color: #F8F9FA;
# #             padding: 1rem;
# #             border-radius: 0.5rem;
# #             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# #         }
# #         .stButton>button {
# #             background-color: #4CAF50;
# #             color: white;
# #             border: none;
# #             border-radius: 4px;
# #             padding: 0.5rem 1rem;
# #         }
# #     </style>
# #     """
    
# #     st.markdown(dark_theme if st.session_state.get('theme', 'dark') == 'dark' else light_theme, unsafe_allow_html=True)

# # def show_metrics(df):
# #     """Display key metrics in a modern card layout"""
# #     st.markdown("### 📊 Key Metrics")
    
# #     col1, col2, col3, col4 = st.columns(4)
# #     with col1:
# #         with st.container():
# #             st.markdown("""
# #             <div class="metric-card">
# #                 <h3 style="margin:0">Active IPOs</h3>
# #                 <h2 style="color:#4CAF50;margin:0">{}</h2>
# #             </div>
# #             """.format(len(df)), unsafe_allow_html=True)
            
# #     with col2:
# #         high_gain = len(df[df['Gain'] >= 50])
# #         with st.container():
# #             st.markdown("""
# #             <div class="metric-card">
# #                 <h3 style="margin:0">High Gain IPOs</h3>
# #                 <h2 style="color:#FF6B6B;margin:0">{}</h2>
# #             </div>
# #             """.format(high_gain), unsafe_allow_html=True)
            
# #     with col3:
# #         avg_gain = df['Gain'].mean()
# #         with st.container():
# #             st.markdown("""
# #             <div class="metric-card">
# #                 <h3 style="margin:0">Average Gain</h3>
# #                 <h2 style="color:#4ECDC4;margin:0">{:.1f}%</h2>
# #             </div>
# #             """.format(avg_gain), unsafe_allow_html=True)
            
# #     with col4:
# #         max_gain = df['Gain'].max()
# #         with st.container():
# #             st.markdown("""
# #             <div class="metric-card">
# #                 <h3 style="margin:0">Highest Gain</h3>
# #                 <h2 style="color:#FFB900;margin:0">{:.1f}%</h2>
# #             </div>
# #             """.format(max_gain), unsafe_allow_html=True)

# # def create_charts(df):
# #     """Create interactive visualizations"""
# #     st.markdown("### 📈 Market Analysis")
    
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         # GMP Distribution Chart with custom styling
# #         fig1 = px.box(df, x='Type', y='Gain',
# #                      title='IPO Gain Distribution by Category',
# #                      color='Type',
# #                      color_discrete_sequence=['#4CAF50', '#FF6B6B', '#4ECDC4'])
        
# #         fig1.update_layout(
# #             plot_bgcolor='rgba(0,0,0,0)',
# #             paper_bgcolor='rgba(0,0,0,0)',
# #             font_color='#666666',
# #             title_font_size=20,
# #             showlegend=True,
# #             title_x=0.5
# #         )
# #         st.plotly_chart(fig1, use_container_width=True)
    
# #     with col2:
# #         # Top Performers Chart
# #         top_performers = df.nlargest(5, 'Gain')
# #         fig2 = go.Figure(data=[
# #             go.Bar(
# #                 x=top_performers['Current IPOs'],
# #                 y=top_performers['Gain'],
# #                 marker_color='#4CAF50'
# #             )
# #         ])
        
# #         fig2.update_layout(
# #             title='Top 5 IPOs by Gain %',
# #             plot_bgcolor='rgba(0,0,0,0)',
# #             paper_bgcolor='rgba(0,0,0,0)',
# #             font_color='#666666',
# #             title_font_size=20,
# #             showlegend=False,
# #             title_x=0.5
# #         )
# #         st.plotly_chart(fig2, use_container_width=True)

# # # def show_subscriber_form():
# # #     """Display subscription form with enhanced UI"""
# # #     st.markdown("### 📱 Subscribe to IPO Alerts")
    
# # #     db = Database()
# # #     notification_manager = NotificationManager()
    
# # #     with st.form("subscriber_form", clear_on_submit=True):
# # #         col1, col2 = st.columns(2)
# # #         with col1:
# # #             name = st.text_input("Full Name", placeholder="Enter your name")
# # #             phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
# # #         with col2:
# # #             gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
# # #             alert_frequency = st.selectbox(
# # #                 "Alert Frequency",
# # #                 ["Immediate", "Daily", "Weekly"]
# # #             )
        
# # #         # Custom styled submit button
# # #         submitted = st.form_submit_button("Subscribe Now", 
# # #                                         help="Click to subscribe for IPO alerts")
# # #         if submitted and name and phone:
# # #             # Process subscription...
# # #             pass
# # def show_subscriber_form():
# #     st.markdown("### 📱 Subscribe to IPO Alerts")
    
# #     db = Database()
# #     notification_manager = NotificationManager()
    
# #     # Request push notification permission
# #     notification_manager.request_push_permission()
    
# #     with st.form("subscriber_form", clear_on_submit=True):
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             name = st.text_input("Full Name", placeholder="Enter your name")
# #             phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
# #         with col2:
# #             gain_threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
# #             alert_frequency = st.selectbox(
# #                 "Alert Frequency",
# #                 ["Immediate", "Daily", "Weekly"]
# #             )
            
# #         # Notification preferences
# #         st.write("Notification Preferences")
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             enable_whatsapp = st.checkbox("WhatsApp Notifications", value=True)
# #             enable_push = st.checkbox("Browser Push Notifications", value=True)
# #         with col2:
# #             st.info("Browser notifications will appear on your desktop/mobile")
        
# #         submitted = st.form_submit_button("Subscribe Now")
# #         if submitted and name and phone:
# #             preferences = {
# #                 "gain_threshold": gain_threshold,
# #                 "alert_frequency": alert_frequency,
# #                 "notifications": {
# #                     "whatsapp": enable_whatsapp,
# #                     "push": enable_push
# #                 }
# #             }
            
# #             try:
# #                 # Add subscriber to database
# #                 subscriber_id = db.add_subscriber(phone, name, gain_threshold, preferences)
                
# #                 if subscriber_id:
# #                     success_messages = []
# #                     error_messages = []
                    
# #                     # Send welcome notifications based on preferences
# #                     if enable_whatsapp:
# #                         whatsapp_result = notification_manager.send_whatsapp_message(
# #                             phone,
# #                             f"Welcome to IPO GMP Monitor, {name}! You'll receive alerts when IPOs match your criteria."
# #                         )
# #                         if whatsapp_result['status'] == 'success':
# #                             success_messages.append("✅ WhatsApp notifications enabled")
# #                         else:
# #                             error_messages.append(f"❌ WhatsApp setup failed: {whatsapp_result['message']}")
                    
# #                     if enable_push:
# #                         push_result = notification_manager.send_push_notification(
# #                             "Welcome to IPO Monitor!",
# #                             f"Hi {name}, you'll receive alerts for IPOs with {gain_threshold}%+ gains.",
# #                             subscriber_id
# #                         )
# #                         if push_result['status'] == 'success':
# #                             success_messages.append("✅ Browser notifications enabled")
# #                         else:
# #                             error_messages.append(f"❌ Browser notifications failed: {push_result['message']}")
                    
# #                     # Show results
# #                     if success_messages:
# #                         st.success("\n".join(success_messages))
# #                     if error_messages:
# #                         st.warning("\n".join(error_messages))
                        
# #                     st.session_state.show_form = False
                    
# #                 else:
# #                     st.error("Failed to add subscriber to database.")
# #             except Exception as e:
# #                 st.error(f"Error: {str(e)}")
# #                 st.info("Please try again or contact support.")
# # def render_dashboard():
# #     st.set_page_config(page_title="IPO Monitor", 
# #                       page_icon="📈",
# #                       layout="wide",
# #                       initial_sidebar_state="expanded")
    
# #     # Theme selector in sidebar
# #     with st.sidebar:
# #         st.markdown("### 🎨 Theme Settings")
# #         theme = st.radio("Choose Theme", ['Light', 'Dark'], 
# #                         index=0 if st.session_state.get('theme', 'dark') == 'light' else 1)
# #         st.session_state.theme = theme.lower()
    
# #     set_theme()
    
# #     # Header
# #     st.markdown("""
# #     <div style="text-align: center; padding: 1rem;">
# #         <h1>📈 IPO GMP Monitor</h1>
# #         <p style="color: #666;">Real-time IPO Grey Market Premium Tracking</p>
# #     </div>
# #     """, unsafe_allow_html=True)
    
# #     # Initialize
# #     scraper = IPOScraper()
    
# #     # Auto-refresh functionality
# #     if 'last_refresh' not in st.session_state:
# #         st.session_state.last_refresh = time.time()
    
# #     # Add refresh button and auto-refresh option
# #     col1, col2 = st.columns([3, 1])
# #     with col1:
# #         st.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# #     with col2:
# #         if st.button('🔄 Refresh Data'):
# #             st.session_state.last_refresh = time.time()
# #             st.experimental_rerun()
    
# #     # Get data
# #     df = scraper.scrape_ipo_data()
    
# #     if df is not None:
# #         # Show metrics
# #         show_metrics(df)
        
# #         # Show charts
# #         create_charts(df)
        
# #         # Data Tables with tabs
# #         st.markdown("### 📋 IPO Details")
# #         tabs = st.tabs(["🔥 High Gain IPOs", "📋 All IPOs", "📊 Analysis"])
        
# #         with tabs[0]:
# #             high_gain_ipos = df[df['Gain'] >= 50].sort_values('Gain', ascending=False)
# #             if not high_gain_ipos.empty:
# #                 st.dataframe(high_gain_ipos, use_container_width=True)
# #             else:
# #                 st.info("No high gain IPOs currently")
        
# #         with tabs[1]:
# #             st.dataframe(df, use_container_width=True)
            
# #         with tabs[2]:
# #             # Additional analysis tab
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 st.write("IPO Type Distribution")
# #                 type_dist = df['Type'].value_counts()
# #                 fig = px.pie(values=type_dist.values, 
# #                            names=type_dist.index,
# #                            title="IPO Distribution by Type")
# #                 st.plotly_chart(fig, use_container_width=True)
            
# #             with col2:
# #                 st.write("Gain Range Distribution")
# #                 fig = px.histogram(df, x='Gain',
# #                                  nbins=20,
# #                                  title="Distribution of IPO Gains")
# #                 st.plotly_chart(fig, use_container_width=True)
        
# #         # Subscription form
# #         if st.sidebar.button("📱 Subscribe to Alerts"):
# #             st.session_state.show_form = True
        
# #         if st.session_state.get('show_form', False):
# #             show_subscriber_form()
            
# #     else:
# #         st.error("Error fetching IPO data. Please try again later.")
        
# #     # Footer
# #     st.markdown("""
# #     <div style="text-align: center; padding: 2rem;">
# #         <p style="color: #666;">Made with ❤️ by Laxman</p>
# #     </div>
# #     """, unsafe_allow_html=True)

# # if __name__ == "__main__":
# #     render_dashboard()


# # pages/1_Dashboard.py
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from utils.database import Database
# from utils.scraper import IPOScraper
# from utils.notifications import NotificationManager
# from datetime import datetime

# # ── Page config ─────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Dashboard | IPO Monitor",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ── Theme CSS (matches main.py) ────────────────────────────────────
# def inject_dashboard_css():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#     #MainMenu, header, footer, .stDeployButton { display: none !important; }

#     .dash-hero {
#         background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
#         border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem;
#         text-align: center; border: 1px solid rgba(255,255,255,.06);
#     }
#     .dash-hero h1 {
#         font-size: 2.2rem; font-weight: 900;
#         background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
#         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#         margin: 0;
#     }
#     .dash-hero p { color: #94a3b8; margin: .3rem 0 0; }

#     .metric-card {
#         background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
#         border: 1px solid rgba(255,255,255,.06);
#         border-radius: 16px; padding: 1.5rem; text-align: center;
#         transition: transform .2s, box-shadow .2s;
#     }
#     .metric-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 12px 40px rgba(99,102,241,.15);
#     }
#     .metric-icon { font-size: 1.6rem; }
#     .metric-value {
#         font-size: 2rem; font-weight: 800;
#         background: linear-gradient(90deg, #a78bfa, #60a5fa);
#         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     }
#     .metric-label { color: #94a3b8; font-size: .85rem; }

#     .section-title {
#         font-size: 1.3rem; font-weight: 700; color: #e2e8f0;
#         margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: .5rem;
#     }
#     .section-title .line {
#         flex: 1; height: 1px;
#         background: linear-gradient(90deg, rgba(99,102,241,.4), transparent);
#     }

#     .ipo-row {
#         background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
#         border: 1px solid rgba(255,255,255,.06);
#         border-radius: 14px; padding: 1rem 1.3rem; margin-bottom: .6rem;
#         display: flex; align-items: center; justify-content: space-between;
#         transition: all .2s;
#     }
#     .ipo-row:hover {
#         border-color: rgba(99,102,241,.35);
#         transform: translateX(4px);
#     }
#     .ipo-row .name { font-weight: 600; color: #e2e8f0; font-size: 1rem; }
#     .ipo-row .meta { color: #64748b; font-size: .8rem; }
#     .gain-pill {
#         font-weight: 700; font-size: 1rem; padding: 5px 14px;
#         border-radius: 10px; min-width: 72px; text-align: center;
#     }
#     .gp { background: rgba(34,197,94,.12); color: #22c55e; }
#     .gn { background: rgba(239,68,68,.12); color: #ef4444; }
#     .gz { background: rgba(234,179,8,.12); color: #eab308; }

#     .badge-main { background: rgba(99,102,241,.18); color: #a78bfa;
#                    font-size:.7rem; padding:2px 8px; border-radius:20px; font-weight:600; }
#     .badge-sme  { background: rgba(52,211,153,.15); color: #34d399;
#                    font-size:.7rem; padding:2px 8px; border-radius:20px; font-weight:600; }

#     .app-footer {
#         text-align: center; color: #475569; font-size: .78rem;
#         padding: 2rem 0 1rem; border-top: 1px solid rgba(255,255,255,.04);
#         margin-top: 3rem;
#     }

#     /* Plotly dark overrides */
#     .js-plotly-plot .plotly .modebar { display: none !important; }
#     </style>
#     """, unsafe_allow_html=True)


# PLOTLY_LAYOUT = dict(
#     plot_bgcolor="rgba(0,0,0,0)",
#     paper_bgcolor="rgba(0,0,0,0)",
#     font=dict(color="#94a3b8", family="Inter"),
#     title_font=dict(size=18, color="#e2e8f0"),
#     title_x=0.5,
#     margin=dict(l=40, r=40, t=60, b=40),
#     legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
#     xaxis=dict(gridcolor="rgba(255,255,255,.04)"),
#     yaxis=dict(gridcolor="rgba(255,255,255,.04)"),
# )

# COLORS = ["#a78bfa", "#60a5fa", "#34d399", "#f472b6", "#fbbf24", "#fb923c"]


# # ── Main ────────────────────────────────────────────────────────────
# def render_dashboard():
#     inject_dashboard_css()

#     # ── Sidebar ──────────────────────────────────────────────────
#     with st.sidebar:
#         st.markdown("## 📊 Dashboard")
#         st.caption("Full analytics & management")
#         st.markdown("---")

#         st.markdown("### 🎛️ Filters")
#         filter_type = st.multiselect(
#             "IPO Type", ["Mainline", "SME"], default=["Mainline", "SME"]
#         )
#         gain_range = st.slider("Gain % Range", -100, 300, (-100, 300), step=5)
#         sort_option = st.selectbox(
#             "Sort by", ["Gain ↓", "Gain ↑", "Name A-Z", "Name Z-A"]
#         )

#         st.markdown("---")
#         if st.button("🔄 Force Refresh", use_container_width=True):
#             st.cache_data.clear()
#             st.rerun()

#         st.markdown("---")
#         st.markdown("### 📱 Quick Actions")
#         show_subscribe = st.toggle("Show Subscribe Form", value=False)

#     # ── Hero ─────────────────────────────────────────────────────
#     st.markdown(f"""
#     <div class="dash-hero">
#         <h1>📊 IPO Dashboard</h1>
#         <p>Comprehensive IPO analytics &amp; monitoring • {datetime.now().strftime('%d %b %Y  •  %I:%M %p')}</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Load data ────────────────────────────────────────────────
#     @st.cache_data(ttl=300, show_spinner=False)
#     def load_data():
#         scraper = IPOScraper()
#         return scraper.scrape_ipo_data()

#     with st.spinner("Loading IPO data…"):
#         df = load_data()

#     if df is None or df.empty:
#         st.error("❌ Unable to fetch IPO data. Please try refreshing.")
#         with st.expander("🔧 Troubleshooting"):
#             st.markdown("""
#             - Check your internet connection
#             - The source website may be down
#             - Try the **Force Refresh** button in the sidebar
#             """)
#         return

#     # ── Apply filters ────────────────────────────────────────────
#     if "Type" in df.columns:
#         df = df[df["Type"].isin(filter_type)]
#     df = df[(df["Gain"] >= gain_range[0]) & (df["Gain"] <= gain_range[1])]

#     if sort_option == "Gain ↓":
#         df = df.sort_values("Gain", ascending=False)
#     elif sort_option == "Gain ↑":
#         df = df.sort_values("Gain", ascending=True)
#     elif sort_option == "Name A-Z":
#         df = df.sort_values("Current IPOs")
#     else:
#         df = df.sort_values("Current IPOs", ascending=False)

#     # ── Save snapshot ────────────────────────────────────────────
#     try:
#         db = Database()
#         db.save_ipo_snapshot(df)
#     except Exception:
#         pass

#     # ── Metrics ──────────────────────────────────────────────────
#     _render_metrics(df)

#     # ── Charts ───────────────────────────────────────────────────
#     _render_charts(df)

#     # ── Data tables ──────────────────────────────────────────────
#     _render_data_tabs(df)

#     # ── Subscribe form ───────────────────────────────────────────
#     if show_subscribe:
#         _render_subscribe_form()

#     # ── Footer ───────────────────────────────────────────────────
#     st.markdown("""
#     <div class="app-footer">
#         Built with ❤️ using Streamlit • Data sourced from public IPO trackers
#     </div>
#     """, unsafe_allow_html=True)


# # ── Metrics ─────────────────────────────────────────────────────────
# def _render_metrics(df):
#     active = len(df)
#     high = int((df["Gain"] >= 50).sum())
#     avg = df["Gain"].mean()
#     mx = df["Gain"].max()
#     neg = int((df["Gain"] < 0).sum())
#     best = df.loc[df["Gain"].idxmax(), "Current IPOs"] if not df.empty else "—"

#     cols = st.columns(5)
#     data = [
#         ("🚀", active, "Active IPOs"),
#         ("🔥", high, "High Gain ≥50%"),
#         ("📊", f"{avg:+.1f}%", "Avg Gain"),
#         ("🏆", f"{mx:+.1f}%", best[:16]),
#         ("📉", neg, "Negative GMP"),
#     ]
#     for col, (icon, val, label) in zip(cols, data):
#         with col:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-icon">{icon}</div>
#                 <div class="metric-value">{val}</div>
#                 <div class="metric-label">{label}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("")


# # ── Charts ──────────────────────────────────────────────────────────
# def _render_charts(df):
#     st.markdown(
#         '<div class="section-title">📈 Market Analysis <span class="line"></span></div>',
#         unsafe_allow_html=True,
#     )

#     tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Top Performers", "📉 Distribution"])

#     with tab1:
#         c1, c2 = st.columns(2)
#         with c1:
#             # Horizontal bar chart
#             sorted_df = df.sort_values("Gain", ascending=True).tail(10)
#             fig = go.Figure(go.Bar(
#                 x=sorted_df["Gain"],
#                 y=sorted_df["Current IPOs"],
#                 orientation="h",
#                 marker=dict(
#                     color=sorted_df["Gain"],
#                     colorscale=[[0, "#ef4444"], [0.5, "#eab308"], [1, "#22c55e"]],
#                     line=dict(width=0),
#                     # cornerradius=6,
#                 ),
#                 text=sorted_df["Gain"].apply(lambda g: f"{g:+.1f}%"),
#                 textposition="outside",
#                 textfont=dict(color="#94a3b8", size=11),
#             ))
#             fig.update_layout(
#                 **PLOTLY_LAYOUT,
#                 title="Top 10 IPOs by Gain %",
#                 xaxis_title="Gain %",
#                 yaxis_title="",
#                 height=420,
#             )
#             st.plotly_chart(fig, use_container_width=True)

#         with c2:
#             # Pie by type
#             type_counts = df["Type"].value_counts()
#             fig2 = go.Figure(go.Pie(
#                 labels=type_counts.index,
#                 values=type_counts.values,
#                 hole=0.55,
#                 marker=dict(colors=COLORS[:len(type_counts)]),
#                 textinfo="label+percent",
#                 textfont=dict(color="#e2e8f0"),
#             ))
#             fig2.update_layout(
#                 **PLOTLY_LAYOUT,
#                 title="IPO Type Distribution",
#                 height=420,
#                 showlegend=False,
#             )
#             st.plotly_chart(fig2, use_container_width=True)

#     with tab2:
#         top5 = df.nlargest(5, "Gain")
#         medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
#         cols = st.columns(min(5, len(top5)))
#         for i, (_, row) in enumerate(top5.iterrows()):
#             with cols[i]:
#                 g = row["Gain"]
#                 color = "#22c55e" if g > 0 else "#ef4444"
#                 st.markdown(f"""
#                 <div class="metric-card" style="padding:1.2rem;">
#                     <div style="font-size:2rem;">{medals[i]}</div>
#                     <div style="font-weight:700;color:#e2e8f0;margin:.4rem 0;font-size:.9rem;">
#                         {row['Current IPOs'][:20]}
#                     </div>
#                     <div style="font-size:1.5rem;font-weight:800;color:{color};">
#                         {g:+.1f}%
#                     </div>
#                     <div style="color:#64748b;font-size:.75rem;margin-top:.2rem;">
#                         {row.get('Date','—')}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#     with tab3:
#         c1, c2 = st.columns(2)
#         with c1:
#             fig3 = px.histogram(
#                 df, x="Gain", nbins=25,
#                 color_discrete_sequence=["#a78bfa"],
#                 title="Gain Distribution",
#             )
#             fig3.update_layout(**PLOTLY_LAYOUT, height=380)
#             st.plotly_chart(fig3, use_container_width=True)

#         with c2:
#             if "Type" in df.columns and df["Type"].nunique() > 1:
#                 fig4 = px.box(
#                     df, x="Type", y="Gain",
#                     color="Type",
#                     color_discrete_sequence=COLORS,
#                     title="Gain by Category",
#                 )
#                 fig4.update_layout(**PLOTLY_LAYOUT, height=380, showlegend=False)
#                 st.plotly_chart(fig4, use_container_width=True)
#             else:
#                 fig4 = px.violin(
#                     df, y="Gain",
#                     color_discrete_sequence=["#60a5fa"],
#                     title="Gain Spread",
#                     box=True,
#                 )
#                 fig4.update_layout(**PLOTLY_LAYOUT, height=380)
#                 st.plotly_chart(fig4, use_container_width=True)


# # ── Data tabs ───────────────────────────────────────────────────────
# def _render_data_tabs(df):
#     st.markdown(
#         '<div class="section-title">📋 IPO Details <span class="line"></span></div>',
#         unsafe_allow_html=True,
#     )

#     t1, t2, t3 = st.tabs(["🔥 High Gain", "📋 All IPOs", "📉 Negative GMP"])

#     with t1:
#         hg = df[df["Gain"] >= 50].sort_values("Gain", ascending=False)
#         if not hg.empty:
#             _render_ipo_cards(hg)
#         else:
#             st.info("No IPOs with ≥50% gain currently.")

#     with t2:
#         search = st.text_input("🔍 Search", placeholder="Type IPO name…",
#                                label_visibility="collapsed", key="dash_search")
#         filtered = df
#         if search:
#             filtered = df[df["Current IPOs"].str.contains(search, case=False, na=False)]
#         _render_ipo_cards(filtered)

#         with st.expander("📄 Raw Data Table"):
#             st.dataframe(
#                 filtered.style.format({"Gain": "{:+.1f}%"})
#                 .background_gradient(subset=["Gain"], cmap="RdYlGn"),
#                 use_container_width=True,
#                 hide_index=True,
#             )

#     with t3:
#         neg = df[df["Gain"] < 0].sort_values("Gain")
#         if not neg.empty:
#             _render_ipo_cards(neg)
#         else:
#             st.success("🎉 No IPOs with negative GMP right now!")


# def _render_ipo_cards(df):
#     """Render IPO data as styled card rows."""
#     if df.empty:
#         return

#     max_abs = max(abs(df["Gain"].max()), abs(df["Gain"].min()), 1)
#     html = ""
#     for _, row in df.iterrows():
#         name = row.get("Current IPOs", "—")
#         gain = row.get("Gain", 0)
#         date = row.get("Date", "—")
#         t = row.get("Type", "Mainline")

#         badge_cls = "badge-sme" if t == "SME" else "badge-main"
#         if gain > 0:
#             gc, gt = "gp", f"+{gain:.1f}%"
#         elif gain < 0:
#             gc, gt = "gn", f"{gain:.1f}%"
#         else:
#             gc, gt = "gz", "0.0%"

#         bar_w = min(abs(gain) / max_abs * 100, 100)
#         bar_c = "#22c55e" if gain > 0 else "#ef4444" if gain < 0 else "#eab308"

#         html += f"""
#         <div class="ipo-row">
#             <div>
#                 <div class="name">{name}</div>
#                 <div class="meta">
#                     {date} &nbsp;<span class="{badge_cls}">{t}</span>
#                 </div>
#                 <div style="background:rgba(255,255,255,.06);border-radius:4px;
#                             height:6px;width:140px;margin-top:4px;overflow:hidden;">
#                     <div style="height:100%;width:{bar_w}%;background:{bar_c};
#                                 border-radius:4px;transition:width .5s;"></div>
#                 </div>
#             </div>
#             <div class="gain-pill {gc}">{gt}</div>
#         </div>
#         """
#     st.markdown(html, unsafe_allow_html=True)


# # ── Subscribe form ──────────────────────────────────────────────────
# def _render_subscribe_form():
#     st.markdown(
#         '<div class="section-title">📱 Subscribe to Alerts <span class="line"></span></div>',
#         unsafe_allow_html=True,
#     )

#     db = Database()
#     nm = NotificationManager()
#     nm.request_push_permission()

#     with st.form("dash_subscribe", clear_on_submit=True):
#         c1, c2 = st.columns(2)
#         with c1:
#             name = st.text_input("Full Name", placeholder="Your name")
#             phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
#         with c2:
#             threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
#             frequency = st.selectbox("Alert Frequency", ["Immediate", "Daily", "Weekly"])

#         st.markdown("**Notification Channels**")
#         nc1, nc2 = st.columns(2)
#         with nc1:
#             wa = st.checkbox("WhatsApp", value=True)
#             push = st.checkbox("Browser Push", value=True)
#         with nc2:
#             st.info("Enable channels to receive IPO alerts")

#         submitted = st.form_submit_button("🚀 Subscribe Now", use_container_width=True)

#         if submitted:
#             if not name or not phone:
#                 st.error("Please fill in name and phone number.")
#                 return

#             prefs = {
#                 "gain_threshold": threshold,
#                 "alert_frequency": frequency,
#                 "notifications": {"whatsapp": wa, "push": push},
#             }
#             result = db.add_subscriber(phone, name, threshold, prefs)

#             if result:
#                 st.success(f"✅ Welcome, {name}! You're now subscribed.")
#                 st.balloons()

#                 if wa:
#                     r = nm.send_whatsapp_message(
#                         phone,
#                         f"Welcome to IPO GMP Monitor, {name}! "
#                         f"You'll get alerts for IPOs with {threshold}%+ gains.",
#                     )
#                     if r["status"] == "success":
#                         st.toast("✅ WhatsApp connected!", icon="📱")
#                     else:
#                         st.toast(f"⚠️ WhatsApp: {r['message']}", icon="⚠️")
#             else:
#                 st.error("Failed to subscribe. Please try again.")


# # ── Entry point ─────────────────────────────────────────────────────
# render_dashboard()

# pages/1_Dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.database import Database
from utils.scraper import IPOScraper
from utils.notifications import NotificationManager
from datetime import datetime

# ── Page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard | IPO Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Theme CSS ──────────────────────────────────────────────────────
def inject_dashboard_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, header, footer, .stDeployButton { display: none !important; }

    .dash-hero {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem;
        text-align: center; border: 1px solid rgba(255,255,255,.06);
    }
    .dash-hero h1 {
        font-size: 2.2rem; font-weight: 900;
        background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .dash-hero p { color: #94a3b8; margin: .3rem 0 0; }

    .metric-card {
        background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px; padding: 1.5rem; text-align: center;
        transition: transform .2s, box-shadow .2s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99,102,241,.15);
    }
    .metric-icon { font-size: 1.6rem; }
    .metric-value {
        font-size: 2rem; font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-label { color: #94a3b8; font-size: .85rem; }

    .section-title {
        font-size: 1.3rem; font-weight: 700; color: #e2e8f0;
        margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: .5rem;
    }
    .section-title .line {
        flex: 1; height: 1px;
        background: linear-gradient(90deg, rgba(99,102,241,.4), transparent);
    }

    .ipo-row {
        background: linear-gradient(145deg, #1e1b4b, #1a1a2e);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 14px; padding: 1rem 1.3rem; margin-bottom: .6rem;
        display: flex; align-items: center; justify-content: space-between;
        transition: all .2s;
    }
    .ipo-row:hover {
        border-color: rgba(99,102,241,.35);
        transform: translateX(4px);
    }
    .ipo-row .name { font-weight: 600; color: #e2e8f0; font-size: 1rem; }
    .ipo-row .meta { color: #64748b; font-size: .8rem; }
    .gain-pill {
        font-weight: 700; font-size: 1rem; padding: 5px 14px;
        border-radius: 10px; min-width: 72px; text-align: center;
    }
    .gp { background: rgba(34,197,94,.12); color: #22c55e; }
    .gn { background: rgba(239,68,68,.12); color: #ef4444; }
    .gz { background: rgba(234,179,8,.12); color: #eab308; }

    .badge-main { background: rgba(99,102,241,.18); color: #a78bfa;
                   font-size:.7rem; padding:2px 8px; border-radius:20px; font-weight:600; }
    .badge-sme  { background: rgba(52,211,153,.15); color: #34d399;
                   font-size:.7rem; padding:2px 8px; border-radius:20px; font-weight:600; }

    .app-footer {
        text-align: center; color: #475569; font-size: .78rem;
        padding: 2rem 0 1rem; border-top: 1px solid rgba(255,255,255,.04);
        margin-top: 3rem;
    }

    /* Plotly dark overrides */
    .js-plotly-plot .plotly .modebar { display: none !important; }
    </style>
    """, unsafe_allow_html=True)


PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", family="Inter"),
    title_font=dict(size=18, color="#e2e8f0"),
    title_x=0.5,
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    xaxis=dict(gridcolor="rgba(255,255,255,.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,.04)"),
)

COLORS = ["#a78bfa", "#60a5fa", "#34d399", "#f472b6", "#fbbf24", "#fb923c"]

# ── Fallback Data Generator ─────────────────────────────────────────
def get_fallback_data():
    """Provides sample data if the live scraper fails."""
    data = {
        'Current IPOs': ['Stallion India', 'Hexaware Tech', 'Ajax Engineering', 'Quality Power', 'Indowind Energy'],
        'IPO GMP': [62.5, 35.0, 18.0, -5.0, 0.0],
        'IPO Price': [150, 450, 210, 85, 45],
        'Gain': [62.5, 35.2, 18.7, -5.0, 0.0],
        'Date': ['20-22 Feb', '19-21 Feb', '18-20 Feb', '17-19 Feb', '15-17 Feb'],
        'Type': ['Mainline', 'Mainline', 'SME', 'SME', 'Mainline']
    }
    return pd.DataFrame(data)

# ── Main ────────────────────────────────────────────────────────────
def render_dashboard():
    inject_dashboard_css()

    # ── Sidebar ──────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 📊 Dashboard")
        st.caption("Full analytics & management")
        st.markdown("---")

        st.markdown("### 🎛️ Filters")
        filter_type = st.multiselect(
            "IPO Type", ["Mainline", "SME"], default=["Mainline", "SME"]
        )
        gain_range = st.slider("Gain % Range", -100, 300, (-100, 300), step=5)
        sort_option = st.selectbox(
            "Sort by", ["Gain ↓", "Gain ↑", "Name A-Z", "Name Z-A"]
        )

        st.markdown("---")
        if st.button("🔄 Force Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")
        st.markdown("### 📱 Quick Actions")
        show_subscribe = st.toggle("Show Subscribe Form", value=False)

    # ── Hero ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="dash-hero">
        <h1>📊 IPO Dashboard</h1>
        <p>Comprehensive IPO analytics &amp; monitoring • {datetime.now().strftime('%d %b %Y  •  %I:%M %p')}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load data ────────────────────────────────────────────────
    @st.cache_data(ttl=300, show_spinner=False)
    def load_data():
        try:
            scraper = IPOScraper()
            df = scraper.scrape_ipo_data()
            if df is not None and not df.empty:
                return df
            return None
        except Exception:
            return None

    with st.spinner("Loading IPO data…"):
        df = load_data()

    # ── FALLBACK LOGIC ───────────────────────────────────────────
    if df is None or df.empty:
        st.toast("⚠️ Live data unavailable. Showing sample data.", icon="📡")
        df = get_fallback_data()
    # ─────────────────────────────────────────────────────────────

    # ── Apply filters ────────────────────────────────────────────
    if "Type" in df.columns:
        df = df[df["Type"].isin(filter_type)]
    
    # Safe filtering for Gain
    if "Gain" in df.columns:
        df = df[(df["Gain"] >= gain_range[0]) & (df["Gain"] <= gain_range[1])]

        if sort_option == "Gain ↓":
            df = df.sort_values("Gain", ascending=False)
        elif sort_option == "Gain ↑":
            df = df.sort_values("Gain", ascending=True)
        elif sort_option == "Name A-Z":
            df = df.sort_values("Current IPOs")
        else:
            df = df.sort_values("Current IPOs", ascending=False)

    # ── Save snapshot ────────────────────────────────────────────
    try:
        db = Database()
        db.save_ipo_snapshot(df)
    except Exception:
        pass

    # ── Metrics ──────────────────────────────────────────────────
    _render_metrics(df)

    # ── Charts ───────────────────────────────────────────────────
    _render_charts(df)

    # ── Data tables ──────────────────────────────────────────────
    _render_data_tabs(df)

    # ── Subscribe form ───────────────────────────────────────────
    if show_subscribe:
        _render_subscribe_form()

    # ── Footer ───────────────────────────────────────────────────
    st.markdown("""
    <div class="app-footer">
        Built with ❤️ using Streamlit • Data sourced from public IPO trackers
    </div>
    """, unsafe_allow_html=True)


# ── Metrics ─────────────────────────────────────────────────────────
def _render_metrics(df):
    active = len(df)
    high = int((df["Gain"] >= 50).sum())
    avg = df["Gain"].mean()
    mx = df["Gain"].max()
    neg = int((df["Gain"] < 0).sum())
    best = df.loc[df["Gain"].idxmax(), "Current IPOs"] if not df.empty else "—"

    cols = st.columns(5)
    data = [
        ("🚀", active, "Active IPOs"),
        ("🔥", high, "High Gain ≥50%"),
        ("📊", f"{avg:+.1f}%", "Avg Gain"),
        ("🏆", f"{mx:+.1f}%", best[:16]),
        ("📉", neg, "Negative GMP"),
    ]
    for col, (icon, val, label) in zip(cols, data):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")


# ── Charts ──────────────────────────────────────────────────────────
def _render_charts(df):
    st.markdown(
        '<div class="section-title">📈 Market Analysis <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Top Performers", "📉 Distribution"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            # Horizontal bar chart
            sorted_df = df.sort_values("Gain", ascending=True).tail(10)
            fig = go.Figure(go.Bar(
                x=sorted_df["Gain"],
                y=sorted_df["Current IPOs"],
                orientation="h",
                marker=dict(
                    color=sorted_df["Gain"],
                    colorscale=[[0, "#ef4444"], [0.5, "#eab308"], [1, "#22c55e"]],
                    line=dict(width=0),
                    # cornerradius=6, # Disabled for compatibility
                ),
                text=sorted_df["Gain"].apply(lambda g: f"{g:+.1f}%"),
                textposition="outside",
                textfont=dict(color="#94a3b8", size=11),
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title="Top 10 IPOs by Gain %",
                xaxis_title="Gain %",
                yaxis_title="",
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Pie by type
            type_counts = df["Type"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                hole=0.55,
                marker=dict(colors=COLORS[:len(type_counts)]),
                textinfo="label+percent",
                textfont=dict(color="#e2e8f0"),
            ))
            fig2.update_layout(
                **PLOTLY_LAYOUT,
                title="IPO Type Distribution",
                height=420,
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        top5 = df.nlargest(5, "Gain")
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        cols = st.columns(min(5, len(top5)))
        for i, (_, row) in enumerate(top5.iterrows()):
            with cols[i]:
                g = row["Gain"]
                color = "#22c55e" if g > 0 else "#ef4444"
                st.markdown(f"""
                <div class="metric-card" style="padding:1.2rem;">
                    <div style="font-size:2rem;">{medals[i]}</div>
                    <div style="font-weight:700;color:#e2e8f0;margin:.4rem 0;font-size:.9rem;">
                        {row['Current IPOs'][:20]}
                    </div>
                    <div style="font-size:1.5rem;font-weight:800;color:{color};">
                        {g:+.1f}%
                    </div>
                    <div style="color:#64748b;font-size:.75rem;margin-top:.2rem;">
                        {row.get('Date','—')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            fig3 = px.histogram(
                df, x="Gain", nbins=25,
                color_discrete_sequence=["#a78bfa"],
                title="Gain Distribution",
            )
            fig3.update_layout(**PLOTLY_LAYOUT, height=380)
            st.plotly_chart(fig3, use_container_width=True)

        with c2:
            if "Type" in df.columns and df["Type"].nunique() > 1:
                fig4 = px.box(
                    df, x="Type", y="Gain",
                    color="Type",
                    color_discrete_sequence=COLORS,
                    title="Gain by Category",
                )
                fig4.update_layout(**PLOTLY_LAYOUT, height=380, showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                fig4 = px.violin(
                    df, y="Gain",
                    color_discrete_sequence=["#60a5fa"],
                    title="Gain Spread",
                    box=True,
                )
                fig4.update_layout(**PLOTLY_LAYOUT, height=380)
                st.plotly_chart(fig4, use_container_width=True)


# ── Data tabs ───────────────────────────────────────────────────────
def _render_data_tabs(df):
    st.markdown(
        '<div class="section-title">📋 IPO Details <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    t1, t2, t3 = st.tabs(["🔥 High Gain", "📋 All IPOs", "📉 Negative GMP"])

    with t1:
        hg = df[df["Gain"] >= 50].sort_values("Gain", ascending=False)
        if not hg.empty:
            _render_ipo_cards(hg)
        else:
            st.info("No IPOs with ≥50% gain currently.")

    with t2:
        search = st.text_input("🔍 Search", placeholder="Type IPO name…",
                               label_visibility="collapsed", key="dash_search")
        filtered = df
        if search:
            filtered = df[df["Current IPOs"].str.contains(search, case=False, na=False)]
        _render_ipo_cards(filtered)

        with st.expander("📄 Raw Data Table"):
            st.dataframe(
                filtered.style.format({"Gain": "{:+.1f}%"})
                # .background_gradient(subset=["Gain"], cmap="RdYlGn"),
                use_container_width=True,
                hide_index=True,
            )

    with t3:
        neg = df[df["Gain"] < 0].sort_values("Gain")
        if not neg.empty:
            _render_ipo_cards(neg)
        else:
            st.success("🎉 No IPOs with negative GMP right now!")


def _render_ipo_cards(df):
    """Render IPO data as styled card rows."""
    if df.empty:
        return

    max_abs = max(abs(df["Gain"].max()), abs(df["Gain"].min()), 1)
    html = ""
    for _, row in df.iterrows():
        name = row.get("Current IPOs", "—")
        gain = row.get("Gain", 0)
        date = row.get("Date", "—")
        t = row.get("Type", "Mainline")

        badge_cls = "badge-sme" if t == "SME" else "badge-main"
        if gain > 0:
            gc, gt = "gp", f"+{gain:.1f}%"
        elif gain < 0:
            gc, gt = "gn", f"{gain:.1f}%"
        else:
            gc, gt = "gz", "0.0%"

        bar_w = min(abs(gain) / max_abs * 100, 100)
        bar_c = "#22c55e" if gain > 0 else "#ef4444" if gain < 0 else "#eab308"

        html += f"""
        <div class="ipo-row">
            <div>
                <div class="name">{name}</div>
                <div class="meta">
                    {date} &nbsp;<span class="{badge_cls}">{t}</span>
                </div>
                <div style="background:rgba(255,255,255,.06);border-radius:4px;
                            height:6px;width:140px;margin-top:4px;overflow:hidden;">
                    <div style="height:100%;width:{bar_w}%;background:{bar_c};
                                border-radius:4px;transition:width .5s;"></div>
                </div>
            </div>
            <div class="gain-pill {gc}">{gt}</div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


# ── Subscribe form ──────────────────────────────────────────────────
def _render_subscribe_form():
    st.markdown(
        '<div class="section-title">📱 Subscribe to Alerts <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    db = Database()
    nm = NotificationManager()
    nm.request_push_permission()

    with st.form("dash_subscribe", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", placeholder="Your name")
            phone = st.text_input("WhatsApp Number", placeholder="+919876543210")
        with c2:
            threshold = st.slider("Gain Threshold (%)", 0, 100, 50)
            frequency = st.selectbox("Alert Frequency", ["Immediate", "Daily", "Weekly"])

        st.markdown("**Notification Channels**")
        nc1, nc2 = st.columns(2)
        with nc1:
            wa = st.checkbox("WhatsApp", value=True)
            push = st.checkbox("Browser Push", value=True)
        with nc2:
            st.info("Enable channels to receive IPO alerts")

        submitted = st.form_submit_button("🚀 Subscribe Now", use_container_width=True)

        if submitted:
            if not name or not phone:
                st.error("Please fill in name and phone number.")
                return

            prefs = {
                "gain_threshold": threshold,
                "alert_frequency": frequency,
                "notifications": {"whatsapp": wa, "push": push},
            }
            try:
                result = db.add_subscriber(phone, name, threshold, prefs)

                if result:
                    st.success(f"✅ Welcome, {name}! You're now subscribed.")
                    st.balloons()

                    if wa:
                        r = nm.send_whatsapp_message(
                            phone,
                            f"Welcome to IPO GMP Monitor, {name}! "
                            f"You'll get alerts for IPOs with {threshold}%+ gains.",
                        )
                        if r["status"] == "success":
                            st.toast("✅ WhatsApp connected!", icon="📱")
                        else:
                            st.toast(f"⚠️ WhatsApp: {r['message']}", icon="⚠️")
                else:
                    st.error("Failed to subscribe. Please try again.")
            except Exception as e:
                st.error(f"Subscription failed: {e}")

# ── Entry point ─────────────────────────────────────────────────────
render_dashboard()