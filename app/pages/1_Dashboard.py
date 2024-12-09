# # pages/1_Dashboard.py
# import streamlit as st
# import pandas as pd
# from utils.scraper import IPOScraper
# import plotly.express as px

# def render_dashboard():
#     st.title("IPO Monitor Dashboard")
    
#     # Sidebar controls
#     st.sidebar.header("Filters")
#     gain_threshold = st.sidebar.slider("Minimum Gain %", 0, 100, 50)
    
#     # Get IPO data
#     df = IPOScraper.scrape_ipo_data()
    
#     if df is not None:
#         # High gain IPOs
#         high_gain_ipos = df[df['Gain'] >= gain_threshold]
        
#         # Display stats
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Total IPOs", len(df))
#         with col2:
#             st.metric("High Gain IPOs", len(high_gain_ipos))
#         with col3:
#             avg_gain = df['Gain'].mean()
#             st.metric("Average Gain", f"{avg_gain:.1f}%")
        
#         # Visualization
#         fig = px.bar(df, x='Current IPOs', y='Gain',
#                     color='Type',
#                     title='IPO Gains by Company')
#         st.plotly_chart(fig)
        
#         # Data tables
#         st.subheader("High Gain IPOs")
#         st.dataframe(high_gain_ipos)
        
#         st.subheader("All IPOs")
#         st.dataframe(df)
#     else:
#         st.error("Error fetching IPO data")

# pages/1_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.scraper import IPOScraper

def render_dashboard():
    st.set_page_config(layout="wide")
    
    # Main title with styling
    st.markdown("""
    <div style='text-align: center'>
        <h1>📈 IPO GMP Monitor Dashboard</h1>
        <p style='color: gray'>Live IPO Grey Market Premium Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    gain_threshold = st.sidebar.slider("Minimum Gain %", 0, 100, 50)
    ipo_type = st.sidebar.multiselect(
        "IPO Type",
        ["Mainboard", "NSE SME", "BSE SME"],
        default=["Mainboard", "NSE SME", "BSE SME"]
    )
    
    # Get IPO data
    df = IPOScraper.scrape_ipo_data()
    
    if df is not None:
        # Filter data based on selections
        filtered_df = df[df['Type'].isin(ipo_type)]
        high_gain_ipos = filtered_df[filtered_df['Gain'] >= gain_threshold]
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Active IPOs",
                len(filtered_df),
                delta=f"{len(high_gain_ipos)} High Gain"
            )
        with col2:
            avg_gain = filtered_df['Gain'].mean()
            st.metric(
                "Average Gain",
                f"{avg_gain:.1f}%",
                delta=f"{avg_gain - 50:.1f}% vs Target"
            )
        with col3:
            max_gain = filtered_df['Gain'].max()
            st.metric(
                "Highest Gain",
                f"{max_gain:.1f}%",
                delta="Current Best"
            )
        with col4:
            total_subscription = len(filtered_df[filtered_df['Gain'] > 0])
            st.metric(
                "Positive GMP IPOs",
                total_subscription,
                delta=f"{(total_subscription/len(filtered_df)*100):.1f}%"
            )
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 GMP Distribution by Type")
            fig1 = px.box(filtered_df, x='Type', y='Gain',
                         color='Type',
                         title='IPO Gain Distribution by Category')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Top Performers")
            top_performers = filtered_df.nlargest(5, 'Gain')
            fig2 = go.Figure(data=[
                go.Bar(
                    x=top_performers['Current IPOs'],
                    y=top_performers['Gain'],
                    marker_color='lightgreen'
                )
            ])
            fig2.update_layout(title='Top 5 IPOs by Gain %')
            st.plotly_chart(fig2, use_container_width=True)
        
        # High Gain IPO Alerts
        st.subheader("🚨 High Gain IPO Alerts")
        if not high_gain_ipos.empty:
            for _, ipo in high_gain_ipos.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2,1,1])
                    with col1:
                        st.markdown(f"**{ipo['Current IPOs']}**")
                    with col2:
                        st.markdown(f"Gain: **{ipo['Gain']}%**")
                    with col3:
                        st.markdown(f"Type: *{ipo['Type']}*")
        else:
            st.info("No IPOs currently meet the gain threshold criteria")
        
        # Detailed Data Tables
        tab1, tab2 = st.tabs(["📈 High Gain IPOs", "📋 All IPOs"])
        
        with tab1:
            if not high_gain_ipos.empty:
                st.dataframe(
                    high_gain_ipos,
                    column_config={
                        "Current IPOs": "Company",
                        "IPO GMP": st.column_config.NumberColumn(
                            "GMP (₹)",
                            format="₹%d"
                        ),
                        "Gain": st.column_config.NumberColumn(
                            "Gain %",
                            format="%d%%"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No high gain IPOs found")
        
        with tab2:
            st.dataframe(
                filtered_df,
                column_config={
                    "Current IPOs": "Company",
                    "IPO GMP": st.column_config.NumberColumn(
                        "GMP (₹)",
                        format="₹%d"
                    ),
                    "Gain": st.column_config.NumberColumn(
                        "Gain %",
                        format="%d%%"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Add last updated timestamp
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("Error fetching IPO data. Please try again later.")

if __name__ == "__main__":
    render_dashboard()