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


# app/main.py
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import traceback

# Import internal modules safely
try:
    from utils.database import Database
except ImportError:
    Database = None

try:
    from utils.scraper import IPOScraper
except ImportError:
    IPOScraper = None


def inject_custom_css():
    """Inject custom CSS for a premium UI look"""
    st.markdown("""
        <style>
        /* Modern Header styling */
        .premium-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .premium-header h1 {
            color: white !important;
            margin: 0;
            font-size: 2.8rem;
            font-weight: 700;
            padding-bottom: 0.5rem;
        }
        .premium-header p {
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .last-updated {
            font-size: 0.85rem !important;
            opacity: 0.7 !important;
            margin-top: 10px !important;
        }
        /* Top performers card styling */
        div {
            background-color: rgba(128, 128, 128, 0.05);
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    try:
        st.set_page_config(
            page_title="IPO GMP Monitor",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        inject_custom_css()
        
        # Initialize database with error handling
        try:
            if Database:
                db = Database()
                st.session_state.db = db
            else:
                db = None
                st.warning("Database module not found.")
        except Exception as e:
            st.error(f"Database initialization failed: {str(e)}")
            st.info("The app will continue to work with limited functionality.")
            db = None
        
        # Main page content
        show_main_page()
        
    except Exception as e:
        st.error("An unexpected error occurred while loading the application.")
        st.error(f"Error details: {str(e)}")
        if st.checkbox("Show technical details"):
            st.code(traceback.format_exc())


def show_main_page():
    """Display the main page content with IPO overview"""
    
    @st.cache_data(ttl=300, show_spinner=False)  # Cache for 5 minutes, custom spinner used below
    def get_ipo_data():
        """Cached function to get IPO data"""
        if not IPOScraper:
            return None
        try:
            scraper = IPOScraper()
            return scraper.scrape_ipo_data()
        except Exception as e:
            # We raise the exception so Streamlit doesn't cache a failed 'None' state
            raise Exception(f"Failed to fetch IPO data: {str(e)}")
    
    # Premium Header
    current_time = datetime.now().strftime('%B %d, %Y • %I:%M %p')
    st.markdown(f"""
    <div class="premium-header">
        <h1>📈 IPO GMP Monitor</h1>
        <p>Real-time IPO Grey Market Premium Tracking</p>
        <p class="last-updated">Last Updated: {current_time}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick navigation (Menu Bar look)
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            if os.path.exists("pages/1_Dashboard.py"):
                st.page_link("pages/1_Dashboard.py", label="📊 **View Dashboard**", use_container_width=True)
            else:
                st.error("Dashboard page not found")
        with col2:
            if os.path.exists("pages/2_Subscribers.py"):
                st.page_link("pages/2_Subscribers.py", label="👥 **Manage Subscribers**", use_container_width=True)
            else:
                st.warning("Subscribers page not available")
        with col3:
            if os.path.exists("pages/3_Settings.py"):
                st.page_link("pages/3_Settings.py", label="⚙️ **Settings**", use_container_width=True)
            else:
                st.warning("Settings page not available")
    
    st.write("") # Spacer
    
    # Try to load and display IPO data
    try:
        col_title, col_btn = st.columns()
        with col_title:
            st.markdown("### 📡 Live Market Data")
        with col_btn:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with st.spinner("Fetching latest Grey Market Premiums..."):
            df = None
            try:
                df = get_ipo_data()
            except Exception as e:
                st.error(str(e))
            
        if df is not None and not df.empty:
            
            # Ensure Gain is numeric for calculations
            df = pd.to_numeric(df, errors='coerce').fillna(0)
            
            # Quick overview metrics inside a styled container
            with st.container(border=True):
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    st.metric("Active IPOs", len(df))
                with m2:
                    high_gain = len(df >= 50])
                    st.metric("High Gain (≥50%)", high_gain, "Hot 🔥" if high_gain > 0 else None)
                with m3:
                    avg_gain = df.mean()
                    st.metric("Average Gain", f"{avg_gain:.1f}%")
                with m4:
                    max_gain = df.max()
                    st.metric("Highest Gain", f"{max_gain:.1f}%")
            
            st.write("") # Spacer

            # Main Layout: Table on left, Top Performers on right
            left_col, right_col = st.columns()
            
            with left_col:
                st.markdown("#### 🔥 Recent IPOs")
                recent_df = df.head(10)[]
                
                # Advanced Dataframe display with progress bars
                st.dataframe(
                    recent_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Current IPOs": st.column_config.TextColumn("Company Name", width="medium"),
                        "Gain": st.column_config.ProgressColumn(
                            "GMP Gain %",
                            help="Current Grey Market Premium Percentage",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100,
                        ),
                        "Date": st.column_config.TextColumn("Timeline"),
                        "Type": st.column_config.TextColumn("Category"),
                    }
                )
            
            with right_col:
                st.markdown("#### 🏆 Top Performers")
                if len(df) > 0:
                    top_performers = df.nlargest(4, 'Gain')]
                    for _, row in top_performers.iterrows():
                        # Displaying as interactive-looking metric cards
                        st.metric(
                            label=row, 
                            value=f"{row:.1f}%", 
                            delta="High Demand" if row >= 40 else "Steady"
                        )
                else:
                    st.info("Not enough data to determine top performers.")
            
        else:
            show_fallback_content()
            
    except Exception as e:
        show_fallback_content()
        if st.checkbox("Show exact error details (for debugging)"):
            st.error(f"Error: {str(e)}")
            st.code(traceback.format_exc())

def show_fallback_content():
    """Show fallback content when data loading fails but keep it looking professional"""
    
    st.warning("⚠️ **Live data feed temporarily unavailable.** Showing demonstration data below.")
    
    # Sample data for demonstration
    sample_data = {
        'Current IPOs':,
        'Gain':,
        'Date':,
        'Type':
    }
    sample_df = pd.DataFrame(sample_data)
    
    with st.container(border=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active IPOs (Demo)", len(sample_df))
        m2.metric("High Gain IPOs", len(sample_df >= 20]))
        m3.metric("Average Gain", f"{sample_df.mean():.1f}%")
        m4.metric("Highest Gain", f"{sample_df.max():.1f}%")
    
    st.write("")
    
    left_col, right_col = st.columns()
    with left_col:
        st.markdown("#### 📊 Sample Data Grid")
        st.dataframe(
            sample_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Current IPOs": st.column_config.TextColumn("Company Name", width="medium"),
                "Gain": st.column_config.ProgressColumn(
                    "GMP Gain %",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                )
            }
        )
        
    with right_col:
        st.markdown("#### 🔧 Troubleshooting")
        with st.expander("Why am I seeing this?", expanded=True):
            st.markdown("""
            - **Scraper Blocked**: Target website may have rate-limited your IP.
            - **Network Issue**: Your server lacks internet access.
            - **Layout Changed**: Target website updated its HTML/CSS structure.
            """)
        if st.button("🔄 Try Fetching Again", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

if __name__ == "__main__":
    main()