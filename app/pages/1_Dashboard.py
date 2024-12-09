# pages/1_Dashboard.py
import streamlit as st
import pandas as pd
from utils.scraper import IPOScraper
import plotly.express as px

def render_dashboard():
    st.title("IPO Monitor Dashboard")
    
    # Sidebar controls
    st.sidebar.header("Filters")
    gain_threshold = st.sidebar.slider("Minimum Gain %", 0, 100, 50)
    
    # Get IPO data
    df = IPOScraper.scrape_ipo_data()
    
    if df is not None:
        # High gain IPOs
        high_gain_ipos = df[df['Gain'] >= gain_threshold]
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total IPOs", len(df))
        with col2:
            st.metric("High Gain IPOs", len(high_gain_ipos))
        with col3:
            avg_gain = df['Gain'].mean()
            st.metric("Average Gain", f"{avg_gain:.1f}%")
        
        # Visualization
        fig = px.bar(df, x='Current IPOs', y='Gain',
                    color='Type',
                    title='IPO Gains by Company')
        st.plotly_chart(fig)
        
        # Data tables
        st.subheader("High Gain IPOs")
        st.dataframe(high_gain_ipos)
        
        st.subheader("All IPOs")
        st.dataframe(df)
    else:
        st.error("Error fetching IPO data")