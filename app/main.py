# # # main.py
# # import streamlit as st
# # from utils.database import Database

# # # Initialize database
# # db = Database()
# # db.setup_database()

# # # Main app
# # def main():
# #     st.set_page_config(
# #         page_title="IPO Monitor",
# #         page_icon="📈",
# #         layout="wide"
# #     )
    
# #     # Main page navigation handled by Streamlit pages

# # if __name__ == "__main__":
# #     main()

# # app/main.py
# import streamlit as st
# import pandas as pd
# from utils.database import Database
# from utils.scraper import IPOScraper
# from datetime import datetime
# import traceback

# def main():
#     try:
#         st.set_page_config(
#             page_title="IPO Monitor",
#             page_icon="📈",
#             layout="wide",
#             initial_sidebar_state="expanded"
#         )
        
#         # Initialize database with error handling
#         try:
#             db = Database()
#             st.session_state.db = db
#         except Exception as e:
#             st.error(f"Database initialization failed: {str(e)}")
#             st.info("Some features may not work properly. Please check your database configuration.")
#             st.info("The app will continue to work with limited functionality.")
#             db = None
        
#         # Main page content
#         show_main_page()
        
#     except Exception as e:
#         st.error("An unexpected error occurred while loading the application.")
#         st.error(f"Error details: {str(e)}")
#         if st.checkbox("Show technical details"):
#             st.code(traceback.format_exc())

# def show_main_page():
#     """Display the main page content with IPO overview"""
    
#     @st.cache_data(ttl=300)  # Cache for 5 minutes
#     def get_ipo_data():
#         """Cached function to get IPO data"""
#         try:
#             scraper = IPOScraper()
#             return scraper.scrape_ipo_data()
#         except Exception as e:
#             st.error(f"Failed to fetch IPO data: {str(e)}")
#             return None
    
#     # Header
#     st.markdown("""
#     <div style="text-align: center; padding: 2rem 0;">
#         <h1>📈 IPO GMP Monitor</h1>
#         <p style="font-size: 1.2em; color: #666;">Real-time IPO Grey Market Premium Tracking</p>
#         <p style="color: #888;">Last Updated: {}</p>
#     </div>
#     """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
    
#     # Quick navigation
#     import os
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if os.path.exists("pages/1_Dashboard.py"):
#             st.page_link("pages/1_Dashboard.py", label="📊 View Dashboard", use_container_width=True)
#         else:
#             st.error("Dashboard page not found")
#     with col2:
#         if os.path.exists("pages/2_Subscribers.py"):
#             st.page_link("pages/2_Subscribers.py", label="👥 Manage Subscribers", use_container_width=True)
#         else:
#             st.warning("Subscribers page not available")
#     with col3:
#         if os.path.exists("pages/3_Settings.py"):
#             st.page_link("pages/3_Settings.py", label="⚙️ Settings", use_container_width=True)
#         else:
#             st.warning("Settings page not available")
    
#     st.markdown("---")
    
#     # Try to load and display IPO data
#     try:
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             st.markdown("### 📈 Live IPO Data")
#         with col2:
#             if st.button("🔄 Refresh", help="Refresh IPO data"):
#                 st.cache_data.clear()
#                 st.rerun()
        
#         with st.spinner("Loading IPO data..."):
#             df = get_ipo_data()
            
#         if df is not None and not df.empty:
#             # Quick overview metrics
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("Active IPOs", len(df))
                
#             with col2:
#                 high_gain = len(df[df['Gain'] >= 50])
#                 st.metric("High Gain IPOs (≥50%)", high_gain)
                
#             with col3:
#                 avg_gain = df['Gain'].mean()
#                 st.metric("Average Gain", f"{avg_gain:.1f}%")
                
#             with col4:
#                 max_gain = df['Gain'].max()
#                 st.metric("Highest Gain", f"{max_gain:.1f}%")
            
#             # Recent IPOs table
#             st.markdown("### 🔥 Recent IPOs")
#             recent_df = df.head(5)[['Current IPOs', 'Gain', 'Date', 'Type']]
#             st.dataframe(recent_df, use_container_width=True)
            
#             # Top performers
#             if len(df) > 0:
#                 st.markdown("### 🏆 Top Performers")
#                 top_performers = df.nlargest(3, 'Gain')[['Current IPOs', 'Gain']]
#                 for _, row in top_performers.iterrows():
#                     st.markdown(f"**{row['Current IPOs']}**: {row['Gain']:.1f}% gain")
            
#         else:
#             show_fallback_content()
            
#     except Exception as e:
#         st.error("Failed to load IPO data. Showing cached/offline content.")
#         show_fallback_content()
#         if st.checkbox("Show error details"):
#             st.code(f"Error: {str(e)}\n\n{traceback.format_exc()}")

# def show_fallback_content():
#     """Show fallback content when data loading fails"""
    
#     st.warning("⚠️ Unable to fetch live IPO data at the moment.")
    
#     # Sample data for demonstration
#     sample_data = {
#         'Current IPOs': ['Sample IPO 1', 'Sample IPO 2', 'Sample IPO 3'],
#         'Gain': [25.5, 15.2, 8.7],
#         'Date': ['20-22 Feb', '18-20 Feb', '15-17 Feb'],
#         'Type': ['Mainline', 'SME', 'Mainline']
#     }
#     sample_df = pd.DataFrame(sample_data)
    
#     st.markdown("### 📊 Sample IPO Data")
#     st.info("This is sample data for demonstration. Live data will be available when the connection is restored.")
    
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("Active IPOs", len(sample_df))
#     with col2:
#         high_gain = len(sample_df[sample_df['Gain'] >= 20])
#         st.metric("High Gain IPOs (≥20%)", high_gain)
#     with col3:
#         avg_gain = sample_df['Gain'].mean()
#         st.metric("Average Gain", f"{avg_gain:.1f}%")
#     with col4:
#         max_gain = sample_df['Gain'].max()
#         st.metric("Highest Gain", f"{max_gain:.1f}%")
    
#     st.dataframe(sample_df, use_container_width=True)
    
#     # Helpful information
#     st.markdown("### 🔧 Troubleshooting")
#     with st.expander("Why might data loading fail?"):
#         st.markdown("""
#         - **Network connectivity**: Check your internet connection
#         - **Website changes**: The source website may have updated its structure
#         - **Rate limiting**: Too many requests to the source website
#         - **Server issues**: The source website may be temporarily down
#         """)
    
#     with st.expander("How to refresh data?"):
#         st.markdown("""
#         - Go to the Dashboard page for full functionality
#         - Use the refresh button on the Dashboard
#         - Check back later if the issue persists
#         """)

# if __name__ == "__main__":
#     main()

# main.py
import streamlit as st
import pandas as pd
from utils.database import Database
from utils.scraper import IPOScraper
from datetime import datetime
import traceback
import os


# ── Page config (must be first st command) ──────────────────────────
def main():
    try:
        st.set_page_config(
            page_title="IPO GMP Monitor",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        inject_css()

        # Database init
        try:
            db = Database()
            st.session_state.db = db
        except Exception as e:
            st.toast(f"⚠️ DB init failed: {e}", icon="🔴")
            db = None

        show_main_page()

    except Exception as e:
        st.error("An unexpected error occurred while loading the application.")
        st.error(f"Error details: {str(e)}")
        if st.checkbox("Show technical details"):
            st.code(traceback.format_exc())


# ── CSS injection ───────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
    <style>
    /* ── Import font ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default decoration ─────────────────── */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ── Hero banner ─────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px;
        padding: 3rem 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,.06);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,.12) 0%, transparent 60%);
        animation: pulse 6s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: .6; }
        50%      { transform: scale(1.1); opacity: 1; }
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: .4rem;
        position: relative;
    }
    .hero .subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        font-weight: 400;
        position: relative;
    }
    .hero .updated {
        color: #64748b;
        font-size: .82rem;
        margin-top: .8rem;
        position: relative;
    }
    .hero .updated span {
        background: rgba(99,102,241,.18);
        padding: 3px 12px;
        border-radius: 20px;
        color: #a78bfa;
        font-weight: 500;
    }

    /* ── Stat cards ──────────────────────────────── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .stat-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .stat-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #1a1a2e 100%);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform .2s, box-shadow .2s;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99,102,241,.15);
    }
    .stat-icon { font-size: 1.8rem; margin-bottom: .4rem; }
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label { color: #94a3b8; font-size: .85rem; margin-top: .2rem; }

    /* ── Section titles ──────────────────────────── */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: .5rem;
    }
    .section-title .line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(99,102,241,.4), transparent);
    }

    /* ── IPO row cards ───────────────────────────── */
    .ipo-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #1a1a2e 100%);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: .75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all .2s;
    }
    .ipo-card:hover {
        border-color: rgba(99,102,241,.35);
        box-shadow: 0 4px 20px rgba(99,102,241,.1);
        transform: translateX(4px);
    }
    .ipo-name {
        font-weight: 600;
        font-size: 1.05rem;
        color: #e2e8f0;
    }
    .ipo-meta {
        color: #64748b;
        font-size: .82rem;
        margin-top: 2px;
    }
    .ipo-badge {
        font-size: .72rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .5px;
    }
    .badge-main { background: rgba(99,102,241,.18); color: #a78bfa; }
    .badge-sme  { background: rgba(52,211,153,.15); color: #34d399; }
    .gain-pill {
        font-weight: 700;
        font-size: 1.1rem;
        padding: 6px 16px;
        border-radius: 12px;
        min-width: 80px;
        text-align: center;
    }
    .gain-positive { background: rgba(34,197,94,.12); color: #22c55e; }
    .gain-negative { background: rgba(239,68,68,.12); color: #ef4444; }
    .gain-neutral  { background: rgba(234,179,8,.12); color: #eab308; }

    /* ── Nav buttons ─────────────────────────────── */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .nav-grid { grid-template-columns: 1fr; }
    }
    .nav-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #1a1a2e 100%);
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all .25s;
        cursor: pointer;
    }
    .nav-card:hover {
        border-color: rgba(99,102,241,.4);
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(99,102,241,.12);
    }
    .nav-card .nav-icon { font-size: 2rem; margin-bottom: .5rem; }
    .nav-card .nav-label {
        font-weight: 600;
        color: #e2e8f0;
        font-size: 1rem;
    }
    .nav-card .nav-desc {
        color: #64748b;
        font-size: .82rem;
        margin-top: .3rem;
    }

    /* ── Gain bar ────────────────────────────────── */
    .gain-bar-bg {
        background: rgba(255,255,255,.06);
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
        margin-top: 6px;
    }
    .gain-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width .5s ease;
    }

    /* ── Alert banner ────────────────────────────── */
    .alert-banner {
        background: linear-gradient(135deg, rgba(234,179,8,.08), rgba(234,179,8,.03));
        border: 1px solid rgba(234,179,8,.2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: .8rem;
        margin-bottom: 1.5rem;
    }
    .alert-banner .alert-icon { font-size: 1.4rem; }
    .alert-banner .alert-text { color: #fbbf24; font-size: .9rem; }

    /* ── Footer ──────────────────────────────────── */
    .app-footer {
        text-align: center;
        color: #475569;
        font-size: .78rem;
        padding: 2rem 0 1rem;
        border-top: 1px solid rgba(255,255,255,.04);
        margin-top: 3rem;
    }

    /* ── Override Streamlit dataframe ─────────────── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* ── Sidebar polish ──────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e2e8f0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ── Main page ───────────────────────────────────────────────────────
def show_main_page():
    """Display the main page content with IPO overview"""

    @st.cache_data(ttl=300, show_spinner=False)
    def get_sample_data():
        """Return sample IPO data when live data is unavailable"""
        import pandas as pd
        sample_data = {
            'Current IPOs': [
                'Gensol Engineering', 'Prima Industries', 'Sona BLW Precision', 
                'Aether Industries', 'Cochin Shipyard', 'Bharat Petroleum'
            ],
            'IPO GMP': ['₹15', '₹8', '₹25', '₹-2', '₹12', '₹5'],
            'IPO Price': ['₹180', '₹220', '₹650', '₹850', '₹450', '₹320'],
            'Gain': [8.3, 3.6, 3.8, -0.2, 2.7, 1.6],
            'Date': ['25-27 Feb', '24-26 Feb', '23-25 Feb', '20-22 Feb', '18-20 Feb', '15-17 Feb'],
            'Type': ['Mainline', 'Mainline', 'Mainline', 'Mainline', 'Mainline', 'Mainline'],
            'Kostak': ['N/A'] * 6,
            'Subject': ['N/A'] * 6
        }
        return pd.DataFrame(sample_data)

    @st.cache_data(ttl=300, show_spinner=False)
    def get_ipo_data():
        try:
            scraper = IPOScraper()
            df = scraper.scrape_ipo_data()
            if df is not None and not df.empty:
                return df
            else:
                # If scraper fails, use sample data
                st.info("📊 Showing sample IPO data (live data temporarily unavailable)")
                return get_sample_data()
        except Exception as e:
            st.error(f"Scraper Error: {str(e)}") 
            st.info("📊 Showing sample IPO data (live data temporarily unavailable)")
            return get_sample_data()

    # ── Sidebar ──────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 📈 IPO Monitor")
        st.caption("Real-time Grey Market Premium tracker")
        st.markdown("---")

        st.markdown("### ⚡ Quick Links")
        if os.path.exists("pages/1_Dashboard.py"):
            st.page_link("pages/1_Dashboard.py", label="📊 Dashboard", use_container_width=True)
        if os.path.exists("pages/2_Subscribers.py"):
            st.page_link("pages/2_Subscribers.py", label="👥 Subscribers", use_container_width=True)
        if os.path.exists("pages/3_Settings.py"):
            st.page_link("pages/3_Settings.py", label="⚙️ Settings", use_container_width=True)

        st.markdown("---")
        st.markdown("### 🎛️ Controls")
        auto_refresh = st.toggle("Auto-refresh (5 min)", value=False)
        show_sme = st.toggle("Show SME IPOs", value=True)
        min_gain = st.slider("Min Gain %", -100, 200, -100, step=5)
        st.markdown("---")
        st.caption(f"v2.0 • {datetime.now().strftime('%d %b %Y')}")

    # ── Hero ─────────────────────────────────────────────────────
    now_str = datetime.now().strftime("%d %b %Y  •  %I:%M %p")
    st.markdown(
        f"""
    <div class="hero">
        <h1>📈 IPO GMP Monitor</h1>
        <div class="subtitle">Real-time Grey Market Premium Tracking</div>
        <div class="updated">Last updated <span>{now_str}</span></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Navigation cards ─────────────────────────────────────────
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    with nav_col1:
        if os.path.exists("pages/1_Dashboard.py"):
            st.page_link(
                "pages/1_Dashboard.py",
                label="📊  View Full Dashboard",
                use_container_width=True,
            )
        else:
            st.info("📊 Dashboard — coming soon")
    with nav_col2:
        if os.path.exists("pages/2_Subscribers.py"):
            st.page_link(
                "pages/2_Subscribers.py",
                label="👥  Manage Subscribers",
                use_container_width=True,
            )
        else:
            st.info("👥 Subscribers — coming soon")
    with nav_col3:
        if os.path.exists("pages/3_Settings.py"):
            st.page_link(
                "pages/3_Settings.py",
                label="⚙️  Settings & Config",
                use_container_width=True,
            )
        else:
            st.info("⚙️ Settings — coming soon")

    st.markdown("")  # spacer

    # ── Data loading ─────────────────────────────────────────────
    header_l, header_r = st.columns([4, 1])
    with header_l:
        st.markdown(
            '<div class="section-title">📡 Live IPO Data <span class="line"></span></div>',
            unsafe_allow_html=True,
        )
    with header_r:
        if st.button("🔄 Refresh", use_container_width=True, help="Clear cache & reload"):
            st.cache_data.clear()
            st.rerun()

    with st.spinner("Fetching latest IPO data…"):
        df = get_ipo_data()

    if df is not None and not df.empty:
        # ── Apply sidebar filters ────────────────────────────────
        if not show_sme and "Type" in df.columns:
            df = df[df["Type"] != "SME"]
        df = df[df["Gain"] >= min_gain]

        render_metrics(df)
        render_ipo_table(df)
        render_top_performers(df)
    else:
        show_fallback_content()

    # ── Auto-refresh ─────────────────────────────────────────────
    if auto_refresh:
        import time
        time.sleep(300)
        st.cache_data.clear()
        st.rerun()

    # ── Footer ───────────────────────────────────────────────────
    st.markdown(
        """
    <div class="app-footer">
        Built with ❤️ using Streamlit &nbsp;•&nbsp; Data sourced from public IPO trackers
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── Metric cards ────────────────────────────────────────────────────
def render_metrics(df: pd.DataFrame):
    active = len(df)
    high_gain = int((df["Gain"] >= 50).sum())
    avg_gain = df["Gain"].mean()
    max_gain = df["Gain"].max()
    best_name = df.loc[df["Gain"].idxmax(), "Current IPOs"] if not df.empty else "—"

    st.markdown(
        f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-icon">🚀</div>
            <div class="stat-value">{active}</div>
            <div class="stat-label">Active IPOs</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🔥</div>
            <div class="stat-value">{high_gain}</div>
            <div class="stat-label">High Gain (≥50%)</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{avg_gain:+.1f}%</div>
            <div class="stat-label">Average Gain</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">{max_gain:+.1f}%</div>
            <div class="stat-label">{best_name[:18]}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── IPO table (card-style rows) ────────────────────────────────────
def render_ipo_table(df: pd.DataFrame):
    st.markdown(
        '<div class="section-title">📋 All IPOs <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    # Search
    search = st.text_input(
        "🔍", placeholder="Search IPO by name…", label_visibility="collapsed"
    )
    if search:
        df = df[df["Current IPOs"].str.contains(search, case=False, na=False)]

    if df.empty:
        st.info("No IPOs match your search / filter criteria.")
        return

    # Sort
    sort_col1, sort_col2 = st.columns([1, 3])
    with sort_col1:
        sort_by = st.selectbox(
            "Sort by",
            ["Gain ↓", "Gain ↑", "Name A-Z"],
            label_visibility="collapsed",
        )
    if sort_by == "Gain ↓":
        df = df.sort_values("Gain", ascending=False)
    elif sort_by == "Gain ↑":
        df = df.sort_values("Gain", ascending=True)
    else:
        df = df.sort_values("Current IPOs")

    max_abs = max(abs(df["Gain"].max()), abs(df["Gain"].min()), 1)

    cards_html = ""
    for _, row in df.iterrows():
        name = row.get("Current IPOs", "—")
        gain = row.get("Gain", 0)
        date = row.get("Date", "—")
        ipo_type = row.get("Type", "—")

        # Badge
        badge_cls = "badge-sme" if ipo_type == "SME" else "badge-main"
        badge = f'<span class="ipo-badge {badge_cls}">{ipo_type}</span>'

        # Gain pill
        if gain > 0:
            g_cls = "gain-positive"
            g_text = f"+{gain:.1f}%"
        elif gain < 0:
            g_cls = "gain-negative"
            g_text = f"{gain:.1f}%"
        else:
            g_cls = "gain-neutral"
            g_text = "0.0%"

        # Bar
        bar_width = min(abs(gain) / max_abs * 100, 100)
        bar_color = (
            "#22c55e" if gain > 0 else "#ef4444" if gain < 0 else "#eab308"
        )

        cards_html += f"""
        <div class="ipo-card">
            <div>
                <div class="ipo-name">{name}</div>
                <div class="ipo-meta">{date} &nbsp;{badge}</div>
                <div class="gain-bar-bg" style="width:160px;">
                    <div class="gain-bar-fill"
                         style="width:{bar_width}%;background:{bar_color};"></div>
                </div>
            </div>
            <div class="gain-pill {g_cls}">{g_text}</div>
        </div>
        """

    st.markdown(cards_html, unsafe_allow_html=True)

    # Expandable raw table
    with st.expander("📄 View raw data table"):
        st.dataframe(
            df.style.format({"Gain": "{:+.1f}%"}),
            use_container_width=True,
            hide_index=True,
        )


# ── Top performers ──────────────────────────────────────────────────
def render_top_performers(df: pd.DataFrame):
    if len(df) < 1:
        return

    st.markdown(
        '<div class="section-title">🏆 Top Performers <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    top3 = df.nlargest(min(3, len(df)), "Gain")
    medals = ["🥇", "🥈", "🥉"]
    cols = st.columns(min(3, len(top3)))

    for idx, (_, row) in enumerate(top3.iterrows()):
        with cols[idx]:
            gain = row["Gain"]
            color = "#22c55e" if gain > 0 else "#ef4444"
            st.markdown(
                f"""
            <div class="stat-card" style="padding:1.2rem;">
                <div style="font-size:2rem;">{medals[idx]}</div>
                <div style="font-weight:700;color:#e2e8f0;margin:.4rem 0;">
                    {row['Current IPOs'][:22]}
                </div>
                <div style="font-size:1.6rem;font-weight:800;color:{color};">
                    {gain:+.1f}%
                </div>
                <div style="color:#64748b;font-size:.8rem;margin-top:.3rem;">
                    {row.get('Date','—')}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Worst performers (if any negatives)
    negatives = df[df["Gain"] < 0]
    if not negatives.empty:
        st.markdown("")
        with st.expander("📉 Negative GMP IPOs"):
            for _, row in negatives.iterrows():
                st.markdown(
                    f"🔴 **{row['Current IPOs']}** — {row['Gain']:+.1f}%  •  {row.get('Date','—')}"
                )


# ── Fallback content ────────────────────────────────────────────────
def show_fallback_content():
    st.markdown(
        """
    <div class="alert-banner">
        <div class="alert-icon">⚠️</div>
        <div class="alert-text">
            Unable to fetch live IPO data right now.
            Showing sample data for demonstration.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    sample_data = {
        "Current IPOs": [
            "Stallion India Fluorochemicals",
            "Hexaware Technologies",
            "Ajax Engineering",
            "Quality Power Electrical",
            "Indowind Energy",
        ],
        "Gain": [62.5, 35.2, 18.7, -5.0, 0.0],
        "Date": [
            "20-22 Feb",
            "19-21 Feb",
            "18-20 Feb",
            "17-19 Feb",
            "15-17 Feb",
        ],
        "Type": ["Mainline", "Mainline", "SME", "SME", "Mainline"],
    }
    sample_df = pd.DataFrame(sample_data)

    render_metrics(sample_df)
    render_ipo_table(sample_df)
    render_top_performers(sample_df)

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🔧 Troubleshooting <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("❓ Why is data unavailable?", expanded=False):
            st.markdown(
                """
            | Cause | Fix |
            |-------|-----|
            | **No internet** | Check your connection |
            | **Website changed** | Scraper may need updating |
            | **Rate limited** | Wait a few minutes |
            | **Server down** | Try again later |
            """
            )
    with col2:
        with st.expander("🔄 How to refresh?", expanded=False):
            st.markdown(
                """
            1. Click the **🔄 Refresh** button above
            2. Enable **Auto-refresh** in the sidebar
            3. Navigate to the **Dashboard** page
            """
            )


if __name__ == "__main__":
    import os          # ensure import for `os.path.exists` checks
    main()